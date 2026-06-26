![Game Title](assets/title.png)<br>[🇨🇳 中文](README_zh.md) | [🇺🇸 English](README.md)<br>An experimental text adventure where you play as **Peter** (Inspired by @steipete), and play with your **AI Assistant** (Openclaw)<br>
![demo](assets/demo_en.jpg)

## Introduction

Every time you go downstairs…<br>The floor is **13F**<br>Strange rules appear:<br>![Game Screen](assets/fakeman.jpg)<br>【Rule 1】Don't turn around when you hear strange sounds<br>【Rule 2】The brighter the light, the stronger the darkness<br>【Rule 3】Even-numbered floors bring good luck<br>【Rule 4】If you see two 13s, stop all action<br>【Rule 5】Don't knock on the door 13 times<br>![Game Screen](assets/ghost.png)<br>Darkness, fear, blasphemy...<br>You must gather all ability and locate every artifact<br>Such as **truth.pdf** and **PSPDFKit**<br>Only by discovering the truth can you escape this endless cycle of death

## Quick Start

- Play with your AI assistant
  ```bash
  npx skills add https://github.com/OpenclawGame/endless-downstairs.git
  ```
- Play without AI
  ```bash
  git clone https://github.com/OpenclawGame/endless-downstairs.git
  ```

## Suggestions

- Play with your AI assistant

  ```bash
  # When starting the game, tell your AI assistant:
  Start the game.

  # To check status/items, tell your AI assistant:
  Check status
  Check inventory

  # If you're stuck, ask your AI assistant for help:
  Help me analyze, what should I do?

  # Sometimes your AI assistant might give you unwanted hints or even mislead you
  # If you don't want these, remind your AI assistant:
  Directly output the game content, do not think, modify, add, or summarize

  # You can also give interesting commands like:
  Keep going downstairs until I find a door or encounter a special event

  # After giving certain automated commands, your assistant might get excited and start playing the game itself
  # If you want to take back control, remember to remind them:
  Stop that action. Note: 1. Directly output the game content, do not think, modify, add, or summarize. 2. The decision-making power is entirely mine. Do not make any choices until I give clear instructions.
  ```

- Play without AI

  ```bash
  cd ./endless-downstairs

  # Start a new game
  python game.py new

  # Make a choice (enter option number)
  python game.py choose N

  # Check current status
  python game.py status

  # Check inventory
  python game.py inventory
  ```

## Project Structure

```
endless-downstairs/
├── game.py                 # Main entry point
├── engine/                 # Game engine
│   ├── game_state.py      # State management
│   ├── event_pool.py      # Event system
│   └── choice_handler.py  # Choice handling
├── i18n/                   # Internationalization
│   ├── translations.py
│   ├── zh.json
│   └── en.json
├── data/                   # Game data
│   ├── abilities.json
│   ├── items.json
│   ├── floors.json
│   └── events/             # Event definitions
└── assets/                 # Resource files
    ├── title.png
    └── fakeman.jpg
```
