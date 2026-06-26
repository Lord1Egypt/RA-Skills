---
name: denon-avr-control
description: Control a network-connected Denon AVR/AVC receiver over its classic IP control interface (TCP telnet-style commands or the goform HTTP endpoint), and expose local audio libraries through DLNA/UPnP for receiver playback. Use when asked to power the receiver on/off, change volume, mute, switch inputs, query status, send raw Denon commands, or serve user-chosen music directories to a compatible Denon/HEOS receiver.
---

# Denon AVR Control

Use this skill to control a Denon receiver on the local network.

## Quick start

1. Identify the receiver host or IP address.
2. Start with a read/query action before making changes.
3. Use `scripts/denon_avr.py` for normal operations.
4. If a model-specific command is missing, read `references/commands.md` and use `--raw`.

## Default workflow

### Query status

Run:

```bash
python3 skills/denon-avr-control/scripts/denon_avr.py --host <ip-or-hostname> --status
```

### Power

```bash
python3 skills/denon-avr-control/scripts/denon_avr.py --host <ip-or-hostname> --power on
python3 skills/denon-avr-control/scripts/denon_avr.py --host <ip-or-hostname> --power off
```

### Volume

```bash
python3 skills/denon-avr-control/scripts/denon_avr.py --host <ip-or-hostname> --volume 35.5
python3 skills/denon-avr-control/scripts/denon_avr.py --host <ip-or-hostname> --volume-up 3
python3 skills/denon-avr-control/scripts/denon_avr.py --host <ip-or-hostname> --volume-down 2
```

### Inputs

```bash
python3 skills/denon-avr-control/scripts/denon_avr.py --host <ip-or-hostname> --input tv
python3 skills/denon-avr-control/scripts/denon_avr.py --host <ip-or-hostname> --input game
python3 skills/denon-avr-control/scripts/denon_avr.py --host <ip-or-hostname> --input heos
```

### Mute

```bash
python3 skills/denon-avr-control/scripts/denon_avr.py --host <ip-or-hostname> --mute on
python3 skills/denon-avr-control/scripts/denon_avr.py --host <ip-or-hostname> --mute off
```

## Transport choice

Prefer the default TCP transport first:

```bash
python3 skills/denon-avr-control/scripts/denon_avr.py --host <ip-or-hostname> --status
```

If the receiver only responds on the HTTP control endpoint:

```bash
python3 skills/denon-avr-control/scripts/denon_avr.py --host <ip-or-hostname> --transport http --status
```

## Raw commands

Use raw mode for model-specific features or when the canned arguments are not enough:

```bash
python3 skills/denon-avr-control/scripts/denon_avr.py --host <ip-or-hostname> --raw PW? --raw MV? --raw SI?
```

Read `references/commands.md` for the common command families.

## Local computer playback

If the user wants to play local audio files on the computer itself, use `scripts/local_audio_jukebox.py` together with this receiver-control skill.

Read `references/local-playback.md` when the task is to:
- scan a local directory for songs
- play a random song or a short random queue
- play tracks that match a user query
- build a simple playlist from user-provided terms
- stop or inspect the local player state

This workflow plays audio on the local computer, so that machine's system output must already be routed to the receiver if sound should come out of the receiver.

## Experimental DLNA push mode

If the user wants the Denon itself to fetch and play a local file over the LAN, use `scripts/dlna_push.py`.

Read `references/dlna-push.md` when the task is to:
- scan a folder for audio files before choosing one
- push a random local track directly to the Denon renderer
- push a track chosen by user query
- push a specific file path to the Denon
- stop the remote playback and shut down the temporary HTTP server
- support the same approach on Windows and macOS

This mode is more cross-platform than local-output playback because it uses Python + HTTP + UPnP/DLNA. It is still experimental and currently strongest for single-track push.

## Real DLNA media server mode

If ad-hoc URL push is unreliable on a receiver, use `scripts/simple_dlna_server.py` instead.

Read `references/dlna-server.md` when the task is to:
- expose one or more user-chosen music directories as a real discoverable DLNA MediaServer
- let the user decide the music path(s) instead of assuming a fixed folder
- let the Denon browse the library through its Local Music / HEOS path
- support a more Windows-friendly and standards-based setup
- avoid raw one-off URL playback hacks

This mode provides SSDP discovery, a device description, a ContentDirectory service, a ConnectionManager service, and direct HTTP media serving.

Prefer this mode for cross-platform local-library playback.

## Guardrails

- Query first when you do not know current state.
- Send one mutating action at a time unless the user explicitly wants a batch.
- Treat input names and sound modes as model-dependent; if a friendly alias fails, switch to `--raw`.
- If the user did not provide the receiver address, ask for the IP/hostname or discover it only if they explicitly want network scanning.
