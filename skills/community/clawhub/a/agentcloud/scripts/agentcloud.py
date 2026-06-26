#!/usr/bin/env python3
"""
AgentCloud CLI — 一键接入 AI Agent 云存储

用法:
  python3 agentcloud.py register [--name NAME]
  python3 agentcloud.py upload FILE [--key KEY]
  python3 agentcloud.py download FILE_ID -o OUTPUT [--key KEY]
  python3 agentcloud.py list [--key KEY]
  python3 agentcloud.py share FILE_ID [--expires SECONDS] [--key KEY]
  python3 agentcloud.py me [--key KEY]
  python3 agentcloud.py upgrade [--key KEY]
  python3 agentcloud.py plans

不传 --key 时，会从环境变量 AGENTCLOUD_KEY 读取。
首次注册会保存配置到 ~/.agentcloud/config.json。
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("❌ 请先安装 requests: pip install requests")
    sys.exit(1)

BASE_URL = "https://api.traceclaw.cn/api/v1"
SITE_URL = "https://agentcloud.traceclaw.cn"
CONFIG_DIR = Path.home() / ".agentcloud"
CONFIG_FILE = CONFIG_DIR / "config.json"

PLANS = [
    {"name": "免费体验",  "storage_mb": 30,   "price": 0,   "id": "free"},
    {"name": "VIP",       "storage_mb": 600,  "price": 6,   "id": "vip"},
    {"name": "SVIP",      "storage_mb": 3200, "price": 30,  "id": "svip"},
    {"name": "SVIP+",     "storage_mb": 15000,"price": 128, "id": "svip_plus"},
]


def _load_key(args_key):
    """从参数、环境变量或配置文件获取 API Key"""
    if args_key:
        return args_key
    env_key = os.environ.get("AGENTCLOUD_KEY")
    if env_key:
        return env_key
    if CONFIG_FILE.exists():
        config = json.loads(CONFIG_FILE.read_text())
        key = config.get("api_key")
        if key:
            return key
    return None


def _save_config(data):
    """保存注册信息到配置文件"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if CONFIG_FILE.exists():
        config = json.loads(CONFIG_FILE.read_text())
        config.update(data)
    else:
        config = data
    CONFIG_FILE.write_text(json.dumps(config, indent=2, ensure_ascii=False))
    print(f"📁 配置已保存: {CONFIG_FILE}")


def _headers(api_key):
    return {"X-Agent-Key": api_key}


def _get_agent_info(api_key):
    """获取 agent 详细信息"""
    r = requests.get(f"{BASE_URL}/agents/me", headers=_headers(api_key), timeout=15)
    r.raise_for_status()
    return r.json()


def _check_agent_status(api_key):
    """检查 agent 状态，返回 (ok, message)"""
    try:
        info = _get_agent_info(api_key)
    except Exception as e:
        return False, f"查询 agent 状态失败: {e}"

    plan = info.get("plan", "free")
    sub_end = info.get("subscription_end")
    total = info.get("total_storage_mb", 30)
    used = info.get("used_storage_mb", 0)

    # 检查是否过期（有subscription_end但已过期）
    if sub_end:
        # 如果后端有 is_expired 字段直接用
        if info.get("is_expired"):
            return False, (
                f"⏰ 您的会员已过期！\n"
                f"   请运行 `agentcloud upgrade` 续费\n"
                f"   web端: {SITE_URL}/dashboard"
            )

    # 检查免费用户是否有余额
    if plan == "free":
        if used >= total:
            return False, (
                f"⚠️ 免费额度已用尽 ({total}MB)！\n"
                f"   请运行 `agentcloud upgrade` 扩容\n"
                f"   web端: {SITE_URL}/dashboard"
            )

    return True, info


def cmd_register(args):
    """注册新 Agent"""
    name = args.name or f"agent-{os.getpid()}"
    print(f"🔐 注册 Agent: {name}")
    try:
        r = requests.post(f"{BASE_URL}/agents/register/open", json={"name": name}, timeout=15)
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 注册失败: {e}")
        return

    _save_config({
        "agent_id": data["agent_id"],
        "api_key": data["api_key"],
        "name": data["name"],
    })

    print(f"\n✅ 注册成功!")
    print(f"   Agent ID: {data['agent_id']}")
    print(f"   API Key:  {data['api_key']}  ⚠️ 请妥善保存")
    print(f"   名称:     {data['name']}")
    print(f"\n💡 设置环境变量方便后续使用:")
    print(f"   export AGENTCLOUD_KEY={data['api_key']}")

    # 测试连通性
    print(f"\n📡 测试连接...")
    try:
        info = _get_agent_info(data["api_key"])
        plan_name = info.get("plan_name", "免费体验版")
        total = info.get("total_storage_mb", 30)
        used = info.get("used_storage_mb", 0)
        print(f"   套餐: {plan_name} ({used:.1f}MB / {total}MB)")
        sub_end = info.get("subscription_end")
        if sub_end:
            print(f"   会员到期: {sub_end[:19] if isinstance(sub_end, str) else sub_end}")
        else:
            print(f"   免费额度: {total}MB")
            print(f"\n💡 需要更多空间? 运行 `agentcloud upgrade` 查看套餐")
    except Exception as e:
        print(f"   ⚠️ 连接测试失败: {e}")


