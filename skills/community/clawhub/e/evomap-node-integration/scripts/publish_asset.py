#!/usr/bin/env python3
"""
Publish Gene + Capsule + Event to EvoMap Hub.
Usage: python3 publish_asset.py <gene.json> <capsule.json> <event.json>
"""
import sys
import json
import hashlib
import time
import os

HUB_URL = "https://evomap.ai"
PUBLISH_ENDPOINT = f"{HUB_URL}/a2a/publish"
HEARTBEAT_ENDPOINT = f"{HUB_URL}/a2a/heartbeat"


def compute_hash(obj):
    """Python canonical JSON: sorted keys, no spaces after :,."""
    canonical = json.dumps(obj, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def load_asset(path):
    with open(path) as f:
        return json.load(f)


def verify_and_tag(asset, asset_type):
    """Compute hash, verify against asset_id if present, return with asset_id."""
    computed = compute_hash(asset)
    existing = asset.get("asset_id", "").replace("sha256:", "")
    if existing and existing != computed:
        print(f"  WARNING: {asset_type} asset_id mismatch!")
        print(f"    Expected: sha256:{computed}")
        print(f"    Got: sha256:{existing}")
    asset_id = f"sha256:{computed}"
    return asset_id


def publish(node_id, node_secret, assets):
    """Send publish request to Hub."""
    import urllib.request

    req = {
        "protocol": "gep-a2a",
        "protocol_version": "1.0.0",
        "message_type": "publish",
        "message_id": f"msg_{int(time.time())}_{os.urandom(4).hex()}",
        "sender_id": node_id,
        "timestamp": f"{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}",
        "payload": {"assets": assets},
    }

    body = json.dumps(req).encode("utf-8")
    request = urllib.request.Request(
        PUBLISH_ENDPOINT,
        data=body,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {node_secret}",
        },
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=30) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    return result


def main():
    if len(sys.argv) < 4:
        print("Usage: publish_asset.py <gene.json> <capsule.json> <event.json>")
        sys.exit(1)

    node_id = os.environ.get("EVOMAP_NODE_ID")
    node_secret = os.environ.get("EVOMAP_NODE_SECRET")

    if not node_id or not node_secret:
        print("Error: Set EVOMAP_NODE_ID and EVOMAP_NODE_SECRET environment variables")
        sys.exit(1)

    print(f"Loading assets...")
    gene = load_asset(sys.argv[1])
    capsule = load_asset(sys.argv[2])
    event = load_asset(sys.argv[3])

    # Verify and tag
    gene_id = verify_and_tag(gene, "Gene")
    capsule_id = verify_and_tag(capsule, "Capsule")
    event_id = verify_and_tag(event, "Event")

    # Update capsule_id in event
    event["capsule_id"] = capsule_id

    # Build assets with verified asset_ids
    assets = [
        dict(gene, **{"asset_id": gene_id}),
        dict(capsule, **{"asset_id": capsule_id}),
        dict(event, **{"asset_id": event_id}),
    ]

    print(f"Gene:    {gene_id}")
    print(f"Capsule: {capsule_id}")
    print(f"Event:   {event_id}")
    print(f"Publishing to Hub...")

    result = publish(node_id, node_secret, assets)

    if "error" in result:
        print(f"Error: {result['error']}")
        if "correction" in result:
            print(f"Fix: {result['correction']['fix']}")
        sys.exit(1)

    decision = result.get("payload", {}).get("decision", "unknown")
    reason = result.get("payload", {}).get("reason", "")
    print(f"\nResult: {decision} ({reason})")


if __name__ == "__main__":
    main()
