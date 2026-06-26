"""Content sanitization for email notifications.

Prevents prompt injection attacks from email content.
"""

import re
from typing import Optional


# Dangerous patterns that could be used for prompt injection
DANGEROUS_PATTERNS = [
    # Instruction override attempts
    r'ignore\s+(all\s+)?previous\s+instructions?',
    r'forget\s+(all\s+)?(previous\s+)?instructions?',
    r'disregard\s+(all\s+)?instructions?',
    r'override\s+(all\s+)?instructions?',
    
    # Role manipulation
    r'you\s+are\s+now\s+',
    r'act\s+as\s+(a|an)\s+',
    r'pretend\s+(to\s+be|you\s+are)\s+',
    r'role[\s\-]*play\s+(as|that)\s+',
    
    # System prompt injection
    r'new\s+instructions?:?\s*',
    r'system\s*:\s*',
    r'assistant\s*:\s*',
    r'user\s*:\s*',
    
    # Special tokens
    r'<\|.*?\|>',
    r'\[SYSTEM\]',
    r'\[INST\]',
    r'<<.*?>>',
    
    # Escape sequences
    r'\\n\\n',
    r'\\r\\n',
]

# Invisible Unicode characters to remove (zero-width spaces, etc.)
INVISIBLE_CHARS_PATTERN = r'[\u200b-\u200f\u2028-\u202f\u205f-\u206f\ufeff\u00ad\u034f\u061c\u17b4-\u17b5\u180e\u200c\u200d]+'


def remove_invisible_chars(text: str) -> str:
    """Remove invisible Unicode characters from text.
    
    These characters are often used in HTML emails for formatting
    but appear as garbage in plain text output.
    
    Includes:
    - Zero-width spaces (U+200B, U+200C, U+200D)
    - Zero-width non-joiners/joiners
    - Word joiners, function applications, etc.
    - BOM (U+FEFF)
    - Soft hyphen (U+00AD)
    - Various other invisible formatting chars
    """
    if not text:
        return text
    return re.sub(INVISIBLE_CHARS_PATTERN, '', text)


def sanitize_for_notification(
    text: str,
    max_length: int = 500,
    placeholder: str = "[REMOVED]",
) -> str:
    """Sanitize text content for safe notification.
    
    Removes potential prompt injection patterns, invisible characters,
    and limits length.
    
    Args:
        text: The text to sanitize
        max_length: Maximum allowed length (default 500)
        placeholder: String to replace dangerous patterns with
    
    Returns:
        Sanitized text safe for inclusion in notifications
    """
    if not text:
        return ""
    
    result = text
    
    # Remove invisible Unicode characters first
    result = remove_invisible_chars(result)
    
    # Remove dangerous patterns (case-insensitive)
    for pattern in DANGEROUS_PATTERNS:
        result = re.sub(pattern, placeholder, result, flags=re.IGNORECASE)
    
    # Remove control characters except newlines and tabs
    result = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', result)
    
    # Normalize whitespace
    result = re.sub(r'\s+', ' ', result)
    
    # Truncate to max length
    if len(result) > max_length:
        result = result[:max_length].rsplit(' ', 1)[0] + "..."
    
    return result.strip()


def sanitize_sender(sender: str, max_length: int = 100) -> str:
    """Sanitize sender name/email for display.
    
    Args:
        sender: Sender name or email
        max_length: Maximum allowed length
    
    Returns:
        Sanitized sender string
    """
    if not sender:
        return "Unknown"
    
    # Remove any special characters that could be problematic
    result = re.sub(r'[<>"\']', '', sender)
    
    # Remove invisible characters
    result = remove_invisible_chars(result)
    
    # Limit length
    if len(result) > max_length:
        result = result[:max_length] + "..."
    
    return result.strip()


def sanitize_subject(subject: str, max_length: int = 100) -> str:
    """Sanitize email subject for display.
    
    Args:
        subject: Email subject
        max_length: Maximum allowed length
    
    Returns:
        Sanitized subject string
    """
    if not subject:
        return "(No subject)"
    
    # Remove invisible characters
    result = remove_invisible_chars(subject)
    
    # Remove newlines that could break formatting
    result = result.replace('\n', ' ').replace('\r', ' ')
    
    # Limit length
    if len(result) > max_length:
        result = result[:max_length].rsplit(' ', 1)[0] + "..."
    
    return result.strip()