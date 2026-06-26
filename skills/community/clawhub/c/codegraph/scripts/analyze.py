#!/usr/bin/env python3
"""Build AST summary + call graph for a project. Outputs JSON cache.

Supports: Python (.py), JavaScript/TypeScript (.js/.jsx/.ts/.tsx), Ruby (.rb)

Usage:
    python3 analyze.py <project_dir> [--output <cache.json>] [--exclude <pattern>...]
    python3 analyze.py <project_dir> --query functions          # list all functions
    python3 analyze.py <project_dir> --query calls <func_name>  # who calls func?
    python3 analyze.py <project_dir> --query callers <func_name> # who does func call?
    python3 analyze.py <project_dir> --query file <path>        # file summary
    python3 analyze.py <project_dir> --query imports            # import graph
    python3 analyze.py <project_dir> --query classes            # all classes
    python3 analyze.py <project_dir> --query stats              # project stats
"""

import ast
import json
import os
import re
import sys
import hashlib
from pathlib import Path
from collections import defaultdict
from typing import Any

# ── Config ──

DEFAULT_EXCLUDES = {
    "node_modules", ".git", "__pycache__", ".venv", "venv", "env",
    "dist", "build", ".next", ".nuxt", "coverage", ".tox", "eggs",
    ".mypy_cache", ".pytest_cache", ".ruff_cache",
}

PY_EXTS = {".py"}
JS_EXTS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}
RB_EXTS = {".rb"}
ALL_EXTS = PY_EXTS | JS_EXTS | RB_EXTS


# ── Python AST Analyzer ──

class PyAnalyzer(ast.NodeVisitor):
    def __init__(self, filepath: str, rel_path: str):
        self.filepath = filepath
        self.rel_path = rel_path
        self.functions: list[dict] = []
        self.classes: list[dict] = []
        self.imports: list[dict] = []
        self.calls: list[dict] = []
        self._current_func: str | None = None
        self._current_class: str | None = None

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append({"module": alias.name, "alias": alias.asname, "line": node.lineno})
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        mod = node.module or ""
        for alias in node.names:
            self.imports.append({"module": f"{mod}.{alias.name}", "alias": alias.asname, "line": node.lineno})
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        bases = [self._name(b) for b in node.bases]
        self.classes.append({
            "name": node.name,
            "bases": bases,
            "line": node.lineno,
            "end_line": getattr(node, "end_lineno", node.lineno),
            "methods": [n.name for n in node.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))],
            "decorators": [self._name(d) for d in node.decorator_list],
        })
        old_class = self._current_class
        self._current_class = node.name
        self.generic_visit(node)
        self._current_class = old_class

    def visit_FunctionDef(self, node):
        self._handle_func(node)

    def visit_AsyncFunctionDef(self, node):
        self._handle_func(node)

    def _handle_func(self, node):
        params = []
        for arg in node.args.args:
            params.append({
                "name": arg.arg,
                "annotation": self._name(arg.annotation) if arg.annotation else None,
            })
        ret = self._name(node.returns) if node.returns else None
        qualified = f"{self._current_class}.{node.name}" if self._current_class else node.name

        self.functions.append({
            "name": node.name,
            "qualified_name": qualified,
            "line": node.lineno,
            "end_line": getattr(node, "end_lineno", node.lineno),
            "params": params,
            "return_type": ret,
            "decorators": [self._name(d) for d in node.decorator_list],
            "is_async": isinstance(node, ast.AsyncFunctionDef),
            "class": self._current_class,
        })

        old_func = self._current_func
        self._current_func = qualified
        self.generic_visit(node)
        self._current_func = old_func

    def visit_Call(self, node):
        callee = self._name(node.func)
        if callee and self._current_func:
            self.calls.append({
                "caller": self._current_func,
                "callee": callee,
                "line": node.lineno,
            })
        self.generic_visit(node)

    def _name(self, node) -> str | None:
        if node is None:
            return None
        if isinstance(node, ast.Name):
            return node.id
        if isinstance(node, ast.Attribute):
            val = self._name(node.value)
            return f"{val}.{node.attr}" if val else node.attr
        if isinstance(node, ast.Subscript):
            return self._name(node.value)
        if isinstance(node, ast.Call):
            return self._name(node.func)
        if isinstance(node, ast.Constant):
            return str(node.value)
        return None

    def analyze(self) -> dict:
        try:
            with open(self.filepath, "r", errors="replace") as f:
                source = f.read()
            tree = ast.parse(source, self.filepath)
            self.visit(tree)
        except SyntaxError:
            pass
        return {
            "file": self.rel_path,
            "language": "python",
            "functions": self.functions,
            "classes": self.classes,
            "imports": self.imports,
            "calls": self.calls,
            "lines": source.count("\n") + 1 if "source" in dir() else 0,
        }


