#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""feishu_card.py —— 飞书 AI 交互卡片零依赖 CLI（通用版 v1.0）

任何语言/框架的智能体都能调：它是命令行工具，输入输出全是 JSON。
只用 Python 标准库（urllib），不需要 lark_oapi / requests / node 任何依赖。

它解决的是「智能体接飞书时交互难看」这件事：
  · 思考过程折叠一张卡，不刷屏
  · 战果正文独立成卡，长按整卡复制＝干净答复
  · 打字机流式输出、卡片尾部自动带状态行
  · 三个必踩的坑（缺 type / sequence 冲突 / 自定义色缺暗色）内置绕开

用法（凭据走环境变量或参数）：
    export FEISHU_APP_ID=cli_xxx
    export FEISHU_APP_SECRET=xxx

    python feishu_card.py probe  --receive-id oc_xxx          # 四步自检，全绿即装好了
    python feishu_card.py think-card --receive-id oc_xxx      # 建思考卡 → 打印 card_id
    python feishu_card.py update --card-id c_xxx --text "…"   # 打字机更新正文
    python feishu_card.py result-card --receive-id oc_xxx     # 建战果卡（正文另起一张）
    python feishu_card.py close  --card-id c_xxx              # 关流式
    python feishu_card.py send   --receive-id oc_xxx --text "（不用 CardKit 权限的降级发卡）"

所有命令都输出一行 JSON：{"ok": true, ...} / {"ok": false, "code": …, "msg": …}
失败退出码 1，方便脚本判断。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
import uuid

DEFAULT_BASE = "https://open.feishu.cn"

# 卡片元素 id：接入方按这几个 id 更新内容即可
ELEMENT_THINK_TITLE = "think_title"      # 折叠面板标题（承载 spinner）
ELEMENT_THINK_LOG = "think_log"          # 折叠面板内的全量思考日志
ELEMENT_THINK_LIVE = "think_live"        # 面板外的一行实时窗
ELEMENT_RESULT_TITLE = "result_title"    # 战果标题
ELEMENT_BODY = "streaming_content"       # 正文（打字机就更新它）

# 琥珀金主题：琥珀金（数字/指标）+ 咖啡（小标题/标签）
# 飞书要求自定义色必须明暗两套都写，缺一套报 11310。
THEME_AMBER = {
    "cus-0": {
        "light_mode": "rgba(166,124,0,1)",
        "dark_mode": "rgba(240,200,90,1)",
    },
    "cus-1": {
        "light_mode": "rgba(139,90,43,1)",
        "dark_mode": "rgba(200,155,105,1)",
    },
}
THEME_NEUTRAL = {
    "cus-0": {
        "light_mode": "rgba(71,105,175,1)",
        "dark_mode": "rgba(130,170,255,1)",
    },
    "cus-1": {
        "light_mode": "rgba(100,100,105,1)",
        "dark_mode": "rgba(180,180,185,1)",
    },
}
THEMES = {"amber": THEME_AMBER, "neutral": THEME_NEUTRAL}


# ----------------------------------------------------------------------
# HTTP（零依赖）
# ----------------------------------------------------------------------

def _request(method, url, token=None, body=None):
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json; charset=utf-8")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        try:
            return json.loads(raw)
        except ValueError:
            return {"code": exc.code, "msg": raw[:300]}


def _ok(payload):
    return int(payload.get("code") or 0) == 0


def _emit(payload, action, **extra):
    out = {"action": action, "ok": _ok(payload)}
    out.update(extra)
    if not out["ok"]:
        out["code"] = payload.get("code")
        out["msg"] = payload.get("msg")
    print(json.dumps(out, ensure_ascii=False))
    return 0 if out["ok"] else 1


# ----------------------------------------------------------------------
# 卡片模板
# ----------------------------------------------------------------------

def think_card_json(theme="amber", title="思考和工具调用过程"):
    """思考卡：首行即折叠面板标题（右侧箭头＝展开入口），下面一行实时窗。

    刻意不放正文元素 —— 正文走独立战果卡，卡片才干净、好复制。
    """
    return {
        "schema": "2.0",
        "config": {
            "streaming_mode": True,
            "style": {"color": THEMES.get(theme, THEME_AMBER)},
        },
        "body": {
            "elements": [
                {
                    "tag": "collapsible_panel",
                    "element_id": "think_panel",
                    "expanded": False,
                    "header": {
                        "title": {
                            "tag": "markdown",
                            "element_id": ELEMENT_THINK_TITLE,
                            "content": "<font color='cus-1'>**%s**</font> ⠋" % title,
                        },
                        "background_color": "grey",
                        "vertical_align": "center",
                        "icon": {
                            "tag": "standard_icon",
                            "token": "down-small-ccm_outlined",
                            "size": "16px 16px",
                        },
                        "icon_position": "right",
                        "icon_expanded_angle": -180,
                    },
                    "border": {"color": "grey", "corner_radius": "5px"},
                    "vertical_spacing": "8px",
                    "padding": "8px 8px 8px 8px",
                    "elements": [
                        {
                            "tag": "markdown",
                            "element_id": ELEMENT_THINK_LOG,
                            "content": " ",
                        },
                    ],
                },
                {
                    "tag": "markdown",
                    "element_id": ELEMENT_THINK_LIVE,
                    "content": "\u200b",
                },
            ],
        },
    }


