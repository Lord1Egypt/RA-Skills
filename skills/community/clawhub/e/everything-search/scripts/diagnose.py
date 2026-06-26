#!/usr/bin/env python3
"""
Complete diagnostic tool for Everything Search.

Runs all checks and provides detailed troubleshooting information.
"""

import sys
import os
import socket
import urllib.request
import json
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


def print_section(title):
    """Print section header."""
    print()
    print("=" * 60)
    print(title)
    print("=" * 60)


def check_everything_process():
    """Check if Everything process is running."""
    print("\n[1/6] Checking Everything Process...")

    try:
        import subprocess

        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq Everything.exe"],
            capture_output=True,
            text=True,
            timeout=5,
        )

        count = result.stdout.count("Everything.exe")

        if count > 0:
            print(f"   ✓ Found {count} Everything process(es)")
            return True, count
        else:
            print("   ✗ No Everything process found")
            print("   → Solution: Start Everything application")
            return False, 0
    except Exception as e:
        print(f"   ? Unable to check: {e}")
        return None, 0


def check_port_listening():
    """Check if port 2853 is listening."""
    print("\n[2/6] Checking Port 2853...")

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex(("127.0.0.1", 2853))
        sock.close()

        if result == 0:
            print("   ✓ Port 2853 is OPEN and listening")
            return True
        else:
            print("   ✗ Port 2853 is CLOSED")
            print(
                "   → Solution: Enable HTTP Server in Everything (Ctrl+P → HTTP Server)"
            )
            return False
    except Exception as e:
        print(f"   ? Error: {e}")
        return False


def check_http_server():
    """Check if HTTP server is responding."""
    print("\n[3/6] Checking HTTP Server...")

    try:
        req = urllib.request.Request("http://127.0.0.1:2853/")
        req.add_header("User-Agent", "Mozilla/5.0")

        start = time.time()
        with urllib.request.urlopen(req, timeout=5) as response:
            elapsed = time.time() - start

            if response.status == 200:
                print(
                    f"   ✓ HTTP server responding (Status: 200, Time: {elapsed:.2f}s)"
                )
                return True
            else:
                print(f"   ✗ Unexpected status: {response.status}")
                return False
    except Exception as e:
        print(f"   ✗ HTTP error: {e}")
        print("   → Solution: Restart Everything after enabling HTTP server")
        return False


def check_search_api():
    """Check if search API is working."""
    print("\n[4/6] Checking Search API...")

    try:
        url = "http://127.0.0.1:2853/?search=test&json=1&maxresults=5"
        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0")

        start = time.time()
        with urllib.request.urlopen(req, timeout=10) as response:
            elapsed = time.time() - start
            data = json.loads(response.read().decode())

            if "totalResults" in data:
                total = data.get("totalResults", 0)
                print(f"   ✓ Search API working ({total} results in {elapsed:.2f}s)")
                return True, total
            else:
                print(f"   ✗ Invalid API response")
                return False, 0
    except Exception as e:
        print(f"   ✗ API error: {e}")
        return False, 0


def check_chinese_search():
    """Check if Chinese character search works."""
    print("\n[5/6] Checking Chinese Search...")

    try:
        import urllib.parse

        keyword = "测试"
        encoded = urllib.parse.quote(keyword)
        url = f"http://127.0.0.1:2853/?search={encoded}&json=1&maxresults=5"

        req = urllib.request.Request(url)
        req.add_header("User-Agent", "Mozilla/5.0")

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())

            if "totalResults" in data:
                print(f"   ✓ Chinese search working")
                return True
            else:
                print(f"   ✗ Invalid response")
                return False
    except Exception as e:
        print(f"   ✗ Chinese search error: {e}")
        return False


def check_config_file():
    """Check Everything configuration file."""
    print("\n[6/6] Checking Configuration File...")

    config_paths = [
        os.path.expandvars(r"%APPDATA%\Everything\Everything.ini"),
        os.path.expandvars(r"%USERPROFILE%\AppData\Roaming\Everything\Everything.ini"),
    ]

    for config_path in config_paths:
        if os.path.exists(config_path):
            print(f"   ✓ Config file found: {config_path}")

            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    content = f.read()

                    if "http_server" in content.lower():
                        print("   ✓ HTTP server section exists")

                        if "enabled=1" in content:
                            print("   ✓ HTTP server enabled in config")
                        else:
                            print("   ⚠ HTTP server not enabled in config")
                            print(
                                "   → Note: Config file changes don't auto-enable HTTP server"
                            )
                            print(
                                "   → Must enable via GUI: Ctrl+P → HTTP Server → Check 'Enable'"
                            )

                        if "port=2853" in content:
                            print("   ✓ Port 2853 configured")
                        else:
                            print("   ⚠ Port may not be 2853")
                    else:
                        print("   ⚠ HTTP server section not found")

                    return True
            except Exception as e:
                print(f"   ? Error reading config: {e}")
                return None

    print("   ⚠ Config file not found in standard locations")
    return None


def main():
    print_section("Everything Search - Complete Diagnostic")

    # Run all checks
    process_ok, process_count = check_everything_process()
    port_ok = check_port_listening()
    http_ok = check_http_server()
    api_ok, result_count = check_search_api()
    chinese_ok = check_chinese_search()
    config_ok = check_config_file()

    # Summary
    print_section("Diagnostic Summary")

    checks = [
        ("Everything Process", process_ok),
        ("Port 2853", port_ok),
        ("HTTP Server", http_ok),
        ("Search API", api_ok),
        ("Chinese Search", chinese_ok),
        ("Config File", config_ok),
    ]

    passed = sum(1 for _, ok in checks if ok is True)
    total = len(checks)

    for name, ok in checks:
        if ok is True:
            status = "✓"
        elif ok is False:
            status = "✗"
        else:
            status = "?"
        print(f"   {status} {name}")

    print()
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("\n✅ Everything is perfectly configured!")
        print("\nYou can now use the search skills:")
        print('  - python examples/basic_search.py "关键词"')
        print('  - python examples/search_photos.py "张三"')
        print('  - python examples/advanced_search.py --type jpg "照片"')
        return 0
    else:
        print("\n❌ Configuration issues detected!")

        print_section("Troubleshooting Guide")

        if not process_ok:
            print("\n1. Everything Not Running:")
            print("   → Download: https://www.voidtools.com/")
            print("   → Install and launch Everything")

        if not port_ok or not http_ok:
            print("\n2. HTTP Server Not Enabled:")
            print("   → Open Everything window")
            print("   → Press Ctrl+P (Options)")
            print("   → Click 'HTTP Server' in left panel")
            print("   → CHECK '☑ Enable HTTP server'")
            print("   → Set Port: 2853")
            print("   → Click OK")
            print("   → Completely exit Everything (tray icon → Exit)")
            print("   → Restart Everything")

        if not api_ok:
            print("\n3. API Not Working:")
            print("   → Verify HTTP server is enabled")
            print("   → Check firewall is not blocking port 2853")
            print("   → Try: http://127.0.0.1:2853/ in browser")

        if not chinese_ok:
            print("\n4. Chinese Search Issues:")
            print("   → This is usually automatic")
            print("   → Make sure to URL-encode Chinese characters")
            print('   → Use: urllib.parse.quote("中文")')

        print()
        print("For detailed troubleshooting, see:")
        print("  - docs/troubleshooting.md")
        print("  - SKILL.md")

        return 1


if __name__ == "__main__":
    sys.exit(main())
