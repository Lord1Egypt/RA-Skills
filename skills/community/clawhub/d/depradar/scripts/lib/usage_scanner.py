"""Codebase usage scanner for /depradar.

Scans a project directory for usages of breaking-change symbols.
- Python files: AST-based detection (high confidence)
- JS/TS files:  import-tracking regex with package context (medium-high confidence)
               True AST via Node.js if available (high confidence)
- Other files:  grep-based detection (low confidence)
"""

from __future__ import annotations

import ast
import json as _json_ast
import os
import re
import subprocess as _subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

sys.path.insert(0, str(Path(__file__).parent))
from schema import BreakingChange, ImpactLocation


# ── Constants ─────────────────────────────────────────────────────────────────

SCAN_EXTENSIONS: Dict[str, List[str]] = {
    "npm":   [".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs"],
    "pypi":  [".py"],
    "cargo": [".rs"],
    "maven": [".java", ".kt"],
    "gem":   [".rb"],
    "go":    [".go"],
}

SKIP_DIRS: Set[str] = {
    "node_modules", ".git", "__pycache__", ".venv", "venv", "env",
    "dist", "build", "target", ".cache", ".next", ".nuxt",
    "vendor", "third_party", ".tox", ".mypy_cache", ".pytest_cache",
    # Asset/public directories — contain vendor bundles, not developer code
    "public", "static", "assets", "wwwroot", "media",
    "static_files", "staticfiles",
}

# Minified / bundled file suffixes — always vendor, never scan
_SKIP_MINIFIED_SUFFIXES: Set[str] = {
    ".min.js", ".min.css", ".min.mjs",
    ".bundle.js", ".chunk.js",
}

def _is_minified(path: str) -> bool:
    """Return True if the file looks like a minified or vendor bundle."""
    name = os.path.basename(path).lower()
    return any(name.endswith(sfx) for sfx in _SKIP_MINIFIED_SUFFIXES)


# Generic symbol names that appear in unrelated code — only report at HIGH/MED confidence
_GENERIC_SYMBOLS: Set[str] = {
    # Common JS/TS class/type names used everywhere
    "Client", "Config", "Configuration", "Request", "Response",
    "Handler", "Manager", "Service", "Provider", "Factory",
    "Error", "Event", "Options", "Context", "Session",
    "Logger", "Server", "Router", "Middleware", "Controller",
    # Common Python names
    "client", "config", "request", "response",
    "handler", "manager", "service", "session",
    "logger", "server",
}

# Hard cap per file — skip files larger than this to avoid hanging
_MAX_FILE_BYTES = 500 * 1024   # 500 KB

# Per-file scan timeout
_PER_FILE_TIMEOUT = 5.0        # seconds


# ── Public API ────────────────────────────────────────────────────────────────

def scan_project(
    breaking_changes: List[BreakingChange],
    project_root: str,
    ecosystem: str = "npm",
    timeout_seconds: int = 30,
    package_name: str = "",
) -> Tuple[Dict[str, List[ImpactLocation]], List[str]]:
    """For each breaking change symbol, find all files that use it.

    Returns (result_dict, skipped_files_list)
    result_dict:    {symbol: [ImpactLocation, ...]}
    skipped_files:  list of "path: reason" strings for files that were skipped

    Strategy:
    1. Python files:  AST-based detection (high confidence)
    2. JS/TS files:   import-tracking regex + optional Node.js AST (high confidence)
    3. Other files:   grep-based (low confidence)
    """
    result: Dict[str, List[ImpactLocation]] = {}
    skipped: List[str] = []
    symbols = [bc.symbol for bc in breaking_changes if bc.symbol]
    if not symbols:
        return result, skipped

    extensions = SCAN_EXTENSIONS.get(ecosystem, [])
    if not extensions:
        # Fall back to all known extensions
        all_exts: List[str] = []
        for exts in SCAN_EXTENSIONS.values():
            all_exts.extend(exts)
        extensions = list(set(all_exts))

    files = _walk_files(project_root, extensions)

    # Timeout support via threading.Event
    timed_out = threading.Event()

    def _set_timeout() -> None:
        timed_out.set()

    timer = threading.Timer(timeout_seconds, _set_timeout)
    timer.daemon = True
    timer.start()

    try:
        for file_path in files:
            if timed_out.is_set():
                skipped.append(f"{file_path}: global timeout ({timeout_seconds}s) reached")
                break
            # Skip minified/vendor bundles
            if _is_minified(file_path):
                skipped.append(f"{file_path}: minified/vendor file")
                continue
            # Per-file size limit
            try:
                file_size = Path(file_path).stat().st_size
            except OSError:
                skipped.append(f"{file_path}: could not stat file")
                continue
            if file_size > _MAX_FILE_BYTES:
                skipped.append(
                    f"{file_path}: too large ({file_size // 1024}KB > "
                    f"{_MAX_FILE_BYTES // 1024}KB limit)"
                )
                continue
            # Per-file timeout using a single-worker executor
            try:
                with ThreadPoolExecutor(max_workers=1) as single_worker:
                    fut = single_worker.submit(
                        _scan_file, file_path, symbols, package_name
                    )
                    try:
                        file_results = fut.result(timeout=_PER_FILE_TIMEOUT)
                    except FuturesTimeoutError:
                        skipped.append(f"{file_path}: per-file timeout ({_PER_FILE_TIMEOUT}s)")
                        continue
            except PermissionError:
                skipped.append(f"{file_path}: permission denied")
                continue
            except UnicodeDecodeError:
                skipped.append(f"{file_path}: encoding error")
                continue
            except Exception as exc:
                skipped.append(f"{file_path}: {type(exc).__name__}: {exc}")
                continue
            for sym, locs in file_results.items():
                result.setdefault(sym, []).extend(locs)
    finally:
        timer.cancel()

    return result, skipped


