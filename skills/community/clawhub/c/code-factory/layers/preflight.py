"""
Phase 0: 环境预检层 —— 生成前先验证环境完整性。

借鉴 CLI-Anything 理念：不通过则直接报告缺少什么，不盲目生成。
"""

import sys
import shutil
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class PreflightResult:
    """环境预检结果"""
    python_ok: bool = False
    dir_writable: bool = False
    disk_sufficient: bool = False
    deps_available: bool = True

    python_version: str = ""
    required_python: str = ""
    target_dir: str = ""

    python_issue: Optional[str] = None
    dir_issue: Optional[str] = None
    disk_issue: Optional[str] = None
    deps_issue: Optional[str] = None

    @property
    def all_ok(self) -> bool:
        return self.python_ok and self.dir_writable and self.disk_sufficient and self.deps_available

    def to_dict(self) -> dict:
        return {
            "all_ok": self.all_ok,
            "python_ok": self.python_ok,
            "python_version": self.python_version,
            "required_python": self.required_python,
            "dir_writable": self.dir_writable,
            "disk_sufficient": self.disk_sufficient,
            "deps_available": self.deps_available,
            "issues": [i for i in [
                self.python_issue, self.dir_issue, self.disk_issue, self.deps_issue
            ] if i],
        }


class PreflightRunner:
    """Phase 0 环境预检执行器"""

    MIN_DISK_MB = 100  # 最少需要 100MB 磁盘空间

    def run(
        self,
        target_dir: Path,
        required_python: str = "3.10",
        required_deps: Optional[List[str]] = None,
    ) -> PreflightResult:
        result = PreflightResult(
            python_version=sys.version.split()[0],
            required_python=required_python,
            target_dir=str(target_dir),
        )

        self._check_python(result)
        self._check_directory(target_dir, result)
        self._check_disk(target_dir, result)
        self._check_dependencies(required_deps or [], result)

        return result

    def _check_python(self, result: PreflightResult) -> None:
        """检查 Python 版本"""
        current = sys.version_info
        try:
            parts = result.required_python.split(".")
            required_major, required_minor = int(parts[0]), int(parts[1])
        except (ValueError, IndexError):
            result.python_ok = False
            result.python_issue = f"无法解析要求的 Python 版本: {result.required_python}"
            return

        if current.major < required_major or (
            current.major == required_major and current.minor < required_minor
        ):
            result.python_ok = False
            result.python_issue = (
                f"Python 版本不满足: 需要 >={result.required_python}, "
                f"当前 {current.major}.{current.minor}"
            )
        else:
            result.python_ok = True

    def _check_directory(self, target_dir: Path, result: PreflightResult) -> None:
        """检查目标目录是否可写"""
        try:
            target_dir.mkdir(parents=True, exist_ok=True)
            test_file = target_dir / ".write_test"
            test_file.write_text("test")
            test_file.unlink()
            result.dir_writable = True
        except (OSError, PermissionError) as e:
            result.dir_writable = False
            result.dir_issue = f"目标目录不可写: {target_dir} ({e})"

    def _check_disk(self, target_dir: Path, result: PreflightResult) -> None:
        """检查磁盘空间"""
        try:
            usage = shutil.disk_usage(target_dir if target_dir.exists() else Path.cwd())
            free_mb = usage.free // (1024 * 1024)
            if free_mb < self.MIN_DISK_MB:
                result.disk_sufficient = False
                result.disk_issue = f"磁盘空间不足: 剩余 {free_mb}MB, 需要至少 {self.MIN_DISK_MB}MB"
            else:
                result.disk_sufficient = True
        except Exception as e:
            # 无法检测磁盘空间时不阻断
            result.disk_sufficient = True

    def _check_dependencies(self, deps: List[str], result: PreflightResult) -> None:
        """检查必要依赖是否已安装"""
        missing = []
        for dep in deps:
            # 尝试 import
            pkg_name = dep.split("==")[0].split(">=")[0].split("<=")[0].strip()
            try:
                __import__(pkg_name.replace("-", "_"))
            except ImportError:
                missing.append(pkg_name)

        if missing:
            result.deps_available = False
            result.deps_issue = f"缺少依赖: {', '.join(missing)}"
