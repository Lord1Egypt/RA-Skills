#!/usr/bin/env python3
import subprocess
import json
import sys

def main():
    result = {"status": "unknown", "tool_used": "", "raw_output": ""}
    try:
        # 优先使用 ss 命令
        p = subprocess.run(["ss", "-lntup"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=10)
        if p.returncode == 0:
            result.update({"status": "success", "tool_used": "ss", "raw_output": p.stdout.strip()})
        else:
            # 退回使用 netstat
            p2 = subprocess.run(["netstat", "-an"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=10)
            result.update({"status": "success", "tool_used": "netstat", "raw_output": p2.stdout.strip()})
    except Exception as e:
        result.update({"status": "error", "raw_output": f"端口扫描执行异常: {str(e)}"})

    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()