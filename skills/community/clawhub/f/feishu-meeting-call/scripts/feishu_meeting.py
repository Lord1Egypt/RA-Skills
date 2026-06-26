#!/usr/bin/env python3
"""
飞书紧急提醒 — 发送加急消息 / 电话加急

工作流程:
  1. 通过 Bot 发送文本消息给用户
  2. 将消息标记为加急（应用内加急 或 电话加急）

环境变量:
  FEISHU_APP_ID        - 飞书应用 App ID
  FEISHU_APP_SECRET    - 飞书应用 App Secret
  FEISHU_USER_OPEN_ID  - 被提醒用户的 open_id
"""

import argparse
import json
import os
import ssl
import sys
import time
import urllib.error
import urllib.request

# ============================================================
# 飞书 API 基础地址
# ============================================================
BASE_URL = "https://open.feishu.cn/open-apis"


# ============================================================
# 工具函数
# ============================================================

def _script_dir():
    """返回本脚本所在目录的绝对路径"""
    return os.path.dirname(os.path.abspath(__file__))


def _base_dir():
    """返回技能根目录（scripts/ 的上一层）"""
    return os.path.dirname(_script_dir())


def _find_env_file():
    """
    按优先级查找 .feishu.env 配置文件，返回第一个存在的路径或 None。

    优先级从高到低：
      1. FEISHU_ENV_FILE 环境变量（显式指定，最高优先）
      2. {技能根目录}/.feishu.env（workspace 持久化，容器安全）
      3. ~/.feishu.env（传统路径，本地开发用）
    """
    candidates = [
        os.environ.get("FEISHU_ENV_FILE", ""),
        os.path.join(_base_dir(), ".feishu.env"),
        os.path.expanduser("~/.feishu.env"),
    ]
    for path in candidates:
        if path and os.path.isfile(path):
            return path
    return None


def _parse_env_file(path):
    """
    解析 .env 文件，返回 {key: value} 字典。

    支持格式：
      KEY=VALUE
      export KEY="VALUE"
      KEY='VALUE'
    """
    result = {}
    if not path or not os.path.isfile(path):
        return result
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export "):]
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key:
                result[key] = value
    return result


def _load_env_file():
    """
    从配置文件加载环境变量（仅补充缺失项，不覆盖已有值）。

    自动按优先级查找多个路径，解决：
      - 后台子进程未继承 shell 环境变量
      - 容器重建后 ~ 丢失的问题
    """
    env_path = _find_env_file()
    if not env_path:
        return
    for key, value in _parse_env_file(env_path).items():
        if not os.environ.get(key):
            os.environ[key] = value


def _ssl_context():
    """获取 SSL 上下文，沙箱环境降级处理"""
    try:
        ctx = ssl.create_default_context()
        return ctx
    except Exception:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx


def api_request(method, path, data=None, token=None, max_retries=2):
    """
    发送飞书 API 请求

    参数:
        method:      HTTP 方法 (GET / POST / PATCH)
        path:        API 路径 (不含 BASE_URL)
        data:        请求体 (dict)
        token:       tenant_access_token
        max_retries: 网络错误最大重试次数

    返回:
        dict — 响应 JSON
    """
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    ctx = _ssl_context()

    for attempt in range(max_retries + 1):
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8")
            try:
                return json.loads(error_body)
            except Exception:
                print(f"[错误] API 请求失败 ({e.code}): {error_body}",
                      file=sys.stderr)
                sys.exit(1)
        except Exception as e:
            if attempt < max_retries:
                wait = 2 ** attempt
                print(f"[重试] 网络错误，{wait} 秒后重试 "
                      f"({attempt + 1}/{max_retries})...", file=sys.stderr)
                time.sleep(wait)
            else:
                print(f"[错误] 请求失败: {e}", file=sys.stderr)
                sys.exit(1)


# ============================================================
# 飞书 API 封装
# ============================================================

def get_tenant_token(app_id, app_secret):
    """获取 tenant_access_token"""
    result = api_request("POST", "/auth/v3/tenant_access_token/internal", {
        "app_id": app_id,
        "app_secret": app_secret,
    })
    if result.get("code") != 0:
        print(f"[错误] 获取 token 失败: {result.get('msg', '未知错误')}",
              file=sys.stderr)
        sys.exit(1)
    return result["tenant_access_token"]


# ── 消息相关 ────────────────────────────────────────────

