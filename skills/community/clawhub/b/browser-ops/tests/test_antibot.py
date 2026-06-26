#!/usr/bin/env python3.13
"""
Parallel anti-bot bypass test: Nodriver vs Camoufox
Tests against real anti-bot sites with 8s wait per page.
"""

import asyncio
import time
import os
import traceback

CHROME_PATH = os.path.expanduser(
    "~/.agent-browser/browsers/chrome-147.0.7727.50/"
    "Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing"
)

SITES = [
    ("nowsecure.nl", "https://nowsecure.nl"),
    ("cloudflare.com", "https://www.cloudflare.com"),
    ("fingerprint.com", "https://fingerprint.com/demo"),
]

WAIT_SECONDS = 8


# ── Nodriver tests ──────────────────────────────────────────────

async def _run_nodriver(name: str, url: str) -> dict:
    """Test a single site with nodriver (undetected-chromedriver successor)."""
    import nodriver as uc

    result = {"tool": "Nodriver", "site": name, "title": "", "length": 0,
              "status": "FAIL", "error": "", "time_s": 0}
    t0 = time.monotonic()
    browser = None
    try:
        browser = await uc.start(
            headless=True,
            browser_executable_path=CHROME_PATH,
            browser_args=["--no-sandbox", "--disable-gpu"],
        )
        page = await browser.get(url)
        await asyncio.sleep(WAIT_SECONDS)

        title = await page.evaluate("document.title")
        length = await page.evaluate("document.body.innerText.length")

        result["title"] = str(title)[:80]
        result["length"] = int(length)
        result["status"] = "PASS" if int(length) > 200 else "PARTIAL"
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {str(e)[:120]}"
        result["status"] = "ERROR"
    finally:
        result["time_s"] = round(time.monotonic() - t0, 1)
        if browser:
            try:
                browser.stop()
            except Exception:
                pass
    return result


async def run_nodriver_tests() -> list[dict]:
    """Run nodriver tests sequentially (shares browser context)."""
    results = []
    for name, url in SITES:
        r = await _run_nodriver(name, url)
        results.append(r)
    return results


# ── Camoufox tests ──────────────────────────────────────────────

def _run_camoufox_single(name: str, url: str) -> dict:
    """Test a single site with Camoufox (anti-fingerprint Firefox)."""
    from camoufox.sync_api import Camoufox

    result = {"tool": "Camoufox", "site": name, "title": "", "length": 0,
              "status": "FAIL", "error": "", "time_s": 0}
    t0 = time.monotonic()
    try:
        with Camoufox(headless=True) as browser:
            page = browser.new_page()
            page.goto(url, timeout=45000, wait_until="domcontentloaded")
            page.wait_for_timeout(WAIT_SECONDS * 1000)

            title = page.title()
            length = page.evaluate("document.body.innerText.length")

            result["title"] = str(title)[:80]
            result["length"] = int(length)
            result["status"] = "PASS" if int(length) > 200 else "PARTIAL"
    except Exception as e:
        result["error"] = f"{type(e).__name__}: {str(e)[:120]}"
        result["status"] = "ERROR"
    finally:
        result["time_s"] = round(time.monotonic() - t0, 1)
    return result


def run_camoufox_tests() -> list[dict]:
    """Run camoufox tests sequentially."""
    results = []
    for name, url in SITES:
        r = _run_camoufox_single(name, url)
        results.append(r)
    return results


# ── Main: run both in parallel ──────────────────────────────────

async def main():
    print("=" * 72)
    print("Anti-Bot Bypass Test: Nodriver vs Camoufox")
    print("=" * 72)
    print(f"Wait per page: {WAIT_SECONDS}s\n")

    # Run Camoufox in a thread (sync API) while Nodriver runs async
    loop = asyncio.get_event_loop()

    nodriver_task = asyncio.create_task(run_nodriver_tests())
    camoufox_task = loop.run_in_executor(None, run_camoufox_tests)

    nodriver_results, camoufox_results = await asyncio.gather(
        nodriver_task, camoufox_task
    )

    all_results = nodriver_results + camoufox_results

    # Print results table
    print("\n" + "=" * 72)
    print(f"{'Tool':<12} {'Site':<20} {'Status':<8} {'Title':<35} {'Len':>6} {'Time':>6}")
    print("-" * 72)
    for r in all_results:
        title_short = r["title"][:33] + ".." if len(r["title"]) > 35 else r["title"]
        print(f"{r['tool']:<12} {r['site']:<20} {r['status']:<8} {title_short:<35} {r['length']:>6} {r['time_s']:>5}s")
        if r["error"]:
            print(f"{'':>12} ERROR: {r['error']}")
    print("=" * 72)

    # Summary
    print("\n── Analysis ──")
    for name, _ in SITES:
        nd = next((r for r in nodriver_results if r["site"] == name), None)
        cf = next((r for r in camoufox_results if r["site"] == name), None)
        print(f"\n{name}:")
        if nd:
            bypass = "Bypassed" if nd["status"] == "PASS" else "Blocked/Error"
            print(f"  Nodriver:  {bypass} (len={nd['length']}, title=\"{nd['title'][:50]}\")")
        if cf:
            bypass = "Bypassed" if cf["status"] == "PASS" else "Blocked/Error"
            print(f"  Camoufox:  {bypass} (len={cf['length']}, title=\"{cf['title'][:50]}\")")


if __name__ == "__main__":
    asyncio.run(main())
