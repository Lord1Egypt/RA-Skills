#!/usr/bin/env python3
"""Validate the public, sanitized reusable Lib module catalog."""

from __future__ import annotations

import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "library" / "modules" / "catalog.json"
BLOCKS = Path(__file__).resolve().parents[4] / "internal" / "blocks" / "data"
ID_RE = re.compile(r"^lib\.[a-z0-9_]+$")
BLOCK_RE = re.compile(r"^block\.[a-z0-9_]+$")
MATURITY = {"draft", "topology_ready", "compose_ready", "verified"}
CATEGORIES = {
    "audio", "button", "comms", "display", "indicator", "mechanical", "mcu",
    "mcu-support", "power", "protection", "rf", "sensing", "storage", "usb", "usb-serial",
}
FORBIDDEN_KEYS = {
    "board", "boardName", "exam", "examName", "question", "questionName", "score",
    "sourcePath", "sourceFile", "bom", "coordinates", "projectName",
}


def fail(errors: list[str], where: str, message: str) -> None:
    errors.append(f"{where}: {message}")


def main() -> int:
    errors: list[str] = []
    try:
        data = json.loads(CATALOG.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"module catalog unreadable: {exc}", file=sys.stderr)
        return 1
    if data.get("schemaVersion") != 1:
        fail(errors, "catalog", "schemaVersion must be 1")
    corpus = data.get("sourceCorpus")
    if not isinstance(corpus, dict) or corpus.get("containsOriginalContent") is not False or corpus.get("containsBoardMapping") is not False:
        fail(errors, "catalog.sourceCorpus", "must explicitly deny original content and board mapping")
    modules = data.get("modules")
    if not isinstance(modules, list) or not modules:
        fail(errors, "catalog.modules", "must be a non-empty array")
        modules = []
    known_blocks = {
        f"block.{path.stem}" for path in BLOCKS.glob("*.json") if not path.name.startswith("_")
    } if BLOCKS.is_dir() else set()
    seen: set[str] = set()
    topology_cache: dict[str, set[str]] = {}
    for index, item in enumerate(modules):
        where = f"modules[{index}]"
        if not isinstance(item, dict):
            fail(errors, where, "must be an object")
            continue
        leaked = FORBIDDEN_KEYS.intersection(item)
        if leaked:
            fail(errors, where, f"forbidden identifying keys: {sorted(leaked)}")
        module_id = item.get("id")
        if not isinstance(module_id, str) or not ID_RE.fullmatch(module_id):
            fail(errors, where, "invalid id")
        elif module_id in seen:
            fail(errors, where, f"duplicate id {module_id}")
        else:
            seen.add(module_id)
        if not isinstance(item.get("title"), str) or not item["title"].strip():
            fail(errors, where, "title is required")
        if item.get("category") not in CATEGORIES:
            fail(errors, where, "invalid category")
        maturity = item.get("maturity")
        if maturity not in MATURITY:
            fail(errors, where, "invalid maturity")
        if not isinstance(item.get("evidenceCount"), int) or item["evidenceCount"] < 1:
            fail(errors, where, "evidenceCount must be a positive aggregate")
        constraints = item.get("constraints")
        if not isinstance(constraints, list) or not constraints or not all(isinstance(v, str) and v.strip() for v in constraints):
            fail(errors, where, "constraints must contain non-empty strings")
        block = item.get("blockTemplate")
        if block is not None:
            if not isinstance(block, str) or not BLOCK_RE.fullmatch(block):
                fail(errors, where, "invalid blockTemplate")
            elif known_blocks and block not in known_blocks:
                fail(errors, where, f"unknown blockTemplate {block}")
        asset_key = "composeAsset" if item.get("composeAsset") else "layoutInput" if item.get("layoutInput") else None
        if maturity in {"compose_ready", "verified"} and asset_key is None:
            fail(errors, where, f"{maturity} requires composeAsset or layoutInput")
        if asset_key:
            asset = item[asset_key]
            if not isinstance(asset, str) or Path(asset).name != asset or not asset.endswith(".json"):
                fail(errors, where, f"invalid {asset_key}")
            elif not (CATALOG.parent / asset).is_file():
                fail(errors, where, f"missing {asset_key} {asset}")
        topology_asset = item.get("topologyAsset")
        if topology_asset is not None:
            if not isinstance(topology_asset, str) or Path(topology_asset).name != topology_asset or not topology_asset.endswith(".json"):
                fail(errors, where, "invalid topologyAsset")
            else:
                path = CATALOG.parent / topology_asset
                if not path.is_file():
                    fail(errors, where, f"missing topologyAsset {topology_asset}")
                elif topology_asset not in topology_cache:
                    try:
                        topology = json.loads(path.read_text(encoding="utf-8"))
                        records = topology.get("modules")
                        if records is None and isinstance(topology.get("module"), dict):
                            records = [topology["module"]]
                        if not isinstance(records, list) or not records:
                            raise ValueError("topology asset needs module or non-empty modules")
                        topology_cache[topology_asset] = {record.get("id") for record in records if isinstance(record, dict)}
                        for record_index, record in enumerate(records):
                            record_where = f"{topology_asset}.modules[{record_index}]"
                            if record.get("maturity") != "topology_ready":
                                fail(errors, record_where, "extracted topology must be topology_ready")
                            pin_nets: dict[str, str] = {}
                            roles: set[str] = set()
                            for part in record.get("parts", []):
                                role = part.get("role")
                                if not isinstance(role, str) or not role or role in roles:
                                    fail(errors, record_where, "part roles must be non-empty and unique")
                                roles.add(role)
                                device = part.get("device", {})
                                if not re.fullmatch(r"[0-9a-f]{32}", str(device.get("deviceUuid", ""))):
                                    fail(errors, record_where, "part lacks 32-character deviceUuid")
                                pins = part.get("pins")
                                if not isinstance(pins, list) or not pins:
                                    fail(errors, record_where, "part lacks complete pins")
                                for pin in pins or []:
                                    states = int("net" in pin) + int(pin.get("connectionState") == "unconnected")
                                    if states != 1:
                                        fail(errors, record_where, "each pin needs exactly one net or unconnected state")
                                    endpoint = f"{role}.{pin.get('number')}"
                                    if endpoint in pin_nets:
                                        fail(errors, record_where, f"duplicate physical pin {endpoint}")
                                    if "net" in pin:
                                        pin_nets[endpoint] = pin["net"]
                            declared: dict[str, str] = {}
                            net_ids: set[str] = set()
                            for net in record.get("nets", []):
                                net_id = net.get("id")
                                if not isinstance(net_id, str) or not net_id or net_id in net_ids:
                                    fail(errors, record_where, "net ids must be non-empty and unique")
                                net_ids.add(net_id)
                                members = net.get("members")
                                if not isinstance(members, list) or not members:
                                    fail(errors, record_where, f"net {net_id} has no members")
                                for endpoint in members or []:
                                    if endpoint in declared:
                                        fail(errors, record_where, f"pin {endpoint} appears in multiple nets")
                                    declared[endpoint] = net_id
                                    if pin_nets.get(endpoint) != net_id:
                                        fail(errors, record_where, f"net member {endpoint} disagrees with its pin")
                            if pin_nets != declared:
                                fail(errors, record_where, "connected pin set does not exactly match declared nets")
                    except (OSError, ValueError, json.JSONDecodeError) as exc:
                        fail(errors, where, f"invalid topologyAsset: {exc}")
                        topology_cache[topology_asset] = set()
                if module_id not in topology_cache.get(topology_asset, set()):
                    fail(errors, where, f"topologyAsset does not contain {module_id}")
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    by_maturity = {name: sum(m.get("maturity") == name for m in modules) for name in sorted(MATURITY)}
    print(f"module catalog OK: {len(modules)} records; " + ", ".join(f"{k}={v}" for k, v in by_maturity.items()))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
