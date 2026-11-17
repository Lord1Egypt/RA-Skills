import re
from pathlib import Path
from typing import Any

# 常见中文需求词汇 → 代码中可能出现的英文对应词
CN_TO_EN_KEYWORDS = {
    "用户": "user users",
    "登录": "login auth session",
    "注册": "register signup",
    "角色": "role roles permission",
    "权限": "permission rbac auth",
    "订单": "order orders",
    "商品": "product goods item",
    "积分": "point credit score",
    "支付": "pay payment",
    "接口": "api route endpoint",
    "路由": "route router api",
    "数据库": "db database table",
    "表": "table",
    "字段": "field column",
    "服务": "service",
    "模块": "module",
    "文件": "file",
    "配置": "config configuration",
    "测试": "test testing",
    "报告": "report report_builder builder",
    "生成": "generate build create",
    "自动化": "automation auto",
    "引擎": "engine",
    "页面": "page vue component",
}

DEFAULT_BLACKLIST = {
    "node_modules", "dist", "build", "target", "__pycache__", ".git",
    ".svn", ".hg", "venv", ".venv", "env", ".env", "site-packages",
    "test", "tests", "coverage", ".pytest_cache",
    ".archmap", "archmap", ".agent_backup", "backup", "backups", "ckpt", "tmp", "temp",
    "logs", "log", "snapshots", "snapshot", "cache", "caches",
    "runtime", "session_cache", "temp_input_cache", "test-evidence", "test-results",
    "lancedb_data", "pdf_storage", "review_storage", "context-archive", "checkpoint",
    "memory", "workspace", ".egg-info",
}

SOURCE_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".vue", ".go", ".java", ".rs", ".cs", ".rb", ".php",
}


class ModuleDetailAnalyzer:
    """模块内精准定位分析器。

    在目录级匹配命中后，对单个业务目录模块做二次解析：
    - 识别模块内源码文件
    - 提取函数、类、接口路由
    - 建立 路由→文件、需求关键词→文件 的映射
    - 按需求文本对文件进行相关度排序
    """

    def __init__(self, max_file_chars: int = 12000):
        self.max_file_chars = max_file_chars

    def _extract_functions(self, text: str) -> list[str]:
        return sorted(set(re.findall(r"^\s*def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(", text, re.M)))

    def _extract_classes(self, text: str) -> list[str]:
        return sorted(set(re.findall(r"^\s*class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[\(:]", text, re.M)))

    def _extract_routes(self, text: str) -> list[str]:
        routes = set()
        for m in re.findall(r'[@\w]*route\(["\']?([^"\')\s]+)', text, re.I):
            routes.add(m)
        for m in re.findall(r'["\'](?:/api/[^"\']+)["\']', text):
            routes.add(m.strip('"\''))
        return sorted(routes)

    def _keyword_relevance(self, requirement: str, file_info: dict) -> float:
        """简单需求关键词相关度：按需求中关键词在文件元信息中的命中次数打分。"""
        req = re.sub(r"[^一-龥a-zA-Z0-9]", " ", requirement).lower()
        raw_tokens = [k for k in req.split() if len(k) >= 2]

        # 中英文分词：英文保持原词，中文拆为 2-gram，提升关键词命中
        keywords = []
        for token in raw_tokens:
            if re.search(r"[一-龥]", token):
                for i in range(len(token) - 1):
                    keywords.append(token[i:i + 2])
            else:
                keywords.append(token)

        # 中文关键词扩展为英文对应词
        expanded = []
        for k in keywords:
            expanded.append(k)
            if k in CN_TO_EN_KEYWORDS:
                expanded.extend(CN_TO_EN_KEYWORDS[k].split())
        keywords = expanded
        if not keywords:
            return 0.0

        def normalize(s: str) -> str:
            return re.sub(r"[^一-龥a-zA-Z0-9]", " ", s).lower()

        corpus = " ".join([
            file_info["file_path"],
            *file_info["functions"],
            *file_info["classes"],
            *file_info["routes"],
        ])
        corpus = normalize(corpus)
        hits = sum(1 for k in keywords if k in corpus)
        return hits / len(keywords)

    def analyze(self, module: dict, requirement_text: str = "") -> dict[str, Any]:
        p = Path(module["abs_path"])
        if not p.is_dir():
            return {"module_id": module["module_id"], "files": [], "route_to_files": {}, "keyword_matches": []}

        files: list[dict[str, Any]] = []
        route_to_files: dict[str, list[str]] = {}
        for f in sorted(p.rglob("*")):
            if not f.is_file():
                continue
            rel_path = f.relative_to(p)
            rel_parts = set(rel_path.parts)
            if rel_parts & DEFAULT_BLACKLIST:
                continue
            if f.suffix.lower() not in SOURCE_EXTENSIONS:
                continue
            rel_path_str = str(rel_path)
            if rel_path_str.endswith(".vue.js") or rel_path_str.endswith(".min.js"):
                continue
            if f.stat().st_size > 512 * 1024:
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            if len(text) > self.max_file_chars:
                text = text[:self.max_file_chars]

            rel_path_str = str(rel_path)
            functions = self._extract_functions(text)
            classes = self._extract_classes(text)
            routes = self._extract_routes(text)

            file_info = {
                "file_path": rel_path_str,
                "functions": functions,
                "classes": classes,
                "routes": routes,
            }
            file_info["relevance"] = self._keyword_relevance(requirement_text, file_info)
            files.append(file_info)

        files.sort(key=lambda x: x["relevance"], reverse=True)
        top_files = [f for f in files if f["relevance"] > 0][:15]

        for f in top_files:
            for r in f["routes"]:
                route_to_files.setdefault(r, []).append(f["file_path"])

        keyword_matches = [f["file_path"] for f in top_files if f["relevance"] > 0]

        return {
            "module_id": module["module_id"],
            "module_path": module["module_path"],
            "files": top_files,
            "route_to_files": route_to_files,
            "keyword_matches": keyword_matches,
        }

    def analyze_modules(self, modules: list[dict], requirement_text: str = "") -> list[dict]:
        return [self.analyze(m, requirement_text) for m in modules]
