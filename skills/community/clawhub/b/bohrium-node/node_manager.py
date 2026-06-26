"""
Programmatic node management: create, query pricing, get SSH credentials.

Usage:
    python node_manager.py list
    python node_manager.py resources
    python node_manager.py price --sku 388 --project_id 154
    python node_manager.py create --project_id 154 --name dev-box --image_id 2168 --sku 388
    python node_manager.py ssh --machine_id 1427300
"""

import argparse
import json
import os
import sys

import requests

AK = os.environ.get("ACCESS_KEY", "")
BASE = "https://openapi.dp.tech/openapi/v1/node"
HEADERS = {"accessKey": AK}
HEADERS_JSON = {**HEADERS, "Content-Type": "application/json"}


def list_resources():
    """Show available machine configs and disk sizes."""
    r = requests.get(f"{BASE}/resources", headers=HEADERS)
    data = r.json().get("data", {})

    print("Available disk sizes:", data.get("disks", []))

    print("\nCPU options:")
    for item in data.get("cpuList", []):
        print(f"  SKU {item['value']:>4} | {item['label']}")

    print("\nGPU options:")
    for item in data.get("gpuList", []):
        print(f"  SKU {item['value']:>4} | {item['label']}")


def query_price(sku_id: int, project_id: int):
    """Query hourly price for a machine SKU."""
    r = requests.get(
        f"{BASE}/resources/price",
        headers=HEADERS,
        params={"skuId": sku_id, "projectId": project_id},
    )
    price = r.json().get("data", {}).get("price", "?")
    print(f"SKU {sku_id} price: ¥{price}/hour")


def create_node(project_id: int, name: str, image_id: int, sku_id: int, disk_size: int = 20):
    """Create a node via API (non-interactive)."""
    r = requests.post(
        f"{BASE}/add",
        headers=HEADERS_JSON,
        json={
            "projectId": project_id,
            "name": name,
            "imageId": image_id,
            "machineConfig": {"type": 0, "value": sku_id, "label": ""},
            "diskSize": disk_size,
        },
    )
    result = r.json()
    if result.get("code") == 0:
        machine_id = result.get("data", {}).get("machineId")
        print(f"Node created! machineId: {machine_id}")
    else:
        print(f"Failed: {result}")


def get_ssh_info(machine_id: int):
    """Get SSH credentials for a node."""
    r = requests.get(f"{BASE}/{machine_id}", headers=HEADERS)
    data = r.json().get("data", {})
    print(f"Node:     {data.get('nodeName')}")
    print(f"Status:   {data.get('status')}")
    print(f"IP:       {data.get('ip')}")
    print(f"Domain:   {data.get('domainName')}")
    print(f"User:     {data.get('nodeUser')}")
    print(f"Password: {data.get('nodePwd')}")
    print(f"\nSSH command:")
    domain = data.get("domainName") or data.get("ip")
    print(f"  ssh {data.get('nodeUser', 'root')}@{domain}")


def main():
    parser = argparse.ArgumentParser(description="Bohrium node manager")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list", help="List nodes (uses bohr CLI)")
    sub.add_parser("resources", help="Show available machine resources")

    p_price = sub.add_parser("price", help="Query machine price")
    p_price.add_argument("--sku", type=int, required=True)
    p_price.add_argument("--project_id", type=int, required=True)

    p_create = sub.add_parser("create", help="Create node via API")
    p_create.add_argument("--project_id", type=int, required=True)
    p_create.add_argument("--name", type=str, required=True)
    p_create.add_argument("--image_id", type=int, required=True)
    p_create.add_argument("--sku", type=int, required=True)
    p_create.add_argument("--disk", type=int, default=20)

    p_ssh = sub.add_parser("ssh", help="Get SSH credentials")
    p_ssh.add_argument("--machine_id", type=int, required=True)

    args = parser.parse_args()

    if not AK:
        print("ERROR: ACCESS_KEY environment variable not set")
        sys.exit(1)

    if args.cmd == "list":
        os.system("bohr node list")
    elif args.cmd == "resources":
        list_resources()
    elif args.cmd == "price":
        query_price(args.sku, args.project_id)
    elif args.cmd == "create":
        create_node(args.project_id, args.name, args.image_id, args.sku, args.disk)
    elif args.cmd == "ssh":
        get_ssh_info(args.machine_id)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
