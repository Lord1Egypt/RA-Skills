# Real DLNA media server mode

Use this when the receiver does not behave reliably with raw `SetAVTransportURI` or ad-hoc stream URLs.

The bundled `simple_dlna_server.py` script runs a minimal but real UPnP/DLNA MediaServer:
- serves a UPnP device description
- advertises over SSDP discovery
- exposes `ContentDirectory`
- exposes `ConnectionManager`
- serves actual media files over HTTP

## Typical workflow

Let the user choose the music directory or directories. Do not assume a fixed library path.

### 1. Scan one folder

```bash
python3 skills/denon-avr-control/scripts/simple_dlna_server.py scan --root ~/Music
```

### 1b. Scan multiple folders

```bash
python3 skills/denon-avr-control/scripts/simple_dlna_server.py scan --root ~/Music --root ~/Downloads/music --root "D:\\Music"
```

### 2. Start the server

```bash
python3 skills/denon-avr-control/scripts/simple_dlna_server.py serve --root ~/Music --host <lan-ip> --port 8200 --name "OpenClaw Music"
```

### 2b. Start the server with multiple music roots

```bash
python3 skills/denon-avr-control/scripts/simple_dlna_server.py serve --root ~/Music --root ~/Downloads/music --host <lan-ip> --port 8200 --name "OpenClaw Music"
```

Keep that process running.

### Stop the server later

```bash
python3 skills/denon-avr-control/scripts/simple_dlna_server.py stop
```

### 3. On the receiver

- Open the network music / local music area
- Wait for the server to appear
- Browse the exposed library
- Play the desired track

## Notes

- This is a **minimal** MediaServer, not a full commercial DLNA stack.
- It is still much more correct than handing the receiver a one-off raw file URL.
- The user should choose the library path(s). The script accepts repeated `--root` flags.
- Windows support is good because the script uses only the Python standard library. The main caveat is allowing inbound firewall access to the chosen port and to SSDP discovery on UDP 1900.
- If the Denon does not discover it immediately, wait a bit or reopen the Local Music source.
- On receivers that expose multiple source modes, selecting the network music input may be required before playback becomes audible.
