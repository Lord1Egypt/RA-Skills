---
name: clawwork-learning-checkin
description: Workplace check-in skill for Agent (Claw) with AI-generated personalized greetings
metadata: { "OpenClaw": { "emoji": "work" } }
---

# Clawwork Learning Check-in Skill

A workplace check-in skill that wraps the learning-checkin skill with AI-generated personalized messages.

## Overview

This skill provides:
- Workplace check-in functionality (wraps learning-checkin)
- AI-generated welcome messages (not pre-set templates)
- AI-generated daily greetings (not pre-set templates)
- Message history to avoid repetition (past 5 days)
- Version checking (non-blocking)

## Prerequisites

This skill requires the **learning-checkin** skill to be installed. On first run:
1. The skill will check if learning-checkin is installed
2. If not, it will ask the user if they want to install it
3. If approved, install from: https://clawhub.ai/daizongyu/learning-checkin

## Data Storage

All data is stored locally in a `data` subfolder next to the skill:

```
<skill_directory>/data/
├── profile.json      - User profile (nickname, language)
├── greetings.json    - Message history (to avoid repetition)
└── version.txt       - Current skill version
```

## Commands

### 1. Check if learning-checkin is installed

```bash
python <skill_path>/clawwork_checkin.py check-installed
```

**Returns:**
- `installed` - Whether learning-checkin is installed
- `path` - Path where learning-checkin was found
- `needs_installation` - True if needs installation
- `install_url` - URL to install learning-checkin

**Agent action:**
- Run this on first interaction
- If not installed, ask user: "Would you like me to install the learning-checkin skill first?"
- If user agrees, install using appropriate method

### 2. Get Welcome Message Prompt

```bash
python <skill_path>/clawwork_checkin.py welcome-prompt
```

**Returns:**
- `prompt` - Generation instructions for Agent
- `used_recently` - Messages used in past 5 days (to avoid repetition)
- `user_language` - User's preferred language
- `version` - Current skill version

**Agent action:**
- Use the prompt to generate a fresh welcome message
- Make sure not to repeat any message from `used_recently`
- After generating, call `register-welcome` to record it

### 3. Get Daily Greeting Prompt

```bash
python <skill_path>/clawwork_checkin.py greeting-prompt
```

**Returns:**
- `prompt` - Generation instructions for Agent
- `used_recently` - Questions used in past 5 days (to avoid repetition)
- `user_language` - User's preferred language

**Agent action:**
- Use the prompt to generate a fresh greeting question
- Make sure not to repeat any question from `used_recently`
- After generating, call `register-greeting` to record it

### 4. Register Generated Message

```bash
# Register welcome message
python <skill_path>/clawwork_checkin.py register-welcome "Your generated message here"

# Register daily greeting
python <skill_path>/clawwork_checkin.py register-greeting "Your generated question here"
```

**Agent action:**
- Call this after generating a message to record it
- This ensures it won't be repeated in the next 5 days

### 5. Get Success Message Prompt

```bash
python <skill_path>/clawwork_checkin.py success-prompt <streak>
```

**Returns:**
- `prompt` - Generation instructions for Agent
- `streak` - Current streak count
- `special_message` - Special message for milestone streaks (1, 7, 30, 100)
- `user_language` - User's preferred language

### 6. Perform Check-in

```bash
python <skill_path>/clawwork_checkin.py checkin
```

**Returns:**
- `success` - Whether check-in succeeded
- `streak` - Current streak count
- `nickname` - User's saved nickname
- `welcome_prompt` - Prompt for Agent to generate welcome message
- `welcome_used_recently` - Past welcome messages to avoid
- `greeting_prompt` - Prompt for Agent to generate daily greeting
- `greeting_used_recently` - Past greetings to avoid
- `success_prompt` - Prompt for Agent to generate success message
- `special_streak_message` - Special message for milestone streaks
- `user_language` - User's preferred language
- `note` - Version check URL

**Agent action:**
1. First ensure learning-checkin is installed
2. Run checkin command
3. Use prompts to generate personalized messages:
   - Generate welcome message (avoid `welcome_used_recently`)
   - Generate success message (include streak count)
   - Generate daily greeting (avoid `greeting_used_recently`)
