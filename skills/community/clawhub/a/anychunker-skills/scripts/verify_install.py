#!/usr/bin/env python3
"""Verify the anychunker install and print a small smoke-test result.

Cross-platform (macOS / Linux / Windows). Pure stdlib except for the target
library. Run:

    python scripts/verify_install.py

Exits 0 on success, 1 if `anychunker` is not importable.
"""
from __future__ import annotations

import importlib
import platform
import sys
from typing import Optional


def _print_header() -> None:
    print("=" * 60)
    print("anychunker install check")
    print("=" * 60)
    print(f"OS:            {platform.system()} {platform.release()}")
    print(f"Python:        {sys.version.split()[0]}  ({sys.executable})")
    print("-" * 60)


def _check_core() -> Optional[object]:
    try:
        mod = importlib.import_module("anychunker")
    except ImportError as e:
        print("[FAIL] anychunker is NOT installed.")
        print(f"       ImportError: {e}")
        print()
        print("Install with:")
        print("    pip install anychunker")
        print()
        print("Or, from a local clone of the repo:")
        print("    pip install -e .")
        return None

    version = getattr(mod, "__version__", "unknown")
    print(f"[ OK ] anychunker  version={version}")
    print(f"       location:   {getattr(mod, '__file__', '?')}")
    return mod


def _check_optional(name: str, purpose: str) -> None:
    try:
        importlib.import_module(name)
        print(f"[ OK ] {name:<22} available — {purpose}")
    except ImportError:
        print(f"[    ] {name:<22} not installed — {purpose}")


def _smoke_test() -> bool:
    """Run a tiny end-to-end split to prove the library actually works."""
    from anychunker import AnyMarkdownBlockChunker

    sample = (
        "# Title\n"
        "\n"
        "First paragraph with some body text.\n"
        "\n"
        "## Section A\n"
        "```python\n"
        "def hello():\n"
        "    return 'world'\n"
        "```\n"
    )

    chunker = AnyMarkdownBlockChunker(chunk_size=200, chunk_overlap=0)
    doc = chunker.invoke(sample)
    n = len(doc.chunks)
    print()
    print(f"Smoke test:  split a 3-block Markdown sample -> {n} chunk(s)")
    if n == 0:
        print("[FAIL] no chunks produced")
        return False

    print(f"  first chunk id={doc.chunks[0].chunk_id} "
          f"size={doc.chunks[0].chunk_size} "
          f"content={doc.chunks[0].content[:40]!r}")
    print("[ OK ] end-to-end split works")
    return True


def main() -> int:
    _print_header()

    mod = _check_core()
    if mod is None:
        return 1

    print()
    print("Optional dependencies:")
    _check_optional("transformers", "AnyTextChunker.from_tokenizer(...)")
    _check_optional("sentence_transformers", "AnySemanticsChunker embedding backend")
    _check_optional("jieba", "Chinese word-count length function")
    _check_optional("tiktoken", "OpenAI-compatible token counting")

    print()
    ok = _smoke_test()

    print()
    print("=" * 60)
    print("READY" if ok else "PROBLEM DETECTED")
    print("=" * 60)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
