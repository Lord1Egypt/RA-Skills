#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""往 GitHub 仓库写 Actions Secret / Variable。

GitHub 的 Secret 必须先用仓库公钥（libsodium sealed box）加密才能提交，
这一步没有官方 CLI 之外的捷径，本脚本用 PyNaCl 直接完成。

依赖：pip install pynacl

用法：
    export GITHUB_TOKEN=ghp_xxx          # 或自动从 ~/.git-credentials 读
    python set_github_secret.py --repo owner/repo --list
    python set_github_secret.py --repo owner/repo --name OSS_ACCESS_KEY_ID --value "$AK_ID"
    python set_github_secret.py --repo owner/repo --name OSS_BUCKET --value my-bucket --variable
    python set_github_secret.py --repo owner/repo --name OSS_ACCESS_KEY_ID --stdin < id.txt

说明：只写不读——GitHub 的 Secret 值一旦写入无法再取回，--list 只能看名字。
"""
import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.request

API = "https://api.github.com"


def get_token():
    tok = os.environ.get("GITHUB_TOKEN", "")
    if tok:
        return tok
    cred = os.path.join(os.path.expanduser("~"), ".git-credentials")
    if os.path.exists(cred):
        m = re.search(r"(gh[oUp]_[A-Za-z0-9]+)",
                      open(cred, encoding="utf-8", errors="replace").read())
        if m:
            return m.group(1)
    sys.exit("拿不到 GitHub token：设置 GITHUB_TOKEN 或确认 ~/.git-credentials 里有凭据")


def req(method, path, token, data=None):
    url = API + path
    body = json.dumps(data).encode() if data is not None else None
    r = urllib.request.Request(url, method=method, data=body, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "User-Agent": "set-github-secret/1.0",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            raw = resp.read()
            return resp.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            return e.code, json.loads(raw or b"{}")
        except Exception:
            return e.code, {"message": raw[:200].decode("utf-8", "replace")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True, help="owner/repo")
    ap.add_argument("--name", help="Secret / Variable 名")
    ap.add_argument("--value", help="值（不给则用 --stdin）")
    ap.add_argument("--stdin", action="store_true", help="从标准输入读值，避免出现在命令行历史里")
    ap.add_argument("--variable", action="store_true", help="写普通 Variable（明文）而非 Secret")
    ap.add_argument("--list", action="store_true", help="列出现有名字（不含值）")
    args = ap.parse_args()

    token = get_token()
    base = "/repos/%s/actions" % args.repo

    if args.list:
        st, body = req("GET", base + "/secrets", token)
        st2, body2 = req("GET", base + "/variables", token)
        print("secrets  :", [s["name"] for s in body.get("secrets", [])] if st == 200 else body)
        print("variables:", [v["name"] for v in body2.get("variables", [])] if st2 == 200 else body2)
        return 0

    if not args.name:
        sys.exit("需要 --name（或用 --list 查看现有配置）")

    value = (sys.stdin.read().strip() if args.stdin else (args.value or ""))
    if not value:
        sys.exit("值为空，用 --value 或 --stdin 提供")

    if args.variable:
        st, body = req("POST", base + "/variables", token, {"name": args.name, "value": value})
        if st not in (201, 204):
            st, body = req("PATCH", base + "/variables/" + args.name, token,
                           {"name": args.name, "value": value})
        print("variable %s -> HTTP %s %s" % (args.name, st, "" if st in (201, 204) else body))
        return 0 if st in (201, 204) else 1

    from nacl import encoding, public

    st, pk = req("GET", base + "/secrets/public-key", token)
    if st != 200:
        sys.exit("取仓库公钥失败 HTTP %s: %s" % (st, pk))
    box = public.SealedBox(public.PublicKey(pk["key"].encode(), encoding.Base64Encoder()))
    enc = base64.b64encode(box.encrypt(value.encode())).decode()
    st, body = req("PUT", base + "/secrets/" + args.name, token,
                   {"encrypted_value": enc, "key_id": pk["key_id"]})
    print("secret %s -> HTTP %s %s" % (args.name, st, "" if st in (201, 204) else body))
    return 0 if st in (201, 204) else 1


if __name__ == "__main__":
    sys.exit(main())
