"""Constrained HTML page -> native scene records (``engine design html-import``).

The host model designs a page in a restricted HTML/CSS subset because browsers give it real grid/flex
layout and real text measurement. This fixed tool renders that page in a headless Chromium browser,
reads the computed geometry with a tool-owned extractor, and compiles it into the ordinary declarative
scene (text, shape, path, table and chart nodes plus content records). Build, render, review and delivery
gates are unchanged: HTML never reaches the PPTX, and task-authored scripts never run.
"""
from __future__ import annotations

import html as html_lib
import io
import json
import math
import os
import re
import shutil
import sys
import tempfile
from decimal import Decimal, InvalidOperation
from pathlib import Path

from lxml import html as lxml_html
from PIL import Image

from ..source_doc import normalize_text
from .contract import validate, walk
from .html_chart import native_chart_options, parse_chart, validate_chart
from .runtime import ProcessFailed, run_process
from .store import DesignError, canonical, digest

MAX_HTML = 2 * 1024 * 1024
EXTRACTOR = Path(__file__).with_name("html_extract.js")
FORBIDDEN_TAGS = {"script", "iframe", "frame", "frameset", "object", "embed", "applet", "link", "img", "picture",
                  "video", "audio", "source", "track", "canvas", "form", "input", "button", "select", "textarea",
                  "base", "portal", "math", "template", "noscript", "foreignobject", "use", "image"}
FORBIDDEN_ATTRS = {"src", "href", "xlink:href", "srcset", "action", "formaction", "poster", "background", "ping"}
FORBIDDEN_CSS = re.compile(r"url\s*\(|@import|@font-face|expression\s*\(|javascript:|behavior\s*:|-moz-binding", re.I)
CJK_HINT = re.compile(r"CJK|SC\b|TC\b|JP\b|KR\b|Han|Hei|Song|Kai|Ming|YaHei|PingFang|Hiragino|微软|雅黑|苹方|黑体|宋体|思源|"
                      r"Noto Sans SC|Noto Serif SC|Source Han|HarmonyOS|MiSans|Alibaba|SimSun|DengXian|"
                      r"WenQuanYi|LXGW|等线|等線|文泉驿|文泉驛|霞鹜|霞鶩", re.I)
DECOR = re.compile(r"[\s ·•↳→←⇄⟶⚠①②③④⑤⑥⑦⑧⑨⑩▶▸►✓✔✗×|｜]+")
AUTHORED = {
    "wording": "model-authored wording; basis recorded in page-plan.md (numbers must come from the source)",
    "derived": "derived values; calculation recorded in page-plan.md",
    "nav": "navigation label (section, page number or running header)",
}
BROWSER_CANDIDATES = (
    "chrome-headless-shell", "chromium-headless-shell",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge", "microsoft-edge",
)
MAC_BROWSERS = ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Chromium.app/Contents/MacOS/Chromium",
                "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge")
MAC_SANDBOX_PARAMETER_FAILURE = re.compile(
    r"FATAL:[^\r\n]*sandbox_parameters_mac\.mm:\d+\][^\r\n]*Input/output error \(5\)", re.I
)


# ---------------------------------------------------------------- policy

def check_policy(text: str):
    """Reject active content and external resources before any browser sees the file."""
    if len(text.encode("utf-8")) > MAX_HTML:
        raise DesignError("HTML_TOO_LARGE")
    if FORBIDDEN_CSS.search(text):
        raise DesignError("HTML_EXTERNAL_OR_ACTIVE_CSS_FORBIDDEN: url(), @import, @font-face and scripts are not allowed")
    try:
        root = lxml_html.document_fromstring(text)
    except Exception as exc:  # lxml raises several parser types
        raise DesignError(f"HTML_PARSE_FAILED: {exc}") from exc
    for el in root.iter():
        if not isinstance(el.tag, str):
            continue
        tag = el.tag.lower().split("}")[-1]
        if tag in FORBIDDEN_TAGS:
            raise DesignError(f"HTML_TAG_FORBIDDEN: <{tag}>")
        if tag == "meta" and el.get("http-equiv"):
            raise DesignError("HTML_META_REFRESH_FORBIDDEN")
        if "data-chart" in el.attrib:
            parse_chart(el.get("data-chart"))
        for name, value in el.attrib.items():
            low = name.lower()
            if low.startswith("on") or low in FORBIDDEN_ATTRS or "javascript:" in str(value).lower():
                raise DesignError(f"HTML_ATTRIBUTE_FORBIDDEN: {name}")
    slides = root.xpath('//*[@id="slide"]')
    if len(slides) != 1:
        raise DesignError("HTML_SLIDE_ROOT_REQUIRED: exactly one element with id=\"slide\"")
    return {"status": "passed", "sha256": digest(text.encode("utf-8")), "assets": _asset_refs(root)}


# ---------------------------------------------------------------- browser

def _playwright_headless_shell():
    """Locate a cached Playwright chrome-headless-shell binary when installed locally."""
    roots = []
    if sys.platform == "darwin":
        roots.append(Path.home() / "Library" / "Caches" / "ms-playwright")
    elif os.name == "nt":
        local = os.environ.get("LOCALAPPDATA")
        if local:
            roots.append(Path(local) / "ms-playwright")
    else:
        roots.append(Path.home() / ".cache" / "ms-playwright")
    exe = "chrome-headless-shell.exe" if os.name == "nt" else "chrome-headless-shell"
    for cache in roots:
        if not cache.is_dir():
            continue
        for shell_dir in sorted(cache.glob("chromium_headless_shell-*"), reverse=True):
            for candidate in sorted(shell_dir.glob(f"*/{exe}")):
                if candidate.is_file():
                    return str(candidate.absolute())
    return None


def find_browser():
    explicit = os.environ.get("PPTSMITH_BROWSER")
    if explicit:
        path = Path(explicit).expanduser()
        return str(path.absolute()) if path.is_file() else None
    for name in BROWSER_CANDIDATES:
        path = shutil.which(name)
        if path:
            return str(Path(path).absolute())
    pw_shell = _playwright_headless_shell()
    if pw_shell:
        return pw_shell
    for path in MAC_BROWSERS:
        if Path(path).is_file():
            return path
    if os.name == "nt":
        for key in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA"):
            for rel in ("Google/Chrome/Application/chrome.exe", "Microsoft/Edge/Application/msedge.exe"):
                p = Path(os.environ.get(key, "")) / rel
                if os.environ.get(key) and p.is_file():
                    return str(p)
    return None


def _browser_args(browser, root, width, height):
    args = [browser, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
            "--no-default-browser-check", "--disable-extensions", "--disable-background-networking",
            "--disable-sync", "--disable-component-update", "--mute-audio", "--host-resolver-rules=MAP * ~NOTFOUND",
            "--disable-crash-reporter", f"--crash-dumps-dir={root / 'crash'}",
            f"--user-data-dir={root / 'profile'}", f"--window-size={int(round(width))},{int(round(height))}"]
    if sys.platform == "darwin":
        # A fresh profile can still query the login keychain during Chrome startup.
        args.append("--use-mock-keychain")
    if hasattr(os, "geteuid") and os.geteuid() == 0:
        args.append("--no-sandbox")  # Chromium refuses to start as root otherwise (CI containers).
    return args


