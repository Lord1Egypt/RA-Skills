from dataclasses import dataclass
from typing import Any

SCHEMA_VERSION = "1.0"

IMAP_SEARCH_COMMANDS = {
    # Message flags
    "ANSWERED", "UNANSWERED", "DELETED", "UNDELETED", "DRAFT", "UNDRAFT",
    "SEEN", "UNSEEN", "FLAGGED", "UNFLAGGED", "RECENT",
    # Keywords
    "KEYWORD", "UNKEYWORD",
    # Date-based
    "ON", "BEFORE", "AFTER", "SINCE", "SENTON", "SENTBEFORE", "SENTAFTER", "SENTSINCE",
    # Content-based
    "FROM", "TO", "CC", "BCC", "SUBJECT", "BODY", "TEXT", "HEADER",
    # Size-based
    "LARGER", "SMALLER",
    # Logical operators
    "ALL", "NEW", "OLD", "NOT", "OR", "AND",
}


@dataclass
class SkillError(Exception):
    code: str
    message: str
    details: dict[str, Any] | None = None

    def as_dict(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "code": self.code,
            "message": self.message,
        }
        if self.details:
            payload["details"] = self.details
        return payload
