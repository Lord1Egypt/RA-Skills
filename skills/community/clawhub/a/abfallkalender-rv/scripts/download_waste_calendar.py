#!/usr/bin/env python3
"""Download waste calendars from the Landkreis Ravensburg Athos portal."""

from __future__ import annotations

import argparse
import difflib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from http.cookiejar import CookieJar
from pathlib import Path
from typing import Iterable


BASE_URL = (
    "https://athos-onlinedienste.rv.de/"
    "WasteManagementRavensburgPrivat/WasteManagementServlet"
)
START_URL = f"{BASE_URL}?SubmitAction=wasteDisposalServices&InFrameMode=FALSE"
USER_AGENT = "AgentBerry waste-calendar downloader/1.0"
DEFAULT_CACHE_MAX_AGE_DAYS = 7


class WasteCalendarError(RuntimeError):
    """Domain-specific error for clean CLI output."""


@dataclass
class PortalState:
    hidden_fields: dict[str, str]
    html: str


@dataclass
class CacheEntry:
    data_path: Path
    meta_path: Path
    metadata: dict[str, object]


def normalize(value: str) -> str:
    value = html.unescape(value or "")
    value = value.replace("\xa0", " ")
    value = value.strip().casefold()
    value = re.sub(r"\s+", " ", value)
    return value


def slugify(value: str) -> str:
    value = normalize(value)
    value = value.replace(" ", "-")
    value = re.sub(r"[^a-z0-9._-]", "-", value)
    value = re.sub(r"-{2,}", "-", value)
    return value.strip("-") or "value"


def build_opener() -> urllib.request.OpenerDirector:
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))
    opener.addheaders = [("User-Agent", USER_AGENT)]
    return opener


def fetch_text(
    opener: urllib.request.OpenerDirector,
    url: str,
    data: bytes | None = None,
    headers: dict[str, str] | None = None,
) -> tuple[str, urllib.response.addinfourl]:
    request = urllib.request.Request(url, data=data, headers=headers or {})
    try:
        response = opener.open(request, timeout=30)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise WasteCalendarError(f"HTTP {exc.code} from portal: {body[:200]}") from exc
    except urllib.error.URLError as exc:
        raise WasteCalendarError(f"Portal not reachable: {exc.reason}") from exc
    content = response.read().decode("utf-8", errors="replace")
    return content, response


def fetch_binary(
    opener: urllib.request.OpenerDirector,
    url: str,
    payload: dict[str, str],
) -> tuple[bytes, urllib.response.addinfourl]:
    data = urllib.parse.urlencode(payload).encode("utf-8")
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    request = urllib.request.Request(url, data=data, headers=headers)
    try:
        response = opener.open(request, timeout=30)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise WasteCalendarError(f"Download failed with HTTP {exc.code}: {body[:200]}") from exc
    except urllib.error.URLError as exc:
        raise WasteCalendarError(f"Download failed: {exc.reason}") from exc
    return response.read(), response


def parse_hidden_fields(page_html: str) -> dict[str, str]:
    pattern = re.compile(r'NAME="([^"]+)" ID="[^"]*"(?: VALUE="([^"]*)")? TYPE="HIDDEN"')
    return {name: value or "" for name, value in pattern.findall(page_html)}


def build_cache_key(city: str, street: str, house_number: str, house_number_suffix: str) -> str:
    parts = [
        slugify(city),
        slugify(street),
        slugify(house_number),
        slugify(house_number_suffix or "nosuffix"),
    ]
    return "__".join(parts)


def default_cache_dir() -> Path:
    return Path.home() / ".cache" / "abfallkalender-rv"


def cache_paths(
    cache_dir: Path,
    city: str,
    street: str,
    house_number: str,
    house_number_suffix: str,
    file_format: str,
) -> tuple[Path, Path]:
    key = build_cache_key(city, street, house_number, house_number_suffix)
    base = cache_dir / key
    return base.with_suffix(f".{file_format}"), base.with_suffix(".json")


