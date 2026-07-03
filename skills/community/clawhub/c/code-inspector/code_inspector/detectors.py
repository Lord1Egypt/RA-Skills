"""Signature-based detection of AI-generated code smells."""

import re
import os
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class CodeSmell:
    """A detected code quality issue."""
    name: str
    severity: str          # "critical", "warning", "info"
    line_number: int
    description: str
    snippet: str
    fix_suggestion: str


@dataclass
class InspectResult:
    """Result of inspecting a single file."""
    file_path: str
    language: str
    smells: List[CodeSmell] = field(default_factory=list)
    quality_score: int = 100
    summary: str = ""


SEVERITY_WEIGHTS = {
    "truncation": 20,
    "thinking_skip": 15,
    "hardcoded_secret": 25,
    "missing_error_handling": 10,
    "todo_bomb": 8,
    "copy_paste": 12,
    "incomplete_import": 10,
    "bare_except": 7,
}


def detect_truncation(code: str) -> List[CodeSmell]:
    """Detect truncated code patterns (// ..., # ..., # rest of, etc.)."""
    smells = []
    lines = code.split("\n")
    patterns = [
        (r"//\s*\.{2,}\s*$", "truncation", "JavaScript/TS truncation comment (// ...)"),
        (r"#\s*\.{2,}\s*$", "truncation", "Python truncation comment (# ...)"),
        (r"//\s*rest\s+of\s+(the\s+)?(code|implementation)", "truncation", "JavaScript 'rest of code' placeholder"),
        (r"#\s*rest\s+of\s+(the\s+)?(code|implementation)", "truncation", "Python 'rest of code' placeholder"),
        (r"//\s*remaining\s+code", "truncation", "JavaScript 'remaining code' placeholder"),
        (r"#\s*remaining\s+code", "truncation", "Python 'remaining code' placeholder"),
        (r"#\s*\.{2,}\s+\(rest\s+of", "truncation", "Python truncation with rest note"),
        (r"//\s*\.{2,}\s+\(rest\s+of", "truncation", "JS truncation with rest note"),
        (r"#\s*\.{2,}\s*#", "truncation", "Python inline truncation (# ... #)"),
        (r"<!--\s*\.{2,}\s*-->", "truncation", "HTML truncation comment"),
    ]
    for i, line in enumerate(lines, start=1):
        for pattern, name, desc in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                smells.append(CodeSmell(
                    name=name,
                    severity="critical",
                    line_number=i,
                    description=desc,
                    snippet=line.strip()[:100],
                    fix_suggestion="Remove truncation marker and complete the implementation."
                ))
                break
    return smells


def detect_thinking_skip(code: str) -> List[CodeSmell]:
    """Detect LLM thinking/planning language leaked into comments."""
    smells = []
    lines = code.split("\n")
    thinking_patterns = [
        r"(?://|#)\s*Let\s+me\s",
        r"(?://|#)\s*I\s+need\s+to\s",
        r"(?://|#)\s*First,\s",
        r"(?://|#)\s*Now,\s",
        r"(?://|#)\s*Then,\s",
        r"(?://|#)\s*Finally,\s",
        r"(?://|#)\s*Next,\s",
        r"(?://|#)\s*We\s+need\s+to\s",
        r"(?://|#)\s*Let\'s\s",
        r"(?://|#)\s*I\'ll\s",
        r"(?://|#)\s*We\'ll\s",
    ]
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not (stripped.startswith("//") or stripped.startswith("#")):
            continue
        for pattern in thinking_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                smells.append(CodeSmell(
                    name="thinking_skip",
                    severity="warning",
                    line_number=i,
                    description="LLM thinking/planning text leaked into comment",
                    snippet=stripped[:100],
                    fix_suggestion="Remove the thinking commentary; keep only documentation-relevant comments."
                ))
                break
    return smells


