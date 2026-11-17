#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""商汤 SenseNova 文生图 (free-media-gen)。

OpenAI /v1/images/generations 兼容：
  POST https://token.sensenova.cn/v1/images/generations
  {"model":"sensenova-u1.5-lite","prompt":..,"n":1,"size":"1024x1024","watermark":false}
  -> {"data":[{"url":..} | {"b64_json":..}]}

商汤公测免费（每 5 小时 1500 次），watermark=false 可免费去水印。
凭证经 _common 从 models.json 解析；端点取自 config.json。

用法:
  python sensenova_image.py --prompt "极简科技感细胞制备中心" [--model sensenova-u1.5-lite]
                            [--size 1024x1024] [--out DIR] [--watermark]
"""
import argparse
import base64
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--model", default="sensenova-u1.5-lite")
    ap.add_argument("--size", default="1024x1024")
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--out", default=None)
    ap.add_argument("--watermark", action="store_true", help="保留水印（默认去除）")
    ap.add_argument("--max-retries", type=int, default=3)
    args = ap.parse_args()

    entry = C.get_model_entry(args.model)
    if not entry:
        print(json.dumps({"ok": False, "error": "未知模型 id：%s" % args.model},
                         ensure_ascii=False))
        sys.exit(1)

    key = C.resolve_api_key(entry.get("api_key_ref"), entry.get("provider"))
    headers = {"Authorization": "Bearer %s" % key, "Content-Type": "application/json"}
    url = entry["endpoint"]

    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "n": args.n,
        "size": args.size,
        "watermark": bool(args.watermark),
    }

    status, body = C.http_json(url, payload, headers, method="POST", retries=args.max_retries)
    if status != 200 or not isinstance(body, dict) or not ("data" in body or "images" in body):
        print(json.dumps({"ok": False, "http": status, "error": body}, ensure_ascii=False))
        sys.exit(1)

    items = body.get("data") or body.get("images") or []
    out_dir = args.out or C.resolve()["generated_images_dir"]
    C.ensure_dir(out_dir)

    urls, saved = [], []
    for i, item in enumerate(items):
        if item.get("url"):
            urls.append(item["url"])
            p = os.path.join(out_dir, C.out_name("sensenova_img", "png", i))
            if C.download(item["url"], p):
                saved.append(p)
        elif item.get("b64_json"):
            p = os.path.join(out_dir, C.out_name("sensenova_img", "png", i))
            with open(p, "wb") as f:
                f.write(base64.b64decode(item["b64_json"]))
            saved.append(p)
            urls.append("(b64 -> %s)" % p)

    print(json.dumps({"ok": True, "model": args.model, "size": args.size,
                      "urls": urls, "saved": saved}, ensure_ascii=False))


if __name__ == "__main__":
    main()
