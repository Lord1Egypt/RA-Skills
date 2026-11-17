#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Agnes 文生图 / 图生图 (free-media-gen)。

基于 agnes-media 实测有效的调用方式：
  POST {base}/images/generations   头部 Authorization: Bearer <key>
  正文 {"model":..., "prompt":..., "n":1, "size":"1024x1024"}
  响应 {"data":[{"url":...} | {"b64_json":...}]}

base 由 config.json 的 endpoint 反推（去掉 /images/generations 后缀），
因此不硬编码域名；凭证经 _common 从 models.json 解析。

用法:
  python agnes_image.py --prompt "一只小红猫" [--model agnes-image-2.1-flash]
                        [--size 1024x1024] [--n 1] [--out DIR]
输出: {"ok":true, "model":..., "urls":[...], "saved":[...]}
"""
import argparse
import base64
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _common as C  # noqa: E402

SUFFIX = "/images/generations"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--model", default="agnes-image-2.1-flash")
    ap.add_argument("--size", default="1024x1024")
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--out", default=None, help="保存目录；默认工作区 generated-images")
    ap.add_argument("--max-retries", type=int, default=4)
    args = ap.parse_args()

    entry = C.get_model_entry(args.model)
    if not entry:
        print(json.dumps({"ok": False, "error": "未知模型 id：%s" % args.model},
                         ensure_ascii=False))
        sys.exit(1)

    try:
        key = C.resolve_api_key(entry.get("api_key_ref"), entry.get("provider"))
    except Exception as e:
        print(json.dumps({"ok": False, "error": "密钥解析失败：%s" % e},
                         ensure_ascii=False))
        sys.exit(1)

    endpoint = entry.get("endpoint", "")
    base = endpoint[: -len(SUFFIX)] if endpoint.endswith(SUFFIX) else endpoint
    url = base + SUFFIX

    headers = {"Authorization": "Bearer %s" % key, "Content-Type": "application/json"}
    payload = {"model": args.model, "prompt": args.prompt, "n": args.n, "size": args.size}

    status, body = C.http_json(url, payload, headers, method="POST", retries=args.max_retries)
    if status != 200 or not isinstance(body, dict) or "data" not in body:
        print(json.dumps({"ok": False, "http": status, "error": body}, ensure_ascii=False))
        sys.exit(1)

    out_dir = args.out or C.resolve()["generated_images_dir"]
    C.ensure_dir(out_dir)

    urls, saved = [], []
    for i, item in enumerate(body["data"]):
        if item.get("url"):
            urls.append(item["url"])
            p = os.path.join(out_dir, C.out_name("agnes_img", "png", i))
            if C.download(item["url"], p):
                saved.append(p)
        elif item.get("b64_json"):
            p = os.path.join(out_dir, C.out_name("agnes_img", "png", i))
            with open(p, "wb") as f:
                f.write(base64.b64decode(item["b64_json"]))
            saved.append(p)
            urls.append("(b64 -> %s)" % p)

    print(json.dumps({"ok": True, "model": args.model, "size": args.size,
                      "urls": urls, "saved": saved}, ensure_ascii=False))


if __name__ == "__main__":
    main()