# ── JS/TS Analyzer (regex-based) ──

_JS_FUNC = re.compile(
    r"(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(([^)]*)\)",
    re.MULTILINE,
)
_JS_ARROW = re.compile(
    r"(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>",
    re.MULTILINE,
)
_JS_METHOD = re.compile(
    r"(?:async\s+)?(\w+)\s*\([^)]*\)\s*\{",
    re.MULTILINE,
)
_JS_CLASS = re.compile(
    r"(?:export\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?",
    re.MULTILINE,
)
_JS_IMPORT = re.compile(
    r"import\s+(?:(?:\{[^}]*\}|\w+|\*\s+as\s+\w+)(?:\s*,\s*(?:\{[^}]*\}|\w+))*\s+from\s+)?['\"]([^'\"]+)['\"]",
    re.MULTILINE,
)
_JS_REQUIRE = re.compile(
    r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
    re.MULTILINE,
)
_JS_CALL = re.compile(r"(\w+(?:\.\w+)*)\s*\(", re.MULTILINE)


def analyze_js(filepath: str, rel_path: str) -> dict:
    try:
        with open(filepath, "r", errors="replace") as f:
            source = f.read()
    except Exception:
        return {"file": rel_path, "language": "javascript", "functions": [], "classes": [], "imports": [], "calls": [], "lines": 0}

    lines = source.split("\n")
    functions = []
    classes = []
    imports = []
    calls = []

    for m in _JS_FUNC.finditer(source):
        ln = source[:m.start()].count("\n") + 1
        raw = m.group(2).strip()
        clean = ", ".join(p.split("=")[0].split(":")[0].strip() for p in raw.split(",") if p.strip()) if raw else ""
        functions.append({"name": m.group(1), "qualified_name": m.group(1), "line": ln, "params": clean})

    for m in _JS_ARROW.finditer(source):
        ln = source[:m.start()].count("\n") + 1
        functions.append({"name": m.group(1), "qualified_name": m.group(1), "line": ln, "params": ""})

    for m in _JS_CLASS.finditer(source):
        ln = source[:m.start()].count("\n") + 1
        classes.append({"name": m.group(1), "bases": [m.group(2)] if m.group(2) else [], "line": ln})

    for m in _JS_IMPORT.finditer(source):
        ln = source[:m.start()].count("\n") + 1
        imports.append({"module": m.group(1), "line": ln})

    for m in _JS_REQUIRE.finditer(source):
        ln = source[:m.start()].count("\n") + 1
        imports.append({"module": m.group(1), "line": ln})

    # Call extraction with caller context
    noise = {"if", "for", "while", "switch", "catch", "return", "throw", "new", "typeof", "instanceof", "import", "export", "require", "console"}
    # Build line→function mapping
    func_ranges = sorted(functions, key=lambda f: f["line"])
    def _find_js_caller(ln: int) -> str | None:
        best = None
        for f in func_ranges:
            if f["line"] <= ln:
                best = f["qualified_name"]
            else:
                break
        return best

    for m in _JS_CALL.finditer(source):
        callee = m.group(1)
        base = callee.split(".")[0]
        if base not in noise and len(callee) < 60:
            ln = source[:m.start()].count("\n") + 1
            caller = _find_js_caller(ln)
            entry = {"callee": callee, "line": ln}
            if caller:
                entry["caller"] = caller
            calls.append(entry)

    return {
        "file": rel_path,
        "language": "javascript",
        "functions": functions,
        "classes": classes,
        "imports": imports,
        "calls": calls,
        "lines": len(lines),
    }


# ── Ruby Analyzer (regex-based) ──

