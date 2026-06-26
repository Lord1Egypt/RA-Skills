#!/usr/bin/env python3
"""Feishu contacts search CLI — sync users from Feishu directory, search by name/pinyin/department."""
import sys, os, json, argparse, time, urllib.request, urllib.parse

CACHE_FILE = os.path.expanduser("~/.openclaw/.feishu-contacts-cache.json")
BASE = "https://open.feishu.cn/open-apis"

def get_feishu_creds():
    cfg_path = os.path.expanduser("~/.openclaw/openclaw.json")
    if not os.path.exists(cfg_path):
        print("Error: ~/.openclaw/openclaw.json not found.", file=sys.stderr); sys.exit(1)
    with open(cfg_path) as f:
        cfg = json.load(f)
    ch = cfg.get("channels", {}).get("feishu", {})
    aid, asec = ch.get("appId", ""), ch.get("appSecret", "")
    if not aid or not asec:
        print("Error: channels.feishu.appId/appSecret not in openclaw.json.", file=sys.stderr); sys.exit(1)
    return aid, asec

def get_token(aid, asec):
    data = json.dumps({"app_id": aid, "app_secret": asec}).encode()
    req = urllib.request.Request(f"{BASE}/auth/v3/tenant_access_token/internal",
                                data=data, headers={"Content-Type": "application/json"})
    resp = json.loads(urllib.request.urlopen(req).read())
    if resp.get("code") != 0:
        print(f"Error getting token: {resp.get('msg')}", file=sys.stderr); sys.exit(1)
    return resp["tenant_access_token"]

def api_get(token, path, params=None):
    url = f"{BASE}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    return json.loads(urllib.request.urlopen(req).read())

def to_pinyin(name):
    try:
        from pypinyin import pinyin, Style
        full = "".join(p[0] for p in pinyin(name, style=Style.NORMAL))
        initials = "".join(p[0][0] for p in pinyin(name, style=Style.NORMAL) if p[0])
        return full, initials
    except ImportError:
        return name.lower(), ""

def cmd_sync(args):
    aid, asec = get_feishu_creds()
    token = get_token(aid, asec)
    # 1. Get all departments with i18n_name field
    all_depts = {}
    dept_queue = ["0"]
    while dept_queue:
        parent_id = dept_queue.pop(0)
        page_token = ""
        while True:
            params = {
                "parent_department_id": parent_id, 
                "page_size": "50", 
                "fetch_child": "false",
                "department_id_type": "open_department_id"
            }
            if page_token:
                params["page_token"] = page_token
            resp = api_get(token, "/contact/v3/departments", params)
            if resp.get("code") != 0:
                print(f"Error listing departments: {resp.get('msg')}", file=sys.stderr); break
            for d in resp.get("data", {}).get("items", []):
                did = d.get("open_department_id")
                if did and did not in all_depts:
                    # Try i18n_name first, then name
                    dept_name = ""
                    if d.get("i18n_name"):
                        dept_name = d["i18n_name"].get("zh_cn", "") or d["i18n_name"].get("en_us", "")
                    if not dept_name:
                        dept_name = d.get("name", "")
                    py_full, py_init = to_pinyin(dept_name)
                    all_depts[did] = {
                        "dept_id": did,
                        "name": dept_name,
                        "parent_id": d.get("parent_department_id", ""),
                        "pinyin": py_full,
                        "pinyin_initials": py_init,
                    }
                    dept_queue.append(did)
            if not resp.get("data", {}).get("has_more"):
                break
            page_token = resp["data"].get("page_token", "")
    print(f"Found {len(all_depts)} departments, syncing users...")
    # 2. Get users from each department
    all_users = {}
    dept_users = {}  # dept_id -> [user_open_ids]
    for i, dept_id in enumerate(all_depts.keys()):
        dept_users[dept_id] = []
        page_token = ""
        while True:
            params = {"department_id": dept_id, "page_size": "50", "department_id_type": "open_department_id", "user_id_type": "open_id"}
            if page_token:
                params["page_token"] = page_token
            resp = api_get(token, "/contact/v3/users/find_by_department", params)
            if resp.get("code") != 0:
                break
            for u in resp.get("data", {}).get("items", []):
                oid = u.get("open_id")
                if oid:
                    dept_users[dept_id].append(oid)
                    if oid not in all_users:
                        name = u.get("name", "")
                        py_full, py_init = to_pinyin(name)
                        all_users[oid] = {
                            "name": name, "open_id": oid,
                            "email": u.get("email", ""),
                            "en_name": u.get("en_name", ""),
                            "pinyin": py_full, "pinyin_initials": py_init,
                            "departments": []
                        }
                    all_users[oid]["departments"].append(dept_id)
            if not resp.get("data", {}).get("has_more"):
                break
            page_token = resp["data"].get("page_token", "")
        if (i + 1) % 20 == 0:
            print(f"  scanned {i+1}/{len(all_depts)} departments, {len(all_users)} users so far...")
    # 3. Save cache
    cache = {
        "synced_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "users": list(all_users.values()),
        "departments": list(all_depts.values()),
        "dept_users": dept_users
    }
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)
    print(f"Synced {len(all_users)} users and {len(all_depts)} departments to {CACHE_FILE}")

def load_cache():
    if not os.path.exists(CACHE_FILE):
        print("No cache found. Run 'sync' first.", file=sys.stderr); sys.exit(1)
    with open(CACHE_FILE) as f:
        return json.load(f)