def detect_hardcoded_secrets(code: str) -> List[CodeSmell]:
    """Detect hardcoded secrets like API keys, tokens, passwords."""
    smells = []
    lines = code.split("\n")
    secret_patterns = [
        (r"(?:api[_-]?key|apikey|secret[_-]?key)\s*[:=]\s*['\"]([^'\"]{8,})['\"]", "hardcoded_secret", "API key or secret key hardcoded"),
        (r"(?:password|passwd|pwd)\s*[:=]\s*['\"]([^'\"]{3,})['\"]", "hardcoded_secret", "Password hardcoded in source"),
        (r"(?:token|auth[_-]?token|access[_-]?token)\s*[:=]\s*['\"]([^'\"]{8,})['\"]", "hardcoded_secret", "Auth token hardcoded"),
        (r"['\"]sk-[a-zA-Z0-9]{20,}['\"]", "hardcoded_secret", "OpenAI-style API key (sk-...)"),
        (r"(?:DATABASE_URL|DB_URL|MONGO_URI)\s*=\s*['\"]([^'\"]+)['\"]", "hardcoded_secret", "Database connection string hardcoded"),
        (r"(?:private[_-]?key|PRIVATE_KEY)\s*[:=]\s*['\"]", "hardcoded_secret", "Private key hardcoded"),
        (r"(?:secret|SECRET)\s*[:=]\s*['\"]([^'\"]{6,})['\"]", "hardcoded_secret", "Generic secret value hardcoded"),
    ]
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith("//") or stripped.startswith("#"):
            continue
        for pattern, name, desc in secret_patterns:
            m = re.search(pattern, line, re.IGNORECASE)
            if m:
                smells.append(CodeSmell(
                    name=name,
                    severity="critical",
                    line_number=i,
                    description=desc,
                    snippet=stripped[:120],
                    fix_suggestion="Use environment variables or a secrets manager instead of hardcoding credentials."
                ))
                break
    return smells


def detect_missing_error_handling(code: str) -> List[CodeSmell]:
    """Detect file/network operations without try/except blocks."""
    smells = []
    lines = code.split("\n")
    risky_patterns = [
        r"open\s*\([^)]+\)",
        r"(?:requests|urllib|http)\.(?:get|post|put|delete|patch|request)\s*\(",
        r"urllib\.request\.urlopen\s*\(",
        r"subprocess\.(?:run|call|Popen|check_output)\s*\(",
        r"socket\.(?:connect|send|recv)\s*\(",
        r"os\.(?:remove|unlink|rmdir)\s*\(",
        r"shutil\.(?:copy|move|rmtree)\s*\(",
        r"(?:fetch|axios)\s*\(\s*['\"]",   # JavaScript fetch/axios
    ]

    # Find likely function/block boundaries
    in_try_block = False
    try_depth = 0
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        # Track try/except blocks (approximate)
        if re.search(r"\btry\b\s*:", stripped):
            in_try_block = True
            try_depth += 1
        if in_try_block and re.search(r"\bexcept\b", stripped):
            try_depth -= 1
            if try_depth <= 0:
                in_try_block = False
                try_depth = 0

        if in_try_block:
            continue

        if stripped.startswith("//") or stripped.startswith("#"):
            continue

        for pattern in risky_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                smells.append(CodeSmell(
                    name="missing_error_handling",
                    severity="warning",
                    line_number=i,
                    description="Potentially risky operation without visible try/except",
                    snippet=stripped[:120],
                    fix_suggestion="Wrap this operation in a try/except (or try/catch) block to handle errors gracefully."
                ))
                break
    return smells


def detect_todo_bombs(code: str) -> List[CodeSmell]:
    """Detect excessive TODO/FIXME/HACK comments (>3 in a file)."""
    todo_pattern = re.compile(
        r"(?://|#|/\*)\s*(TODO|FIXME|HACK|XXX|OPTIMIZE|WORKAROUND)\b",
        re.IGNORECASE
    )
    lines = code.split("\n")
    todos = []
    for i, line in enumerate(lines, start=1):
        if todo_pattern.search(line):
            todos.append((i, line.strip()[:100]))

    smells = []
    if len(todos) > 3:
        for line_no, snippet in todos:
            smells.append(CodeSmell(
                name="todo_bomb",
                severity="warning",
                line_number=line_no,
                description=f"File has {len(todos)} TODO/FIXME/HACK markers (threshold: >3)",
                snippet=snippet,
                fix_suggestion="Address or triage outstanding TODOs before merging. Consider filing issues instead."
            ))
    return smells


