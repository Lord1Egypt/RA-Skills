import os
from pathlib import Path

DEFAULT_BLACKLIST = {
    "node_modules", "dist", "build", "target", "__pycache__", ".git",
    ".svn", ".hg", "venv", ".venv", "env", ".env", "site-packages",
    "test", "tests", "spec", "specs", "coverage", ".pytest_cache",
    ".archmap", "archmap", ".agent_backup", "backup", "backups", "ckpt", "tmp", "temp",
    "logs", "log", "snapshots", "snapshot", "cache", "caches",
    # 运行时/缓存/存储/测试产物
    "runtime", "session_cache", "temp_input_cache", "test-evidence", "test-results",
    "lancedb_data", "pdf_storage", "review_storage", "context-archive", "checkpoint",
    "memory", "workspace", "mempalace.egg-info", "logs", "output",
}


class SourceScanner:
    SOURCE_EXTENSIONS = {
        ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".java", ".rs",
        ".cpp", ".c", ".h", ".vue", ".cs", ".rb", ".php", ".kt", ".scala", ".swift",
    }

    def __init__(self, blacklist: set[str] | None = None):
        self.blacklist = blacklist or DEFAULT_BLACKLIST

    def _has_source_files(self, dirpath: Path) -> bool:
        for root, dirs, files in os.walk(dirpath):
            dirs[:] = [d for d in dirs if not self.is_blacklisted(Path(root) / d)]
            if any(Path(f).suffix.lower() in self.SOURCE_EXTENSIONS for f in files):
                return True
        return False

    def is_blacklisted(self, path: Path) -> bool:
        for part in path.parts:
            lower = part.lower()
            if lower in self.blacklist or part.startswith(".") or part.endswith(".egg-info"):
                return True
        return any(part in self.blacklist for part in path.parts)

    def scan(self, source_root: str | Path) -> list[dict]:
        root = Path(source_root).resolve()
        modules = []
        # 仅扫描项目根目录下的一级业务目录，避免子目录、存储分片、版本目录被识别为独立模块
        for dirpath in sorted(root.iterdir()):
            if not dirpath.is_dir():
                continue
            if self.is_blacklisted(dirpath):
                continue
            if not self._has_source_files(dirpath):
                continue
            rel = dirpath.relative_to(root)
            modules.append({
                "module_id": str(rel).replace("/", "_"),
                "module_path": str(rel) + "/",
                "abs_path": str(dirpath),
            })
        if not modules:
            modules.append({
                "module_id": "root",
                "module_path": "./",
                "abs_path": str(root),
            })
        return modules
