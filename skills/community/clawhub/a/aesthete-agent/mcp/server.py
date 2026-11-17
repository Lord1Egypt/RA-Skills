#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""aesthete-agent MCP server — the engine as MCP tools.

Run (FastMCP environment):
    uvx aesthete-agent-mcp            # PyPI (self-contained wheel)
    # or: uvx --from "git+https://github.com/docsor1212/aesthete-agent#subdirectory=mcp" aesthete-agent-mcp
    # or: python mcp/server.py            # stdio mode

Design (inherited from the family pattern):
- Core logic `_call_engine` shells out to scripts/palette_forge.py — single source of
  truth, no duplicated color math, works without fastmcp (safe to import for tests).
- Zero keys, zero telemetry; fully offline engine.
- Tools cover the highest-value surface: library match, generation, validation
  (scorecard / WCAG / APCA / color-blind), themes, and token exports (w3c/context).
"""
import argparse
import json
import os
import re
import subprocess
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
# 引擎解析: skill 安装树优先(单一事实源), PyPI 独立安装用捆绑副本
_ENGINE_CANDIDATES = [
    os.path.join(_HERE, "..", "scripts", "palette_forge.py"),
    os.path.join(_HERE, "server_data", "scripts", "palette_forge.py"),
]
ENGINE = next((p for p in _ENGINE_CANDIDATES if os.path.exists(p)), _ENGINE_CANDIDATES[0])

try:
    from fastmcp import FastMCP
except ImportError:  # pragma: no cover - engine calls remain available without fastmcp
    FastMCP = None


def _call_engine(args, timeout=60):
    """Run palette_forge.py with args; return (ok, text)."""
    cmd = [sys.executable, ENGINE] + [str(a) for a in args]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, "engine timeout"
    text = (r.stdout or r.stderr or "").strip()
    return r.returncode == 0, text


def _tool(fn):
    """Register a tool when FastMCP is available; expose impl regardless."""
    if FastMCP is not None:
        return mcp.tool(fn)
    return fn


def _mcp_version():
    """版本单一事实源 = mcp/pyproject.toml(数字一致性:serverInfo 不再手写)。"""
    try:
        pp = os.path.join(_HERE, "pyproject.toml")
        m = re.search(r'version\s*=\s*"([^"]+)"', open(pp, encoding="utf-8").read())
        return m.group(1) if m else "0.0.0"
    except Exception:
        return "0.0.0"


def palette_match_impl(brief: str, limit: int = 6, no_flags: bool = False) -> str:
    """Rank the 118-palette evidence library for a natural-language brief.
    Auto-detects register, applies learned preference penalties, sorts by endorsement tiers."""
    args = ["match", "--brief", brief, "--limit", str(limit)]
    if no_flags:
        args.append("--no-flags")
    ok, text = _call_engine(args)
    return text


def palette_harmony_impl(base: str, mode: str = "analogous", theme: str = "light") -> str:
    """Generate an OKLCH harmony palette from a seed color (7 rules x light/dark)."""
    ok, text = _call_engine(["harmony", "--base", base, "--mode", mode, "--theme", theme])
    return text


def palette_score_impl(palette: str) -> str:
    """5-dimension scorecard (/20) with P0-P3 findings: architecture, readability,
    CB-safety, saturation discipline, uniqueness. Exit non-zero = untrustworthy."""
    ok, text = _call_engine(["score", "--palette", palette])
    return text


def palette_contrast_impl(fg: str, bg: str, method: str = "wcag") -> str:
    """Contrast for one fg/bg pair. method='apca' uses the APCA 0.1.9 perceptual
    algorithm (WCAG 3 draft direction; Lc>=75 body, >=60 large, >=45 bold)."""
    ok, text = _call_engine(["contrast", "--fg", fg, "--bg", bg, "--method", method])
    return text


def palette_matrix_impl(palette: str, method: str = "wcag", recommend: bool = True) -> str:
    """Full pairwise contrast matrix (WCAG ratios or APCA Lc) + best-pair recommendation."""
    args = ["matrix", "--palette", palette, "--method", method]
    if recommend:
        args.append("--recommend")
    ok, text = _call_engine(args)
    return text


def palette_blind_impl(palette: str) -> str:
    """Simulate protanopia/deuteranopia/tritanopia; flags collision risk."""
    ok, text = _call_engine(["blind", "--palette", palette])
    return text


def palette_semantic_impl(count: int = 8, base: str = "") -> str:
    """Color-blind-safe categorical colors for charts: interleaved luminance ramp +
    evenly spread hues, verified >=0.08 min separation under deuteranopia."""
    args = ["semantic", "--count", str(count)]
    if base:
        args += ["--base", base]
    ok, text = _call_engine(args)
    return text


def palette_themes_impl() -> str:
    """List named theme packs (colors + fonts + voice + use-when), all dogfood-proven."""
    ok, text = _call_engine(["themes"])
    return text


def palette_theme_impl(name: str, fmt: str = "css") -> str:
    """Emit a named theme as CSS custom properties (or full JSON)."""
    ok, text = _call_engine(["theme", name, "--format", fmt])
    return text


def palette_export_impl(palette: str, fmt: str = "css") -> str:
    """Export tokens: css | tailwind | json | svg | w3c (W3C Design Tokens) |
    context (paste-ready color-system context for any LLM)."""
    ok, text = _call_engine(["export", "--palette", palette, "--format", fmt])
    return text


def palette_slop_impl(palette: str) -> str:
    """Detect AI-slop signatures: training-median hexes, purple gradients,
    flat lightness, all-loud palettes."""
    ok, text = _call_engine(["slop", "--palette", palette])
    return text


def palette_report_impl(palette: str) -> str:
    """One-shot acceptance artifact: contrast / color-blind / AI-slop / scorecard
    gates aggregated into a single PASS/FAIL JSON. Exit code = verdict."""
    ok, text = _call_engine(["report", "--palette", palette])
    return text


def palette_visualize_impl(palette: str, out: str = "visualizer.html", theme: str = "") -> str:
    """Render the palette into 6 realistic UI scenes (mobile, landing, dashboard,
    branding, typography, pattern) with derived roles and legibility gates;
    optionally recolor an SVG keeping pure black/white."""
    args = ["visualize", "--palette", palette, "--out", out]
    if theme:
        args += ["--theme", theme]
    ok, text = _call_engine(args)
    return text


def palette_directions_impl(brief: str = "", registers: str = "", n: int = 3,
                            out_dir: str = "directions") -> str:
    """Cross-register design directions: whole-page candidates from different register
    families side by side (difference enforced), each with metadata + a pick-back sentence."""
    args = ["directions", "--n", str(n), "--out-dir", out_dir]
    if registers:
        args += ["--registers", registers]
    elif brief:
        args += ["--brief", brief]
    ok, text = _call_engine(args)
    return text


def palette_evidence_impl(page: str, palette: str, render: str = "", out: str = "") -> str:
    """Evidence dossier for a finished page: four mechanical gates + static lint
    (+ optional render-probe JSON) aggregated into one PASS/FAIL verdict record."""
    args = ["evidence", page, "--palette", palette]
    if render:
        args += ["--render", render]
    if out:
        args += ["--out", out]
    ok, text = _call_engine(args)
    return text


def palette_tokens_impl(palette: str = "", theme: str = "", name: str = "",
                        dark: bool = False, out: str = "") -> str:
    """Full semantic design-token sheet (CSS + JSON): color roles auto-tuned to
    contrast, accent split into graphic/text variants, space/radius/motion tokens,
    measured ratios as comments. Give `palette` (comma hex) or `theme` (pack name)."""
    if palette:
        args = ["tokens", "--palette", palette]
    elif theme:
        args = ["tokens", "--theme", theme]
    else:
        return "error: palette or theme required"
    if name:
        args += ["--name", name]
    if dark:
        args += ["--dark"]
    if out:
        args += ["--out", out]
    ok, text = _call_engine(args)
    return text


def palette_audit_impl(page: str, palette: str = "", floor: float = 12.0, out: str = "") -> str:
    """Mechanical audit of an EXISTING page: palette drift (nearest-library
    replacements), gradient ban, purple-background guard, contrast pairs with
    tuned fix values, font floor, AI-default signatures. FAIL on P0 or P1>=2."""
    args = ["audit", page]
    if palette:
        args += ["--palette", palette]
    args += ["--floor", floor]
    if out:
        args += ["--out", out]
    ok, text = _call_engine(args)
    return text


def palette_chartpal_impl(kind: str, palette: str = "", theme: str = "",
                          series: int = 6, out: str = "") -> str:
    """Chart palette derivation: categorical (CVD-optimized series colors),
    sequential (single-hue lightness ramp) or diverging (two hues, neutral
    midpoint). Emits JSON + annotated swatch HTML; exit reflects verdict."""
    args = ["chartpal", "--kind", kind]
    if palette:
        args += ["--palette", palette]
    elif theme:
        args += ["--theme", theme]
    args += ["--series", series]
    if out:
        args += ["--out", out]
    ok, text = _call_engine(args)
    return text


def palette_typescale_impl(base: float = 16.0, ratio: float = 1.25,
                           name: str = "", out: str = "") -> str:
    """CJK-friendly modular type scale (12px floor, line-height pairing,
    tabular-nums token) as CSS + specimen HTML + JSON."""
    args = ["typescale", "--base", base, "--ratio", ratio]
    if name:
        args += ["--name", name]
    if out:
        args += ["--out", out]
    ok, text = _call_engine(args)
    return text


def palette_qc_impl(image: str, tokens: str = "", palette: str = "",
                    bg: str = "", out: str = "") -> str:
    """Reconcile a rendered screenshot against declared tokens/palette:
    background authenticity and off-palette intrusions, digest-bound JSON.
    The mechanical gate of the render feedback loop."""
    args = ["qc", image]
    if tokens:
        args += ["--tokens", tokens]
    elif palette:
        args += ["--palette", palette]
    if bg:
        args += ["--bg", bg]
    if out:
        args += ["--out", out]
    ok, text = _call_engine(args)
    return text


def palette_narrate_impl(palette: str = "", theme: str = "",
                         name: str = "", out: str = "") -> str:
    """Measured-numbers-only bilingual rationale from the report gates
    (contrast pair, blind sims, slop scan, score, fingerprint) — every number
    traceable, template sentences, zero invented claims."""
    if palette:
        args = ["narrate", "--palette", palette]
    elif theme:
        args = ["narrate", "--theme", theme]
    else:
        return "error: palette or theme required"
    if name:
        args += ["--name", name]
    if out:
        args += ["--out", out]
    ok, text = _call_engine(args)
    return text


if FastMCP is not None:
    mcp = FastMCP("aesthete-agent")

    _tool(palette_match_impl)
    _tool(palette_harmony_impl)
    _tool(palette_score_impl)
    _tool(palette_contrast_impl)
    _tool(palette_matrix_impl)
    _tool(palette_blind_impl)
    _tool(palette_semantic_impl)
    _tool(palette_themes_impl)
    _tool(palette_theme_impl)
    _tool(palette_export_impl)
    _tool(palette_slop_impl)
    _tool(palette_visualize_impl)
    _tool(palette_report_impl)
    _tool(palette_directions_impl)
    _tool(palette_evidence_impl)
    _tool(palette_tokens_impl)
    _tool(palette_audit_impl)
    _tool(palette_chartpal_impl)
    _tool(palette_typescale_impl)
    _tool(palette_qc_impl)
    _tool(palette_narrate_impl)



# ---- pure-stdlib stdio transport (fallback when fastmcp is absent) ----
_STDIO_TOOLS = [
    ("palette_match", "Rank the evidence palette library for a design brief",
     {"brief": {"type": "string"}, "limit": {"type": "number"}}, ["brief"]),
    ("palette_harmony", "Generate an OKLCH harmony from a base hex",
     {"base": {"type": "string"}, "mode": {"type": "string"}, "theme": {"type": "string"}}, ["base"]),
    ("palette_score", "5-dimension scorecard /20 for a palette",
     {"palette": {"type": "string"}}, ["palette"]),
    ("palette_contrast", "WCAG/APCA contrast for fg+bg with fix suggestions",
     {"fg": {"type": "string"}, "bg": {"type": "string"}, "method": {"type": "string"}}, ["fg", "bg"]),
    ("palette_matrix", "Full pairwise contrast matrix",
     {"palette": {"type": "string"}, "method": {"type": "string"}, "recommend": {"type": "boolean"}}, ["palette"]),
    ("palette_blind", "Three color-blindness simulations with collision checks",
     {"palette": {"type": "string"}}, ["palette"]),
    ("palette_semantic", "CB-safe categorical data colors",
     {"count": {"type": "number"}, "base": {"type": "string"}}, []),
    ("palette_themes", "List named theme packs", {}, []),
    ("palette_theme", "Emit a named theme pack as css/json tokens",
     {"name": {"type": "string"}, "fmt": {"type": "string"}}, ["name"]),
    ("palette_export", "Export palette as css/tailwind/json/w3c/context",
     {"palette": {"type": "string"}, "fmt": {"type": "string"}}, ["palette"]),
    ("palette_slop", "AI-slop signature detection (exit-code enforced)",
     {"palette": {"type": "string"}}, ["palette"]),
    ("palette_visualize", "Render palette into 11 realistic UI scenes (+svg recolor)",
     {"palette": {"type": "string"}, "out": {"type": "string"}, "theme": {"type": "string"}}, ["palette"]),
    ("palette_report", "One-shot acceptance artifact: 4 mechanical gates, PASS/FAIL",
     {"palette": {"type": "string"}}, ["palette"]),
    ("palette_directions", "Cross-register whole-page design directions with pick-back sentences",
     {"brief": {"type": "string"}, "registers": {"type": "string"}, "n": {"type": "number"},
      "out_dir": {"type": "string"}}, []),
    ("palette_evidence", "Evidence dossier: 4 gates + lint (+render probe) for a finished page",
     {"page": {"type": "string"}, "palette": {"type": "string"}, "render": {"type": "string"},
      "out": {"type": "string"}}, ["page", "palette"]),
    ("palette_tokens", "Semantic design-token sheet (CSS+JSON) with contrast-tuned inks",
     {"palette": {"type": "string"}, "theme": {"type": "string"}, "name": {"type": "string"},
      "dark": {"type": "boolean"}, "out": {"type": "string"}}, []),
    ("palette_audit", "Mechanical audit of an existing page with concrete fix values",
     {"page": {"type": "string"}, "palette": {"type": "string"}, "floor": {"type": "number"},
      "out": {"type": "string"}}, ["page"]),
    ("palette_chartpal", "Chart palette: CVD-checked categorical / sequential / diverging",
     {"kind": {"type": "string"}, "palette": {"type": "string"}, "theme": {"type": "string"},
      "series": {"type": "number"}, "out": {"type": "string"}}, ["kind"]),
    ("palette_typescale", "CJK-friendly modular type scale (CSS + specimen)",
     {"base": {"type": "number"}, "ratio": {"type": "number"}, "name": {"type": "string"},
      "out": {"type": "string"}}, []),
    ("palette_qc", "Reconcile rendered screenshot vs declared tokens (bg truth / intruders)",
     {"image": {"type": "string"}, "tokens": {"type": "string"}, "palette": {"type": "string"},
      "bg": {"type": "string"}, "out": {"type": "string"}}, ["image"]),
    ("palette_narrate", "Bilingual measured-numbers rationale from report gates",
     {"palette": {"type": "string"}, "theme": {"type": "string"}, "name": {"type": "string"},
      "out": {"type": "string"}}, []),
]


def _stdio_serve():
    """MCP stdio JSON-RPC loop in pure stdlib — zero-dependency fallback."""
    dispatch = {
        "palette_match": lambda a: palette_match_impl(a.get("brief", ""), int(a.get("limit", 6))),
        "palette_harmony": lambda a: palette_harmony_impl(a.get("base", ""), a.get("mode", "analogous"), a.get("theme", "light")),
        "palette_score": lambda a: palette_score_impl(a.get("palette", "")),
        "palette_contrast": lambda a: palette_contrast_impl(a.get("fg", ""), a.get("bg", ""), a.get("method", "wcag")),
        "palette_matrix": lambda a: palette_matrix_impl(a.get("palette", ""), a.get("method", "wcag"), bool(a.get("recommend", True))),
        "palette_blind": lambda a: palette_blind_impl(a.get("palette", "")),
        "palette_semantic": lambda a: palette_semantic_impl(int(a.get("count", 8)), a.get("base", "")),
        "palette_themes": lambda a: palette_themes_impl(),
        "palette_theme": lambda a: palette_theme_impl(a.get("name", ""), a.get("fmt", "css")),
        "palette_export": lambda a: palette_export_impl(a.get("palette", ""), a.get("fmt", "css")),
        "palette_slop": lambda a: palette_slop_impl(a.get("palette", "")),
        "palette_visualize": lambda a: palette_visualize_impl(a.get("palette", ""), a.get("out", "visualizer.html"), a.get("theme", "")),
        "palette_report": lambda a: palette_report_impl(a.get("palette", "")),
        "palette_directions": lambda a: palette_directions_impl(
            a.get("brief", ""), a.get("registers", ""), int(a.get("n", 3)), a.get("out_dir", "directions")),
        "palette_evidence": lambda a: palette_evidence_impl(
            a.get("page", ""), a.get("palette", ""), a.get("render", ""), a.get("out", "")),
        "palette_tokens": lambda a: palette_tokens_impl(
            a.get("palette", ""), a.get("theme", ""), a.get("name", ""),
            bool(a.get("dark", False)), a.get("out", "")),
        "palette_audit": lambda a: palette_audit_impl(
            a.get("page", ""), a.get("palette", ""), float(a.get("floor", 12.0)), a.get("out", "")),
        "palette_chartpal": lambda a: palette_chartpal_impl(
            a.get("kind", "categorical"), a.get("palette", ""), a.get("theme", ""),
            int(a.get("series", 6)), a.get("out", "")),
        "palette_typescale": lambda a: palette_typescale_impl(
            float(a.get("base", 16.0)), float(a.get("ratio", 1.25)),
            a.get("name", ""), a.get("out", "")),
        "palette_qc": lambda a: palette_qc_impl(
            a.get("image", ""), a.get("tokens", ""), a.get("palette", ""),
            a.get("bg", ""), a.get("out", "")),
        "palette_narrate": lambda a: palette_narrate_impl(
            a.get("palette", ""), a.get("theme", ""), a.get("name", ""), a.get("out", "")),
    }
    tools = [{"name": n, "description": (d.strip() if d else n),
              "inputSchema": {"type": "object", "properties": props, "required": req}}
             for n, d, props, req in _STDIO_TOOLS]

    def respond(mid, result=None, error=None):
        msg = {"jsonrpc": "2.0", "id": mid}
        if error is not None:
            msg["error"] = error
        else:
            msg["result"] = result if result is not None else {}
        sys.stdout.write(json.dumps(msg) + "\n")
        sys.stdout.flush()

    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        try:
            msg = json.loads(raw)
        except ValueError:
            continue
        method = msg.get("method")
        mid = msg.get("id")
        if method == "initialize":
            respond(mid, {"protocolVersion": msg.get("params", {}).get("protocolVersion", "2025-06-18"),
                          "capabilities": {"tools": {}},
                          "serverInfo": {"name": "aesthete-agent-mcp", "version": _mcp_version()}})
        elif method == "notifications/initialized" or mid is None:
            continue
        elif method == "ping":
            respond(mid, {})
        elif method == "tools/list":
            respond(mid, {"tools": tools})
        elif method == "tools/call":
            params = msg.get("params", {}) or {}
            name = params.get("name")
            try:
                text = dispatch[name](params.get("arguments", {}) or {})
                respond(mid, {"content": [{"type": "text", "text": str(text)}]})
            except KeyError:
                respond(mid, error={"code": -32602, "message": f"unknown tool: {name}"})
            except Exception as e:
                respond(mid, {"content": [{"type": "text", "text": f"error: {e}"}], "isError": True})
        else:
            respond(mid, error={"code": -32601, "message": f"method not found: {method}"})
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="import/impl self-check, no server")
    ap.add_argument("--stdio", action="store_true", help="force pure-stdlib stdio MCP transport")
    a = ap.parse_args(argv)
    if a.check:
        ok, text = _call_engine(["selftest"])
        print("engine selftest:", "OK" if ok else "FAIL")
        n = len(_STDIO_TOOLS) if FastMCP is not None else 0
        print("tools exposed:", n, "(fastmcp",
              "available)" if FastMCP is not None else "NOT installed — impl-only mode)")
        return 0 if ok else 1
    if FastMCP is None or a.stdio:
        return _stdio_serve()  # zero-dependency stdio MCP (MCPB bundles / bare venvs)
    mcp.run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