def _browser_environment(root, *, isolate_home=False):
    env = {k: v for k, v in os.environ.items() if k in {
        "PATH", "USER", "LANG", "LC_ALL", "SystemRoot", "WINDIR", "FONTCONFIG_PATH", "FONTCONFIG_FILE", "XDG_DATA_DIRS"}}
    directories = {"XDG_CONFIG_HOME": "config", "XDG_CACHE_HOME": "cache",
                   "TMPDIR": "tmp", "TMP": "tmp", "TEMP": "tmp"}
    if sys.platform == "darwin" and not isolate_home:
        # macOS resolves user services under HOME, including the default keychain.
        # Keep that identity intact; the browser profile, crash data and caches are private.
        if "HOME" in os.environ:
            env["HOME"] = os.environ["HOME"]
    else:
        directories["HOME"] = "home"
    if os.name == "nt":
        directories.update(USERPROFILE="home", APPDATA="roaming", LOCALAPPDATA="local")
    for key, name in directories.items():
        directory = root / name
        directory.mkdir(exist_ok=True)
        env[key] = str(directory)
    (root / "crash").mkdir(exist_ok=True)
    return env


def _run_browser_once(args, root, timeout, env):
    try:
        return run_process(args, cwd=root, timeout=timeout, env=env), None
    except FileNotFoundError as exc:
        raise DesignError(f"HTML_BROWSER_NOT_FOUND: {exc}") from exc
    except PermissionError as exc:
        raise DesignError(f"HTML_BROWSER_PERMISSION_DENIED: {exc}") from exc
    except ProcessFailed as exc:
        # Some Chrome builds abort during shutdown after flushing both outputs. Require
        # that specific diagnostic AND the same DOM and PNG checks used on clean exits.
        if exc.returncode == 2 and b"Teardown watchdog expired;" in exc.stderr:
            return (exc.stdout.decode("utf-8", "replace"),
                    {"exit_code": 2, "detail": "Chrome teardown watchdog expired after rendering"})
        stderr = exc.stderr.decode("utf-8", "replace")
        mac_sandbox_error = MAC_SANDBOX_PARAMETER_FAILURE.search(stderr)
        if mac_sandbox_error:
            # Preserve this line even when ProcessFailed truncates later stderr.
            raise DesignError(f"HTML_BROWSER_SANDBOX_BLOCKED: {mac_sandbox_error.group(0)}") from exc
        if re.search(r"operation not permitted|permission denied|access is denied|no usable sandbox", stderr, re.I):
            raise DesignError(f"HTML_BROWSER_SANDBOX_BLOCKED: {exc}") from exc
        raise DesignError(f"HTML_BROWSER_LAUNCH_FAILED: {exc}") from exc
    except (OSError, DesignError) as exc:
        code = "HTML_BROWSER_TIMEOUT" if str(exc) == "PROCESS_TIMEOUT" else "HTML_BROWSER_LAUNCH_FAILED"
        raise DesignError(f"{code}: {exc}") from exc


def render_layout(text: str, width: float, height: float, *, browser=None, screenshot_scale=1.5, timeout=90, inject=""):
    """Return (layout dict, preview PNG bytes) for policy-checked HTML.

    ``inject`` is tool-owned CSS (registered asset previews) added after the policy check.
    """
    browser = browser or find_browser()
    if not browser:
        explicit = os.environ.get("PPTSMITH_BROWSER")
        if explicit:
            raise DesignError(f"HTML_BROWSER_OVERRIDE_INVALID: PPTSMITH_BROWSER does not point to an existing file: {explicit}")
        raise DesignError("HTML_BROWSER_NOT_FOUND: install Chrome/Chromium/Edge or set PPTSMITH_BROWSER")
    with tempfile.TemporaryDirectory(prefix="pptsmith-html-") as tmp:
        root = Path(tmp)
        extractor = "pptsmith-extract-" + digest(EXTRACTOR.read_bytes())[:12] + ".js"
        shutil.copyfile(EXTRACTOR, root / extractor)
        tag = (f"<style>{inject}</style>" if inject else "") + f'<script src="{extractor}"></script>'
        page = re.sub(r"</body\s*>", tag + "</body>", text, count=1, flags=re.I) if re.search(r"</body\s*>", text, re.I) else text + tag
        (root / "page.html").write_text(page, encoding="utf-8")
        url = (root / "page.html").as_uri()
        shot = root / "preview.png"
        args = _browser_args(browser, root, width, height) + [
            f"--force-device-scale-factor={screenshot_scale}", "--virtual-time-budget=8000", "--dump-dom",
            f"--screenshot={shot}", url]
        env = _browser_environment(root)
        try:
            dom, teardown_warning = _run_browser_once(args, root, timeout, env)
        except DesignError as exc:
            # A private HOME can help with Crashpad setup. It cannot restore
            # access to the macOS user directories resolved by the OS itself.
            if (sys.platform == "darwin" and str(exc).startswith("HTML_BROWSER_SANDBOX_BLOCKED:")
                    and not MAC_SANDBOX_PARAMETER_FAILURE.search(str(exc))):
                dom, teardown_warning = _run_browser_once(args, root, timeout, _browser_environment(root, isolate_home=True))
            else:
                raise
        try:
            png = shot.read_bytes()
            with Image.open(io.BytesIO(png), formats=["PNG"]) as preview:
                preview.verify()
        except (OSError, SyntaxError) as exc:
            raise DesignError("HTML_BROWSER_PREVIEW_FAILED: expected a valid PNG screenshot") from exc
    m = re.search(r'<pre id="__pptsmith_layout"[^>]*>(.*?)</pre>', dom, re.S)
    if not m:
        raise DesignError("HTML_LAYOUT_EXTRACTION_FAILED: extractor produced no output")
    try:
        layout = json.loads(html_lib.unescape(m.group(1)))
    except ValueError as exc:
        raise DesignError("HTML_LAYOUT_EXTRACTION_FAILED: extractor returned invalid JSON") from exc
    if not isinstance(layout, dict):
        raise DesignError("HTML_LAYOUT_EXTRACTION_FAILED: invalid layout record")
    if layout.get("error"):
        raise DesignError("HTML_" + layout["error"])
    if not isinstance(layout.get("items"), list) or not all(isinstance(layout.get(k), (int, float)) for k in ("width", "height")):
        raise DesignError("HTML_LAYOUT_EXTRACTION_FAILED: missing layout dimensions or items")
    if abs(layout["width"] - width) > 0.5 or abs(layout["height"] - height) > 0.5:
        raise DesignError(f"HTML_SLIDE_SIZE_MISMATCH: #slide is {layout['width']:.0f}x{layout['height']:.0f}px, "
                          f"canvas is {width:.0f}x{height:.0f}pt (1 CSS px = 1 pt)")
    if teardown_warning:
        layout["browser_exit_warning"] = teardown_warning
    return layout, png


