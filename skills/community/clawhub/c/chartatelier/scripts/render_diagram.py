#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render a diagram (HTML or standalone SVG) to a high-resolution PNG.

Three backends, tried in order unless --backend pins one:

  1. playwright  - element screenshot with device_scale_factor. Tightest result,
                   no window-size guessing. Needs `pip install playwright` plus a
                   browser (a local Chrome/Edge runtime is reused when present).
  2. chrome      - headless Chrome/Edge CLI. Zero Python dependencies beyond the
                   interpreter. Window size must equal the SVG intrinsic size.
  3. wkhtmltoimage - last resort. No devicePixelRatio support, so the scale is
                   emulated with --zoom; modern CSS and some SVG features degrade.

Every run re-reads the PNG header and reports dimensions plus content coverage,
because "the file was written" does not mean "the render is correct".

Examples
--------
    python render_diagram.py diagram.html --out diagram@2x.png --scale 2
    python render_diagram.py diagram.svg  --out diagram@3x.png --scale 3
    python render_diagram.py card.html --selector "#canvas" --out card@2x.png
    python render_diagram.py diagram.html --print-cmd        # show the CLI fallback

This file depends only on the Python standard library except for the optional
backends noted above. No machine-specific paths are baked in: browsers are
discovered from PATH and from the install roots the operating system reports
through environment variables.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_MIN_WIDTH = 3000
BROWSER_NAMES = (
    "google-chrome",
    "google-chrome-stable",
    "chromium",
    "chromium-browser",
    "chrome",
    "msedge",
    "microsoft-edge",
)
BROWSER_RELPATHS = (
    ("Google", "Chrome", "Application", "chrome.exe"),
    ("Google", "Chrome Beta", "Application", "chrome.exe"),
    ("Microsoft", "Edge", "Application", "msedge.exe"),
)
BROWSER_ENV_ROOTS = ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA", "PROGRAMW6432")


# --------------------------------------------------------------------------- #
# discovery
# --------------------------------------------------------------------------- #
def find_browser() -> str | None:
    """Locate a Chromium-family browser without hardcoding a machine path."""
    for var in ("CHROME_PATH", "BROWSER_PATH", "EDGE_PATH"):
        candidate = os.environ.get(var, "").strip()
        if candidate and os.path.isfile(candidate):
            return candidate
    for name in BROWSER_NAMES:
        found = shutil.which(name)
        if found:
            return found
    roots = [os.environ.get(v) for v in BROWSER_ENV_ROOTS]
    for root in roots:
        if not root:
            continue
        for parts in BROWSER_RELPATHS:
            candidate = Path(root).joinpath(*parts)
            if candidate.is_file():
                return str(candidate)
    return None


def find_wkhtmltoimage() -> str | None:
    for name in ("wkhtmltoimage", "wkhtmltoimage.exe"):
        found = shutil.which(name)
        if found:
            return found
    return None


def have_playwright() -> bool:
    try:
        import playwright  # noqa: F401
        from playwright.sync_api import sync_playwright  # noqa: F401
        return True
    except Exception:
        return False


# --------------------------------------------------------------------------- #
# geometry
# --------------------------------------------------------------------------- #
def svg_intrinsic_size(text: str) -> tuple[int, int] | None:
    """Read width/height from the opening <svg> tag, falling back to the viewBox."""
    head = re.search(r"<svg\b[^>]*>", text, re.S | re.I)
    if not head:
        return None
    tag = head.group(0)

    def attr(name: str) -> float | None:
        m = re.search(rf'\b{name}\s*=\s*"([^"]+)"', tag, re.I)
        if not m:
            return None
        value = m.group(1).strip()
        m2 = re.match(r"^([\d.]+)\s*(px)?$", value)
        return float(m2.group(1)) if m2 else None

    width, height = attr("width"), attr("height")
    if width and height:
        return round(width), round(height)
    vb = re.search(r'viewBox\s*=\s*"([^"]+)"', tag, re.I)
    if vb:
        parts = re.split(r"[,\s]+", vb.group(1).strip())
        if len(parts) == 4:
            try:
                return round(float(parts[2])), round(float(parts[3]))
            except ValueError:
                return None
    return None