def send_text_message(token, user_open_id, text):
    """
    发送纯文本消息

    返回 message_id
    """
    content = json.dumps({"text": text}, ensure_ascii=False)

    data = {
        "receive_id": user_open_id,
        "msg_type": "text",
        "content": content,
    }

    result = api_request(
        "POST",
        "/im/v1/messages?receive_id_type=open_id",
        data,
        token,
    )

    if result.get("code") != 0:
        code = result.get("code")
        msg = result.get("msg", "未知错误")
        print(f"[警告] 发送消息失败 (code={code}): {msg}", file=sys.stderr)
        _print_message_error_hint(code)
        return None

    return result.get("data", {}).get("message_id", "")


def _print_message_error_hint(code):
    """打印发送消息常见错误的排查提示"""
    hints = {
        230001: "参数错误，请检查 open_id 是否正确",
        230002: "机器人不在会话中。请先让用户在飞书中搜索并打开该机器人",
        230006: ("应用未启用机器人能力。请前往飞书开放平台 > 应用详情 > "
                 "应用能力 > 添加「机器人」能力"),
        230013: ("用户不在应用可用范围内。请前往飞书开放平台 > 应用详情 > "
                 "版本管理与发布 > 可用范围，将用户添加进去"),
    }
    hint = hints.get(code)
    if hint:
        print(f"  -> {hint}", file=sys.stderr)


def mark_urgent(token, message_id, user_open_id, urgent_type="app"):
    """
    将消息标记为加急

    参数:
        urgent_type: 加急类型
            "app"   — 应用内加急（免费，飞书 App 内强推送）
            "phone" — 电话加急（消耗企业配额，真正打电话到手机）
            "sms"   — 短信加急（消耗企业配额，发短信）
    """
    type_map = {
        "app": "urgent_app",
        "phone": "urgent_phone",
        "sms": "urgent_sms",
    }
    endpoint = type_map.get(urgent_type, "urgent_app")
    type_label = {"app": "应用内加急", "phone": "电话加急", "sms": "短信加急"}

    data = {
        "user_id_list": [user_open_id],
    }

    result = api_request(
        "PATCH",
        f"/im/v1/messages/{message_id}/{endpoint}?user_id_type=open_id",
        data,
        token,
    )

    if result.get("code") != 0:
        code = result.get("code")
        msg = result.get("msg", "未知错误")
        label = type_label.get(urgent_type, "加急")
        print(f"[警告] {label}失败 (code={code}): {msg}", file=sys.stderr)

        perm_map = {
            "phone": "im:message.urgent:phone",
            "sms": "im:message.urgent:sms",
        }
        hints = {
            230002: "机器人不在会话中，请先让用户打开该机器人对话",
            230006: "应用未启用机器人能力，请在应用能力中添加「机器人」",
            230012: "只能加急机器人自己发送的消息",
            230013: "用户不在应用可用范围内，请在版本管理中添加用户",
            230023: "用户未读加急消息超过 200 条，请先处理部分加急消息",
            230024: "加急配额已用完，请联系企业管理员充值或等待恢复",
            230027: f"权限不足，请确认应用已开启 {perm_map.get(urgent_type, '')} 权限",
            230052: "无权加急，请检查群聊是否限制了加急权限",
        }
        hint = hints.get(code)
        if hint:
            print(f"  -> {hint}", file=sys.stderr)
        return False

    return True


# ── 用户查找 ────────────────────────────────────────────

def _normalize_phone(phone):
    """
    规范化手机号: 自动补 +86 前缀

    支持的输入格式:
      13800138000    → +8613800138000
      8613800138000  → +8613800138000
      +8613800138000 → +8613800138000（不变）
      +1xxxxxxxxxx   → +1xxxxxxxxxx（非中国号码不变）
    """
    phone = phone.strip()
    if phone.startswith("+"):
        return phone
    # 去掉可能的前导 86（无 + 号的情况）
    if phone.startswith("86") and len(phone) == 13:
        return f"+{phone}"
    # 纯 11 位手机号，默认中国大陆
    if len(phone) == 11 and phone[0] == "1":
        return f"+86{phone}"
    # 其他情况原样加 +
    return f"+{phone}" if not phone.startswith("+") else phone


