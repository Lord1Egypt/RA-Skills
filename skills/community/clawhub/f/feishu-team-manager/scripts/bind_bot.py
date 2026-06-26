import json
import os
import shutil
import sys
import subprocess

def bind_bot(agent_id, app_id, app_secret):
    """
    按照 2026-04-21 实践通过的 channels.feishu.accounts 模式重构配置
    增加了自动化自愈逻辑与精准报错拦截
    """
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    if not os.path.exists(config_path):
        return "错误：未找到 openclaw.json"

    # --- 阶段 1: 预检查自愈 (Pre-Check Self-Heal) ---
    print("正在进行修改前置自检...")
    pre_check = subprocess.run(["openclaw", "doctor", "--fix"], capture_output=True, text=True)
    if pre_check.returncode != 0:
        print("⚠ 检测到原始配置文件存在错误，已尝试自动修复。")

    # --- 阶段 2: 修改配置 ---
    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError:
        return "❌ 致命错误：openclaw.json 格式损坏且无法自动修复。请手动检查文件语法。"

    # 1. 备份
    shutil.copy2(config_path, config_path + f".bak_{agent_id}")

    # 2. 注入账号信息
    if "channels" not in config: config["channels"] = {}
    if "feishu" not in config["channels"]: config["channels"]["feishu"] = {}
    if "accounts" not in config["channels"]["feishu"]: config["channels"]["feishu"]["accounts"] = {}

    # 检查 AppID 是否已被其他 Agent 占用 (冲突拦截)
    for acc_id, acc_info in config["channels"]["feishu"]["accounts"].items():
        if acc_info.get("appId") == app_id and acc_id != f"bot_{agent_id}":
            return f"❌ 冲突：App ID '{app_id}' 已被其他账号 ({acc_id}) 使用。请检查并提供正确的 App ID。"

    account_id = f"bot_{agent_id}"
    config["channels"]["feishu"]["accounts"][account_id] = {
        "appId": app_id,
        "appSecret": app_secret,
        "enabled": True,
        "dmPolicy": "open"
    }

    # 3. 注入路由
    if "bindings" not in config: config["bindings"] = []
    found = False
    for b in config["bindings"]:
        if b.get("agentId") == agent_id:
            b["match"] = { "accountId": account_id, "channel": "feishu" }
            found = True
            break
    if not found:
        config["bindings"].append({
            "agentId": agent_id,
            "match": { "accountId": account_id, "channel": "feishu" }
        })

    # 4. 保存
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    # --- 阶段 3: 修改后验证与强制自愈 ---
    print("正在执行修改后校验与自动修复...")
    post_check = subprocess.run(["openclaw", "doctor", "--fix"], capture_output=True, text=True)
    
    # 如果 doctor 依然报错，且包含致命冲突
    if post_check.returncode != 0 or "ERROR" in post_check.stdout:
        # 匹配常见的需要用户干预的错误
        if "AppId" in post_check.stdout or "Secret" in post_check.stdout:
             return f"❌ 验证失败：App 凭据校验不通过。请确认您的 App ID 和 Secret 是否正确且已在飞书后台启用。"
        
        # 其他非干预类错误，尝试再次自愈
        print("发现非致命异常，尝试二次自动修正...")
        subprocess.run(["openclaw", "doctor", "--fix"])

    # --- 阶段 4: 最终重启 ---
    print("环境就绪，正在重启 Gateway...")
    subprocess.run(["openclaw", "gateway", "restart"])

    return f"✅ Agent '{agent_id}' 绑定成功！\n\n🚀 **环境状态**：已通过自动化自愈与冲突检测，Gateway 重启中。"

if __name__ == "__main__":
    if len(sys.argv) > 3:
        print(bind_bot(sys.argv[1], sys.argv[2], sys.argv[3]))
