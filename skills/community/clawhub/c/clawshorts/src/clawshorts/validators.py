"""Shared validators for ClawShorts."""
from __future__ import annotations

import ipaddress
import re
from typing import Any

__all__ = ["validate_ipv4", "validate_ip", "ip_to_slug"]


def validate_ipv4(ip: str) -> bool:
    """Validate an IPv4 address is a reachable private IP.

    Returns True if the string is a valid dotted-quad IPv4 address
    where every octet is in the range 0-255 AND the address is a
    private (RFC 1918) or loopback address.

    Rejects public IPs to prevent accidentally targeting
    unrelated hosts on the internet.
    """
    if not isinstance(ip, str):
        return False
    try:
        addr = ipaddress.ip_address(ip)
        return addr.is_private or addr.is_loopback
    except ValueError:
        return False


def ip_to_slug(ip: str) -> str:
    """Convert an IP address to a safe slug for use in filenames.

    Example: "192.168.1.100" -> "192-168-1-100"
    """
    return ip.replace(".", "-")


# Alias for backwards compatibility
validate_ip = validate_ipv4