def fuzzy_match(query, target):
    q = query.lower()
    name = target.get("name", "").lower()
    py = target.get("pinyin", "").lower()
    py_init = target.get("pinyin_initials", "").lower()
    en = target.get("en_name", "").lower() if "en_name" in target else ""
    # convert query to pinyin too
    q_py, q_init = to_pinyin(query)
    q_py = q_py.lower()
    q_init = q_init.lower()
    # exact substring on name
    if q in name or (en and q in en):
        return 100
    # query pinyin == target pinyin
    if q_py and q_py == py:
        return 95
    # pinyin full match
    if q in py:
        return 80
    # query pinyin is substring
    if len(q_py) >= 4 and q_py in py:
        return 80
    # pinyin initials match
    if q in py_init or (q_init and q_init == py_init):
        return 70
    # character-level fuzzy
    if len(q) >= 2 and len(name) >= 2:
        common = sum(1 for c in q if c in name)
        ratio = common / max(len(q), len(name))
        if ratio >= 0.5:
            return int(60 * ratio)
    # pinyin fuzzy
    if len(q_py) >= 2 and len(py) >= 2:
        common = sum(1 for c in q_py if c in py)
        ratio = common / max(len(q_py), len(py))
        if ratio >= 0.6:
            return int(50 * ratio)
    return 0

def cmd_search(args):
    query = " ".join(args.query)
    if not query:
        print("Usage: search <name>", file=sys.stderr); sys.exit(1)
    cache = load_cache()
    results = []
    for u in cache.get("users", []):
        score = fuzzy_match(query, u)
        if score > 0:
            results.append((score, u))
    results.sort(key=lambda x: -x[0])
    results = results[:10]
    if not results:
        print(f"No users found matching '{query}'.")
        return
    print(f"Found {len(results)} match(es) for '{query}':")
    print("-" * 70)
    for score, u in results:
        email_str = f"  email={u['email']}" if u.get("email") else ""
        en_str = f"  en={u['en_name']}" if u.get("en_name") else ""
        print(f"  {u['name']:<10} open_id={u['open_id']}{email_str}{en_str}  (score={score})")

def cmd_search_dept(args):
    query = " ".join(args.query)
    if not query:
        print("Usage: search-dept <department_name>", file=sys.stderr); sys.exit(1)
    cache = load_cache()
    results = []
    for d in cache.get("departments", []):
        score = fuzzy_match(query, d)
        if score > 0:
            results.append((score, d))
    results.sort(key=lambda x: -x[0])
    results = results[:10]
    if not results:
        print(f"No departments found matching '{query}'.")
        return
    print(f"Found {len(results)} department(s) matching '{query}':")
    print("-" * 70)
    for score, d in results:
        dept_users = cache.get("dept_users", {}).get(d["dept_id"], [])
        print(f"  {d['name']:<20} dept_id={d['dept_id']}  ({len(dept_users)} members, score={score})")

def cmd_list_dept(args):
    cache = load_cache()
    dept_id = args.dept_id
    # Find department
    dept = None
    for d in cache.get("departments", []):
        if d["dept_id"] == dept_id:
            dept = d
            break
    if not dept:
        print(f"Department {dept_id} not found.", file=sys.stderr); sys.exit(1)
    # Get users in this department
    user_ids = cache.get("dept_users", {}).get(dept_id, [])
    users_map = {u["open_id"]: u for u in cache.get("users", [])}
    users = [users_map[uid] for uid in user_ids if uid in users_map]
    print(f"Department: {dept['name']} ({dept_id})")
    print(f"Members: {len(users)}")
    print("-" * 70)
    for u in users:
        email_str = f"  email={u['email']}" if u.get("email") else ""
        en_str = f"  en={u['en_name']}" if u.get("en_name") else ""
        print(f"  {u['name']:<10} open_id={u['open_id']}{email_str}{en_str}")

def cmd_get(args):
    aid, asec = get_feishu_creds()
    token = get_token(aid, asec)
    resp = api_get(token, f"/contact/v3/users/{args.open_id}", {"user_id_type": "open_id"})
    if resp.get("code") != 0:
        print(f"Error: {resp.get('msg')}", file=sys.stderr); sys.exit(1)
    u = resp.get("data", {}).get("user", {})
    print(f"Name: {u.get('name', 'N/A')}")
    print(f"Open ID: {u.get('open_id', 'N/A')}")
    print(f"Union ID: {u.get('union_id', 'N/A')}")
    if u.get("email"):
        print(f"Email: {u['email']}")
    if u.get("enterprise_email"):
        print(f"Enterprise Email: {u['enterprise_email']}")
    if u.get("mobile"):
        print(f"Mobile: {u['mobile']}")
    if u.get("en_name"):
        print(f"English Name: {u['en_name']}")

def cmd_info(args):
    cache = load_cache()
    print(f"Cache file: {CACHE_FILE}")
    print(f"Synced at: {cache.get('synced_at', 'N/A')}")
    print(f"Total users: {len(cache.get('users', []))}")
    print(f"Total departments: {len(cache.get('departments', []))}")

def main():
    p = argparse.ArgumentParser(description="Feishu Contacts CLI")
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("sync", help="Sync all users and departments from Feishu directory to local cache")
    s = sub.add_parser("search", help="Search users by name or pinyin")
    s.add_argument("query", nargs="+")
    sd = sub.add_parser("search-dept", help="Search departments by name")
    sd.add_argument("query", nargs="+")
    ld = sub.add_parser("list-dept", help="List all users in a department")
    ld.add_argument("dept_id", help="Department ID (from search-dept)")
    g = sub.add_parser("get", help="Get user details by open_id (live API call)")
    g.add_argument("open_id")
    sub.add_parser("info", help="Show cache info")
    args = p.parse_args()
    cmds = {"sync": cmd_sync, "search": cmd_search, "search-dept": cmd_search_dept,
            "list-dept": cmd_list_dept, "get": cmd_get, "info": cmd_info}
    fn = cmds.get(args.cmd)
    if fn:
        fn(args)
    else:
        p.print_help()

if __name__ == "__main__":
    main()
