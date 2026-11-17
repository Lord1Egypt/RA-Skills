"""Validate gateway origins before either CLI dispatch or REST transport."""

import ipaddress
import os
import re
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler


DEFAULT_GATEWAY_URL = "http://127.0.0.1:9765"


def validate_gateway_url(value, *, allow_remote=True):
    """Allow canonical loopback HTTP or TLS origins; never URL credentials."""
    if not isinstance(value, str) or re.search(r"[\s\\%]", value):
        raise ValueError("gateway URL contains ambiguous characters")
    parsed = urlsplit(value)
    host = parsed.hostname
    if (parsed.scheme not in {"http", "https"} or not host
            or parsed.username is not None or parsed.password is not None
            or parsed.path not in {"", "/"} or parsed.query or parsed.fragment
            or "?" in value or "#" in value):
        raise ValueError("gateway must be an HTTP(S) origin without credentials, query or fragment")
    port = parsed.port
    if port is not None and not 1 <= port <= 65535:
        raise ValueError("gateway port is invalid")
    try:
        address = ipaddress.ip_address(host)
        loopback = address.is_loopback and getattr(address, "ipv4_mapped", None) is None
    except ValueError:
        if not re.fullmatch(r"[a-zA-Z0-9]+(?:[.-][a-zA-Z0-9]+)*", host):
            raise ValueError("gateway hostname is invalid")
        loopback = host == "localhost"
    if parsed.scheme == "http" and not loopback:
        raise ValueError("remote gateways require HTTPS; use an explicitly trusted origin")
    if not loopback and not allow_remote:
        raise ValueError(
            "a remote gateway cannot be selected through DCC_MCP_BASE_URL; "
            "pass its exact approved HTTPS origin with --base-url"
        )
    return value.rstrip("/")


def resolve_gateway_url(explicit_value=None, *, environment=None):
    """Resolve an endpoint without treating inherited environment as remote trust."""
    if explicit_value is not None:
        return validate_gateway_url(explicit_value, allow_remote=True)
    env = os.environ if environment is None else environment
    inherited = env.get("DCC_MCP_BASE_URL")
    if inherited:
        return validate_gateway_url(inherited, allow_remote=False)
    return DEFAULT_GATEWAY_URL


class NoGatewayRedirect(HTTPRedirectHandler):
    """Never forward operational payloads through a redirect."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None
