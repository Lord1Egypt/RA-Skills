"""Unit tests for scripts/lib/profile.py.

The parser handles two profile.md forms in the wild — the schema form
documented in templates/profile.example.md, and the heading-list form
used in real-world profile.md files. Cover both, plus the edge cases
that previously slipped through silently.
"""
from lib.profile import parse_profile


def test_parse_profile_schema_form_with_path_keys():
    """Form (a): `reference_photos:` then `- path: /...` entries."""
    text = """\
- name: Jane Doe
- email: jane@example.com
- gender: m

## Sizes
- shirt: L
- pant: 32x32

reference_photos:
  - path: /home/jane/portrait.jpg
  - path: /home/jane/fullbody.jpg
"""
    out = parse_profile(text)
    assert out["name"] == "Jane Doe"
    assert out["email"] == "jane@example.com"
    assert out["gender"] == "m"
    assert out["reference_photos"] == [
        "/home/jane/portrait.jpg",
        "/home/jane/fullbody.jpg",
    ]
    assert out["sizes"] == {"shirt": "L", "pant": "32x32"}


def test_parse_profile_heading_list_form_with_spaces_in_paths():
    """Form (b): `## Reference photos` heading + bare `- /path/...` lines.

    This is the form the real .workspace/profile.md uses, and the form that
    previously broke parsing (caused the verify-face gate to silently skip).
    Paths contain spaces ("Styling example pics") and trailing parenthetical
    descriptions; both should be handled.
    """
    text = """\
- name: Nick Merwin
- gender: m

## Reference photos
- /Users/nickmerwin/Pictures/Styling example pics/SCR-20260426-pppa.jpeg  (full body, cream linen)
- /Users/nickmerwin/Pictures/Styling example pics/SCR-20260426-pqar.jpeg  (full body, white tee + walk short)
- /Users/nickmerwin/Pictures/Styling example pics/SCR-20260426-pozh.jpeg  (full body, shirtless boat — build anchor)
"""
    out = parse_profile(text)
    assert out["reference_photos"] == [
        "/Users/nickmerwin/Pictures/Styling example pics/SCR-20260426-pppa.jpeg",
        "/Users/nickmerwin/Pictures/Styling example pics/SCR-20260426-pqar.jpeg",
        "/Users/nickmerwin/Pictures/Styling example pics/SCR-20260426-pozh.jpeg",
    ]


def test_parse_profile_no_reference_photos_returns_empty():
    """Profile without a Reference photos block: no crash, no key."""
    text = """\
- name: Jane Doe
- gender: w
"""
    out = parse_profile(text)
    assert "reference_photos" not in out


def test_parse_profile_dedups_repeated_paths():
    """Same path repeated under the heading: keep first, drop dup."""
    text = """\
## Reference photos
- /home/jane/portrait.jpg
- /home/jane/portrait.jpg
- /home/jane/fullbody.jpg
"""
    out = parse_profile(text)
    assert out["reference_photos"] == [
        "/home/jane/portrait.jpg",
        "/home/jane/fullbody.jpg",
    ]


def test_parse_profile_drops_relative_paths():
    """Relative paths are filtered out (defends against parenthetical
    comments that look path-like)."""
    text = """\
## Reference photos
- /home/jane/portrait.jpg
- portrait.jpg
- ../relative/file.jpg
"""
    out = parse_profile(text)
    assert out["reference_photos"] == ["/home/jane/portrait.jpg"]


def test_parse_profile_coerces_bools_and_nulls():
    """`true` / `false` / `null` values should coerce. Empty values
    (`key:` with nothing after) are dropped — the regex requires at
    least one non-whitespace character in the value."""
    text = """\
- pima_account_linked: true
- jwt: null
- preferred_lookbook_host_auto: false
- empty_field:
"""
    out = parse_profile(text)
    assert out["pima_account_linked"] is True
    assert out["preferred_lookbook_host_auto"] is False
    assert out["jwt"] is None
    # Empty values are silently dropped, not stored as None.
    assert "empty_field" not in out


def test_parse_profile_strips_quoted_values():
    """Single + double quotes are stripped from values."""
    text = """\
- style_ethos: "relaxed European cool"
- name: 'Jane Doe'
"""
    out = parse_profile(text)
    assert out["style_ethos"] == "relaxed European cool"
    assert out["name"] == "Jane Doe"


def test_parse_profile_sizes_block_only_under_heading():
    """`shirt:` outside `## Sizes` should not be captured into sizes."""
    text = """\
shirt: should-not-be-captured-as-size

## Sizes
- shirt: L
- pant: 32x32

## Style ethos
- shirt: should-not-be-captured-either
"""
    out = parse_profile(text)
    assert out["sizes"] == {"shirt": "L", "pant": "32x32"}


def test_parse_profile_handles_inline_comments():
    """`key: value  # comment` strips the comment."""
    text = """\
- gender: m  # male
- home_zip: 90291  # Venice
- lookbook_votes_kv_id: 0e0b9122c04141f8b79b43d1081b3697  # Cloudflare KV
"""
    out = parse_profile(text)
    assert out["gender"] == "m"
    assert out["home_zip"] == "90291"
    assert out["lookbook_votes_kv_id"] == "0e0b9122c04141f8b79b43d1081b3697"


def test_parse_profile_preferred_link_payment_methods():
    """Purpose-specific Link card preferences are stored by last4 only."""
    text = """\
preferred_link_payment_methods:
  clothing: "0896"  # personal clothing card
  business: '3410'
  invalid: "not-a-last4"
"""
    out = parse_profile(text)
    assert out["preferred_link_payment_methods"] == {
        "clothing": "0896",
        "business": "3410",
    }


def test_parse_profile_path_form_takes_precedence_over_heading():
    """If the schema form is present, use it; don't also pull from the
    heading-list form (avoid double-counting in mixed profiles)."""
    text = """\
reference_photos:
  - path: /a/b.jpg

## Reference photos
- /c/d.jpg
"""
    out = parse_profile(text)
    assert out["reference_photos"] == ["/a/b.jpg"]
    assert "/c/d.jpg" not in out["reference_photos"]


def test_parse_profile_empty_text_returns_empty_dict():
    assert parse_profile("") == {}
