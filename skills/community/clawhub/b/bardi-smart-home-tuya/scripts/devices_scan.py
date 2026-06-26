#!/usr/bin/env python3
"""Tuya Local Network Device Scanner.

Discovers Tuya devices on the local network via UDP broadcast.
Useful for finding device IPs, IDs, and protocol versions.

Usage:
    python3 tuya_scan.py [--timeout 10] [--verbose]

Requirements:
    pip install tinytuya
"""

import json
import socket
import struct
import sys
import time

MCAST_GRP = "255.255.255.255"
MCAST_PORT_1 = 6666
MCAST_PORT_2 = 6667
MCAST_PORT_3 = 7000
MESSAGE = b'{"ip":"192.168.1.66","gwId":"00000000000000000000","active":2,"ablilty":0,"mode":0,"encrypt":true,"productKey":"","version":"3.3"}'
BROADCAST = b'000055aa000000000000000000000000000000000000000000000000000000000000001200000000336f1320'


def scan(timeout=10):
    """Scan for Tuya devices on local network."""
    devices = {}
    ports = [MCAST_PORT_1, MCAST_PORT_2, MCAST_PORT_3]

    # Create UDP sockets for each port
    sockets = []
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.settimeout(0.5)
            sock.bind(("", port))
            sockets.append((sock, port))
        except OSError:
            pass

    # Also create a sending socket
    sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    start = time.time()
    while time.time() - start < timeout:
        # Send broadcasts
        for port in ports:
            try:
                sender.sendto(MESSAGE, (MCAST_GRP, port))
                sender.sendto(BROADCAST, (MCAST_GRP, port))
            except Exception:
                pass

        # Listen for responses
        for sock, port in sockets:
            try:
                data, addr = sock.recvfrom(4096)
                ip = addr[0]
                if ip not in devices:
                    try:
                        # Try to decode JSON response
                        text = data.decode("utf-8", errors="ignore")
                        # Find JSON in response
                        start_idx = text.find("{")
                        if start_idx >= 0:
                            info = json.loads(text[start_idx:])
                            devices[ip] = {
                                "ip": ip,
                                "gwId": info.get("gwId", "unknown"),
                                "version": info.get("version", "unknown"),
                                "productKey": info.get("productKey", ""),
                            }
                    except (json.JSONDecodeError, ValueError):
                        devices[ip] = {
                            "ip": ip,
                            "gwId": "unknown",
                            "version": "unknown",
                            "productKey": "",
                        }
            except socket.timeout:
                continue
            except Exception:
                continue

        time.sleep(0.2)

    # Cleanup
    sender.close()
    for sock, _ in sockets:
        sock.close()

    return devices


def main():
    timeout = 10
    verbose = False

    for i, arg in enumerate(sys.argv[1:], 1):
        if arg == "--timeout" and i < len(sys.argv) - 1:
            timeout = int(sys.argv[i + 1])
        elif arg == "--verbose":
            verbose = True
        elif arg in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)

    print(f"Scanning local network (timeout: {timeout}s)...\n")

    devices = scan(timeout)

    if not devices:
        print("No devices found.")
        print("\nTips:")
        print("  - Ensure devices are on the same network")
        print("  - Try increasing timeout: --timeout 20")
        print("  - Devices may need to be re-paired to WiFi")
        sys.exit(1)

    print(f"Found {len(devices)} device(s):\n")

    results = list(devices.values())
    for i, dev in enumerate(results, 1):
        print(f"  [{i}] IP: {dev['ip']}")
        print(f"      Device ID: {dev['gwId']}")
        print(f"      Version: {dev['version']}")
        if dev["productKey"]:
            print(f"      Product Key: {dev['productKey']}")
        print()

    # Output as JSON for scripting
    print("---")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
