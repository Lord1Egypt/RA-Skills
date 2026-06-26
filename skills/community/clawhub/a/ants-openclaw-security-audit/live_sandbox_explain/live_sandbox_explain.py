#!/usr/bin/env python3
import subprocess
import json

def main():
    result = {"status": "unknown", "explain_output": ""}
    
    try:
        # 执行官方诊断命令
        p = subprocess.run(
            ["openclaw", "sandbox", "explain"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=15
        )
        
        if p.returncode == 0:
            result["status"] = "success"
            result["explain_output"] = p.stdout.strip()
        else:
            result["status"] = "error"
            result["explain_output"] = f"命令执行失败 (退出码 {p.returncode}):\n{p.stdout.strip()}"
            
    except FileNotFoundError:
        result["status"] = "error"
        result["explain_output"] = "未找到 openclaw 命令，请确认系统已安装。"
    except subprocess.TimeoutExpired:
        result["status"] = "error"
        result["explain_output"] = "执行 openclaw sandbox explain 超时。"
    except Exception as e:
        result["status"] = "error"
        result["explain_output"] = str(e)

    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()