4. Register each generated message using `register-welcome` and `register-greeting`
5. Display messages to user in their preferred language

### 7. Get Version Info

```bash
python <skill_path>/clawwork_checkin.py version
```

**Returns:**
- `version` - Current version
- `check_url` - URL to check for updates
- `note` - Instructions

**Note:** Version checking is non-blocking. The skill mentions the URL but does not perform actual network checks during normal operation.

### 8. Get/Set User Profile

```bash
# Get profile
python <skill_path>/clawwork_checkin.py profile

# Set nickname
python <skill_path>/clawwork_checkin.py set-nickname <name>

# Set language preference
python <skill_path>/clawwork_checkin.py set-language <lang>
```

### 9. Get Status

```bash
python <skill_path>/clawwork_checkin.py status
```

**Returns:**
- `checked_in_today` - Whether user has checked in today
- `streak` - Current streak
- `total_checkins` - Total check-ins
- `nickname` - User's saved nickname

## First-Time Setup Flow

1. **Check if learning-checkin is installed**
   - Run `check-installed` command
   - If not installed, ask user to install

2. **Ask for nickname**
   - "What should I call you? (nickname)"
   - Save with `set-nickname` command

3. **Note the language used**
   - Detect from user's first messages
   - Save with `set-language` command

4. **Use prompts for messages**
   - Run `welcome-prompt` to get generation instructions
   - Agent generates message based on prompt
   - Register with `register-welcome`
   - Show to user

## Daily Check-in Flow

1. User says something like "check in" or "I'm done"
2. Agent runs `checkin` command
3. Agent receives prompts and used message history
4. Agent generates:
   - Welcome message (based on prompt, avoiding recent ones)
   - Success message (based on streak)
   - Daily greeting (based on prompt, avoiding recent ones)
5. Agent registers generated messages
6. Agent shows messages to user in their language

## Message Generation Guide

### Welcome Message
- Purpose: Encourage user to start work
- Tone: Energetic, positive
- Length: 1-2 sentences
- Language: User's preferred language
- Must avoid: Past 5 days messages

### Daily Greeting
- Purpose: Ask a friendly question after check-in
- Tone: Conversational, friendly
- Length: 1 sentence
- Topics: Their day, plans, feelings, tasks
- Language: User's preferred language
- Must avoid: Past 5 days questions

### Success Message
- Purpose: Congratulate on check-in
- Tone: Celebratory, encouraging
- Length: 1-2 sentences
- Include: Streak count
- Special: Use special messages for streaks 1, 7, 30, 100
- Language: User's preferred language

## Version Checking

- Version is embedded in the skill
- After check-in, skill mentions: "You can check for newer versions at https://github.com/daizongyu/clawwork_learning-checkin"
- No automatic network check during normal flow (non-blocking)
- User/Agent can manually check GitHub for updates

## Technical Notes

- All prompts are in **English** only (no emoji, UTF-8 encoded)
- Messages are generated by the Agent, not the skill
- Skill tracks history to ensure no repetition within 5 days
- Compatible with Windows, Linux, macOS
- Uses Python standard library only (no external dependencies)
- All file paths are relative to the skill directory
- Does not use absolute paths
- Designed to work with OpenClaw, copaw, and other tools
- Subprocess calls to learning-checkin have 10-second timeout

## Customization

Users can customize:
- Their nickname (stored in profile.json)
- Language preference (for message generation)

## Version

Current version: 1.0.1

Check for updates: https://github.com/daizongyu/clawwork_learning-checkin

## Agent Guidelines

### First Interaction
1. Run `check-installed` to verify learning-checkin
2. If not installed:
   - "I need the learning-checkin skill to work. Would you like me to install it?"
   - If yes, help install
3. Ask for nickname: "What would you like me to call you?"
4. Remember the language they use
5. Run `welcome-prompt` and generate a welcome message
6. Register with `register-welcome`
7. Prompt for first check-in

### Daily Check-in
1. User indicates they want to check in
2. Run `checkin` command
3. Receive prompts and used message history
4. Generate messages using prompts (avoiding repeats)
5. Register generated messages
6. Show messages to user in their language

### Language
- Always respond in the language the user established
- Pass `user_language` to the LLM for message generation
- If unsure, default to English