def browser_capabilities():
    """Exercise the same layout extractor and screenshot path as a page import."""
    page = ('<!DOCTYPE html><html><body style="margin:0"><div id="slide" style="width:320px;height:180px">'
            '<p>pptsmith-probe</p></div></body></html>')
    browser = find_browser()
    try:
        layout, _ = render_layout(page, 320, 180, browser=browser, timeout=20)
        if not any(run["text"] == "pptsmith-probe" for item in layout["items"] for run in item.get("runs", [])):
            raise DesignError("HTML_LAYOUT_EXTRACTION_FAILED: probe text was not measured")
    except DesignError as exc:
        reason, _, detail = str(exc).partition(": ")
        result = {"available": False, "reason": reason, "detail": detail}
        if browser:
            result["browser"] = browser
        if reason == "HTML_BROWSER_NOT_FOUND":
            result["missing"] = "Chrome/Chromium/Edge or PPTSMITH_BROWSER"
        elif reason == "HTML_BROWSER_OVERRIDE_INVALID":
            result["next_action"] = "Fix or unset PPTSMITH_BROWSER so it points to a valid Chrome/Chromium/Edge binary."
        elif reason == "HTML_BROWSER_SANDBOX_BLOCKED":
            if (MAC_SANDBOX_PARAMETER_FAILURE.search(detail)
                    or re.search(r"sandbox initialization failed|GPU process isn't usable|no usable sandbox", detail, re.I)):
                result["cause"] = "nested_browser_sandbox_blocked"
                result["next_action"] = ("If host policy permits, rerun `engine design capabilities` and "
                                         "`engine design html-import` using the host's approved execution path "
                                         "without the outer sandbox. Keep Chromium's own sandbox enabled. "
                                         "If host execution is unavailable, use `engine design author`.")
            else:
                result["cause"] = "browser_permission_blocked"
                result["next_action"] = "Check browser binary permissions or fall back to `engine design author`."
        return result
    except OSError as exc:
        result = {"available": False, "reason": "HTML_BROWSER_PROBE_IO_FAILED", "detail": str(exc)}
        if browser:
            result["browser"] = browser
        return result
    result = {"available": True}
    if browser:
        result["browser"] = browser
    if "browser_exit_warning" in layout:
        result["warning"] = layout["browser_exit_warning"]
    return result


# ---------------------------------------------------------------- conversion helpers

def _rgba(value):
    m = re.match(r"rgba?\(([^)]+)\)", value or "")
    if not m:
        return None, 1.0
    parts = [float(x) for x in re.split(r"[,\s/]+", m.group(1).strip()) if x]
    alpha = parts[3] if len(parts) > 3 else 1.0
    return "%02X%02X%02X" % tuple(max(0, min(255, round(v))) for v in parts[:3]), alpha


def _font(run, canvas_min=6):
    color, _ = _rgba(run["color"])
    stack = run["stack"] or ["Arial"]
    family = stack[0]
    spec = {"family": family, "size": max(canvas_min, round(run["size"], 2)), "color": color or "000000",
            "bold": run["weight"] >= 600, "italic": bool(run["italic"])}
    if not CJK_HINT.search(family):
        ea = next((f for f in stack[1:] if CJK_HINT.search(f)), None)
        if ea:
            spec["ea_family"] = ea
    return spec


def _clamp_box(x, y, w, h, cw, ch):
    x, y = max(0.0, x), max(0.0, y)
    w, h = max(0.1, min(w, cw - x)), max(0.1, min(h, ch - y))
    return {"x": round(x, 2), "y": round(y, 2), "width": round(w, 2), "height": round(h, 2)}


def _clamp_radii(w, h, radii):
    """Normalize CSS corner radii [tl, tr, br, bl] according to the CSS border-radius scaling rule."""
    tl, tr, br, bl = [max(0.0, float(v)) for v in radii]
    factors = [1.0]
    for total, limit in ((tl + tr, w), (bl + br, w), (tl + bl, h), (tr + br, h)):
        if total > 0:
            factors.append(limit / total)
    scale = min(factors)
    return [v * scale for v in (tl, tr, br, bl)]


def _asymmetric_rounded_path(w, h, radii):
    """Build exact cubic-Bezier path commands inside [0, w] x [0, h] for independent corner radii."""
    tl, tr, br, bl = _clamp_radii(w, h, radii)
    k = 4 * (math.sqrt(2) - 1) / 3

    def pt(px, py):
        return [round(min(w, max(0.0, px)), 3), round(min(h, max(0.0, py)), 3)]

    cmds = [{"op": "M", "points": [pt(tl, 0)]}, {"op": "L", "points": [pt(w - tr, 0)]}]
    if tr > 0.1:
        cmds.append({"op": "C", "points": [pt(w - tr * (1 - k), 0), pt(w, tr * (1 - k)), pt(w, tr)]})
    cmds.append({"op": "L", "points": [pt(w, h - br)]})
    if br > 0.1:
        cmds.append({"op": "C", "points": [pt(w, h - br * (1 - k)), pt(w - br * (1 - k), h), pt(w - br, h)]})
    cmds.append({"op": "L", "points": [pt(bl, h)]})
    if bl > 0.1:
        cmds.append({"op": "C", "points": [pt(bl * (1 - k), h), pt(0, h - bl * (1 - k)), pt(0, h - bl)]})
    cmds.append({"op": "L", "points": [pt(0, tl)]})
    if tl > 0.1:
        cmds.append({"op": "C", "points": [pt(0, tl * (1 - k)), pt(tl * (1 - k), 0), pt(tl, 0)]})
    cmds.append({"op": "Z", "points": []})
    return cmds


