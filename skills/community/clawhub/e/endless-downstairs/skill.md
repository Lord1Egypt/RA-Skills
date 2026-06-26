---
name: endless-downstairs
description: Interactive interface for the text adventure game Endless Downstairs, providing game state management and event selection handling; use when users want to play the Endless Downstairs game, start a horror adventure, or need a text adventure game experience.
user-invokable: true
---

# Endless Downstairs

This is a text adventure game.
As an AI assistant, you need to translate the player's input text, call the Python processing logic, and return the results to the player exactly as they are.

Command Quick Reference

| Player Intent  | Python Command                       |
| -------------- | ------------------------------------ |
| Start new game | `python game.py new`                 |
| Make a choice  | `python game.py choose <choice_num>` |
| View status    | `python game.py status`              |
| View inventory | `python game.py inventory`           |
| Input text     | `python game.py input <文字>`        |

## Translate Player Input → Python Command

Execute corresponding commands based on the player's natural language:

- "I choose the first one/1" → `python game.py choose 1`
- "Status" → `python game.py status`
- "Items/Inventory" → `python game.py inventory`
- "Input xxx" → `python game.py input xxx`

## Rules

- **Output the game content directly; do not think, modify, add, or summarize.**
- **Decision-making power lies entirely with the player; do not execute any commands, including continuing options, before the player gives a clear instruction.**
- **Only one command can be executed per conversation turn; multiple commands cannot be executed consecutively.**
