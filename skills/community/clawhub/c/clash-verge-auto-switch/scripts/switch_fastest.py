#!/usr/bin/env python3
"""Speed test Clash Verge/Mihomo selector groups and switch to the fastest node."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Optional

DEFAULT_DELAY_URL = "http://1.1.1.1"
DEFAULT_TIMEOUT_MS = 5000
IGNORE_NAMES = {"DIRECT", "REJECT", "PASS", "COMPATIBLE"}
EXPANDABLE_TYPES = {"urltest", "fallback", "loadbalance"}
SELECTOR_TYPES = {"selector"}
GROUP_SCOPE_CHOICES = ("current", "top-level", "all")


def timestamp() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")


def log(message: str) -> None:
    print(f"[{timestamp()}] {message}")


def read_simple_yaml_value(paths: list[Path], key: str) -> Optional[str]:
    pattern = re.compile(rf"^{re.escape(key)}:\s*(.*?)\s*$")
    for path in paths:
        if not path.exists():
            continue
        for raw_line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            match = pattern.match(line)
            if not match:
                continue
            value = match.group(1).split(" #", 1)[0].strip().strip("'").strip('"')
            return value or None
    return None


def maybe_launch_clash_verge(wait_seconds: int) -> None:
    commands = [
        ["open", "-g", "-b", "io.github.clash-verge-rev.clash-verge-rev"],
        ["open", "-g", "-a", "Clash Verge"],
        ["open", "-g", "-a", "Clash Verge Rev"],
    ]
    for command in commands:
        subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    if wait_seconds > 0:
        time.sleep(wait_seconds)


def build_candidates(args: argparse.Namespace) -> list[dict[str, str]]:
    config_paths = [
        Path.home() / "Library/Application Support/io.github.clash-verge-rev.clash-verge-rev/config.yaml",
        Path.home() / ".config/clash/config.yaml",
    ]
    candidates: list[dict[str, str]] = []

    if args.unix_socket:
        candidates.append({"kind": "unix", "address": args.unix_socket, "secret": args.secret or ""})
    if args.controller_url:
        candidates.append({"kind": "http", "address": args.controller_url, "secret": args.secret or ""})

    env_socket = os.environ.get("CLASH_API_UNIX_SOCKET")
    env_url = os.environ.get("CLASH_API_URL")
    env_secret = os.environ.get("CLASH_API_SECRET", "")
    if env_socket:
        candidates.append({"kind": "unix", "address": env_socket, "secret": env_secret})
    if env_url:
        candidates.append({"kind": "http", "address": env_url, "secret": env_secret})

    config_socket = read_simple_yaml_value(config_paths, "external-controller-unix")
    config_url = read_simple_yaml_value(config_paths, "external-controller")
    config_secret = read_simple_yaml_value(config_paths, "secret") or ""
    if config_socket:
        candidates.append({"kind": "unix", "address": config_socket, "secret": config_secret})
    if config_url:
        if not config_url.startswith("http://") and not config_url.startswith("https://"):
            config_url = f"http://{config_url}"
        candidates.append({"kind": "http", "address": config_url, "secret": config_secret})

    # Preserve order while deduplicating.
    deduped: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for candidate in candidates:
        secret = candidate.get("secret", "")
        if secret == "set-your-secret":
            secret = ""
        key = (candidate["kind"], candidate["address"], secret)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(
            {"kind": candidate["kind"], "address": candidate["address"], "secret": secret}
        )
    return deduped


def run_curl(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, capture_output=True, text=True, check=False)


def api_request(
    controller: dict[str, str],
    method: str,
    path: str,
    query: Optional[dict[str, str]] = None,
    body: Optional[dict[str, object]] = None,
) -> object:
    command = ["curl", "--silent", "--show-error", "--fail-with-body"]

    if controller["kind"] == "unix":
        command.extend(["--unix-socket", controller["address"]])
        url = f"http://localhost{path}"
    else:
        base = controller["address"].rstrip("/")
        url = f"{base}{path}"

    if controller.get("secret"):
        command.extend(["-H", f"Authorization: Bearer {controller['secret']}"])
    if body is not None:
        command.extend(["-H", "Content-Type: application/json", "--data", json.dumps(body)])
    if query:
        command.append("--get")
        for key, value in query.items():
            command.extend(["--data-urlencode", f"{key}={value}"])
    command.extend(["-X", method.upper(), url])

    result = run_curl(command)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        raise RuntimeError(detail or f"curl failed with exit code {result.returncode}")

    payload = result.stdout.strip()
    if not payload:
        return None
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        return payload


def discover_controller(args: argparse.Namespace) -> dict[str, str]:
    candidates = build_candidates(args)

    if args.launch_if_needed:
        for candidate in candidates:
            if controller_reachable(candidate):
                return candidate
        maybe_launch_clash_verge(args.launch_wait)

    for candidate in candidates:
        if controller_reachable(candidate):
            return candidate

    raise RuntimeError(
        "Could not reach the Mihomo controller. Open Clash Verge first, "
        "or pass --controller-url / --unix-socket explicitly."
    )


def controller_reachable(controller: dict[str, str]) -> bool:
    try:
        api_request(controller, "GET", "/version")
        return True
    except RuntimeError:
        return False


def normalize_type(entry: Optional[dict[str, object]]) -> str:
    if not entry:
        return ""
    value = entry.get("type")
    return str(value or "").strip().lower()


def group_options(entry: Optional[dict[str, object]]) -> list[str]:
    if not entry:
        return []
    options = entry.get("all")
    if not isinstance(options, list):
        options = entry.get("proxies")
    if not isinstance(options, list):
        return []
    return [str(option) for option in options]


def is_selector_group(name: str, entry: Optional[dict[str, object]]) -> bool:
    if name.upper() == "GLOBAL":
        return False
    if normalize_type(entry) not in SELECTOR_TYPES:
        return False
    return len(group_options(entry)) >= 2


def build_reverse_references(
    proxies: dict[str, dict[str, object]]
) -> dict[str, set[str]]:
    reverse_refs: dict[str, set[str]] = {}
    for parent_name, entry in proxies.items():
        for option in group_options(entry):
            reverse_refs.setdefault(option, set()).add(parent_name)
    return reverse_refs


def list_all_selector_groups(proxies: dict[str, dict[str, object]]) -> list[str]:
    groups: list[str] = []
    for name, entry in proxies.items():
        if is_selector_group(name, entry):
            groups.append(name)
    return groups


def list_top_level_selector_groups(
    proxies: dict[str, dict[str, object]]
) -> list[str]:
    reverse_refs = build_reverse_references(proxies)
    groups: list[str] = []

    for name in list_all_selector_groups(proxies):
        parents = reverse_refs.get(name, set())
        nested_parents = {
            parent
            for parent in parents
            if parent != "GLOBAL"
            and normalize_type(proxies.get(parent)) in SELECTOR_TYPES.union(EXPANDABLE_TYPES)
        }
        if not nested_parents:
            groups.append(name)

    return groups or list_all_selector_groups(proxies)


def follow_selected_chain(
    start_name: str, proxies: dict[str, dict[str, object]]
) -> list[str]:
    chain: list[str] = []
    visited: set[str] = set()
    current_name = start_name

    while current_name and current_name not in visited:
        visited.add(current_name)
        entry = proxies.get(current_name)
        if not isinstance(entry, dict):
            break

        if is_selector_group(current_name, entry):
            chain.append(current_name)

        next_name = str(entry.get("now") or "").strip()
        if not next_name or next_name == current_name or next_name not in proxies:
            break
        current_name = next_name

    return chain


def list_current_selector_groups(
    proxies: dict[str, dict[str, object]]
) -> list[str]:
    roots: list[str] = []

    if "GLOBAL" in proxies:
        roots.append("GLOBAL")

    for parent_name, entry in proxies.items():
        parent_type = normalize_type(entry)
        if parent_name != "GLOBAL" and parent_type not in SELECTOR_TYPES.union(EXPANDABLE_TYPES):
            continue
        selected_name = str((entry or {}).get("now") or "").strip()
        if not selected_name or selected_name not in proxies:
            continue
        if normalize_type(proxies.get(selected_name)) in SELECTOR_TYPES:
            roots.append(selected_name)

    groups: list[str] = []
    for root in unique_preserving_order(roots):
        groups.extend(follow_selected_chain(root, proxies))

    groups = unique_preserving_order(groups)
    return groups or list_top_level_selector_groups(proxies)


def list_target_groups(
    args: argparse.Namespace, proxies: dict[str, dict[str, object]]
) -> list[str]:
    if args.group:
        return args.group

    if args.group_scope == "current":
        return list_current_selector_groups(proxies)
    if args.group_scope == "top-level":
        return list_top_level_selector_groups(proxies)
    return list_all_selector_groups(proxies)


def unique_preserving_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def expand_candidates(
    group_name: str,
    proxies: dict[str, dict[str, object]],
    expand_select_groups: bool,
    seen: Optional[set[str]] = None,
) -> list[str]:
    seen = seen or set()
    if group_name in seen:
        return []
    seen.add(group_name)

    entry = proxies.get(group_name) or {}
    options = group_options(entry)
    if not options:
        return []

    resolved: list[str] = []
    for option in options:
        option_name = str(option)
        if option_name in IGNORE_NAMES:
            continue
        option_entry = proxies.get(option_name)
        option_type = normalize_type(option_entry)
        if option_type in EXPANDABLE_TYPES:
            resolved.extend(expand_candidates(option_name, proxies, expand_select_groups, seen))
            continue
        if option_type in SELECTOR_TYPES and expand_select_groups:
            resolved.extend(expand_candidates(option_name, proxies, expand_select_groups, seen))
            continue
        if option_type in SELECTOR_TYPES:
            continue
        resolved.append(option_name)

    return unique_preserving_order(resolved)


def measure_delay(
    controller: dict[str, str], proxy_name: str, url: str, timeout_ms: int
) -> Optional[int]:
    response = api_request(
        controller,
        "GET",
        f"/proxies/{urllib.parse.quote(proxy_name, safe='')}/delay",
        query={"url": url, "timeout": str(timeout_ms)},
    )
    if not isinstance(response, dict):
        return None
    delay = response.get("delay")
    if isinstance(delay, int):
        return delay
    return None


def select_proxy(
    controller: dict[str, str], group_name: str, proxy_name: str
) -> None:
    api_request(
        controller,
        "PUT",
        f"/proxies/{urllib.parse.quote(group_name, safe='')}",
        body={"name": proxy_name},
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Speed test Clash Verge selector groups and switch to the fastest proxy."
    )
    parser.add_argument("--group", action="append", help="Selector group to optimize. Repeatable.")
    parser.add_argument("--controller-url", help="HTTP controller base URL, e.g. http://127.0.0.1:9097")
    parser.add_argument("--unix-socket", help="Unix socket path for the controller")
    parser.add_argument("--secret", help="Controller secret token")
    parser.add_argument(
        "--group-scope",
        choices=GROUP_SCOPE_CHOICES,
        default="current",
        help="How to auto-discover target groups when --group is not provided",
    )
    parser.add_argument("--delay-url", default=DEFAULT_DELAY_URL, help="URL used for delay testing")
    parser.add_argument("--timeout-ms", type=int, default=DEFAULT_TIMEOUT_MS, help="Delay test timeout in milliseconds")
    parser.add_argument("--dry-run", action="store_true", help="Measure and report only; do not switch groups")
    parser.add_argument("--list-groups", action="store_true", help="Print discovered target groups and exit")
    parser.add_argument(
        "--expand-select-groups",
        action="store_true",
        help="Recursively expand nested selector groups into leaf proxies",
    )
    parser.add_argument(
        "--launch-if-needed",
        action="store_true",
        help="Try to open Clash Verge before giving up on controller discovery",
    )
    parser.add_argument(
        "--launch-wait",
        type=int,
        default=8,
        help="Seconds to wait after attempting to launch Clash Verge",
    )
    args = parser.parse_args()

    try:
        controller = discover_controller(args)
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2

    version = api_request(controller, "GET", "/version")
    if isinstance(version, dict):
        log(
            "Connected to controller via "
            f"{controller['kind']} ({version.get('mihomo') or version.get('version') or 'unknown version'})"
        )
    else:
        log(f"Connected to controller via {controller['kind']}")

    payload = api_request(controller, "GET", "/proxies")
    if not isinstance(payload, dict) or not isinstance(payload.get("proxies"), dict):
        print("Unexpected /proxies response from controller.", file=sys.stderr)
        return 3
    proxies = payload["proxies"]

    groups = list_target_groups(args, proxies)
    if not groups:
        print("No selector groups found to optimize.", file=sys.stderr)
        return 4

    group_source = "explicit" if args.group else args.group_scope
    log(f"Discovered target groups ({group_source}): {', '.join(groups)}")

    if args.list_groups:
        for group_name in groups:
            print(group_name)
        return 0

    overall_success = False

    for group_name in groups:
        group_entry = proxies.get(group_name)
        if normalize_type(group_entry) not in SELECTOR_TYPES:
            log(f"Skipping {group_name}: not a selector group.")
            continue

        candidates = expand_candidates(group_name, proxies, args.expand_select_groups)
        if not candidates:
            log(f"Skipping {group_name}: no leaf proxies found.")
            continue

        results: list[tuple[int, str]] = []
        for candidate in candidates:
            try:
                delay = measure_delay(controller, candidate, args.delay_url, args.timeout_ms)
            except RuntimeError:
                delay = None
            if delay is not None:
                results.append((delay, candidate))

        if not results:
            log(f"{group_name}: no healthy proxies responded within {args.timeout_ms} ms.")
            continue

        results.sort(key=lambda item: item[0])
        winner_delay, winner_name = results[0]
        current_name = str((group_entry or {}).get("now") or "")

        if args.dry_run:
            log(
                f"{group_name}: best candidate is {winner_name} ({winner_delay} ms); "
                f"current selection is {current_name or 'unknown'}."
            )
            overall_success = True
            continue

        if current_name == winner_name:
            log(f"{group_name}: already on fastest node {winner_name} ({winner_delay} ms).")
            overall_success = True
            continue

        try:
            select_proxy(controller, group_name, winner_name)
        except RuntimeError as exc:
            log(f"{group_name}: failed to switch to {winner_name}: {exc}")
            continue

        log(
            f"{group_name}: switched from {current_name or 'unknown'} "
            f"to {winner_name} ({winner_delay} ms)."
        )
        overall_success = True

    return 0 if overall_success else 5


if __name__ == "__main__":
    sys.exit(main())
