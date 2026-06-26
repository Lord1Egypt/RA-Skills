#!/usr/bin/env python3
import argparse, json

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source_txt")
    ap.add_argument("--channels", nargs="+", default=["wechat_article","xiaohongshu_note","douyin_script"])
    ap.add_argument("--out", default="channel_pack.json")
    args = ap.parse_args()
    src = open(args.source_txt, "r", encoding="utf-8").read().strip()
    payload = {"source_excerpt": src[:500], "channels": {}}
    for ch in args.channels:
        payload["channels"][ch] = {"title": "", "hook": "", "body_outline": [], "cta": ""}
    json.dump(payload, open(args.out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"Wrote {args.out}")

if __name__ == "__main__":
    main()
