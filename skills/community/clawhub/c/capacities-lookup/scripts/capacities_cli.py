from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from capacities_cache import load_structures_cache
from capacities_lookup import lookup_with_metadata
from capacities_sync import sync_structures, verify_main_space


def _print_json(data: object) -> None:
    print(json.dumps(data, indent=2))


def _has_flag(argv: list[str], flag: str) -> bool:
    return flag in argv


def _lookup_search_term(argv: list[str]) -> str:
    terms = [arg for arg in argv[2:] if not arg.startswith("--")]
    return " ".join(terms).strip()


def _print_lookup_human(result: dict[str, object]) -> None:
    print(f"Search: {result.get('searchTerm')}")
    print(f"Space: {result.get('spaceId')}")
    print(f"Results: {result.get('resultCount')}")
    if result.get("requestedTypes"):
        print(f"Requested types: {', '.join(result.get('requestedTypes') or [])}")
        if result.get("requestedTypeFound") is False:
            print("Requested type matches: none")
    if result.get("expandRelated"):
        print(f"Query terms: {', '.join(result.get('queryTerms') or [])}")
    print()

    results = result.get("results", []) or []
    if not results:
        print("No matches found.")
        return

    for i, item in enumerate(results, start=1):
        if not isinstance(item, dict):
            continue
        matched_terms = item.get("allMatchedTerms") or [item.get("matchedOn")]
        matched_on_text = ", ".join([str(x) for x in matched_terms if x])
        print(f"{i}. {item.get('title')}")
        print(f"   Type: {item.get('structureLabel')}")
        print(f"   Match: {item.get('matchKind')} ({item.get('queryRole')})")
        if matched_on_text:
            print(f"   Matched on: {matched_on_text}")
        print(f"   Object ID: {item.get('id')}")
        print(f"   Link: {item.get('deepLink')}")
        print()

    fallback_results = result.get("fallbackResults") or []
    if result.get("requestedTypeFound") is False and fallback_results:
        print("Fallback suggestions:")
        for item in fallback_results:
            if not isinstance(item, dict):
                continue
            print(f"- {item.get('title')} [{item.get('structureLabel')}] -> {item.get('deepLink')}")


def cmd_sync_structures() -> int:
    result = sync_structures()
    _print_json(result)
    return 0


def cmd_verify_space() -> int:
    result = verify_main_space()
    _print_json(result)
    return 0


def cmd_list_structures() -> int:
    data = load_structures_cache()
    structures = data.get("structures", [])
    if not structures:
        print("No structures cache found. Run: sync-structures")
        return 1

    print(f"Space: {data.get('spaceId')}")
    print(f"Synced: {data.get('syncedAt')}")
    print()
    for item in structures:
        print(f"- {item.get('title')} ({item.get('id')})")
    return 0


def cmd_lookup(argv: list[str]) -> int:
    if len(argv) < 3:
        print('Usage: capacities_cli.py lookup "search phrase" [--json] [--include-structures] [--no-related]')
        return 1
    search_term = _lookup_search_term(argv)
    if not search_term:
        print('Usage: capacities_cli.py lookup "search phrase" [--json] [--include-structures] [--no-related]')
        return 1
    as_json = _has_flag(argv, "--json")
    include_structures = _has_flag(argv, "--include-structures")
    expand_related = not _has_flag(argv, "--no-related")
    result = lookup_with_metadata(search_term, include_structures=include_structures, expand_related=expand_related)
    if as_json:
        _print_json(result)
    else:
        _print_lookup_human(result)
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print("Usage: capacities_cli.py <sync-structures|list-structures|verify-space|lookup>")
        return 1

    command = argv[1]
    if command == "sync-structures":
        return cmd_sync_structures()
    if command == "list-structures":
        return cmd_list_structures()
    if command == "verify-space":
        return cmd_verify_space()
    if command == "lookup":
        return cmd_lookup(argv)

    print(f"Unknown command: {command}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
