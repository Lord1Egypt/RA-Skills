"""Shared validators for ClawShorts."""
from __future__ import annotations

import re
from typing import Any

__all__ = ["validate_ipv4", "validate_ip", "ip_to_slug"]


def validate_ipv4(ip: str) -> bool:
    """Validate an IPv4 address.

    Returns True if the string is a valid dotted-quad IPv4 address
    where every octet is in the range 0-255.
    """
    if not isinstance(ip, str):
        return False
    pattern = r"^(\d{1,3}\.){3}\d{1,3}$"
    if not re.match(pattern, ip):
        return False
    return all(0 <= int(o) <= 255 for o in ip.split("."))


def ip_to_slug(ip: str) -> str:
    """Convert an IP address to a safe slug for use in filenames.

    Example: "192.168.1.100" -> "192-168-1-100"
    """
    return ip.replace(".", "-")


# Alias for backwards compatibility
validate_ip = validate_ipv4
