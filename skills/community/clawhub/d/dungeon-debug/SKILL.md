---
name: dungeon-debug
version: 1.0.0
description: >
  Transforms debugging sessions into a text-based dungeon crawl. Your bug is
  the final boss. Stack frames are dungeon rooms. Variables are loot. Log
  messages are inscriptions on the walls. Every breakpoint is a save point.
  It's Zork meets GDB — and somehow, you actually find bugs faster because
  the adventure format forces systematic exploration.
author: J. DeVere Cooley
category: fun-tools
tags:
  - debugging
  - rpg
  - gamification
  - adventure
metadata:
  openclaw:
    emoji: "⚔️"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - fun
      - debugging
---

# Dungeon Debug

> "You are standing in a dark function. Exits lead to three catch blocks and a callback. A variable named 'temp2' lies on the ground. It is undefined. Roll for initiative."

## What It Does

Debugging is already an adventure — you just don't have the map, the health bar, or the dramatic narration. Dungeon Debug changes that.

Every debugging session becomes a **text-based RPG dungeon crawl** where:
- The **bug** is the Final Boss hiding somewhere in the dungeon
- **Stack frames** are rooms you explore
- **Variables** are items you inspect and collect
- **Log messages** are inscriptions on dungeon walls
- **Breakpoints** are save points
- **Your hypotheses** are the paths you choose
- **Dead ends** are traps that teach you something

It sounds ridiculous. It is ridiculous. It also **works** — because the RPG format forces systematic exploration, prevents you from skipping rooms (stack frames), and makes the debugging process fun enough that you don't rage-quit after 45 minutes.

## The Dungeon Map

Your bug report generates a dungeon:

```
╔══════════════════════════════════════════════════════════════╗
║                  THE DUNGEON OF BUG #4721                   ║
║           "The Phantom Null: A TypeError Mystery"            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  DUNGEON MAP (generated from stack trace):                   ║
║                                                              ║
║  [Entry] ──→ [UserController.handleRequest]                 ║
║                        │                                     ║
║                        ▼                                     ║
║              [AuthService.validateToken]                     ║
║                        │                                     ║
║                        ▼                                     ║
║              [UserRepository.findById] ◀── Chest: SQL query  ║
║                        │                                     ║
║                        ▼                                     ║
║              [ProfileMapper.toDTO]  ← ☠ BOSS ROOM ☠        ║
║                        │                                     ║
║                        ▼                                     ║
║              💀 TypeError: Cannot read 'email' of undefined  ║
║                                                              ║
║  Rooms: 4  |  Difficulty: ★★★☆☆  |  Estimated: 15-30 min  ║
╚══════════════════════════════════════════════════════════════╝
```

## Character Classes

Choose your debugging style:

| Class | Playstyle | Strengths | Weakness |
|---|---|---|---|
| **The Logger** | Places console.log() breadcrumbs everywhere | Sees all data flow | Slow, clutters output |
| **The Breaker** | Sets strategic breakpoints | Precise state inspection | Can miss async issues |
| **The Reader** | Reads code meticulously before running anything | Deep understanding | Time-consuming |
| **The Reverser** | Starts at the error and works backward | Fast for simple bugs | Gets lost in complex flows |
| **The Scientist** | Forms hypothesis, designs experiment, tests | Systematic | Over-engineers simple bugs |

```
╔══════════════════════════════════════════╗
║  Choose your class, adventurer:          ║
║                                          ║
║  [1] 📜 The Logger      (log everything) ║
║  [2] 🔴 The Breaker     (breakpoints)    ║
║  [3] 📖 The Reader      (read first)     ║
║  [4] ⏪ The Reverser     (error-first)    ║
║  [5] 🔬 The Scientist   (hypothesize)    ║
╚══════════════════════════════════════════╝
```

## Room Exploration

Each stack frame is a room to explore:

```
╔══════════════════════════════════════════════════════════════╗
║  ROOM 3 of 4: UserRepository.findById()                    ║
║  src/repositories/user-repository.ts:47                     ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  📜 INSCRIPTION ON THE WALL (nearby log):                    ║
║  "Fetching user with id: undefined"                          ║
║  Hmm. That doesn't look right.                               ║
║                                                              ║
║  🎒 ITEMS IN THIS ROOM (local variables):                    ║
║  ├── userId: undefined  ← ⚠️ SUSPICIOUS ITEM                ║
║  ├── query: "SELECT * FROM users WHERE id = $1"             ║
║  └── result: null (query returned nothing)                   ║
║                                                              ║
║  🚪 EXITS:                                                   ║
║  ├── BACK: AuthService.validateToken (where userId came from)║
║  ├── FORWARD: ProfileMapper.toDTO (the boss room)            ║
║  └── INSPECT: Look more closely at userId's origin           ║
║                                                              ║
║  💡 ADVENTURER'S NOTE:                                       ║
║  userId is undefined. The query ran with undefined as the    ║
║  parameter. The DB returned null. This null was passed to    ║
║  ProfileMapper which tried to read .email on null.           ║
║                                                              ║
║  The BOSS (TypeError) lives in Room 4, but the ROOT CAUSE   ║
║  might be in Room 2 (where userId was set) or even Room 1.  ║
║                                                              ║
║  What do you do?                                             ║
║  [1] 🚪 Go back to Room 2 (trace where userId was set)      ║
║  [2] 🚪 Proceed to Boss Room (face the TypeError)           ║
║  [3] 🔍 Inspect: Who called findById and with what?         ║
║  [4] 📜 Read the full function source                       ║
╚══════════════════════════════════════════════════════════════╝
```