def load_cache_entry(
    cache_dir: Path,
    city: str,
    street: str,
    house_number: str,
    house_number_suffix: str,
    file_format: str,
) -> CacheEntry | None:
    data_path, meta_path = cache_paths(
        cache_dir,
        city=city,
        street=street,
        house_number=house_number,
        house_number_suffix=house_number_suffix,
        file_format=file_format,
    )
    if not data_path.exists() or not meta_path.exists():
        return None
    try:
        metadata = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return CacheEntry(data_path=data_path, meta_path=meta_path, metadata=metadata)


def is_cache_valid(
    entry: CacheEntry | None,
    city: str,
    street: str,
    house_number: str,
    house_number_suffix: str,
    file_format: str,
    max_age_days: int,
) -> bool:
    if entry is None:
        return False
    metadata = entry.metadata
    expected = {
        "city": city,
        "street": street,
        "house_number": house_number,
        "house_number_suffix": house_number_suffix,
        "format": file_format,
    }
    for key, value in expected.items():
        if normalize(str(metadata.get(key, ""))) != normalize(value):
            return False
    downloaded_at = metadata.get("downloaded_at_epoch")
    if not isinstance(downloaded_at, (int, float)):
        return False
    max_age_seconds = max_age_days * 24 * 60 * 60
    return (time.time() - float(downloaded_at)) <= max_age_seconds


def write_cache_entry(
    cache_dir: Path,
    city: str,
    street: str,
    house_number: str,
    house_number_suffix: str,
    file_format: str,
    filename: str,
    data: bytes,
) -> CacheEntry:
    data_path, meta_path = cache_paths(
        cache_dir,
        city=city,
        street=street,
        house_number=house_number,
        house_number_suffix=house_number_suffix,
        file_format=file_format,
    )
    cache_dir.mkdir(parents=True, exist_ok=True)
    data_path.write_bytes(data)
    metadata = {
        "city": city,
        "street": street,
        "house_number": house_number,
        "house_number_suffix": house_number_suffix,
        "format": file_format,
        "filename": filename,
        "downloaded_at_epoch": int(time.time()),
    }
    meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    return CacheEntry(data_path=data_path, meta_path=meta_path, metadata=metadata)


def parse_city_options(page_html: str) -> list[str]:
    match = re.search(r'<SELECT NAME="Ort" ID="Ort".*?>(.*?)</SELECT>', page_html, re.S)
    if not match:
        return []
    return [html.unescape(value) for value in re.findall(r'<OPTION VALUE="([^"]*)"', match.group(1))]


def parse_house_number_options(page_html: str) -> list[str]:
    match = re.search(r'NAME="Hausnummernwahl".*?>(.*?)</SELECT>', page_html, re.S)
    if not match:
        return []
    return [html.unescape(value) for value in re.findall(r'<OPTION VALUE="([^"]*)"', match.group(1))]


def parse_json_response(payload: str) -> dict:
    try:
        return json.loads(payload)["Response"]
    except (json.JSONDecodeError, KeyError) as exc:
        raise WasteCalendarError("Portal returned invalid JSON during Ajax step") from exc


def match_exact_or_suggest(label: str, wanted: str, candidates: Iterable[str]) -> str:
    items = list(candidates)
    normalized = {normalize(item): item for item in items}
    wanted_key = normalize(wanted)
    if wanted_key in normalized:
        return normalized[wanted_key]

    suggestions = difflib.get_close_matches(wanted, items, n=5, cutoff=0.45)
    if suggestions:
        suggestion_text = ", ".join(suggestions)
        raise WasteCalendarError(f"Unknown {label} '{wanted}'. Suggestions: {suggestion_text}")
    raise WasteCalendarError(f"Unknown {label} '{wanted}'")


def start_session(opener: urllib.request.OpenerDirector) -> PortalState:
    page_html, _ = fetch_text(opener, START_URL)
    hidden_fields = parse_hidden_fields(page_html)
    if not hidden_fields.get("SessionId"):
        raise WasteCalendarError("Portal session could not be initialized")
    return PortalState(hidden_fields=hidden_fields, html=page_html)


