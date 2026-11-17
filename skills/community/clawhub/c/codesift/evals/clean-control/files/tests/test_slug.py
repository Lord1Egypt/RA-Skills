"""Contract tests for slugify."""

import pytest

from textutil.slug import slugify


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        ("Hello World", "hello-world"),
        ("  Already--Slugged  ", "already-slugged"),
        ("C++ & Rust: 2024 Edition", "c-rust-2024-edition"),
        ("Caf\u00e9 au lait", "caf-au-lait"),
        ("!!!", ""),
        ("", ""),
    ],
)
def test_slugify_contract(title, expected):
    """Each documented rule produces the expected slug."""
    assert slugify(title) == expected