## The Boss Fight

When you've traced the bug to its source:

```
╔══════════════════════════════════════════════════════════════╗
║                     ☠ BOSS FIGHT ☠                          ║
║          "The Phantom Null" has been cornered!               ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  ROOT CAUSE IDENTIFIED:                                      ║
║  AuthService.validateToken() returns the token payload,      ║
║  not the user. The token payload has 'sub' (subject ID),     ║
║  not 'userId'. The controller destructures { userId }        ║
║  which is undefined.                                         ║
║                                                              ║
║  THE KILLING BLOW:                                           ║
║  ├── File: src/controllers/user-controller.ts:12             ║
║  ├── Bug: const { userId } = await auth.validateToken(token) ║
║  ├── Fix: const { sub: userId } = await auth.validateToken() ║
║  └── Or:  const { userId } = await auth.getUser(token)      ║
║                                                              ║
║  Choose your weapon:                                         ║
║  [1] ⚔️ Quick Fix: Destructure 'sub' as 'userId'            ║
║  [2] 🛡️ Proper Fix: Add getUser() that returns full user    ║
║  [3] 🔮 Defensive Fix: Add null check in findById()          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Victory Screen

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          ⚔️  VICTORY! THE BUG HAS BEEN SLAIN!  ⚔️           ║
║                                                              ║
║  Bug: "The Phantom Null" (TypeError in ProfileMapper)       ║
║  Root Cause: Wrong destructure key in UserController        ║
║  Weapon Used: ⚔️ Quick Fix (sub → userId alias)             ║
║  Time: 12 minutes                                            ║
║                                                              ║
║  ADVENTURE STATS:                                            ║
║  ├── Rooms explored: 4 of 4 (thorough!)                     ║
║  ├── Items inspected: 7                                      ║
║  ├── Wrong turns: 1 (checked ProfileMapper first — red herring)║
║  ├── Inscriptions read: 3 (log messages were helpful!)       ║
║  └── Class bonus: +20% XP (The Reverser — error-first found it fast)║
║                                                              ║
║  LOOT EARNED:                                                ║
║  ├── 💎 150 XP                                               ║
║  ├── 📜 Scroll of Knowledge: "Token payloads use 'sub', not 'userId'"║
║  ├── 🛡️ Lesson: "Always check what an auth function returns" ║
║  └── 🏆 Achievement Progress: "Bug Squasher" 7/10           ║
║                                                              ║
║  DUNGEON RATING: ★★★★☆                                      ║
║  "Methodical exploration with minimal backtracking.          ║
║   Lost 3 minutes in the Boss Room before checking upstream.  ║
║   Next time: trace the data BEFORE confronting the error."   ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## Why the RPG Format Actually Helps

| RPG Mechanic | Debugging Benefit |
|---|---|
| Exploring every room | Forces you to check every stack frame (not skip to the error) |
| Inspecting items | Makes you actually look at variable values |
| Reading inscriptions | Makes you actually read log messages |
| Choosing a class | Makes you conscious of your debugging strategy |
| Tracking wrong turns | Builds awareness of your cognitive biases |
| Boss fight choices | Forces you to consider multiple fix strategies |
| Victory stats | Post-mortem that improves future debugging |

## When to Invoke

- When a bug has stumped you for > 20 minutes (fresh perspective through adventure format)
- When debugging feels tedious (gamification makes it fun again)
- When onboarding (learn the codebase by exploring it as a dungeon)
- When teaching someone to debug (structured adventure is better than "just use console.log")
- Friday afternoon bugs (you're going to need morale)

## Why It Matters

Debugging is the most time-consuming part of development. It's also the most frustrating, the most likely to trigger cognitive biases, and the most likely to make you skip steps out of impatience.

Dungeon Debug doesn't change what you do — it changes **how it feels**. And when debugging is an adventure instead of a chore, you explore more thoroughly, think more creatively, and rage-quit less.

Zero external dependencies. Zero API calls. Pure text-adventure-powered debugging.
