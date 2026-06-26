"""Extraction helpers for email content.

Provides utilities to extract useful information from emails:
- Verification codes (OTP, confirmation codes)
- Action links (verify, confirm, reset password, unsubscribe)
"""

import re
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse, unquote


@dataclass
class VerificationCode:
    """Extracted verification code."""
    code: str
    context: Optional[str] = None  # e.g., "Google", "GitHub", "Your code"


@dataclass
class ActionLink:
    """Extracted action link."""
    url: str
    link_type: str  # verify, confirm, reset, unsubscribe, action
    domain: Optional[str] = None
    text: Optional[str] = None  # Link text if available


# Patterns for verification codes
VERIFICATION_PATTERNS = [
    # Numeric codes (4-8 digits)
    (r'\b(\d{4,8})\b', 'numeric'),
    # Alphanumeric codes (common formats)
    (r'\b([A-Z0-9]{4,8})\b', 'alphanumeric'),
    # Codes with dashes
    (r'\b([A-Z0-9]{3,4}-[A-Z0-9]{3,4})\b', 'dashed'),
    # Chinese verification code patterns
    (r'验证码[：:\s]*(\d{4,8})', 'chinese_numeric'),
    (r'验证码[：:\s]*([A-Z0-9]{4,8})', 'chinese_alphanumeric'),
]

# Context patterns that indicate verification codes
VERIFICATION_CONTEXTS = [
    r'verification\s*code',
    r'confirm(?:ation)?\s*code',
    r'security\s*code',
    r'OTP',
    r'one[- ]?time[- ]?password',
    r'PIN',
    r'authenticate',
    r'验证码',
    r'校验码',
    r'确认码',
    r'动态码',
    r'Your\s+(?:verification|security|confirmation)?\s*code\s+is',
    r'Enter\s+(?:this|the)\s+code',
    r'Use\s+(?:this|the)\s+code',
    r'code\s+(?:is|:)\s*[A-Z0-9]',
]

# Link patterns for different action types
LINK_PATTERNS = {
    'verify': [
        r'verify',
        r'confirm',
        r'activate',
        r'validate',
        r'认证',
        r'验证',
    ],
    'reset': [
        r'reset',
        r'change\s+password',
        r'new\s+password',
        r'forgot\s+password',
        r'重置',
        r'修改密码',
    ],
    'unsubscribe': [
        r'unsubscribe',
        r'opt[- ]?out',
        r'remove',
        r'stop\s+receiving',
        r'cancel\s+subscription',
        r'退订',
        r'取消订阅',
    ],
    'action': [
        r'click\s+here',
        r'view\s+(?:your|the)',
        r'respond',
        r'reply',
        r'accept',
        r'decline',
        r'join',
        r'start',
        r'continue',
    ],
}


def extract_verification_codes(text: str) -> list[VerificationCode]:
    """Extract verification codes from email text.

    IMPORTANT: This function ONLY extracts codes that appear near verification
    keywords. Standalone numbers are NOT extracted to avoid false positives
    (addresses, order numbers, tracking numbers, etc.).

    Args:
        text: Email body text to search

    Returns:
        List of VerificationCode objects found
    """
    if not text:
        return []

    codes = []
    seen = set()

    # Only extract codes that are near verification keywords
    # This is the ONLY extraction method to avoid false positives
    text_lower = text.lower()

    for context_pattern in VERIFICATION_CONTEXTS:
        # Find context matches
        for match in re.finditer(context_pattern, text_lower, re.IGNORECASE):
            # Look for codes in surrounding text (100 chars before and after)
            start = max(0, match.start() - 100)
            end = min(len(text), match.end() + 100)
            context_text = text[start:end]

            # Try to find codes in this context
            for code_pattern, _ in VERIFICATION_PATTERNS:
                for code_match in re.finditer(code_pattern, context_text):
                    code = code_match.group(1)
                    if code not in seen and _is_likely_code_in_context(code, context_text):
                        seen.add(code)
                        # Extract context (service name if available)
                        ctx = _extract_service_context(text, match.start())
                        codes.append(VerificationCode(code=code, context=ctx))

    return codes


def _is_likely_code(code: str) -> bool:
    """Check if a string looks like a verification code.

    Filters out things like years, prices, phone numbers, etc.
    """
    # Filter out years (2000-2100)
    if len(code) == 4 and code.isdigit():
        year = int(code)
        if 2000 <= year <= 2100:
            return False

    # Filter out common non-code patterns
    if code.lower() in ['http', 'https', 'html', 'www', 'utf8', 'json']:
        return False

    # Filter out pure letters (likely words)
    if code.isalpha():
        return False

    # Filter out very long numeric sequences (likely phone/tracking numbers)
    if code.isdigit() and len(code) > 8:
        return False

    # Filter out dates in YYYYMMDD format
    if code.isdigit() and len(code) == 8:
        if code.startswith('20'):  # Likely a date like 20260321
            return False

    return True