def png_size(path: Path) -> tuple[int, int] | None:
    """Parse the IHDR chunk. Standard library only - PIL is optional everywhere."""
    try:
        with path.open("rb") as fh:
            header = fh.read(26)
        if header[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        width, height = struct.unpack(">II", header[16:24])
        return int(width), int(height)
    except Exception:
        return None


def content_coverage(path: Path, step: int = 8) -> tuple[float, float] | None:
    """Saturation-based coverage. Brightness buckets misread pastel fills as blank."""
    try:
        from PIL import Image
    except Exception:
        return None
    im = Image.open(path).convert("RGB")
    w, h = im.size
    px = im.load()
    min_x, min_y, max_x, max_y = w, h, -1, -1
    for y in range(0, h, step):
        for x in range(0, w, step):
            r, g, b = px[x, y]
            if max(r, g, b) - min(r, g, b) > 30:
                min_x, max_x = min(min_x, x), max(max_x, x)
                min_y, max_y = min(min_y, y), max(max_y, y)
    if max_x < 0 or max_y < 0:
        return 0.0, 0.0
    return round((max_x - min_x) / w * 100, 1), round((max_y - min_y) / h * 100, 1)


# --------------------------------------------------------------------------- #
# backends
# --------------------------------------------------------------------------- #
def render_with_playwright(page_url: str, out: Path, scale: int, selector: str,
                           size: tuple[int, int], browser_path: str | None,
                           timeout_ms: int) -> None:
    from playwright.sync_api import sync_playwright

    width, height = max(size[0], 320), max(size[1], 240)
    with sync_playwright() as pw:
        launch: dict = {}
        if browser_path:
            launch["executable_path"] = browser_path
        browser = pw.chromium.launch(**launch)
        page = browser.new_page(
            viewport={"width": width, "height": height},
            device_scale_factor=scale,   # omit this and the capture is silently 1x
        )
        page.goto(page_url, wait_until="networkidle", timeout=timeout_ms)
        page.wait_for_timeout(300)
        try:
            page.evaluate("() => document.fonts.ready.then(() => true)")
        except Exception:
            pass
        page.wait_for_timeout(150)
        page.locator(selector).first.screenshot(path=str(out))
        browser.close()


def render_with_chrome(browser_path: str, page_url: str, out: Path, scale: int,
                       size: tuple[int, int], profile_dir: Path,
                       timeout_ms: int) -> None:
    window = f"{size[0]},{size[1]}"
    cmd = [
        browser_path,
        "--headless=new",
        "--disable-gpu",
        "--hide-scrollbars",
        "--no-first-run",
        "--no-default-browser-check",
        f"--user-data-dir={profile_dir}",
        f"--window-size={window}",
        f"--force-device-scale-factor={scale}",
        f"--screenshot={out}",
        page_url,
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True,
                          timeout=max(30, timeout_ms // 1000))
    if not out.exists() or out.stat().st_size == 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-4:]
        raise RuntimeError("chrome produced no screenshot: " + " | ".join(tail))


def render_with_wkhtmltoimage(exe: str, page_url: str, out: Path, scale: int,
                              size: tuple[int, int]) -> None:
    cmd = [
        exe,
        "--enable-local-file-access",
        "--quality", "100",
        "--width", str(size[0]),
        "--zoom", str(scale),
        page_url,
        str(out),
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=180)


# --------------------------------------------------------------------------- #
# page preparation
# --------------------------------------------------------------------------- #
def prepare_source(src: Path, pad: int, tmp: Path) -> tuple[str, tuple[int, int]]:
    """Return (file URI, logical size). SVG inputs get a zero-margin wrapper page."""
    raw = src.read_text(encoding="utf-8", errors="replace")
    if src.suffix.lower() == ".svg":
        size = svg_intrinsic_size(raw)
        if not size:
            raise SystemExit("cannot read width/height or viewBox from the SVG; add explicit pixel size")
        body = raw
        if 'xmlns="http://www.w3.org/2000/svg"' not in body:
            body = body.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
        shell = (
            "<!doctype html><meta charset=\"utf-8\">"
            "<style>html,body{margin:0;padding:0;background:#fff;}"
            "svg{display:block;}</style>"
            f"<div style=\"padding:{pad}px;background:#fff\">{body}</div>"
        )
        page = tmp / "wrap.html"
        page.write_text(shell, encoding="utf-8")
        return page.as_uri(), (size[0] + pad * 2, size[1] + pad * 2)

    size = svg_intrinsic_size(raw)
    if not size:
        size = (1520, 856)
    return src.resolve().as_uri(), size


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Render a diagram to a high-resolution PNG.")
    ap.add_argument("input", help=".html or .svg source")
    ap.add_argument("--out", required=False, help="output PNG path")
    ap.add_argument("--scale", type=int, default=2, help="2 (default) or 3")
    ap.add_argument("--min-width", type=int, default=DEFAULT_MIN_WIDTH,
                    help=f"minimum acceptable long edge in pixels (default {DEFAULT_MIN_WIDTH})")
    ap.add_argument("--selector", default="svg", help="element to capture with Playwright")
    ap.add_argument("--pad", type=int, default=0, help="padding around a standalone SVG")
    ap.add_argument("--backend", choices=("auto", "playwright", "chrome", "wkhtmltoimage"),
                    default="auto")
    ap.add_argument("--browser", default=None, help="explicit Chrome/Edge executable")
    ap.add_argument("--timeout", type=int, default=60, help="seconds")
    ap.add_argument("--json", action="store_true", help="print a JSON report only")
    ap.add_argument("--print-cmd", action="store_true", help="print the equivalent Chrome command")
    args = ap.parse_args(argv)

    src = Path(args.input).expanduser()
    if not src.is_file():
        raise SystemExit(f"input not found: {src}")
    if args.scale not in (1, 2, 3, 4):
        raise SystemExit("--scale must be 1, 2, 3 or 4")

    out = Path(args.out).expanduser() if args.out else src.with_name(f"{src.stem}@{args.scale}x.png")
    if out.suffix.lower() != ".png":
        out = out.with_suffix(".png")
    out.parent.mkdir(parents=True, exist_ok=True)

    browser = args.browser or find_browser()
    wkhtml = find_wkhtmltoimage()

    if args.print_cmd:
        size = svg_intrinsic_size(src.read_text(encoding="utf-8", errors="replace")) or (1520, 856)
        print(f'"{browser or "<chrome>"}" --headless=new --disable-gpu --hide-scrollbars '
              f'--window-size={size[0]},{size[1]} --force-device-scale-factor={args.scale} '
              f'--screenshot={out} "{src.resolve().as_uri()}"')
        return 0

    order: list[str] = []
    if args.backend == "auto":
        if have_playwright():
            order.append("playwright")
        if browser:
            order.append("chrome")
        if wkhtml:
            order.append("wkhtmltoimage")
        if not order:
            raise SystemExit("no renderer available: install playwright, or a Chrome/Edge browser, "
                             "or wkhtmltoimage")
    else:
        order = [args.backend]

    report: dict = {"input": str(src), "output": str(out), "scale": args.scale}
    tmp = Path(tempfile.mkdtemp(prefix="charta-render-"))
    errors: list[str] = []
    used = None
    size = (1520, 856)
    try:
        page_url, size = prepare_source(src, args.pad, tmp)
        report["logical"] = list(size)
        for backend in order:
            try:
                if backend == "playwright":
                    render_with_playwright(page_url, out, args.scale, args.selector, size,
                                           browser, args.timeout * 1000)
                elif backend == "chrome":
                    if not browser:
                        raise RuntimeError("no Chrome/Edge executable found")
                    render_with_chrome(browser, page_url, out, args.scale, size,
                                       tmp / "profile", args.timeout * 1000)
                elif backend == "wkhtmltoimage":
                    if not wkhtml:
                        raise RuntimeError("wkhtmltoimage not on PATH")
                    render_with_wkhtmltoimage(wkhtml, page_url, out, args.scale, size)
                used = backend
                break
            except SystemExit:
                raise
            except Exception as exc:                      # try the next backend
                errors.append(f"{backend}: {exc}")
        if used is None:
            raise SystemExit("all backends failed:\n  " + "\n  ".join(errors))

        actual = png_size(out)
        report["backend"] = used
        report["expected_px"] = [size[0] * args.scale, size[1] * args.scale]
        report["actual_px"] = list(actual) if actual else None
        ok = True
        if not actual:
            ok = False
            report["error"] = "output is not a readable PNG"
        else:
            if abs(actual[0] - report["expected_px"][0]) > 2 or \
               abs(actual[1] - report["expected_px"][1]) > 2:
                ok = False
                report["error"] = ("pixel size mismatch - device scale factor lost, or the window "
                                   "size did not match the intrinsic SVG size")
            if max(actual) < args.min_width:
                ok = False
                report.setdefault("warnings", []).append(
                    f"long edge {max(actual)}px is below --min-width {args.min_width}px")
            cover = content_coverage(out)
            if cover is None:
                report["cover_w"] = report["cover_h"] = "skipped (install pillow)"
            else:
                report["cover_w"], report["cover_h"] = cover
                if cover[0] < 95 or cover[1] < 93:
                    ok = False
                    report.setdefault("warnings", []).append(
                        "content coverage below 95%/93% - trim the viewBox or page padding")
        report["ok"] = ok

        if args.json:
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            print(f"backend  : {used}")
            print(f"logical  : {size[0]}x{size[1]}  ->  expected {report['expected_px'][0]}"
                  f"x{report['expected_px'][1]} @ {args.scale}x")
            print(f"actual   : {report['actual_px']}")
            print(f"coverage : {report.get('cover_w')} / {report.get('cover_h')}")
            for warning in report.get("warnings", []):
                print(f"WARN     : {warning}")
            print("RESULT   :", "OK" if ok else "CHECK NEEDED")
            print(f"file     : {out}")
        if errors and not args.json:
            for err in errors:
                print(f"(fallback) {err}")
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
