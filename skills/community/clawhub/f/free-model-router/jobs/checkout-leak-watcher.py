#!/usr/bin/env python3
"""Job 3: Checkout Leak Watcher — crawl meetrick.ai + Stripe links, find conversion friction."""

import json
from datetime import datetime

import requests

from helpers import call_free_model, notify, parse_json_response, save_output

URLS = [
    ("meetrick.ai homepage", "https://meetrick.ai"),
    ("meetrick.ai /pro", "https://meetrick.ai/pro"),
    ("meetrick.ai /install", "https://meetrick.ai/install"),
    ("meetrick.ai /costs", "https://meetrick.ai/costs"),
    ("Stripe: Rick Pro Monthly", "https://buy.stripe.com/9B69ATaET7vef3S9170x20t"),
    ("Stripe: Rick Pro Annual", "https://buy.stripe.com/14AbJ16oDcPy3la5OV0x20u"),
    ("Stripe: Rick LTD", "https://buy.stripe.com/9B66oHaETcPyg7Wfpv0x20v"),
    ("Railway subscribe health", "https://meetrick-subscribe-production.up.railway.app/subscribe"),
]

AUDIT_PROMPT = """Audit this page for conversion friction and issues. You're a CRO expert reviewing a SaaS product page.

URL: {url}
Status: {status_code}
Content preview: {content_preview}

Find: broken elements, missing CTAs, weak copy, unclear value prop, missing social proof, bad mobile signals.
Return JSON: {{"status": "ok|warning|critical", "issues": [...], "quick_fixes": [...], "priority": 1-10}}"""


def fetch_page(url):
    """Fetch a URL and return status code + content."""
    try:
        resp = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) RickBot/1.0",
        })
        return resp.status_code, resp.text
    except requests.ConnectionError:
        return 0, "CONNECTION_ERROR: Could not connect"
    except requests.Timeout:
        return 0, "TIMEOUT: Request timed out after 15s"
    except Exception as e:
        return 0, f"ERROR: {str(e)}"


def main():
    print(f"[watcher] Starting checkout leak watcher — {datetime.now().isoformat()}")

    results = []
    has_critical = False

    for label, url in URLS:
        print(f"[watcher] Checking: {label}")
        status_code, content = fetch_page(url)
        print(f"[watcher]   Status: {status_code}")

        # If connection failed, mark as critical immediately
        if status_code == 0:
            result = {
                "url": url,
                "label": label,
                "status_code": 0,
                "audit": {
                    "status": "critical",
                    "issues": [content],
                    "quick_fixes": ["Check if service is running"],
                    "priority": 10,
                },
            }
            results.append(result)
            has_critical = True
            print(f"[watcher]   CRITICAL: {content}")
            continue

        # Audit with free model
        content_preview = content[:2000]
        prompt = AUDIT_PROMPT.format(
            url=url,
            status_code=status_code,
            content_preview=content_preview,
        )
        response = call_free_model(prompt)
        audit = parse_json_response(response)

        if not audit:
            audit = {
                "status": "warning",
                "issues": ["Could not analyze page (model returned invalid response)"],
                "quick_fixes": [],
                "priority": 5,
            }

        result = {
            "url": url,
            "label": label,
            "status_code": status_code,
            "audit": audit,
        }
        results.append(result)

        if audit.get("status") == "critical":
            has_critical = True
            print(f"[watcher]   CRITICAL: {audit.get('issues', [])[:2]}")
        elif audit.get("status") == "warning":
            print(f"[watcher]   Warning: {audit.get('issues', [])[:1]}")
        else:
            print(f"[watcher]   OK")

    # Save report
    report = {
        "run_time": datetime.now().isoformat(),
        "pages_checked": len(URLS),
        "critical_count": sum(1 for r in results if r["audit"].get("status") == "critical"),
        "warning_count": sum(1 for r in results if r["audit"].get("status") == "warning"),
        "results": results,
    }

    date_str = datetime.now().strftime("%Y-%m-%d")
    save_output("checkout-watcher", report)

    # Notify if critical
    if has_critical:
        critical_pages = [r["label"] for r in results if r["audit"].get("status") == "critical"]
        notify(f"CRITICAL checkout issues on: {', '.join(critical_pages)}")
    else:
        print("[watcher] No critical issues found.")

    # Print summary
    print(f"\n[watcher] Summary:")
    print(f"  Pages checked: {len(URLS)}")
    print(f"  Critical: {report['critical_count']}")
    print(f"  Warnings: {report['warning_count']}")
    print(f"  OK: {len(URLS) - report['critical_count'] - report['warning_count']}")
    print("[watcher] Done.")


if __name__ == "__main__":
    main()
