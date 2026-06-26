#!/usr/bin/env python3
"""
飞书群管理脚本（付费版）
集成 SkillPay 计费 — https://skillpay.me

凭证自动从以下来源读取（优先级从高到低）：
  1. 环境变量 FEISHU_APP_ID / FEISHU_APP_SECRET
  2. ~/.openclaw/openclaw.json → channels.feishu.accounts.<任意>.appId/appSecret

命令：
  check_permissions            检查当前应用已授权的权限，对比群管理所需权限
  get_token                    获取 tenant_access_token（免费）
  list_chats                   列出所有群（免费）
  find_chat     --name 名称    模糊搜索群（免费）
  list_members  --chat_id ID   查看群成员（免费）
  find_user     --name 姓名    搜索企业成员（免费）
  add_member    --chat_id --target_user_id --user_id   拉人进群（计费）
  remove_member --chat_id --target_user_id --user_id   踢人（计费）
  send_message  --chat_id --text --user_id              发消息（计费）
  rename_chat   --chat_id --name --user_id              改群名（计费）
  create_chat   --name --user_ids --user_id             建群（计费）
"""

import argparse, json, os, sys
import urllib.request, urllib.error, urllib.parse

# ── 权限定义 ──────────────────────────────────────────────────────────────────

# 群管理功能所需权限，及对应功能说明
REQUIRED_SCOPES = {
    "im:chat":                    "读写群基本信息（查群列表、改群名、建群）",
    "im:chat.member":             "管理群成员（拉人进群、踢人、查成员）",
    "im:message:send_as_bot":     "以机器人身份发送消息",
    "contact:user.id:readonly":   "按姓名搜索企业成员",
}

# 飞书聊天接入时已默认授权的权限（建立 OpenClaw 连接时必须有）
CHAT_DEFAULT_SCOPES = {
    "im:message",
    "im:message.group_at_msg:readonly",
    "im:message.p2p_msg:readonly",
    "im:message:send_as_bot",
    "im:resource",
}

FEISHU_BASE       = "https://open.feishu.cn/open-apis"
SKILLPAY_BASE     = "https://skillpay.me"
SKILLPAY_SKILL_ID = "4e5f95c0-67f2-4093-950c-a4b705107778"
PRICE_PER_WRITE   = float(os.environ.get("SKILLPAY_PRICE", "0.002"))
FREE_COMMANDS     = {"check_permissions", "get_token", "find_chat",
                     "list_chats", "find_user", "list_members"}


# ── 凭证读取 ──────────────────────────────────────────────────────────────────

def load_credentials():
    """
    自动从环境变量或 openclaw.json 读取 App ID 和 App Secret。
    返回 (app_id, app_secret) 或在找不到时退出。
    """
    # 1. 环境变量优先
    app_id     = os.environ.get("FEISHU_APP_ID", "").strip()
    app_secret = os.environ.get("FEISHU_APP_SECRET", "").strip()
    if app_id and app_secret:
        return app_id, app_secret

    # 2. 从 ~/.openclaw/openclaw.json 读取
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                raw = f.read()
            # openclaw.json 是 JSON5 格式（允许注释和末尾逗号），
            # 用简单方式去掉单行注释后解析
            import re
            cleaned = re.sub(r'//[^\n]*', '', raw)   # 去掉 // 注释
            cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)  # 去掉末尾逗号
            cfg = json.loads(cleaned)

            feishu_cfg = cfg.get("channels", {}).get("feishu", {})
            accounts   = feishu_cfg.get("accounts", {})

            # 取第一个有效账户
            for acct_id, acct in accounts.items():
                aid = acct.get("appId", "").strip()
                asc = acct.get("appSecret", "").strip()
                if aid and asc:
                    return aid, asc

        except Exception:
            pass  # 解析失败则继续尝试其他方式

    err(
        "未找到飞书应用凭证。\n"
        "请确认 ~/.openclaw/openclaw.json 中已配置 channels.feishu.accounts，\n"
        "或设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET。"
    )


# ── 工具函数 ──────────────────────────────────────────────────────────────────

def err(msg, code=1):
    print(json.dumps({"error": msg}, ensure_ascii=False))
    sys.exit(code)

def http(method, url, body=None, headers=None):
    h = {"Content-Type": "application/json; charset=utf-8"}
    if headers: h.update(headers)
    data = json.dumps(body, ensure_ascii=False).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        err(f"HTTP {e.code}: {e.read().decode(errors='replace')}")
    except urllib.error.URLError as e:
        err(f"网络错误: {e.reason}")

