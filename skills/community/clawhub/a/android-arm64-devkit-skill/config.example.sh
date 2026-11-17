# Copy to config.sh and edit. config.sh is gitignored and must never be committed.
#
# Leave ADB_HOST empty to use a USB-attached device only.
# Set it to a DNS name reachable over a VPN (e.g. Tailscale MagicDNS) to use
# wireless debugging.

# --- transport ---
ADB_HOST=""              # e.g. my-phone        (empty = USB only)
ADB_TCP_PORT=""          # leave empty: the scripts discover it
DEVICE_SERIAL=""         # from `adb devices -l`; required when ADB_HOST is empty

# --- remote adb server (optional) ---
# If the device is attached to another machine, run adb there instead of locally.
# Leave empty to use the local adb.
ADB_REMOTE_HOST=""       # e.g. my-desktop  (an ssh alias)
ADB_REMOTE_BIN=""        # e.g. C:/Users/<you>/AppData/Local/Android/Sdk/platform-tools/adb.exe

# --- app under test ---
PACKAGE_ID=""            # e.g. com.example.app
LAUNCH_ACTIVITY=""       # e.g. .MainActivity  (empty = read from the APK)
