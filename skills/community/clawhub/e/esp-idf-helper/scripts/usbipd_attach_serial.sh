#!/usr/bin/env bash
set -euo pipefail

# Auto map a USB serial device from Windows to WSL2 via usbipd
# Usage:
#   usbipd_attach_serial.sh [--busid <BUSID>] [--distro <DISTRO>] [--keyword <TEXT>] [--dry-run]

BUSID=""
DISTRO=""
KEYWORD=""
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage:
  usbipd_attach_serial.sh [--busid <BUSID>] [--distro <DISTRO>] [--keyword <TEXT>] [--dry-run]

Options:
  --busid <BUSID>    Specify bus id directly, e.g. 2-1
  --distro <DISTRO>  WSL distro name for attach command (optional)
  --keyword <TEXT>   Filter device line by keyword (e.g. ESP32, COM37, CP210x)
  --list             List all matching devices and exit
  --dry-run          Print command only, do not execute
  --bind             Only bind the device (skip attach), useful for first-time setup
  -h, --help         Show help

Behavior:
  1) Reads `usbipd list` from Windows PowerShell
  2) Auto-selects first "Connected" serial-like device (prefer STATE=Shared)
  3) Executes: usbipd bind --busid=<BUSID> (admin required, makes device shareable)
  4) Executes: usbipd attach --wsl --busid=<BUSID> [--distribution <DISTRO>]
  5) Prints detected /dev/ttyACM* and /dev/ttyUSB* in WSL
  (Use --bind to only perform bind, skip attach)

Multiple devices:
  When --keyword matches multiple devices, all matching devices will be bound/attached.
EOF
}

BIND_ONLY=0
LIST_MODE=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --busid) BUSID="${2:-}"; shift 2;;
    --distro) DISTRO="${2:-}"; shift 2;;
    --keyword) KEYWORD="${2:-}"; shift 2;;
    --list) LIST_MODE=1; shift;;
    --dry-run) DRY_RUN=1; shift;;
    --bind) BIND_ONLY=1; shift;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown arg: $1" >&2; usage; exit 2;;
  esac
done

PS_LIST=$(powershell.exe -NoProfile -Command "usbipd list" | tr -d '\r')

echo "=== usbipd list ==="
echo "$PS_LIST"

get_serial_devices() {
  local lines
  lines=$(echo "$PS_LIST" | awk '
    BEGIN{inConnected=0}
    /^Connected:/ {inConnected=1; next}
    /^Persisted:/ {inConnected=0}
    { if (inConnected) print }
  ')

  # Keep likely serial rows only
  local serial_rows
  serial_rows=$(echo "$lines" | grep -E "USB 串行设备|USB JTAG/serial debug unit|USB-Enhanced-SERIAL|CP210|CH34|FTDI|Serial|UART|ESP32|COM" || true)

  if [[ -n "$KEYWORD" ]]; then
    serial_rows=$(echo "$serial_rows" | grep -i -- "$KEYWORD" || true)
  fi

  echo "$serial_rows"
}

auto_pick_busid() {
  local serial_rows="$1"
  # Prefer Shared first
  local preferred
  preferred=$(echo "$serial_rows" | grep -E "Shared\s*$" | head -n1 || true)
  if [[ -z "$preferred" ]]; then
    preferred=$(echo "$serial_rows" | head -n1 || true)
  fi

  if [[ -n "$preferred" ]]; then
    echo "$preferred" | awk '{print $1}'
  fi
}

# Get all matching serial devices
ALL_DEVICES=$(get_serial_devices)

# List mode: print matching devices and exit
if [[ "$LIST_MODE" == "1" ]]; then
  if [[ -z "$ALL_DEVICES" ]]; then
    echo "No matching serial devices found."
    exit 0
  fi
  echo ""
  echo "=== Matching serial devices ==="
  echo "$ALL_DEVICES"
  exit 0
fi

# Auto-pick busid if not specified
if [[ -z "$BUSID" ]]; then
  BUSID=$(auto_pick_busid "$ALL_DEVICES" || true)
fi

if [[ -z "$BUSID" ]]; then
  echo "ERROR: No candidate BUSID found. Please specify --busid <BUSID> or use --list to see available devices." >&2
  exit 1
fi

# Get all matching BUSIDs for batch processing
ALL_BUSIDS=$(echo "$ALL_DEVICES" | awk '{print $1}')

# When using keyword and multiple devices found, process all of them
if [[ -n "$KEYWORD" && $(echo "$ALL_BUSIDS" | wc -l) -gt 1 ]]; then
  echo ""
  echo "=== Multiple devices matched, processing all ==="
  echo "$ALL_DEVICES"
  echo ""
fi

# Process each BUSID
process_device() {
  local busid="$1"
  
  local cmd="usbipd attach --wsl --busid=$busid"
  if [[ -n "$DISTRO" ]]; then
    cmd+=" --distribution $DISTRO"
  fi

  echo ""
  echo "--- Processing BUSID: $busid ---"
  echo "Attach command: $cmd"

  # Bind the device first (admin may be required for first-time bind)
  local bind_cmd="usbipd bind --busid=$busid"
  echo "Bind command: $bind_cmd"

  if [[ "$DRY_RUN" == "1" ]]; then
    echo "[dry-run] not executing bind/attach"
    return 0
  fi

  # Execute bind (may fail if already bound, that's ok)
  set +e
  local bind_out
  bind_out=$(powershell.exe -NoProfile -Command "$bind_cmd" 2>&1)
  local bind_rc=$?
  set -e
  if [[ $bind_rc -ne 0 ]]; then
    if echo "$bind_out" | grep -qi "already bound\|already shared"; then
      echo "[info] device already bound/shared, continue."
    else
      echo "[warn] bind failed (may require admin): $bind_out"
    fi
  else
    echo "$bind_out"
  fi

  if [[ "$BIND_ONLY" == "1" ]]; then
    echo "[info] bind-only mode, skipping attach."
    return 0
  fi

  set +e
  local attach_out
  attach_out=$(powershell.exe -NoProfile -Command "$cmd" 2>&1)
  local attach_rc=$?
  set -e
  echo "$attach_out"
  if [[ $attach_rc -ne 0 ]]; then
    if echo "$attach_out" | grep -qi "already attached"; then
      echo "[info] device already attached, continue."
    else
      echo "[error] attach failed" >&2
      return $attach_rc
    fi
  fi
}

# Process single device or all devices
if [[ -n "$KEYWORD" && $(echo "$ALL_BUSIDS" | wc -l) -gt 1 ]]; then
  # Multiple devices mode - process each busid
  for busid in $ALL_BUSIDS; do
    [[ -n "$busid" ]] && process_device "$busid"
  done
else
  # Single device mode
  process_device "$BUSID"
fi

echo ""
echo "=== WSL serial nodes ==="
found=0
# Check various serial device patterns
for pat in /dev/ttyACM* /dev/ttyUSB*; do
  for dev in $pat; do
    if [[ -e "$dev" ]]; then
      echo "$dev"
      found=1
    fi
  done
done
if [[ "$found" -eq 0 ]]; then
  echo "No /dev/ttyACM* or /dev/ttyUSB* yet."
fi

# Also show USB device info if available
if command -v lsusb >/dev/null 2>&1; then
  echo ""
  echo "=== USB devices (lsusb) ==="
  lsusb | grep -i "serial\|uart\|ch34\|cp210\|ftdi" || echo "No matching USB serial devices found in lsusb"
fi

echo ""
echo "Done."
