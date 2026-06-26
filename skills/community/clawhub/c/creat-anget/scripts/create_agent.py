#!/usr/bin/env python3
"""
Agent Creator Script

辅助脚本，用于使用指定配置生成新的子 Agent。
此脚本由 agent-creator 技能调用，根据用户描述以编程方式创建 Agent。

用法:
    python create_agent.py --task "你的任务描述" --label "Agent 名称"
    
选项:
    --task        Agent 的任务/角色描述 (必填)
    --label       Agent 的易读名称 (必填)
    --runtime     运行时类型: subagent 或 acp (默认: subagent)
    --mode        模式: session 或 run (默认: session)
    --model       模型别名 (例如: qwen) (默认: None, 使用系统默认)
    --thinking    启用思考: on 或 off (默认: off)
    --thread      绑定到线程: true 或 false (默认: false)
    --cwd         工作目录 (默认: 继承父目录)
"""

import argparse
import json
import sys
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="生成一个新的子 Agent")
    parser.add_argument("--task", required=True, help="Agent 的任务/角色描述")
    parser.add_argument("--label", required=True, help="Agent 的易读名称")
    parser.add_argument("--runtime", choices=["subagent", "acp"], default="subagent",
                        help="运行时类型 (默认: subagent)")
    parser.add_argument("--mode", choices=["session", "run"], default="session",
                        help="模式: session 或 run (默认: session)")
    parser.add_argument("--model", default=None, help="模型别名 (默认: 系统默认)")
    parser.add_argument("--thinking", choices=["on", "off"], default="off",
                        help="启用思考模式 (默认: off)")
    parser.add_argument("--thread", action="store_true", default=False,
                        help="绑定到线程 (用于 Discord/ACP)")
    parser.add_argument("--cwd", default=None, help="工作目录 (默认: 继承)")
    parser.add_argument("--agent-id", default=None, help="ACP 运行时的 Agent ID")
    parser.add_argument("--output", default=None, help="会话信息的输出文件")
    return parser.parse_args()


def build_spawn_params(args):
    """构建 sessions_spawn 调用的参数。"""
    params = {
        "task": args.task,
        "label": args.label,
        "runtime": args.runtime,
        "mode": args.mode,
        "thinking": args.thinking,
        "thread": args.thread,
    }
    
    if args.model:
        params["model"] = args.model
    
    if args.cwd:
        params["cwd"] = args.cwd
    
    if args.runtime == "acp" and args.agent_id:
        params["agentId"] = args.agent_id
    
    # 清理 None 值
    params = {k: v for k, v in params.items() if v is not None}
    
    return params


def main():
    args = parse_args()
    params = build_spawn_params(args)
    
    # 输出 JSON 格式的参数供调用 Agent 使用
    output = {
        "action": "spawn_agent",
        "parameters": params,
        "summary": f"正在创建 Agent '{args.label}'，runtime={args.runtime}, mode={args.mode}"
    }
    
    print(json.dumps(output, indent=2, ensure_ascii=False))
    
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\n会话信息已写入: {output_path}", file=sys.stderr)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