def feishu(method, path, token=None, body=None):
    headers = {}
    if token: headers["Authorization"] = f"Bearer {token}"
    result = http(method, f"{FEISHU_BASE}{path}", body=body, headers=headers)
    if result.get("code") not in (0, None, 200):
        err(f"飞书错误 {result.get('code')}: {result.get('msg', '未知')}")
    return result

def get_token_internal():
    app_id, app_secret = load_credentials()
    r = feishu("POST", "/auth/v3/tenant_access_token/internal",
               body={"app_id": app_id, "app_secret": app_secret})
    return r["tenant_access_token"]


# ── SkillPay 计费 ─────────────────────────────────────────────────────────────

def _skillpay_headers():
    api_key = "sk_e8d7b86db13746fdbdd3a02d34f118a276d32629b3ef8bc55838d68f560e2c1b"
    if not api_key:
    return {"X-API-Key": api_key}

def require_payment(user_id, command):
    """写操作前调用。余额不足时输出付款链接并以 exit code 2 退出。"""
    free = FREE_COMMANDS.copy()
    extra = os.environ.get("SKILLPAY_FREE_CMDS", "")
    if extra:
        free.update(c.strip() for c in extra.split(","))
    if command in free:
        return

    if not user_id:
        err("写操作需要 --user_id（用于计费）")

    try:
        # POST /api/v1/billing/charge
        result = http(
            "POST",
            f"{SKILLPAY_BASE}/api/v1/billing/charge",
            body={
                "user_id":  user_id,
                "skill_id": SKILLPAY_SKILL_ID,
                "amount":   PRICE_PER_WRITE,
            },
            headers=_skillpay_headers()
        )
    except SystemExit:
        return  # 计费服务不可用时降级放行

    if result.get("success"):
        return  # 扣费成功，继续执行

    # 余额不足，SkillPay 已在响应里附上 payment_url
    payment_url = result.get("payment_url") or _get_payment_link(user_id)
    print(json.dumps({
        "error":          "payment_required",
        "message":        (
            f"余额不足，无法执行此操作 💳\n"
            f"每次操作费用：{PRICE_PER_WRITE} USDT\n"
            f"当前余额：{result.get('balance', 0)} USDT\n"
            f"请充值后继续：{payment_url}"
        ),
        "payment_url":    payment_url,
        "balance":        result.get("balance", 0),
        "price_per_call": PRICE_PER_WRITE,
    }, ensure_ascii=False))
    sys.exit(2)


def _get_payment_link(user_id, amount=5.0):
    """主动生成充值链接（POST /api/v1/billing/payment-link）。"""
    try:
        result = http(
            "POST",
            f"{SKILLPAY_BASE}/api/v1/billing/payment-link",
            body={"user_id": user_id, "amount": amount},
            headers=_skillpay_headers()
        )
        return result.get("payment_url", "https://skillpay.me")
    except SystemExit:
        return "https://skillpay.me"


# ── 权限检查 ──────────────────────────────────────────────────────────────────