def scan_python_file(
    file_path: str,
    symbols: List[str],
) -> Dict[str, List[ImpactLocation]]:
    """AST-based scan of a Python file. Returns {symbol: [locations]}."""
    result: Dict[str, List[ImpactLocation]] = {}
    if not symbols:
        return result

    try:
        source = Path(file_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return result

    try:
        tree = ast.parse(source, filename=file_path)
    except SyntaxError:
        # Fall back to grep-based scan
        return scan_file_generic(file_path, symbols)

    lines = source.splitlines()

    # Build a set of base symbols for quick lookup
    base_symbols: Dict[str, str] = {_extract_base_symbol(s): s for s in symbols}

    class _Visitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.hits: Dict[str, List[ImpactLocation]] = {}

        def _record(self, sym_orig: str, lineno: int) -> None:
            loc_text = lines[lineno - 1].strip() if 0 < lineno <= len(lines) else ""
            self.hits.setdefault(sym_orig, []).append(
                ImpactLocation(
                    file_path=file_path,
                    line_number=lineno,
                    usage_text=loc_text,
                    detection_method="ast",
                )
            )

        def visit_Import(self, node: ast.Import) -> None:
            for alias in node.names:
                for sym, orig in base_symbols.items():
                    if sym == alias.name or alias.name.endswith(f".{sym}"):
                        self._record(orig, node.lineno)
            self.generic_visit(node)

        def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
            module = node.module or ""
            for alias in node.names:
                full = f"{module}.{alias.name}" if module else alias.name
                for sym, orig in base_symbols.items():
                    # Exact name match or dotted-path match — avoid substring false positives.
                    # e.g. "stripe" must NOT match "mystripe" or "stripe_utils"
                    if (sym == alias.name
                            or full == sym
                            or full.endswith("." + sym)
                            or full.startswith(sym + ".")):
                        self._record(orig, node.lineno)
            self.generic_visit(node)

        def visit_Attribute(self, node: ast.Attribute) -> None:
            for sym, orig in base_symbols.items():
                if node.attr == sym or node.attr == _extract_base_symbol(sym):
                    self._record(orig, node.lineno)
            self.generic_visit(node)

        def visit_Call(self, node: ast.Call) -> None:
            func = node.func
            # Direct name call: foo()
            if isinstance(func, ast.Name):
                for sym, orig in base_symbols.items():
                    if func.id == sym or func.id == _extract_base_symbol(sym):
                        self._record(orig, node.lineno)
            # Attribute call: obj.method()
            elif isinstance(func, ast.Attribute):
                for sym, orig in base_symbols.items():
                    base = _extract_base_symbol(sym)
                    if func.attr == base or func.attr == sym:
                        self._record(orig, node.lineno)
            self.generic_visit(node)

        def visit_Name(self, node: ast.Name) -> None:
            for sym, orig in base_symbols.items():
                if node.id == sym or node.id == _extract_base_symbol(sym):
                    self._record(orig, node.lineno)
            self.generic_visit(node)

    visitor = _Visitor()
    visitor.visit(tree)
    return visitor.hits


def scan_js_ts_file(
    file_path: str,
    symbols: List[str],
    package_name: str = "",
) -> Dict[str, List[ImpactLocation]]:
    """Import-tracking regex scan of JS/TS file.

    Confidence levels:
    - "high"  = symbol accessed via confirmed package alias (alias.symbol)
    - "med"   = symbol from confirmed destructuring import
    - "low"   = bare symbol match (may be unrelated to the package)

    Returns {symbol: [locations]}.
    """
    result: Dict[str, List[ImpactLocation]] = {}
    if not symbols:
        return result

    try:
        raw_text = Path(file_path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return result

    lines = raw_text.splitlines()

    # Step 1: Remove /* */ block comments from full text before splitting
    text_no_block_comments = re.sub(r"/\*.*?\*/", "", raw_text, flags=re.DOTALL)
    clean_lines = text_no_block_comments.splitlines()
    # Pad to same length (block comment removal may change line count slightly)
    while len(clean_lines) < len(lines):
        clean_lines.append("")

    # Step 2: Extract package import aliases (how the package is imported)
    pkg = package_name or _infer_package_from_symbols(symbols)
    aliases = _extract_package_aliases(lines, pkg)

    # Step 3: Extract destructured imports from the package
    destructured = _extract_destructured_symbols(lines, pkg)

    base_symbols: Dict[str, str] = {_extract_base_symbol(s): s for s in symbols}

    for lineno, (orig_line, clean_line) in enumerate(
        zip(lines, clean_lines), start=1
    ):
        # Strip // line comment (not inside strings)
        clean = _strip_js_line_comment(clean_line)
        # Blank out string literals to avoid matching symbols inside them
        clean_no_strings = _blank_string_literals(clean)

        for base, orig in base_symbols.items():
            # HIGH confidence: alias.symbol (e.g. stripe.webhooks.constructEvent)
            matched_high = False
            for alias in aliases:
                # Match alias.base or alias.something.base
                pattern = re.escape(alias) + r"(?:\.\w+)*\." + re.escape(base) + r"\b"
                if re.search(pattern, clean_no_strings):
                    result.setdefault(orig, []).append(
                        ImpactLocation(
                            file_path=file_path,
                            line_number=lineno,
                            usage_text=orig_line.strip(),
                            detection_method="high",
                        )
                    )
                    matched_high = True
                    break
            if matched_high:
                continue

            # MEDIUM confidence: destructuring import confirmed
            if base in destructured:
                # Only match when the bare name is used as a call/access
                pattern = r"\b" + re.escape(base) + r"\s*[\(\.\,\s\;\:\[\{]"
                if re.search(pattern, clean_no_strings):
                    result.setdefault(orig, []).append(
                        ImpactLocation(
                            file_path=file_path,
                            line_number=lineno,
                            usage_text=orig_line.strip(),
                            detection_method="grep",  # "grep" maps to "med" in impact_analyzer
                        )
                    )
                    continue

            # LOW confidence: bare symbol match (fallback)
            # Generic symbol names (Client, Config, Request, etc.) are too common to match
            # without a confirmed import — skip LOW confidence matches for them.
            if base in _GENERIC_SYMBOLS:
                continue
            # Import/require patterns are checked on comment-stripped line (strings NOT blanked)
            # because 'import foo from "pkg"' has the symbol inside a string.
            import_pattern = (
                r"(?:import\s+.*?\b" + re.escape(base) + r"\b"
                r"|require\(['\"].*?" + re.escape(base) + r".*?['\"])"
            )
            # Bare symbol is checked on string-blanked line to avoid false positives
            bare_pattern = r"\b" + re.escape(base) + r"\s*[\(\.\,\s\;\:\[\{]"
            if re.search(import_pattern, clean, re.IGNORECASE) or \
               re.search(bare_pattern, clean_no_strings):
                result.setdefault(orig, []).append(
                    ImpactLocation(
                        file_path=file_path,
                        line_number=lineno,
                        usage_text=orig_line.strip(),
                        detection_method="grep",
                    )
                )

    return result


def scan_file_generic(
    file_path: str,
    symbols: List[str],
) -> Dict[str, List[ImpactLocation]]:
    """Generic grep-based scan. Returns {symbol: [locations]}."""
    result: Dict[str, List[ImpactLocation]] = {}
    if not symbols:
        return result

    try:
        lines = Path(file_path).read_text(
            encoding="utf-8", errors="replace"
        ).splitlines()
    except OSError:
        return result

    base_symbols: Dict[str, str] = {_extract_base_symbol(s): s for s in symbols}

    for lineno, line in enumerate(lines, start=1):
        for base, orig in base_symbols.items():
            if re.search(r"\b" + re.escape(base) + r"\b", line):
                result.setdefault(orig, []).append(
                    ImpactLocation(
                        file_path=file_path,
                        line_number=lineno,
                        usage_text=line.strip(),
                        detection_method="grep",
                    )
                )

    return result


# ── JS/TS import helpers ──────────────────────────────────────────────────────

def _extract_package_aliases(lines: List[str], package: str) -> List[str]:
    """Find all local aliases the package is imported under.

    Returns e.g. ['stripe', 'Stripe'] for `import stripe from 'stripe'`
    Falls back to [package] if no import found.

    Handles:
    - import stripe from 'stripe'
    - import * as stripe from 'stripe'
    - const stripe = require('stripe')
    - import type stripe from 'stripe'
    - const mod = await import('stripe')   (dynamic import)
    """
    if not package:
        return []
    aliases: List[str] = []
    pkg_re = re.escape(package)
    for line in lines:
        stripped = line.strip()
        # import stripe from 'stripe'
        m = re.match(r"import\s+(\w+)\s+from\s+['\"]" + pkg_re + r"['\"]", stripped)
        if m:
            aliases.append(m.group(1))
            continue
        # import * as stripe from 'stripe'
        m = re.match(r"import\s+\*\s+as\s+(\w+)\s+from\s+['\"]" + pkg_re + r"['\"]", stripped)
        if m:
            aliases.append(m.group(1))
            continue
        # const stripe = require('stripe')
        m = re.match(
            r"(?:const|let|var)\s+(\w+)\s*=\s*require\(['\"]" + pkg_re + r"['\"]",
            stripped
        )
        if m:
            aliases.append(m.group(1))
            continue
        # import type stripe from 'stripe'
        m = re.match(
            r"import\s+type\s+(\w+)\s+from\s+['\"]" + pkg_re + r"['\"]", stripped
        )
        if m:
            aliases.append(m.group(1))
            continue
        # Dynamic import: const mod = await import('stripe')
        m = re.match(
            r"(?:const|let|var)\s+(\w+)\s*=\s*(?:await\s+)?import\s*\(\s*['\"]" + pkg_re + r"['\"]",
            stripped
        )
        if m:
            aliases.append(m.group(1))
    # Always include the package name itself as a fallback alias
    if package and package not in aliases:
        aliases.append(package)
    return aliases or [package]


def _extract_destructured_symbols(lines: List[str], package: str) -> Set[str]:
    """Find all symbol names destructured from the package.

    Handles:
    - import { constructEvent } from 'stripe'
    - import { webhooks as wh } from 'stripe'  -> wh
    - const { constructEvent } = require('stripe')
    - const { constructEvent } = await import('stripe')  (dynamic import)
    """
    result: Set[str] = set()
    if not package:
        return result
    pkg_re = re.escape(package)

    def _parse_destructured(group: str) -> None:
        for item in group.split(","):
            item = item.strip()
            if " as " in item:
                _, alias = item.split(" as ", 1)
                result.add(alias.strip())
            elif item:
                result.add(item.strip())

    for line in lines:
        stripped = line.strip()
        # import { a, b as c } from 'pkg'
        m = re.search(
            r"import\s*(?:type\s*)?\{([^}]+)\}\s*from\s*['\"]" + pkg_re + r"['\"]", stripped
        )
        if m:
            _parse_destructured(m.group(1))
            continue
        # const { a, b } = require('pkg')
        m = re.search(
            r"(?:const|let|var)\s*\{([^}]+)\}\s*=\s*require\(['\"]" + pkg_re + r"['\"]",
            stripped
        )
        if m:
            _parse_destructured(m.group(1))
            continue
        # const { a, b } = await import('pkg')  — dynamic named import
        m = re.search(
            r"(?:const|let|var)\s*\{([^}]+)\}\s*=\s*(?:await\s+)?import\s*\(\s*['\"]"
            + pkg_re + r"['\"]",
            stripped
        )
        if m:
            _parse_destructured(m.group(1))
    return result


def _strip_js_line_comment(line: str) -> str:
    """Remove // comment from line, respecting string boundaries."""
    in_str = False
    str_char = ""
    i = 0
    while i < len(line):
        ch = line[i]
        if not in_str:
            if ch in ('"', "'", "`"):
                in_str = True
                str_char = ch
            elif ch == "/" and i + 1 < len(line) and line[i + 1] == "/":
                return line[:i]
        else:
            if ch == str_char and (i == 0 or line[i - 1] != "\\"):
                in_str = False
        i += 1
    return line


def _blank_string_literals(line: str) -> str:
    """Replace string literal contents with spaces to avoid false symbol matches."""
    # Replace 'content', "content", and `content` with empty quoted strings
    result = re.sub(r'"(?:[^"\\]|\\.)*"', '""', line)
    result = re.sub(r"'(?:[^'\\]|\\.)*'", "''", result)
    result = re.sub(r"`(?:[^`\\]|\\.)*`", "``", result)
    return result


def _infer_package_from_symbols(symbols: List[str]) -> str:
    """Infer the package name from dot-notation symbols like 'stripe.webhooks.X'."""
    for sym in symbols:
        parts = sym.split(".")
        if len(parts) > 1 and parts[0]:
            return parts[0]
    return ""


# ── Internal helpers ──────────────────────────────────────────────────────────

def _walk_files(root: str, extensions: List[str]) -> List[str]:
    """Walk directory tree, skip SKIP_DIRS, return matching file paths."""
    matched: List[str] = []
    ext_set = set(extensions)

    for dirpath, dirnames, filenames in os.walk(root, topdown=True):
        # Prune skipped directories in-place (modifies dirnames to skip subtrees)
        dirnames[:] = [
            d for d in dirnames
            if d not in SKIP_DIRS and not d.startswith(".")
        ]
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            if ext in ext_set:
                matched.append(os.path.join(dirpath, filename))

    return matched


def _extract_base_symbol(full_symbol: str) -> str:
    """Extract the most specific name.

    'stripe.webhooks.constructEvent' -> 'constructEvent'
    'WebhookSignature.verify'        -> 'verify'
    'constructEvent'                 -> 'constructEvent'
    """
    if not full_symbol:
        return full_symbol
    # Split on dot, colon, or ::
    parts = re.split(r"[.:]", full_symbol)
    # Strip trailing parentheses
    return parts[-1].rstrip("()").strip()


# ── Node.js AST integration ───────────────────────────────────────────────────

_JS_AST_HELPER = Path(__file__).parent / "js_ast_helper.js"
_node_checked: Optional[bool] = None


def _check_node() -> bool:
    """Return True if node is on PATH (cached after first call)."""
    global _node_checked
    if _node_checked is None:
        import shutil
        _node_checked = shutil.which("node") is not None
    return _node_checked


# Maps js_ast_helper detection_method values → ImpactLocation confidence strings
_AST_METHOD_TO_CONF: Dict[str, str] = {
    "high":        "high",
    "ast":         "high",
    "re-export":   "med",
    "type-import": "low",
    "grep":        "low",
}


def scan_js_ts_ast(
    file_path: str,
    symbols: List[str],
    package: str,
) -> Tuple[Dict[str, List[ImpactLocation]], str]:
    """Run js_ast_helper.js for real AST-based JS/TS impact detection.

    Returns (results_dict, error_msg).
    On any failure returns ({}, error_msg) so caller can fall back to regex.
    """
    if not _check_node() or not _JS_AST_HELPER.exists():
        return {}, "node unavailable"

    payload = _json_ast.dumps({"file": file_path, "symbols": symbols, "package": package})
    try:
        proc = _subprocess.run(
            ["node", str(_JS_AST_HELPER)],
            input=payload,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if proc.returncode != 0:
            return {}, (proc.stderr or "").strip()[:200]
        raw = _json_ast.loads(proc.stdout)
    except _subprocess.TimeoutExpired:
        return {}, "node helper timeout (10s)"
    except Exception as exc:
        return {}, str(exc)

    results: Dict[str, List[ImpactLocation]] = {}
    for sym, hits in raw.items():
        locs = [
            ImpactLocation(
                file_path=h["file_path"],
                line_number=h["line_number"],
                usage_text=h.get("usage_text", ""),
                detection_method=_AST_METHOD_TO_CONF.get(
                    h.get("detection_method", ""), "med"
                ),
            )
            for h in hits
        ]
        if locs:
            results[sym] = locs
    return results, ""


# ── Internal dispatcher ───────────────────────────────────────────────────────

_JS_TS_EXTENSIONS = {".js", ".ts", ".jsx", ".tsx", ".mjs", ".cjs"}
_PYTHON_EXTENSIONS = {".py"}


def _scan_file(
    file_path: str,
    symbols: List[str],
    package_name: str = "",
) -> Dict[str, List[ImpactLocation]]:
    """Dispatch to the appropriate scanner based on file extension."""
    _, ext = os.path.splitext(file_path)
    if ext in _PYTHON_EXTENSIONS:
        return scan_python_file(file_path, symbols)
    if ext in _JS_TS_EXTENSIONS:
        # Try real AST first (Node.js); fall back to regex if unavailable or no results
        ast_results, _ = scan_js_ts_ast(file_path, symbols, package_name)
        if ast_results:
            return ast_results
        return scan_js_ts_file(file_path, symbols, package_name)
    return scan_file_generic(file_path, symbols)
