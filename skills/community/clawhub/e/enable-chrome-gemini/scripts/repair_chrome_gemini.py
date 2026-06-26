#!/usr/bin/env python3
"""Enable or repair Chrome Gemini (Glic) eligibility state in Chrome's Local State."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


def default_user_data_dir() -> Path:
    system = platform.system().lower()
    home = Path.home()

    if system == "windows":
        local_appdata = os.environ.get("LOCALAPPDATA")
        if not local_appdata:
            raise SystemExit("LOCALAPPDATA is not set.")
        return Path(local_appdata) / "Google" / "Chrome" / "User Data"

    if system == "darwin":
        return home / "Library" / "Application Support" / "Google" / "Chrome"

    if system == "linux":
        return home / ".config" / "google-chrome"

    raise SystemExit(f"Unsupported platform: {platform.system()}")


def chrome_is_running() -> bool:
    system = platform.system().lower()

    if system == "windows":
        try:
            result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq chrome.exe", "/NH"],
                capture_output=True,
                text=True,
                check=False,
            )
        except OSError:
            return False
        output = (result.stdout or "").lower()
        return "chrome.exe" in output and "no tasks are running" not in output

    if system == "darwin":
        for pattern in ("Google Chrome", "chrome", "Chromium"):
            try:
                result = subprocess.run(
                    ["pgrep", "-f", pattern],
                    capture_output=True,
                    text=True,
                    check=False,
                )
            except OSError:
                continue
            if result.returncode == 0 and (result.stdout or "").strip():
                return True
        return False

    if system == "linux":
        for pattern in ("google-chrome", "chrome", "chromium"):
            try:
                result = subprocess.run(
                    ["pgrep", "-f", pattern],
                    capture_output=True,
                    text=True,
                    check=False,
                )
            except OSError:
                continue
            if result.returncode == 0 and (result.stdout or "").strip():
                return True
        return False

    return False


def ensure_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def normalize_country_list(value: Any, country: str) -> Any:
    if isinstance(value, list):
        updated = list(value)
        if not updated:
            return [country]
        updated[-1] = country
        return updated
    if value is None:
        return [country]
    if isinstance(value, str):
        if value == country:
            return value
        return [value, country]
    return [country]


def update_language_settings(data: dict[str, Any], language: str | None) -> list[str]:
    changes: list[str] = []
    if not language:
        return changes

    intl = data.get("intl")
    if not isinstance(intl, dict):
        changes.append("intl: created missing object")
        intl = {}
        data["intl"] = intl

    if intl.get("app_locale") != language:
        changes.append(f"intl.app_locale: {intl.get('app_locale')!r} -> {language!r}")
        intl["app_locale"] = language

    if intl.get("selected_languages") != language:
        changes.append(
            f"intl.selected_languages: {intl.get('selected_languages')!r} -> {language!r}"
        )
        intl["selected_languages"] = language

    accept_languages = f"{language},en"
    if intl.get("accept_languages") != accept_languages:
        changes.append(
            f"intl.accept_languages: {intl.get('accept_languages')!r} -> {accept_languages!r}"
        )
        intl["accept_languages"] = accept_languages

    return changes


def update_local_state(data: dict[str, Any], language: str | None) -> list[str]:
    changes: list[str] = []

    if data.get("variations_country") != "us":
        changes.append(f"variations_country: {data.get('variations_country')!r} -> 'us'")
        data["variations_country"] = "us"

    current_perm = data.get("variations_permanent_consistency_country")
    updated_perm = normalize_country_list(current_perm, "us")
    if updated_perm != current_perm:
        changes.append(
            "variations_permanent_consistency_country: "
            f"{current_perm!r} -> {updated_perm!r}"
        )
        data["variations_permanent_consistency_country"] = updated_perm

    for key in (
        "variations_safe_seed_permanent_consistency_country",
        "variations_safe_seed_session_consistency_country",
    ):
        if data.get(key) != "us":
            changes.append(f"{key}: {data.get(key)!r} -> 'us'")
            data[key] = "us"

    glic = data.get("glic")
    if not isinstance(glic, dict):
        changes.append("glic: created missing object")
        glic = {}
        data["glic"] = glic
    if glic.get("is_glic_eligible") is not True:
        changes.append(f"glic.is_glic_eligible: {glic.get('is_glic_eligible')!r} -> True")
        glic["is_glic_eligible"] = True

    browser = data.get("browser")
    if not isinstance(browser, dict):
        changes.append("browser.enabled_labs_experiments: created missing object")
        browser = {}
        data["browser"] = browser

    experiments = ensure_list(browser.get("enabled_labs_experiments"))
    added = []
    for entry in ("glic@1", "glic-side-panel@1"):
        if entry not in experiments:
            experiments.append(entry)
            added.append(entry)
    if added or browser.get("enabled_labs_experiments") != experiments:
        if added:
            changes.append(
                "browser.enabled_labs_experiments: added " + ", ".join(added)
            )
        browser["enabled_labs_experiments"] = experiments

    changes.extend(update_language_settings(data, language))

    return changes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Back up and repair Chrome Gemini eligibility in Local State for first-time setup or recovery on Windows, macOS, or Linux.",
    )
    parser.add_argument(
        "--user-data-dir",
        default=str(default_user_data_dir()),
        help="Chrome user data directory that contains Local State. Defaults to the current platform's Chrome profile location.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the planned changes without writing files.",
    )
    parser.add_argument(
        "--language",
        default="en-US",
        help="Chrome UI language to normalize in Local State. Use an empty string to skip.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow running even if chrome.exe is still open.",
    )
    args = parser.parse_args()

    if chrome_is_running() and not args.force:
        print("Chrome appears to be running.")
        print("Close all Chrome windows and rerun, or pass --force if you know the risk.")
        return 2

    user_data_dir = Path(args.user_data_dir).expanduser().resolve()
    local_state = user_data_dir / "Local State"
    if not local_state.exists():
        print(f"Local State not found: {local_state}")
        return 1

    try:
        data = json.loads(local_state.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        print(f"Could not parse Local State: {exc}")
        return 1

    if not isinstance(data, dict):
        print("Local State root is not a JSON object.")
        return 1

    language = args.language if args.language else None
    changes = update_local_state(data, language)
    if not changes:
        print("No Gemini repair changes were needed.")
        return 0

    print("Planned changes:")
    for change in changes:
        print(f"- {change}")

    if args.dry_run:
        print("Dry run only; no files written.")
        return 0

    timestamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = local_state.with_name(f"Local State.bak.{timestamp}")
    shutil.copy2(local_state, backup)

    temp_path = local_state.with_name(f"Local State.tmp.{timestamp}")
    temp_path.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    temp_path.replace(local_state)

    print(f"Backup written to: {backup}")
    print(f"Updated: {local_state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
