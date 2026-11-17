#!/usr/bin/env python3
"""
Git Worktree Manager — 隔离开发工作区管理

功能：
- create: 创建新 worktree + 新分支
- list: 列出所有 worktree
- cleanup: 清理已合并的 worktree
- switch: 切换到指定 worktree

用法：
    python worktree-manager.py create --name "feature-x" [--base master]
    python worktree-manager.py list
    python worktree-manager.py cleanup [--merged]
    python worktree-manager.py switch --name "feature-x"

目录结构：
    workspace/
      .worktrees/
        feature-x/    # 隔离的工作区
        feature-y/
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


class WorktreeManager:
    """Git Worktree 管理器"""
    
    def __init__(self, repo_root: str = None):
        """初始化
        
        Args:
            repo_root: 仓库根目录，默认当前目录
        """
        self.repo_root = Path(repo_root) if repo_root else Path.cwd()
        self.worktrees_dir = self.repo_root / ".worktrees"
        self.worktrees_dir.mkdir(exist_ok=True)
        
    def run_git(self, *args, check=True) -> subprocess.CompletedProcess:
        """运行 git 命令
        
        Args:
            *args: git 命令参数
            check: 是否检查返回码
            
        Returns:
            CompletedProcess 对象
        """
        cmd = ["git"] + list(args)
        return subprocess.run(
            cmd,
            cwd=self.repo_root,
            capture_output=True,
            text=True,
            check=check
        )
    
    def create(self, name: str, base: str = "master") -> dict:
        """创建新 worktree
        
        Args:
            name: worktree 名称（也是分支名）
            base: 基础分支
            
        Returns:
            包含状态信息的字典
        """
        # 检查是否已存在
        worktree_path = self.worktrees_dir / name
        if worktree_path.exists():
            return {
                "status": "error",
                "message": f"Worktree '{name}' 已存在: {worktree_path}"
            }
        
        # 检查分支是否存在
        branch_result = self.run_git("rev-parse", "--verify", name, check=False)
        branch_exists = branch_result.returncode == 0
        
        # 创建 worktree
        if branch_exists:
            # 分支已存在，直接创建 worktree
            result = self.run_git(
                "worktree", "add",
                str(worktree_path),
                name
            )
        else:
            # 创建新分支并创建 worktree
            result = self.run_git(
                "worktree", "add",
                "-b", name,
                str(worktree_path),
                base
            )
        
        if result.returncode != 0:
            return {
                "status": "error",
                "message": f"创建 worktree 失败: {result.stderr}"
            }
        
        # 记录元数据
        metadata = {
            "name": name,
            "branch": name,
            "base": base,
            "created_at": datetime.now().isoformat(),
            "path": str(worktree_path)
        }
        
        metadata_file = worktree_path / ".worktree-metadata.json"
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        return {
            "status": "success",
            "message": f"已创建 worktree '{name}'",
            "path": str(worktree_path),
            "branch": name,
            "metadata": metadata
        }
    
    def list(self) -> dict:
        """列出所有 worktree
        
        Returns:
            包含 worktree 列表的字典
        """
        result = self.run_git("worktree", "list", "--porcelain")
        
        worktrees = []
        current = {}
        
        for line in result.stdout.splitlines():
            if line.startswith("worktree "):
                if current:
                    worktrees.append(current)
                current = {"path": line[9:]}
            elif line.startswith("HEAD "):
                current["head"] = line[5:]
            elif line.startswith("branch "):
                current["branch"] = line[7:]
            elif line == "bare":
                current["bare"] = True
            elif line == "detached":
                current["detached"] = True
        
        if current:
            worktrees.append(current)
        
        # 过滤 .worktrees 下的 worktree
        managed_worktrees = [
            wt for wt in worktrees
            if str(self.worktrees_dir) in wt.get("path", "")
        ]
        
        # 加载元数据
        for wt in managed_worktrees:
            metadata_file = Path(wt["path"]) / ".worktree-metadata.json"
            if metadata_file.exists():
                with open(metadata_file, "r", encoding="utf-8") as f:
                    wt["metadata"] = json.load(f)
        
        return {
            "status": "success",
            "total": len(managed_worktrees),
            "worktrees": managed_worktrees
        }
    
    def cleanup(self, merged_only: bool = False) -> dict:
        """清理 worktree
        
        Args:
            merged_only: 是否只清理已合并的
            
        Returns:
            包含清理结果的字典
        """
        worktrees_info = self.list()
        removed = []
        errors = []
        
        for wt in worktrees_info["worktrees"]:
            path = wt["path"]
            branch = wt.get("branch", "").replace("refs/heads/", "")
            
            # 检查是否已合并
            if merged_only and branch:
                merge_check = self.run_git(
                    "branch", "--merged", "master",
                    check=False
                )
                if branch not in merge_check.stdout:
                    continue
            
            # 移除 worktree
            result = self.run_git("worktree", "remove", path, check=False)
            
            if result.returncode == 0:
                removed.append({"path": path, "branch": branch})
                
                # 删除分支（如果已合并）
                if merged_only and branch:
                    self.run_git("branch", "-d", branch, check=False)
            else:
                errors.append({
                    "path": path,
                    "error": result.stderr.strip()
                })
        
        return {
            "status": "success",
            "removed": removed,
            "errors": errors,
            "message": f"已清理 {len(removed)} 个 worktree"
        }
    
    def switch(self, name: str) -> dict:
        """切换到指定 worktree
        
        Args:
            name: worktree 名称
            
        Returns:
            包含切换结果的字典
        """
        worktree_path = self.worktrees_dir / name
        
        if not worktree_path.exists():
            return {
                "status": "error",
                "message": f"Worktree '{name}' 不存在"
            }
        
        return {
            "status": "success",
            "message": f"切换到 worktree '{name}'",
            "path": str(worktree_path),
            "command": f"cd {worktree_path}"
        }
    
    def status(self, name: str = None) -> dict:
        """获取 worktree 状态
        
        Args:
            name: worktree 名称，None 表示当前
            
        Returns:
            包含状态信息的字典
        """
        if name:
            worktree_path = self.worktrees_dir / name
        else:
            worktree_path = self.repo_root
        
        if not worktree_path.exists():
            return {
                "status": "error",
                "message": f"Worktree 不存在: {worktree_path}"
            }
        
        # 获取 git status
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            check=False
        )
        
        changes = []
        for line in result.stdout.splitlines():
            if line.strip():
                status = line[0]
                file_path = line[3:]
                changes.append({"status": status, "file": file_path})
        
        # 获取当前分支
        branch_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=worktree_path,
            capture_output=True,
            text=True,
            check=False
        )
        branch = branch_result.stdout.strip()
        
        return {
            "status": "success",
            "path": str(worktree_path),
            "branch": branch,
            "changes": changes,
            "clean": len(changes) == 0
        }


def main():
    parser = argparse.ArgumentParser(description="Git Worktree Manager")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # create 命令
    create_parser = subparsers.add_parser("create", help="创建新 worktree")
    create_parser.add_argument("--name", required=True, help="worktree 名称")
    create_parser.add_argument("--base", default="master", help="基础分支")
    
    # list 命令
    subparsers.add_parser("list", help="列出所有 worktree")
    
    # cleanup 命令
    cleanup_parser = subparsers.add_parser("cleanup", help="清理 worktree")
    cleanup_parser.add_argument("--merged", action="store_true", help="只清理已合并的")
    
    # switch 命令
    switch_parser = subparsers.add_parser("switch", help="切换到指定 worktree")
    switch_parser.add_argument("--name", required=True, help="worktree 名称")
    
    # status 命令
    status_parser = subparsers.add_parser("status", help="获取 worktree 状态")
    status_parser.add_argument("--name", help="worktree 名称（可选）")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    manager = WorktreeManager()
    
    if args.command == "create":
        result = manager.create(args.name, args.base)
    elif args.command == "list":
        result = manager.list()
    elif args.command == "cleanup":
        result = manager.cleanup(args.merged)
    elif args.command == "switch":
        result = manager.switch(args.name)
    elif args.command == "status":
        result = manager.status(args.name)
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    if result.get("status") == "error":
        sys.exit(1)


if __name__ == "__main__":
    main()
