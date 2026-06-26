"""Unit test: verify the markdown -> Ghost Lexical converter produces the
expected node types. Does not hit Ghost."""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import publisher as pub_mod


def _nodes(md):
    """Helper: parse markdown and return the top-level Lexical children."""
    lexical = json.loads(pub_mod.markdown_to_lexical(md))
    return lexical["root"]["children"]


def test_heading_levels():
    children = _nodes("# One\n\n## Two\n\n### Three\n\n#### Four")
    # Note: leading "# One" is stripped by the title-stripper (Ghost stores
    # title separately). We should still see h2, h3, h4.
    tags = [c.get("tag") for c in children if c.get("type") == "heading"]
    assert tags == ["h2", "h3", "h4"], f"got heading tags: {tags}"
    print(f"[PASS] heading levels parsed: {tags}")


def test_paragraph_with_bold_italic_code():
    children = _nodes("Plain **bold** and *italic* and `code`.")
    assert len(children) == 1 and children[0]["type"] == "paragraph"
    formats = [c.get("format") for c in children[0]["children"] if c.get("type") == "text"]
    # Expect at least one of each: 0 (plain), 1 (bold), 2 (italic), 16 (code)
    assert 0 in formats, f"no plain text: {formats}"
    assert 1 in formats, f"no bold: {formats}"
    assert 2 in formats, f"no italic: {formats}"
    assert 16 in formats, f"no code: {formats}"
    print(f"[PASS] inline formats: plain/bold/italic/code all present")


def test_link():
    children = _nodes("See [the docs](https://example.com) for more.")
    # The paragraph should contain a link node
    assert children[0]["type"] == "paragraph"
    link_nodes = [c for c in children[0]["children"] if c.get("type") == "link"]
    assert len(link_nodes) == 1, f"expected 1 link, got {len(link_nodes)}"
    assert link_nodes[0]["url"] == "https://example.com"
    print("[PASS] link node parsed with correct url")


def test_unordered_list():
    children = _nodes("- one\n- two\n- three")
    assert len(children) == 1 and children[0]["type"] == "list"
    assert children[0]["listType"] == "bullet"
    assert len(children[0]["children"]) == 3
    print("[PASS] unordered list with 3 items")


def test_ordered_list():
    children = _nodes("1. first\n2. second\n3. third")
    assert len(children) == 1 and children[0]["type"] == "list"
    assert children[0]["listType"] == "number"
    assert len(children[0]["children"]) == 3
    print("[PASS] ordered list with 3 items")


def test_blockquote():
    children = _nodes("> Quoted text here.")
    assert children[0]["type"] == "quote"
    print("[PASS] blockquote node produced")


def test_horizontal_rule():
    children = _nodes("Before\n\n---\n\nAfter")
    types = [c["type"] for c in children]
    assert "horizontalrule" in types, f"got types: {types}"
    print("[PASS] horizontal rule node produced")


def test_leading_title_stripped():
    """A markdown file starting with `# Title` should have that line removed
    -- Ghost stores title separately from body."""
    md = "# This is the article title\n\nFirst paragraph."
    children = _nodes(md)
    # No heading should remain; the stripped title leaves just one paragraph.
    headings = [c for c in children if c.get("type") == "heading"]
    paragraphs = [c for c in children if c.get("type") == "paragraph"]
    assert len(headings) == 0, f"title heading not stripped: {headings}"
    assert len(paragraphs) == 1
    print("[PASS] leading '# Title' line stripped from body")


def test_empty_markdown():
    children = _nodes("")
    assert children == [], f"expected empty, got {children}"
    print("[PASS] empty markdown produces empty node list")


if __name__ == "__main__":
    test_heading_levels()
    test_paragraph_with_bold_italic_code()
    test_link()
    test_unordered_list()
    test_ordered_list()
    test_blockquote()
    test_horizontal_rule()
    test_leading_title_stripped()
    test_empty_markdown()
    print("\nAll 9 markdown tests passed.")
