#!/usr/bin/env python3
"""
Rollback Script — generic-skill lane 回滚工具

支持依据 receipt / backup / rollback pointer 恢复目标文件。

当前支持范围:
- generic-skill lane 的文档类修改回滚
- 基于 backup 文件恢复
- 基于 receipt 追溯回滚信息

用法:
    python rollback.py --receipt <receipt-path>
    python rollback.py --backup <backup-path> --target <target-path>
    python rollback.py --run-id <run-id> --candidate-id <candidate-id>
    python rollback.py --help
"""

import argparse
import json
import os
import shutil
import sys
from pathlib import Path
from datetime import datetime

_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from lib.common import read_json, write_json


# 默认根目录
DEFAULT_ROOT = Path(os.environ.get("OPENCLAW_ROOT", os.path.expanduser("~/.openclaw"))) / "shared-context/intel/auto-improvement/generic-skill"


def find_receipt(run_id: str, candidate_id: str) -> Path:
    """根据 run_id 和 candidate_id 查找 receipt"""
    receipts_dir = DEFAULT_ROOT / "receipts"
    pattern = f"{run_id}-{candidate_id}-gate.json"
    
    for receipt_file in receipts_dir.glob(pattern):
        return receipt_file
    
    # 尝试模糊匹配
    for receipt_file in receipts_dir.glob(f"*{run_id}*{candidate_id}*.json"):
        return receipt_file
    
    raise FileNotFoundError(f"Receipt not found: {run_id}-{candidate_id}")


def rollback_from_receipt(receipt_path: Path, dry_run: bool = False) -> dict:
    """
    从 receipt 执行回滚
    
    参数:
        receipt_path: receipt JSON 文件路径
        dry_run: 是否仅模拟不实际执行
    
    返回:
        回滚结果字典
    """
    receipt = read_json(receipt_path)
    
    # 检查是否需要回滚
    decision = receipt.get("decision", "")
    if decision == "keep":
        return {
            "status": "skipped",
            "reason": "Receipt decision is 'keep', no rollback needed",
            "receipt_path": str(receipt_path)
        }
    
    # 查找 execution artifact
    execution_path = receipt.get("truth_anchor", {}).get("execution_path")
    if not execution_path:
        # 尝试从 receipt 中推断
        run_id = receipt.get("run_id")
        candidate_id = receipt.get("candidate_id")
        if run_id and candidate_id:
            executions_dir = DEFAULT_ROOT / "executions"
            for exec_file in executions_dir.glob(f"{run_id}-{candidate_id}.json"):
                execution_path = str(exec_file)
                break
    
    if not execution_path:
        return {
            "status": "error",
            "reason": "Cannot find execution artifact",
            "receipt_path": str(receipt_path)
        }
    
    execution = read_json(Path(execution_path))
    
    # 获取 rollback pointer from result
    result = execution.get("result", {})
    rollback_pointer = result.get("rollback_pointer", {})
    backup_path = rollback_pointer.get("backup_path")

    if not backup_path:
        return {
            "status": "error",
            "reason": "No backup information found in execution artifact",
            "execution_path": execution_path
        }

    # 获取目标路径 (truth_anchor is a string path, not a dict)
    target_path = rollback_pointer.get("target_path")
    if not target_path:
        return {
            "status": "error",
            "reason": "No target path found in execution artifact",
            "execution_path": execution_path
        }
    
    # 执行回滚
    backup_file = Path(backup_path)
    target_file = Path(target_path)
    
    if not backup_file.exists():
        return {
            "status": "error",
            "reason": f"Backup file not found: {backup_path}",
            "backup_path": backup_path
        }
    
    result = {
        "status": "dry_run" if dry_run else "success",
        "action": "rollback",
        "target_path": str(target_file),
        "backup_path": str(backup_file),
        "rollback_pointer": rollback_pointer,
        "receipt_path": str(receipt_path),
        "dry_run": dry_run
    }
    
    if not dry_run:
        # 创建目标文件的备份（回滚前的状态）
        pre_rollback_backup = target_file.parent / f"{target_file.name}.pre-rollback-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        if target_file.exists():
            shutil.copy2(target_file, pre_rollback_backup)
            result["pre_rollback_backup"] = str(pre_rollback_backup)
        
        # 恢复 backup
        shutil.copy2(backup_file, target_file)
        result["restored_from"] = str(backup_file)
    
    return result