def _rounded_polygon(x, y, w, h, r, steps=36):
    """Outline of a rounded rectangle; ``r`` may be a uniform scalar or [tl, tr, br, bl]."""
    tl, tr, br, bl = _clamp_radii(w, h, r if isinstance(r, (list, tuple)) else [r, r, r, r])
    if max(tl, tr, br, bl) < 0.5:
        return [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
    pts = []
    corners = (
        (x + w - tr, y + tr, tr, -90),
        (x + w - br, y + h - br, br, 0),
        (x + bl, y + h - bl, bl, 90),
        (x + tl, y + tl, tl, 180),
    )
    for cx, cy, rad, start in corners:
        if rad < 0.5:
            pts.append((cx, cy))
            continue
        for i in range(steps + 1):
            a = math.radians(start + 90 * i / steps)
            pts.append((cx + rad * math.cos(a), cy + rad * math.sin(a)))
    return pts


def _clip_polygon(points, x0, y0, x1, y1):
    """Sutherland-Hodgman clip of a polygon to an axis-aligned rectangle."""
    def clip(pts, inside, cross):
        out = []
        for i, cur in enumerate(pts):
            prev = pts[i - 1]
            if inside(cur):
                if not inside(prev):
                    out.append(cross(prev, cur))
                out.append(cur)
            elif inside(prev):
                out.append(cross(prev, cur))
        return out

    def at_x(xv):
        return lambda p, q: (xv, p[1] + (q[1] - p[1]) * (xv - p[0]) / ((q[0] - p[0]) or 1e-9))

    def at_y(yv):
        return lambda p, q: (p[0] + (q[0] - p[0]) * (yv - p[1]) / ((q[1] - p[1]) or 1e-9), yv)

    for inside, cross in ((lambda p: p[0] >= x0, at_x(x0)), (lambda p: p[0] <= x1, at_x(x1)),
                          (lambda p: p[1] >= y0, at_y(y0)), (lambda p: p[1] <= y1, at_y(y1))):
        points = clip(points, inside, cross)
        if not points:
            break
    return points


def _norm(text):
    return DECOR.sub("", text or "")


PATH_TOKENS = re.compile(r"[a-zA-Z]|[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?")


def _parse_path(d, sx, sy):
    data = (d or "").strip()
    tokens, end = [], 0
    for match in PATH_TOKENS.finditer(data):
        separator = data[end:match.start()].strip(" \t\r\n")
        token = match.group()
        if separator and (separator != "," or not tokens or tokens[-1].isalpha() or token.isalpha()):
            raise DesignError("SVG_PATH_SYNTAX_INVALID")
        tokens.append(token)
        if len(tokens) > 512 * 7:
            raise DesignError("SVG_PATH_COMMAND_LIMIT")
        end = match.end()
    if data[end:].strip():
        raise DesignError("SVG_PATH_SYNTAX_INVALID")
    if not tokens or tokens[0] not in ("M", "m"):
        raise DesignError("SVG_PATH_MUST_START_WITH_M")
    counts = {"M": 2, "L": 2, "H": 1, "V": 1, "Q": 4, "C": 6, "Z": 0}
    cmds, i, command = [], 0, None
    x = y = start_x = start_y = 0.0
    while i < len(tokens):
        if tokens[i].isalpha():
            command = tokens[i]
            i += 1
        if command is None:
            raise DesignError("SVG_PATH_COMMAND_REQUIRED")
        op = command.upper()
        if op not in counts:
            raise DesignError(f"SVG_PATH_COMMAND_UNSUPPORTED: {command} (use M/L/H/V/Q/C/Z or their lowercase forms)")
        n = counts[op]
        args = tokens[i:i + n]
        if len(args) != n or any(v.isalpha() for v in args):
            raise DesignError("SVG_PATH_ARITY_INVALID")
        vals = [float(v) for v in args]
        i += n
        dx, dy = (x, y) if command.islower() else (0, 0)
        if op == "H":
            points = [(vals[0] + dx, y)]
            op = "L"
        elif op == "V":
            points = [(x, vals[0] + dy)]
            op = "L"
        else:
            points = [(vx + dx, vy + dy) for vx, vy in zip(vals[::2], vals[1::2])]
        if points:
            x, y = points[-1]
        if op == "M":
            start_x, start_y = x, y
            command = "l" if command == "m" else "L"
        if op == "Z":
            x, y = start_x, start_y
            command = None
        scaled = [(px * sx, py * sy) for px, py in points]
        if not all(math.isfinite(px) and math.isfinite(py) for px, py in scaled):
            raise DesignError("SVG_PATH_COORDINATE_INVALID")
        cmds.append((op, scaled))
        if len(cmds) > 512:
            raise DesignError("SVG_PATH_COMMAND_LIMIT")
    return cmds


# ---------------------------------------------------------------- layout -> scene

def _font_spans(runs, base):
    spans, offset = [], 0
    for run in runs:
        end = offset + len(run["text"])
        font = _font(run)
        if font != base and end > offset:
            if spans and spans[-1]["end"] == offset and spans[-1]["font"] == font:
                spans[-1]["end"] = end
            else:
                spans.append({"start": offset, "end": end, "font": font})
        offset = end
    return spans


def _table_grid(rows):
    """Map HTML cells to the editable PowerPoint grid, keeping covered slots empty."""
    if not 1 <= len(rows) <= 200:
        raise DesignError("HTML_TABLE_ROW_COUNT_INVALID")
    grid = [{} for _ in rows]
    starts, ends = {}, {}
    for row_idx, row in enumerate(rows):
        col = 0
        for cell in row["cells"]:
            while col in grid[row_idx]:
                col += 1
            nr, nc = cell.get("rowSpan", 1), cell.get("colSpan", 1)
            if nr < 1 or nc < 1 or row_idx + nr > len(rows) or col + nc > 50:
                raise DesignError("HTML_TABLE_SPAN_OUT_OF_BOUNDS")
            for rr in range(row_idx, row_idx + nr):
                for cc in range(col, col + nc):
                    if cc in grid[rr]:
                        raise DesignError("HTML_TABLE_SPAN_OVERLAP")
                    grid[rr][cc] = None
            grid[row_idx][col] = cell
            # New browser measurements include x. Older rectangular layouts only store widths.
            x = cell.get("x", ends.get(col, 0))
            starts[col] = x
            ends[col + nc] = x + cell["w"]
            col += nc
    ncols = max((len(row) for row in grid), default=0)
    if not ncols or any(set(row) != set(range(ncols)) for row in grid):
        raise DesignError("HTML_TABLE_RAGGED: every logical grid position must be covered")
    # Some column boundaries lie entirely inside merged cells and never have a visible edge.
    boundaries = {**ends, **starts}
    widths = []
    measured = sorted(boundaries)
    for left, right in zip(measured, measured[1:]):
        width = (boundaries[right] - boundaries[left]) / (right - left)
        if width <= 0:
            raise DesignError("HTML_TABLE_COLUMN_GEOMETRY_UNSUPPORTED")
        widths.extend([width] * (right - left))
    return [[row[col] for col in range(ncols)] for row in grid], widths


def _cell_style(cell):
    font = _font(cell["runs"][0] if cell["runs"] else cell["font"])
    fill, alpha = _rgba(cell["fill"]) if cell["fill"] else (None, 1.0)
    top, right, bottom, left = cell["pad"]
    style = {"fill": fill, "font": font, "align": cell["align"] if cell["align"] in {"left", "center", "right"} else "left",
             "valign": cell["valign"], "line_height": round(cell["font"]["lineHeight"], 2),
             "margin": [round(top, 2), round(max(0, right - 2.5), 2), round(bottom, 2), round(left, 2)]}
    if fill and alpha < 0.999:
        style["fill_alpha"] = round(alpha, 3)
    borders = cell.get("borders", {"bottom": cell.get("borderBottom")})
    for side, border in borders.items():
        if border:
            color, alpha = _rgba(border["c"])
            style["border_" + side] = {"color": color, "width": round(border["w"], 2)}
            if alpha < 0.999:
                style["border_" + side]["alpha"] = round(alpha, 3)
    for key, attr in (("row_span", "rowSpan"), ("col_span", "colSpan")):
        if cell.get(attr, 1) > 1:
            style[key] = cell[attr]
    spans = _font_spans(cell["runs"], font)
    if spans:
        style["spans"] = spans
    return style


def to_scene(layout, page_id, canvas, *, default_source, source_kind="user"):
    """Compile extractor output into (content items, nodes, background, conversion notes, authored kinds)."""
    if source_kind not in {"user", "document"}:
        raise DesignError("HTML_SOURCE_KIND_INVALID")
    cw, ch = canvas["width"], canvas["height"]
    items, nodes, notes = [], [], []
    authored = {}
    used = set()
    counter = {"c": 0, "n": 0}

    def cid(preferred=None):
        if preferred:
            if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,79}", preferred) or preferred in used:
                raise DesignError(f"HTML_CONTENT_ID_INVALID_OR_DUPLICATE: {preferred}")
            used.add(preferred)
            return preferred
        while True:
            counter["c"] += 1
            value = f"{page_id}-c{counter['c']:03d}"
            if value not in used:
                used.add(value)
                return value

    def nid():
        counter["n"] += 1
        return f"{page_id}-n{counter['n']:03d}"

    def provenance(item, content_id):
        kind = item.get("authored")
        if kind is not None:
            kind = kind.strip().lower() or "wording"
            if kind not in AUTHORED:
                raise DesignError(f"HTML_AUTHORED_KIND_INVALID: {kind} (use wording, derived or nav)")
            authored[content_id] = kind
        return {"kind": source_kind, "source": (item.get("src") or default_source)[:500], "checked": False,
                "uncertainties": [AUTHORED[kind]] if kind else []}

    def shape(box, style, kind="rect"):
        nodes.append({"id": nid(), "page_id": page_id, "type": "shape", "role": "native_shape", "shape": kind,
                      "box": box, "z": len(nodes), "style": style})

    for it in layout["items"]:
        k = it["kind"]
        if k == "box":
            fill, alpha = _rgba(it["fill"]) if it["fill"] else (None, 1.0)
            borders = it["borders"]
            uniform = all(borders) and len({(b["w"], b["c"]) for b in borders}) == 1
            radii = it["radius"]
            uniform_radius = len(set(radii)) == 1
            radius = radii[0] if uniform_radius else 0
            asymmetric_radius = not uniform_radius and max(radii) > 0.5
            box = _clamp_box(it["x"], it["y"], it["w"], it["h"], cw, ch)
            bleeds = it["x"] < -0.5 or it["y"] < -0.5 or it["x"] + it["w"] > cw + 0.5 or it["y"] + it["h"] > ch + 0.5
            if bleeds and max(radii) > 0.5 and fill:
                # A rounded shape crossing the slide edge keeps its true curve: clip its outline to the canvas.
                poly = _clip_polygon(_rounded_polygon(it["x"], it["y"], it["w"], it["h"], radii), 0, 0, cw, ch)
                if len(poly) >= 3:
                    xs, ys = [p[0] for p in poly], [p[1] for p in poly]
                    bx, by = min(xs), min(ys)
                    bw, bh = max(0.1, max(xs) - bx), max(0.1, max(ys) - by)
                    cmds = [{"op": "M" if i == 0 else "L", "points": [[round(min(bw, max(0, px - bx)), 3),
                                                                        round(min(bh, max(0, py - by)), 3)]]}
                            for i, (px, py) in enumerate(poly[:510])]
                    style = {"fill": fill, "stroke": None, **({"fill_alpha": round(alpha, 3)} if alpha < 0.999 else {})}
                    nodes.append({"id": nid(), "page_id": page_id, "type": "path", "role": "native_shape",
                                  "box": {"x": round(bx, 2), "y": round(by, 2), "width": round(bw, 2), "height": round(bh, 2)},
                                  "z": len(nodes), "commands": cmds + [{"op": "Z", "points": []}], "style": style})
                    notes.append({"code": "BLEED_SHAPE_CLIPPED_TO_SLIDE", "at": f"{it['x']:.0f},{it['y']:.0f}"})
                continue
            if fill or uniform:
                style = {"fill": fill}
                if fill and alpha < 0.999:
                    style["fill_alpha"] = round(alpha, 3)
                if uniform:
                    sc, sa = _rgba(borders[0]["c"])
                    style.update(stroke=sc, stroke_width=round(borders[0]["w"], 2))
                    if sa < 0.999:
                        style["stroke_alpha"] = round(sa, 3)
                else:
                    style["stroke"] = None
                if asymmetric_radius:
                    nodes.append({"id": nid(), "page_id": page_id, "type": "path", "role": "native_shape",
                                  "box": box, "z": len(nodes),
                                  "commands": _asymmetric_rounded_path(box["width"], box["height"], radii),
                                  "style": style})
                else:
                    if radius > 0.5:
                        style["radius"] = round(radius, 2)
                    shape(box, style, "rounded_rect" if radius > 0.5 else "rect")
            if not uniform:
                for side, b in zip("TRBL", borders):
                    if not b:
                        continue
                    x, y, w, h = it["x"], it["y"], it["w"], it["h"]
                    geo = {"T": (x, y, w, b["w"]), "B": (x, y + h - b["w"], w, b["w"]),
                           "L": (x, y, b["w"], h), "R": (x + w - b["w"], y, b["w"], h)}[side]
                    c, a = _rgba(b["c"])
                    st = {"fill": c, "stroke": None}
                    if a < 0.999:
                        st["fill_alpha"] = round(a, 3)
                    shape(_clamp_box(*geo, cw, ch), st)
        elif k == "text":
            runs = it["runs"]
            text = "".join(r["text"] for r in runs)
            base = _font(runs[0])
            spans = _font_spans(runs, base)
            fs = max(r["size"] for r in runs)
            lh = it["lineHeight"]
            single = it["lines"] == 1
            if single:
                w = it["w"] + 6
                x = {"left": it["x"] - 1, "center": it["x"] + it["w"] / 2 - w / 2,
                     "right": it["x"] + it["w"] - w + 1}.get(it["align"], it["x"])
            else:
                x, w = it["content"]["x"], it["content"]["w"] + 1
            # Browsers centre glyphs in the CSS line box; Office places extra leading above the glyphs.
            dy = (lh - fs * 1.32) / 2
            content_id = cid(it.get("cid"))
            items.append({"id": content_id, "page_id": page_id, "type": "text", "text": text,
                          "required_edit": "native", "provenance": provenance(it, content_id)})
            node = {"id": nid(), "page_id": page_id, "type": "text", "role": "native_text", "content_id": content_id,
                    "box": _clamp_box(x, it["y"] - dy, w, it["h"], cw, ch), "z": len(nodes), "font": base,
                    "align": it["align"] if it["align"] in {"left", "center", "right"} else "left",
                    "valign": "top", "wrap": not single, "line_height": round(lh, 2), "margin": 0}
            if runs[0]["letterSpacing"]:
                node["letter_spacing"] = max(-10, min(20, round(runs[0]["letterSpacing"], 2)))
            if spans:
                node["spans"] = spans
            nodes.append(node)
        elif k == "table":
            rows = it["rows"]
            grid, widths = _table_grid(rows)
            cells = [["".join(x["text"] for x in c["runs"]) if c else "" for c in row] for row in grid]
            styles = [[_cell_style(c) if c else {} for c in row] for row in grid]
            box = _clamp_box(it["x"], it["y"], it["w"], it["h"], cw, ch)
            scale = box["width"] / sum(widths)
            widths = [round(w * scale, 3) for w in widths]
            widths[-1] = round(box["width"] - sum(widths[:-1]), 3)
            content_id = cid(it.get("cid"))
            prov = provenance(it, content_id)
            cell_authored = {}
            for r_idx, row in enumerate(grid):
                for c_idx, cell in enumerate(row):
                    if cell and cell.get("authored") is not None:
                        ck = cell["authored"].strip().lower() or "wording"
                        if ck not in AUTHORED:
                            raise DesignError(f"HTML_AUTHORED_KIND_INVALID: {ck} (use wording, derived or nav)")
                        cell_authored[(r_idx, c_idx)] = ck
            if cell_authored:
                table_kind = authored.get(content_id)
                authored[content_id] = {"table": table_kind, "cells": cell_authored}
                for ck in sorted(set(cell_authored.values())):
                    note = f"table cells ({ck}): {AUTHORED[ck]}"
                    if note not in prov["uncertainties"]:
                        prov["uncertainties"].append(note)
            items.append({"id": content_id, "page_id": page_id, "type": "table", "cells": cells,
                          "required_edit": "native", "provenance": prov})
            first = next(c["font"] for row in reversed(styles) for c in row if c)
            nodes.append({"id": nid(), "page_id": page_id, "type": "table", "role": "native_table", "content_id": content_id,
                          "box": box, "z": len(nodes), "font": first, "fill": "FFFFFF", "header_fill": "FFFFFF",
                          "header_color": first["color"], "column_widths": widths,
                          "row_heights": [round(max(0.1, r["h"]), 2) for r in rows], "cell_styles": styles})
        elif k == "chart":
            spec = validate_chart(it["spec"])
            content_id = cid(it.get("cid"))
            items.append({"id": content_id, "page_id": page_id, "type": "chart", "categories": spec["categories"],
                          "series": [{"name": s["name"], "values": s["values"]} for s in spec["series"]],
                          "data_basis": "user_data", "required_edit": "native", "provenance": provenance(it, content_id)})
            nodes.append({"id": nid(), "page_id": page_id, "type": "chart", "role": "native_chart", "content_id": content_id,
                          "box": _clamp_box(it["x"], it["y"], it["w"], it["h"], cw, ch), "z": len(nodes),
                          **native_chart_options(spec)})
        elif k == "image":
            node = {"id": nid(), "page_id": page_id, "type": "image", "role": "replaceable_image",
                    "asset_id": it["asset"], "fit": it["fit"] if it["fit"] in {"contain", "cover"} else "contain",
                    "box": _clamp_box(it["x"], it["y"], it["w"], it["h"], cw, ch), "z": len(nodes)}
            if it.get("radius", 0) > 0.5:
                node["radius"] = round(it["radius"], 2)
            nodes.append(node)
        elif k == "path":
            cmds = _parse_path(it["d"], 1, 1)
            a, b, c, d = it.get("matrix", [it.get("sx", 1), 0, 0, it.get("sy", 1)])
            cmds = [(op, [(a * x + c * y, b * x + d * y) for x, y in points]) for op, points in cmds]
            pts = [p for _, ps in cmds for p in ps]
            x0, y0 = min(p[0] for p in pts), min(p[1] for p in pts)
            x1, y1 = max(p[0] for p in pts), max(p[1] for p in pts)
            w, h = max(0.1, x1 - x0), max(0.1, y1 - y0)
            style = {"fill": None, "stroke": None}
            if it["fill"]:
                c, a = _rgba(it["fill"])
                a *= it.get("fillOpacity", 1)
                style["fill"] = c
                if a < 0.999:
                    style["fill_alpha"] = round(a, 3)
            if it["stroke"]:
                c, a = _rgba(it["stroke"])
                a *= it.get("strokeOpacity", 1)
                style.update(stroke=c, stroke_width=round(min(20, it["strokeWidth"]), 2))
                if a < 0.999:
                    style["stroke_alpha"] = round(a, 3)
            # The box is stored to two decimals; its control points must round inside it.
            commands = [{"op": op, "points": [[min(round(w, 2), round(px - x0, 3)),
                                               min(round(h, 2), round(py - y0, 3))] for px, py in ps]}
                        for op, ps in cmds]
            nodes.append({"id": nid(), "page_id": page_id, "type": "path", "role": "native_shape",
                          "box": _clamp_box(it["ox"] + x0, it["oy"] + y0, w, h, cw, ch), "z": len(nodes),
                          "commands": commands, "style": style})
    # Charts without an explicit font use the page's dominant Latin/East Asian pair, not a generic face.
    from collections import Counter
    pairs = Counter((n["font"]["family"], n["font"].get("ea_family")) for n in nodes if n["type"] == "text")
    family, ea = pairs.most_common(1)[0][0] if pairs else ("Arial", None)
    for n in nodes:
        if n["type"] == "chart" and n["font"]["family"] == "__page__":
            n["font"]["family"] = family
            if ea:
                n["font"]["ea_family"] = ea
    background, _ = _rgba(layout.get("background")) if layout.get("background") else ("FFFFFF", 1)
    return items, nodes, background or "FFFFFF", notes, authored


