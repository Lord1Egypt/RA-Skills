#!/usr/bin/env python3
"""Link freshness checker for content-claim-navigator.

Run daily via cron/CI in an environment with normal network egress:
    python3 scripts/check_links.py

Reads every official URL from references/links.md, fetches each,
records HTTP status and a content fingerprint, diffs against the
previous run (scripts/link_state.json), and appends a dated,
human-readable summary to references/freshness-log.md.

This script only detects change and reachability. It never rewrites
skill content: a detected change is a prompt for human re-verification
per S-08, not an automatic update. Nothing unverified enters the
skill.
"""

import hashlib
import json
import re
import sys
import urllib.request
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINKS_FILE = ROOT / "references" / "links.md"
STATE_FILE = Path(__file__).resolve().parent / "link_state.json"
LOG_FILE = ROOT / "references" / "freshness-log.md"

URL_PATTERN = re.compile(
    r"\b((?:support\.google\.com|youtube\.com|www\.youtube\.com|"
    r"facebook\.com|www\.facebook\.com|business\.facebook\.com|"
    r"tiktok\.com|www\.tiktok\.com|support\.tiktok\.com)"
    r"/[\w\-./?=&%]+)"
)

HEADERS = {"User-Agent": "Mozilla/5.0 (content-claim-navigator link check)"}
TIMEOUT = 20
FINGERPRINT_BYTES = 65536


def extract_urls(text: str) -> list[str]:
    seen, urls = set(), []
    for match in URL_PATTERN.finditer(text):
        url = "https://" + match.group(1).rstrip(".,)")
        if url not in seen:
            seen.add(url)
            urls.append(url)
    return urls


def check(url: str) -> dict:
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            body = resp.read(FINGERPRINT_BYTES)
            return {
                "status": resp.status,
                "fingerprint": hashlib.sha256(body).hexdigest()[:16],
                "final_url": resp.geturl(),
                "error": None,
            }
    except Exception as exc:  # noqa: BLE001 - report, don't crash the sweep
        return {"status": None, "fingerprint": None,
                "final_url": None, "error": str(exc)[:200]}


def main() -> int:
    if not LINKS_FILE.exists():
        print(f"missing {LINKS_FILE}", file=sys.stderr)
        return 1
    urls = extract_urls(LINKS_FILE.read_text(encoding="utf-8"))
    previous = {}
    if STATE_FILE.exists():
        previous = json.loads(STATE_FILE.read_text(encoding="utf-8"))

    current, changed, unreachable, new = {}, [], [], []
    for url in urls:
        result = check(url)
        current[url] = result
        prior = previous.get(url)
        if result["error"] or (result["status"] and result["status"] >= 400):
            unreachable.append((url, result["error"] or result["status"]))
        elif prior is None:
            new.append(url)
        elif prior.get("fingerprint") != result["fingerprint"]:
            changed.append(url)

    STATE_FILE.write_text(json.dumps(current, indent=2), encoding="utf-8")

    today = date.today().isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [f"\n## Sweep {stamp}", f"- Checked {len(urls)} links."]
    if not (changed or unreachable or new):
        lines.append("- All reachable, no content changes detected.")
    if new:
        lines.append(f"- Newly tracked ({len(new)}): " + "; ".join(new))
    if changed:
        lines.append(
            f"- CONTENT CHANGED ({len(changed)}), re-verify per S-08 "
            f"before next surfacing: " + "; ".join(changed))
    if unreachable:
        lines.append(
            f"- UNREACHABLE ({len(unreachable)}), do not surface until "
            f"re-verified: "
            + "; ".join(f"{u} ({e})" for u, e in unreachable))
    with LOG_FILE.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print(f"[{today}] {len(urls)} checked, {len(changed)} changed, "
          f"{len(unreachable)} unreachable, {len(new)} new")
    return 0


if __name__ == "__main__":
    sys.exit(main())