def ajax_city_changed(
    opener: urllib.request.OpenerDirector,
    state: PortalState,
    city: str,
) -> tuple[dict[str, str], list[str]]:
    payload = dict(state.hidden_fields)
    payload.update(
        {
            "Ajax": "TRUE",
            "AjaxOnPage": "false",
            "PageName": "Lageadresse",
            "Ort": city,
            "Strasse": "",
            "Hausnummer": "",
            "Hausnummerzusatz": "",
            "SubmitAction": "CITYCHANGED",
        }
    )
    body = urllib.parse.urlencode(payload).encode("utf-8")
    response_text, _ = fetch_text(
        opener,
        BASE_URL,
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    response = parse_json_response(response_text)
    values = {entry["name"]: entry for entry in response.get("values", [])}
    streets = [item["item"] for item in values.get("Strasse", {}).get("items", [])]
    return values, streets


def submit_address(
    opener: urllib.request.OpenerDirector,
    state: PortalState,
    city: str,
    street: str,
    house_number: str,
    house_number_suffix: str,
) -> PortalState:
    payload = dict(state.hidden_fields)
    payload.update(
        {
            "Ort": city,
            "Strasse": street,
            "Hausnummer": house_number,
            "Hausnummerzusatz": house_number_suffix,
            "SubmitAction": "forward",
        }
    )
    page_html, _ = fetch_text(
        opener,
        BASE_URL,
        data=urllib.parse.urlencode(payload).encode("utf-8"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    return PortalState(hidden_fields=parse_hidden_fields(page_html), html=page_html)


def resolve_house_number_step(
    opener: urllib.request.OpenerDirector,
    state: PortalState,
    city: str,
    street: str,
    house_number: str,
    house_number_suffix: str,
) -> PortalState:
    if state.hidden_fields.get("PageName") == "Terminliste":
        return state

    options = parse_house_number_options(state.html)
    if not options:
        raise WasteCalendarError("Portal did not return a calendar page or a house number selection")

    requested = f"{house_number}{house_number_suffix}".strip()
    try:
        chosen = match_exact_or_suggest("house number", requested, options)
    except WasteCalendarError as exc:
        option_text = ", ".join(options[:10])
        raise WasteCalendarError(f"{exc}. Available values: {option_text}") from exc

    payload = dict(state.hidden_fields)
    payload.update(
        {
            "Ort": city,
            "Strasse": street,
            "Hausnummernwahl": chosen,
            "SubmitAction": "forward",
        }
    )
    page_html, _ = fetch_text(
        opener,
        BASE_URL,
        data=urllib.parse.urlencode(payload).encode("utf-8"),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    next_state = PortalState(hidden_fields=parse_hidden_fields(page_html), html=page_html)
    if next_state.hidden_fields.get("PageName") != "Terminliste":
        raise WasteCalendarError("Portal did not reach the calendar page after house number selection")
    return next_state


def extract_filename(headers) -> str | None:
    disposition = headers.get("Content-Disposition", "")
    match = re.search(r'filename="?([^";]+)"?', disposition)
    return match.group(1) if match else None


def ensure_calendar_page(state: PortalState) -> None:
    if state.hidden_fields.get("PageName") != "Terminliste":
        raise WasteCalendarError("Portal did not reach the calendar page")
    if "filedownload_ICAL" not in state.html or "filedownload_PDF" not in state.html:
        raise WasteCalendarError("Calendar page does not contain download actions")


def download_calendar(
    opener: urllib.request.OpenerDirector,
    state: PortalState,
    city: str,
    street: str,
    house_number: str,
    house_number_suffix: str,
    file_format: str,
) -> tuple[bytes, str]:
    action = {"ics": "filedownload_ICAL", "pdf": "filedownload_PDF"}[file_format]
    payload = dict(state.hidden_fields)
    payload.update(
        {
            "Ajax": "TRUE",
            "AjaxOnPage": "false",
            "Ort": city,
            "Strasse": street,
            "Hausnummer": house_number,
            "Hausnummerzusatz": house_number_suffix,
            "SubmitAction": action,
        }
    )
    data, response = fetch_binary(opener, BASE_URL, payload)
    content_type = response.headers.get("Content-Type", "")
    if file_format == "ics" and "text/calendar" not in content_type:
        preview = data[:200].decode("utf-8", errors="replace")
        raise WasteCalendarError(f"Portal did not return ICS data: {preview}")
    if file_format == "pdf" and "application/pdf" not in content_type:
        preview = data[:200].decode("utf-8", errors="replace")
        raise WasteCalendarError(f"Portal did not return PDF data: {preview}")
    filename = extract_filename(response.headers) or f"waste-calendar.{file_format}"
    return data, filename


def choose_output_path(requested_path: str | None, filename: str) -> Path:
    if requested_path:
        return Path(requested_path).expanduser().resolve()
    return Path.cwd() / filename


def write_file(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def materialize_output(
    requested_path: str | None,
    filename: str,
    data: bytes,
) -> Path:
    output_path = choose_output_path(requested_path, filename)
    write_file(output_path, data)
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--city", required=True, help="Municipality name from the portal")
    parser.add_argument("--street", required=True, help="Street name from the portal")
    parser.add_argument("--house-number", required=True, help="House number")
    parser.add_argument(
        "--house-number-suffix",
        default="",
        help="Optional house number suffix such as a or b",
    )
    parser.add_argument(
        "--format",
        choices=("ics", "pdf"),
        default="ics",
        help="Download format",
    )
    parser.add_argument("--output", help="Optional target path")
    parser.add_argument(
        "--cache-dir",
        default=str(default_cache_dir()),
        help="Cache directory for address-specific downloads",
    )
    parser.add_argument(
        "--max-cache-age-days",
        type=int,
        default=DEFAULT_CACHE_MAX_AGE_DAYS,
        help="Refresh cache after this many days",
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Always download a fresh file instead of reusing cache",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    opener = build_opener()

    try:
        cache_dir = Path(args.cache_dir).expanduser().resolve()
        if args.max_cache_age_days < 0:
            raise WasteCalendarError("--max-cache-age-days must be >= 0")

        state = start_session(opener)
        valid_cities = parse_city_options(state.html)
        city = match_exact_or_suggest("city", args.city, valid_cities)
        _, streets = ajax_city_changed(opener, state, city)
        street = match_exact_or_suggest("street", args.street, streets)
        cache_entry = None
        if not args.no_cache:
            cache_entry = load_cache_entry(
                cache_dir,
                city=city,
                street=street,
                house_number=args.house_number,
                house_number_suffix=args.house_number_suffix,
                file_format=args.format,
            )
            if is_cache_valid(
                cache_entry,
                city=city,
                street=street,
                house_number=args.house_number,
                house_number_suffix=args.house_number_suffix,
                file_format=args.format,
                max_age_days=args.max_cache_age_days,
            ):
                filename = str(cache_entry.metadata.get("filename") or cache_entry.data_path.name)
                data = cache_entry.data_path.read_bytes()
                output_path = materialize_output(args.output, filename, data)
                size = os.path.getsize(output_path)
                print(str(output_path))
                print(
                    f"Reused cached {args.format.upper()} for "
                    f"{city}, {street} {args.house_number}{args.house_number_suffix}"
                )
                print(f"Cache file: {cache_entry.data_path}")
                print(f"Size: {size} bytes")
                return 0

        state = submit_address(
            opener,
            state,
            city=city,
            street=street,
            house_number=args.house_number,
            house_number_suffix=args.house_number_suffix,
        )
        state = resolve_house_number_step(
            opener,
            state,
            city=city,
            street=street,
            house_number=args.house_number,
            house_number_suffix=args.house_number_suffix,
        )
        ensure_calendar_page(state)
        data, filename = download_calendar(
            opener,
            state,
            city=city,
            street=street,
            house_number=args.house_number,
            house_number_suffix=args.house_number_suffix,
            file_format=args.format,
        )
        if not args.no_cache:
            write_cache_entry(
                cache_dir,
                city=city,
                street=street,
                house_number=args.house_number,
                house_number_suffix=args.house_number_suffix,
                file_format=args.format,
                filename=filename,
                data=data,
            )
        output_path = materialize_output(args.output, filename, data)
        size = os.path.getsize(output_path)
        print(str(output_path))
        print(f"Downloaded {args.format.upper()} for {city}, {street} {args.house_number}{args.house_number_suffix}")
        if not args.no_cache:
            print(f"Cache dir: {cache_dir}")
        print(f"Size: {size} bytes")
        return 0
    except WasteCalendarError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
