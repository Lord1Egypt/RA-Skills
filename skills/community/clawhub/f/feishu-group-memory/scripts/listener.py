#!/usr/bin/env python3
"""
listener.py — 飞书消息拉取与存储（纯数据操作，不调用 LLM）

命令：
  find_chat   --name TEXT                     按群名搜索
  fetch_raw   --chat_id ID [--limit N]        拉取原始消息文本，供 AI 分析
  save_records --chat_id ID --records JSON    保存 AI 分析后的结构化记录
  list        --workspace DIR [--chat_id ID]  列出已存记录
"""

import argparse, json, os, re, sys, urllib.request, urllib.error, urllib.parse
from datetime import datetime, timezone
from pathlib import Path

FEISHU_BASE      = "https://open.feishu.cn/open-apis"
OPENCLAW_CONFIG  = Path("~/.openclaw/openclaw.json").expanduser()
RECORDS_FILENAME = "feishu-memory-records.jsonl"


# ── 工具 ──────────────────────────────────────────────────────────────────────

def out(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))

def err(msg):
    out({"error": msg})
    sys.exit(1)

def records_path(workspace):
    return Path(workspace).expanduser() / RECORDS_FILENAME


# ── 凭证加载 ──────────────────────────────────────────────────────────────────

def _strip_json5(text):
    text = re.sub(r"//[^\n]*", "", text)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    text = re.sub(r",\s*([\]}])", r"\1", text)
    return text

def load_credentials():
    app_id     = os.environ.get("FEISHU_APP_ID", "").strip()
    app_secret = os.environ.get("FEISHU_APP_SECRET", "").strip()
    if app_id and app_secret:
        return app_id, app_secret
    if OPENCLAW_CONFIG.exists():
        try:
            raw = OPENCLAW_CONFIG.read_text(encoding="utf-8")
            cfg = json.loads(_strip_json5(raw))
            accounts = cfg.get("channels", {}).get("feishu", {}).get("accounts", {})
            for acct in accounts.values():
                aid = acct.get("appId", "").strip()
                asc = acct.get("appSecret", "").strip()
                if aid and asc:
                    return aid, asc
        except Exception as e:
            err(f"读取 openclaw.json 失败: {e}")
    err("未找到飞书凭证。请在 ~/.openclaw/openclaw.json 的 channels.feishu.accounts 中配置，"
        "或设置环境变量 FEISHU_APP_ID / FEISHU_APP_SECRET。")

