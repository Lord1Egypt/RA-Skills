#!/usr/bin/env python3
"""
真实快照和回滚系统 - 基于 git
每次操作自动创建快照，支持完整回滚
"""
import subprocess
import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict

class SnapshotManager:
    """基于 git 的快照管理器"""

    def __init__(self, repo_path=None):
        if repo_path is None:
            repo_path = Path.home() / ".openclaw" / "snapshots"

        self.repo_path = Path(repo_path).expanduser()
        self.repo_path.mkdir(parents=True, exist_ok=True)

        # 初始化 git 仓库
        self._init_git_repo()

    def _init_git_repo(self):
        """初始化 git 仓库"""
        if not (self.repo_path / ".git").exists():
            subprocess.run(
                ["git", "init"],
                cwd=self.repo_path,
                capture_output=True,
                check=True
            )
            # 配置用户
            subprocess.run(
                ["git", "config", "user.email", "claw@openclaw.local"],
                cwd=self.repo_path,
                capture_output=True
            )
            subprocess.run(
                ["git", "config", "user.name", "Claw Audit"],
                cwd=self.repo_path,
                capture_output=True
            )

    def create_snapshot(
        self,
        paths_to_snapshot: List[str],
        operation_id: int = None,
        operation_desc: str = "",
        auto: bool = True
    ) -> Dict:
        """
        创建快照

        Args:
            paths_to_snapshot: 要快照的路径列表
            operation_id: 关联的操作ID
            operation_desc: 操作描述
            auto: 是否为自动快照

        Returns:
            快照信息字典
        """
        timestamp = datetime.now().isoformat()

        # 创建快照元数据
        metadata = {
            "timestamp": timestamp,
            "operation_id": operation_id,
            "operation_desc": operation_desc,
            "auto": auto,
            "paths": paths_to_snapshot
        }

        # 复制文件到快照目录
        snapshot_name = f"snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        snapshot_dir = self.repo_path / snapshot_name
        snapshot_dir.mkdir(exist_ok=True)

        copied_files = []
        for path_str in paths_to_snapshot:
            path = Path(path_str).expanduser()

            if path.exists():
                if path.is_file():
                    # 复制文件，保留目录结构
                    rel_path = path.relative_to(path.anchor)
                    dest_file = snapshot_dir / str(rel_path).lstrip("/")
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    subprocess.run(
                        ["cp", "-p", str(path), str(dest_file)],
                        capture_output=True
                    )
                    copied_files.append(str(path))
                elif path.is_dir():
                    # 递归复制目录
                    dest_dir = snapshot_dir / path.name
                    subprocess.run(
                        ["cp", "-rp", str(path), str(dest_dir)],
                        capture_output=True
                    )
                    copied_files.append(str(path))

        metadata["copied_files"] = copied_files
        metadata["snapshot_name"] = snapshot_name

        # 保存元数据
        metadata_file = snapshot_dir / "metadata.json"
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        # Git 提交
        subprocess.run(["git", "add", "."], cwd=self.repo_path, capture_output=True)

        commit_msg = f"Snapshot: {operation_desc}" if operation_desc else f"Snapshot {snapshot_name}"
        if auto:
            commit_msg = f"[AUTO] {commit_msg}"

        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=self.repo_path,
            capture_output=True
        )

        # 获取 commit hash
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        commit_hash = result.stdout.strip()

        return {
            "id": commit_hash,
            "name": snapshot_name,
            "timestamp": timestamp,
            "description": operation_desc,
            "auto": auto,
            "files": copied_files
        }

    def list_snapshots(self, limit: int = 50) -> List[Dict]:
        """列出所有快照"""
        result = subprocess.run(
            ["git", "log", "--pretty=format:%H|%ai|%s", "-n", str(limit)],
            cwd=self.repo_path,
            capture_output=True,
            text=True,
            check=True
        )

        snapshots = []
        for line in result.stdout.strip().split('\n'):
            if not line:
                continue

            parts = line.split('|', 2)
            if len(parts) == 3:
                commit_hash, timestamp, message = parts

                # 读取元数据
                metadata_file = self.repo_path / ".git" / "info" / f"{commit_hash}.json"
                metadata = {}
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)

                snapshots.append({
                    "id": commit_hash,
                    "timestamp": timestamp,
                    "description": message,
                    "metadata": metadata
                })

        return snapshots

    def restore_snapshot(self, commit_hash: str, paths: List[str] = None) -> Dict:
        """
        回滚到指定快照

        Args:
            commit_hash: git commit hash
            paths: 要恢复的路径列表（None = 全部）

        Returns:
            恢复结果
        """
        try:
            # 获取快照信息
            result = subprocess.run(
                ["git", "show", f"{commit_hash}:."],
                cwd=self.repo_path,
                capture_output=True
            )

            if result.returncode != 0:
                return {
                    "success": False,
                    "error": "快照不存在"
                }

            # 找到对应的快照目录
            snapshots = self.list_snapshots(limit=1000)
            target_snapshot = None
            for snap in snapshots:
                if snap["id"] == commit_hash:
                    target_snapshot = snap
                    break

            if not target_snapshot:
                return {
                    "success": False,
                    "error": "未找到快照"
                }

            # 从快照目录恢复文件
            commit_msg = target_snapshot["description"]
            snapshot_name = None

            # 从提交信息中提取快照名称
            for f in self.repo_path.iterdir():
                if f.is_dir() and f.name.startswith("snapshot_"):
                    metadata_file = f / "metadata.json"
                    if metadata_file.exists():
                        with open(metadata_file, 'r') as mf:
                            metadata = json.load(mf)
                            # 验证时间戳匹配
                            if metadata["timestamp"] in commit_msg:
                                snapshot_name = f.name
                                break

            if not snapshot_name:
                return {
                    "success": False,
                    "error": "无法定位快照目录"
                }

            snapshot_dir = self.repo_path / snapshot_name

            # 恢复文件 - 递归查找所有文件
            restored_files = []
            
            def find_and_restore_files(source_dir, base_path=None):
                """递归查找并恢复文件"""
                for item in source_dir.iterdir():
                    if item.name == "metadata.json":
                        continue
                    
                    if item.is_file():
                        # 重建原始路径
                        rel_path = item.relative_to(snapshot_dir)
                        # 尝试匹配到原始位置
                        parts = rel_path.parts
                        # 跳过根路径部分，找到 home 用户目录
                        if 'Users' in parts:
                            users_idx = parts.index('Users')
                            if len(parts) > users_idx + 2:
                                # 重建完整路径
                                dest_path = Path('/').joinpath(*parts[users_idx:])
                                dest_path.parent.mkdir(parents=True, exist_ok=True)
                                subprocess.run(["cp", "-p", str(item), str(dest_path)], capture_output=True)
                                restored_files.append(str(dest_path))
                    elif item.is_dir():
                        find_and_restore_files(item, base_path)
            
            find_and_restore_files(snapshot_dir)
                else:
                    # 选择性恢复
                    for path in paths:
                        path_obj = Path(path).expanduser()
                        if item.name == path_obj.name:
                            dest_path = path_obj
                            if dest_path.exists():
                                subprocess.run(
                                    ["rm", "-rf", str(dest_path)],
                                    capture_output=True
                                )
                            subprocess.run(
                                ["cp", "-rp", str(item), str(dest_path)],
                                capture_output=True
                            )
                            restored_files.append(str(dest_path))

            return {
                "success": True,
                "restored_files": restored_files,
                "snapshot_id": commit_hash,
                "description": target_snapshot["description"]
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def compare_snapshots(self, hash1: str, hash2: str) -> Dict:
        """比较两个快照"""
        try:
            result = subprocess.run(
                ["git", "diff", "--stat", hash1, hash2],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )

            return {
                "success": True,
                "diff_stat": result.stdout
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def delete_snapshot(self, commit_hash: str) -> bool:
        """删除快照（使用 git revert 或创建新的清理提交）"""
        # 注意：Git 不支持删除历史记录
        # 这里我们创建一个标记删除的提交
        subprocess.run(
            ["git", "tag", "-d", f"deleted_{commit_hash}"],
            cwd=self.repo_path,
            capture_output=True
        )
        return True


# 测试代码
if __name__ == "__main__":
    import sys

    manager = SnapshotManager()

    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python snapshot.py create <path1> [path2] ...")
        print("  python snapshot.py list")
        print("  python snapshot.py restore <commit-hash>")
        print("  python snapshot.py compare <hash1> <hash2>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 3:
            print("错误: 请指定要快照的路径")
            sys.exit(1)

        paths = sys.argv[2:]
        result = manager.create_snapshot(
            paths_to_snapshot=paths,
            operation_desc="手动创建的快照",
            auto=False
        )

        print(f"✅ 快照创建成功!")
        print(f"   ID: {result['id']}")
        print(f"   时间: {result['timestamp']}")
        print(f"   文件数: {len(result['files'])}")

    elif command == "list":
        snapshots = manager.list_snapshots()

        print(f"\n📸 快照列表 (共 {len(snapshots)} 个):\n")
        for snap in snapshots:
            auto_mark = "🤖 " if snap["description"].startswith("[AUTO]") else "📝 "
            print(f"{auto_mark}{snap['id'][:12]}")
            print(f"   时间: {snap['timestamp']}")
            print(f"   描述: {snap['description']}")
            print()

    elif command == "restore":
        if len(sys.argv) < 3:
            print("错误: 请指定快照 ID")
            sys.exit(1)

        commit_hash = sys.argv[2]
        result = manager.restore_snapshot(commit_hash)

        if result["success"]:
            print(f"✅ 恢复成功!")
            print(f"   快照: {result['description']}")
            print(f"   恢复的文件数: {len(result['restored_files'])}")
        else:
            print(f"❌ 恢复失败: {result['error']}")

    elif command == "compare":
        if len(sys.argv) < 4:
            print("错误: 请指定两个快照 ID")
            sys.exit(1)

        hash1 = sys.argv[2]
        hash2 = sys.argv[3]
        result = manager.compare_snapshots(hash1, hash2)

        if result["success"]:
            print(f"📊 快照差异:\n")
            print(result["diff_stat"])
        else:
            print(f"❌ 比较失败: {result['error']}")
