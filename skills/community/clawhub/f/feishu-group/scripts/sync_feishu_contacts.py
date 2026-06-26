#!/usr/bin/env python3
"""
Sync Feishu contacts into USER.md.

Pulls the full user list from Feishu contacts API using app credentials
from openclaw.json, then updates the contacts table in USER.md.

Usage:
    python3 sync_feishu_contacts.py <openclaw_config> <account_name> <user_md_path>

Example:
    python3 sync_feishu_contacts.py ~/.openclaw/openclaw.json fourier ~/workspace/USER.md
"""
import json, os, sys, urllib.request, re

def main():
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <config_path> <app_name> <user_md_path>")
        sys.exit(1)

    config_path = os.path.expanduser(sys.argv[1])
    app_name = sys.argv[2]
    user_md_path = os.path.expanduser(sys.argv[3])

    # 1. Read config and get app credentials
    with open(config_path) as f:
        cfg = json.load(f)

    try:
        acct = cfg["channels"]["feishu"]["accounts"][app_name]
    except KeyError:
        print(f"Error: account '{app_name}' not found in {config_path}")
        print(f"Available accounts: {list(cfg.get('channels', {}).get('feishu', {}).get('accounts', {}).keys())}")
        sys.exit(1)

    # 2. Get tenant access token
    req = urllib.request.Request(
        "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data=json.dumps({
            "app_id": acct["appId"],
            "app_secret": acct["appSecret"]
        }).encode(),
        headers={"Content-Type": "application/json"}
    )
    resp = json.loads(urllib.request.urlopen(req).read())
    if resp.get("code", 0) != 0:
        print(f"Error getting token: {resp.get('msg', 'unknown error')}")
        sys.exit(1)
    token = resp["tenant_access_token"]

    # 3. Fetch all users (paginated)
    users = []
    page_token = None
    while True:
        url = "https://open.feishu.cn/open-apis/contact/v3/users/find_by_department?department_id=0&page_size=50"
        if page_token:
            url += f"&page_token={page_token}"
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        })
        data = json.loads(urllib.request.urlopen(req).read()).get("data", {})
        for u in data.get("items", []):
            name = u.get("name", "")
            open_id = u.get("open_id", "")
            if name and open_id:
                users.append({"name": name, "open_id": open_id})
        if not data.get("has_more"):
            break
        page_token = data.get("page_token")

    if not users:
        print("Warning: no users found. Check app permissions (need contact:user.base:readonly).")
        sys.exit(1)

    # 4. Update USER.md contacts table
    TABLE_HEADER = "| 姓名 | open_id |\n|------|---------|"
    table_rows = "\n".join(f"| {u['name']} | {u['open_id']} |" for u in users)

    with open(user_md_path, "r") as f:
        content = f.read()

    # Match: ## 飞书通讯录 ... header line ... description line ... | table |
    pattern = r"(## 飞书通讯录[^\n]*\n[^\n]*\n)\| 姓名 \| open_id \|\n\|[-| ]*\n((\|[^\n]*\n)*)"
    new_table = f"\\1{TABLE_HEADER}\n{table_rows}\n"
    new_content = re.sub(pattern, new_table, content)

    if new_content == content:
        # Check if the section exists at all
        if "## 飞书通讯录" not in content:
            print(f"Error: USER.md has no '## 飞书通讯录' section. Add it first:")
            print(f"  ## 飞书通讯录 ({app_name} App)")
            print(f"  飞书 DM 不携带发送者姓名。用 inbound metadata 的 chat_id（格式 `user:ou_xxx`）匹配下表识别发送者。")
            print(f"  | 姓名 | open_id |")
            print(f"  |------|---------|")
            sys.exit(1)
        print(f"OK: {len(users)} users (USER.md unchanged)")
    else:
        with open(user_md_path, "w") as f:
            f.write(new_content)
        print(f"OK: {len(users)} users → USER.md updated")

if __name__ == "__main__":
    main()
