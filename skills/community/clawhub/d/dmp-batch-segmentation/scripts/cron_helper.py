#!/usr/bin/env python3
"""
cron_helper.py - cron监控硬约束工具

目的：用脚本级别的"锁文件"机制，强制AI在执行批量任务时必须创建cron监控，
     避免AI因忘记、忽略提示词或session断连导致任务完成后不通知用户。

核心机制：
1. 项目创建后，必须在锁文件中记录 "cron已创建" 标记
2. 脚本每次推进批次前（monitor模式/创建下一批）检查锁文件，没有标记则拒绝执行
3. AI看到拒绝提示后，必须先调用cron工具创建监控，再用 --mark-cron-set 命令写入标记
4. 全部完成后 --cleanup 删除锁文件

锁文件路径：data/plans/<project_id>/cron_monitor.lock
锁文件内容：{"createdAt": "...", "cronName": "...", "status": "active"}
"""

import sys
import json
import argparse
from pathlib import Path
from datetime import datetime


def get_project_dir(project_id: str, base_dir="data/plans") -> Path:
    return Path(base_dir) / project_id


def get_lock_file(project_id: str, base_dir="data/plans") -> Path:
    return get_project_dir(project_id, base_dir) / "cron_monitor.lock"


def ensure_project_dir(project_id: str, base_dir="data/plans") -> Path:
    d = get_project_dir(project_id, base_dir)
    d.mkdir(parents=True, exist_ok=True)
    return d


def check_cron_setup(project_id: str, base_dir="data/plans") -> dict:
    """
    检查cron是否已设置。返回：
    - {"setup": True, ...} 已设置
    - {"setup": False, "instruction": "..."} 未设置，附带AI必须执行的指令
    """
    lock = get_lock_file(project_id, base_dir)
    if lock.exists():
        try:
            data = json.loads(lock.read_text(encoding="utf-8"))
            if data.get("status") == "active":
                return {"setup": True, "data": data}
        except Exception:
            pass
    # 未设置或锁文件损坏
    return {
        "setup": False,
        "blocker": "CRON_NOT_SETUP",
        "message": (
            "🔴 硬拦截：本项目的cron监控任务尚未创建，无法推进批次或查询状态。\n"
            "你必须立即执行以下操作（不要用exec background、不要用openclaw cron add命令行）：\n\n"
            "1. 调用 cron(action='add', job=<下方cron_params>) 创建监控任务\n"
            "2. 创建成功后，运行：python3 scripts/cron_helper.py --project-id " + project_id + " mark-cron-set --cron-name <cron任务名>\n"
            "3. 然后重新执行你之前的命令\n"
        ),
        "cron_action_required": "cron(action='add', job=...)",
        "cron_forbidden": [
            "exec(background=true)+sleep轮询（session断连后无法唤醒AI，已导致故障）",
            "openclaw cron add 命令行（无法设置sessionTarget=current）"
        ]
    }


def mark_cron_setup(project_id: str, cron_name: str, base_dir="data/plans"):
    """标记cron已创建（AI调用完cron工具后必须执行此命令）"""
    ensure_project_dir(project_id, base_dir)
    lock = get_lock_file(project_id, base_dir)
    data = {
        "projectId": project_id,
        "cronName": cron_name,
        "status": "active",
        "createdAt": datetime.now().isoformat()
    }
    lock.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return {
        "status": "ok",
        "message": f"✅ 已记录cron监控状态：{cron_name}",
        "lockFile": str(lock)
    }


def cleanup(project_id: str, base_dir="data/plans"):
    """全部完成后清理锁文件"""
    lock = get_lock_file(project_id, base_dir)
    if lock.exists():
        data = json.loads(lock.read_text(encoding="utf-8"))
        cron_name = data.get("cronName", "")
        lock.unlink()
        return {
            "status": "ok",
            "message": f"✅ 锁文件已清理。请同时调用 cron(action='remove', jobId='{cron_name}') 删除cron监控任务。",
            "cron_cleanup_required": True,
            "cron_name": cron_name
        }
    return {"status": "ok", "message": "锁文件不存在，无需清理"}