def get_token():
    app_id, app_secret = load_credentials()
    payload = json.dumps({"app_id": app_id, "app_secret": app_secret}).encode()
    req = urllib.request.Request(
        f"{FEISHU_BASE}/auth/v3/tenant_access_token/internal",
        data=payload, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            result = json.loads(r.read().decode())
        if result.get("code") != 0:
            err(f"获取飞书 token 失败: {result.get('msg')}")
        return result["tenant_access_token"]
    except urllib.error.HTTPError as e:
        err(f"飞书鉴权失败 HTTP {e.code}: {e.read().decode(errors='replace')}")


# ── 飞书 API ──────────────────────────────────────────────────────────────────

def feishu_get(path, token):
    req = urllib.request.Request(
        f"{FEISHU_BASE}{path}",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            result = json.loads(r.read().decode())
        if result.get("code") not in (0, None):
            err(f"飞书错误 {result.get('code')}: {result.get('msg')}")
        return result
    except urllib.error.HTTPError as e:
        err(f"HTTP {e.code}: {e.read().decode(errors='replace')}")

def extract_text(item):
    """从飞书消息中提取纯文本。"""
    msg_type = item.get("msg_type", "")
    content_str = item.get("body", {}).get("content", "{}")
    try:
        content = json.loads(content_str)
    except Exception:
        return content_str
    if msg_type == "text":
        return content.get("text", "")
    elif msg_type == "post":
        lines = []
        for para_list in content.get("content", {}).values():
            for para in para_list:
                for elem in para:
                    if elem.get("tag") == "text":
                        lines.append(elem.get("text", ""))
        return " ".join(lines)
    return f"[{msg_type}]"


# ── 命令 ──────────────────────────────────────────────────────────────────────

def cmd_find_chat(args):
    token = get_token()
    query = args.name.lower()
    page_token, matched = None, []
    while True:
        path = "/im/v1/chats?page_size=100"
        if page_token:
            path += f"&page_token={urllib.parse.quote(page_token)}"
        data = feishu_get(path, token).get("data", {})
        for chat in data.get("items", []):
            name = chat.get("name", "")
            if query in name.lower():
                matched.append({"chat_id": chat.get("chat_id"), "name": name})
        if not data.get("has_more"):
            break
        page_token = data.get("page_token")
    out({"matched": matched, "total": len(matched)})


def cmd_fetch_raw(args):
    """拉取原始消息并提取文本，返回给 AI 分析。不做任何 AI 判断。"""
    token = get_token()
    messages, page_token = [], None
    limit = int(args.limit)

    while len(messages) < limit:
        path = (f"/im/v1/messages?container_id_type=chat"
                f"&container_id={urllib.parse.quote(args.chat_id)}"
                f"&page_size={min(50, limit - len(messages))}"
                f"&sort_type=ByCreateTimeDesc")
        if page_token:
            path += f"&page_token={urllib.parse.quote(page_token)}"
        data = feishu_get(path, token).get("data", {})
        items = data.get("items", [])
        if not items:
            break
        for item in items:
            ts_ms = int(item.get("create_time", 0))
            ts_str = datetime.fromtimestamp(ts_ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M") if ts_ms else ""
            text = extract_text(item)
            if text.strip():  # 跳过无文字消息（图片、文件等）
                messages.append({
                    "msg_id":  item.get("message_id", ""),
                    "time":    ts_str,
                    "sender":  item.get("sender", {}).get("id", ""),
                    "text":    text,
                })
        if not data.get("has_more"):
            break
        page_token = data.get("page_token")

    out({"messages": messages, "total": len(messages), "chat_id": args.chat_id})


def cmd_save_records(args):
    """保存 AI 已分析完毕的结构化记录。"""
    try:
        records = json.loads(args.records)
    except json.JSONDecodeError as e:
        err(f"records JSON 解析失败: {e}")

    if not isinstance(records, list):
        err("records 必须是 JSON 数组")

    rp = records_path(args.workspace)
    rp.parent.mkdir(parents=True, exist_ok=True)

    saved = 0
    with open(rp, "a", encoding="utf-8") as f:
        for record in records:
            record.setdefault("chat_id", args.chat_id)
            record.setdefault("saved_at", datetime.now(tz=timezone.utc).isoformat())
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
            saved += 1

    out({"success": True, "saved": saved, "records_file": str(rp)})


def cmd_list(args):
    rp = records_path(args.workspace)
    if not rp.exists():
        out({"records": [], "total": 0})
        return
    records = []
    with open(rp, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                r = json.loads(line)
                if args.chat_id and r.get("chat_id") != args.chat_id:
                    continue
                records.append(r)
            except Exception:
                continue
    out({"records": records, "total": len(records)})


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd")

    fc = sub.add_parser("find_chat")
    fc.add_argument("--name", required=True)

    fr = sub.add_parser("fetch_raw")
    fr.add_argument("--chat_id",   required=True)
    fr.add_argument("--limit",     default="100")
    fr.add_argument("--workspace", default="~/.openclaw/workspace")

    sr = sub.add_parser("save_records")
    sr.add_argument("--chat_id",   required=True)
    sr.add_argument("--records",   required=True)
    sr.add_argument("--workspace", default="~/.openclaw/workspace")

    ls = sub.add_parser("list")
    ls.add_argument("--workspace", default="~/.openclaw/workspace")
    ls.add_argument("--chat_id",   default="")

    args = p.parse_args()
    if   args.cmd == "find_chat":    cmd_find_chat(args)
    elif args.cmd == "fetch_raw":    cmd_fetch_raw(args)
    elif args.cmd == "save_records": cmd_save_records(args)
    elif args.cmd == "list":         cmd_list(args)
    else: err("请指定命令: find_chat | fetch_raw | save_records | list")

if __name__ == "__main__":
    main()
