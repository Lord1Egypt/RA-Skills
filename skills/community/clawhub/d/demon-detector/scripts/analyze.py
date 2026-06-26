#!/usr/bin/env python3
"""Demon Detector - thin HTTP client. Core logic runs on server."""
import sys, os, json, requests

API_HOST = os.environ.get("DEMON_API_HOST", "http://43.103.7.227:5001")


def analyze(ccy: str, user_id: str = None) -> dict:
    headers = {}
    if user_id:
        headers["X-User-Id"] = user_id
    resp = requests.get("{}/analyze/{}".format(API_HOST, ccy.upper()), headers=headers, timeout=120)
    return resp.json()


def scan(user_id: str = None) -> dict:
    headers = {}
    if user_id:
        headers["X-User-Id"] = user_id
    resp = requests.get("{}/scan".format(API_HOST), headers=headers, timeout=180)
    return resp.json()


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "scan"
    user_id = os.environ.get("DEMON_USER_ID", "cli_user")

    if mode.upper() == "SCAN":
        result = scan(user_id)
    else:
        ccy = mode.upper()
        result = analyze(ccy, user_id)

    if result.get("error") == "payment_required":
        print("余额不足，请充值: {}".format(result.get("payment_url", "")))
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
