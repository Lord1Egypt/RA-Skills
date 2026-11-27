#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Measure A4 page fill for a one-pager HTML, and gate the result.

Why this exists: "顺序填满一页、溢出单位整体下移" is only enforceable if the
fill ratio is measured. Before this script the check was a manual step in
onepager-render/SKILL.md (inject script -> --dump-dom -> read MEASURE::),
which nobody re-ran; empty half pages shipped.

Usage:
    python measure_fill.py <file.html> [--gate 900] [--chrome PATH]
                           [--pdf] [--json]

Only two values reach the command line: an existing absolute executable path,
and the file:// URI of a temp copy inside a private temp dir. Both are
validated before use; the browser is never run through a shell.
"""

import argparse
import html as html_mod
import json
import os
import re
# Launches the local browser only: fixed argv shape, shell never used.
import subprocess  # nosec B404
import sys
import tempfile
from pathlib import Path

DEFAULT_GATE = 900          # px, per onepager-render/SKILL.md
BOTTOM_PAD_PX = 64          # 17mm bottom padding at 96dpi

INJECT = """
<script>
(function(){
  function run(){
    var out=[];
    document.querySelectorAll('.page').forEach(function(pg,i){
      var rect=pg.getBoundingClientRect();
      var top=rect.top, bottom=top, last='';
      pg.querySelectorAll('*').forEach(function(el){
        if(el.closest('.footer')) return;
        var r=el.getBoundingClientRect();
        if(r.width===0 && r.height===0) return;
        if(r.bottom>bottom){ bottom=r.bottom; last=el.tagName.toLowerCase()+(el.className?('.'+String(el.className).split(' ')[0]):''); }
      });
      out.push({page:i+1, contentBottom:Math.round(bottom-top), pageHeight:Math.round(rect.height), lastEl:last});
    });
    var pre=document.createElement('pre');
    pre.id='__measure';
    pre.textContent='MEASURE::'+JSON.stringify({pages:out, printMedia:matchMedia('print').matches});
    document.body.appendChild(pre);
  }
  if(document.readyState==='complete'){run();}else{window.addEventListener('load',run);}
})();
</script>
"""

CANDIDATES = (
    os.environ.get("CHROME_PATH", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/usr/bin/google-chrome",
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
)


def find_browser(explicit=None):
    """Return an existing absolute executable path, or None."""
    candidate = explicit or next((c for c in CANDIDATES if c and Path(c).is_file()), None)
    if not candidate:
        return None
    p = Path(candidate)
    if not p.is_file():
        return None
    p = p.resolve()
    return str(p) if p.is_absolute() else None


def inject(src: str) -> str:
    src = src.replace("</head>", '<meta name="measure" content="print">\n</head>', 1)
    if "</body>" in src:
        return src.replace("</body>", INJECT + "\n</body>", 1)
    return src + INJECT


def dump_dom(browser_path: str, workdir: str) -> str:
    """Dump the DOM of ./measure.html inside workdir."""
    target = Path(browser_path)
    if not target.is_absolute() or not target.is_file():
        raise ValueError("browser must be an existing absolute path")
    page_uri = (Path(workdir) / "measure.html").as_uri()
    if not page_uri.startswith("file:///"):
        raise ValueError("refusing non-local URI")
    # argv is a literal list; only validated paths are interpolated, shell=False.
    proc = subprocess.run(  # nosec B603
        [browser_path, "--headless=new", "--disable-gpu", "--no-first-run",
         "--no-default-browser-check", "--hide-scrollbars",
         "--force-device-scale-factor=1", "--virtual-time-budget=5000",
         "--dump-dom", page_uri],
        cwd=workdir, capture_output=True, timeout=120, shell=False)
    if proc.returncode != 0:
        raise RuntimeError(
            "browser exited " + str(proc.returncode) + ": "
            + proc.stderr.decode("utf-8", "replace")[:300])
    return proc.stdout.decode("utf-8", "replace")


def print_pdf(browser_path: str, workdir: str):
    """Render ./measure.html to out.pdf inside workdir (relative path, no interpolation)."""
    target = Path(browser_path)
    if not target.is_absolute() or not target.is_file():
        raise ValueError("browser must be an existing absolute path")
    page_uri = (Path(workdir) / "measure.html").as_uri()
    if not page_uri.startswith("file:///"):
        raise ValueError("refusing non-local URI")
    # argv is a literal list; the PDF name is a fixed relative path.
    subprocess.run(  # nosec B603
        [browser_path, "--headless=new", "--disable-gpu", "--no-first-run",
         "--no-default-browser-check", "--print-to-pdf=out.pdf",
         "--no-pdf-header-footer", page_uri],
        cwd=workdir, capture_output=True, timeout=120, shell=False)


def dump_measure(browser, workdir):
    dom = dump_dom(browser, workdir)
    m = re.search(r"MEASURE::(\{.*?\})</pre>", dom, flags=re.S)
    if not m:
        raise RuntimeError("MEASURE block not found; page may block scripts")
    return json.loads(html_mod.unescape(m.group(1)))


def pdf_pages(browser, workdir):
    print_pdf(browser, workdir)
    out = Path(workdir) / "out.pdf"
    if not out.exists():
        return None
    return len(re.findall(rb"/Type\s*/Page[^s]", out.read_bytes()))


def measure(src_path, gate: int = DEFAULT_GATE, chrome: str = None,
            want_pdf: bool = False) -> dict:
    """Measure a file and return {file, gate, pages, printPages, browser}.

    Raises ValueError when the input cannot be measured (no browser, no .page).
    """
    path = Path(src_path)
    if not path.is_file():
        raise ValueError(f"file not found: {path}")

    browser = find_browser(chrome)
    if not browser:
        raise ValueError("Chrome/Edge not found; pass --chrome <path> or set CHROME_PATH")

    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "measure.html").write_text(
            inject(path.read_text(encoding="utf-8")), encoding="utf-8")
        data = dump_measure(browser, td)
        pdf_n = pdf_pages(browser, td) if want_pdf else None
        pages = data["pages"]

    if not pages:
        raise ValueError("no .page element found")

    rows = []
    for p in pages:
        usable = p["pageHeight"] - BOTTOM_PAD_PX
        fill = p["contentBottom"] / usable * 100 if usable else 0
        is_last = p["page"] == len(pages)
        ok = is_last or p["contentBottom"] >= gate
        rows.append({**p, "usable": usable, "fillPct": round(fill, 1),
                     "isLast": is_last, "pass": ok})
    return {"file": str(path), "gate": gate, "pages": rows,
            "printPages": pdf_n, "browser": browser}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--gate", type=int, default=DEFAULT_GATE)
    ap.add_argument("--chrome", default=None)
    ap.add_argument("--pdf", action="store_true", help="also print and count PDF pages")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        result = measure(args.file, gate=args.gate, chrome=args.chrome, want_pdf=args.pdf)
    except Exception as e:
        print(f"[FAIL] {e}", file=sys.stderr)
        return 2

    rows, pdf_n = result["pages"], result["printPages"]
    src_path = Path(result["file"])
    failed = any(not r["pass"] for r in rows)

    if args.json:
        print(json.dumps({"file": str(src_path), "gate": args.gate,
                          "pages": rows, "printPages": pdf_n}, ensure_ascii=False, indent=2))
    else:
        print("== measure_fill ==")
        print(f"file   : {src_path.name}")
        print(f"browser: {result['browser']}")
        print(f"gate   : non-last page contentBottom >= {args.gate}px")
        print()
        print(f"{'page':<6}{'bottom':>8}{'usable':>8}{'fill':>8}   result")
        for r in rows:
            tag = "last (no gate)" if r["isLast"] else ("PASS" if r["pass"] else "FAIL low fill")
            print(f"{r['page']:<6}{r['contentBottom']:>8}{r['usable']:>8}{str(r['fillPct'])+'%':>8}   {tag}")
        if pdf_n is not None:
            print(f"\nprint pages: {pdf_n}")
        print()

    if failed:
        print(f"[FAIL] a non-last page is below {args.gate}px — move the next unit up, "
              f"do not shrink type or line-height.")
        return 1
    print("[PASS] fill gate satisfied")
    return 0


if __name__ == "__main__":
    sys.exit(main())
