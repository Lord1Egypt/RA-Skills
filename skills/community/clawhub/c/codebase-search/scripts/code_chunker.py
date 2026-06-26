"""CodeChunker — splits Python source files into class/function chunks using ast."""
from __future__ import annotations
import ast
import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class CodeChunk:
    chunk_id: str
    filepath: str       # relative to repo root
    symbol_name: str
    symbol_type: str    # "class" or "function"
    start_line: int
    end_line: int
    source: str
    docstring: str
    module_path: str

class CodeChunker:
    def __init__(self, repo_root: str):
        self.repo_root = Path(repo_root).resolve()

    def _rel(self, path: str) -> str:
        return str(Path(path).resolve().relative_to(self.repo_root))

    def _chunk_id(self, filepath: str, name: str, line: int) -> str:
        return hashlib.sha256(f"{filepath}:{name}:{line}".encode()).hexdigest()[:16]

    def _module_path(self, filepath: str) -> str:
        rel = self._rel(filepath)
        return rel.replace(os.sep, ".").removesuffix(".py")

    def chunk_file(self, filepath: str) -> List[CodeChunk]:
        try:
            source = Path(filepath).read_text(encoding="utf-8", errors="ignore")
            tree = ast.parse(source)
        except SyntaxError:
            return []
        lines = source.splitlines()
        chunks = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if not isinstance(node, ast.ClassDef) and not (
                node.col_offset == 0 or isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            ):
                continue
            # Only top-level or class-level
            if node.col_offset != 0:
                continue
            sym_type = "class" if isinstance(node, ast.ClassDef) else "function"
            start = node.lineno - 1
            end = node.end_lineno
            sym_source = "\n".join(lines[start:end])
            docstring = ast.get_docstring(node) or ""
            rel = self._rel(filepath)
            chunks.append(CodeChunk(
                chunk_id=self._chunk_id(rel, node.name, node.lineno),
                filepath=rel,
                symbol_name=node.name,
                symbol_type=sym_type,
                start_line=node.lineno,
                end_line=node.end_lineno,
                source=sym_source,
                docstring=docstring,
                module_path=self._module_path(filepath),
            ))
        return chunks

    def chunk_repo(self, include_patterns=None, exclude_patterns=None) -> List[CodeChunk]:
        exclude = exclude_patterns or ["__pycache__", ".venv", "migrations", "tests", "scripts", ".git", "node_modules", ".codebase_index"]
        chunks = []
        for py_file in self.repo_root.rglob("*.py"):
            rel = str(py_file.relative_to(self.repo_root))
            if any(ex in rel for ex in exclude):
                continue
            chunks.extend(self.chunk_file(str(py_file)))
        return chunks