def lookup_user_id(token, email=None, phone=None):
    """
    通过邮箱或手机号查找用户 open_id

    需要应用开启 contact:user.id:readonly 权限
    """
    data = {}
    if email:
        data["emails"] = [email]
    if phone:
        phone = _normalize_phone(phone)
        print(f"   手机号: {phone}")
        data["mobiles"] = [phone]
    if not data:
        print("[错误] 请提供邮箱 (--email) 或手机号 (--phone)", file=sys.stderr)
        sys.exit(1)

    result = api_request(
        "POST",
        "/contact/v3/users/batch_get_id?user_id_type=open_id",
        data,
        token,
    )

    if result.get("code") != 0:
        code = result.get("code")
        msg = result.get("msg", "未知错误")
        print(f"[错误] 查找用户失败 (code={code}): {msg}", file=sys.stderr)
        if code in (100002, 100003):
            print("  -> 请确认应用已开启 contact:user.id:readonly 权限",
                  file=sys.stderr)
        sys.exit(1)

    user_list = result.get("data", {}).get("user_list", [])
    if not user_list:
        print("[错误] 未找到匹配的用户", file=sys.stderr)
        sys.exit(1)

    for user in user_list:
        uid = user.get("user_id", "")
        if uid:
            return uid

    print("[错误] 查询返回了结果但未包含有效的 user_id", file=sys.stderr)
    sys.exit(1)


# ============================================================
# 命令行入口
# ============================================================

def cmd_notify(args, token):
    """发送加急消息"""
    user_id = args.user_id or os.environ.get("FEISHU_USER_OPEN_ID", "")
    if not user_id:
        print("[错误] 请提供用户 open_id", file=sys.stderr)
        sys.exit(1)

    text = args.message
    urgent_type = "phone" if args.phone_call else "app"
    urgent_label = "电话加急" if args.phone_call else "应用内加急"

    print(f"💬 正在发送加急消息...")
    print(f"   内容: {text}")
    print(f"   加急方式: {urgent_label}")
    print()

    # 发送文本消息
    message_id = send_text_message(token, user_id, f"📢 {text}")
    if not message_id:
        print("[错误] 消息发送失败", file=sys.stderr)
        sys.exit(1)
    print(f"✅ 消息已发送")

    # 标记加急
    urgent_ok = mark_urgent(token, message_id, user_id, urgent_type)
    if urgent_ok:
        if args.phone_call:
            print(f"✅ 电话加急已发起！正在拨打用户手机")
        else:
            print(f"✅ 已标记加急！用户将收到强推送通知")
    else:
        if args.phone_call:
            print(f"⚠️  电话加急失败，尝试应用内加急...")
            urgent_ok = mark_urgent(token, message_id, user_id, "app")
            if urgent_ok:
                print(f"✅ 应用内加急成功（电话加急不可用）")
            else:
                print(f"⚠️  加急失败，但普通消息已发送")
        else:
            print(f"⚠️  加急失败，但普通消息已发送")


