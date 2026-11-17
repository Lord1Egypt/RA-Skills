"""URL slug generation for article titles."""

import re

_SEPARATORS = re.compile(r"[^A-Za-z0-9]+")


def slugify(title: str) -> str:
    """Return a lowercase ASCII slug for title.

    ASCII letters and digits are kept; every other run of characters becomes one
    hyphen, and leading or trailing hyphens are removed. Non-ASCII letters count as
    separators by design, because slugs must stay ASCII for the CDN. A title without
    ASCII letters or digits yields an empty string.
    """
    return _SEPARATORS.sub("-", title).strip("-").lower()
