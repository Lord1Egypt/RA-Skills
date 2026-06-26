"""Unit test: verify compose_prompt and load_aesthetic work correctly
without needing nano-banana-pro to actually run."""

import sys
from pathlib import Path

# Import the skill module from the parent directory (works regardless of
# where the skill is installed)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import art_director as ad


def test_load_strips_comments():
    """load_aesthetic should strip HTML comments (operator guidance)."""
    # Write a temp aesthetic with comments
    tmp = Path("tmp_aesthetic.md")
    tmp.write_text(
        "# Brand Aesthetic\n\n"
        "<!-- this is operator guidance, should be stripped -->\n\n"
        "## Palette\n"
        "Desaturated cool tones.\n"
        "<!-- multi\nline\ncomment -->\n"
        "## Tone\n"
        "Serious.\n",
        encoding="utf-8",
    )
    result = ad.load_aesthetic(str(tmp))
    tmp.unlink()
    assert "operator guidance" not in result, "HTML comments were not stripped"
    assert "multi" not in result, "multiline HTML comments were not stripped"
    assert "Desaturated cool tones." in result
    assert "Serious." in result
    print("[PASS] load_aesthetic strips HTML comments")


def test_load_missing_returns_empty():
    """load_aesthetic should return empty string if file missing."""
    result = ad.load_aesthetic("does-not-exist.md")
    assert result == "", f"Expected empty string, got: {result!r}"
    print("[PASS] load_aesthetic returns '' for missing file")


def test_compose_appends_tech_specs():
    """compose_prompt should append 16:9 and no-text specs if missing."""
    result = ad.compose_prompt("", "a candle in a library")
    assert "16:9" in result, "16:9 not appended"
    assert "no embedded text" in result, "no-text spec not appended"
    print("[PASS] compose_prompt appends technical specs")


def test_compose_preserves_existing_specs():
    """compose_prompt should not double-append if specs already present."""
    brief = "a candle, 16:9 aspect ratio, no embedded text"
    result = ad.compose_prompt("", brief)
    # Count occurrences
    assert result.count("16:9") == 1, f"16:9 appears {result.count('16:9')} times"
    assert result.count("no embedded text") == 1
    print("[PASS] compose_prompt does not double-append existing specs")


def test_compose_merges_aesthetic_and_brief():
    """compose_prompt should place aesthetic first, then brief separator."""
    aesthetic = "## Palette\nCool blue-grey."
    brief = "a candle"
    result = ad.compose_prompt(aesthetic, brief)
    assert "Palette" in result, "aesthetic not included"
    assert "Image brief:" in result, "brief separator not included"
    assert "a candle" in result
    # Order: aesthetic before brief
    assert result.index("Palette") < result.index("a candle"), "aesthetic should precede brief"
    print("[PASS] compose_prompt merges aesthetic + brief in correct order")


def test_compose_no_aesthetic_just_brief():
    """compose_prompt with empty aesthetic should return the tech-enhanced brief alone."""
    result = ad.compose_prompt("", "a candle in a library")
    assert "Image brief:" not in result, "separator should not appear when no aesthetic"
    assert "a candle in a library" in result
    print("[PASS] compose_prompt handles no-aesthetic case cleanly")


def test_available_presets_finds_all_nine():
    """available_presets should return all nine shipped presets."""
    result = ad.available_presets()
    expected = [
        "documentary",
        "conceptual-illustration",
        "product-render",
        "product-photo",
        "schematic",
        "editorial-collage",
        "synthwave",
        "phosphor",
        "orbital",
    ]
    for name in expected:
        assert name in result, f"{name} missing from {result}"
    print(f"[PASS] available_presets finds all nine: {result}")


if __name__ == "__main__":
    test_load_strips_comments()
    test_load_missing_returns_empty()
    test_compose_appends_tech_specs()
    test_compose_preserves_existing_specs()
    test_compose_merges_aesthetic_and_brief()
    test_compose_no_aesthetic_just_brief()
    test_available_presets_finds_all_nine()
    print("\nAll 7 unit tests passed.")
