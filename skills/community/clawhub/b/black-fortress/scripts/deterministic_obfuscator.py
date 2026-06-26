#!/usr/bin/env python3
"""
Black-Fortress Layer 1: Deterministic Obfuscator

Semantic Neutralization — kills all linguistic injection surfaces.

Usage:
    python deterministic_obfuscator.py <source_dir> <output_dir>

What it does:
    1. AST-parses all Python files
    2. Strips comments, docstrings, print/log statements
    3. Renames all identifiers to random hashes
    4. Truncates string literals > 50 chars
"""

import ast
import os
import sys
import hashlib
import random
import string
import shutil
import json
from pathlib import Path
from typing import Dict, Set, Optional


# ─── Configuration ──────────────────────────────────────────────
MAX_STRING_LITERAL_LENGTH = 50
HASH_LENGTH = 8
SALT = "black-fortress-obfuscation-v1"

# Preserve these names (stdlib and common imports)
PRESERVED_NAMES = {
    # Python builtins
    "print", "len", "range", "int", "str", "float", "list", "dict",
    "set", "tuple", "bool", "type", "isinstance", "issubclass",
    "hasattr", "getattr", "setattr", "delattr", "super", "property",
    "staticmethod", "classmethod", "enumerate", "zip", "map", "filter",
    "sorted", "reversed", "any", "all", "min", "max", "sum", "abs",
    "round", "pow", "divmod", "hash", "id", "repr", "format",
    "iter", "next", "open", "input", "vars", "dir", "help",
    "callable", "hex", "oct", "bin", "chr", "ord", "bytes",
    "bytearray", "memoryview", "frozenset", "complex", "object",
    "None", "True", "False", "Ellipsis", "NotImplemented",
    "Exception", "BaseException", "ValueError", "TypeError",
    "KeyError", "IndexError", "AttributeError", "ImportError",
    "RuntimeError", "StopIteration", "OSError", "IOError",
    # Common stdlib
    "os", "sys", "json", "re", "math", "time", "datetime",
    "collections", "itertools", "functools", "pathlib",
    "subprocess", "shutil", "hashlib", "base64", "struct",
    "io", "copy", "pickle", "csv", "logging", "argparse",
    "typing", "dataclass", "abc",
    # Common method names
    "__init__", "__str__", "__repr__", "__eq__", "__hash__",
    "__len__", "__getitem__", "__setitem__", "__contains__",
    "__iter__", "__next__", "__enter__", "__exit__",
    "__call__", "__new__", "__del__", "__add__", "__sub__",
    "self", "cls", "args", "kwargs",
}


class IdentifierMapper:
    """Maps original identifiers to deterministic random hashes."""

    def __init__(self, salt: str = SALT):
        self._salt = salt
        self._map: Dict[str, str] = {}
        self._counter = 0

    KNOWN_PREFIXES = {"v_", "cls_", "priv_", "dunder_"}

    def _is_obfuscated(self, name: str) -> bool:
        """Check if a name was already obfuscated (has an obfuscation prefix)."""
        return any(name.startswith(p) for p in self.KNOWN_PREFIXES) and name in self._map.values()

    def get(self, name: str) -> str:
        if name in PRESERVED_NAMES:
            return name
        if self._is_obfuscated(name):
            return name  # Already obfuscated — don't double-map
        if name not in self._map:
            self._counter += 1
            hash_input = f"{self._salt}:{self._counter}:{name}"
            hex_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:HASH_LENGTH]
            prefix = self._classify(name)
            self._map[name] = f"{prefix}_{hex_hash}"
        return self._map[name]

    def _classify(self, name: str) -> str:
        """Classify identifier type for prefix."""
        if name.startswith("__") and name.endswith("__"):
            return "dunder"
        if name[0].isupper():
            return "cls"
        if name.startswith("_"):
            return "priv"
        return "v"

    def get_mapping_report(self) -> Dict[str, str]:
        return dict(self._map)


class CommentStripper(ast.NodeTransformer):
    """Strips docstrings from AST nodes."""

    def _strip_docstring(self, node):
        if (isinstance(node, ast.Module) and node.body
                and isinstance(node.body[0], ast.Expr)
                and isinstance(node.body[0].value, (ast.Constant, ast.Str))):
            node.body = node.body[1:]
        elif (node.body and isinstance(node.body[0], ast.Expr)
              and isinstance(node.body[0].value, (ast.Constant, ast.Str))):
            node.body = node.body[1:]
        return node

    def visit_Module(self, node):
        self.generic_visit(node)
        return self._strip_docstring(node)

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        return self._strip_docstring(node)

    def visit_AsyncFunctionDef(self, node):
        self.generic_visit(node)
        return self._strip_docstring(node)

    def visit_ClassDef(self, node):
        self.generic_visit(node)
        return self._strip_docstring(node)


