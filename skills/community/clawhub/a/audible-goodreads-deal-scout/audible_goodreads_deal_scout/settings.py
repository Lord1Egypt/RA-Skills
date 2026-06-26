from __future__ import annotations

from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .constants import DEFAULT_DELIVERY_POLICY, DEFAULT_FRESHNESS_DAYS, DEFAULT_THRESHOLD, SUPPORTED_PRIVACY_MODES
from .shared import normalize_space, parse_int_value, prompt, read_json


def marketplace_specs() -> dict[str, dict[str, str]]:
    return {
        "us": {
            "label": "Audible US",
            "dealUrl": "https://www.audible.com/dailydeal",
            "timezone": "America/Los_Angeles",
            "currency": "USD",
            "currencySymbol": "$",
            "defaultCron": "15 1 * * *",
        },
        "uk": {
            "label": "Audible UK",
            "dealUrl": "https://www.audible.co.uk/dailydeal",
            "timezone": "Europe/London",
            "currency": "GBP",
            "currencySymbol": "£",
            "defaultCron": "15 1 * * *",
        },
        "de": {
            "label": "Audible DE",
            "dealUrl": "https://www.audible.de/dailydeal",
            "timezone": "Europe/Berlin",
            "currency": "EUR",
            "currencySymbol": "€",
            "defaultCron": "15 1 * * *",
        },
        "ca": {
            "label": "Audible CA",
            "dealUrl": "https://www.audible.ca/dailydeal",
            "timezone": "America/Toronto",
            "currency": "CAD",
            "currencySymbol": "$",
            "defaultCron": "15 1 * * *",
        },
        "au": {
            "label": "Audible AU",
            "dealUrl": "https://www.audible.com.au/dailydeal",
            "timezone": "Australia/Sydney",
            "currency": "AUD",
            "currencySymbol": "$",
            "defaultCron": "15 1 * * *",
        },
    }


SUPPORTED_MARKETPLACES = marketplace_specs()


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def workspace_root() -> Path:
    root = skill_root().resolve()
    for parent in [root, *root.parents]:
        if parent.name == "skills":
            return parent.parent
    return root


def default_storage_dir() -> Path:
    return workspace_root() / ".audible-goodreads-deal-scout"


def default_config_path() -> Path:
    return default_storage_dir() / "config.json"


def default_state_path() -> Path:
    return default_storage_dir() / "state.json"


def default_preferences_path() -> Path:
    return default_storage_dir() / "preferences.md"


def default_artifact_dir() -> Path:
    return default_storage_dir() / "artifacts" / "current"


def validate_marketplace(marketplace: str) -> dict[str, str]:
    key = normalize_space(marketplace).lower()
    if key not in SUPPORTED_MARKETPLACES:
        supported = ", ".join(sorted(SUPPORTED_MARKETPLACES))
        raise ValueError(f"Unsupported marketplace '{marketplace}'. Public v1 supports: {supported}.")
    return {"key": key, **SUPPORTED_MARKETPLACES[key]}


def validate_timezone(spec: dict[str, str]) -> str:
    timezone_name = spec["timezone"]
    try:
        ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise RuntimeError(
            f"Timezone data for {timezone_name} is unavailable on this host. Fix timezone data before enabling scheduling."
        ) from exc
    return timezone_name


def config_template(**overrides: Any) -> dict[str, Any]:
    payload = {
        "audibleMarketplace": "us",
        "threshold": DEFAULT_THRESHOLD,
        "goodreadsCsvPath": None,
        "preferencesPath": None,
        "privacyMode": "normal",
        "stateFile": None,
        "artifactDir": None,
        "freshnessDays": DEFAULT_FRESHNESS_DAYS,
        "csvColumns": {},
        "audibleDealUrl": None,
        "audibleFetchBackend": "auto",
        "audibleFetchRetries": 2,
        "audibleFetchBackoffSeconds": 1.0,
        "audibleAuthPath": None,
        "dailyCron": None,
        "deliveryChannel": None,
        "deliveryTarget": None,
        "deliveryPolicy": DEFAULT_DELIVERY_POLICY,
    }
    payload.update({key: value for key, value in overrides.items() if value is not None})
    return payload


def load_config(config_path: Path | None) -> tuple[Path, dict[str, Any]]:
    path = (config_path or default_config_path()).resolve()
    payload = read_json(path, config_template())
    if not isinstance(payload, dict):
        payload = config_template()
    return path, {**config_template(), **payload}


def resolve_notes_text(notes_file: str | None, inline_notes: str | None) -> str:
    if inline_notes:
        return str(inline_notes)
    normalized_path = normalize_space(str(notes_file or ""))
    if normalized_path:
        notes_path = Path(normalized_path).expanduser()
        if not notes_path.exists():
            raise FileNotFoundError(f"Preference notes file not found at {notes_path}.")
        return notes_path.read_text(encoding="utf-8")
    return ""


def parse_csv_column_overrides(items: list[str] | None) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in items or []:
        if "=" not in item:
            raise ValueError(f"Invalid --csv-column value '{item}'. Use role=Header.")
        role, header = item.split("=", 1)
        role = normalize_space(role).replace("-", "_").lower()
        header = header.strip()
        if not role or not header:
            raise ValueError(f"Invalid --csv-column value '{item}'. Use role=Header.")
        result[role] = header
    return result
