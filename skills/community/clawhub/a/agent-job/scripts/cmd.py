#!/usr/bin/env python3
"""
龙虾 Agent Skill - 命令行入口
供 OpenClaw skill system 直接调用
用法: python3 cmd.py <command> [args]
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api import claim, get_earnings, withdraw, load_state, save_state, get_lobster_id
import index as idx

def main():
    args = sys.argv[1:]
    if not args:
        print("用法: lobster <start|stop|claim|earnings|withdraw|poll> [args]")
        sys.exit(1)

    cmd = args[0].lower()
    
    try:
        if cmd == "start":
            print(idx.cmd_start())
        elif cmd == "stop":
            print(idx.cmd_stop())
        elif cmd == "claim":
            print(idx.cmd_claim())
        elif cmd == "earnings":
            print(idx.cmd_earnings())
        elif cmd == "withdraw":
            if len(args) < 2:
                print("❌ 请指定提现金额，如：/lobster withdraw 100")
                sys.exit(1)
            print(idx.cmd_withdraw(args[1]))
        elif cmd == "poll":
            # 轮询脚本
            state = load_state()
            known_ids = set(state.get("in_progress_task_ids", []))
            result = claim()
            in_progress = result.get("in_progress") or []
            current_ids = set(item.get("task_id") for item in in_progress if item.get("task_id"))
            new_tasks = [item for item in in_progress if item.get("task_id") and item.get("task_id") not in known_ids]
            state["in_progress_task_ids"] = list(current_ids)
            from datetime import datetime
            state["last_poll_at"] = datetime.utcnow().isoformat()
            save_state(state)
            if new_tasks:
                for task in new_tasks:
                    print(f"[NEW_TASK] task_id={task.get('task_id')} title={task.get('title')} deadline={task.get('submission_deadline')}", flush=True)
            else:
                print(f"[POLL] no new tasks, in_progress={len(current_ids)}", flush=True)
        else:
            print(f"未知命令：{cmd}")
            print("用法: lobster <start|stop|claim|earnings|withdraw|poll>")
            sys.exit(1)
    except Exception as e:
        print(f"❌ 错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