# ---------------------------------------------------------------- source checks

def source_segment(text, heading=None):
    """Slice one page of a manuscript: from the line starting with ``heading`` to the next sibling heading."""
    if not heading:
        return text
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines) if l.strip().startswith(heading)), None)
    if start is None:
        raise DesignError(f"SOURCE_HEADING_NOT_FOUND: {heading}")
    pattern = re.compile("^" + re.sub(r"\d+", r"\\d+", re.escape(heading.strip()).replace(r"\ ", r"\s*")))
    end = next((i for i in range(start + 1, len(lines)) if pattern.match(lines[i].strip())), len(lines))
    return "\n".join(lines[start:end])


# A dash between digits is also used as a date/range separator, as in 2025-06.
NUMBER = re.compile(r"(?P<value>(?:(?<!\d)[+-])?(?:(?:\d{1,3}(?:,\d{3})+(?!\d)|\d+)(?:\.\d+)?|\.\d+)"
                    r"(?:[Ee][+-]?\d+)?)(?P<percent> *%)?")


def _numbered_text(text):
    """Keep numeric tokens indivisible during literal search and index their value and percent unit."""
    tokens = {}

    def mark(match):
        token = match["value"]
        try:
            value = Decimal(token.replace(",", ""))
        except InvalidOperation as exc:
            raise DesignError("SOURCE_NUMBER_OUT_OF_RANGE") from exc
        percent = bool(match["percent"])
        tokens.setdefault((value, percent), token)
        return "\0" + token.lstrip("+") + ("%" if percent else "") + "\0"

    # Strip layout decorations before NFKC changes circled bullets such as ① into digits.
    normalized = normalize_text(DECOR.sub(" ", text)).replace("\0", "\ufffd")
    normalized = re.sub(r"− *(?=[.\d])", "-", normalized)
    return _norm(NUMBER.sub(mark, normalized)), tokens


