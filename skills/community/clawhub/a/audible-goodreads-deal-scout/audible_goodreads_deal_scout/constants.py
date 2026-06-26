from __future__ import annotations

import re


MIN_PYTHON = (3, 9)
HTTP_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)
DEFAULT_THRESHOLD = 3.8
DEFAULT_FRESHNESS_DAYS = 180
DEFAULT_NOTES_WARNING_CHARS = 50_000
FIT_REVIEW_SUMMARY_LIMIT = 500
SUPPORTED_PRIVACY_MODES = {"normal", "minimal"}
SUPPORTED_DELIVERY_POLICIES = {"positive_only", "always_full", "summary_on_non_match"}
DEFAULT_DELIVERY_POLICY = "positive_only"
FIT_NO_PERSONAL_DATA = "Fit: No personal preference data was configured, so this recommendation is based only on the public Goodreads score."
FIT_MODEL_UNAVAILABLE = "Fit: Personalized fit feedback is unavailable right now, but the recommendation decision still completed."
FIT_MODEL_UNAVAILABLE_TO_READ = "Fit: Strong match, on your 'to-read' shelf. Personalized fit feedback is unavailable right now, but this is already on the books you explicitly want to read."
AUTHOR_SUFFIXES = {"jr", "sr", "ii", "iii", "iv", "v"}
AUTHOR_ROLE_PATTERNS = (
    r"\bnarrated by\b",
    r"\bforeword by\b",
    r"\bafterword by\b",
    r"\bintroduction by\b",
    r"\bwith\b",
    r"\bfull cast\b",
)
AUDIBLE_BLOCK_MARKERS = (
    "captcha",
    "robot check",
    "automated access",
)
PROMOTION_MARKERS = (
    "daily deal",
    "deal ends",
    "angebot endet",
    "begrenztes angebot",
    "promotion ends",
)
PRICE_TOKEN_RE = re.compile(
    r"(?:(?P<prefix>[£$€])\s*(?P<prefix_amount>\d[\d.,]*))|(?:(?P<suffix_amount>\d[\d.,]*)\s*(?P<suffix>[£$€]))"
)
CSV_ROLE_DEFAULTS: dict[str, tuple[str, ...]] = {
    "title": ("Title",),
    "author": ("Author",),
    "shelf": ("Exclusive Shelf",),
    "bookshelves": ("Bookshelves",),
    "rating": ("My Rating",),
    "review": ("My Review",),
    "average_rating": ("Average Rating", "Avg Rating", "Avg. Rating", "Book Average Rating", "Community Rating"),
    "date_read": ("Date Read",),
    "date_added": ("Date Added",),
    "isbn": ("ISBN",),
    "isbn13": ("ISBN13",),
    "book_id": ("Book Id",),
}

UNICODE_BOLD_TRANSLATION = str.maketrans(
    {
        **{chr(ord("A") + index): chr(0x1D5D4 + index) for index in range(26)},
        **{chr(ord("a") + index): chr(0x1D5EE + index) for index in range(26)},
        **{chr(ord("0") + index): chr(0x1D7EC + index) for index in range(10)},
    }
)
