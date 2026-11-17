import hashlib
import json
import re
from pathlib import Path
from typing import Any

from .granularity_validator import GranularityValidator
from .source_scanner import DEFAULT_BLACKLIST, SourceScanner

_SOURCE_EXTS = SourceScanner.SOURCE_EXTENSIONS


def _is_source_file(f: Path, root: Path) -> bool:
    return f.is_file() and f.suffix.lower() in _SOURCE_EXTS and not (set(f.relative_to(root).parts) & DEFAULT_BLACKLIST)


def _file_hash(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    except Exception:
        return ""


class WorkerAgent:
    def __init__(self, max_input_chars: int = 12000, validator: GranularityValidator | None = None):
        self.max_input_chars = max_input_chars
        self.validator = validator or GranularityValidator()

    def _collect_source_snippets(self, module: dict) -> str:
        p = Path(module["abs_path"])
        if not p.is_dir():
            return ""
        chunks = []
        for f in sorted(p.rglob("*")):
            if not _is_source_file(f, p):
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if len(text) > self.max_input_chars:
                text = text[:self.max_input_chars]
            chunks.append(f"# {f.relative_to(p)}\n{text}")
        return "\n\n".join(chunks)

    def _heuristic_parse(self, text: str) -> dict:
        storages = []
        # 定义路由（服务端框架装饰器/注册，提供方证据）：FastAPI/Flask 装饰器 + Express 注册
        defined = set(re.findall(r'@\w+\.(?:get|post|put|delete|patch|route)\(\s*["\']([^"\']+)["\']', text, re.I))
        defined |= set(re.findall(r'(?:app|router)\.(?:get|post|put|delete|patch)\(\s*["\']([^"\']+)["\']', text, re.I))
        # 引用路由（消费方证据；扣除自身已定义的）：
        # ① 引号包裹的 /api/ 路径或完整 URL ② 无引号裸 URL（curl 等脚本调用）
        referenced = set(re.findall(r'["\'](?:https?://[^"\'/\s]+)?(/api/[^"\'?\s]+)', text))
        referenced |= set(re.findall(r'https?://[^/\s"\'\)]+(/api/[^?\s"\'\)]+)', text))
        referenced -= defined
        apis = [{"route": r, "purpose": "heuristic", "shared": False, "kind": "defined"} for r in sorted(defined)]
        apis += [{"route": r, "purpose": "heuristic", "shared": False, "kind": "referenced"} for r in sorted(referenced)]
        # 存储名称模式
        for m in set(re.findall(r'(?:redis|kafka|rabbitmq|mysql|postgres|mongodb|elasticsearch|table)["\']?\s*[:=]\s*["\']([^"\']+)["\']', text, re.I)):
            storages.append({"name": m, "shared": False})
        # 真实 import 提取（代码级依赖证据）：Python 顶层包 + JS/TS 非相对包
        imports = {m.split(".")[0] for m in re.findall(r'^\s*(?:from|import)\s+([\w][\w.]*)', text, re.M)}
        for py_pkg, js_pkg in re.findall(r'from\s+["\']([^"\']+)["\']|require\(\s*["\']([^"\']+)["\']\s*\)', text):
            pkg = py_pkg or js_pkg
            if not pkg.startswith("."):
                parts = pkg.split("/")
                imports.add("/".join(parts[:2]) if pkg.startswith("@") else parts[0])
        return {"apis": apis, "storages": storages, "imports": sorted(imports - {""})}

    def parse(self, module: dict) -> dict:
        text = self._collect_source_snippets(module)
        parsed = self._heuristic_parse(text)
        result = {
            "module_id": module["module_id"],
            "module_path": module["module_path"],
            "apis": parsed["apis"],
            "storages": parsed["storages"],
            "imports": parsed["imports"],
            "dependencies": [],
            "dependents": [],
        }
        ok, violations = self.validator.validate(result)
        result["granularity_ok"] = ok
        result["violations"] = violations
        return result

    def parse_batch(self, modules: list[dict]) -> list[dict]:
        return [self.parse(m) for m in modules]

    def module_hash(self, module: dict) -> str:
        """计算模块内容指纹，用于同步模式识别变更模块。"""
        p = Path(module["abs_path"])
        if not p.is_dir():
            return ""
        hashes = []
        for f in sorted(p.rglob("*")):
            if not _is_source_file(f, p):
                continue
            h = _file_hash(f)
            if h:
                hashes.append(f"{f.relative_to(p)}:{h}")
        return hashlib.sha256("|".join(hashes).encode("utf-8")).hexdigest()[:16]

    def module_hashes(self, modules: list[dict]) -> dict[str, str]:
        return {m["module_id"]: self.module_hash(m) for m in modules}