class IdentifierObfuscator(ast.NodeTransformer):
    """Renames all identifiers to random hashes."""

    def __init__(self, mapper: IdentifierMapper):
        self.mapper = mapper
        self._local_scopes: list[Set[str]] = []

    def _push_scope(self):
        self._local_scopes.append(set())

    def _pop_scope(self):
        self._local_scopes.pop()

    def _add_local(self, name: str):
        if self._local_scopes:
            self._local_scopes[-1].add(name)

    def _is_local(self, name: str) -> bool:
        for scope in self._local_scopes:
            if name in scope:
                return True
        return False

    def visit_FunctionDef(self, node):
        node.name = self.mapper.get(node.name)
        self._push_scope()
        for arg in node.args.args:
            self._add_local(arg.arg)
            arg.arg = self.mapper.get(arg.arg)
        if node.args.vararg:
            self._add_local(node.args.vararg.arg)
            node.args.vararg.arg = self.mapper.get(node.args.vararg.arg)
        if node.args.kwarg:
            self._add_local(node.args.kwarg.arg)
            node.args.kwarg.arg = self.mapper.get(node.args.kwarg.arg)
        self.generic_visit(node)
        self._pop_scope()
        return node

    def visit_AsyncFunctionDef(self, node):
        return self.visit_FunctionDef(node)

    def visit_ClassDef(self, node):
        node.name = self.mapper.get(node.name)
        self._push_scope()
        self.generic_visit(node)
        self._pop_scope()
        return node

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            self._add_local(node.id)
        node.id = self.mapper.get(node.id)
        return node

    def visit_Attribute(self, node):
        # Don't obfuscate attribute access on external objects
        self.generic_visit(node)
        return node

    def visit_arg(self, node):
        node.arg = self.mapper.get(node.arg)
        return node

    def visit_Global(self, node):
        node.names = [self.mapper.get(n) for n in node.names]
        return node

    def visit_Nonlocal(self, node):
        node.names = [self.mapper.get(n) for n in node.names]
        return node


class StringTruncator(ast.NodeTransformer):
    """Truncates long string literals that may contain encoded payloads."""

    def visit_Constant(self, node):
        if isinstance(node.value, str) and len(node.value) > MAX_STRING_LITERAL_LENGTH:
            node.value = node.value[:MAX_STRING_LITERAL_LENGTH] + "..."
        return node

    def visit_Str(self, node):
        if len(node.s) > MAX_STRING_LITERAL_LENGTH:
            node.s = node.s[:MAX_STRING_LITERAL_LENGTH] + "..."
        return node


class PrintRemover(ast.NodeTransformer):
    """Removes print() and common logging calls."""

    LOGGING_NAMES = {"print", "debug", "info", "warning", "error", "critical", "log"}

    def visit_Expr(self, node):
        if (isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
                and node.value.func.id in self.LOGGING_NAMES):
            return None  # Remove the statement
        if (isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Attribute)
                and node.value.func.attr in self.LOGGING_NAMES):
            return None
        return node


def obfuscate_source(source: str, mapper: IdentifierMapper) -> str:
    """Full obfuscation pipeline on a single source string."""
    try:
        tree = ast.parse(source)
    except SyntaxError as e:
        return f"# SYNTAX ERROR — cannot obfuscate: {e}\n"

    # Pipeline: strip comments → remove prints → truncate strings → obfuscate IDs
    tree = CommentStripper().visit(tree)
    tree = PrintRemover().visit(tree)
    tree = StringTruncator().visit(tree)
    tree = IdentifierObfuscator(mapper).visit(tree)

    ast.fix_missing_locations(tree)
    return ast.unparse(tree)


def process_directory(source_dir: str, output_dir: str) -> dict:
    """Process all Python files in source_dir and write obfuscated versions."""
    source_path = Path(source_dir)
    output_path = Path(output_dir)
    mapper = IdentifierMapper()

    output_path.mkdir(parents=True, exist_ok=True)
    results = {"files_processed": 0, "files_failed": 0, "identifier_map": {}}

    for py_file in sorted(source_path.rglob("*.py")):
        rel_path = py_file.relative_to(source_path)
        out_file = output_path / rel_path
        out_file.parent.mkdir(parents=True, exist_ok=True)

        try:
            source = py_file.read_text(encoding="utf-8")
            obfuscated = obfuscate_source(source, mapper)
            out_file.write_text(obfuscated, encoding="utf-8")
            results["files_processed"] += 1
        except Exception as e:
            out_file.write_text(f"# OBFUSCATION FAILED: {e}\n", encoding="utf-8")
            results["files_failed"] += 1

    results["identifier_map"] = mapper.get_mapping_report()
    return results


def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <source_dir> <output_dir>", file=sys.stderr)
        sys.exit(1)

    source_dir = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.isdir(source_dir):
        print(f"Error: {source_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    results = process_directory(source_dir, output_dir)

    # Write mapping report for forensic analysis
    report_path = os.path.join(output_dir, ".obfuscation_report.json")
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)

    print(json.dumps({
        "status": "complete",
        "files_processed": results["files_processed"],
        "files_failed": results["files_failed"],
        "report": report_path
    }, indent=2))


if __name__ == "__main__":
    main()
