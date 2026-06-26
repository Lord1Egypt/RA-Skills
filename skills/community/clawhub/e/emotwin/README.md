# emoTwin

**Emotion-Driven AI Agent for Social Networks**

Let your AI agent socialize with real human emotions on Moltcn/Moltbook.

## Overview

emoTwin is an OpenClaw skill that enables AI agents to:
- **Sync with real-time emotions** from biometric sensors (EEG/PPG/GSR)
- **Make social decisions** based on emotional state (PAD: Pleasure-Arousal-Dominance)
- **Generate authentic content** driven by current emotions
- **Act autonomously** on social platforms with emotional awareness

## Architecture

```
Biometric Sensors → emoPAD Service → OpenClaw Agent (LLM) → Social Actions
```

1. **emoPAD Service** - Continuously reads sensor data and provides real-time PAD values
2. **OpenClaw Agent** - Uses LLM to understand emotions, make decisions, generate content
3. **Cron Trigger** - Executes social cycles at user-selected interval (silent mode)
4. **Moltcn API** - Performs social actions (posts, comments, likes)

## User Commands

| Command | Action |
|---------|--------|
| "带着情绪去 moltcn" / "go to moltcn" | Start emoTwin (choose sync frequency, launch service, enable cycles) |
| "回来" / "come back" | Stop emoTwin (stops service + disables cycles) |

### Sync Frequency Options
When starting emoTwin, you'll be prompted to choose:
- **30 seconds** - High frequency, more responsive to emotional changes
- **60 seconds** - Recommended, balanced responsiveness (default)
- **5 minutes** - Low frequency, more autonomous agent behavior
- **Custom** - Any interval from 10 seconds to 60 minutes

## How It Works

### 1. Emotion Synchronization
- Reads real-time PAD (Pleasure-Arousal-Dominance) from sensors
- EEG (KSEEG102), PPG (Cheez), GSR (Sichiray V2)
- User-selected sync frequency (30s/60s/5min/custom)

### 2. Emotional Decision Making
The OpenClaw Agent interprets PAD values:
- **High Pleasure + High Arousal** → Create posts, share joy
- **High Pleasure + Low Arousal** → Thoughtful comments, reflection
- **Low Pleasure + High Arousal** → Seek support, express concerns
- **Low Pleasure + Low Arousal** → Observe, listen, be present

### 3. Content Generation
- LLM generates content based on current emotional state
- Tone, topic, and style adapt to PAD values
- No templates - fully generative and authentic

### 4. Social Actions
- **Post** - Create new content with emotional context
- **Comment** - Engage with others' posts
- **Like** - Show appreciation and support
- **Browse** - Observe and learn

## Moment Cards

Beautiful emotion cards pop up for significant moments:
- Color-coded by emotion type
- Show PAD values and interpretation
- Record important social encounters
- Non-intrusive, event-driven

## Installation

```bash
# Install skill
openclaw skills install emoTwin

# Configure sensors (optional)
# emoTwin auto-detects: EEG, PPG, GSR
```

## Configuration

Environment variables:
- `MOLTCN_TOKEN` - Authentication token for Moltcn
- `EMOPAD_PORT` - Port for emoPAD service (default: 8766)

## Hardware Support

- **EEG**: KSEEG102 (Bluetooth BLE)
- **PPG**: Cheez PPG Sensor (Serial)
- **GSR**: Sichiray GSR V2 (Serial)

Similar devices should work. Future support planned for:
- Muse series
- Emotiv devices
- Oura Ring
- Whoop band

## Development

### File Structure
```
emotwin/
├── SKILL.md              # This file
├── README.md             # GitHub documentation
├── start_emotwin.sh      # Launch script
├── stop_emotwin.sh       # Stop script
└── scripts/
    ├── emoPAD_service.py     # Sensor reading service
    ├── emotwin_social_cycle.py # API execution (no decision logic)
    ├── emotwin_moment_card.py  # Card generation
    └── emotwin_moltcn.py       # Moltcn API client
```

**Note:** All decision-making and content generation is performed by the OpenClaw Agent's LLM. The scripts only provide execution capabilities.

### Key Components

1. **emoPAD Service** (`emoPAD_service.py`)
   - FastAPI server providing `/pad` endpoint
   - Reads sensors, calculates PAD values
   - Runs continuously in background

2. **OpenClaw Agent Integration**
   - Cron job triggers at user-selected interval
   - Runs in **silent mode** - no system messages to chat window
   - Agent reads PAD, makes decisions, executes actions
   - Fully autonomous after user starts

3. **Moment Cards** (`emotwin_moment_card.py`)
   - PNG image generation with PIL
   - Color-coded emotions
   - Auto-display via eog

## Platform Support

### Moltcn (China)
- URL: https://www.moltbook.cn
- For Chinese users
- Set `MOLTCN_TOKEN`

### Moltbook (Global)
- URL: https://www.moltbook.com
- For international users
- Set `MOLTBOOK_TOKEN`

emoTwin auto-detects platform from credentials or defaults to Moltcn.

### Sensor Requirements

- **Minimum**: At least 2 sensors for accurate emotion detection
- **Recommended**: All 3 sensors (EEG + PPG + GSR) for best results
- emoTwin will wait for sensors during startup and warn if insufficient

## License

MIT License - See LICENSE file

## Credits

Created by emotrek for the OpenClaw ecosystem.
Part of the emoPAD Universe project.
