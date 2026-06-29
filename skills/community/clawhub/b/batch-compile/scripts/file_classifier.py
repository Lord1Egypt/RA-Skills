from __future__ import annotations

from pathlib import Path

COMMON_MODULE_VERSION = "paperkb-v3.0"

DOC_EXT = {".md", ".txt", ".pdf", ".docx", ".xlsx", ".xls"}
CODE_EXT = {".py", ".js", ".ts", ".java", ".cpp", ".c", ".h", ".hpp", ".go", ".rs", ".sh", ".bat", ".ps1", ".ipynb"}
DEP_NAMES = {"requirements.txt", "environment.yml", "environment.yaml", "pyproject.toml", "package.json", "Dockerfile", "docker-compose.yml", "setup.py", "CMakeLists.txt"}
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", "target", ".cache", ".idea", ".vscode"}
SKIP_EXT = {".png", ".jpg", ".jpeg", ".gif", ".mp4", ".avi", ".zip", ".rar", ".7z", ".pt", ".pth", ".onnx", ".ckpt", ".bin", ".npy", ".npz"}


def classify(path: str, size: int = 0) -> dict:
    p = Path(path)
    parts = set(p.parts)
    if parts & SKIP_DIRS:
        return {"kind": "skip", "action": "skip", "reason": "ignored directory"}
    if p.suffix in SKIP_EXT:
        return {"kind": "binary", "action": "skip", "reason": "binary/media/model file"}
    if p.name in DEP_NAMES:
        return {"kind": "dependency", "action": "dependency_context", "reason": "dependency/config file"}
    if p.name.lower().startswith("readme"):
        return {"kind": "markdown", "action": "code_context", "reason": "README included in codebase overview"}
    if p.suffix.lower() in DOC_EXT:
        return {"kind": p.suffix.lower().lstrip(".") or "text", "action": "document", "reason": "document file"}
    if p.suffix.lower() in CODE_EXT:
        return {"kind": "code", "action": "code_context", "reason": "code file"}
    return {"kind": "other", "action": "skip", "reason": "unsupported file type"}