def result_card_json(theme="amber", title="🏆 战果", body_text="\u200b"):
    """战果卡：标题 + 正文两个元素。

    正文元素 id 固定为 streaming_content —— 状态行靠
    insert_after streaming_content 追加，少了这个 id 状态行就落不进来。
    """
    return {
        "schema": "2.0",
        "config": {
            "streaming_mode": True,
            "style": {"color": THEMES.get(theme, THEME_AMBER)},
        },
        "body": {
            "direction": "vertical",
            "elements": [
                {
                    "tag": "markdown",
                    "element_id": ELEMENT_RESULT_TITLE,
                    "content": "<font color='cus-1'>**%s**</font>" % title,
                },
                {
                    "tag": "markdown",
                    "element_id": ELEMENT_BODY,
                    "content": body_text,
                },
            ],
        },
    }


def static_card_json(theme="amber", title="", text=""):
    """老版静态卡片（不走 CardKit）：兼容没开 CardKit 权限的账号。"""
    card = {
        "config": {"wide_screen_mode": True},
        "elements": [
            {"tag": "div", "text": {"tag": "lark_md", "content": text}},
        ],
    }
    if title:
        card["header"] = {
            "title": {"tag": "plain_text", "content": title},
            "template": "grey" if theme == "neutral" else "orange",
        }
    return card


# ----------------------------------------------------------------------
# API 封装
# ----------------------------------------------------------------------

class Feishu:
    def __init__(self, app_id, app_secret, base=DEFAULT_BASE, verbose=False):
        self.app_id = app_id
        self.app_secret = app_secret
        self.base = base.rstrip("/")
        self.verbose = verbose
        self._token = None

    @property
    def token(self):
        if not self._token:
            r = _request(
                "POST",
                self.base + "/open-apis/auth/v3/tenant_access_token/internal",
                body={"app_id": self.app_id, "app_secret": self.app_secret},
            )
            if not _ok(r):
                raise RuntimeError(
                    "tenant_access_token 失败: code=%s msg=%s"
                    % (r.get("code"), r.get("msg"))
                )
            self._token = r.get("tenant_access_token")
        return self._token

    def create_card(self, card_json):
        return _request(
            "POST",
            self.base + "/open-apis/cardkit/v1/cards",
            token=self.token,
            body={
                "type": "card_json",
                "data": json.dumps(card_json, ensure_ascii=False),
            },
        )

    def send_card_id(self, receive_id, receive_id_type, card_id):
        return _request(
            "POST",
            "%s/open-apis/im/v1/messages?receive_id_type=%s"
            % (self.base, receive_id_type),
            token=self.token,
            body={
                "receive_id": receive_id,
                "msg_type": "interactive",
                "content": json.dumps(
                    {"type": "card", "data": {"card_id": card_id}},
                    ensure_ascii=False,
                ),
            },
        )

    def send_static_card(self, receive_id, receive_id_type, card_json):
        return _request(
            "POST",
            "%s/open-apis/im/v1/messages?receive_id_type=%s"
            % (self.base, receive_id_type),
            token=self.token,
            body={
                "receive_id": receive_id,
                "msg_type": "interactive",
                "content": json.dumps(card_json, ensure_ascii=False),
            },
        )

    def update_element(self, card_id, element_id, text, sequence=None):
        body = {"content": text, "uuid": str(uuid.uuid4())}
        if sequence is not None:
            body["sequence"] = int(sequence)
        return _request(
            "PUT",
            "%s/open-apis/cardkit/v1/cards/%s/elements/%s/content"
            % (self.base, card_id, element_id),
            token=self.token,
            body=body,
        )

    def append_element(self, card_id, after_element_id, elements, sequence=None):
        """追加元素。

        两个必填项最容易踩：
          · type 必填（insert_after / insert_before / append），少了报 99992402
          · elements 必须是 JSON 字符串，不是数组，传数组报 9499
        """
        body = {
            "type": "insert_after",
            "target_element_id": after_element_id,
            "elements": json.dumps(elements, ensure_ascii=False),
            "uuid": str(uuid.uuid4()),
        }
        if sequence is not None:
            body["sequence"] = int(sequence)
        return _request(
            "POST",
            "%s/open-apis/cardkit/v1/cards/%s/elements" % (self.base, card_id),
            token=self.token,
            body=body,
        )

    def list_chats(self, page_size=50):
        """机器人所在的群列表 —— 用来拿 receive_id（chat_id）。"""
        return _request(
            "GET",
            "%s/open-apis/im/v1/chats?page_size=%d" % (self.base, page_size),
            token=self.token,
        )

    def close_stream(self, card_id, summary="", sequence=None):
        body = {
            "settings": json.dumps(
                {
                    "config": {
                        "streaming_mode": False,
                        "summary": {"content": summary or "\u200b"},
                    },
                },
                ensure_ascii=False,
            ),
            "uuid": str(uuid.uuid4()),
        }
        if sequence is not None:
            body["sequence"] = int(sequence)
        return _request(
            # 注意：settings 接口是 PATCH，写成 PUT 会 404（踩过）
            "PATCH",
            "%s/open-apis/cardkit/v1/cards/%s/settings" % (self.base, card_id),
            token=self.token,
            body=body,
        )


