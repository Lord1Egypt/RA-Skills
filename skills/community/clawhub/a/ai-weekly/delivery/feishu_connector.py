#!/usr/bin/env python3
"""把 AI 周报头条卡片推送到飞书 —— 走 WorkBuddy 飞书连接器（lark-cli），不落 webhook token。

设计原则（沿用 skill 合规约束）：
- 复用 ``delivery/feishu_bot.build_headline_card`` 构造消息卡片（Card 1.0，飞书仍支持），
  通过 lark-cli 的 raw HTTP 通道 ``api POST /open-apis/im/v1/messages`` 发送——卡片 body
  经 stdin 传入，彻底规避 Windows 命令行长度上限（见 R6 注释）；密钥由连接器托管，绝不写进任何配置文件。
- 仅依赖标准库 + 已连接的飞书连接器（lark-cli）。

目标会话解析（优先级从高到低，命中即停）：
  1. CLI 参数 ``--chat-id`` / ``--user-id``
  2. 环境变量 ``FEISHU_CHAT_ID`` / ``FEISHU_USER_ID``
  3. ``delivery/feishu_target.json``：``{"chat_id": "oc_xxx"}`` 或 ``{"user_id": "ou_xxx"}``

发送身份：``--as bot``（默认，应用机器人）或 ``--as user``（以你本人身份）。
  注意：bot 身份发送前，需先把「WorkBuddy-Feishu CLI」这个应用机器人拉进目标群；
  user 身份发送则不需要，但需你本人对该会话有发消息权限。

用法：
  # 预览请求（不发）
  python feishu_connector.py --report report.json --chat-id oc_xxx --dry-run

  # 真实发送（bot 身份 → 群）
  python feishu_connector.py --report report.json --chat-id oc_xxx

  # 发给自己（user 身份 → 私聊），适合首次冒烟测试
  python feishu_connector.py --report report.json --user-id ou_xxx --as user

  # 也可把目标写进 delivery/feishu_target.json，省去每次传参
  python feishu_connector.py --report report.json
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys

logger = logging.getLogger("aiweekly.delivery.feishu_connector")

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from feishu_bot import build_headline_card  # noqa: E402

_TARGET_JSON = os.path.join(_HERE, "feishu_target.json")

# R6（已彻底修复）：原实现把整卡 JSON 作为 --content 命令行参数传给
# `lark-cli im +messages-send`，受 Windows CreateProcess 命令行上限（~8191 字符）约束，
# 满配卡片逼近上限时 spawn 失败且无提示。现改为 raw HTTP 通道
# `api POST /open-apis/im/v1/messages`，卡片 body 经 **stdin**（--data -）传入，
# 完全不进入 argv，从根本上消除命令行长度限制（经 --dry-run 实测请求体与原路径一致）。


def load_report(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_card(report: dict) -> dict:
    """从 feishu_bot 的 {msg_type, card} 信封里取出内层 card（lark-cli --content 需要卡片本体）。"""
    built = build_headline_card(report)
    return built.get("card", built)


def resolve_lark() -> tuple[str, str]:
    """定位 lark-cli 的真实启动方式（node + run.js）。

    ``lark-cli`` 在 Windows 上是个无扩展名 shim / ``lark-cli.cmd``，Python 的
    ``subprocess.CreateProcess`` 无法直接启动；而经 ``cmd /c`` 又会被 JSON 里的引号坑。
    最稳的做法是直接拿 ``node`` 调它的 ``run.js`` 入口（与 shim 内部行为一致）。
    """
    cli = shutil.which("lark-cli.cmd") or shutil.which("lark-cli")
    pkg_dir = os.path.dirname(os.path.abspath(cli)) if cli else None
    if not pkg_dir:
        cand = os.path.join(os.path.expanduser("~"), ".workbuddy", "binaries",
                            "node", "cli-connector-packages")
        if os.path.isdir(cand):
            pkg_dir = cand
    if not pkg_dir:
        from aiweekly.errors import UserFacingError
        raise UserFacingError("ERR-FS-CON-001", "找不到 lark-cli 安装目录",
                              ["确认飞书连接器已安装：WorkBuddy → 设置 → 连接器 → 安装 'Lark CLI'",
                               "或用 --chat-id / --user-id 参数绕过连接器模式"])
    run_js = os.path.join(pkg_dir, "node_modules", "@larksuite", "cli",
                          "scripts", "run.js")
    if not os.path.exists(run_js):
        from aiweekly.errors import UserFacingError
        raise UserFacingError("ERR-FS-CON-002", "找不到 lark-cli 入口脚本",
                              [f"期望位置：{run_js}",
                               "重新安装飞书连接器后重试"],
                              verbose=f"pkg_dir={pkg_dir!r} 但 run.js 不在预期路径")

    node = shutil.which("node")
    if not node:
        for ver in ("22.22.2", "24.14.1"):
            c = os.path.join(os.path.expanduser("~"), ".workbuddy", "binaries",
                             "node", "versions", ver, "node.exe")
            if os.path.exists(c):
                node = c
                break
    if not node:
        from aiweekly.errors import UserFacingError
        raise UserFacingError("ERR-FS-NODE-001", "找不到 node 可执行文件",
                              ["安装 Node.js：https://nodejs.org/",
                               "或 WorkBuddy 已自带 node，确保 PATH 包含 ~/.workbuddy/binaries/node/versions/*"])
    return node, run_js


def resolve_target(args: argparse.Namespace):
    """返回 (flag, value)，如 ('--chat-id', 'oc_xxx') 或 ('--user-id', 'ou_xxx')；解析失败返回 (None, None)。"""
    if args.chat_id:
        return "--chat-id", args.chat_id
    if args.user_id:
        return "--user-id", args.user_id
    if os.environ.get("FEISHU_CHAT_ID"):
        return "--chat-id", os.environ["FEISHU_CHAT_ID"]
    if os.environ.get("FEISHU_USER_ID"):
        return "--user-id", os.environ["FEISHU_USER_ID"]
    if os.path.exists(_TARGET_JSON):
        try:
            with open(_TARGET_JSON, "r", encoding="utf-8") as f:
                d = json.load(f)
            if d.get("chat_id"):
                return "--chat-id", d["chat_id"]
            if d.get("user_id"):
                return "--user-id", d["user_id"]
        except (ValueError, OSError) as e:
            logger.warning("读取 %s 失败：%s", _TARGET_JSON, e)
    return None, None


def send_card(card: dict, target_flag: str, target_value: str,
              identity: str = "bot", dry_run: bool = False) -> subprocess.CompletedProcess:
    """调用 lark-cli 发送 interactive 卡片。返回 CompletedProcess 供调用方判断 ok。

    R6 彻底修复：不再把整卡 JSON 塞进命令行参数（Windows CreateProcess 命令行上限
    ~8191 字符，满配卡片逼近上限时 spawn 失败且无提示）。改为走 lark-cli 的 raw HTTP
    通道 ``api POST /open-apis/im/v1/messages``，卡片 body 通过 **stdin**（``--data -``）
    传入，完全不进入 argv，从根本上消除命令行长度限制。

    飞书 im/v1/messages 契约：
      - query ``receive_id_type``：群 → chat_id，私聊 open_id
      - body ``{msg_type, content, receive_id}``，其中 content 为**字符串化的卡片 JSON**
    """
    # content 必须是「字符串化的卡片 JSON」（与 im +messages-send 内部一致）
    body = {
        "msg_type": "interactive",
        "content": json.dumps(card, ensure_ascii=False),
        "receive_id": target_value,
    }
    # receive_id_type：群 → chat_id，私聊 open_id
    receive_id_type = "chat_id" if target_flag == "--chat-id" else "open_id"
    params = json.dumps({"receive_id_type": receive_id_type}, ensure_ascii=False)
    body_str = json.dumps(body, ensure_ascii=False)

    node, run_js = resolve_lark()
    cmd = [
        node, run_js, "api", "POST", "/open-apis/im/v1/messages",
        "--params", params,
        "--data", "-",  # 大 JSON 走 stdin，不进 argv（R6 修复核心）
    ]
    if identity:
        cmd += ["--as", identity]
    if dry_run:
        cmd += ["--dry-run"]
    logger.info("执行：node lark-cli api POST /open-apis/im/v1/messages "
                "--params %s --data - (stdin %d chars) --as %s%s",
                params, len(body_str), identity, " --dry-run" if dry_run else "")
    # 关键：body 通过 stdin（input=）传入，绝不经命令行参数
    return subprocess.run(cmd, input=body_str, capture_output=True, text=True)


def main() -> int:
    ap = argparse.ArgumentParser(description="通过飞书连接器推送 AI 周报头条卡片")
    ap.add_argument("--report", required=True, help="report.json 路径（publish.py 产物或样例）")
    ap.add_argument("--chat-id", help="目标群 chat_id（oc_xxx）")
    ap.add_argument("--user-id", help="目标用户 open_id（ou_xxx），用于私聊")
    ap.add_argument("--as", dest="identity", default="bot", choices=["bot", "user"])
    ap.add_argument("--dry-run", action="store_true", help="只打印请求，不实际发送")
    args = ap.parse_args()

    if not os.path.exists(args.report):
        print(f"ERROR: 找不到 report 文件：{args.report}", file=sys.stderr)
        return 2

    report = load_report(args.report)
    card = extract_card(report)

    flag, val = resolve_target(args)
    if not flag:
        print("ERROR: 未指定推送目标。请传 --chat-id/--user-id，或设置环境变量 "
              "FEISHU_CHAT_ID/FEISHU_USER_ID，或在 delivery/feishu_target.json 写入目标。",
              file=sys.stderr)
        return 2

    res = send_card(card, flag, val, args.identity, args.dry_run)
    sys.stdout.write(res.stdout)
    if res.stderr:
        sys.stderr.write(res.stderr)
    return res.returncode


if __name__ == "__main__":
    sys.exit(main())
