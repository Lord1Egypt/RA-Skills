#!/usr/bin/env python3
import argparse
import os
import pathlib
import shutil
import sys
from urllib.parse import urlparse

try:
    from i18n import add_locale_argument, resolve_locale, t
except ModuleNotFoundError:  # Imported by the repository test suite.
    from scripts.i18n import add_locale_argument, resolve_locale, t


VIEWPORTS = {
    "desktop": (1440, 900),
    "tablet": (1024, 768),
    "mobile": (390, 844),
}


def normalize_target(target: str) -> str:
    parsed = urlparse(target)
    if parsed.scheme in {"http", "https", "file"}:
        return target
    path = pathlib.Path(target).expanduser().resolve()
    return path.as_uri()


def load_sync_playwright():
    try:
        from playwright.sync_api import sync_playwright
    except ModuleNotFoundError:
        pw_python = shutil.which("pw-python")
        if pw_python and pathlib.Path(sys.executable).name != "pw-python":
            os.execvp(pw_python, [pw_python, *sys.argv])
        raise
    return sync_playwright


def main() -> int:
    parser = argparse.ArgumentParser(
        description=t("Capture desktop, tablet, and mobile screenshots for frontend QA.", resolve_locale())
    )
    add_locale_argument(parser)
    parser.add_argument("target", help=t("URL or local HTML file path"))
    parser.add_argument("--out", default=".codex/frontend-audit", help=t("Output directory"))
    parser.add_argument("--wait-ms", type=int, default=1200, help=t("Wait after load"))
    parser.add_argument(
        "--chromium",
        default="/usr/bin/chromium",
        help=t("Chromium executable path"),
    )
    args = parser.parse_args()

    out_dir = pathlib.Path(args.out).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    target = normalize_target(args.target)
    sync_playwright = load_sync_playwright()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, executable_path=args.chromium)
        for name, (width, height) in VIEWPORTS.items():
            page = browser.new_page(viewport={"width": width, "height": height})
            page.goto(target, wait_until="networkidle")
            page.wait_for_timeout(args.wait_ms)
            screenshot = out_dir / f"{name}-{width}x{height}.png"
            page.screenshot(path=str(screenshot), full_page=True)
            print(f"{name}: {screenshot}")
            page.close()
        browser.close()

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(t("capture-audit failed: {error}", resolve_locale(), error=exc), file=sys.stderr)
        raise SystemExit(1)