def _is_likely_code_in_context(code: str, context: str) -> bool:
    """Check if a code is likely a verification code given surrounding context.

    This is more strict than _is_likely_code and considers the context
    to filter out order numbers, invoice numbers, etc.
    """
    if not _is_likely_code(code):
        return False

    # Check if the code appears after order/invoice/tracking markers
    context_lower = context.lower()
    false_positive_markers = [
        'order #', 'order no', 'order:', 'invoice', 'tracking',
        'reference #', 'ref #', 'account #', 'transaction',
        'zip', 'postal', 'phone', 'tel:', 'fax:',
        # Address patterns
        'ste', 'st', 'ave', 'avenue', 'blvd', 'rd', 'road',
        'drive', 'dr', 'lane', 'ln', 'court', 'ct',
    ]

    # Look for these markers within 30 chars before the code
    code_pos = context.find(code)
    if code_pos > 0:
        before = context[max(0, code_pos - 30):code_pos].lower()
        for marker in false_positive_markers:
            if marker in before:
                return False

    return True


def _extract_service_context(text: str, position: int) -> Optional[str]:
    """Try to extract service/company name near a code."""
    # Look backwards for common patterns
    before = text[max(0, position - 200):position]

    # Pattern: "Your Google verification code" or "GitHub code"
    patterns = [
        r'(?:your\s+)?([A-Z][a-zA-Z]+)\s+(?:verification|security|confirmation)\s+code',
        r'([A-Z][a-zA-Z]+)\s+code\s+is',
        r'from\s+([A-Z][a-zA-Z]+)',
    ]

    for pattern in patterns:
        match = re.search(pattern, before, re.IGNORECASE)
        if match:
            return match.group(1)

    return None


def extract_action_links(text: str, html: Optional[str] = None) -> list[ActionLink]:
    """Extract action links from email content.

    Args:
        text: Plain text email body
        html: Optional HTML email body for better link extraction

    Returns:
        List of ActionLink objects found
    """
    links = []
    seen_urls = set()

    # Extract from HTML if available (better link text extraction)
    if html:
        links.extend(_extract_links_from_html(html, seen_urls))

    # Also extract from plain text
    links.extend(_extract_links_from_text(text, seen_urls))

    # Filter and classify links
    action_links = []
    for link in links:
        classified = _classify_link(link)
        if classified:
            action_links.append(classified)

    return action_links


def _extract_links_from_html(html: str, seen_urls: set) -> list[ActionLink]:
    """Extract links from HTML content."""
    links = []

    # Match <a href="URL">text</a>
    pattern = r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>([^<]+)</a>'

    for match in re.finditer(pattern, html, re.IGNORECASE):
        url = match.group(1).strip()
        text = match.group(2).strip()

        # Clean up URL
        url = _clean_url(url)
        if url and url not in seen_urls:
            seen_urls.add(url)
            domain = _extract_domain(url)
            links.append(ActionLink(
                url=url,
                link_type='unknown',
                domain=domain,
                text=text[:100] if text else None
            ))

    return links


def _extract_links_from_text(text: str, seen_urls: set) -> list[ActionLink]:
    """Extract links from plain text content."""
    links = []

    # Match URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'

    for match in re.finditer(url_pattern, text):
        url = match.group(0).strip()
        url = _clean_url(url)

        if url and url not in seen_urls:
            seen_urls.add(url)
            domain = _extract_domain(url)

            # Try to get context before the URL
            context_start = max(0, match.start() - 50)
            context = text[context_start:match.start()].strip()

            links.append(ActionLink(
                url=url,
                link_type='unknown',
                domain=domain,
                text=context if context else None
            ))

    return links


def _clean_url(url: str) -> str:
    """Clean and normalize a URL."""
    # Remove trailing punctuation
    url = url.rstrip('.,;:)>]')

    # Decode URL encoding for better pattern matching
    try:
        url = unquote(url)
    except Exception:
        pass

    return url


def _extract_domain(url: str) -> Optional[str]:
    """Extract domain from URL."""
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return None


def _classify_link(link: ActionLink) -> Optional[ActionLink]:
    """Classify a link by type based on URL and text."""

    # Combine URL and text for pattern matching
    check_text = f"{link.url} {link.text or ''}".lower()

    for link_type, patterns in LINK_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, check_text, re.IGNORECASE):
                return ActionLink(
                    url=link.url,
                    link_type=link_type,
                    domain=link.domain,
                    text=link.text
                )

    # Not an action link
    return None


def extract_from_email(
    subject: str,
    body_text: Optional[str] = None,
    body_html: Optional[str] = None
) -> dict:
    """Extract all useful information from an email.

    Args:
        subject: Email subject line
        body_text: Plain text body
        body_html: HTML body

    Returns:
        Dict with 'codes' and 'links' keys
    """
    # Combine subject with body for code extraction
    full_text = f"{subject}\n\n{body_text or ''}"

    codes = extract_verification_codes(full_text)
    links = extract_action_links(body_text or '', body_html)

    return {
        'codes': codes,
        'links': links,
    }
