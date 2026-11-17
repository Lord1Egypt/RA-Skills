#!/usr/bin/env python3
"""钉钉群自定义机器人命令行工具（零依赖，仅标准库）。

环境变量:
    DING_WEBHOOK   机器人 Webhook 完整地址（含 access_token）
    DING_SECRET    加签密钥（安全设置选"加签"时必填，SEC 开头）

子命令:
    text <内容> [@手机号,手机号|@all]      发文本消息
    markdown <标题> <md文件或内容>          发 markdown 消息
    link <标题> <正文> <跳转URL> [图片URL]  发链接卡片

示例:
    export DING_WEBHOOK='https://oapi.dingtalk.com/robot/send?access_token=xxx'
    export DING_SECRET='SECxxxx'
    python3 dingbot.py text "构建完成 ✅" @all
    python3 dingbot.py markdown "日报" report.md
"""
import base64
import hashlib
import hmac
import json
import os
import sys
import time
import urllib.parse
import urllib.request


def die(msg: str) -> None:
    print(f"错误: {msg}", file=sys.stderr)
    sys.exit(1)


def signed_url() -> str:
    url = os.environ.get("DING_WEBHOOK") or die("未设置 DING_WEBHOOK")
    secret = os.environ.get("DING_SECRET")
    if not secret:
        return url
    ts = str(round(time.time() * 1000))
    string_to_sign = f"{ts}\n{secret}".encode("utf-8")
    sign = base64.b64encode(
        hmac.new(secret.encode("utf-8"), string_to_sign,
                 digestmod=hashlib.sha256).digest())
    return f"{url}&timestamp={ts}&sign={urllib.parse.quote_plus(sign)}"


def send(body: dict) -> None:
    req = urllib.request.Request(
        signed_url(), json.dumps(body, ensure_ascii=False).encode("utf-8"),
        {"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        r = json.loads(resp.read())
    print(json.dumps(r, ensure_ascii=False))
    if r.get("errcode") != 0:
        # 310000=安全设置校验失败(关键词/加签/IP) 300005=token不存在
        sys.exit(2)


def read_arg_or_file(v: str) -> str:
    return open(v, encoding="utf-8").read() if os.path.isfile(v) else v


def parse_at(arg: str) -> dict:
    if arg == "@all":
        return {"isAtAll": True}
    if arg.startswith("@"):
        return {"atMobiles": arg[1:].split(","), "isAtAll": False}
    die(f"@参数格式错误: {arg}（应为 @all 或 @手机号,手机号）")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    cmd, rest = args[0], args[1:]

    if cmd == "text":
        rest or die("用法: text <内容> [@手机号,手机号|@all]")
        body = {"msgtype": "text", "text": {"content": rest[0]}}
        if len(rest) > 1:
            body["at"] = parse_at(rest[1])
        send(body)
    elif cmd == "markdown":
        len(rest) >= 2 or die("用法: markdown <标题> <md文件或内容>")
        send({"msgtype": "markdown",
              "markdown": {"title": rest[0],
                           "text": read_arg_or_file(rest[1])}})
    elif cmd == "link":
        len(rest) >= 3 or die("用法: link <标题> <正文> <跳转URL> [图片URL]")
        link = {"title": rest[0], "text": rest[1], "messageUrl": rest[2]}
        if len(rest) > 3:
            link["picUrl"] = rest[3]
        send({"msgtype": "link", "link": link})
    else:
        die(f"未知子命令: {cmd}（运行不带参数查看帮助）")


if __name__ == "__main__":
    main()
