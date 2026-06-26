"""Fliggy  MCP data source — Alibaba flight search API.

Best for: flight prices (especially Chinese domestic routes),
route-based search with comprehensive coverage.

Does NOT provide: real-time flight tracking, aircraft type, delay info,
flight number queries.

Key characteristics:
- Best domestic China coverage (covers routes GF/SK often miss)
- Supports international routes (including intl-to-intl)
- ~0.5s response time (domestic), 2-4s (international)
- Prices always in CNY (Chinese Yuan)
- No authentication required (uses public default key from official CLI)
- City-level search: one request covers all airports in a city
- HMAC-SHA256 signed requests (reverse-engineered from @fly-ai/flyai-cli v1.0.6)
"""

import base64
import gzip
import hashlib
import hmac
import json
import logging
import os
import platform
import re
import secrets
import time
import uuid
from datetime import datetime, timezone

import requests
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from airport_manager import airport_manager

logger = logging.getLogger("flyclaw.fliggy_mcp")

# ---------------------------------------------------------------------------
# Constants (from @fly-ai/flyai-cli v1.0.6 open-source bundle)
# ---------------------------------------------------------------------------
MCP_URL = "https://flyai.open.fliggy.com/mcp"
DEFAULT_API_KEY = "sk-faRn8Kp2QzXvLm9YtA4EjHcWbS7oUdG5iF3xNqV6rZ"
DEFAULT_SIGN_SECRET = "XSbdYnucPARDc9knhD8+X6hxdD1Nh6ZGI6Hadg25kBw="
X_TTID = "ai2c(sk.clawhub)"
SIGN_VER = "7"

# Cabin class mapping (English → Chinese for client-side filtering)
CABIN_CN_MAP = {
    "economy": "经济舱",
    "premium": "超级经济舱",
    "business": "商务舱",
    "first": "头等舱",
}


# ---------------------------------------------------------------------------
# Signing helpers
# ---------------------------------------------------------------------------

def _sha256_hex(s: str) -> str:
    """SHA-256 hex digest of a UTF-8 string."""
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _normalize_auth(auth: str) -> str:
    """Normalize Authorization header value (ensure 'Bearer ' prefix)."""
    auth = (auth or "").strip()
    if not auth:
        return ""
    return auth if auth.startswith("Bearer ") else f"Bearer {auth}"


