import asyncio
import ipaddress
import json
import socket
import subprocess
from dataclasses import dataclass
from typing import Iterable

from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class NetworkAddress:
    interface: str
    family: str
    address: str


def _server_hosts() -> set[str]:
    host = settings.SERVER_HOST.strip()
    if host in {"0.0.0.0", "::", ""}:
        return {"0.0.0.0", "::"}
    return {host}


def _is_wildcard_bind() -> bool:
    return bool(_server_hosts() & {"0.0.0.0", "::"})


def _url_host(address: str) -> str:
    ip = ipaddress.ip_address(address)
    return f"[{address}]" if ip.version == 6 else address


def _address_url(address: str) -> str:
    return f"http://{_url_host(address)}:{settings.SERVER_PORT}"


def _parse_ip_json(output: str) -> list[NetworkAddress]:
    addresses: list[NetworkAddress] = []
    for link in json.loads(output):
        ifname = link.get("ifname")
        flags = set(link.get("flags") or [])
        if not ifname or "UP" not in flags:
            continue

        for addr in link.get("addr_info") or []:
            family = addr.get("family")
            local = addr.get("local")
            if family not in {"inet", "inet6"} or not local:
                continue

            try:
                parsed = ipaddress.ip_address(local)
            except ValueError:
                continue

            if parsed.is_loopback or parsed.is_link_local:
                continue

            addresses.append(
                NetworkAddress(
                    interface=ifname,
                    family="ipv4" if parsed.version == 4 else "ipv6",
                    address=str(parsed),
                )
            )
    return addresses


def _hostname_addresses() -> list[NetworkAddress]:
    found: dict[str, NetworkAddress] = {}
    hostname = socket.gethostname()
    for info in socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP):
        address = info[4][0]
        try:
            parsed = ipaddress.ip_address(address)
        except ValueError:
            continue
        if parsed.is_loopback or parsed.is_link_local:
            continue
        found[str(parsed)] = NetworkAddress(
            interface="hostname",
            family="ipv4" if parsed.version == 4 else "ipv6",
            address=str(parsed),
        )
    return sorted(found.values(), key=lambda item: (item.family, item.address))


def active_addresses() -> list[NetworkAddress]:
    try:
        result = subprocess.run(
            ["ip", "-j", "addr", "show"],
            check=True,
            capture_output=True,
            text=True,
            timeout=2,
        )
        return sorted(
            _parse_ip_json(result.stdout),
            key=lambda item: (item.interface, item.family, item.address),
        )
    except Exception as exc:
        logger.warning(f"Falling back to hostname network discovery: {exc}")
        return _hostname_addresses()


def current_bindings() -> dict:
    wildcard = _is_wildcard_bind()
    configured_hosts = sorted(_server_hosts())
    addresses = active_addresses()

    if wildcard:
        urls = [_address_url(item.address) for item in addresses]
        bound_addresses = addresses
    else:
        configured = set(configured_hosts)
        bound_addresses = [item for item in addresses if item.address in configured]
        urls = [_address_url(host) for host in configured_hosts]

    return {
        "server_host": settings.SERVER_HOST,
        "server_port": settings.SERVER_PORT,
        "wildcard_bind": wildcard,
        "interfaces": [
            {
                "name": item.interface,
                "family": item.family,
                "address": item.address,
                "url": _address_url(item.address),
                "bound": wildcard or item.address in configured_hosts,
            }
            for item in addresses
        ],
        "active_urls": urls,
        "bound_addresses": [
            {
                "name": item.interface,
                "family": item.family,
                "address": item.address,
                "url": _address_url(item.address),
            }
            for item in bound_addresses
        ],
    }


def _address_keys(addresses: Iterable[NetworkAddress]) -> set[tuple[str, str, str]]:
    return {(item.interface, item.family, item.address) for item in addresses}


async def monitor_network_bindings(interval: int = 5) -> None:
    previous = _address_keys(active_addresses())
    logger.info(
        "Network binding monitor started",
        extra={
            "operation": "network_bind_monitor_start",
            "server_host": settings.SERVER_HOST,
            "server_port": settings.SERVER_PORT,
            "wildcard_bind": _is_wildcard_bind(),
        },
    )

    while True:
        await asyncio.sleep(interval)
        current_addresses = active_addresses()
        current = _address_keys(current_addresses)
        added = current - previous
        removed = previous - current

        if added or removed:
            logger.info(
                f"Network interfaces changed: added={sorted(added)} removed={sorted(removed)}",
                extra={
                    "operation": "network_bind_change",
                    "added": sorted(added),
                    "removed": sorted(removed),
                    "wildcard_bind": _is_wildcard_bind(),
                    "active_urls": current_bindings()["active_urls"],
                },
            )

        previous = current