def rollback_from_backup(backup_path: str, target_path: str, dry_run: bool = False) -> dict:
    """
    直接从 backup 文件回滚
    
    参数:
        backup_path: backup 文件路径
        target_path: 目标文件路径
        dry_run: 是否仅模拟不实际执行
    
    返回:
        回滚结果字典
    """
    backup_file = Path(backup_path)
    target_file = Path(target_path)
    
    if not backup_file.exists():
        return {
            "status": "error",
            "reason": f"Backup file not found: {backup_path}"
        }
    
    result = {
        "status": "dry_run" if dry_run else "success",
        "action": "rollback",
        "target_path": str(target_file),
        "backup_path": str(backup_file),
        "dry_run": dry_run
    }
    
    if not dry_run:
        # 创建目标文件的备份（回滚前的状态）
        pre_rollback_backup = target_file.parent / f"{target_file.name}.pre-rollback-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        if target_file.exists():
            shutil.copy2(target_file, pre_rollback_backup)
            result["pre_rollback_backup"] = str(pre_rollback_backup)
        
        # 恢复 backup
        shutil.copy2(backup_file, target_file)
        result["restored_from"] = str(backup_file)
    
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Rollback tool for generic-skill lane",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 从 receipt 回滚
  python rollback.py --receipt /path/to/receipt.json
  
  # 从 backup 文件回滚
  python rollback.py --backup /path/to/backup.bak --target /path/to/target.md
  
  # 从 run-id 和 candidate-id 回滚
  python rollback.py --run-id run-20260401-143022 --candidate-id cand-001
  
  # 模拟回滚（不实际执行）
  python rollback.py --receipt /path/to/receipt.json --dry-run

支持范围:
  - generic-skill lane 的文档类修改回滚
  - 基于 backup 文件恢复
  - 基于 receipt 追溯回滚信息
  
注意:
  - 回滚前会自动创建当前状态的备份（pre-rollback-*.bak）
  - 仅支持有 backup 信息的 execution
  - 默认 dry-run 模式，需要实际执行请去掉 --dry-run 标志
        """
    )
    
    parser.add_argument(
        "--receipt",
        type=Path,
        help="Receipt JSON file path"
    )
    
    parser.add_argument(
        "--backup",
        type=str,
        help="Backup file path"
    )
    
    parser.add_argument(
        "--target",
        type=str,
        help="Target file path (required with --backup)"
    )
    
    parser.add_argument(
        "--run-id",
        type=str,
        help="Run ID (alternative to --receipt)"
    )
    
    parser.add_argument(
        "--candidate-id",
        type=str,
        help="Candidate ID (required with --run-id)"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=True,  # 默认 dry-run 模式
        help="Simulate rollback without actual file operations (default: True)"
    )
    
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually execute the rollback (override --dry-run)"
    )
    
    args = parser.parse_args()
    
    # 处理 execute 标志
    if args.execute:
        args.dry_run = False
    
    # 验证参数组合
    if args.receipt:
        result = rollback_from_receipt(args.receipt, dry_run=args.dry_run)
    elif args.backup and args.target:
        result = rollback_from_backup(args.backup, args.target, dry_run=args.dry_run)
    elif args.run_id and args.candidate_id:
        try:
            receipt_path = find_receipt(args.run_id, args.candidate_id)
            result = rollback_from_receipt(receipt_path, dry_run=args.dry_run)
        except FileNotFoundError as e:
            result = {"status": "error", "reason": str(e)}
    else:
        parser.print_help()
        sys.exit(1)
    
    # 输出结果
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 错误时退出码非零
    if result.get("status") == "error":
        sys.exit(1)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
