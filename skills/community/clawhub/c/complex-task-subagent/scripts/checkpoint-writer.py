#!/usr/bin/env python3
"""
checkpoint-writer.py - 检查点写入工具
用途：在子代理完成任务后，写入检查点文件
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any


class CheckpointWriter:
    """检查点写入器"""

    def __init__(self, checkpoints_dir: str = None):
        """
        初始化检查点写入器

        Args:
            checkpoints_dir: 检查点目录路径
        """
        if checkpoints_dir is None:
            checkpoints_dir = "/root/.openclaw/workspace/complex-task-subagent-experience/checkpoints"

        self.checkpoints_dir = Path(checkpoints_dir)
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)

    def write(
        self,
        checkpoint_file: str,
        phase: str,
        phase_name: str,
        status: str = "completed",
        subagent: str = None,
        output: str = None,
        result: Dict[str, Any] = None,
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        写入检查点文件

        Args:
            checkpoint_file: 检查点文件名（如 "phase1.json"）
            phase: 阶段 ID（如 "phase1"）
            phase_name: 阶段名称
            status: 状态（pending/starting/running/completed/failed）
            subagent: 子代理标签
            output: 输出文件路径
            result: 任务结果
            metadata: 元数据

        Returns:
            检查点文件路径
        """
        checkpoint_path = self.checkpoints_dir / checkpoint_file

        checkpoint = {
            "checkpointId": checkpoint_file.replace(".json", ""),
            "phase": phase,
            "phaseName": phase_name,
            "status": status,
            "completedAt": datetime.utcnow().isoformat() + "Z" if status == "completed" else None,
            "subagent": subagent,
            "output": output,
            "result": result or {},
            "metadata": metadata or {}
        }

        # 写入文件
        with open(checkpoint_path, 'w', encoding='utf-8') as f:
            json.dump(checkpoint, f, indent=2, ensure_ascii=False)

        return str(checkpoint_path)

    def read(self, checkpoint_file: str) -> Dict[str, Any]:
        """
        读取检查点文件

        Args:
            checkpoint_file: 检查点文件名

        Returns:
            检查点数据
        """
        checkpoint_path = self.checkpoints_dir / checkpoint_file

        if not checkpoint_path.exists():
            raise FileNotFoundError(f"检查点文件不存在: {checkpoint_path}")

        with open(checkpoint_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def exists(self, checkpoint_file: str) -> bool:
        """
        检查检查点文件是否存在

        Args:
            checkpoint_file: 检查点文件名

        Returns:
            是否存在
        """
        checkpoint_path = self.checkpoints_dir / checkpoint_file
        return checkpoint_path.exists()

    def list_checkpoints(self) -> list:
        """
        列出所有检查点文件

        Returns:
            检查点文件列表
        """
        if not self.checkpoints_dir.exists():
            return []

        return sorted(self.checkpoints_dir.glob("*.json"))


# 便捷函数
def write_checkpoint(
    checkpoint_file: str,
    phase: str,
    phase_name: str,
    status: str = "completed",
    **kwargs
) -> str:
    """
    便捷函数：写入检查点

    Args:
        checkpoint_file: 检查点文件名
        phase: 阶段 ID
        phase_name: 阶段名称
        status: 状态
        **kwargs: 其他参数

    Returns:
        检查点文件路径
    """
    writer = CheckpointWriter()
    path = writer.write(
        checkpoint_file=checkpoint_file,
        phase=phase,
        phase_name=phase_name,
        status=status,
        **kwargs
    )

    print(f"✅ 检查点已写入: {path}")
    return path


# 命令行接口
def main():
    """命令行接口"""
    if len(sys.argv) < 4:
        print("用法: python3 checkpoint-writer.py <checkpoint-file> <phase> <phase-name> [status]")
        print("")
        print("示例:")
        print("  python3 checkpoint-writer.py phase1.json phase1 '审核现有指南'")
        print("  python3 checkpoint-writer.py phase1.json phase1 '审核现有指南' completed")
        sys.exit(1)

    checkpoint_file = sys.argv[1]
    phase = sys.argv[2]
    phase_name = sys.argv[3]
    status = sys.argv[4] if len(sys.argv) > 4 else "completed"

    write_checkpoint(
        checkpoint_file=checkpoint_file,
        phase=phase,
        phase_name=phase_name,
        status=status
    )


if __name__ == "__main__":
    main()