def detect_copy_paste(code: str) -> List[CodeSmell]:
    """Detect repeated identical code blocks (>5 lines duplicated)."""
    lines = code.split("\n")
    non_empty = [(i, line) for i, line in enumerate(lines) if line.strip() and not line.strip().startswith(("//", "#"))]

    smells = []
    min_block = 5
    seen_blocks = {}

    for start_idx in range(len(non_empty) - min_block + 1):
        block_lines = tuple(non_empty[start_idx + j][1].strip() for j in range(min_block))
        block_key = "\n".join(block_lines)

        if block_key in seen_blocks:
            prev_line = seen_blocks[block_key]
            curr_line = non_empty[start_idx][0] + 1
            smells.append(CodeSmell(
                name="copy_paste",
                severity="warning",
                line_number=curr_line,
                description=f"Duplicate code block (first seen at line {prev_line})",
                snippet=block_lines[0][:100],
                fix_suggestion="Extract duplicated code into a shared function or module."
            ))
        else:
            seen_blocks[block_key] = non_empty[start_idx][0] + 1

    # Deduplicate by first occurrence
    return smells


def detect_incomplete_imports(code: str) -> List[CodeSmell]:
    """Detect usage of functions/variables that appear unimported (heuristic)."""
    smells = []
    lines = code.split("\n")

    # Known builtins and common names to exclude
    builtins_py = {
        "print", "len", "range", "int", "str", "float", "list", "dict", "set",
        "tuple", "bool", "type", "isinstance", "hasattr", "getattr", "setattr",
        "open", "enumerate", "zip", "map", "filter", "sorted", "reversed",
        "min", "max", "sum", "any", "all", "abs", "round", "input", "id",
        "super", "Exception", "ValueError", "TypeError", "KeyError", "None",
        "True", "False", "self", "cls", "object", "classmethod", "staticmethod",
        "property", "iter", "next", "__init__", "__name__", "__main__",
    }

    builtins_js = {
        "console", "window", "document", "Math", "JSON", "Array", "Object",
        "String", "Number", "Boolean", "Date", "RegExp", "Error", "Promise",
        "fetch", "setTimeout", "setInterval", "clearTimeout", "clearInterval",
        "undefined", "null", "NaN", "Infinity", "this", "arguments",
        "parseInt", "parseFloat", "isNaN", "isFinite",
    }

    # Detect language
    is_python = any(line.strip().startswith(("import ", "from ")) for line in lines)
    is_js = any(line.strip().startswith(("import ", "const ", "let ", "var ", "function ")) for line in lines)

    if not is_python and not is_js:
        return smells

    # Collect imported names
    imported_names = set()
    if is_python:
        for line in lines:
            m = re.match(r"^from\s+(\S+)\s+import\s+(.+)$", line.strip())
            if m:
                parts = m.group(2)
                for part in parts.split(","):
                    name = part.strip().split(" as ")[0].strip()
                    if name and name != "*":
                        imported_names.add(name)
            m = re.match(r"^import\s+(.+)$", line.strip())
            if m:
                for part in m.group(1).split(","):
                    name = part.strip().split(" as ")[-1].strip().split(".")[0]
                    imported_names.add(name)

    if is_js:
        for line in lines:
            m = re.match(r"import\s+\{([^}]+)\}\s+from", line.strip())
            if m:
                for part in m.group(1).split(","):
                    name = part.strip().split(" as ")[-1].strip()
                    imported_names.add(name)
            m = re.match(r"import\s+(\S+)\s+from", line.strip())
            if m:
                imported_names.add(m.group(1))
            m = re.match(r"const\s+\{([^}]+)\}\s*=\s*require", line.strip())
            if m:
                for part in m.group(1).split(","):
                    name = part.strip().split(":")[0].strip()
                    imported_names.add(name)

    # Find potential unimported function calls
    call_pattern = re.compile(r"\b([a-zA-Z_][a-zA-Z0-9_]{2,})\s*\(")
    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith(("import ", "from ", "//", "#", "def ", "class ", "function ")):
            continue
        for m in call_pattern.finditer(line):
            name = m.group(1)
            if name in builtins_py or name in builtins_js:
                continue
            if name in imported_names:
                continue
            if name[0].isupper():
                continue   # Probably a class instantiation or type annotation
            # Heuristic: common third-party names that are frequently unimported
            common_third_party = {"pd", "np", "tf", "torch", "plt", "sns", "px", "sqlalchemy"}
            if name in common_third_party:
                smells.append(CodeSmell(
                    name="incomplete_import",
                    severity="info",
                    line_number=i,
                    description=f"'{name}' appears used but may not be imported",
                    snippet=stripped[:100],
                    fix_suggestion=f"Ensure '{name}' is imported (e.g., 'import {name}')."
                ))
    return smells


