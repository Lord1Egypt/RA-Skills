"""Unit test: verify the standard post object <-> Ghost post translation
and the config/author-resolution logic. Does not hit Ghost."""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import publisher as pub_mod


def test_standard_to_ghost_basic_fields():
    post = {
        "title": "Hello",
        "seo_title": "Hello SEO",
        "excerpt": "Short summary",
        "body_md": "# ignored\n\nBody text.",
        "tags": ["a", "b"],
        "status": "draft",
    }
    g = pub_mod._standard_to_ghost(post, {})
    assert g["title"] == "Hello"
    assert g["meta_title"] == "Hello SEO"
    assert g["custom_excerpt"] == "Short summary"
    assert g["status"] == "draft"
    assert g["tags"] == [{"name": "a"}, {"name": "b"}]
    # body_md -> lexical JSON string
    assert isinstance(g["lexical"], str)
    parsed = json.loads(g["lexical"])
    assert parsed["root"]["type"] == "root"
    print("[PASS] standard->ghost basic fields map correctly")


def test_standard_to_ghost_author_mapping():
    config = {
        "default_author_id": "default_staff",
        "agent_author_map": {
            "staff_1": "ghost_1",
            "staff_2": "ghost_2",
        },
    }
    # Known author -> mapped
    g = pub_mod._standard_to_ghost({"title": "T", "author": "staff_1"}, config)
    assert g["authors"] == [{"id": "ghost_1"}], f"got {g.get('authors')}"

    # Unknown author -> fallback to default
    g = pub_mod._standard_to_ghost({"title": "T", "author": "nobody"}, config)
    assert g["authors"] == [{"id": "default_staff"}], f"got {g.get('authors')}"

    # No author supplied -> default
    g = pub_mod._standard_to_ghost({"title": "T"}, config)
    assert g["authors"] == [{"id": "default_staff"}]
    print("[PASS] author mapping resolves known / unknown / missing")


def test_standard_to_ghost_no_author_no_default():
    """With no author and no default_author_id, authors key should be absent."""
    g = pub_mod._standard_to_ghost({"title": "T"}, {"agent_author_map": {}})
    assert "authors" not in g, f"unexpected authors key: {g.get('authors')}"
    print("[PASS] authors key absent when nothing is configured")


def test_ghost_to_standard_roundtrip_fields():
    ghost_post = {
        "id": "abc123",
        "title": "Hello",
        "meta_title": "Hello SEO",
        "custom_excerpt": "Summary",
        "tags": [{"name": "a"}, {"name": "b"}],
        "authors": [{"slug": "staff-1", "id": "ghost_1"}],
        "status": "published",
        "feature_image": "https://cdn.example.com/h.jpg",
        "feature_image_alt": "hero alt",
        "url": "https://example.com/hello/",
        "updated_at": "2026-04-15T00:00:00Z",
    }
    s = pub_mod._ghost_to_standard(ghost_post)
    assert s["id"] == "abc123"
    assert s["title"] == "Hello"
    assert s["seo_title"] == "Hello SEO"
    assert s["excerpt"] == "Summary"
    assert s["tags"] == ["a", "b"]
    assert s["author"] == "staff-1"
    assert s["status"] == "published"
    assert s["featured_image_url"] == "https://cdn.example.com/h.jpg"
    assert s["image_alt_text"] == "hero alt"
    assert s["url"] == "https://example.com/hello/"
    print("[PASS] ghost->standard maps all documented fields")


def test_load_config_missing_file_returns_defaults():
    cfg = pub_mod.load_config("does-not-exist.json")
    assert cfg["default_author_id"] is None
    assert cfg["agent_author_map"] == {}
    assert cfg["newsletter_id"] is None
    assert cfg["max_image_size_mb"] == pub_mod.DEFAULT_MAX_IMAGE_MB
    print("[PASS] load_config returns safe defaults for missing file")


def test_load_config_reads_json():
    tmp = Path("tmp-ghost-publisher-test-cfg.json")
    tmp.write_text(json.dumps({
        "default_author_id": "xyz",
        "agent_author_map": {"staff_1": "ghost_1"},
        "max_image_size_mb": 5,
    }), encoding="utf-8")
    try:
        cfg = pub_mod.load_config(str(tmp))
        assert cfg["default_author_id"] == "xyz"
        assert cfg["agent_author_map"] == {"staff_1": "ghost_1"}
        assert cfg["max_image_size_mb"] == 5
        assert cfg["newsletter_id"] is None  # default preserved
    finally:
        tmp.unlink()
    print("[PASS] load_config reads values from JSON file")


def test_schedule_uses_published_at():
    """The scheduled_at standard field should map to Ghost's published_at."""
    g = pub_mod._standard_to_ghost(
        {"title": "T", "status": "scheduled", "scheduled_at": "2026-05-01T09:00:00Z"},
        {},
    )
    assert g["status"] == "scheduled"
    assert g["published_at"] == "2026-05-01T09:00:00Z"
    print("[PASS] scheduled_at maps to Ghost published_at")


if __name__ == "__main__":
    test_standard_to_ghost_basic_fields()
    test_standard_to_ghost_author_mapping()
    test_standard_to_ghost_no_author_no_default()
    test_ghost_to_standard_roundtrip_fields()
    test_load_config_missing_file_returns_defaults()
    test_load_config_reads_json()
    test_schedule_uses_published_at()
    print("\nAll 7 mapping/config tests passed.")
