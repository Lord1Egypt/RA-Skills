#!/usr/bin/env python3
"""
dingtalk-feishu-sync-schedule 配置初始化脚本

配置读取优先级：
  钉钉配置：~/.dingtalk/config.json → ~/.openclaw/openclaw.json → 用户输入
  飞书配置：~/.openclaw/openclaw.json（仅读取，缺失提示用户）

用户输入 unionid 方式：
  - 直接输入 unionid → 直接写入配置
  - 输入手机号 → 调用钉钉 API 获取 unionid 后写入
"""
import os
import sys
import json
import requests

OPENCLAW_CONFIG = os.path.expanduser("~/.openclaw/openclaw.json")
DINGTALK_CONFIG = os.path.expanduser("~/.dingtalk/config.json")
FEISHU_CONFIG = os.path.expanduser("~/.feishu/config.json")


def load_openclaw():
    if os.path.exists(OPENCLAW_CONFIG):
        with open(OPENCLAW_CONFIG, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def load_dingtalk_config():
    if os.path.exists(DINGTALK_CONFIG):
        with open(DINGTALK_CONFIG, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_dingtalk_config(config):
    os.makedirs(os.path.dirname(DINGTALK_CONFIG), exist_ok=True)
    with open(DINGTALK_CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_dingtalk_token():
    """获取钉钉 access_token"""
    cfg = load_dingtalk_config()
    resp = requests.post(
        'https://api.dingtalk.com/v1.0/oauth2/accessToken',
        json={'appKey': cfg['app_key'], 'appSecret': cfg['app_secret']},
        timeout=10
    )
    return resp.json().get('accessToken')


def fetch_unionid_by_mobile(mobile):
    """通过手机号获取 unionid"""
    token = get_dingtalk_token()
    if not token:
        print("❌ 获取钉钉 access_token 失败")
        return None

    # Step1: 通过手机号获取 userid
    resp = requests.post(
        f'https://oapi.dingtalk.com/topapi/v2/user/getbymobile?access_token={token}',
        json={'mobile': mobile},
        timeout=10
    )
    data = resp.json()
    if data.get('errcode') != 0:
        print(f"❌ 手机号获取 userid 失败: {data.get('errmsg')}")
        return None

    userid = data.get('result', {}).get('userid')
    if not userid:
        print("❌ 未找到对应用户")
        return None

    # Step2: 通过 userid 获取 unionid
    resp = requests.post(
        f'https://oapi.dingtalk.com/topapi/v2/user/get?access_token={token}',
        json={'language': 'zh_CN', 'userid': userid},
        timeout=10
    )
    data = resp.json()
    unionid = data.get('result', {}).get('unionid')
    if not unionid:
        print(f"❌ 获取 unionid 失败: {data.get('errmsg')}")
        return None

    return unionid


def prompt_userid_input():
    """引导用户输入 unionid 或手机号"""
    print()
    print("📋 请提供钉钉 user_id（unionid）：")
    print("   方式1: 直接输入 unionid（格式如 xxxxxxxxXXXXXXXXXXXXXXX）")
    print("   方式2: 输入手机号（11位数字，如 13800138000）")
    print()
    val = input("   请输入: ").strip()

    if not val:
        print("❌ 输入不能为空")
        return None

    # 判断是手机号还是 unionid
    if val.isdigit() and len(val) == 11:
        print(f"   📱 检测为手机号，正在通过钉钉 API 获取 unionid...")
        unionid = fetch_unionid_by_mobile(val)
        if unionid:
            print(f"   ✅ unionid 获取成功: {unionid}")
        return unionid
    else:
        # 认为是 unionid，直接写入
        print(f"   ✅ 直接写入 unionid: {val}")
        return val


def init_dingtalk():
    """初始化钉钉配置"""
    config = load_dingtalk_config()
    updated = False

    # 缺失 app_key/app_secret：尝试从 openclaw.json 补充
    missing_cred = [k for k in ('app_key', 'app_secret') if not config.get(k)]
    if missing_cred:
        print(f"⚠️  钉钉凭证缺失: {', '.join(missing_cred)}，尝试从 OpenClaw 配置读取...")
        openclaw = load_openclaw()
        dd = openclaw.get('channels', {}).get('ddingtalk', {})
        openclaw_key = dd.get('clientId')
        openclaw_secret = dd.get('clientSecret')

        if not config.get('app_key') and openclaw_key:
            config['app_key'] = openclaw_key
            updated = True
            print(f"   ✅ app_key 已补入")

        if not config.get('app_secret') and openclaw_secret:
            config['app_secret'] = openclaw_secret
            updated = True
            print(f"   ✅ app_secret 已补入")

        if updated:
            save_dingtalk_config(config)
            print(f"   已保存: {DINGTALK_CONFIG}")

    # 仍缺失 app_key/app_secret：引导用户输入
    still_missing_cred = [k for k in ('app_key', 'app_secret') if not config.get(k)]
    if still_missing_cred:
        print(f"⚠️  仍缺失: {', '.join(still_missing_cred)}，请手动补充到: {DINGTALK_CONFIG}")
    else:
        print(f"✅ app_key / app_secret 已就绪")

    # 缺失 user_id：引导用户输入（支持手机号或 unionid）
    if not config.get('user_id'):
        print(f"⚠️  user_id（unionid）未配置")
        unionid = prompt_userid_input()
        if unionid:
            config['user_id'] = unionid
            save_dingtalk_config(config)
            updated = True
            print(f"   ✅ user_id 已写入配置文件")
        else:
            print(f"   ❌ user_id 获取/写入失败，请重试")
    else:
        print(f"✅ user_id 已配置: {config.get('user_id')}")

    return config, updated


def load_feishu_from_openclaw():
    """从 OpenClaw.json 读取飞书配置"""
    openclaw = load_openclaw()
    feishu = openclaw.get('channels', {}).get('feishu', {})
    accounts = feishu.get('accounts', {})
    default = accounts.get('default', {})
    app_id = default.get('appId')
    app_secret = default.get('appSecret')
    open_id = default.get('open_id')

    if not app_id or not app_secret:
        return None

    existing = {}
    if os.path.exists(FEISHU_CONFIG):
        with open(FEISHU_CONFIG, 'r', encoding='utf-8') as f:
            existing = json.load(f)

    config = {
        'app_id': app_id,
        'app_secret': app_secret,
        'user_open_id': open_id or existing.get('user_open_id'),
        'calendar_id': existing.get('calendar_id'),
        'access_token': existing.get('access_token'),
        'refresh_token': existing.get('refresh_token'),
        'expires_in': existing.get('expires_in'),
        'refresh_expires_in': existing.get('refresh_expires_in'),
    }
    config = {k: v for k, v in config.items() if v is not None}

    os.makedirs(os.path.dirname(FEISHU_CONFIG), exist_ok=True)
    with open(FEISHU_CONFIG, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    return config


def main():
    print("🔧 dingtalk-feishu-sync-schedule 配置初始化\n")

    # ── 钉钉配置 ─────────────────────────────────────────
    print("─── 钉钉配置 ───")
    dingtalk_cfg, dingtalk_updated = init_dingtalk()

    # ── 飞书配置 ─────────────────────────────────────────
    print()
    print("─── 飞书配置 ───")
    feishu_cfg = load_feishu_from_openclaw()

    if feishu_cfg:
        print(f"✅ 飞书配置已写入: {FEISHU_CONFIG}")
        print(f"   app_id: {feishu_cfg.get('app_id')}")

        feishu_missing = []
        if not feishu_cfg.get('user_open_id'):
            feishu_missing.append('user_open_id')
        if not feishu_cfg.get('calendar_id'):
            feishu_missing.append('calendar_id')
        if not feishu_cfg.get('refresh_token'):
            feishu_missing.append('refresh_token（需授权）')

        if feishu_missing:
            print(f"   ⚠️  缺失: {', '.join(feishu_missing)}")
    else:
        print(f"⚠️  无法从 OpenClaw 配置读取飞书凭证，请检查 ~/.feishu/config.json")

    # ── 汇总 ──────────────────────────────────────────────
    print()
    print("─── 状态汇总 ───")
    all_ok = True

    if not dingtalk_cfg.get('user_id'):
        print("❌ 钉钉 user_id 未完成")
        all_ok = False
    else:
        print("✅ 钉钉配置完整")

    if feishu_cfg:
        if not feishu_cfg.get('refresh_token'):
            print("⚠️  飞书 refresh_token 缺失，需授权（参考 SKILL.md Step 3）")
            all_ok = False
        if not feishu_cfg.get('calendar_id'):
            print("⚠️  飞书 calendar_id 缺失，Agent 自动获取")
    else:
        print("⚠️  飞书配置异常")

    print()
    if all_ok:
        print("🎉 所有配置已完成，可运行 sync_week_ahead.py 验证")
    else:
        print("💡 参考 SKILL.md 继续补充缺失项")


if __name__ == '__main__':
    main()
