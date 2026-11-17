#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""飞书机器人桥：接收飞书事件/消息，把网盘链接转发给本机/NAS 的 pan serve。

模式说明：
  - 群机器人 Webhook          : 只能“发通知”，不能收到用户消息（用 pan notify --channel feishu）。
  - 自建应用 App + 事件订阅   : 能真正收到你发给机器人的消息；需要 APP_ID/APP_SECRET、
                                公网回调地址（或飞书长连接接入）。本脚本提供“事件回调 HTTP
                                服务”这一轻量桥：飞书把消息 POST 过来，脚本自动抽链接并转发到
                                本机/NAS 的 POST /api/download，然后返回结果。

用法：
  python3 feishu_bot.py --check                     # 离线自检，不联网
  python3 feishu_bot.py --host 0.0.0.0 --port 9001  # 常驻事件回调服务
  python3 feishu_bot.py --target http://127.0.0.1:17890
  # 飞书开放平台配回调地址为：http://<本机或NAS公网地址>:9001/feishu/callback

安全边界：
  - 本脚本不存放、不打印 APP_SECRET/token；飞书加密回调解密需在独立配置中启用 Encrypt Key。
  - 公网暴露前请用 SSH 反向隧道或 VPS，并确认只投递你主动发送的链接。
"""
from __future__ import annotations

try:
    import os as _boot_os, sys as _boot_sys
    _boot_here = _boot_os.path.dirname(_boot_os.path.abspath(__file__))
    _boot_parent = _boot_os.path.dirname(_boot_here)
    for _boot_dir in (_boot_here, _boot_parent):
        if _boot_dir not in _boot_sys.path:
            _boot_sys.path.insert(0, _boot_dir)
    import pyboot as _boot_pyboot
    _boot_pyboot.ensure_utf8_io()
except Exception:
    pass


import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

_URL_RE = re.compile(r"https?://[^\s<>\"]+", re.IGNORECASE)

DEFAULT_TARGET = "http://127.0.0.1:17890"


def extract_urls(text: str):
    """从消息文本中抽取 http(s) 链接。"""
    return [m.group(0).rstrip("，。;；,，!！?？") for m in _URL_RE.finditer(text or "")]


def extract_pwd(text: str):
    """尝试从消息里识别常见提取码写法：提取码/密码/pwd/pass 后跟 4-6 位码。"""
    m = re.search(r"(?:提取码|密码|pwd|pass|提取码：?)\s*[:：]?\s*([A-Za-z0-9]{4,6})", text or "", re.IGNORECASE)
    return m.group(1) if m else ""


def forward_download(url: str, pwd: str, target: str, timeout: float = 30.0, token: str = ""):
    """把链接投递到 pan serve 的 POST /api/download；成功返回 (ok, info)。"""
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if token:
        # v0.19.0 起 pan serve 的 API 需要 token 鉴权
        headers["Authorization"] = "Bearer " + token
    payload = json.dumps({"url": url, "pwd": pwd or ""}, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(target.rstrip("/") + "/api/download",
                                 data=payload, method="POST", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = (resp.read() or b"{}").decode("utf-8", "replace")
            data = json.loads(body or "{}")
        return True, data
    except Exception as exc:  # noqa: BLE001
        return False, {"error": "转发下载失败：%s" % exc}


def handle_event(body: dict, target: str, token: str = ""):
    """处理飞书事件 JSON。返回 (handled, response_json_or_None, messages)。

    - url_verification 校验：原样回 challenge。
    - 消息事件：抽取链接转发下载；无链接返回提示。
    """
    body = body or {}
    challenge = body.get("challenge")
    if challenge:
        return True, {"challenge": challenge}, ["飞书 URL 校验通过"]

    event = body.get("event") or {}
    msg = event.get("message") or {}
    content = msg.get("content") or "{}"
    text = ""
    try:
        content_obj = json.loads(content) if isinstance(content, str) else (content or {})
        text = content_obj.get("text") or content_obj.get("content") or ""
    except (ValueError, TypeError):
        text = str(content)

    # 兼容明文 text 场景
    if not text:
        text = str(event.get("text") or body.get("text") or "")

    urls = extract_urls(text)
    if not urls:
        return True, None, ["收到消息但未发现可下载的 http(s) 链接"]

    msgs = []
    for url in urls:
        ok, info = forward_download(url, extract_pwd(text), target, token=token)
        msgs.append(("✅ 已开始下载：%s\n%s" % (url, json.dumps(info, ensure_ascii=False)))
                    if ok else ("❌ %s" % info.get("error", "下载启动失败")))
    return True, None, msgs


class FeishuHandler(BaseHTTPRequestHandler):
    target = DEFAULT_TARGET
    verify_token = ""  # 飞书开放平台"事件订阅"页的 Verification Token；非空时校验 body.token

    def log_message(self, *args):  # 关闭默认访问日志（由业务逻辑打印）
        pass

    def _reply(self, status: int, data):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._reply(200, {"ok": True, "service": "feishu-bot", "target": self.target})

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0) or 0)
        raw = self.rfile.read(length) if length else b""
        try:
            body = json.loads(raw.decode("utf-8") or "{}")
        except (ValueError, UnicodeDecodeError):
            body = {}
        if self.verify_token and str(body.get("token") or "") != self.verify_token:
            print("❌ 回调 token 校验失败，已拒绝（来自 %s）" % (self.client_address[0] if self.client_address else "?"), flush=True)
            self._reply(403, {"ok": False, "error": "invalid token"})
            return
        handled, resp, msgs = handle_event(body, self.target, token=self._pan_token)
        for m in msgs:
            print(m, flush=True)
        if resp is not None:
            self._reply(200, resp)
            return
        self._reply(200, {"ok": handled})


def run_server(host: str, port: int, target: str, verify_token: str = "", pan_token: str = ""):
    loopback = host in ("127.0.0.1", "localhost", "::1")
    if not loopback and not verify_token:
        # 安全修复：非回环暴露必须先配 Verification Token，否则任何人都能借你的 pan 投递下载
        print("❌ 拒绝启动：--host 为非回环地址时必须提供 --feishu-verify-token（飞书开放平台-事件订阅-Verification Token）")
        return 2
    server = ThreadingHTTPServer((host, port), FeishuHandler)
    FeishuHandler.target = target
    FeishuHandler.verify_token = verify_token
    FeishuHandler._pan_token = pan_token
    print("飞书桥已启动：监听 %s:%d，转发目标 %s" % (host, port, target), flush=True)
    print("回调鉴权：%s；pan token 转发：%s" % ("已启用 Verification Token" if verify_token else "未配置（仅建议回环使用）", "已启用" if pan_token else "未配置"), flush=True)
    print("飞书回调地址：http://%s:%d/feishu/callback" % (host, port), flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n已停止", flush=True)
    return 0


def self_check():
    """离线自检：验证链接抽取、提取码抽取、事件分流与转发 payload 拼装。"""
    assert extract_urls("下载 https://pan.baidu.com/s/abc123 谢谢") == ["https://pan.baidu.com/s/abc123"]
    assert extract_pwd("https://pan.baidu.com/s/x 提取码：2abc4") == "2abc4"
    handled, resp, msgs = handle_event({"challenge": "ch_123"}, DEFAULT_TARGET)
    assert handled and resp == {"challenge": "ch_123"}, "url_verification 未回 challenge"
    # 事件消息（不真正联网，转发调用会在 target 无效时报错但会走到转发分支）
    handled, resp, msgs = handle_event({"event": {"message": {"content": json.dumps({"text": "https://pan.baidu.com/s/abc123 提取码：9f2k"})}}},
                                       "http://127.0.0.1:1")
    assert resp is None and handled, "消息事件未进入转发分支"
    assert any("已开始下载" in m or "转发下载失败" in m for m in msgs), "消息事件应返回转发结果"
    print("FEISHU_BOT_SELF_CHECK_OK")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="飞书机器人桥：事件回调 → pan serve 下载")
    ap.add_argument("--check", action="store_true", help="离线自检，不联网")
    ap.add_argument("--host", default="127.0.0.1", help="回调服务监听地址（默认 127.0.0.1）")
    ap.add_argument("--port", type=int, default=9001, help="回调服务端口（默认 9001）")
    ap.add_argument("--target", default=DEFAULT_TARGET, help="pan serve 地址（默认 http://127.0.0.1:17890）")
    ap.add_argument("--feishu-verify-token", default=os.environ.get("FEISHU_VERIFY_TOKEN", ""),
                    help="飞书 Verification Token（非回环监听时必填；也可用环境变量 FEISHU_VERIFY_TOKEN）")
    ap.add_argument("--pan-token", default=os.environ.get("PAN_WEB_TOKEN", ""),
                    help="pan serve 的 API token（v0.19.0 起需要；也可用环境变量 PAN_WEB_TOKEN）")
    args = ap.parse_args(argv)
    if args.check:
        return self_check()
    return run_server(args.host, args.port, args.target, args.feishu_verify_token, args.pan_token)


if __name__ == "__main__":
    sys.exit(main())