def generate_cron_params_combine(project_id: str, audience_ids: list, skill_dir: str) -> dict:
    """生成批量圈包的cron监控任务参数"""
    aid_str = ','.join(str(a) for a in audience_ids)
    return {
        "name": f"DMP圈包监控-{project_id}",
        "schedule": {"kind": "every", "everyMs": 60000},
        "payload": {
            "kind": "agentTurn",
            "message": (
                f"[DMP监控-圈包] 检查项目 {project_id} 状态。"
                f"运行 cd {skill_dir} && python3 scripts/create_combine_batch.py 或 poll_task_status.py 检查audienceIds=[{aid_str}]。"
                f"本批全部audienceStatus=1后：若有下一批则自动创建；若全部完成则运行 "
                f"python3 scripts/cron_helper.py --project-id {project_id} cleanup，然后汇报结果并删除本cron任务。"
                f"若有失败按failureStrategy处理。"
            )
        },
        "sessionTarget": "current",
        "delivery": {"mode": "none"}
    }


def generate_cron_params_idlink(project_id: str, skill_dir: str) -> dict:
    """生成批量打通的cron监控任务参数"""
    return {
        "name": f"DMP打通监控-{project_id}",
        "schedule": {"kind": "every", "everyMs": 60000},
        "payload": {
            "kind": "agentTurn",
            "message": (
                f"[DMP监控-打通] 检查项目 {project_id} 状态。"
                f"运行 cd {skill_dir} && python3 scripts/run_idlink_project.py --mode monitor --project-id {project_id} 推进批次。"
                f"全部完成后运行 python3 scripts/cron_helper.py --project-id {project_id} cleanup，然后汇报结果并删除本cron任务。"
                f"若有失败按failureStrategy处理。"
            )
        },
        "sessionTarget": "current",
        "delivery": {"mode": "none"}
    }


def main():
    parser = argparse.ArgumentParser(description="cron监控硬约束工具")
    parser.add_argument("--project-id", required=True, help="项目ID")
    parser.add_argument("--base-dir", default="data/plans", help="项目数据目录")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # check
    p_chk = sub.add_parser("check", help="检查cron是否已设置（供monitor脚本内部调用）")
    p_chk.add_argument("--json", action="store_true", help="JSON输出")

    # mark-cron-set
    p_mark = sub.add_parser("mark-cron-set", help="标记cron已创建")
    p_mark.add_argument("--cron-name", required=True, help="cron任务名称")

    # cleanup
    sub.add_parser("cleanup", help="任务全部完成后清理锁文件")

    # generate-cron-params（用于AI读取）
    p_gen = sub.add_parser("gen-cron-params", help="生成cron任务参数（JSON）")
    p_gen.add_argument("--type", required=True, choices=["combine", "idlink"], help="技能类型")
    p_gen.add_argument("--audience-ids", default="", help="combine类型：当前批audienceIds，逗号分隔")
    p_gen.add_argument("--skill-dir", required=True, help="技能根目录绝对路径")

    args = parser.parse_args()

    if args.cmd == "check":
        result = check_cron_setup(args.project_id, args.base_dir)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            if result["setup"]:
                print(f"✅ cron已设置: {result['data'].get('cronName','')}")
            else:
                print(result["message"], file=sys.stderr)
                print(json.dumps(result, ensure_ascii=False, indent=2))
                sys.exit(1)

    elif args.cmd == "mark-cron-set":
        result = mark_cron_setup(args.project_id, args.cron_name, args.base_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.cmd == "cleanup":
        result = cleanup(args.project_id, args.base_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.cmd == "gen-cron-params":
        if args.type == "combine":
            aids = [int(x) for x in args.audience_ids.split(",") if x.strip()]
            params = generate_cron_params_combine(args.project_id, aids, args.skill_dir)
        else:
            params = generate_cron_params_idlink(args.project_id, args.skill_dir)
        print(json.dumps(params, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
