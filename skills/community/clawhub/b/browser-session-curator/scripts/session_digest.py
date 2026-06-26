#!/usr/bin/env python3
import argparse, json

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tabs_json", help="JSON list with title,url")
    ap.add_argument("--out", default="session_digest.json")
    args = ap.parse_args()
    tabs = json.load(open(args.tabs_json, "r", encoding="utf-8"))
    digest = {"action": [], "reading": [], "archive": []}
    for tab in tabs:
        title = (tab.get("title") or "").lower()
        bucket = "reading"
        if any(k in title for k in ["todo", "task", "reply", "invoice", "submit"]):
            bucket = "action"
        elif any(k in title for k in ["archive", "old", "closed"]):
            bucket = "archive"
        digest[bucket].append(tab)
    json.dump(digest, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