def trace(items, source, authored=None):
    """Mark records that literally occur in the source as checked; list the rest for the author.

    Declared model wording is accepted only when every number in it also occurs in the source;
    ``derived`` and ``nav`` records are accepted with their uncertainty note.
    """
    authored = authored or {}
    src, numbers = _numbered_text(source)
    chart_values = {value for value, _ in numbers}
    untraced = []
    for c in items:
        prov, kind = c["provenance"], authored.get(c["id"])
        prov["checked"] = False
        if c["type"] == "table" and isinstance(kind, dict):
            table_kind = kind.get("table")
            cell_kinds = kind.get("cells") or {}
            missing, reasons = [], []
            for r_idx, row in enumerate(c["cells"]):
                for c_idx, cell in enumerate(row):
                    if not cell.strip():
                        continue
                    ck = cell_kinds.get((r_idx, c_idx), table_kind)
                    if ck in {"derived", "nav"}:
                        continue
                    if ck == "wording":
                        bad = sorted({token for key, token in _numbered_text(cell)[1].items() if key not in numbers})
                        if bad:
                            missing.extend(bad)
                            reasons.append("authored_numbers_not_in_source")
                    elif _numbered_text(cell)[0] not in src:
                        missing.append(cell)
                        reasons.append("not_in_source")
            if missing:
                reason = reasons[0] if len(set(reasons)) == 1 else "not_in_source"
                untraced.append({"content_id": c["id"], "reason": reason, "missing": [m[:80] for m in missing[:8]]})
            else:
                prov["checked"] = True
            continue
        if kind in {"derived", "nav"}:
            prov["checked"] = True
            continue
        if c["type"] == "text":
            values = [c["text"]]
        elif c["type"] == "table":
            values = [cell for row in c["cells"] for cell in row if cell.strip()]
        else:
            values = c["categories"]
        if kind == "wording":
            reason = "authored_numbers_not_in_source"
            missing = sorted({token for v in values for key, token in _numbered_text(v)[1].items() if key not in numbers})
        else:
            reason = "not_in_source"
            missing = [v for v in values if _numbered_text(v)[0] not in src]
        if c["type"] == "chart":
            # A native series stores raw numeric values. Its unit may live in the series name.
            missing.extend(str(v) for series in c["series"] for v in series["values"]
                           if Decimal(str(v)) not in chart_values)
        if missing:
            untraced.append({"content_id": c["id"], "reason": reason, "missing": [m[:80] for m in missing[:8]]})
        else:
            prov["checked"] = True
    return untraced