# ----------------------------------------------------------------------
# 命令
# ----------------------------------------------------------------------

def cmd_token(fs, args):
    print(json.dumps({"action": "token", "ok": True, "token_acquired": bool(fs.token)}))
    return 0


def cmd_send(fs, args):
    card = static_card_json(args.theme, args.title or "", args.text)
    r = fs.send_static_card(args.receive_id, args.receive_id_type, card)
    return _emit(r, "send", message_id=(r.get("data") or {}).get("message_id"))


def _new_card(fs, args, card_json, action):
    r = fs.create_card(card_json)
    if not _ok(r):
        return _emit(r, action)
    card_id = (r.get("data") or {}).get("card_id")
    out = {"card_id": card_id}
    if args.receive_id:
        s = fs.send_card_id(args.receive_id, args.receive_id_type, card_id)
        if not _ok(s):
            return _emit(s, action, card_id=card_id)
        out["message_id"] = (s.get("data") or {}).get("message_id")
    return _emit({"code": 0}, action, **out)


def cmd_think_card(fs, args):
    return _new_card(
        fs,
        args,
        think_card_json(args.theme, args.title or "思考和工具调用过程"),
        "think-card",
    )


def cmd_result_card(fs, args):
    return _new_card(
        fs,
        args,
        result_card_json(args.theme, args.title or "🏆 战果", args.text or "\u200b"),
        "result-card",
    )


def cmd_update(fs, args):
    if not args.card_id or not args.element_id:
        print(json.dumps({"action": "update", "ok": False, "msg": "--card-id 与 --element-id 必填"}))
        return 1
    r = fs.update_element(args.card_id, args.element_id, args.text, args.sequence)
    return _emit(r, "update", element_id=args.element_id)


def cmd_append(fs, args):
    r = fs.append_element(
        args.card_id,
        args.after_element_id or ELEMENT_BODY,
        [{"tag": "markdown", "content": args.text}],
        args.sequence,
    )
    return _emit(r, "append")


def cmd_close(fs, args):
    r = fs.close_stream(args.card_id, args.summary or "", args.sequence)
    return _emit(r, "close")


def cmd_chats(fs, args):
    """列出机器人所在的群 —— 拿 chat_id 最省事的办法。"""
    r = fs.list_chats(args.page_size)
    if not _ok(r):
        return _emit(r, "chats")
    items = (r.get("data") or {}).get("items") or []
    print(
        json.dumps(
            {
                "action": "chats",
                "ok": True,
                "count": len(items),
                "chats": [
                    {"chat_id": i.get("chat_id"), "name": i.get("name")}
                    for i in items
                ],
            },
            ensure_ascii=False,
        ),
    )
    return 0


def cmd_probe(fs, args):
    """四步自检：建卡 → 打字机 → 追加状态行 → 关流式。

    不发消息、不打扰使用者；全绿说明账号权限与网络都通了，
    而且三个经典的坑（99992402 / 300317 / 11310）都不存在。
    """
    steps = []
    r = fs.create_card(result_card_json(args.theme, "🧪 自检", "自检中…"))
    ok = _ok(r)
    steps.append({"step": "1_create_card", "ok": ok, "code": r.get("code"), "msg": r.get("msg")})
    if not ok:
        print(json.dumps({"action": "probe", "ok": False, "steps": steps}, ensure_ascii=False))
        return 1
    card_id = (r.get("data") or {}).get("card_id")

    r = fs.update_element(card_id, ELEMENT_BODY, "自检：打字机成功了。", sequence=1)
    steps.append({"step": "2_typewriter", "ok": _ok(r), "code": r.get("code"), "msg": r.get("msg")})

    r = fs.append_element(
        card_id,
        ELEMENT_BODY,
        [{"tag": "markdown", "content": "<font color='grey'>✅ 自检 · 状态行落卡</font>"}],
        sequence=2,
    )
    steps.append({"step": "3_append_status_line", "ok": _ok(r), "code": r.get("code"), "msg": r.get("msg")})

    r = fs.close_stream(card_id, "自检完成", sequence=3)
    steps.append({"step": "4_close_stream", "ok": _ok(r), "code": r.get("code"), "msg": r.get("msg")})

    all_ok = all(s["ok"] for s in steps)
    print(json.dumps({"action": "probe", "ok": all_ok, "card_id": card_id, "steps": steps}, ensure_ascii=False))
    if not all_ok:
        print(_hint(steps), file=sys.stderr)
    return 0 if all_ok else 1


