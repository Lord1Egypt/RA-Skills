#!/usr/bin/env python3
import argparse
import base64
import json
import os
import re
import urllib.request
from pathlib import Path


def parse_pages(doc_text: str):
    pages = []
    in_pages = False
    for raw in doc_text.splitlines():
        line = raw.strip()
        if line.lower().startswith('## 5. pages') or line.lower().startswith('## 5) pages'):
            in_pages = True
            continue
        if in_pages and line.startswith('## '):
            break
        if in_pages:
            m = re.match(r"^\d+[\.)]\s+(.+)$", line)
            if m:
                pages.append(m.group(1).strip())
    return pages[:8]


def extract_claims(doc_text: str):
    t = doc_text.lower()
    claims = {
        "no_upload": ("no user upload" in t) or ("不包含用户上传" in doc_text),
        "no_report": ("no report" in t) or ("不包含举报" in doc_text),
        "hide_publisher": ("do not display uploader" in t) or ("不展示" in doc_text and "发布者" in doc_text),
        "pexels": "pexels.com/api" in t,
    }
    return claims


def ai_image(prompt: str, api_key: str, size: str = "1536x1024"):
    url = "https://api.openai.com/v1/images/generations"
    payload = {
        "model": "gpt-image-1",
        "prompt": prompt,
        "size": size,
        "quality": "high",
    }
    req = urllib.request.Request(url, method="POST")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")
    data = json.dumps(payload).encode("utf-8")
    with urllib.request.urlopen(req, data=data, timeout=180) as r:
        body = json.loads(r.read().decode("utf-8"))
    b64 = body["data"][0]["b64_json"]
    return base64.b64decode(b64)


def slug(s: str):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s or "page"


def main():
    ap = argparse.ArgumentParser(description="Generate page UI PNGs with AI model from approved feature doc")
    ap.add_argument("--doc", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--primary-color", default="#0A84FF")
    ap.add_argument("--app-name", default="App")
    args = ap.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Missing OPENAI_API_KEY. Set it before running AI UI generation.")

    doc_text = Path(args.doc).read_text(encoding="utf-8")
    pages = parse_pages(doc_text)
    if not pages:
        pages = ["Home", "Search", "Details", "Favorites", "Settings"]

    claims = extract_claims(doc_text)
    constraints = [
        "iOS app screen design, Apple-style, high fidelity, production-ready",
        f"bright accent color {args.primary_color}",
        "clean spacing, clear hierarchy, realistic mobile UI",
        "no watermark, no lorem ipsum",
    ]
    if claims["pexels"]:
        constraints.append("media browsing experience based on open stock photo/video style")
    if claims["no_upload"]:
        constraints.append("do not include upload buttons or upload flows")
    if claims["no_report"]:
        constraints.append("do not include report/moderation/audit UI")
    if claims["hide_publisher"]:
        constraints.append("do not show publisher/uploader identity fields")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    for i, page in enumerate(pages, start=1):
        prompt = (
            f"Design an iPhone app screen for '{args.app_name}', page: {page}. "
            + "; ".join(constraints)
            + ". Include realistic status/navigation bars and actionable components."
        )
        png = ai_image(prompt, api_key)
        fn = out / f"page-{i:02d}-{slug(page)}.png"
        fn.write_bytes(png)
        print(fn)


if __name__ == "__main__":
    main()
