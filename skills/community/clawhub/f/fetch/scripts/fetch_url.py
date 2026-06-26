#!/usr/bin/env python3
import argparse
import json
import os
import sys
import uuid
from datetime import datetime
from urllib.parse import urlparse
from urllib.request import Request, urlopen

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import load_jobs, save_jobs, PAGES_DIR
from lib.extract import strip_html, extract_title, extract_links

def main():
    parser = argparse.ArgumentParser(description="Fetch a public URL")
    parser.add_argument("--url", required=True, help="Public URL to fetch")
    args = parser.parse_args()

    parsed = urlparse(args.url)
    if parsed.scheme not in ("http", "https"):
        print("Only http/https URLs are allowed.")
        sys.exit(1)

    req = Request(
        args.url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; FetchSkill/1.0.0)"}
    )

    with urlopen(req, timeout=20) as resp:
        raw_bytes = resp.read()
        content_type = resp.headers.get("Content-Type", "")
        status_code = getattr(resp, "status", 200)

    raw_html = raw_bytes.decode("utf-8", errors="replace")
    title = extract_title(raw_html)
    clean_text = strip_html(raw_html)
    links = extract_links(raw_html)

    job_id = f"JOB-{str(uuid.uuid4())[:4].upper()}"
    now = datetime.now().isoformat()

    raw_path = os.path.join(PAGES_DIR, f"{job_id}.raw.html")
    clean_path = os.path.join(PAGES_DIR, f"{job_id}.clean.txt")

    with open(raw_path, "w", encoding="utf-8") as f:
        f.write(raw_html)
    with open(clean_path, "w", encoding="utf-8") as f:
        f.write(clean_text)

    data = load_jobs()
    data["jobs"][job_id] = {
        "id": job_id,
        "url": args.url,
        "title": title,
        "status_code": status_code,
        "content_type": content_type,
        "created_at": now,
        "raw_path": raw_path,
        "clean_path": clean_path,
        "text_chars": len(clean_text),
        "link_count": len(links)
    }
    save_jobs(data)

    print(f"✓ Fetched: {job_id}")
    print(f"  Title: {title}")
    print(f"  Status: {status_code}")
    print(f"  Links: {len(links)}")
    print(f"  Clean text chars: {len(clean_text)}")

if __name__ == "__main__":
    main()