def _hint(steps):
    hints = []
    codes = {s.get("code") for s in steps if not s["ok"]}
    if 99992402 in codes:
        hints.append("99992402：接口必填字段没给全（追加元素记得带 type，elements 要 JSON 字符串）")
    if 9499 in codes:
        hints.append("9499：elements 传成了数组，要 json.dumps 成字符串")
    if 300317 in codes:
        hints.append("300317：sequence 乱序（并发写同一张卡才会出现；先别传 sequence 或加锁发号）")
    if 11310 in codes:
        hints.append("11310：自定义色缺少暗色，明暗两套都要写")
    if 99991672 in codes or 99991663 in codes:
        hints.append("权限不足：后台给应用开 im:message 与 cardkit:card:write，并发布版本")
    return "排查提示：" + "；".join(hints) if hints else ""


def main(argv=None):
    p = argparse.ArgumentParser(
        description="飞书 AI 交互卡片零依赖 CLI（通用版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--app-id", default=os.getenv("FEISHU_APP_ID"))
    p.add_argument("--app-secret", default=os.getenv("FEISHU_APP_SECRET"))
    p.add_argument("--base-url", default=os.getenv("FEISHU_BASE_URL", DEFAULT_BASE))
    sub = p.add_subparsers(dest="cmd", required=True)

    def add_common(sp, need_recv=False, need_card=False):
        sp.add_argument("--receive-id", required=need_recv, default=os.getenv("FEISHU_RECEIVE_ID"))
        sp.add_argument("--receive-id-type", default=os.getenv("FEISHU_RECEIVE_ID_TYPE", "chat_id"))
        sp.add_argument("--theme", default="amber", choices=sorted(THEMES))
        if need_card:
            sp.add_argument("--card-id", required=True)
        else:
            sp.add_argument("--card-id", default="")
        sp.add_argument("--text", default="")
        sp.add_argument("--title", default="")
        sp.add_argument("--summary", default="")
        sp.add_argument("--sequence", type=int, default=None)
        sp.add_argument("--element-id", default=ELEMENT_BODY)
        sp.add_argument("--after-element-id", default=ELEMENT_BODY)

    add_common(sub.add_parser("token", help="只验凭据能不能换到 tenant_access_token"))
    _chats = sub.add_parser("chats", help="列出机器人所在的群（拿 chat_id 最省事）")
    _chats.add_argument("--page-size", type=int, default=50)
    add_common(sub.add_parser("probe", help="四步自检（不发消息）"))
    add_common(sub.add_parser("send", help="发静态卡片（不需要 CardKit 权限）"), need_recv=True)
    add_common(sub.add_parser("think-card", help="建思考卡并发消息"), need_recv=True)
    add_common(sub.add_parser("result-card", help="建战果卡并发消息"), need_recv=True)
    add_common(sub.add_parser("update", help="更新元素（打字机）"), need_recv=False, need_card=True)
    add_common(sub.add_parser("append", help="元素后追加（状态行）"), need_recv=False, need_card=True)
    add_common(sub.add_parser("close", help="关流式并收起"), need_recv=False, need_card=True)

    args = p.parse_args(argv)
    if not args.app_id or not args.app_secret:
        print(
            json.dumps(
                {
                    "ok": False,
                    "msg": "缺少凭据：请设置 FEISHU_APP_ID / FEISHU_APP_SECRET 或传 --app-id/--app-secret",
                },
                ensure_ascii=False,
            ),
        )
        return 1
    if args.cmd in ("send", "think-card", "result-card") and not args.receive_id:
        print(json.dumps({"ok": False, "msg": "%s 需要 --receive-id" % args.cmd}, ensure_ascii=False))
        return 1

    fs = Feishu(args.app_id, args.app_secret, args.base_url)
    handler = {
        "token": cmd_token,
        "chats": cmd_chats,
        "probe": cmd_probe,
        "send": cmd_send,
        "think-card": cmd_think_card,
        "result-card": cmd_result_card,
        "update": cmd_update,
        "append": cmd_append,
        "close": cmd_close,
    }[args.cmd]
    try:
        return handler(fs, args)
    except RuntimeError as exc:
        print(json.dumps({"ok": False, "msg": str(exc)}, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    sys.exit(main())
