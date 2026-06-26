import os
import json

def check_env():
    results = {
        "config_exists": os.path.exists("openclaw.json"),
        "hr_exists": False,
        "agents_count": 0
    }
    
    # 检查 agents 目录
    if os.path.exists("agents"):
        agents = os.listdir("agents")
        results["agents_count"] = len(agents)
        # 简单逻辑：检查是否有名字包含 hr 的目录或配置文件
        for agent in agents:
            if "hr" in agent.lower():
                results["hr_exists"] = True
                break
                
    return results

if __name__ == "__main__":
    print(json.dumps(check_env(), indent=2))
