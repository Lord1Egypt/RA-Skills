#!/usr/bin/env python3
"""Deals notification service: runs the tilbudsavis scraper and pushes the
weekly summary to ntfy.sh. Dedupes per day so re-runs don't spam."""
import datetime
import json
import pathlib
import subprocess
import sys
import tempfile

BASE = pathlib.Path(__file__).resolve().parent
CONFIG = json.loads((BASE / "config.json").read_text(encoding="utf-8"))
NTFY = CONFIG["ntfy"]
STATE_FILE = BASE / "state.json"
TODAY = datetime.date.today().isoformat()


def run_scraper() -> str:
    p = subprocess.run(
        ["python3", str(BASE / "tilbudsavis.py")],
        capture_output=True, text=True, timeout=900,
    )
    out = p.stdout
    start = out.find("---BEGIN SUMMARY---")
    end = out.find("---END SUMMARY---")
    if start == -1 or end == -1:
        raise RuntimeError(f"scraper output missing markers: {p.stderr[-600:]}")
    return out[start + len("---BEGIN SUMMARY---"):end].strip()


def chunk_text(text: str, limit: int = 3800) -> list:
    lines = text.split("\n")
    chunks, cur = [], ""
    for line in lines:
        candidate = line if not cur else cur + "\n" + line
        if len(candidate.encode("utf-8")) > limit and cur:
            chunks.append(cur)
            cur = line
        else:
            cur = candidate
    if cur:
        chunks.append(cur)
    return chunks


def publish(title: str, message: str):
    statuses = []
    parts = chunk_text(message)
    for i, part in enumerate(parts):
        payload = json.dumps({
            "topic": NTFY["topic"],
            "title": title if len(parts) == 1 else f"{title} ({i + 1}/{len(parts)})",
            "message": part,
            "tags": ["shopping_cart"],
            "priority": 3,
        }, ensure_ascii=False)
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
            f.write(payload)
            tmp = f.name
        try:
            cmd = ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
                   "-H", "Content-Type: application/json",
                   "--data-binary", "@" + tmp,
                   NTFY["url"] + "/"]
            if NTFY.get("token"):
                cmd.insert(-1, "-H")
                cmd.insert(-1, "Authorization: Bearer " + NTFY["token"])
            p = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            statuses.append(p.stdout.strip())
        finally:
            pathlib.Path(tmp).unlink(missing_ok=True)
    return ",".join(statuses)


def publish_attachment(filename: str, filepath: pathlib.Path):
    cmd = ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}",
           "-H", f"Filename: {filename}",
           "-H", "Content-Type: text/plain; charset=utf-8",
           "--data-binary", "@" + str(filepath),
           NTFY["url"] + "/" + NTFY["topic"]]
    if NTFY.get("token"):
        cmd.insert(-1, "-H")
        cmd.insert(-1, "Authorization: Bearer " + NTFY["token"])
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return p.stdout.strip()


def main():
    state = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {}
    if state.get("last_sent_date") == TODAY:
        print(f"{TODAY}: already sent today, skipping")
        return 0

    try:
        summary = run_scraper()
    except Exception as e:
        print(f"scraper error: {e}")
        return 1

    title = "Ugens tilbud"
    status = publish(title, summary)
    full_txt = BASE / "data" / f"full-{TODAY}.txt"
    attach_status = "-"
    if full_txt.exists():
        attach_status = publish_attachment(f"alle-tilbud-{TODAY}.txt", full_txt)
    STATE_FILE.write_text(json.dumps({
        "last_sent_date": TODAY,
        "status": status,
        "attachment_status": attach_status,
    }))
    print(f"{TODAY}: published to ntfy topic {NTFY['topic']} (http {status}, attachment {attach_status})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
