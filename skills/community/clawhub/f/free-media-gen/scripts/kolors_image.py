#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""硅基流动 SiliconFlow — Kolors 文生图 (free-media-gen)。

  POST https://api.siliconflow.cn/v1/images/generations
  {"model":"Kwai-Kolors/Kolors","prompt":..,"image_size":"1024x1024"}
  -> {"data":[{"url":..}]}   （部分版本返回 {"images":[{"url":..}]}，脚本两者都处理）

注意：硅基流动上 Kolors 免费，而 Qwen-Image 为付费（¥0.3/张），后者不纳入本技能。
凭证经 _common 从 models.json 解析；端点取自 config.json。

用法:
  python kolors_image.py --prompt "中国古代山水，水墨风格" [--model Kwai-Kolors/Kolors]
                         [--size 1024x1024] [--out DIR]
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
    ap.add_argument("--model", default="Kwai-Kolors/Kolors")
    ap.add_argument("--size", default="1024x1024")
    ap.add_argument("--out", default=None)
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

    # 硅基流动使用 image_size 而非 size；两者都带上以兼容不同版本
    payload = {
        "model": args.model,
        "prompt": args.prompt,
        "image_size": args.size,
        "size": args.size,
        "n": 1,
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
            p = os.path.join(out_dir, C.out_name("kolors_img", "png", i))
            if C.download(item["url"], p):
                saved.append(p)
        elif item.get("b64_json"):
            p = os.path.join(out_dir, C.out_name("kolors_img", "png", i))
            with open(p, "wb") as f:
                f.write(base64.b64decode(item["b64_json"]))
            saved.append(p)
            urls.append("(b64 -> %s)" % p)

    print(json.dumps({"ok": True, "model": args.model, "size": args.size,
                      "urls": urls, "saved": saved}, ensure_ascii=False))


if __name__ == "__main__":
    main()
