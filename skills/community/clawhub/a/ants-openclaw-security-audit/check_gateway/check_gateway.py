#!/usr/bin/env python3
import subprocess
import json
import sys

def main():
    result = {"status": "unknown", "output": ""}
    try:
        p = subprocess.run(
            ["openclaw", "gateway", "status"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=15
        )
        result["status"] = "success" if p.returncode == 0 else "error"
        result["output"] = p.stdout.strip() if p.stdout else "无输出"
    except FileNotFoundError:
        result["status"] = "error"
        result["output"] = "未找到 openclaw 命令，可能未安装或不在系统 PATH 中。"
    except subprocess.TimeoutExpired:
        result["status"] = "timeout"
        result["output"] = "状态检查命令执行超时 (15秒)。"
    except Exception as e:
        result["status"] = "error"
        result["output"] = str(e)

    # 打印标准 JSON 供 AI 智能体捕获
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()