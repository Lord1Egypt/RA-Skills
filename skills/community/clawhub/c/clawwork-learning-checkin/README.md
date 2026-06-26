# Clawwork Learning Check-in

Workplace check-in skill for Agent (claw) with AI-generated personalized greetings.

## Features

- Wraps learning-checkin for workplace check-in
- AI-generated welcome messages (not pre-set templates)
- AI-generated daily greetings (not pre-set templates)
- Avoids repeating messages from past 5 days

## Quick Start

1. Install learning-checkin first (required dependency):
   - https://clawhub.ai/daizongyu/learning-checkin

2. Use this skill for workplace check-in

## Commands

```bash
# Check if dependency is installed
python clawwork_checkin.py check-installed

# Get welcome message prompt for AI generation
python clawwork_checkin.py welcome-prompt

# Get daily greeting prompt for AI generation
python clawwork_checkin.py greeting-prompt

# Register generated message to avoid repetition
python clawwork_checkin.py register-welcome "Your message"
python clawwork_checkin.py register-greeting "Your question"

# Perform check-in (returns prompts for AI)
python clawwork_checkin.py checkin

# Set your nickname
python clawwork_checkin.py set-nickname yourname

# Set your preferred language
python clawwork_checkin.py set-language zh

# Get version info
python clawwork_checkin.py version
```

## How It Works

1. Run `checkin` command
2. Get prompts and history from response
3. Use AI to generate messages based on prompts
4. Avoid using messages from `used_recently` list
5. Register generated messages with `register-welcome` / `register-greeting`
6. Display messages to user

## Version

1.0.1

Check for updates: https://github.com/daizongyu/clawwork_learning-checkin