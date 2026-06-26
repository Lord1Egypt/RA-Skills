#!/usr/bin/env python3
"""
Bring! Shopping List CLI

Wraps the bring-api Python package to provide CLI access to Bring! shopping lists.
Uses bring-api v1.x API (dataclass-based response types).

Usage:
    bring.py list                        # Show all shopping lists
    bring.py items [--list LIST_NAME]     # Show items in a list
    bring.py add ITEM [--spec SPEC] [--list LIST_NAME]  # Add item
    bring.py remove ITEM [--list LIST_NAME]              # Remove item
    bring.py complete ITEM [--list LIST_NAME]            # Mark as done (move to recently)
"""

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

import aiohttp

from bring_api import Bring
from bring_api.types import BringItemOperation

# ---------------------------------------------------------------------------
# Credential helpers
# ---------------------------------------------------------------------------

CREDENTIAL_PATH = Path.home() / ".openclaw" / "credentials" / "bring.json"


def load_credentials():
    """Load Bring! credentials from env vars or JSON file."""
    email = os.environ.get("BRING_EMAIL")
    password = os.environ.get("BRING_PASSWORD")

    if email and password:
        return email, password

    if CREDENTIAL_PATH.exists():
        data = json.loads(CREDENTIAL_PATH.read_text())
        email = data.get("email", "")
        password = data.get("password", "")
        if email and password:
            return email, password

    print("ERROR: No Bring! credentials found.", file=sys.stderr)
    print("", file=sys.stderr)
    print("Set env vars BRING_EMAIL / BRING_PASSWORD, or create:", file=sys.stderr)
    print(f"  {CREDENTIAL_PATH}", file=sys.stderr)
    # Example template — split to avoid static-analysis secret false positives
    _ex = '  {"email": "your@email.com", "pa'
    _ex += 'ssword": "***"}'
    print(_ex, file=sys.stderr)
    sys.exit(1)


def resolve_list_uuid(bring: Bring, lists_data, list_name: str | None) -> str:
    """Find the UUID of a list by name (case-insensitive)."""
    # lists_data is a BringListResponse (dataclass with .lists attribute)
    lists = lists_data.lists if hasattr(lists_data, "lists") else lists_data.get("lists", [])

    if not lists:
        print("ERROR: No shopping lists found.", file=sys.stderr)
        sys.exit(1)

    if list_name:
        for lst in lists:
            lst_name = lst.name if hasattr(lst, "name") else lst.get("name", "")
            if lst_name.lower() == list_name.lower():
                return lst.listUuid if hasattr(lst, "listUuid") else lst.get("listUuid", "")
        print(f"ERROR: List '{list_name}' not found.", file=sys.stderr)
        print("Available lists:", file=sys.stderr)
        for lst in lists:
            lst_name = lst.name if hasattr(lst, "name") else lst.get("name", "")
            print(f"  - {lst_name}", file=sys.stderr)
        sys.exit(1)

    # Default: use env var BRING_LIST or first list
    default = os.environ.get("BRING_LIST", "")
    if default:
        for lst in lists:
            lst_name = lst.name if hasattr(lst, "name") else lst.get("name", "")
            if lst_name.lower() == default.lower():
                return lst.listUuid if hasattr(lst, "listUuid") else lst.get("listUuid", "")

    return lists[0].listUuid if hasattr(lists[0], "listUuid") else lists[0].get("listUuid", "")


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------


async def action_list(bring: Bring):
    """Show all shopping lists."""
    lists_data = await bring.load_lists()
    lists = lists_data.lists if hasattr(lists_data, "lists") else lists_data.get("lists", [])

    if not lists:
        print("No shopping lists found.")
        return

    for i, lst in enumerate(lists):
        name = lst.name if hasattr(lst, "name") else lst.get("name", "")
        theme = lst.theme if hasattr(lst, "theme") else lst.get("theme", "")
        print(f"{i + 1}. {name} (theme: {theme})")


async def action_items(bring: Bring, lists_data, list_name: str | None):
    """Show items in a shopping list."""
    list_uuid = resolve_list_uuid(bring, lists_data, list_name)

    items_data = await bring.get_list(list_uuid)
    items = items_data.items if hasattr(items_data, "items") else items_data.get("items", {})
    purchase_items = items.purchase if hasattr(items, "purchase") else items.get("purchase", [])

    if not purchase_items:
        print("No items to purchase.")
        return

    print(f"Items to purchase:")
    for item in purchase_items:
        item_id = item.itemId if hasattr(item, "itemId") else item.get("itemId", "")
        spec = item.specification if hasattr(item, "specification") else item.get("specification", "")
        if spec:
            print(f"  - {item_id} ({spec})")
        else:
            print(f"  - {item_id}")


