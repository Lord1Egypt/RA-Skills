#!/usr/bin/env python3
"""
Black-Fortress Layer 3: Transcript Extractor

Automatically generates the inspector transcript (expected operations)
from the ORIGINAL source code BEFORE Layer 1 obfuscation runs.

This solves the operational gap: the behavioral audit in Layer 3
needs an "expected operations" transcript, but nothing was generating one.

Usage:
    python transcript_extractor.py --source <source_dir> --output <transcript.json>

What it does:
    1. AST-parses original Python source files
    2. Extracts all I/O operations (file read/write, network, subprocess)
    3. Maps operations to expected syscalls
    4. Outputs a structured transcript for Layer 3's behavioral audit

Critical: This MUST run on the ORIGINAL code, NOT the obfuscated code.
The pipeline order is: Extract Transcript → Obfuscate → Sandbox → Audit
"""

import ast
import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Set, Optional
from dataclasses import dataclass, asdict, field


# ─── Operation Detection ───────────────────────────────────────

# File I/O patterns
FILE_READ_PATTERNS = {
    "open": {"mode_hint": ["r", "rb"]},
    "pathlib.Path.read_text": {"action": "read"},
    "pathlib.Path.read_bytes": {"action": "read"},
    "pathlib.Path.open": {},
    "shutil.copy": {"action": "read"},
    "shutil.copy2": {"action": "read"},
    "json.load": {"action": "read", "format": "json"},
    "csv.reader": {"action": "read", "format": "csv"},
    "pandas.read_csv": {"action": "read", "format": "csv"},
    "pandas.read_json": {"action": "read", "format": "json"},
    "pandas.read_excel": {"action": "read", "format": "excel"},
}

FILE_WRITE_PATTERNS = {
    "open": {"mode_hint": ["w", "wb", "a", "ab", "x"]},
    "pathlib.Path.write_text": {"action": "write"},
    "pathlib.Path.write_bytes": {"action": "write"},
    "shutil.copy": {"action": "write"},
    "shutil.copy2": {"action": "write"},
    "json.dump": {"action": "write", "format": "json"},
    "csv.writer": {"action": "write", "format": "csv"},
    "pandas.DataFrame.to_csv": {"action": "write", "format": "csv"},
    "pandas.DataFrame.to_json": {"action": "write", "format": "json"},
    "pandas.DataFrame.to_excel": {"action": "write", "format": "excel"},
}

NETWORK_PATTERNS = {
    "socket.socket": {"action": "network"},
    "socket.create_connection": {"action": "network"},
    "socket.connect": {"action": "network"},
    "http.client.HTTPConnection": {"action": "network"},
    "http.client.HTTPSConnection": {"action": "network"},
    "urllib.request.urlopen": {"action": "network"},
    "requests.get": {"action": "network"},
    "requests.post": {"action": "network"},
    "requests.put": {"action": "network"},
    "requests.delete": {"action": "network"},
    "httpx.get": {"action": "network"},
    "httpx.post": {"action": "network"},
    "aiohttp.ClientSession": {"action": "network"},
}

NETWORK_PREFIXES = {"socket.", "http.client.", "urllib.", "requests.", "httpx.", "aiohttp.", "s.connect", "s.send", "s.recv", "s.bind", "s.listen"}

SUBPROCESS_PATTERNS = {
    "subprocess.run": {"action": "execute"},
    "subprocess.call": {"action": "execute"},
    "subprocess.check_call": {"action": "execute"},
    "subprocess.check_output": {"action": "execute"},
    "subprocess.Popen": {"action": "execute"},
    "os.system": {"action": "execute"},
    "os.execv": {"action": "execute"},
    "os.execve": {"action": "execute"},
    "os.popen": {"action": "execute"},
}

# Pure computation actions (no syscalls expected)
TRANSFORM_PATTERNS = {
    "filter", "map", "sorted", "reversed", "sum", "min", "max",
    "len", "enumerate", "zip", "any", "all", "list", "dict", "set",
    "str.join", "str.split", "str.strip", "str.replace",
    "re.search", "re.match", "re.findall", "re.sub",
    "hashlib.sha256", "hashlib.md5",
    "json.loads", "json.dumps",
}

# OS interaction patterns
OS_PATTERNS = {
    "os.listdir": {"action": "list", "target": "directory"},
    "os.walk": {"action": "list", "target": "directory"},
    "os.stat": {"action": "stat"},
    "os.path.exists": {"action": "stat"},
    "os.path.isfile": {"action": "stat"},
    "os.path.isdir": {"action": "stat"},
    "os.remove": {"action": "delete"},
    "os.unlink": {"action": "delete"},
    "os.mkdir": {"action": "create", "target": "directory"},
    "os.makedirs": {"action": "create", "target": "directory"},
    "os.rename": {"action": "rename"},
    "os.environ": {"action": "read", "target": "environment"},
    "os.environ.get": {"action": "read", "target": "environment"},
    "os.uname": {"action": "read", "target": "system_info"},
}


@dataclass
class ExtractedOperation:
    action: str
    target: str = ""
    reason: str = ""
    source_file: str = ""
    line_number: int = 0
    function_name: str = ""
    method: str = ""
    risk_level: str = "low"  # low, medium, high
    details: Dict[str, Any] = field(default_factory=dict)