def detect_bare_except(code: str) -> List[CodeSmell]:
    """Detect bare 'except:' clauses without exception type."""
    smells = []
    lines = code.split("\n")

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()
        # Python: except: without exception class
        if re.match(r"except\s*:", stripped):
            smells.append(CodeSmell(
                name="bare_except",
                severity="warning",
                line_number=i,
                description="Bare 'except:' clause catches all exceptions including SystemExit and KeyboardInterrupt",
                snippet=stripped[:100],
                fix_suggestion="Specify the exception type(s) to catch, e.g. 'except ValueError:' or 'except Exception:'."
            ))
        # JavaScript: catch without parameter (rarely an issue, but flag)
        if re.match(r"\}\s*catch\s*\{", stripped):
            smells.append(CodeSmell(
                name="bare_except",
                severity="info",
                line_number=i,
                description="JavaScript 'catch' without error parameter discards error info",
                snippet=stripped[:100],
                fix_suggestion="Capture the error: 'catch (error) {' to handle or log it."
            ))
    return smells


def detect_language(file_path: str) -> str:
    """Determine language from file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    lang_map = {".py": "Python", ".js": "JavaScript", ".ts": "TypeScript"}
    return lang_map.get(ext, "unknown")


def inspect_code(file_path: str) -> InspectResult:
    """Run all detectors on a single file and return an InspectResult."""
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        code = f.read()

    language = detect_language(file_path)
    result = InspectResult(file_path=file_path, language=language)

    detectors = [
        detect_truncation,
        detect_thinking_skip,
        detect_hardcoded_secrets,
        detect_missing_error_handling,
        detect_todo_bombs,
        detect_copy_paste,
        detect_incomplete_imports,
        detect_bare_except,
    ]

    all_smells = []
    for detector in detectors:
        smells = detector(code)
        all_smells.extend(smells)

    result.smells = all_smells
    result.quality_score = calculate_quality_score(result)
    result.summary = generate_summary(result)
    return result


def inspect_directory(dir_path: str) -> List[InspectResult]:
    """Recursively scan a directory for Python, JS, and TS files."""
    results = []
    supported_exts = {".py", ".js", ".ts"}
    for root, dirs, files in os.walk(dir_path):
        # Skip hidden directories and common non-source dirs
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in
                   ("node_modules", "venv", ".venv", "__pycache__", "dist", "build", ".git")]
        for fname in sorted(files):
            ext = os.path.splitext(fname)[1].lower()
            if ext in supported_exts:
                file_path = os.path.join(root, fname)
                try:
                    result = inspect_code(file_path)
                    results.append(result)
                except Exception:
                    pass
    return results


def calculate_quality_score(result: InspectResult) -> int:
    """Calculate quality score starting at 100, deducting for each smell."""
    score = 100
    for smell in result.smells:
        weight = SEVERITY_WEIGHTS.get(smell.name, 5)
        score -= weight
    return max(0, score)


def generate_summary(result: InspectResult) -> str:
    """Generate a human-readable summary."""
    if not result.smells:
        return f"{result.file_path}: Clean — no AI code smells detected."
    smell_counts = {}
    for s in result.smells:
        smell_counts[s.name] = smell_counts.get(s.name, 0) + 1
    parts = [f"{result.file_path}: {len(result.smells)} smell(s), score={result.quality_score}"]
    for name, count in smell_counts.items():
        parts.append(f"  {name}: {count}")
    return "\n".join(parts)
