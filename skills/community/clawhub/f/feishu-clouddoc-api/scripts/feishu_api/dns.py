from __future__ import annotations

import socket
from typing import Any


FEISHU_HOST = "open.feishu.cn"
FALLBACK_IPV4 = (
    "101.89.125.72",
    "117.24.169.93",
    "106.227.20.100",
)


def install_feishu_dns_fallback() -> None:
    """Install a process-local DNS fallback for Feishu OpenAPI only."""
    if getattr(socket, "_openclaw_feishu_dns_fallback", False):
        return

    original_getaddrinfo = socket.getaddrinfo

    def patched_getaddrinfo(
        host: str | bytes | None,
        port: str | int | None,
        family: int = 0,
        type: int = 0,
        proto: int = 0,
        flags: int = 0,
    ) -> list[Any]:
        hostname = host.decode("utf-8", errors="ignore") if isinstance(host, bytes) else host
        if str(hostname or "").lower() != FEISHU_HOST:
            return original_getaddrinfo(host, port, family, type, proto, flags)

        try:
            return original_getaddrinfo(host, port, family, type, proto, flags)
        except socket.gaierror:
            pass

        if family == socket.AF_INET6:
            raise socket.gaierror(socket.EAI_NONAME, "Name or service not known")

        results: list[Any] = []
        for ip in FALLBACK_IPV4:
            results.extend(original_getaddrinfo(ip, port, socket.AF_INET, type, proto, flags))
        return results

    socket.getaddrinfo = patched_getaddrinfo
    socket._openclaw_feishu_dns_fallback = True
