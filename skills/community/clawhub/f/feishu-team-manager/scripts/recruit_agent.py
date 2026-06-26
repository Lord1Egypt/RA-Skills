import sys
import os
import subprocess

def recruit(agent_name, role_template):
    print(f"正在招聘 Agent: {agent_name}...")
    # 1. 调用 CLI 添加 Agent
    try:
        subprocess.run(["openclaw", "agents", "add", agent_name], check=True)
    except Exception as e:
        return f"添加 Agent 失败: {str(e)}"

    # 2. 初始化配置 (这里简化演示，实际会读取 assets/templates)
    agent_path = f"agents/{agent_name}"
    # 兼容处理：检查是否存在于 /root/.openclaw/agents/
    full_agent_path = os.path.expanduser(f"~/.openclaw/agents/{agent_name}")
    if os.path.exists(full_agent_path):
        with open(f"{full_agent_path}/IDENTITY.md", "w") as f:
            f.write(f"# IDENTITY\nname: {agent_name}\nrole: {role_template}")
            
    return f"Agent {agent_name} 招聘成功！\n\n📢 **HR 提示**：Agent 已在后台入职，但尚未在飞书上线。请提供该 Agent 对应的飞书机器人 App ID 和 App Secret 进行绑定。"

if __name__ == "__main__":
    if len(sys.argv) > 2:
        print(recruit(sys.argv[1], sys.argv[2]))
