from scripts.models.schemas import is_red_level, normalize_published_at


def test_is_red_level():
    assert is_red_level("A") is True
    assert is_red_level("B") is True
    assert is_red_level("C") is False
    assert is_red_level("") is False


def test_normalize_published_at():
    assert normalize_published_at(1774577349).startswith("2026-03-27")
    assert normalize_published_at(None) == ""