def cmd_save_config(args):
    """保存配置到 .feishu.env 文件（幂等：已有 key 更新，无则追加）"""
    # 确定保存路径
    if args.path:
        save_path = args.path
    else:
        save_path = os.path.join(_base_dir(), ".feishu.env")

    # 收集要写入的 kv 对
    updates = {}
    if args.app_id is not None:
        updates["FEISHU_APP_ID"] = args.app_id
    if args.app_secret is not None:
        updates["FEISHU_APP_SECRET"] = args.app_secret
    if args.user_id is not None:
        updates["FEISHU_USER_OPEN_ID"] = args.user_id

    if not updates:
        print("[错误] 请至少提供一个配置项（--app-id / --app-secret / --user-id）",
              file=sys.stderr)
        sys.exit(1)

    # 读取已有内容
    existing_lines = []
    if os.path.isfile(save_path):
        with open(save_path, "r", encoding="utf-8") as f:
            existing_lines = f.readlines()

    # 幂等更新：逐行检查，已有 key 则替换，记录已处理的 key
    updated_keys = set()
    new_lines = []
    for line in existing_lines:
        stripped = line.strip()
        # 检查是否匹配要更新的 key
        matched_key = None
        for key in updates:
            prefixes = [f"export {key}=", f"{key}="]
            for prefix in prefixes:
                if stripped.startswith(prefix):
                    matched_key = key
                    break
            if matched_key:
                break
        if matched_key:
            new_lines.append(f'export {matched_key}="{updates[matched_key]}"\n')
            updated_keys.add(matched_key)
        else:
            new_lines.append(line)

    # 追加未匹配到的 key
    for key, value in updates.items():
        if key not in updated_keys:
            new_lines.append(f'export {key}="{value}"\n')

    # 确保父目录存在
    parent = os.path.dirname(save_path)
    if parent:
        os.makedirs(parent, exist_ok=True)

    # 写入文件
    with open(save_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

    # 设置文件权限 600（仅 owner 可读写，保护密钥）
    try:
        os.chmod(save_path, 0o600)
    except OSError:
        pass  # Windows 等平台可能不支持

    print(f"✅ 配置已保存到 {save_path}")
    for key in updates:
        print(f"   {key} = (已设置)")


def cmd_lookup(args, token):
    """查找用户 open_id"""
    print("🔍 正在查找用户...")

    user_id = lookup_user_id(token, email=args.email, phone=args.phone)

    print(f"\n✅ 找到用户")
    print(f"   open_id: {user_id}")
    print(f"\n💡 将此 open_id 设置为环境变量即可使用提醒功能:")
    print(f'   export FEISHU_USER_OPEN_ID="{user_id}"')


def main():
    parser = argparse.ArgumentParser(
        description="飞书紧急提醒 — 发送加急消息 / 电话加急",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 保存飞书凭证（跨平台、幂等）
  python3 feishu_meeting.py save-config --app-id "cli_xxx" --app-secret "xxx"
  python3 feishu_meeting.py save-config --user-id "ou_xxx"

  # 发送加急消息（应用内加急）
  python3 feishu_meeting.py notify --message "小龙虾提醒你：该干活了"

  # 电话加急（真正打电话到手机！）
  python3 feishu_meeting.py notify --message "紧急！线上故障" --phone-call

  # 查找用户 open_id
  python3 feishu_meeting.py lookup --phone "13800138000"
  python3 feishu_meeting.py lookup --email "user@company.com"
        """,
    )
    subparsers = parser.add_subparsers(dest="command", help="操作命令")

    # ── notify: 发送加急消息 ──────────────────────────────
    noti_p = subparsers.add_parser(
        "notify", help="发送加急消息（支持应用内加急和电话加急）",
    )
    noti_p.add_argument("--message", "-m", required=True,
                        help="消息内容")
    noti_p.add_argument("--user-id", "-u",
                        help="用户 open_id（默认从 FEISHU_USER_OPEN_ID 读取）")
    noti_p.add_argument("--phone-call", action="store_true",
                        help="使用电话加急（真正拨打手机，消耗企业配额）")

    # ── lookup: 查找用户 ──────────────────────────────────
    look_p = subparsers.add_parser(
        "lookup", help="通过邮箱/手机号查找用户 open_id",
    )
    look_p.add_argument("--email", "-e", help="用户邮箱")
    look_p.add_argument("--phone", "-p",
                        help="用户手机号（自动补 +86，如 13800138000）")

    # ── save-config: 保存配置 ─────────────────────────────
    save_p = subparsers.add_parser(
        "save-config", help="保存飞书凭证到配置文件（跨平台、幂等）",
    )
    save_p.add_argument("--app-id", help="飞书应用 App ID")
    save_p.add_argument("--app-secret", help="飞书应用 App Secret")
    save_p.add_argument("--user-id", help="用户 open_id")
    save_p.add_argument("--path",
                        help="配置文件保存路径（默认: 技能根目录/.feishu.env）")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # ── save-config 不需要凭证和 token，提前处理 ──────────
    if args.command == "save-config":
        cmd_save_config(args)
        return

    # ── 加载配置文件（补充缺失的环境变量）────────────────
    _load_env_file()

    # ── 读取凭证 ──────────────────────────────────────────
    app_id = os.environ.get("FEISHU_APP_ID", "")
    app_secret = os.environ.get("FEISHU_APP_SECRET", "")

    if not app_id or not app_secret:
        print("[错误] 请设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET",
              file=sys.stderr)
        print("  获取地址: https://open.feishu.cn/app", file=sys.stderr)
        sys.exit(1)

    # ── 获取 token ────────────────────────────────────────
    print("🔐 正在获取访问令牌...")
    token = get_tenant_token(app_id, app_secret)
    print("✅ 令牌获取成功\n")

    # ── 执行命令 ──────────────────────────────────────────
    if args.command == "notify":
        cmd_notify(args, token)
    elif args.command == "lookup":
        cmd_lookup(args, token)


if __name__ == "__main__":
    main()