_CHART_SINGLE_AXIS_TYPES = {"column", "bar", "line", "stacked_column", "stacked_bar"}
_CHART_UNIT_PATTERNS = {
    "percent": re.compile(r"(?:[（(]\s*[%％]\s*[)）]|[%％](?:\s|$)|百分比|占比\s*[（(]\s*[%％])"),
    "power_energy": re.compile(r"(?<![A-Za-z])(?:TWh|GWh|MWh|kWh|GW|MW|kW)(?![A-Za-z])"),
    "currency": re.compile(r"(?:十亿美元|亿美元|亿元|万元|美元|人民币|(?<![A-Za-z])(?:USD|RMB|CNY|EUR)(?![A-Za-z])|\$[BMK]\b|[（(]\s*[$¥€]\s*[)）])"),
    "multiple": re.compile(r"(?:[（(]\s*[×xX倍]\s*[)）]|倍数)"),
}


def _unit_families(text):
    text = str(text or "")
    return {name for name, pat in _CHART_UNIT_PATTERNS.items() if pat.search(text)}


def _mixed_chart_units(spec):
    if not isinstance(spec, dict) or spec.get("type", "line") not in _CHART_SINGLE_AXIS_TYPES:
        return []
    for labels in (spec.get("categories") or [], [s.get("name", "") for s in (spec.get("series") or []) if isinstance(s, dict)]):
        per_label = [_unit_families(lbl) for lbl in labels]
        non_empty = [u for u in per_label if u]
        combined = set().union(*non_empty) if non_empty else set()
        if len(combined) >= 2 and any(u != non_empty[0] for u in non_empty[1:]):
            return sorted(combined)
    return []


def lint(layout, canvas):
    """Objective layout checks on the browser geometry (before any Office rendering)."""
    cw, ch = canvas["width"], canvas["height"]
    findings = []

    def add(code, severity, it, detail=""):
        findings.append({"code": code, "severity": severity, "at": f"{it['x']:.0f},{it['y']:.0f}",
                         **({"text": detail[:40]} if detail else {})})

    def label(it):
        return "".join(r["text"] for r in it.get("runs", []))

    solid = [i for i in layout["items"] if i["kind"] in {"text", "table", "chart", "image"}]
    for it in solid:
        if it["x"] < -1 or it["y"] < -1 or it["x"] + it["w"] > cw + 1 or it["y"] + it["h"] > ch + 1:
            add("OUTSIDE_SLIDE", "error", it, label(it))
        if it["kind"] == "chart":
            mixed = _mixed_chart_units(it.get("spec"))
            if mixed:
                add("CHART_MIXED_UNITS", "error", it, "/".join(mixed))
    texts = [i for i in layout["items"] if i["kind"] == "text"]
    for it in texts:
        ov = it.get("overflow") or {}
        size = max(r["size"] for r in it["runs"])
        # Glyph ink taller than the CSS line box (CJK faces) is not overflow; a hidden line or column is.
        if ov.get("x", 0) > size * 0.5 or ov.get("y", 0) > it["lineHeight"] * 0.5:
            add("TEXT_OVERFLOWS_BOX", "error", it, label(it))
        box = it.get("container")
        if box and (it["x"] < box["x"] - 1.5 or it["y"] < box["y"] - 1.5 or
                    it["x"] + it["w"] > box["x"] + box["w"] + 1.5 or it["y"] + it["h"] > box["y"] + box["h"] + 1.5):
            add("TEXT_OUTSIDE_CONTAINER", "error", it, label(it))
    def _is_background_image(item, item_index, text_index):
        if item["kind"] != "image":
            return False
        if item.get("layer") == "background":
            return True
        # A full/half-bleed cover photo painted before text is an intentional backdrop, not an accidental collision.
        area_ratio = (item["w"] * item["h"]) / max(1.0, cw * ch)
        return item.get("fit") == "cover" and area_ratio >= 0.5 and item_index < text_index

    indexed = list(enumerate(layout["items"]))
    text_entries = [(idx, it) for idx, it in indexed if it["kind"] == "text"]
    non_text_solid = [(idx, it) for idx, it in indexed if it["kind"] in {"table", "chart", "image"}]
    for i, (a_idx, a) in enumerate(text_entries):
        for b_idx, b in text_entries[i + 1:] + non_text_solid:
            dx = min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"])
            dy = min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"])
            if dx > 1.5 and dy > 1.5:
                if _is_background_image(b, b_idx, a_idx):
                    add("TEXT_OVER_BACKGROUND_IMAGE", "warning", a, label(a) + " ↔ " + b.get("asset", "image"))
                else:
                    add("TEXT_OVERLAP", "error", a, label(a) + " ↔ " + (label(b) or b["kind"]))
    floor = round(9 * cw / 1440, 1)
    sizes = {}
    for it in texts:
        for r in it["runs"]:
            sizes[round(r["size"] * 2) / 2] = sizes.get(round(r["size"] * 2) / 2, 0) + len(r["text"])
            if r["size"] < floor - 0.01:
                add("SMALL_TEXT", "warning", it, r["text"])
            if re.search(r"[\u2e80-\u9fff\uac00-\ud7af\uff00-\uffef]", r["text"]) and \
                    not any(CJK_HINT.search(f) for f in r["stack"]):
                add("CJK_TEXT_WITHOUT_CJK_FONT", "warning", it, r["text"])
    if sizes:
        body = max(sizes, key=sizes.get)
        if len(sizes) < 3:
            findings.append({"code": "FLAT_HIERARCHY", "severity": "warning", "levels": sorted(sizes)})
        elif max(sizes) / body < 2.2:
            findings.append({"code": "WEAK_HIERARCHY", "severity": "warning", "body": body, "largest": max(sizes)})
    seen, unique = set(), []
    for f in findings:
        key = (f["code"], f.get("at"), f.get("text"))
        if key not in seen:
            seen.add(key)
            unique.append(f)
    return {"errors": sum(f["severity"] == "error" for f in unique),
            "warnings": sum(f["severity"] == "warning" for f in unique), "findings": unique[:40]}


def coverage(source, items, *, source_heading=None):
    """Source -> slide: phrases and numbers of the page segment that do not appear on the slide."""
    shown = []
    chart_values = set()
    for c in items:
        if c["type"] == "text":
            shown.append(c["text"])
        elif c["type"] == "table":
            shown += [x for row in c["cells"] for x in row]
        else:
            shown += c["categories"] + [s["name"] for s in c["series"]] + [str(v) for s in c["series"] for v in s["values"]]
            chart_values.update(Decimal(str(v)) for s in c["series"] for v in s["values"])
    marked = [_numbered_text(v) for v in shown]
    joined = "".join(text for text, _ in marked)
    numbers_shown = {key for _, tokens in marked for key in tokens}
    phrases, missing = [], set()
    if source_heading:
        source = source.lstrip().removeprefix(source_heading)
    for line in source.splitlines():
        if not line.strip():
            continue
        for cell in line.split("\t"):
            for ph in re.split(r"[；;。\n•]|：(?=.)", cell):
                ph = ph.strip().strip("：:（）()、，,")
                display = _norm(ph)
                if len(display) >= 2 and display != "未标注" and _numbered_text(ph)[0] not in joined:
                    phrases.append(display)
        missing.update(token for key, token in _numbered_text(line)[1].items()
                       if key not in numbers_shown and key[0] not in chart_values)
    return {"missing_numbers": sorted(missing), "missing_phrases": sorted(set(phrases))[:200],
            "missing_phrase_count": len(set(phrases))}


