"""
Brother DCP-T426W Printer — Main Print CLI

Primary: CUPS + IPP driverless (full support: text, images, PDFs)
Fallback: TCP direct printing (text only, no CUPS required)

Usage:
    python scripts/print.py --text "Hello World"
    python scripts/print.py --file document.txt
    python scripts/print.py --file photo.jpg
    python scripts/print.py --status
    python scripts/print.py --test
"""

import argparse
import os
import socket
import subprocess
import sys
from datetime import datetime

PRINTER_IP = "192.168.50.232"
PRINTER_PORT = 9100
PRINTER_NAME = "Brother_DCP-T426W"
SOCKET_TIMEOUT = 10  # seconds


def main():
    parser = argparse.ArgumentParser(
        description="Print to Brother DCP-T426W (IPP/CUPS primary, TCP fallback)"
    )
    parser.add_argument("--text", "-t", help="Text string to print")
    parser.add_argument("--file", "-f", help="File to print")
    parser.add_argument(
        "--mode",
        choices=["normal", "receipt"],
        default="normal",
        help="Print formatting mode",
    )
    parser.add_argument("--status", "-s", action="store_true", help="Check printer status")
    parser.add_argument("--test", action="store_true", help="Print a test page")
    parser.add_argument(
        "--method",
        choices=["tcp", "cups"],
        default="cups",
        help="Print method (default: cups/IPP)",
    )

    args = parser.parse_args()

    if args.status:
        check_printer_status()
        return

    if args.test:
        if args.method == "cups":
            print_test_page_cups()
        else:
            print_test_page_tcp()
        return

    if not args.text and not args.file:
        parser.print_help()
        sys.exit(1)

    if args.method == "tcp":
        if args.text:
            print_text_tcp(args.text, args.mode)
        elif args.file:
            print_file_tcp(args.file)
    else:
        if args.text:
            print_text_cups(args.text, args.mode)
        elif args.file:
            print_file_cups(args.file)


# ─── CUPS/IPP Printing (primary, full support) ─────────────────────────────


def send_to_printer(data: bytes):
    """Send raw bytes to printer via TCP socket port 9100."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(SOCKET_TIMEOUT)
    try:
        sock.connect((PRINTER_IP, PRINTER_PORT))
        sock.sendall(data)
        sock.shutdown(socket.SHUT_WR)
        # Read printer response (status feedback)
        sock.settimeout(3)
        try:
            response = sock.recv(1024)
            if response:
                return response
        except socket.timeout:
            pass
    except ConnectionRefusedError:
        print(f"Error: Printer {PRINTER_IP}:{PRINTER_PORT} refused connection.")
        print("Check: printer is on, connected to WiFi, correct IP address.")
        sys.exit(1)
    except socket.timeout:
        print(f"Error: Connection to {PRINTER_IP}:{PRINTER_PORT} timed out.")
        sys.exit(1)
    finally:
        sock.close()
    return b""


def print_text_tcp(text: str, mode: str):
    """Print text via TCP direct."""
    if mode == "receipt":
        text = format_receipt(text)

    # PJL + plain text: most Brother printers accept this on port 9100
    # PJL header enters printer language mode, then we send text
    pjl_header = b"\x1b%-12345X@PJL\n@PJL ENTER LANGUAGE = PLAINTEXT\n"
    pjl_footer = b"\x1b%-12345X\n"
    form_feed = b"\x0c"  # Form feed to eject page

    data = pjl_header + text.encode("utf-8") + b"\n" + form_feed + pjl_footer
    send_to_printer(data)
    print("Print job sent via TCP. Check printer for output.")


def print_file_tcp(filepath: str):
    """Print a file via TCP direct. Text files sent as-is, binary files sent raw."""
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    abs_path = os.path.abspath(filepath)
    ext = os.path.splitext(filepath)[1].lower()

    with open(abs_path, "rb") as f:
        data = f.read()

    if ext in (".txt", ".csv", ".log", ".md", ".html"):
        # Text files: wrap in PJL for proper handling
        pjl_header = b"\x1b%-12345X@PJL\n@PJL ENTER LANGUAGE = PLAINTEXT\n"
        pjl_footer = b"\x1b%-12345X\n"
        form_feed = b"\x0c"
        data = pjl_header + data + b"\n" + form_feed + pjl_footer
    elif ext in (".jpg", ".jpeg", ".png", ".gif", ".bmp"):
        print(
            f"Warning: Image files ({ext}) need raster conversion.\n"
            f"TCP direct sends raw bytes which the printer may not interpret.\n"
            f"Use --method cups for image printing, or convert to PDF first."
        )
        print("Sending raw data anyway...")

    send_to_printer(data)
    print(f"File '{filepath}' sent via TCP. Check printer for output.")


def print_test_page_tcp():
    """Print a test page via TCP."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = (
        f"=== Brother DCP-T426W Test Page ===\n"
        f"Printer IP: {PRINTER_IP}\n"
        f"Print Method: TCP Direct (port {PRINTER_PORT})\n"
        f"Date: {now}\n"
        f"Status: OK\n"
        f"=================================\n"
    )
    print_text_tcp(text, "normal")