_RB_CLASS = re.compile(r"^\s*class\s+(\w+)(?:\s*<\s*([\w:]+))?", re.MULTILINE)
_RB_MODULE = re.compile(r"^\s*module\s+([\w:]+)", re.MULTILINE)
_RB_DEF = re.compile(r"^\s*def\s+(self\.)?(\w+[?!=]?)\s*(?:\(([^)]*)\))?", re.MULTILINE)
_RB_REQUIRE = re.compile(r"^\s*require(?:_relative)?\s+['\"]([^'\"]+)['\"]", re.MULTILINE)
_RB_INCLUDE = re.compile(r"^\s*(?:include|extend|prepend)\s+([\w:]+)", re.MULTILINE)
_RB_CALL = re.compile(r"(\w+(?:\.\w+)*)\s*[\(]", re.MULTILINE)
_RB_HAS = re.compile(r"^\s*(has_many|has_one|belongs_to|has_and_belongs_to_many)\s+:(\w+)", re.MULTILINE)
_RB_SCOPE = re.compile(r"^\s*scope\s+:(\w+)", re.MULTILINE)
_RB_BEFORE = re.compile(r"^\s*(before_action|after_action|around_action|before_filter|after_filter)\s+:(\w+)", re.MULTILINE)


def analyze_rb(filepath: str, rel_path: str) -> dict:
    """Line-by-line Ruby analyzer that tracks method scope for call graph edges."""
    try:
        with open(filepath, "r", errors="replace") as f:
            source = f.read()
    except Exception:
        return {"file": rel_path, "language": "ruby", "functions": [], "classes": [], "imports": [], "calls": [], "lines": 0}

    source_lines = source.split("\n")
    functions = []
    classes = []
    imports = []
    calls = []
    associations = []

    # Track nesting via def/end balance
    current_class: str | None = None
    current_method: str | None = None
    class_stack: list[str] = []
    method_stack: list[str] = []
    # Simple indent/end tracker for scope
    scope_stack: list[str] = []  # "class", "module", "def", "block"

    noise = {"if", "unless", "while", "until", "case", "when", "return", "raise",
             "puts", "print", "require", "require_relative", "include", "extend",
             "prepend", "attr_accessor", "attr_reader", "attr_writer", "rescue",
             "lambda", "proc", "loop", "begin", "ensure", "yield", "super"}

    re_end = re.compile(r"^\s*end\b")
    re_block_open = re.compile(r"\b(do)\s*(\|[^|]*\|)?\s*$")
    # Inline block openers that also need end tracking
    re_inline_scope = re.compile(r"^\s*(if|unless|while|until|case|begin)\b(?!.*\bthen\b.*\bend\b)")

    for lineno, line in enumerate(source_lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        # ── Class / Module ──
        m = _RB_CLASS.match(line)
        if m:
            current_class = m.group(1)
            class_stack.append(current_class)
            scope_stack.append("class")
            classes.append({
                "name": m.group(1),
                "bases": [m.group(2)] if m.group(2) else [],
                "line": lineno,
                "methods": [],
                "associations": [],
                "scopes": [],
            })
            continue

        m = _RB_MODULE.match(line)
        if m:
            current_class = m.group(1)
            class_stack.append(current_class)
            scope_stack.append("module")
            continue

        # ── Method def ──
        m = _RB_DEF.match(line)
        if m:
            is_class_method = bool(m.group(1))
            name = m.group(2)
            params_raw = m.group(3) or ""
            qualified = f"{current_class}.{name}" if current_class else name
            current_method = qualified
            method_stack.append(qualified)
            scope_stack.append("def")
            # Strip default values from params to avoid leaking secrets
            clean_params = ", ".join(
                p.split("=")[0].strip() for p in params_raw.split(",") if p.strip()
            ) if params_raw.strip() else ""
            functions.append({
                "name": name,
                "qualified_name": qualified,
                "line": lineno,
                "params": clean_params,
                "is_class_method": is_class_method,
                "class": current_class,
            })
            for c in classes:
                if c["name"] == current_class:
                    c["methods"].append(name)
                    break
            # Don't continue — the line might also contain a call

        # ── end ──
        if re_end.match(line):
            if scope_stack:
                popped = scope_stack.pop()
                if popped == "def":
                    if method_stack:
                        method_stack.pop()
                    current_method = method_stack[-1] if method_stack else None
                elif popped in ("class", "module"):
                    if class_stack:
                        class_stack.pop()
                    current_class = class_stack[-1] if class_stack else None
            continue

        # ── Track block/if/etc scope for end matching ──
        if re_block_open.search(line) and not _RB_DEF.match(line):
            scope_stack.append("block")
        elif re_inline_scope.match(line):
            # Only count if this isn't a single-line if/unless (modifier form)
            # Modifier form: `return x if cond` — no end needed
            # Block form: `if cond` on its own line — needs end
            if not re.match(r"^\s*(if|unless)\b", stripped):
                pass  # modifier form, no scope push
            else:
                scope_stack.append("block")

        # ── Requires / Includes ──
        m = _RB_REQUIRE.match(line)
        if m:
            imports.append({"module": m.group(1), "line": lineno})
            continue

        m = _RB_INCLUDE.match(line)
        if m:
            imports.append({"module": m.group(1), "line": lineno, "kind": "mixin"})
            continue

        # ── Rails associations ──
        m = _RB_HAS.match(line)
        if m:
            associations.append({"type": m.group(1), "name": m.group(2), "line": lineno})
            for c in classes:
                if c["name"] == current_class and "associations" in c:
                    c["associations"].append(f"{m.group(1)} :{m.group(2)}")
                    break
            continue

        # ── Scopes ──
        m = _RB_SCOPE.match(line)
        if m:
            for c in classes:
                if c["name"] == current_class and "scopes" in c:
                    c["scopes"].append(m.group(1))
                    break
            continue

        # ── Callbacks (class-level calls) ──
        m = _RB_BEFORE.match(line)
        if m:
            caller_ctx = current_class or rel_path
            calls.append({"caller": caller_ctx, "callee": m.group(2), "line": lineno, "kind": m.group(1)})
            continue

        # ── Method calls — attributed to current_method ──
        for m in _RB_CALL.finditer(line):
            callee = m.group(1)
            base = callee.split(".")[0]
            if base not in noise and len(callee) < 80:
                caller_ctx = current_method or current_class or rel_path
                calls.append({"caller": caller_ctx, "callee": callee, "line": lineno})

    return {
        "file": rel_path,
        "language": "ruby",
        "functions": functions,
        "classes": classes,
        "imports": imports,
        "calls": calls,
        "associations": associations,
        "lines": len(source_lines),
    }


# ── Project Scanner ──

def scan_project(project_dir: str, excludes: set[str] = None) -> dict:
    root = Path(project_dir).resolve()
    excludes = excludes or DEFAULT_EXCLUDES
    files: list[dict] = []
    all_calls = []
    all_imports = []
    stats = {"py_files": 0, "js_files": 0, "rb_files": 0, "total_lines": 0, "total_functions": 0, "total_classes": 0}

    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in excludes]
        for fname in sorted(filenames):
            fpath = Path(dirpath) / fname
            ext = fpath.suffix.lower()
            if ext not in ALL_EXTS:
                continue
            rel = str(fpath.relative_to(root))

            if ext in PY_EXTS:
                result = PyAnalyzer(str(fpath), rel).analyze()
                stats["py_files"] += 1
            elif ext in JS_EXTS:
                result = analyze_js(str(fpath), rel)
                stats["js_files"] += 1
            elif ext in RB_EXTS:
                result = analyze_rb(str(fpath), rel)
                stats["rb_files"] += 1
            else:
                continue

            stats["total_lines"] += result.get("lines", 0)
            stats["total_functions"] += len(result.get("functions", []))
            stats["total_classes"] += len(result.get("classes", []))

            for c in result.get("calls", []):
                c["file"] = rel
            all_calls.extend(result.get("calls", []))

            for imp in result.get("imports", []):
                imp["file"] = rel
            all_imports.extend(result.get("imports", []))

            files.append(result)

    # Build call graph index
    call_graph = defaultdict(list)  # caller -> [callee]
    reverse_graph = defaultdict(list)  # callee -> [caller]
    for c in all_calls:
        caller = c.get("caller", c.get("file", "?"))
        callee = c["callee"]
        call_graph[caller].append({"callee": callee, "file": c["file"], "line": c["line"]})
        reverse_graph[callee].append({"caller": caller, "file": c["file"], "line": c["line"]})

    # Build import graph
    import_graph = defaultdict(list)
    for imp in all_imports:
        import_graph[imp["file"]].append(imp["module"])

    # Hash for cache invalidation
    h = hashlib.md5()
    for f in files:
        h.update(f["file"].encode())
        h.update(str(f.get("lines", 0)).encode())
    fingerprint = h.hexdigest()[:12]

    return {
        "project": str(root),
        "fingerprint": fingerprint,
        "stats": stats,
        "files": files,
        "call_graph": dict(call_graph),
        "reverse_graph": dict(reverse_graph),
        "import_graph": dict(import_graph),
    }


