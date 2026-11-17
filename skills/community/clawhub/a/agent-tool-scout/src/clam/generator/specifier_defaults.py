"""Per-app default values for specifier and document type parameters.

When a command's direct parameter is of type "specifier" or "document",
the generated CLI can use a sensible default (e.g. "active tab of window 1"
for Chrome) so the user doesn't need to manually construct AppleScript
object references.
"""

from __future__ import annotations


# Default specifier reference per app — for "specifier" type direct params.
# The value is an AppleScript object reference string used when the user
# doesn't pass an explicit target.
_SPECIFIER_DEFAULTS: dict[str, str] = {
    "google-chrome": "active tab of window 1",
    "arc": "active tab of window 1",
    "doubao": "active tab of window 1",
    "safari": "current tab of window 1",
    "finder": "Finder window 1",
}

# Default for "document" type direct params — works for most apps.
DOCUMENT_DEFAULT = "front document"


def get_specifier_default(app_id: str, param_type: str) -> str | None:
    """Return the default AppleScript reference for a specifier/document param.

    Returns None if no default is available (the command stays unsupported).
    """
    if param_type == "document":
        return DOCUMENT_DEFAULT
    if param_type == "specifier":
        return _SPECIFIER_DEFAULTS.get(app_id)
    return None