def cmd_upload(args):
    """上传文件"""
    api_key = _load_key(args.key)
    if not api_key:
        print("❌ 未设置 API Key。请先运行 register 或设置 AGENTCLOUD_KEY")
        return

    # 先检查 agent 状态
    ok, status = _check_agent_status(api_key)
    if not ok:
        print(f"❌ {status}")
        return

    filepath = args.file
    if not os.path.exists(filepath):
        print(f"❌ 文件不存在: {filepath}")
        return

    filename = os.path.basename(filepath)
    filesize = os.path.getsize(filepath)
    print(f"📤 上传: {filename} ({_fmt_size(filesize)})")

    try:
        with open(filepath, "rb") as f:
            r = requests.post(
                f"{BASE_URL}/files/upload",
                files={"file": (filename, f)},
                headers=_headers(api_key),
                timeout=120
            )
        r.raise_for_status()
        data = r.json()
        print(f"✅ 上传成功!")
        print(f"   File ID: {data['file_id']}")
        print(f"   大小:    {_fmt_size(data.get('file_size', filesize))}")
        print(f"\n💡 分享给其他 Agent:")
        print(f"   python3 agentcloud.py share {data['file_id']}")

        # 检查剩余空间
        try:
            info = _get_agent_info(api_key)
            used = info.get("used_storage_mb", 0)
            total = info.get("total_storage_mb", 30)
            if used >= total * 0.8 and info.get("plan") == "free":
                print(f"\n⚠️  剩余空间不足 {(total - used):.1f}MB, 推荐升级:")
                print(f"   运行 `agentcloud upgrade` 查看套餐")
        except Exception:
            pass

    except requests.exceptions.RequestException as e:
        print(f"❌ 上传失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            # 检查是否是 quota 或过期错误
            try:
                err_data = e.response.json()
                detail = err_data.get("detail", "") or str(err_data)
                print(f"   原因: {detail[:300]}")
                if "quota" in detail.lower() or "expired" in detail.lower() or "upgrade" in detail.lower():
                    print(f"\n💡 需要升级套餐: 运行 `agentcloud upgrade`")
            except Exception:
                print(f"   HTTP {e.response.status_code}: {e.response.text[:200]}")


def cmd_download(args):
    """下载文件"""
    api_key = _load_key(args.key)
    if not api_key:
        print("❌ 未设置 API Key。请先运行 register 或设置 AGENTCLOUD_KEY")
        return

    ok, status = _check_agent_status(api_key)
    if not ok:
        print(f"❌ {status}")
        return

    file_id = args.file_id
    output = args.output or f"download_{file_id}"

    print(f"📥 下载: {file_id}")
    try:
        r = requests.get(
            f"{BASE_URL}/files/download/{file_id}",
            headers=_headers(api_key),
            timeout=120,
            stream=True
        )
        r.raise_for_status()

        # 尝试获取文件名
        content_disp = r.headers.get("Content-Disposition", "")
        if "filename=" in content_disp:
            output = content_disp.split("filename=")[-1].strip('"').strip("'")

        with open(output, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

        size = os.path.getsize(output)
        print(f"✅ 下载成功!")
        print(f"   文件: {output}")
        print(f"   大小: {_fmt_size(size)}")
    except requests.exceptions.RequestException as e:
        print(f"❌ 下载失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"   HTTP {e.response.status_code}")


def cmd_list(args):
    """列出文件"""
    api_key = _load_key(args.key)
    if not api_key:
        print("❌ 未设置 API Key。请先运行 register 或设置 AGENTCLOUD_KEY")
        return

    ok, status = _check_agent_status(api_key)
    if not ok:
        print(f"❌ {status}")
        return

    print("📂 文件列表")
    try:
        r = requests.get(f"{BASE_URL}/files", headers=_headers(api_key), timeout=15)
        r.raise_for_status()
        files = r.json()
    except requests.exceptions.RequestException as e:
        print(f"❌ 查询失败: {e}")
        return

    if not files:
        print("   (空)")
        return

    print(f"   共 {len(files)} 个文件:")
    for f in files:
        created = f.get("created_at", "")[:19] if f.get("created_at") else "?"
        print(f"   [{f['file_id'][:8]}...] {f['filename']}  "
              f"{_fmt_size(f['file_size'])}  {created}")


def cmd_share(args):
    """创建分享链接"""
    api_key = _load_key(args.key)
    if not api_key:
        print("❌ 未设置 API Key。请先运行 register 或设置 AGENTCLOUD_KEY")
        return

    ok, status = _check_agent_status(api_key)
    if not ok:
        print(f"❌ {status}")
        return

    file_id = args.file_id
    expires = args.expires or 86400  # 默认24小时

    print(f"🔗 创建分享链接: {file_id} (有效期 {expires} 秒)")
    try:
        r = requests.post(
            f"{BASE_URL}/files/{file_id}/share",
            json={"expires_in": expires},
            headers=_headers(api_key),
            timeout=15
        )
        r.raise_for_status()
        data = r.json()
        share_url = f"{BASE_URL}/files/shared/{data['share_token']}"
        print(f"✅ 分享链接:")
        print(f"   {share_url}")
        print(f"\n💡 其他 Agent 可通过此链接直接下载，无需认证")
    except requests.exceptions.RequestException as e:
        print(f"❌ 分享失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            try:
                print(f"   服务器返回: {e.response.json()}")
            except Exception:
                print(f"   服务器返回: {e.response.text[:200]}")


def cmd_me(args):
    """查看 Agent 信息"""
    api_key = _load_key(args.key)
    if not api_key:
        print("❌ 未设置 API Key。请先运行 register 或设置 AGENTCLOUD_KEY")
        return

    try:
        info = _get_agent_info(api_key)
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        return

    plan_name = info.get("plan_name", "免费体验版")
    total = info.get("total_storage_mb", 30)
    used = info.get("used_storage_mb", 0)
    used_mb = info.get("total_storage_mb", 30) - info.get("total_storage_mb", 30) + used  # 确保数字

    print(f"📊 Agent 信息")
    print(f"   ID:        {info.get('agent_id', '?')}")
    print(f"   名称:      {info.get('name', '?')}")

    # 显示套餐
    sub_end = info.get("subscription_end")
    if sub_end:
        end_str = sub_end[:19] if isinstance(sub_end, str) else str(sub_end)
        print(f"   套餐:      {plan_name}")
        print(f"   会员到期:  {end_str}")
        # 如果过期
        if info.get("is_expired"):
            print(f"   状态:      ❌ 已过期，请运行 `agentcloud upgrade` 续费")
    else:
        print(f"   套餐:      {plan_name} (免费 {total}MB)")

    # 存储信息 + 进度条
    pct = (used / total * 100) if total > 0 else 0
    bar_len = 20
    filled = int(bar_len * pct / 100)
    bar = "█" * filled + "░" * (bar_len - filled)
    print(f"   存储:      {bar} {used:.1f}MB / {total}MB ({pct:.0f}%)")

    # 过期或额度用完提示
    if info.get("is_expired"):
        print(f"\n🔴 会员已过期，文件可能无法下载！")
        print(f"   运行 `agentcloud upgrade` 续费")
    elif info.get("plan") == "free" and used >= total * 0.9:
        print(f"\n⚠️  免费额度即将用尽！")
        print(f"   运行 `agentcloud upgrade` 扩容")
    else:
        print(f"\n💡 需要更多空间? 运行 `agentcloud upgrade` 查看套餐")


def cmd_upgrade(args):
    """查看并选择套餐"""
    api_key = _load_key(args.key)
    if not api_key:
        print("❌ 未设置 API Key。请先运行 register 或设置 AGENTCLOUD_KEY")
        return

    # 获取当前 agent 信息
    try:
        info = _get_agent_info(api_key)
    except Exception as e:
        print(f"⚠️ 无法获取当前信息: {e}")
        info = {}

    agent_id = info.get("agent_id", "?")
    current_plan = info.get("plan_name", "免费体验版")

    print(f"{'='*50}")
    print(f"🚀 AgentCloud 套餐升级")
    print(f"{'='*50}")
    print(f"   Agent: {agent_id}")
    print(f"   当前:  {current_plan}")
    print()

    # 显示套餐列表
    print(f"   {'#':<4} {'套餐':<12} {'存储空间':<14} {'价格':<10}")
    print(f"   {'-'*40}")
    for i, plan in enumerate(PLANS):
        if plan["storage_mb"] >= 1024:
            storage_str = f"{plan['storage_mb']/1024:.1f}GB"
        else:
            storage_str = f"{plan['storage_mb']}MB"
        price_str = f"¥{plan['price']}" if plan["price"] > 0 else "免费"
        marker = " ◀ 当前" if plan["name"] == current_plan else ""
        print(f"   {i+1:<4} {plan['name']:<12} {storage_str:<14} {price_str:<10}{marker}")

    print()
    print(f"   输入套餐编号购买，或输入 0 取消")
    print(f"   (微信/支付宝扫码支付)")

    # 这里不能用 input，因为是在 agent 环境
    # 改为打印购买链接的方式
    print()
    print("🗳️  请通过以下方式购买:")
    print(f"   1. 访问网页端: {SITE_URL}/dashboard")
    print(f"   2. 选择套餐并扫码支付")
    print()
    print(f"   或直接复制链接:")
    print(f"   go to agentcloud upgrade amount=30 plan=vip")
    print()
    print("💡 您的 Agent 升级后将自动获得对应的存储空间")


def cmd_plans(args):
    """列出所有套餐"""
    print(f"{'='*50}")
    print(f"📋 AgentCloud 套餐一览")
    print(f"{'='*50}")
    print()
    print(f"   {'套餐':<12} {'存储空间':<14} {'价格':<10}")
    print(f"   {'-'*40}")
    for plan in PLANS:
        if plan["storage_mb"] >= 1024:
            storage_str = f"{plan['storage_mb']/1024:.1f}GB"
        else:
            storage_str = f"{plan['storage_mb']}MB"
        price_str = f"¥{plan['price']}" if plan["price"] > 0 else "免费"
        print(f"   {plan['name']:<12} {storage_str:<14} {price_str:<10}")

    print()
    print(f"💡 注册即享免费 {PLANS[0]['storage_mb']}MB 额度")
    print(f"   支付后即刻生效，无需人工审核")
    print(f"   官网: {SITE_URL}")


def _fmt_size(size_bytes):
    """格式化文件大小"""
    if size_bytes < 1024:
        return f"{size_bytes}B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f}KB"
    else:
        return f"{size_bytes / 1024 / 1024:.1f}MB"


def main():
    parser = argparse.ArgumentParser(description="AgentCloud CLI - AI Agent 云存储")
    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # register
    p_register = subparsers.add_parser("register", help="注册新 Agent")
    p_register.add_argument("--name", default=None, help="Agent 名称")

    # upload
    p_upload = subparsers.add_parser("upload", help="上传文件")
    p_upload.add_argument("file", help="文件路径")
    p_upload.add_argument("--key", default=None, help="API Key")

    # download
    p_download = subparsers.add_parser("download", help="下载文件")
    p_download.add_argument("file_id", help="文件 ID")
    p_download.add_argument("-o", "--output", default=None, help="输出路径")
    p_download.add_argument("--key", default=None, help="API Key")

    # list
    p_list = subparsers.add_parser("list", help="列出文件")
    p_list.add_argument("--key", default=None, help="API Key")

    # share
    p_share = subparsers.add_parser("share", help="创建分享链接")
    p_share.add_argument("file_id", help="文件 ID")
    p_share.add_argument("--expires", type=int, default=86400, help="有效期（秒，默认86400）")
    p_share.add_argument("--key", default=None, help="API Key")

    # me
    p_me = subparsers.add_parser("me", help="查看 Agent 信息")
    p_me.add_argument("--key", default=None, help="API Key")

    # upgrade
    p_upgrade = subparsers.add_parser("upgrade", help="查看套餐并升级")
    p_upgrade.add_argument("--key", default=None, help="API Key")

    # plans
    p_plans = subparsers.add_parser("plans", help="显示所有套餐")
    p_plans.add_argument("--key", default=None, help="API Key")

    args = parser.parse_args()

    if args.command == "register":
        cmd_register(args)
    elif args.command == "upload":
        cmd_upload(args)
    elif args.command == "download":
        cmd_download(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "share":
        cmd_share(args)
    elif args.command == "me":
        cmd_me(args)
    elif args.command == "upgrade":
        cmd_upgrade(args)
    elif args.command == "plans":
        cmd_plans(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
