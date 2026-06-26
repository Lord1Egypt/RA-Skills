from anime_character_loader.storage.merge import merge_soul_content


def test_merge_idempotency_same_content():
    existing = "## Character A\nhello"
    merged = merge_soul_content(existing, "## Character A\nhello")
    assert merged == existing