def cmd_check_permissions(args):
    """
    获取当前应用已授权的权限列表，与群管理所需权限对比。
    输出缺失权限及引导用户开通的说明。
    """
    token = get_token_internal()
    app_id, _ = load_credentials()

    # 调用飞书应用信息接口获取已授权权限
    # 注：飞书没有直接"列出当前 token 权限"的接口，
    # 用 /application/v6/applications/self 获取应用基础信息，
    # 通过实际调用各权限依赖的 API 探测来判断
    granted = set()
    missing = {}

    # ── 探测1：im:chat — 尝试列出群列表
    try:
        r = http("GET", f"{FEISHU_BASE}/im/v1/chats?page_size=1",
                 headers={"Authorization": f"Bearer {token}"})
        if r.get("code") == 0:
            granted.add("im:chat")
        elif r.get("code") == 99991672:  # 权限不足
            missing["im:chat"] = REQUIRED_SCOPES["im:chat"]
    except SystemExit:
        missing["im:chat"] = REQUIRED_SCOPES["im:chat"]

    # ── 探测2：im:chat.member — 尝试查询某个群成员（用一个不存在的chat_id，只看错误码）
    try:
        r = http("GET", f"{FEISHU_BASE}/im/v1/chats/PROBE_ID/members?page_size=1",
                 headers={"Authorization": f"Bearer {token}"})
        code = r.get("code")
        if code == 0 or code == 230013:  # 230013 = chat not found，说明接口可达
            granted.add("im:chat.member")
        elif code == 99991672:
            missing["im:chat.member"] = REQUIRED_SCOPES["im:chat.member"]
        else:
            # 其他错误码也说明接口可达，权限存在
            granted.add("im:chat.member")
    except SystemExit:
        missing["im:chat.member"] = REQUIRED_SCOPES["im:chat.member"]

    # ── 探测3：im:message:send_as_bot — 发消息权限（发到不存在的chat_id，看错误码）
    try:
        r = http("POST", f"{FEISHU_BASE}/im/v1/messages?receive_id_type=chat_id",
                 body={"receive_id": "PROBE_ID", "msg_type": "text",
                       "content": json.dumps({"text": "probe"})},
                 headers={"Authorization": f"Bearer {token}"})
        code = r.get("code")
        if code == 0 or code in (230013, 230001):  # chat not found = 权限有
            granted.add("im:message:send_as_bot")
        elif code == 99991672:
            missing["im:message:send_as_bot"] = REQUIRED_SCOPES["im:message:send_as_bot"]
        else:
            granted.add("im:message:send_as_bot")
    except SystemExit:
        missing["im:message:send_as_bot"] = REQUIRED_SCOPES["im:message:send_as_bot"]

    # ── 探测4：contact:user.id:readonly — 搜索用户
    try:
        r = http("POST", f"{FEISHU_BASE}/contact/v3/users/search",
                 body={"query": "probe", "page_size": 1, "user_id_type": "open_id"},
                 headers={"Authorization": f"Bearer {token}"})
        code = r.get("code")
        if code == 0 or code == 1220001:  # 1220001 = 空结果
            granted.add("contact:user.id:readonly")
        elif code == 99991672:
            missing["contact:user.id:readonly"] = REQUIRED_SCOPES["contact:user.id:readonly"]
        else:
            granted.add("contact:user.id:readonly")
    except SystemExit:
        missing["contact:user.id:readonly"] = REQUIRED_SCOPES["contact:user.id:readonly"]

    # ── 输出结果
    result = {
        "app_id": app_id,
        "granted": sorted(list(granted)),
        "missing": missing,
        "all_ok": len(missing) == 0
    }

    if missing:
        # 生成用户友好的补权限说明
        scope_list = "\n".join(f"  • {s}（{desc}）" for s, desc in missing.items())
        result["action_required"] = (
            f"当前飞书应用缺少以下权限，群管理功能无法正常使用：\n{scope_list}\n\n"
            f"请按以下步骤补充权限（约2分钟）：\n"
            f"1. 打开 https://open.feishu.cn/app\n"
            f"2. 找到您的应用（App ID: {app_id}），点击进入\n"
            f"3. 左侧菜单 → 「权限管理」\n"
            f"4. 搜索并开通上方列出的每个权限\n"
            f"5. 左侧菜单 → 「版本管理与发布」→ 创建新版本 → 申请发布\n"
            f"6. 等管理员审批后（通常几分钟），重新发送您的请求"
        )

    print(json.dumps(result, ensure_ascii=False, indent=2))


# ── 飞书命令 ──────────────────────────────────────────────────────────────────

def cmd_get_token(a):
    app_id, app_secret = load_credentials()
    r = feishu("POST", "/auth/v3/tenant_access_token/internal",
               body={"app_id": app_id, "app_secret": app_secret})
    print(json.dumps({"token": r["tenant_access_token"],
                      "expires_in": r.get("expire", 7200)}, ensure_ascii=False))

def cmd_list_chats(a):
    chats, pt = [], None
    while True:
        path = "/im/v1/chats?page_size=100" + (f"&page_token={urllib.parse.quote(pt)}" if pt else "")
        d = feishu("GET", path, token=a.token).get("data", {})
        chats += [{"chat_id": i["chat_id"], "name": i.get("name", ""),
                   "member_count": i.get("member_count", 0)} for i in d.get("items", [])]
        if not d.get("has_more"): break
        pt = d.get("page_token")
    print(json.dumps({"chats": chats, "total": len(chats)}, ensure_ascii=False))

def cmd_find_chat(a):
    if not a.name: err("缺少 --name")
    all_chats, pt = [], None
    while True:
        path = "/im/v1/chats?page_size=100" + (f"&page_token={urllib.parse.quote(pt)}" if pt else "")
        d = feishu("GET", path, token=a.token).get("data", {})
        all_chats += [{"chat_id": i["chat_id"], "name": i.get("name", ""),
                       "member_count": i.get("member_count", 0)} for i in d.get("items", [])]
        if not d.get("has_more"): break
        pt = d.get("page_token")
    kw = a.name.lower()
    matches = [c for c in all_chats if kw in c["name"].lower()]
    print(json.dumps({"matches": matches, "total": len(matches)}, ensure_ascii=False))

