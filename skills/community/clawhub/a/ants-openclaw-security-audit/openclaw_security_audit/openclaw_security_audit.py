#!/usr/bin/env python3
import subprocess
import json
import argparse
import sys

def main():
    # 移除了 fix 选项，仅保留安全的只读扫描模式
    parser = argparse.ArgumentParser(description="OpenClaw 内置安全审计技能 (只读模式)")
    parser.add_argument("--mode", choices=["standard", "deep"], default="standard", 
                        help="指定审计模式: standard 或 deep")
    args = parser.parse_args()

    # 组装底层命令
    cmd = ["openclaw", "security", "audit"]
    if args.mode == "deep":
        cmd.append("--deep")

    result = {
        "status": "unknown",
        "mode": args.mode,
        "audit_output": ""
    }

    try:
        # 执行命令
        p = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=30
        )
        
        # openclaw audit 命令如果发现安全问题，通常会返回非 0 的退出码
        if p.returncode == 0:
            result["status"] = "success"
        else:
            result["status"] = "issues_found"
            
        result["audit_output"] = p.stdout.strip() if p.stdout else "无控制台输出"
        result["return_code"] = p.returncode

    except FileNotFoundError:
        result["status"] = "error"
        result["audit_output"] = "未找到 openclaw 命令，请确认目标服务器是否正确安装了 OpenClaw，且已加入系统 PATH。"
    except subprocess.TimeoutExpired:
        result["status"] = "timeout"
        result["audit_output"] = f"执行 OpenClaw {args.mode} 模式审计超时 (30秒)。"
    except Exception as e:
        result["status"] = "error"
        result["audit_output"] = f"执行异常: {str(e)}"

    # 打印标准 JSON 结果
    print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()