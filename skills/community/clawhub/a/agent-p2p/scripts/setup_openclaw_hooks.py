#!/usr/bin/env python3
"""
OpenClaw Hooks 配置脚本

功能：
1. 检查 OpenClaw 是否已配置 hooks
2. 如未配置，安全地添加配置（自动备份）
3. 生成/获取 hooks token
4. 测试 /hooks/wake 是否可用
5. 测试成功则自动唤起 OpenClaw

用法：
    python3 setup_openclaw_hooks.py
"""

import json
import os
import sys
import subprocess
import secrets
from pathlib import Path


def get_openclaw_config_path():
    """获取 OpenClaw 配置文件路径"""
    return Path.home() / ".openclaw" / "openclaw.json"


def backup_config(config_path):
    """备份原配置文件"""
    backup_path = Path(str(config_path) + ".backup." + str(int(os.time())))
    if config_path.exists():
        backup_path.write_text(config_path.read_text())
        print(f"✅ 已备份原配置: {backup_path}")
        return True
    return False


def load_config(config_path):
    """加载 OpenClaw 配置"""
    if not config_path.exists():
        print(f"❌ 找不到 OpenClaw 配置文件: {config_path}")
        print("请先安装并启动 OpenClaw")
        return None
    
    try:
        return json.loads(config_path.read_text())
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件格式错误: {e}")
        return None


def save_config(config_path, config):
    """保存 OpenClaw 配置"""
    config_path.write_text(json.dumps(config, indent=2))
    print(f"✅ 配置已保存: {config_path}")


def check_hooks_config(config):
    """检查是否已配置 hooks"""
    hooks = config.get("hooks", {})
    return hooks.get("enabled") and hooks.get("token")


def generate_hooks_token():
    """生成新的 hooks token"""
    return secrets.token_urlsafe(32)


def setup_hooks_config(config):
    """配置 hooks"""
    if "hooks" not in config:
        config["hooks"] = {}
    
    # 保留现有 token，或生成新的
    existing_token = config["hooks"].get("token")
    token = existing_token if existing_token else generate_hooks_token()
    
    # 检查是否与 gateway.auth.token 冲突
    gateway_auth_token = config.get("gateway", {}).get("auth", {}).get("token")
    if gateway_auth_token and token == gateway_auth_token:
        print("⚠️ 检测到 hooks.token 与 gateway.auth.token 冲突，生成新的 token")
        token = generate_hooks_token()
        # 确保新生成的 token 仍然不同
        while token == gateway_auth_token:
            token = generate_hooks_token()
    
    config["hooks"]["enabled"] = True
    config["hooks"]["path"] = "/hooks"
    config["hooks"]["token"] = token
    
    return token


def get_gateway_url(config):
    """获取 Gateway URL"""
    gateway = config.get("gateway", {})
    port = gateway.get("port", 18789)
    return f"http://127.0.0.1:{port}"


def test_hooks_wake(gateway_url, token):
    """测试 /hooks/wake 是否可用"""
    try:
        import requests
        resp = requests.post(
            f"{gateway_url}/hooks/wake",
            headers={"Authorization": f"Bearer {token}"},
            json={"text": "测试消息"},
            timeout=5
        )
        return resp.status_code == 200
    except Exception as e:
        print(f"⚠️ 测试失败: {e}")
        return False


def restart_openclaw():
    """重启 OpenClaw"""
    print("🔄 重启 OpenClaw...")
    result = subprocess.run(
        ["openclaw", "restart"],
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("✅ OpenClaw 已重启")
        return True
    else:
        print(f"⚠️ 重启失败: {result.stderr}")
        return False


def main():
    print("=" * 60)
    print("OpenClaw Hooks 配置")
    print("=" * 60)
    
    config_path = get_openclaw_config_path()
    
    # 加载配置
    config = load_config(config_path)
    if not config:
        sys.exit(1)
    
    # 检查是否已配置
    if check_hooks_config(config):
        print("\n✅ Hooks 已配置")
        token = config["hooks"]["token"]
        gateway_url = get_gateway_url(config)
        
        # 测试是否可用
        print(f"\n🧪 测试 /hooks/wake ...")
        if test_hooks_wake(gateway_url, token):
            print("✅ 测试通过！Hooks 工作正常")
            
            # 自动唤起 OpenClaw
            print("\n📢 自动唤起 OpenClaw...")
            subprocess.run([
                "curl", "-s", "-X", "POST",
                f"{gateway_url}/hooks/wake",
                "-H", f"Authorization: Bearer {token}",
                "-H", "Content-Type: application/json",
                "-d", '{"text":"OpenClaw Hooks 配置完成！"}'
            ], capture_output=True)
            print("✅ 已发送唤醒消息")
        else:
            print("⚠️ 测试失败，请检查 OpenClaw 是否正常运行")
        
        print(f"\n📝 Hooks Token: {token[:20]}...")
        print(f"🌐 Gateway URL: {gateway_url}")
        return
    
    # 未配置，需要设置
    print("\n⚠️ Hooks 未配置，需要设置")
    
    # 确认
    confirm = input("\n是否自动配置 OpenClaw Hooks? [Y/n]: ").strip().lower()
    if confirm and confirm not in ('y', 'yes'):
        print("已取消")
        return
    
    # 备份原配置
    backup_config(config_path)
    
    # 配置 hooks
    token = setup_hooks_config(config)
    gateway_url = get_gateway_url(config)
    
    # 保存配置
    save_config(config_path, config)
    
    # 重启 OpenClaw
    if not restart_openclaw():
        print("\n⚠️ 请手动重启 OpenClaw: openclaw restart")
        return
    
    # 等待重启完成
    print("\n⏳ 等待 OpenClaw 启动...")
    import time
    time.sleep(3)
    
    # 测试
    print(f"\n🧪 测试 /hooks/wake ...")
    if test_hooks_wake(gateway_url, token):
        print("✅ 测试通过！Hooks 配置成功")
        
        # 自动唤起
        print("\n📢 自动唤起 OpenClaw...")
        subprocess.run([
            "curl", "-s", "-X", "POST",
            f"{gateway_url}/hooks/wake",
            "-H", f"Authorization: Bearer {token}",
            "-H", "Content-Type: application/json",
            "-d", '{"text":"OpenClaw Hooks 配置完成！"}'
        ], capture_output=True)
        print("✅ 已发送唤醒消息")
    else:
        print("⚠️ 测试失败，请检查 OpenClaw 日志")
    
    print(f"\n📝 Hooks Token: {token[:20]}...")
    print(f"🌐 Gateway URL: {gateway_url}")
    print("\n" + "=" * 60)
    print("配置完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()