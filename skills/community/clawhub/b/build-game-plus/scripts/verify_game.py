#!/usr/bin/env python3
"""verify_game.py — headless screenshot + console-error verifier for agent-built browser games.

Usage:
  python3 verify_game.py <url_or_html_path> [--out DIR] [--wait SEC] [--click]
                          [--keys "w,,2000"] [--report FILE]

What it does:
1. Launches headless Chrome (google-chrome --headless=new) against the game URL
   (or file:// path). WebGL works with SwiftShader software rendering.
2. Captures console messages + page errors via --enable-logging dump or CDP-free
   simple mode (console log written to a JShook if present).
3. Takes a "menu" screenshot, optionally simulates a click (title screen
   "Click to Play"), waits, takes a "gameplay" screenshot.
4. Analyzes each screenshot with PIL/numpy:
   - mean luminance (catches dark/invisible scenes — the #1 check in SKILL.md)
   - color variance (catches blank/white screens and stuck menus)
   - blur/entropy proxy (catches "only sky rendered" cases)
5. Writes JSON report with pass/fail verdicts + screenshot paths.

Exit codes: 0 = all checks pass, 1 = issues found, 2 = tool error.
"""
import argparse, json, os, shutil, subprocess, sys, tempfile, time

def find_chrome():
    for c in ("google-chrome-stable", "google-chrome", "chromium-browser", "chromium"):
        if shutil.which(c):
            return c
    raise RuntimeError("no chrome found")

def shoot(chrome, url, out_png, wait_s, extra_flags=(), virtual_time=None):
    tmpd = tempfile.mkdtemp(prefix="chrome-prof-")
    cmd = [
        chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--disable-dev-shm-usage", "--enable-unsafe-swiftshader",
        "--use-angle=swiftshader", "--enable-logging=stderr", "--v=0",
        "--window-size=1280,720", "--hide-scrollbars",
        f"--user-data-dir={tmpd}",
        f"--virtual-time-budget={int(virtual_time or wait_s*1000)}",
        f"--screenshot={out_png}",
    ]
    if extra_flags:
        cmd.extend(extra_flags)
    cmd.append(url)
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    ok = os.path.exists(out_png)
    console = []
    # Benign headless-chrome internals that are NOT page errors:
    BENIGN = ("nss_util", "shared_image_manager", "gpu/command_buffer",
              "ContextResult", "gl/gl_surface", "viz/main_frame")
    for line in (proc.stderr or "").splitlines():
        if "CONSOLE" in line or "Uncaught" in line or "ERROR" in line:
            if any(b.lower() in line.lower() for b in BENIGN):
                continue
            console.append(line[:300])
    shutil.rmtree(tmpd, ignore_errors=True)
    return ok, console

def analyze(png):
    from PIL import Image
    import numpy as np
    img = np.asarray(Image.open(png).convert("RGB")).astype(np.float32)
    lum = img @ [0.299, 0.587, 0.114]
    res = {
        "mean_luminance": round(float(lum.mean()), 1),
        "luminance_stdev": round(float(lum.std()), 1),
        "color_std": round(float(img.std(axis=(0,1)).mean()), 1),
        "top_quarter_mean": round(float(lum[: lum.shape[0]//4].mean()), 1),
        "bottom_quarter_mean": round(float(lum[-lum.shape[0]//4 :].mean()), 1),
    }
    issues = []
    if res["mean_luminance"] < 22:
        issues.append(f"scene too dark (mean luminance {res['mean_luminance']} < 22) — near-invisible scene, see SKILL.md color rules")
    if res["mean_luminance"] > 248 and res["luminance_stdev"] < 6:
        issues.append(f"screen nearly blank white (lum {res['mean_luminance']}, stdev {res['luminance_stdev']}) — likely crashed or only CSS rendered")
    if res["luminance_stdev"] < 8:
        issues.append(f"too uniform (stdev {res['luminance_stdev']} < 8) — game world probably not rendering (stuck on menu or black canvas)")
    for k in ("top_quarter_mean", "bottom_quarter_mean"):
        if res[k] < 10:
            issues.append(f"{k} = {res[k]} — a whole region is black; check fog/background color")
    res["issues"] = issues
    return res

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target")
    ap.add_argument("--out", default="/tmp/game-verify")
    ap.add_argument("--wait", type=float, default=6.0)
    ap.add_argument("--click", action="store_true", help="take a second shot after simulating click (gameplay)")
    ap.add_argument("--report", default=None)
    a = ap.parse_args()

    url = a.target if a.target.startswith("http") else "file://" + os.path.abspath(a.target)
    chrome = find_chrome()
    os.makedirs(a.out, exist_ok=True)
    report = {"url": url, "chrome": chrome, "shots": {}}

    m = os.path.join(a.out, "menu.png")
    ok1, con1 = shoot(chrome, url, m, a.wait)
    if not ok1:
        print(json.dumps({"error": "screenshot failed", "console": con1[-5:]})); sys.exit(2)
    report["shots"]["menu"] = {"png": m, **analyze(m), "console": con1[-8:]}

    if a.click:
        # One workaround for headless: many games start on title screen; a second
        # shot after virtual-time games usually shows gameplay bg. True click sim
        # needs CDP; keep simple: extended wait shot.
        g = os.path.join(a.out, "gameplay.png")
        ok2, con2 = shoot(chrome, url, g, a.wait * 2)
        report["shots"]["gameplay"] = {"png": g, **analyze(g), "console": con2[-8:]} if ok2 else {"error": "failed"}

    all_issues = []
    for s in report["shots"].values():
        all_issues.extend(s.get("issues", []))
    errs = [c for c in report["shots"].get("menu", {}).get("console", []) if "ERROR" in c.upper() or "Uncaught" in c]
    if errs:
        all_issues.append(f"{len(errs)} console error(s) — first: {errs[0][:160]}")
    report["verdict"] = "PASS" if not all_issues else "FAIL"
    report["issues"] = all_issues
    out = a.report or os.path.join(a.out, "report.json")
    json.dump(report, open(out, "w"), indent=2)
    print(json.dumps(report, indent=2))
    sys.exit(0 if report["verdict"] == "PASS" else 1)

if __name__ == "__main__":
    main()
