from __future__ import annotations

from common_isbn import (
    extract_isbn_candidates_from_text,
    is_valid_isbn10,
    is_valid_isbn13,
    normalize_isbn,
)


def test_isbn_normalization_removes_separators_and_converts_isbn10():
    assert normalize_isbn(" 978-0-306-40615-7 ") == "9780306406157"
    assert normalize_isbn("0-306-40615-2") == "9780306406157"


def test_isbn_checksum_validation_rejects_changed_digits():
    assert is_valid_isbn13("9780306406157") is True
    assert is_valid_isbn13("9780306406158") is False
    assert is_valid_isbn10("0306406152") is True
    assert is_valid_isbn10("0306406153") is False


def test_ocr_text_extracts_only_valid_unique_candidates():
    text = "ISBN 978-0-306-40615-7 and again 9780306406157; invalid 9780306406158"
    assert extract_isbn_candidates_from_text(text) == ["9780306406157"]
