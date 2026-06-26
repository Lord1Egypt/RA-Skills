# Local audio playback on the computer

Use this workflow when the user wants to play local music files but the receiver itself is only being used as the sound output target.

## Constraint

The Denon control protocol does not upload arbitrary local files to the AVR for playback.

Instead:

1. Route the computer's audio output to the receiver (AirPlay, HDMI, USB audio, etc.).
2. Use `scripts/local_audio_jukebox.py` to scan and pick tracks.
3. Use `scripts/denon_avr.py` to set receiver power/input/volume if needed.

## Typical commands

### Scan a music directory

```bash
python3 skills/denon-avr-control/scripts/local_audio_jukebox.py scan --root ~/Music
```

### List matches

```bash
python3 skills/denon-avr-control/scripts/local_audio_jukebox.py list --root ~/Music --query jazz
```

### Play one random track

```bash
python3 skills/denon-avr-control/scripts/local_audio_jukebox.py play --root ~/Music --mode random
```

### Play three random tracks

```bash
python3 skills/denon-avr-control/scripts/local_audio_jukebox.py play --root ~/Music --mode random --count 3
```

### Play a specific track by fuzzy substring

```bash
python3 skills/denon-avr-control/scripts/local_audio_jukebox.py play --root ~/Music --mode match --query "hotel california"
```

### Build a simple ordered playlist from comma-separated search terms

```bash
python3 skills/denon-avr-control/scripts/local_audio_jukebox.py play --root ~/Music --mode playlist --query "intro,theme,finale"
```

### Check/stop playback

```bash
python3 skills/denon-avr-control/scripts/local_audio_jukebox.py status
python3 skills/denon-avr-control/scripts/local_audio_jukebox.py stop
```

## Player choice

- Prefer `afplay` on macOS for simple local playback.
- Use `ffplay` if a format is unsupported by `afplay`.