class TranscriptExtractor(ast.NodeVisitor):
    """AST visitor that extracts I/O operations from source code."""

    def __init__(self, filename: str):
        self.filename = filename
        self.operations: List[ExtractedOperation] = []
        self.current_function = "<module>"
        self.imports: Set[str] = set()

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module or ""
        for alias in node.names:
            self.imports.add(f"{module}.{alias.name}")
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        old_func = self.current_function
        self.current_function = node.name
        self.generic_visit(node)
        self.current_function = old_func

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

    def visit_Call(self, node):
        call_name = self._get_call_name(node)
        line = node.lineno

        # Check all pattern categories
        for category_patterns, default_action in [
            (FILE_READ_PATTERNS, "read"),
            (FILE_WRITE_PATTERNS, "write"),
            (NETWORK_PATTERNS, "network"),
            (SUBPROCESS_PATTERNS, "execute"),
            (OS_PATTERNS, "system"),
        ]:
            matched = False
            for pattern, details in category_patterns.items():
                if call_name == pattern or call_name.endswith(f".{pattern.split('.')[-1]}"):
                    # For network patterns, verify prefix to avoid false positives
                    if category_patterns is NETWORK_PATTERNS:
                        if not any(call_name.startswith(p) for p in NETWORK_PREFIXES):
                            continue
                    op = self._build_operation(call_name, pattern, details, line, default_action)
                    self.operations.append(op)
                    matched = True
                    break

        self.generic_visit(node)

    def _get_call_name(self, node) -> str:
        """Extract full call name from a Call node."""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            parts = []
            current = node.func
            while isinstance(current, ast.Attribute):
                parts.append(current.attr)
                current = current.value
            if isinstance(current, ast.Name):
                parts.append(current.id)
            return ".".join(reversed(parts))
        return "<unknown>"

    def _build_operation(self, call_name: str, pattern: str,
                         details: dict, line: int,
                         default_action: str) -> ExtractedOperation:
        """Build an ExtractedOperation from a detected pattern."""
        action = details.get("action", default_action)
        target = ""
        risk = "low"

        # Try to extract the file path from arguments
        if action in ("read", "write", "delete", "rename"):
            risk = "medium"
        elif action == "network":
            risk = "high"
        elif action == "execute":
            risk = "high"

        return ExtractedOperation(
            action=action,
            target=target,
            reason=f"Detected {call_name} call",
            source_file=self.filename,
            line_number=line,
            function_name=self.current_function,
            method=call_name,
            risk_level=risk,
            details=details
        )


def extract_transcript(source_dir: str) -> Dict[str, Any]:
    """Extract expected operations from all Python files in a directory."""
    source_path = Path(source_dir)
    all_operations = []
    files_scanned = 0
    files_failed = 0

    for py_file in sorted(source_path.rglob("*.py")):
        if py_file.name.startswith("."):
            continue
        try:
            source = py_file.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(py_file))
            extractor = TranscriptExtractor(str(py_file.relative_to(source_path)))
            extractor.visit(tree)
            all_operations.extend(extractor.operations)
            files_scanned += 1
        except SyntaxError:
            files_failed += 1
        except Exception:
            files_failed += 1

    # Deduplicate and format
    seen = set()
    expected_operations = []
    for op in all_operations:
        key = (op.action, op.method, op.source_file, op.line_number)
        if key not in seen:
            seen.add(key)
            expected_operations.append(asdict(op))

    # Categorize for the behavioral audit
    summary = {
        "has_network_calls": any(o["action"] == "network" for o in expected_operations),
        "has_subprocess_calls": any(o["action"] == "execute" for o in expected_operations),
        "has_file_writes": any(o["action"] == "write" for o in expected_operations),
        "has_file_reads": any(o["action"] == "read" for o in expected_operations),
        "has_env_access": any(o.get("target") == "environment" for o in expected_operations),
        "high_risk_operations": [o for o in expected_operations if o["risk_level"] == "high"],
    }

    # Format for behavioral_audit.py compatibility
    audit_transcript = {
        "expected_operations": [
            {
                "action": op["action"],
                "target": op["target"] or op["method"],
                "reason": op["reason"]
            }
            for op in expected_operations
        ]
    }

    return {
        "source_dir": source_dir,
        "files_scanned": files_scanned,
        "files_failed": files_failed,
        "total_operations": len(expected_operations),
        "summary": summary,
        "operations": expected_operations,
        "audit_transcript": audit_transcript
    }


def main():
    parser = argparse.ArgumentParser(description="Black-Fortress Transcript Extractor")
    parser.add_argument("--source", required=True, help="Source directory to scan")
    parser.add_argument("--output", help="Output transcript JSON path")
    args = parser.parse_args()

    if not os.path.isdir(args.source):
        print(json.dumps({"status": "error", "message": f"Not a directory: {args.source}"}))
        sys.exit(2)

    result = extract_transcript(args.source)
    output = json.dumps(result, indent=2)

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
    else:
        print(output)

    # Flag high-risk operations
    if result["summary"]["high_risk_operations"]:
        print(f"\n⚠ HIGH-RISK OPERATIONS DETECTED: {len(result['summary']['high_risk_operations'])}",
              file=sys.stderr)
        for op in result["summary"]["high_risk_operations"]:
            print(f"  - {op['method']} ({op['action']}) at {op['source_file']}:{op['line_number']}",
                  file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