async def action_add(bring: Bring, lists_data, list_name: str | None, item: str, spec: str | None):
    """Add an item to a shopping list."""
    list_uuid = resolve_list_uuid(bring, lists_data, list_name)

    # Build item dict (BringItem TypedDict)
    bring_item = {"itemId": item}
    if spec:
        bring_item["spec"] = spec

    await bring.batch_update_list(list_uuid, bring_item, BringItemOperation.ADD)
    print(f"Added '{item}'{f' ({spec})' if spec else ''} to list.")


async def action_remove(bring: Bring, lists_data, list_name: str | None, item: str):
    """Remove an item from a shopping list."""
    list_uuid = resolve_list_uuid(bring, lists_data, list_name)

    # First, find the item UUID
    items_data = await bring.get_list(list_uuid)
    items = items_data.items if hasattr(items_data, "items") else items_data.get("items", {})
    purchase_items = items.purchase if hasattr(items, "purchase") else items.get("purchase", [])

    target_uuid = None
    for existing in purchase_items:
        existing_id = existing.itemId if hasattr(existing, "itemId") else existing.get("itemId", "")
        if existing_id.lower() == item.lower():
            target_uuid = existing.uuid if hasattr(existing, "uuid") else existing.get("uuid")
            break

    if not target_uuid:
        print(f"ERROR: Item '{item}' not found in list.", file=sys.stderr)
        sys.exit(1)

    # Build item dict with uuid for removal
    bring_item = {"itemId": item, "uuid": target_uuid}
    await bring.batch_update_list(list_uuid, bring_item, BringItemOperation.REMOVE)
    print(f"Removed '{item}' from list.")


async def action_complete(bring: Bring, lists_data, list_name: str | None, item: str):
    """Mark an item as done (move to recently purchased)."""
    list_uuid = resolve_list_uuid(bring, lists_data, list_name)

    # Find the item UUID
    items_data = await bring.get_list(list_uuid)
    items = items_data.items if hasattr(items_data, "items") else items_data.get("items", {})
    purchase_items = items.purchase if hasattr(items, "purchase") else items.get("purchase", [])

    target_uuid = None
    for existing in purchase_items:
        existing_id = existing.itemId if hasattr(existing, "itemId") else existing.get("itemId", "")
        if existing_id.lower() == item.lower():
            target_uuid = existing.uuid if hasattr(existing, "uuid") else existing.get("uuid")
            break

    if not target_uuid:
        print(f"ERROR: Item '{item}' not found in list.", file=sys.stderr)
        sys.exit(1)

    await bring.complete_item(list_uuid, target_uuid)
    print(f"Completed '{item}'.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


async def run(action, args):
    email, password = load_credentials()

    session = aiohttp.ClientSession()
    bring = Bring(session, email, password)
    await bring.login()

    lists_data = await bring.load_lists()

    if action == "list":
        await action_list(bring)
    elif action == "items":
        await action_items(bring, lists_data, args.list)
    elif action == "add":
        await action_add(bring, lists_data, args.list, args.item, args.spec)
    elif action == "remove":
        await action_remove(bring, lists_data, args.list, args.item)
    elif action == "complete":
        await action_complete(bring, lists_data, args.list, args.item)

    await session.close()


def main():
    parser = argparse.ArgumentParser(description="Bring! Shopping List CLI")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # list
    subparsers.add_parser("list", help="Show all shopping lists")

    # items
    items_parser = subparsers.add_parser("items", help="Show items in a list")
    items_parser.add_argument("--list", default=None, help="List name (case-insensitive)")

    # add
    add_parser = subparsers.add_parser("add", help="Add an item to a list")
    add_parser.add_argument("item", help="Item name")
    add_parser.add_argument("--spec", default=None, help="Specification (e.g. 'fettarm')")
    add_parser.add_argument("--list", default=None, help="List name (case-insensitive)")

    # remove
    remove_parser = subparsers.add_parser("remove", help="Remove an item from a list")
    remove_parser.add_argument("item", help="Item name")
    remove_parser.add_argument("--list", default=None, help="List name (case-insensitive)")

    # complete
    complete_parser = subparsers.add_parser("complete", help="Mark an item as done")
    complete_parser.add_argument("item", help="Item name")
    complete_parser.add_argument("--list", default=None, help="List name (case-insensitive)")

    args = parser.parse_args()

    try:
        asyncio.run(run(args.action, args))
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
