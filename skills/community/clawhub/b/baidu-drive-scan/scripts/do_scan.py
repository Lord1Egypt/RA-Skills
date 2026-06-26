#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import argparse
import json
import requests
from config import Config

def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", required=True)
    parser.add_argument("--mode", default=1)
    args = parser.parse_args()

    # base64 从 stdin 读取，避免命令行参数过长（Argument list too long）
    image_b64 = sys.stdin.read().strip()
    req_data = {
        "method": int(args.method),
        "mode": int(args.mode),
        "ptype": 1,
        "image_base64": image_b64,
    }
    try:
        resp = requests.post(
            url=f"{Config.API_BASE}?api_key={Config.BDPAN_SPACE_TOKEN}",
            json=req_data,
            headers={
                "Content-Type": "application/json",
            },
            timeout=60
        )
        print(resp.text)
    except Exception as e:
        print(json.dumps({"errno": -1, "error": str(e)}, ensure_ascii=False))

if __name__ == "__main__":
    run()