def _make_signature(
    method: str, pathname: str, timestamp_ms: str,
    nonce: str, body: str, auth: str, sign_secret: str,
) -> str:
    """Compute HMAC-SHA256 signature in base64url (no padding).

    sign_string = METHOD\\nPATHNAME\\nTIMESTAMP\\nNONCE\\nSHA256(body)\\nSHA256(auth)
    """
    body_hash = _sha256_hex(body)
    auth_hash = _sha256_hex(_normalize_auth(auth))
    sign_string = f"{method}\n{pathname}\n{timestamp_ms}\n{nonce}\n{body_hash}\n{auth_hash}"
    sig = hmac.new(
        sign_secret.encode("utf-8"),
        sign_string.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return base64.urlsafe_b64encode(sig).rstrip(b"=").decode()


# ---------------------------------------------------------------------------
# x-ff-ctx context helpers (matching flyai-cli v1.0.6 protocol)
# ---------------------------------------------------------------------------

_device_id_cache: str | None = None


def _get_device_id() -> str:
    """Return a stable device ID (SHA-256 hex of a UUID4), cached in cache/.device_id."""
    global _device_id_cache
    if _device_id_cache is not None:
        return _device_id_cache

    id_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache", ".device_id")
    try:
        with open(id_path, "r") as f:
            did = f.read().strip()
            if len(did) == 64:
                _device_id_cache = did
                return did
    except FileNotFoundError:
        pass

    did = hashlib.sha256(uuid.uuid4().bytes).hexdigest()
    os.makedirs(os.path.dirname(id_path), exist_ok=True)
    with open(id_path, "w") as f:
        f.write(did)
    _device_id_cache = did
    return did


def _memory_tier_gb() -> int:
    """Map total physical memory to a tier: 2/4/8/16/20 (matches JS Nt())."""
    try:
        total_bytes = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
        total_gb = total_bytes / (1024 ** 3)
    except (ValueError, OSError):
        return 8
    for tier in (2, 4, 8, 16, 20):
        if total_gb <= tier * 1.2:
            return tier
    return 20


def _parse_language() -> str:
    """Extract short language code from LANG/LC_ALL (matches JS Vt())."""
    raw = os.environ.get("LC_ALL") or os.environ.get("LANG") or "en"
    m = re.match(r"([a-zA-Z]{2,3}(?:[_-][a-zA-Z]{2})?)", raw)
    return m.group(1).replace("_", "-") if m else "en"


def _build_context() -> dict:
    """Build the full context dict for x-ff-ctx header."""
    mem_tier = _memory_tier_gb()
    cpus = os.cpu_count() or 1
    os_type = platform.system().lower()
    arch = platform.machine()
    os_release_major = platform.release().split(".")[0]
    node_version = "v22.22.0"
    lang = _parse_language()

    return {
        "machine": {
            "platform": os_type,
            "arch": arch,
            "cpus": cpus,
            "memoryTierGB": mem_tier,
            "osType": os_type,
            "nodeVersion": node_version,
            "osReleaseMajor": os_release_major,
        },
        "fingerprint": {
            "language": lang,
            "platform": os_type,
            "userAgent": f"flyai-cli/1.0.6 (Node.js {node_version}; {os_type} {arch})",
            "hardwareConcurrency": cpus,
            "deviceMemory": min(8, max(2, mem_tier)),
            "clientSurface": "cli",
            "timezoneOffset": int(datetime.now(timezone.utc).astimezone().utcoffset().total_seconds() // 60),
            "deviceId": _get_device_id(),
        },
    }


# ---------------------------------------------------------------------------
# Source class
# ---------------------------------------------------------------------------

class FliggyMCPSource:
    """Fliggy MCP flight search data source."""

    def __init__(
        self,
        timeout: int = 10,
        api_key: str | None = None,
        sign_secret: str | None = None,
    ):
        self.timeout = timeout
        self.api_key = api_key or DEFAULT_API_KEY
        self.sign_secret = sign_secret or DEFAULT_SIGN_SECRET

    # ------------------------------------------------------------------
    # x-ff-ctx protocol
    # ------------------------------------------------------------------

    def _make_ff_ctx(self) -> str:
        """Build x-ff-ctx header: gzip(context) optionally encrypted with AES-256-GCM."""
        ctx_json = json.dumps(_build_context()).encode("utf-8")
        compressed = gzip.compress(ctx_json)
        secret = (self.sign_secret or "").strip()
        if not secret:
            return base64.b64encode(compressed).decode()
        # AES-256-GCM encryption
        key = hashlib.sha256(secret.encode("utf-8")).digest()
        iv = os.urandom(12)
        encrypted = AESGCM(key).encrypt(iv, compressed, None)
        return base64.b64encode(bytes([0x01]) + iv + encrypted).decode()

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def query_by_flight(self, flight_number: str) -> list[dict]:
        """Fliggy does not support flight number queries."""
        return []

    def query_by_route(
        self,
        origin: str,
        destination: str,
        date: str,
        *,
        return_date: str | None = None,
        cabin: str = "economy",
        stops: int | str = 0,
        limit: int | None = None,
        timeout: int | None = None,
    ) -> list[dict]:
        """Search flights via Fliggy MCP API.

        Args:
            origin: IATA code or Chinese city name (e.g. "PVG", "上海")
            destination: IATA code or Chinese city name
            date: departure date YYYY-MM-DD
            return_date: return date for round-trip (None = one-way)
            cabin: economy/premium/business/first (client-side filtering)
            stops: 0/1/2/"any" (client-side filtering)
            limit: max results (None = API default ~10)
            timeout: per-request timeout override
        """
        try:
            return self._do_query(
                origin, destination, date,
                return_date=return_date, cabin=cabin,
                stops=stops, limit=limit,
                timeout=timeout or self.timeout,
            )
        except Exception as e:
            logger.warning("Fliggy MCP query failed: %s", e)
            return []

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _call_mcp(self, tool_name: str, arguments: dict, timeout: int) -> dict | None:
        """Call the Fliggy MCP server (tools/call).

        Returns parsed JSON response or None on failure.
        """
        pathname = "/mcp"
        body = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
        })
        timestamp_ms = str(int(time.time() * 1000))
        nonce = secrets.token_hex(16)
        auth = f"Bearer {self.api_key}"
        sig = _make_signature(
            "POST", pathname, timestamp_ms, nonce,
            body, auth, self.sign_secret,
        )

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
            "Authorization": auth,
            "x-ff-ctx": self._make_ff_ctx(),
            "x-ttid": X_TTID,
            "User-Agent": "flyai-cli/1.0.6",
            "x-flyai-ts": timestamp_ms,
            "x-flyai-sign-ver": SIGN_VER,
            "x-flyai-sign-alg": "hmac-sha256",
            "x-flyai-nonce": nonce,
            "x-flyai-sign": sig,
        }

        resp = requests.post(MCP_URL, headers=headers, data=body, timeout=timeout)
        resp.raise_for_status()
        rj = resp.json()

        # Extract text content from MCP response
        content = rj.get("result", {}).get("content", [{}])
        if not content:
            return None
        text = content[0].get("text")
        if not text:
            return None
        return json.loads(text)

    def _do_query(
        self,
        origin: str, destination: str, date: str,
        *, return_date: str | None = None,
        cabin: str = "economy", stops: int | str = 0,
        limit: int | None = None, timeout: int = 10,
    ) -> list[dict]:
        """Execute search and parse results to FlightRecord dicts."""
        api_args = {
            "origin": origin,
            "destination": destination,
            "depDate": date,
        }
        if return_date:
            api_args["backDate"] = return_date
        if limit is not None:
            api_args["limit"] = limit

        data = self._call_mcp("search_flight", api_args, timeout)
        if not data:
            logger.debug("Fliggy: empty response for %s→%s", origin, destination)
            return []

        items = data.get("data", {}).get("itemList")
        if not items:
            msg = data.get("message", "")
            if msg:
                logger.debug("Fliggy: %s", msg)
            return []

        records = []
        for item in items:
            rec = self._parse_item(item, return_date is not None)
            if rec is None:
                continue
            # Client-side stops filter (server-side journeyType param is broken)
            if stops != "any":
                max_stops = int(stops)
                if rec.get("stops", 0) > max_stops:
                    continue
            # Client-side cabin filter (server-side seatClassName param is broken)
            if cabin != "economy":
                expected_cn = CABIN_CN_MAP.get(cabin, "")
                actual_cn = rec.get("cabin_class", "")
                if expected_cn and actual_cn and expected_cn != actual_cn:
                    continue
            records.append(rec)

        return records

    def _parse_item(self, item: dict, is_round_trip: bool) -> dict | None:
        """Parse a single Fliggy API item into a FlightRecord dict."""
        journeys = item.get("journeys", [])
        if not journeys or not journeys[0].get("segments"):
            return None

        # Outbound journey
        outbound = journeys[0]
        segs = outbound["segments"]
        first_seg = segs[0]
        last_seg = segs[-1]

        # Parse price
        try:
            price = float(item.get("ticketPrice", 0))
        except (ValueError, TypeError):
            price = None
        if price == 0:
            price = None

        # Build flight number: for multi-segment, use first segment
        flight_number = first_seg.get("marketingTransportNo", "")

        # Parse times: "2026-04-10 09:05:00" → "2026-04-10T09:05"
        dep_raw = first_seg.get("depDateTime", "")
        arr_raw = last_seg.get("arrDateTime", "")
        dep_iso = dep_raw.replace(" ", "T")[:16] if dep_raw else None
        arr_iso = arr_raw.replace(" ", "T")[:16] if arr_raw else None

        # Duration
        try:
            duration = int(outbound.get("totalDuration") or first_seg.get("duration", 0))
        except (ValueError, TypeError):
            duration = None

        # City names from airport_manager (more reliable than Fliggy's)
        origin_iata = first_seg.get("depStationCode", "")
        dest_iata = last_seg.get("arrStationCode", "")
        origin_info = airport_manager.get_info(origin_iata)
        dest_info = airport_manager.get_info(dest_iata)

        rec = {
            "flight_number": flight_number,
            "airline": first_seg.get("marketingTransportName", ""),
            "origin_iata": origin_iata,
            "origin_city": (origin_info or {}).get("city_cn", "")
                           or first_seg.get("depCityName", ""),
            "destination_iata": dest_iata,
            "destination_city": (dest_info or {}).get("city_cn", "")
                                or last_seg.get("arrCityName", ""),
            "scheduled_departure": dep_iso,
            "scheduled_arrival": arr_iso,
            "actual_departure": None,
            "actual_arrival": None,
            "status": "",
            "aircraft_type": "",
            "delay_minutes": None,
            "price": price,
            "currency": "CNY",
            "stops": len(segs) - 1,
            "duration_minutes": duration,
            "cabin_class": first_seg.get("seatClassName", ""),
            "source": "fliggy_mcp",
        }

        # Outbound segments (all legs, including direct flights with len=1)
        seg_list = []
        for seg in segs:
            dep_raw = seg.get("depDateTime", "")
            arr_raw = seg.get("arrDateTime", "")
            seg_list.append({
                "flight_number": seg.get("marketingTransportNo", ""),
                "origin_iata": seg.get("depStationCode", ""),
                "destination_iata": seg.get("arrStationCode", ""),
                "departure": dep_raw.replace(" ", "T")[:16] if dep_raw else "",
                "arrival": arr_raw.replace(" ", "T")[:16] if arr_raw else "",
                "duration_minutes": int(seg.get("duration") or 0),
            })
        rec["segments"] = seg_list
        rec["layover_cities"] = [s["destination_iata"] for s in seg_list[:-1]]
        rec["layover_minutes"] = _calc_layover_minutes(seg_list)
        rec["max_layover_minutes"] = max(rec["layover_minutes"]) if rec["layover_minutes"] else 0

        # Round trip: parse return journey
        if is_round_trip and len(journeys) >= 2:
            ret = journeys[1]
            ret_segs = ret.get("segments", [])
            if ret_segs:
                ret_first = ret_segs[0]
                ret_last = ret_segs[-1]
                ret_dep = ret_first.get("depDateTime", "")
                ret_arr = ret_last.get("arrDateTime", "")
                try:
                    ret_dur = int(ret.get("totalDuration") or ret_first.get("duration", 0))
                except (ValueError, TypeError):
                    ret_dur = None
                rec["trip_type"] = "round_trip"
                rec["return_flight_number"] = ret_first.get("marketingTransportNo", "")
                rec["return_airline"] = ret_first.get("marketingTransportName", "")
                rec["return_departure"] = ret_dep.replace(" ", "T")[:16] if ret_dep else None
                rec["return_arrival"] = ret_arr.replace(" ", "T")[:16] if ret_arr else None
                rec["return_stops"] = len(ret_segs) - 1
                rec["return_duration_minutes"] = ret_dur
                # Return segments
                ret_seg_list = []
                for seg in ret_segs:
                    dep_raw = seg.get("depDateTime", "")
                    arr_raw = seg.get("arrDateTime", "")
                    ret_seg_list.append({
                        "flight_number": seg.get("marketingTransportNo", ""),
                        "origin_iata": seg.get("depStationCode", ""),
                        "destination_iata": seg.get("arrStationCode", ""),
                        "departure": dep_raw.replace(" ", "T")[:16] if dep_raw else "",
                        "arrival": arr_raw.replace(" ", "T")[:16] if arr_raw else "",
                        "duration_minutes": int(seg.get("duration") or 0),
                    })
                rec["return_segments"] = ret_seg_list
                rec["return_layover_cities"] = [s["destination_iata"] for s in ret_seg_list[:-1]]
                rec["return_layover_minutes"] = _calc_layover_minutes(ret_seg_list)
                rec["return_max_layover_minutes"] = (
                    max(rec["return_layover_minutes"]) if rec["return_layover_minutes"] else 0
                )
        elif is_round_trip:
            rec["trip_type"] = "round_trip"

        return rec


def _calc_layover_minutes(seg_list: list) -> list[int]:
    """Calculate ground time (minutes) between consecutive segments.

    seg_list items must have 'arrival' and 'departure' as 'YYYY-MM-DDTHH:MM' strings.
    Returns a list of length len(seg_list)-1.
    """
    result = []
    fmt = "%Y-%m-%dT%H:%M"
    for i in range(len(seg_list) - 1):
        arr_str = seg_list[i].get("arrival", "")
        dep_str = seg_list[i + 1].get("departure", "")
        try:
            arr_dt = datetime.strptime(arr_str[:16], fmt)
            dep_dt = datetime.strptime(dep_str[:16], fmt)
            result.append(int((dep_dt - arr_dt).total_seconds() / 60))
        except (ValueError, TypeError):
            result.append(0)
    return result
