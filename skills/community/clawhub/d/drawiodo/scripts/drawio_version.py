"""
drawio_version - draw.io 图表版本管理系统
支持5版本回溯、版本日志、文件备份与恢复
"""

import os
import shutil
import json
from datetime import datetime
from pathlib import Path


class VersionManager:
    """draw.io 图表版本管理器"""

    def __init__(self, base_dir: str, max_versions: int = 5):
        """
        Args:
            base_dir: 图表文件所在目录
            max_versions: 最大保留版本数（默认5）
        """
        self.base_dir = Path(base_dir)
        self.max_versions = max_versions
        self.versions_dir = self.base_dir / ".drawio_versions"

    def _ensure_dir(self):
        """确保版本目录存在"""
        self.versions_dir.mkdir(parents=True, exist_ok=True)

    def _version_dir(self, filepath: str, version: str) -> Path:
        """获取指定版本的目录路径"""
        filename = Path(filepath).stem  # 不含扩展名
        return self.versions_dir / filename / version

    def _meta_file(self, version_dir: Path) -> Path:
        """获取版本元数据文件路径"""
        return version_dir / "meta.json"

    def _log_file(self, filepath: str) -> Path:
        """获取变更日志文件路径"""
        filename = Path(filepath).stem
        return self.versions_dir / filename / "changelog.json"

    def init(self, filepath: str, description: str = "") -> dict:
        """
        初始化一个图表的版本管理

        Args:
            filepath: 图表文件路径
            description: 初始版本描述

        Returns:
            版本信息字典
        """
        self._ensure_dir()
        fp = Path(filepath)
        if not fp.exists():
            raise FileNotFoundError(f"文件不存在: {filepath}")

        version = "v1"
        vdir = self._version_dir(filepath, version)
        vdir.mkdir(parents=True, exist_ok=True)

        # 复制文件到版本目录
        shutil.copy2(fp, vdir / fp.name)

        # 写入元数据
        meta = {
            "version": version,
            "timestamp": datetime.now().isoformat(),
            "description": description or "初始版本",
            "source_file": fp.name,
            "source_path": str(fp),
            "file_size": fp.stat().st_size,
        }
        with open(self._meta_file(vdir), "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

        # 初始化变更日志
        changelog_path = self._log_file(filepath)
        changelog_path.parent.mkdir(parents=True, exist_ok=True)
        changelog = [meta]
        with open(changelog_path, "w", encoding="utf-8") as f:
            json.dump(changelog, f, ensure_ascii=False, indent=2)

        return meta

    def save_version(self, filepath: str, description: str = "") -> dict:
        """
        保存当前文件为新版本

        Args:
            filepath: 当前图表文件路径
            description: 版本描述（如"修改了XX"）

        Returns:
            新版本信息字典
        """
        self._ensure_dir()
        fp = Path(filepath)
        if not fp.exists():
            raise FileNotFoundError(f"文件不存在: {filepath}")

        # 获取当前版本号
        current = self.current_version(filepath)
        if current is None:
            return self.init(filepath, description)

        # 计算新版本号
        version_num = int(current["version"].lstrip("v")) + 1
        new_version = f"v{version_num}"

        # 创建新版本目录
        vdir = self._version_dir(filepath, new_version)
        vdir.mkdir(parents=True, exist_ok=True)

        # 复制当前文件
        shutil.copy2(fp, vdir / fp.name)

        # 写入元数据
        meta = {
            "version": new_version,
            "timestamp": datetime.now().isoformat(),
            "description": description or f"版本 {new_version}",
            "source_file": fp.name,
            "source_path": str(fp),
            "file_size": fp.stat().st_size,
        }
        with open(self._meta_file(vdir), "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)

        # 更新变更日志
        changelog_path = self._log_file(filepath)
        if changelog_path.exists():
            with open(changelog_path, "r", encoding="utf-8") as f:
                changelog = json.load(f)
        else:
            changelog = []
        changelog.append(meta)

        # 超过最大版本数时，删除最旧的版本
        while len(changelog) > self.max_versions:
            oldest = changelog.pop(0)
            old_dir = self._version_dir(filepath, oldest["version"])
            if old_dir.exists():
                shutil.rmtree(old_dir)

        with open(changelog_path, "w", encoding="utf-8") as f:
            json.dump(changelog, f, ensure_ascii=False, indent=2)

        return meta

    def current_version(self, filepath: str) -> dict | None:
        """获取当前最新版本信息"""
        changelog_path = self._log_file(filepath)
        if not changelog_path.exists():
            return None
        with open(changelog_path, "r", encoding="utf-8") as f:
            changelog = json.load(f)
        return changelog[-1] if changelog else None

    def list_versions(self, filepath: str) -> list[dict]:
        """
        列出所有版本

        Returns:
            版本列表，从旧到新
        """
        changelog_path = self._log_file(filepath)
        if not changelog_path.exists():
            return []
        with open(changelog_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def restore_version(self, filepath: str, version: str) -> dict:
        """
        恢复到指定版本（不会删除当前版本，而是基于目标版本创建新的恢复版本）

        Args:
            filepath: 当前图表文件路径
            version: 要恢复的版本号，如 "v2"

        Returns:
            恢复后的新版本信息
        """
        vdir = self._version_dir(filepath, version)
        if not vdir.exists():
            raise FileNotFoundError(f"版本 {version} 不存在")

        fp = Path(filepath)
        # 找到版本目录中的 .drawio 文件
        version_files = list(vdir.glob("*.drawio"))
        if not version_files:
            raise FileNotFoundError(f"版本 {version} 中没有找到 .drawio 文件")

        # 备份当前文件到新版本（标记为恢复前快照）
        current = self.current_version(filepath)
        if current:
            # 先保存当前状态
            self.save_version(filepath, description=f"恢复前自动备份（当前 {current['version']}）")

        # 恢复目标版本文件
        shutil.copy2(version_files[0], fp)

        # 创建新版本记录
        return self.save_version(filepath, description=f"从 {version} 恢复")

    def get_version_file(self, filepath: str, version: str) -> str | None:
        """
        获取指定版本的文件路径（用于预览）

        Returns:
            版本文件的绝对路径，不存在则返回None
        """
        vdir = self._version_dir(filepath, version)
        version_files = list(vdir.glob("*.drawio"))
        if version_files:
            return str(version_files[0])
        return None

    def diff_versions(self, filepath: str, v1: str, v2: str) -> dict:
        """
        比较两个版本的差异（简单比较文件大小和描述）

        Returns:
            差异信息字典
        """
        versions = self.list_versions(filepath)
        v1_info = next((v for v in versions if v["version"] == v1), None)
        v2_info = next((v for v in versions if v["version"] == v2), None)

        if not v1_info or not v2_info:
            raise ValueError(f"版本 {v1} 或 {v2} 不存在")

        return {
            "from": v1_info,
            "to": v2_info,
            "size_change": v2_info["file_size"] - v1_info["file_size"],
            "time_diff": "",
        }

    def status(self, filepath: str) -> dict:
        """
        获取图表的版本管理状态

        Returns:
            状态信息字典
        """
        changelog = self.list_versions(filepath)
        current = self.current_version(filepath)

        return {
            "filepath": filepath,
            "is_managed": len(changelog) > 0,
            "total_versions": len(changelog),
            "current_version": current["version"] if current else None,
            "last_modified": current["timestamp"] if current else None,
            "max_versions": self.max_versions,
            "versions": changelog,
        }


# ============== CLI ==============

def main():
    import sys

    if len(sys.argv) < 3:
        print("用法:")
        print("  python drawio_version.py init <文件> [描述]       - 初始化版本管理")
        print("  python drawio_version.py save <文件> [描述]       - 保存新版本")
        print("  python drawio_version.py list <文件>              - 列出所有版本")
        print("  python drawio_version.py restore <文件> <版本号>  - 恢复到指定版本")
        print("  python drawio_version.py status <文件>            - 查看版本状态")
        return

    command = sys.argv[1]
    filepath = sys.argv[2]
    base_dir = str(Path(filepath).parent)
    vm = VersionManager(base_dir)

    if command == "init":
        desc = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        result = vm.init(filepath, desc)
        print(f"[OK] 已初始化版本管理: {result['version']} - {result['description']}")

    elif command == "save":
        desc = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        result = vm.save_version(filepath, desc)
        print(f"[OK] 已保存: {result['version']} - {result['description']}")

    elif command == "list":
        versions = vm.list_versions(filepath)
        if not versions:
            print("暂无版本记录")
        for v in versions:
            ts = v["timestamp"][:19]
            size_kb = v["file_size"] / 1024
            marker = " <-- current" if v == versions[-1] else ""
            print(f"  {v['version']:>4}  {ts}  {size_kb:6.1f}KB  {v['description']}{marker}")

    elif command == "restore":
        if len(sys.argv) < 4:
            print("请指定版本号，如: python drawio_version.py restore test.drawio v2")
            return
        version = sys.argv[3]
        result = vm.restore_version(filepath, version)
        print(f"[OK] 已从 {version} 恢复: {result['version']} - {result['description']}")
        print(f"     文件已更新: {filepath}")

    elif command == "status":
        status = vm.status(filepath)
        if status["is_managed"]:
            print(f"文件: {status['filepath']}")
            print(f"当前版本: {status['current_version']}")
            print(f"版本总数: {status['total_versions']}/{status['max_versions']}")
            print(f"最后修改: {status['last_modified'][:19]}")
        else:
            print(f"文件: {status['filepath']}")
            print("状态: 未纳入版本管理（使用 init 命令初始化）")

    else:
        print(f"未知命令: {command}")
        print("支持的命令: init, save, list, restore, status")


if __name__ == "__main__":
    main()
