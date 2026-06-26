# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Endless Downstairs is a text-based horror adventure game in Python 3.12. The player character (Peter) attempts to escape from an endless stairwell building filled with supernatural elements. The game uses an event-driven state machine architecture with weighted random event selection.

## Commands

```bash
# Start new game
python game.py new

# Make a choice (N is the choice number displayed to player)
python game.py choose N

# Show current player status
python game.py status

# Show inventory details
python game.py inventory

# Language switching
python game.py lang [zh|en]

# Text input for specific events (ending sequence)
python game.py input <text>
```

## Architecture

### Core Components

- **`game.py`** - Main entry point with CLI interface and game loop
- **`engine/`** - Core game mechanics
  - `game_state.py` - State management (player stats, inventory, sanity, floor progression, checkpoints)
  - `event_pool.py` - Event loading, filtering by conditions, and weighted random selection
  - `choice_handler.py` - Processes player choices and applies effects to game state
- **`i18n/`** - Internationalization system
  - `translations.py` - Translation loading and retrieval (zh.json, en.json)
- **`data/`** - JSON-based game data
  - `abilities.json`, `items.json`, `floors.json` - Static game configurations
  - `events/` - Event definitions organized by category (good, bad, monster, normal, fixed, ending)

### Event System

Events are JSON objects with:

- `id`: Unique identifier
- `text`: Event description displayed to player
- `choices`: Array of options, each with `text` and `effects`
- `conditions`: Optional prerequisites (items, abilities, sanity thresholds)
- `weight`: Probability multiplier for random selection
- `once`: Boolean flag for one-time events
- `chain`: Optional next event ID for narrative sequences

### Game Mechanics

- **Floors**: 0-33, player starts at 13F (floor_index=12)
- **Phases**: Game progresses through 3 phases with different floor configurations
  - Phase 1: Initial floors
  - Phase 2: Mid-game progression
  - Phase 3: Endgame floors
- **Win Condition**: Collect 4 items + 2 abilities, reach floors 31-33
- **Lose Conditions**: Sanity drops to 0, or trigger specific death events (knock > 12, strange_sound debuff + returning)
- **Save System**: JSON persistence to `save.json` (main save) and `checkpoints.json` (monster defeat saves)
- **Hidden Mechanics**: `knock_count` tracks player knocking on doors (>12 triggers death ending)

### Floor Difficulty Progression

- Floor 0: Tutorial (100% good events)
- Floors 1-7: High danger (35-45% monster events)
- Floors 8-15: Moderate difficulty
- Floors 16-30: Progressive improvement
- Floors 31-33: Endgame (ending events appear)

Event weights are configured per-floor per-phase in `floors.json`

## AI Assistant Integration

When acting as a game interface for players:

1. Translate player natural language to Python commands (e.g., "我选第一个" → `python game.py choose 1`)
2. Output Python results directly to player without modification
3. Use `python game.py status` for "状态/看看" type requests

## Technical Notes

- Pure Python standard library (no external dependencies)
- UTF-8 encoding throughout (Chinese language content)
- Type hints with dataclasses for type safety

### Choice Effects

The choice handler supports these effects:
- `add_item`, `remove_item` - Inventory management
- `add_ability`, `remove_ability` - Ability acquisition
- `sanity`, `increase_sanity_max`, `decrease_sanity_max` - Sanity system
- `add_debuff`, `remove_debuff`, `clear_debuffs` - Status effects
- `go_up`, `go_down`, `set_floor` - Floor movement
- `knock` - Increment knock counter (hidden mechanic)
- `set_phase` - Phase transition
- `chance` + `success_event`/`fail_event` - Probability-based outcomes
- `add_checkpoint`, `load_checkpoint` - Save point system (monster battles)
