---
name: ambient-audio
description: |
  Play scientifically-proven ambient sounds for focus, relaxation, meditation, and sleep. Perfect for programmers, office workers, students, and anyone needing concentration or rest.
  Use when user wants: white noise, pink noise, brown noise, rain sounds, singing bowl, binaural beats, brain wave tones (alpha/beta/gamma/theta).
  No copyright issues - all audio is algorithmically generated using ffmpeg.
---

# Ambient Audio - Ambient Sound Player

Play white noise, pink noise, brown noise, brain wave tones, and more for deep focus, relaxation, or sleep. Runs on Linux servers with audio output.

> All audio files are pre-generated (10-second loops) for instant playback. No copyright concerns - sounds are algorithmically generated.

## Quick Start

```bash
# Play white noise (default, 10 seconds)
bash scripts/play.sh white

# Play specific type
bash scripts/play.sh pink
bash scripts/play.sh brown
bash scripts/play.sh theta

# With duration
bash scripts/play.sh white -d 30     # 30 seconds
bash scripts/play.sh pink -d 60       # 1 minute

# With volume control (0.1 - 2.0)
bash scripts/play.sh white -v 0.5     # 50% volume

# Stop playing
bash scripts/play.sh stop

# List all available modes
bash scripts/play.sh --list
```

## Available Audio Types

### 🎯 Focus (Concentration)
| Mode | Best For | Description |
|------|----------|-------------|
| `white` | Deep work, coding | Classic white noise - eliminates ambient distractions |
| `alpha` | Light focus | Alpha waves (8-14Hz) - relaxed alertness |
| `beta` | Active thinking | Beta waves (14-30Hz) - mental clarity |
| `gamma` | Peak focus | Gamma waves (30Hz+) - cognitive enhancement |

### 😌 Relax (Stress Relief)
| Mode | Best For | Description |
|------|----------|-------------|
| `pink` | Gentle background | Softer than white, easier on ears |
| `rain` | Reading, working | Simulated rain ambience |
| `nature` | Breaks | Filtered natural-style ambience |

### 😴 Sleep (Rest)
| Mode | Best For | Description |
|------|----------|-------------|
| `brown` | Deep sleep | Deep, rumbling noise - best for sleeping |
| `delta` | Sleep onset | Delta waves (0.5-4Hz) - helps fall asleep |

### 🧘 Meditation
| Mode | Best For | Description |
|------|----------|-------------|
| `theta` | Meditation | Theta waves (4-8Hz) - deep relaxation |
| `binaural` | Focus/relax | 10Hz binaural beats - brain wave entrainment |
| `bowl` | Calming | Singing bowl - instant calm |

## Usage Examples

### Voice Commands (via AI Assistant)

- "Play white noise" → Starts white noise
- "I need to focus for coding" → Plays white/alpha
- "Can't sleep, play something" → Plays brown noise
- "Let me meditate" → Plays theta waves
- "Stop" → Stops playback

### Custom Duration

```bash
# 5 minutes (300 seconds)
bash scripts/play.sh white -d 300

# 1 hour
bash scripts/play.sh brown -d 3600
```

### Volume Control

```bash
# Half volume
bash scripts/play.sh white -v 0.5

# Quiet (25%)
bash scripts/play.sh pink -v 0.25

# Louder
bash scripts/play.sh brown -v 1.5
```

## How It Works

1. **Pre-generated Audio**: All sounds are 10-second loops stored in `samples/` directory
2. **Instant Playback**: ffplay loops the file seamlessly
3. **Duration Control**: Calculates loop count: `duration / 10`
4. **Volume Control**: Uses ffplay's `-af volume=` filter

## File Structure

```
focus-audio/
├── SKILL.md              # This file
├── scripts/
│   └── play.sh          # Main player script
└── samples/             # Pre-generated audio files (10s loops)
    ├── white_10s.mp3    # White noise - focus/work
    ├── pink_10s.mp3     # Pink noise - relaxed focus
    ├── brown_10s.mp3    # Brown noise - deep sleep
    ├── theta_10s.mp3    # Theta waves - meditation
    ├── rain_10s.mp3     # Rain sound - relaxation
    ├── alpha_10s.mp3    # Alpha waves - light focus
    ├── beta_10s.mp3    # Beta waves - active thinking
    ├── gamma_10s.mp3    # Gamma waves - peak focus
    ├── bowl_10s.mp3    # Singing bowl - calming/meditation
    └── binaural_10s.mp3 # Binaural beats - brain wave entrainment
```

## Requirements

- **ffmpeg**: For audio playback
  ```bash
  sudo apt-get install ffmpeg
  ```
- **Audio output**: Speakers or headphones connected to the server

## Troubleshooting

### No sound plays
- Check if audio device is connected: `aplay -l`
- Check if ffplay is installed: `which ffplay`
- Verify audio file exists: `ls samples/`

### Audio too loud/quiet
- Adjust volume: `bash scripts/play.sh white -v 0.3`

### Want to add more sounds
- Generate new 10-second loop:
  ```bash
  ffmpeg -y -f lavfi -i "anoisesrc=d=10:c=pink:a=0.35" -c:a libmp3lame -b:a 64k -t 10 newname_10s.mp3
  ```
- Place in `samples/` directory

## Technical Notes

- **Audio Format**: MP3, 48kHz, mono, 64kbps
- **Loop Duration**: 10 seconds (seamless loop)
- **Volume Range**: 0.1 - 2.0 (default 1.0)
- **Max Duration**: No hard limit (limited by system resources)

## Security

- Input validation on volume and duration parameters
- File paths are hardcoded (no user input for paths)
- No external network calls
- No sensitive data access

---

*Focus Audio - Improve concentration, reduce stress, sleep better.*