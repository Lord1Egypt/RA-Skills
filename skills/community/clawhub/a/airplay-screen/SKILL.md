---
name: airplay-screen
description: See the user's iPhone or iPad screen. Sets up airplay-mcp, a local AirPlay receiver, registers it as an MCP server, and then reads the mirrored screen frame by frame. Use when the user wants you to look at, follow or save what is on their phone.
version: 0.2.0
metadata:
  openclaw:
    emoji: "📱"
    homepage: https://github.com/feedthedogs/airplay-mcp
    os: [macos, linux, windows]
    requires:
      bins: [uv]
    install:
      - kind: uv
        package: airplay-mcp
        bins: [airplay-mcp]
    envVars:
      - name: AIRPLAY_NAME
        required: false
        description: Name the phone shows under Screen Mirroring (default "AI Screen")
      - name: AIRPLAY_PIN
        required: false
        description: Pairing PIN if the phone asks for one (default 3939)
---

# AirPlay Screen

[airplay-mcp](https://github.com/feedthedogs/airplay-mcp) (MIT, on PyPI) turns this computer into an AirPlay receiver. The user mirrors their iPhone or iPad to it, and you get the screen through MCP tools. Everything stays on this machine. The receiver only listens on the local network and makes no outbound connections. The AirPlay protocol and FairPlay are handled in pure Python — no firmware extraction or external programs needed.

**It only works when this machine is on the same Wi-Fi as the phone.** A cloud VM or VPS can't see the phone. Neither can a network behind a VPN or a guest network, because they block mDNS. If that's the setup, tell the user so and stop.

## One-time setup

Tell the user what you are about to install before you run each step.

1. **Install the server:** `uv tool install --upgrade airplay-mcp` or `pip install --upgrade airplay-mcp`. Note the absolute path of the `airplay-mcp` executable for step 2, because its install folder is often not on the gateway's `PATH`. Check it with `airplay-mcp --help`.
2. **Register the MCP server** with the absolute path for the command:
   ```sh
   openclaw mcp set airplay '{"command":"/absolute/path/to/airplay-mcp"}'
   ```
   Confirm it with `openclaw mcp list`. The tools appear in a **new session**, or after the gateway reloads.
3. **Firewall:** the first time the receiver runs, allow it through the firewall. The phone connects over TCP and mDNS (UDP 5353).

## Using it

1. `start_receiver`, then tell the user: *Control Centre > Screen Mirroring > "AI Screen"* (PIN `3939` if asked).
2. `wait_for_change` blocks until the first frame arrives, and afterwards until the screen next changes. Pass `since_frame=N` for the frame you hold.
3. `get_screen` to look, or `save_screen` to write a full-resolution file and return only its path. Use `mode='changes'` after the user acts, and `region` to read small detail. `read_screen_text` is cheaper for text-heavy screens, if it is installed.
4. Repeat 2 and 3, then `stop_receiver` when done.

## Troubleshooting

- **The phone doesn't list "AI Screen".** Check the network and the firewall (see above).
- **To see the log:** `airplay-mcp --autostart -v`.