# ── Query Engine ──

def _graph_lookup(graph: dict, name: str) -> list:
    """Look up a name in the call/reverse graph with fuzzy matching.

    Priority: exact match → unqualified match → case-insensitive suffix match.
    Merges results from all matching keys.
    """
    # 1. Exact match
    if name in graph:
        return graph[name]

    # 2. Try unqualified: "Offer.validate_conditions" → also check "validate_conditions"
    short = name.split(".")[-1] if "." in name else None
    results = []

    # 3. Collect all matching keys (case-insensitive, suffix match)
    name_lower = name.lower()
    short_lower = short.lower() if short else None
    for key, values in graph.items():
        key_lower = key.lower()
        if key_lower == name_lower:
            results.extend(values)
        elif short_lower and key_lower == short_lower:
            results.extend(values)
        elif key_lower.endswith(f".{name_lower}") or (short_lower and key_lower.endswith(f".{short_lower}")):
            results.extend(values)

    # Deduplicate by (caller/callee + file + line)
    seen = set()
    deduped = []
    for r in results:
        key = (r.get("caller", r.get("callee", "")), r.get("file", ""), r.get("line", 0))
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    return deduped


def query(cache: dict, args: list[str]) -> Any:
    cmd = args[0] if args else "stats"

    if cmd == "stats":
        s = cache["stats"]
        s["files"] = len(cache["files"])
        s["fingerprint"] = cache["fingerprint"]
        return s

    if cmd == "functions":
        funcs = []
        for f in cache["files"]:
            for fn in f.get("functions", []):
                funcs.append({"name": fn.get("qualified_name", fn["name"]), "file": f["file"], "line": fn["line"]})
        return sorted(funcs, key=lambda x: x["name"])

    if cmd == "classes":
        cls = []
        for f in cache["files"]:
            for c in f.get("classes", []):
                cls.append({"name": c["name"], "bases": c.get("bases", []), "file": f["file"], "line": c["line"], "methods": c.get("methods", [])})
        return sorted(cls, key=lambda x: x["name"])

    if cmd == "calls" and len(args) > 1:
        name = args[1]
        # What does `name` call? Try exact, then fuzzy.
        return _graph_lookup(cache["call_graph"], name)

    if cmd == "callers" and len(args) > 1:
        name = args[1]
        # Who calls `name`? Try exact, then fuzzy.
        return _graph_lookup(cache["reverse_graph"], name)

    if cmd == "file" and len(args) > 1:
        target = args[1]
        for f in cache["files"]:
            if f["file"] == target or f["file"].endswith(target):
                return f
        return {"error": f"file not found: {target}"}

    if cmd == "imports":
        return cache["import_graph"]

    if cmd == "search" and len(args) > 1:
        pattern = args[1].lower()
        results = []
        for f in cache["files"]:
            for fn in f.get("functions", []):
                if pattern in fn.get("qualified_name", fn["name"]).lower():
                    results.append({"name": fn.get("qualified_name", fn["name"]), "file": f["file"], "line": fn["line"], "kind": "function"})
            for c in f.get("classes", []):
                if pattern in c["name"].lower():
                    results.append({"name": c["name"], "file": f["file"], "line": c["line"], "kind": "class"})
        return results

    return {"error": f"unknown query: {cmd}", "available": ["stats", "functions", "classes", "calls <name>", "callers <name>", "file <path>", "imports", "search <pattern>"]}


# ── Main ──

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)

    project_dir = args[0]
    excludes = set(DEFAULT_EXCLUDES)

    # Parse flags
    output_file = None
    query_args = None
    i = 1
    while i < len(args):
        if args[i] == "--output" and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        elif args[i] == "--exclude" and i + 1 < len(args):
            excludes.add(args[i + 1])
            i += 2
        elif args[i] == "--query":
            query_args = args[i + 1:]
            break
        else:
            i += 1

    # Check for cached data
    if not output_file:
        output_file = os.path.join(project_dir, ".code-graph.json")

    if query_args and os.path.exists(output_file):
        with open(output_file) as f:
            cache = json.load(f)
        result = query(cache, query_args)
        print(json.dumps(result, indent=2))
        return

    # Build or rebuild
    cache = scan_project(project_dir, excludes)

    with open(output_file, "w") as f:
        json.dump(cache, f, indent=2)

    if query_args:
        result = query(cache, query_args)
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(cache["stats"], indent=2))
        print(f"\nCache written to {output_file}")


if __name__ == "__main__":
    main()