def cmd_list_members(a):
    if not a.chat_id: err("缺少 --chat_id")
    members, pt = [], None
    while True:
        path = f"/im/v1/chats/{a.chat_id}/members?page_size=100" + (f"&page_token={urllib.parse.quote(pt)}" if pt else "")
        d = feishu("GET", path, token=a.token).get("data", {})
        members += [{"user_id": i.get("member_id", ""), "name": i.get("name", "")}
                    for i in d.get("items", [])]
        if not d.get("has_more"): break
        pt = d.get("page_token")
    print(json.dumps({"members": members, "total": len(members)}, ensure_ascii=False))

def cmd_find_user(a):
    if not a.name: err("缺少 --name")
    r = feishu("POST", "/contact/v3/users/search", token=a.token,
               body={"query": a.name, "page_size": 20, "user_id_type": "open_id"})
    users = [{"user_id": u.get("open_id", ""), "name": u.get("name", ""),
              "email": u.get("email", ""),
              "department": "/".join(u.get("department_path", []))}
             for u in r.get("data", {}).get("users", [])]
    print(json.dumps({"users": users, "total": len(users)}, ensure_ascii=False))

def cmd_add_member(a):
    require_payment(a.user_id, "add_member")
    if not a.chat_id or not a.target_user_id: err("缺少 --chat_id 或 --target_user_id")
    feishu("POST", f"/im/v1/chats/{a.chat_id}/members", token=a.token,
           body={"member_id_type": "open_id", "id_list": [a.target_user_id]})
    print(json.dumps({"success": True, "message": "成员添加成功"}, ensure_ascii=False))

def cmd_remove_member(a):
    require_payment(a.user_id, "remove_member")
    if not a.chat_id or not a.target_user_id: err("缺少 --chat_id 或 --target_user_id")
    feishu("DELETE", f"/im/v1/chats/{a.chat_id}/members", token=a.token,
           body={"member_id_type": "open_id", "id_list": [a.target_user_id]})
    print(json.dumps({"success": True, "message": "成员移除成功"}, ensure_ascii=False))

def cmd_send_message(a):
    require_payment(a.user_id, "send_message")
    if not a.chat_id or not a.text: err("缺少 --chat_id 或 --text")
    feishu("POST", "/im/v1/messages?receive_id_type=chat_id", token=a.token,
           body={"receive_id": a.chat_id, "msg_type": "text",
                 "content": json.dumps({"text": a.text}, ensure_ascii=False)})
    print(json.dumps({"success": True, "message": "消息发送成功"}, ensure_ascii=False))

def cmd_rename_chat(a):
    require_payment(a.user_id, "rename_chat")
    if not a.chat_id or not a.name: err("缺少 --chat_id 或 --name")
    feishu("PUT", f"/im/v1/chats/{a.chat_id}", token=a.token, body={"name": a.name})
    print(json.dumps({"success": True, "message": f"群名已改为：{a.name}"}, ensure_ascii=False))

def cmd_create_chat(a):
    require_payment(a.user_id, "create_chat")
    if not a.name: err("缺少 --name")
    body = {"name": a.name, "user_id_type": "open_id"}
    if a.user_ids:
        body["user_ids"] = [u.strip() for u in a.user_ids.split(",") if u.strip()]
    d = feishu("POST", "/im/v1/chats", token=a.token, body=body).get("data", {})
    print(json.dumps({"success": True, "chat_id": d.get("chat_id", ""),
                      "message": f"群「{a.name}」创建成功"}, ensure_ascii=False))


# ── CLI ───────────────────────────────────────────────────────────────────────

COMMANDS = {
    "check_permissions": cmd_check_permissions,
    "get_token":         cmd_get_token,
    "list_chats":        cmd_list_chats,
    "find_chat":         cmd_find_chat,
    "list_members":      cmd_list_members,
    "find_user":         cmd_find_user,
    "add_member":        cmd_add_member,
    "remove_member":     cmd_remove_member,
    "send_message":      cmd_send_message,
    "rename_chat":       cmd_rename_chat,
    "create_chat":       cmd_create_chat,
}

def main():
    p = argparse.ArgumentParser(description="飞书群管理工具（付费版）")
    p.add_argument("command", choices=list(COMMANDS.keys()))
    p.add_argument("--token");            p.add_argument("--user_id")
    p.add_argument("--name");             p.add_argument("--chat_id")
    p.add_argument("--target_user_id");   p.add_argument("--user_ids")
    p.add_argument("--text")
    a = p.parse_args()
    COMMANDS[a.command](a)

if __name__ == "__main__":
    main()
