# Experimental DLNA push to a Denon receiver

Use this when the user wants the receiver itself to fetch and play a local file over the network, instead of playing on the local computer.

## How it works

1. Select a local audio file.
2. Start a small HTTP server on the local machine to expose that file.
3. Send `SetAVTransportURI` to the Denon MediaRenderer.
4. Send `Play`.
5. Keep the HTTP server alive while the receiver is playing.

## Important constraints

- The local machine and the receiver must be on the same LAN.
- The receiver must be able to reach the local machine's HTTP server.
- Local firewall rules can break playback.
- This is currently **single-track push**. Queue/playlist support can be layered on later.
- File compatibility still depends on what the Denon can decode.

## Basic examples

### Scan a folder

```bash
python3 skills/denon-avr-control/scripts/dlna_push.py scan --root ~/Music
```

### List tracks matching a term

```bash
python3 skills/denon-avr-control/scripts/dlna_push.py list --root ~/Music --query jazz
```

### Push a random local track to the Denon

```bash
python3 skills/denon-avr-control/scripts/dlna_push.py push --root ~/Music --mode random --denon-host <denon-ip>
```

### Push a matching track to the Denon

```bash
python3 skills/denon-avr-control/scripts/dlna_push.py push --root ~/Music --mode match --query "hotel california" --denon-host <denon-ip>
```

### Push an explicit file

```bash
python3 skills/denon-avr-control/scripts/dlna_push.py push --file ~/Music/example.mp3 --denon-host <denon-ip>
```

### Stop playback and shut down the temporary file server

```bash
python3 skills/denon-avr-control/scripts/dlna_push.py stop
```

### Inspect current state

```bash
python3 skills/denon-avr-control/scripts/dlna_push.py status
```

## Windows notes

The script is pure Python and should work on Windows too, but the machine's firewall must allow inbound access to the temporary HTTP port (default `8123`). On Windows, you may need to use a LAN IP explicitly with `--serve-host`.
