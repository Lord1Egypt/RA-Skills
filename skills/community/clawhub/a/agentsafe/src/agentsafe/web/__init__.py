"""Public web pages served by the MCP HTTP transport.

Pages:
  /         - landing page (pricing, Claude config, legal links, Tally CTA)
  /terms    - Terms of Service rendered from TERMS_OF_SERVICE.md
  /privacy  - Privacy Policy rendered from PRIVACY_POLICY.md
  /refund   - Refund Policy rendered from REFUND_POLICY.md
"""

from agentsafe.web.access_log import ACCESS_LOG_RETENTION_DAYS, AccessLogMiddleware, AccessLogStore
from agentsafe.web.pages import (
    INDEX_HTML,
    LegalDocumentMissingError,
    legal_html,
    legal_markdown,
)

__all__ = [
    "INDEX_HTML",
    "ACCESS_LOG_RETENTION_DAYS",
    "AccessLogMiddleware",
    "AccessLogStore",
    "LegalDocumentMissingError",
    "legal_html",
    "legal_markdown",
]
