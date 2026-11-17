#!/usr/bin/env python3
"""End-to-end demo of AnyMarkdownBlockChunker (structure-preserving split).

Cross-platform (macOS / Linux / Windows). Run:

    python scripts/quick_demo.py

Prints each chunk's id, title, block hierarchy (parent/child ids), and a
content preview so you can see the tree structure.
"""
from __future__ import annotations

import json
import sys
import textwrap


SAMPLE_MARKDOWN = textwrap.dedent(
    """
    Intro paragraph outside any heading.

    # Guide

    Some overview text under the top-level heading.

    ## Installation

    Install with pip:

    ```bash
    pip install anychunker
    ```

    ## Usage

    ### Basic

    Import and go.

    ```python
    from anychunker import AnyMarkdownBlockChunker
    chunker = AnyMarkdownBlockChunker(chunk_size=500)
    ```

    ### Advanced

    See the API reference.

    # Appendix

    <table>
        <tr><th>Key</th><th>Value</th></tr>
        <tr><td>lib</td><td>anychunker</td></tr>
    </table>
    """
).strip()


def main() -> int:
    try:
        from anychunker import AnyMarkdownBlockChunker
    except ImportError as e:
        print("anychunker is not installed. Run: pip install anychunker", file=sys.stderr)
        print(f"({e})", file=sys.stderr)
        return 1

    chunker = AnyMarkdownBlockChunker(chunk_size=200, chunk_overlap=20)
    doc = chunker.invoke(SAMPLE_MARKDOWN)

    print(f"Total chunks: {len(doc.chunks)}\n")

    for c in doc.chunks:
        m = c.metadata
        title = m.get("title", {}) or {}
        headings = m.get("headings", {}) or {}
        title_str = title.get("name", "-") if title else "-"
        heading_str = headings.get("name", "-") if headings else "-"

        print(
            f"[block={m.get('block_id')} chunk={m.get('chunk_id')}] "
            f"title={title_str!r} heading={heading_str!r}"
        )
        print(
            f"    block_parents={m.get('block_parent_id')} "
            f"block_children={m.get('block_child_id')}"
        )
        preview = c.content.replace("\n", " ").strip()
        if len(preview) > 70:
            preview = preview[:67] + "..."
        print(f"    content: {preview}")
        print()

    print("---")
    print("Batch iteration demo (batch_size=2):")
    for batch in doc.batchIterator(batch_size=2):
        print(
            f"  batch #{batch.batch_index}  "
            f"chunks={len(batch.chunks)}  "
            f"ids={batch.get_chunk_ids()}  "
            f"total_content_len={batch.total_content_length}"
        )

    print("\n---")
    print("First chunk as JSON:")
    print(json.dumps(doc.chunks[0].model_dump(mode="json"), ensure_ascii=False, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