# ─── TCP Direct Printing (fallback, text only) ─────────────────────────────


def run_cups(args: list[str]) -> subprocess.CompletedProcess:
    """Run a CUPS command and handle errors."""
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"CUPS Error: {result.stderr.strip()}")
        sys.exit(1)
    return result


def print_text_cups(text: str, mode: str):
    """Print text via CUPS."""
    if mode == "receipt":
        text = format_receipt(text)

    process = subprocess.Popen(
        ["lp", "-d", PRINTER_NAME, "-"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = process.communicate(input=text.encode("utf-8"))
    if process.returncode != 0:
        print(f"CUPS Error: {stderr.decode().strip()}")
        sys.exit(1)
    print(stdout.decode().strip())


def print_file_cups(filepath: str):
    """Print a file via CUPS."""
    if not os.path.exists(filepath):
        print(f"Error: File not found: {filepath}")
        sys.exit(1)

    abs_path = os.path.abspath(filepath)
    result = subprocess.run(
        ["lp", "-d", PRINTER_NAME, abs_path],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"CUPS Error: {result.stderr.strip()}")
        sys.exit(1)
    print(result.stdout.strip())


def print_test_page_cups():
    """Print a test page via CUPS."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = (
        f"=== Brother DCP-T426W Test Page ===\n"
        f"Printer: {PRINTER_NAME}\n"
        f"IP: {PRINTER_IP}\n"
        f"Date: {now}\n"
        f"Status: OK\n"
    )
    print_text_cups(text, "normal")


# ─── Shared ────────────────────────────────────────────────────────────────


def format_receipt(text: str, width: int = 40) -> str:
    """Format text in a receipt style."""
    lines = text.strip().split("\n")
    border = "=" * width

    parts = [border, ""]
    for i, line in enumerate(lines):
        if i == 0:
            parts.append(line.center(width))
            parts.append("")
        else:
            parts.append(line)
    parts.append("")
    parts.append(border)
    return "\n".join(parts)


def check_printer_status():
    """Check printer status via TCP + CUPS (if available)."""
    # TCP connectivity (always available)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((PRINTER_IP, PRINTER_PORT))
        sock.close()
        tcp_status = "Online (TCP reachable)"
    except Exception as e:
        tcp_status = f"Offline ({e})"

    print(f"Printer: {PRINTER_NAME}")
    print(f"IP: {PRINTER_IP}:{PRINTER_PORT}")
    print(f"Network: {tcp_status}")

    # CUPS status (optional, if available)
    try:
        result = subprocess.run(
            ["lpstat", "-p", PRINTER_NAME],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            print(f"CUPS: {result.stdout.strip()}")
            result = subprocess.run(
                ["lpstat", "-v", PRINTER_NAME],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.stdout:
                print(f"Device: {result.stdout.strip()}")
        else:
            print("CUPS: printer not configured (TCP direct still works)")
    except FileNotFoundError:
        print("CUPS: not installed (TCP direct still works)")
    except subprocess.TimeoutExpired:
        pass


if __name__ == "__main__":
    main()