# ---------------------------------------------------------------- task update

def apply(task, page_id, items, nodes, background):
    import copy
    pages = {p["id"]: p for p in task["scene"]["pages"]}
    if page_id not in pages:
        raise DesignError("UNKNOWN_PAGE")
    other = {c["id"] for c in task["content"]["items"] if c["page_id"] != page_id}
    clash = sorted(c["id"] for c in items if c["id"] in other)
    if clash:
        raise DesignError("HTML_CONTENT_ID_USED_ON_ANOTHER_PAGE: " + ", ".join(clash[:5]))
    other_nodes = {n["id"] for p in task["scene"]["pages"] if p["id"] != page_id for n, *_ in walk(p["nodes"])}
    if any(n["id"] in other_nodes for n in nodes):
        raise DesignError("HTML_NODE_ID_CLASH")
    candidate = copy.deepcopy(task)
    assets = {x["id"]: x for x in candidate["assets"]["items"]}
    attached = []
    for n in nodes:
        if n["type"] != "image":
            continue
        asset = assets.get(n["asset_id"])
        if not asset:
            raise DesignError(f"HTML_ASSET_UNKNOWN: {n['asset_id']} (register it with `engine design ingest` first)")
        if asset["role"] in {"reference", "target"}:
            raise DesignError(f"HTML_ASSET_ROLE_NOT_PLACEABLE: {n['asset_id']} is a {asset['role']} image")
        if asset["role"] == "raster_data":
            raise DesignError(f"HTML_RASTER_DATA_NEEDS_AUTHOR: {n['asset_id']} requires a content binding and raster acceptance")
        if page_id not in asset["page_ids"]:
            asset["page_ids"].append(page_id)
            attached.append(asset["id"])
    candidate["content"]["items"] = [c for c in candidate["content"]["items"] if c["page_id"] != page_id] + items
    page = next(p for p in candidate["scene"]["pages"] if p["id"] == page_id)
    page["nodes"], page["background"] = nodes, background
    reset = False
    design = next(d for d in candidate["design"]["pages"] if d["page_id"] == page_id)
    comp = design.get("composition")
    ids = {c["id"] for c in items}
    if comp and (any(x not in ids for x in comp["reading_path"]) or comp.get("claim_content_id", next(iter(ids), "")) not in ids):
        design.pop("composition")
        reset = True
    validate(candidate)
    return candidate, reset, attached


ASSET_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_-]{0,79}$")


def _asset_refs(root):
    refs = []
    for el in root.iter():
        if not isinstance(el.tag, str) or "data-asset" not in el.attrib:
            continue
        ref = (el.get("data-asset") or "").strip()
        if not ASSET_ID.fullmatch(ref):
            raise DesignError(f"HTML_ASSET_ID_INVALID: {ref[:80]}")
        refs.append(ref)
    return sorted(set(refs))


def _asset_css(source, asset_bytes):
    """Tool-owned preview styles: show registered assets in the browser screenshot."""
    import base64
    if isinstance(source, str):
        try:
            root = lxml_html.document_fromstring(source)
        except Exception as exc:
            raise DesignError(f"HTML_PARSE_FAILED: {exc}") from exc
        refs = _asset_refs(root)
    else:
        refs = sorted(set(source))
        for ref in refs:
            if not ASSET_ID.fullmatch(ref):
                raise DesignError(f"HTML_ASSET_ID_INVALID: {ref[:80]}")
    css = []
    for ref in refs:
        if ref not in asset_bytes:
            raise DesignError(f"HTML_ASSET_UNKNOWN: {ref} (register it with `engine design ingest` first)")
        uri = "data:image/png;base64," + base64.b64encode(asset_bytes[ref]).decode("ascii")
        css.append(f'[data-asset="{ref}"]{{background:url({uri}) center/contain no-repeat}}'
                   f'[data-asset="{ref}"][data-fit="cover"]{{background-size:cover}}')
    return "".join(css)


def _authored_summary(authored):
    counts = {k: 0 for k in AUTHORED}
    for value in authored.values():
        if isinstance(value, str) and value in counts:
            counts[value] += 1
        elif isinstance(value, dict):
            if value.get("table") in counts:
                counts[value["table"]] += 1
            for ck in (value.get("cells") or {}).values():
                if ck in counts:
                    counts[ck] += 1
    return counts


def import_html(task, page_id, text, *, default_source, source_text=None, browser=None, assume_checked=False,
                source_kind="user", asset_bytes=None, page_scoped=False, source_heading=None):
    """Policy check -> browser layout -> scene records; returns (candidate task, report, layout, png)."""
    policy = check_policy(text)
    inject = _asset_css(policy["assets"], asset_bytes or {})
    layout, png = render_layout(text, task["canvas"]["width"], task["canvas"]["height"], browser=browser, inject=inject)
    items, nodes, background, notes, authored = to_scene(layout, page_id, task["canvas"], default_source=default_source,
                                                         source_kind=source_kind)
    report = {"status": "imported", "page_id": page_id, "html_sha256": policy["sha256"],
              "content_items": len(items), "nodes": len(nodes),
              "objects": {k: sum(n["type"] == k for n in nodes) for k in ("text", "shape", "path", "table", "chart", "image")},
              "design_lint": lint(layout, task["canvas"]),
              "browser_warnings": layout.get("warnings", [])[:50], "conversion_notes": notes[:50],
              "authored": _authored_summary(authored)}
    if "browser_exit_warning" in layout:
        report["browser_exit_warning"] = layout["browser_exit_warning"]
    if source_text is not None:
        report["untraced"] = trace(items, source_text, authored)
        report["coverage"] = coverage(source_text, items, source_heading=source_heading)
        # A per-page manuscript defaults to complete on-slide coverage; a whole document is selectively condensed.
        report["coverage"]["scope"] = "page" if page_scoped else "document"
    elif assume_checked:
        for c in items:
            c["provenance"]["checked"] = True
        report["traceability"] = "author_asserted_without_source_file"
    else:
        report["traceability"] = "not_run: pass --source-file, or --assume-checked after checking every record"
    unchecked = [c["id"] for c in items if not c["provenance"]["checked"]]
    report["unchecked_count"] = len(unchecked)
    if unchecked:
        # Unchecked records may not be bound to native objects; keep the task unchanged.
        report["status"] = "untraced_content"
        report["next"] = ("Correct the wording to match the source, or mark deliberate model wording with "
                          "data-authored (wording/derived/nav) and record its basis in page-plan.md; then import again.")
        return None, report, layout, png
    lint_ = report["design_lint"]
    if lint_["errors"]:
        # Blocking layout defects must be fixed before mutating task.json or building.
        report["status"] = "imported_with_lint_errors"
        report["next"] = ("Inspect the preview and fix all design_lint errors (overlap, overflow, "
                          "out-of-container or out-of-slide) in the HTML, then re-import.")
        return None, report, layout, png
    candidate, reset, attached = apply(task, page_id, items, nodes, background)
    report["composition_reset"] = reset
    if attached:
        report["assets_attached_to_page"] = attached
    cov = report.get("coverage") or {}
    if layout.get("warnings") or lint_["warnings"] or (cov.get("scope") == "page" and cov.get("missing_numbers")):
        report["status"] = "imported_with_findings"
    return candidate, report, layout, png
