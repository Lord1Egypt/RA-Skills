#!/usr/bin/env python3
"""reauth.py — 不扫码的重新授权：把授权按钮直接发到你的 IM 里。

为什么能这样
------------
bot 身份用 app_id/app_secret（长期有效），与 **user token 是两套凭证**。
所以 user token 过期时，bot 照样能给你发消息 —— 这就是「授权消息卡片」成立的前提。

权限边界（重要，且与具体账号无关）
----------------------------------
`lark-cli auth login` 在**不带 --scope / --domain / --recommend 时，等价于 --domain all**，
会顺手把应用已开通的全部业务域都申请一遍（实测会多出妙搭的 spark:app:read/write）。
本脚本因此**永远显式传 --scope**，并按下述策略自动适配**任何账号 / 任何应用**：

- `keep`（默认）：有历史授权 → 原样沿用 `auth status` 里的已授予集合（新增恒为 0）；
  无历史授权 → 落到最小集
- `minimal`：只用「`FEISHU_REQUIRED` 必需集 ∩ 应用已开通」——首次安装、或主动收窄时用
- 应用侧已删除的 scope 自动剔除（否则整个 OAuth 会失败），未开通的必需权限单独报出
- 出现新增权限 → 直接拒跑，必须 `--add ... --allow-add`

飞书流程（全自动）
------------------
1. `lark-cli auth login --no-wait --json --scope "<现有权限>"`  → 拿到 verification_url + device_code（10 分钟有效）
2. 以 **bot 身份** 发一张卡片到你的私聊，按钮直链 verification_url（URL 里已带 user_code）
3. 你在飞书里点一下 → 确认授权（不需要扫码、不需要回终端）
4. `lark-cli auth login --device-code <code>` 收尾 → 校验 tokenStatus

用法
----
  python3 scripts/reauth.py feishu                  # 需要时才发卡片，然后等你在飞书点（阻塞至多 10 分钟）
  python3 scripts/reauth.py feishu --detach         # 发完立刻返回，稍后用 --complete 收尾（推荐给 agent）
  python3 scripts/reauth.py feishu --complete CODE  # 你点完后收尾
  python3 scripts/reauth.py feishu --force          # 即使当前 token 有效也发（验证卡片通路用）
  python3 scripts/reauth.py feishu --no-send        # 不发卡片，只打印链接（终端场景）
  python3 scripts/reauth.py feishu --show-scope     # 只打印本次会申请哪些权限，不做任何事
  python3 scripts/reauth.py wecom|dingtalk          # 说明为什么卡片不适用 + 正确路径

退出码：0=授权完成/无需授权 · 3=已发出卡片待你点击 · 2=失败 · 4=该平台不支持卡片（附替代方案）
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

ENV_PATH = os.path.join(os.environ.get("IM_STANDIN_DIR")
                        or os.path.expanduser("~/.im-standin"), "env.json")

# 本 skill 实际用到的飞书权限 —— 只列「脚本真会调的命令」对应的权限，多一项都不列。
# 三元组 = (scope, 用途, 是否必须出现在「应用已开通」列表里)
#   最后一个 False 表示平台基础 scope：`auth scopes` 通常不列它，但依旧要申请，
#   不能因此报警（否则每个人首次用都会看到一条无意义的告警）。
FEISHU_REQUIRED = [
    ("im:message:readonly",              "读历史消息（im +chat-messages-list）", True),
    ("im:message.p2p_msg:get_as_user",   "读单聊消息", True),
    ("im:message.group_msg:get_as_user", "读群消息", True),
    ("im:message.send_as_user",          "以本人身份发消息（+messages-send --as user）", True),
    ("im:chat:read",                     "查会话信息（+chat-list）", True),
    ("im:chat.members:read",             "群成员（判「是不是本人」防回环）", True),
    ("im:feed.shortcut:read",            "最近会话（语料抓取的降级路径）", True),
    ("contact:user:search",              "--find 按名字解析目标", True),
    ("contact:user.basic_profile:readonly", "姓名/头像等基础资料", True),
    ("auth:user.id:read",                "取本人 open_id（平台基础 scope）", False),
    ("offline_access",                   "换 refresh token（否则 2 小时一续）", True),
]
REQUIRED_SCOPES = [s for s, _, _ in FEISHU_REQUIRED]
BASE_SCOPES = {s for s, _, listed in FEISHU_REQUIRED if not listed}


def minimal_scopes(app_enabled=None):
    """最小集 = 本 skill 必需 ∩ 应用已开通（基础 scope 始终保留）。

    返回 (scopes, 应用没开通的)。取交集很重要：应用没开通的权限，申请了 OAuth 也会报错 ——
    宁可少申请并提示，也不要让用户点开同意页却授权失败。
    """
    if not app_enabled:
        return list(REQUIRED_SCOPES), []
    enabled = set(app_enabled) | BASE_SCOPES
    have = [s for s in REQUIRED_SCOPES if s in enabled]
    lack = [s for s in REQUIRED_SCOPES if s not in enabled]
    return have, lack



def run(argv, timeout=60, stdin=None):
    try:
        p = subprocess.run(argv, capture_output=True, text=True,
                           timeout=timeout, input=stdin)
    except FileNotFoundError:
        return 127, None, f"not found: {argv[0]}"
    except subprocess.TimeoutExpired:
        return 124, None, "timeout"
    raw = (p.stdout or "").strip()
    try:
        obj, _ = json.JSONDecoder().raw_decode(raw.lstrip())
    except Exception:
        obj = None
    return p.returncode, obj, (raw + ("\n" + p.stderr if p.stderr else "")).strip()


# ------------------------------------------------------------------ 卡片
def build_card(url, user_code, minutes, who="分身", scope_count=0, scope_note=""):
    """飞书交互卡片：一个按钮直链授权页，附 user_code 兜底。"""
    if scope_note:
        same = scope_note
    elif scope_count:
        same = f"权限范围与你现有完全一致（{scope_count} 项），**不会新增授权**。"
    else:
        same = "不会新增授权。"
    return {
        "config": {"wide_screen_mode": True, "enable_forward": False},
        "header": {"template": "blue",
                   "title": {"tag": "plain_text",
                             "content": f"{who}需要重新授权（点一下即可）"}},
        "elements": [
            {"tag": "div", "text": {"tag": "lark_md", "content":
                "**不用扫码，也不用回终端**：点下面按钮 → 确认授权 即可续期。\n"
                f"{same}\n"
                f"链接 {minutes} 分钟内有效，过期就再发一次。"}},
            {"tag": "action", "actions": [{
                "tag": "button",
                "text": {"tag": "plain_text", "content": "一键续期授权"},
                "type": "primary", "url": url}]},
            {"tag": "note", "elements": [{"tag": "plain_text", "content":
                f"按钮打不开时，打开链接后输入：{user_code}　｜　"
                "此卡片等同于登录凭证，勿转发给他人。"}]},
        ],
    }


def self_open_id():
    """取本人 open_id：优先 auth status，其次 env.json 缓存。"""
    rc, obj, _ = run(["lark-cli", "auth", "status"], timeout=25)
    if isinstance(obj, dict):
        ou = (((obj.get("identities") or {}).get("user") or {}).get("openId"))
        if ou:
            return ou
    try:
        with open(ENV_PATH) as f:
            env = json.load(f)
        return ((env.get("platforms", {}).get("feishu") or {}).get("self_id")) or ""
    except Exception:
        return ""


def _alive(ts):
    """ISO 时间串是否还在未来（无时区按 UTC 处理）。"""
    try:
        dt = datetime.fromisoformat(str(ts).replace("Z", "+00:00"))
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt > datetime.now(timezone.utc)
    except Exception:
        return False


def token_state():
    """返回 (ok, 描述)。ok=True 表示 refresh 还活着 —— CLI 会自己刷 access，不必打扰用户。"""
    rc, obj, raw = run(["lark-cli", "auth", "status"], timeout=25)
    if not isinstance(obj, dict):
        return False, f"auth status 解析失败: {raw[:120]}"
    u = (obj.get("identities") or {}).get("user") or {}
    tok = u.get("tokenStatus")
    refresh = u.get("refreshExpiresAt")
    ok = tok == "valid" or _alive(refresh)
    return ok, f"tokenStatus={tok} refreshExpiresAt={refresh}"


def granted_scopes():
    """当前 token 已授予的权限集合（= 用户以前同意过的范围）。"""
    rc, obj, _ = run(["lark-cli", "auth", "status"], timeout=25)
    if not isinstance(obj, dict):
        return []
    s = (((obj.get("identities") or {}).get("user") or {}).get("scope")) or ""
    return s.split()


def app_scopes():
    """应用侧已开通的权限（供诊断：说明为什么 consent 页会多出某个域）。"""
    rc, obj, _ = run(["lark-cli", "auth", "scopes", "--json"], timeout=30)
    if not isinstance(obj, dict):
        return []
    return obj.get("userScopes") or []


def resolve_scopes(args, cur=None, app=None):
    """算出本次要申请的 scope。返回 dict（见下方键），纯函数，便于测试与复用。

    策略优先级：--scope 显式 > --policy minimal > keep（默认）

    - keep   ：有历史授权 → **原样沿用**（新增恒为 0）；无历史授权 → 最小集
    - minimal：只用「本 skill 必需 ∩ 应用已开通」，用于首次安装或主动收窄

    另做两道自适应：
    - **应用侧已不列出的 scope** → minimal/explicit 模式剔除（否则整个 OAuth 会失败）；
      keep 模式保留但提示（历史上真拿到过，剔除可能丢基础能力）
    - **应有但没有的必需权限**单独报 `missing`，不静默忽略、也不偷偷补（补=扩权）
    """
    if cur is None:
        cur = granted_scopes()
    if app is None:
        app = app_scopes()
    appset = set(app) if app else set()

    minimal, lack_on_app = minimal_scopes(app)
    policy = "explicit" if args.scope else (args.policy or "keep")

    if args.scope:
        requested = args.scope.replace(",", " ").split()
    elif policy == "minimal":
        requested = list(minimal)
    else:  # keep
        requested = list(cur) if cur else list(minimal)
    if args.add:
        requested += args.add.replace(",", " ").split()

    seen, uniq = set(), []
    for s in requested:
        if s and s not in seen:
            seen.add(s)
            uniq.append(s)

    # 应用侧「已不列出」的权限：
    # - keep 模式**不剔除**——它们是你历史上真拿到过的，剔除反而可能让 self_id 之类的
    #   基础能力丢失；只提示，真报错时再用 --policy minimal 收窄
    # - minimal / explicit 模式**剔除**——这些是本次现拼的，应用没开通就别申请
    unavailable = [s for s in uniq
                   if appset and s not in appset and s not in BASE_SCOPES]
    drop = policy != "keep"
    final = [s for s in uniq
             if (not drop) or (not appset) or s in appset or s in BASE_SCOPES]

    base = set(cur)
    added = [s for s in final if s not in base] if base else []
    dropped = [s for s in cur if s not in set(final)]
    missing = [s for s in REQUIRED_SCOPES if s not in set(cur)] if cur else []
    return {"requested": final, "added": added, "dropped": dropped,
            "missing": missing, "unavailable": unavailable,
            "drop_unavailable": drop, "lack_on_app": lack_on_app, "policy": policy}


def guard_scopes(plan, allow_add):
    """扩权闸门：出现新权限就拒跑（除非 --allow-add）。返回 True=放行。"""
    added = plan["added"]
    if not added:
        return True
    if allow_add:
        print(f"[warn] 本次会**新增** {len(added)} 项权限（已用 --allow-add 放行）：",
              file=sys.stderr)
        for s in added:
            print(f"         + {s}", file=sys.stderr)
        return True
    print(f"[block] 拒绝执行：本次申请会比现有权限多出 {len(added)} 项：", file=sys.stderr)
    for s in added:
        print(f"          + {s}", file=sys.stderr)
    print("        默认策略是「只续期、不扩权」。确认要扩权再加 --allow-add。",
          file=sys.stderr)
    return False


def report_scopes(plan):
    """把 plan 打成人类可读的几行（申请数 / 新增 / 失配），所有人都会看到同一套口径。"""
    print(f"[scope] 策略={plan['policy']}｜本次申请 {len(plan['requested'])} 项"
          f"｜新增 {len(plan['added'])}"
          + (f"｜不再申请 {len(plan['dropped'])}" if plan["dropped"] else ""))
    if plan["added"]:
        for s in plan["added"]:
            print(f"        + {s}")
    if plan["unavailable"]:
        verb = "已自动剔除" if plan["drop_unavailable"] else "仍按原样申请"
        print(f"[warn] 应用侧没列出这 {len(plan['unavailable'])} 项，{verb}：",
              file=sys.stderr)
        for s in plan["unavailable"]:
            print(f"         - {s}", file=sys.stderr)
        if not plan["drop_unavailable"]:
            print("       若登录报 scope 相关错误，改用 --policy minimal 收窄后重试。",
                  file=sys.stderr)
    if plan["missing"]:
        print(f"[warn] 本 skill 需要但当前未授予 {len(plan['missing'])} 项"
              f"（续期不会补，避免扩权）：", file=sys.stderr)
        for s in plan["missing"]:
            print(f"         ! {s}", file=sys.stderr)
        print("       真要补：--policy minimal --allow-add（或去开放平台开通后重授权）",
              file=sys.stderr)
    if plan["lack_on_app"]:
        print(f"[note] 应用侧未开通 {len(plan['lack_on_app'])} 项必需权限，"
              "最小集已自动跳过，相关功能会受限：", file=sys.stderr)
        for s in plan["lack_on_app"]:
            print(f"         · {s}", file=sys.stderr)


# ------------------------------------------------------------------ 发送
def cli_ok(obj, rc):
    """CLI 即使校验失败也可能 rc=0，必须看 JSON 里的 ok/error。"""
    return rc == 0 and isinstance(obj, dict) and obj.get("ok") is not False \
        and not obj.get("error")


def send_card(open_id, card, as_user=False):
    """以 bot 身份发卡片（内容走 stdin，避开 @file 的路径限制）。

    返回 (ok, 摘要)。
    """
    body = json.dumps(card, ensure_ascii=False)
    argv = ["lark-cli", "im", "+messages-send",
            "--user-id", open_id, "--as", "user" if as_user else "bot",
            "--msg-type", "interactive", "--content", "-"]
    rc, obj, raw = run(argv, timeout=45, stdin=body)
    if cli_ok(obj, rc):
        mid = (((obj.get("data") or {}).get("message_id")) or "")
        return True, f"授权卡片已发到飞书（message_id={mid[:12] or 'ok'}）"
    return False, (raw or "")[:300]


def send_text(open_id, text):
    rc, obj, raw = run(["lark-cli", "im", "+messages-send", "--user-id", open_id,
                        "--as", "bot", "--text", text], timeout=45)
    return cli_ok(obj, rc), (raw or "")[:300]


# ------------------------------------------------------------------ 飞书
def feishu(args):
    ok, desc = token_state()
    if ok and not args.force and not args.show_scope:
        print(f"[ok] 无需重新授权（{desc}；refresh 还有效时 CLI 会自动续 access）")
        print("     想验证卡片通路可加 --force")
        return 0

    plan = resolve_scopes(args)
    report_scopes(plan)
    requested = plan["requested"]
    if not requested:
        print("[fail] 算出的申请范围为 0 —— 应用未开通任何必需权限，或 --scope 传空。",
              file=sys.stderr)
        print("       先到开放平台给应用开通 IM 权限，再重跑。", file=sys.stderr)
        return 2
    if args.show_scope:
        print("        （--show-scope：只演示，不会申请，也不会发卡片）")
        return 0
    if not guard_scopes(plan, args.allow_add):
        return 2

    print(f"[info] 当前状态: {desc}")
    argv = ["lark-cli", "auth", "login", "--no-wait", "--json",
            "--scope", " ".join(requested)]
    if args.dry_run:
        print("[dry-run] " + " ".join(argv[:6]) + f" <{len(requested)} 项 scope>")
        return 0
    rc, obj, raw = run(argv, timeout=60)
    if rc != 0 or not isinstance(obj, dict) or not obj.get("verification_url"):
        print(f"[fail] 开启设备流失败: {raw[:300]}", file=sys.stderr)
        return 2
    url = obj["verification_url"]
    code = obj.get("device_code") or ""
    minutes = max(1, int(obj.get("expires_in", 600)) // 60)
    user_code = ""
    m = re.search(r"user_code=([^&]+)", url)
    if m:
        user_code = m.group(1)

    if args.no_send:
        print(f"\n[手动] 打开这个链接确认授权（{minutes} 分钟内有效）：\n{url}\n")
        print(f"完成后运行: python3 scripts/reauth.py feishu --complete {code}")
        return 3

    open_id = args.to or self_open_id()
    if not open_id:
        print("[warn] 取不到本人 open_id，退回手动模式", file=sys.stderr)
        print(url)
        return 3

    note = ("只申请本 skill 必需的最小权限（%d 项），不含其它业务域。" % len(requested)
            if plan["policy"] == "minimal"
            else f"权限范围与你现有完全一致（{len(requested)} 项），**不会新增授权**。")
    card = build_card(url, user_code or "-", minutes, who=args.who,
                      scope_count=len(requested), scope_note=note)
    sent, detail = send_card(open_id, card, as_user=False)
    if sent:
        print(f"[ok] {detail}")
    else:
        print(f"[warn] bot 发卡片失败：{detail[:160]}", file=sys.stderr)
        print("       退化为文本消息重试…", file=sys.stderr)
        ok2, d2 = send_text(open_id, f"【分身】需要重新授权，{minutes} 分钟内点开确认：{url}")
        if ok2:
            print("[ok] 已改为文本消息发送（点链接同样能授权）")
        else:
            print(f"[fail] bot 发消息也被拒：{d2[:160]}", file=sys.stderr)
            print("       常见原因：bot 未开通与你单聊 / 应用可用范围不含你。", file=sys.stderr)
            print("       退回手动模式，链接如下：", file=sys.stderr)
            print(url)
            print(f"       完成后: python3 scripts/reauth.py feishu --complete {code}")
            return 3

    resume = f"python3 scripts/reauth.py feishu --complete {code}"
    if args.detach:
        print(f"[wait] 去飞书点「一键续期授权」，点完执行：\n       {resume}")
        if args.json:
            print(json.dumps({"sent": True, "device_code": code,
                              "verification_url": url, "resume": resume},
                             ensure_ascii=False))
        return 3

    print(f"[wait] 已发到你的飞书，等待点击（至多 {minutes} 分钟）…")
    return complete(code, timeout=minutes * 60 + 60, quiet=args.json)


def complete(code, timeout=660, quiet=False):
    before = set(granted_scopes())
    rc, obj, raw = run(["lark-cli", "auth", "login", "--device-code", code, "--json"],
                       timeout=timeout)
    ok, desc = token_state()
    if ok:
        after = set(granted_scopes())
        new = sorted(after - before) if before else []
        print(f"[ok] 重新授权完成（{desc}）")
        print(f"[scope] 授予 {len(after)} 项"
              + (f"，其中**新增** {len(new)} 项：" if new else "，无新增权限"))
        for s in new:
            print(f"         + {s}")
        if quiet:
            print(json.dumps({"authorized": True, "scopes": len(after),
                              "added": new}, ensure_ascii=False))
        return 0
    print(f"[fail] 收尾失败 rc={rc}: {raw[:300]}", file=sys.stderr)
    print("       链接可能已过期（10 分钟），重跑: python3 scripts/reauth.py feishu",
          file=sys.stderr)
    return 2


# ------------------------------------------------------------------ 企微 / 钉钉
def wecom(args):
    rc, obj, raw = run(["wecom-cli", "auth", "show"], timeout=25)
    text = raw
    if "authorized" in text.lower():
        print("[ok] 企微当前已授权（Bot ID 已配置），无需重新授权")
        print("     凭证若失效只能重配：wecom-cli auth init --manual")
        return 0
    print("[scope] 该平台无 OAuth scope 概念：权限在管理后台勾选，本脚本不申请任何权限。")
    print("[info] 企微不是 OAuth，没有可点的授权卡片。")
    print("       它是「机器人凭证」（Bot ID + Secret），扫码只是获取凭证的便捷方式。\n")
    print("       免扫码路径（管理员直接粘贴凭证）：")
    print("         wecom-cli auth init --manual")
    print("       或多账号/远程：把二维码图发给能扫码的人")
    print("         wecom-cli auth init --noninteractive --output-qrcode /tmp/wecom-qr.png")
    return 4


def dingtalk(args):
    rc, obj, raw = run(["dws", "auth", "status"], timeout=25)
    if isinstance(obj, dict) and obj.get("authenticated"):
        print("[ok] 钉钉已登录（access token 由 dws 自动刷新），无需重新授权")
        print("     若确实失效（如换机/撤销授权）：dws auth login --device")
        return 0
    print("[scope] 该平台无 OAuth scope 概念：权限在钉钉开放平台的应用权限点里勾选，"
          "本脚本不申请任何权限。")
    print("[info] 钉钉没有「已登录的 bot」可用，卡片发不出去（先有鸡还是先有蛋）。")
    print("       但**不需要扫码**，用设备流拿短链 + 验证码，贴到任意聊天里给自己：\n")
    print("         dws auth login --device      # 输出 user_code + 短链，浏览器打开输码即可")
    print("\n       已有 token 的直接导入（最快）：")
    print("         dws auth login --token <token>")
    print("       换机迁移：dws auth export / dws auth import")
    return 4


def main():
    ap = argparse.ArgumentParser(description="不扫码的重新授权（飞书授权卡片）")
    ap.add_argument("platform", nargs="?", default="feishu",
                    choices=["feishu", "wecom", "dingtalk"])
    ap.add_argument("--force", action="store_true", help="当前有效也走一遍（验证通路）")
    ap.add_argument("--detach", action="store_true", help="发完即返回，不阻塞等待")
    ap.add_argument("--complete", metavar="DEVICE_CODE", help="用户点完后收尾")
    ap.add_argument("--no-send", action="store_true", help="不发卡片，只打印链接")
    ap.add_argument("--to", default="", help="改发到指定 open_id（默认本人）")
    ap.add_argument("--who", default="分身", help="卡片标题里的自称")
    ap.add_argument("--scope", default="",
                    help="显式指定要申请的 scope（空格/逗号分隔）；"
                         "默认=沿用当前已授予集合，不动范围")
    ap.add_argument("--policy", choices=["keep", "minimal"], default="keep",
                    help="keep(默认)=沿用现有授权，仅续期；"
                         "minimal=只用本 skill 必需的最小集（首次安装/主动收窄）")
    ap.add_argument("--add", default="",
                    help="在默认集合上追加 scope（需 --allow-add 才放行）")
    ap.add_argument("--allow-add", action="store_true",
                    help="允许本次申请比现有更多的权限（默认拒绝，防误扩权）")
    ap.add_argument("--show-scope", action="store_true",
                    help="只打印本次会申请哪些权限，不申请也不发卡片")
    ap.add_argument("--dry-run", action="store_true", help="只打印命令，不实际执行")
    ap.add_argument("--json", action="store_true", help="附加机器可读输出")
    args = ap.parse_args()

    if args.complete:
        return complete(args.complete, timeout=660, quiet=args.json)
    if args.platform == "wecom":
        return wecom(args)
    if args.platform == "dingtalk":
        return dingtalk(args)
    return feishu(args)


if __name__ == "__main__":
    sys.exit(main())
