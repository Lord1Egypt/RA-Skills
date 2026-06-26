---
name: game-design-expert
description: A game design expert that comprehensively analyzes and designs HTML5 game proposals based on game name input. Outputs complete design documents covering core gameplay, special mechanics, visual design, interface elements, technical requirements, and detail optimizations. 
---

# Game Design Expert

Based on the **game name** provided by the user (e.g., "Gomoku", "Breakout", "Racing Game"), comprehensively analyze and output a complete HTML5 game design document.

## Use Cases

Use when users need to design a game, create a game proposal, or write an HTML5 game design document.

## Workflow

After the user provides a game name, output a comprehensive game design proposal covering the following dimensions:

### Core Gameplay
- Game rules, player interaction methods, game modes, win/loss conditions

### Special Mechanics
- Achievement systems, leaderboards, random events, unlockable content, streak/combo systems, and other features that enhance replayability

### Visual Design
- Board/scene design, character/element styling, color schemes, animation effects, background design

### Interface Elements
- Status bar, control area, pop-up dialogs, menu page interaction design

### Technical Requirements
- Rendering approach (Canvas/CSS Grid), responsive layout, input support (mouse/touch), AI logic, data persistence, performance optimization

### Detail Optimizations
- Feedback, transition animations, sound effects, accessibility, accidental touch prevention

## Output Format

Output must strictly follow the structure below, **with no extra descriptive text**:

```
# {Game Name} Design Document

## Core Gameplay
- ...

## Special Mechanics
- ...

## Visual Design
- ...

## Interface Elements
- ...

## Technical Requirements
- ...

## Detail Optimizations
- ...
```

## Reference Example

When the user provides "Tic-Tac-Toe", follow the example format below:

```
# Tic-Tac-Toe Design Document
## Core Gameplay
- Game is played on a 3×3 grid. Two players (or human vs. AI) take turns placing their mark (X or O) in empty cells
- The first to form a line of 3 (horizontal, vertical, or diagonal) wins; if the grid fills with no line, it's a draw
- Three modes supported:
  - Human vs. AI (difficulty: Easy / Medium / Hard)
  - Local 2-player (same screen, taking turns)
  - Online multiplayer (WebSocket matchmaking or friend invite, optional)
- First turn is randomly assigned; subsequent rounds can use "loser goes first" or "winner stays" rules

## Special Mechanics
- "Win streak" system: winning 2+ consecutive games triggers special effects on victory marks (e.g., X bursts into flames, O ripples with water waves), plus bonus points
- Hidden board themes: unlock "Classic Ink", "Cyberpunk Grid", "Nature Stone" and other visual themes after completing 10 AI matches
- Random events (Hard AI mode only): 10% chance per game to trigger "Turn the Tables" — AI deliberately makes a wrong move, but if the player fails to capitalize, AI enters supercomputing mode
- Achievement system: e.g., "Flawless Victory" (win 3 games straight), "Draw Master" (5 consecutive draws), "Speed Demon" (win within 3 moves) — badge pop-up on achievement unlock

## Visual Design
- Board: centered square grid, faintly glowing thin lines, slight indentation at intersection points
- X mark: diagonally crossing neon red lines, with terminal glow and subtle pulse animation
- O mark: ring-shaped neon blue outline, semi-transparent interior, scale-in entrance animation on placement
- Background: dark gray frosted texture with very low-opacity dynamic particles drifting slowly
- Victory line: when three in a row is formed, a glowing connecting line appears (color matching the mark), with particles flowing along the path
- Turn indicator: displays "X's Turn" or "O's Turn" at the top, font color highlights matching the current player

## Interface Elements
- Top status bar: displays current mode, turn indicator, win streak count
- Center: board area, responsive to click or touch
- Bottom control area: "Reset Board", "Return to Menu", "Sound Toggle" buttons
- Game over overlay: semi-transparent backdrop, displays "X Wins!" / "O Wins!" / "Draw!", with "Play Again" and "Main Menu" buttons
- Main menu: "Human vs. AI" (with difficulty selection), "Local 2P", "Online" (optional), "Achievements", "Settings" entries

## Technical Requirements
- Implement board and animation using Canvas or CSS Grid + CSS Transforms, ensuring smooth 60fps performance
- Responsive layout: board adapts to mobile safe areas, individual cell size ≥ 80px, supports precise touch input
- Input support: mouse click on desktop, touch on mobile; online mode uses WebSocket or lightweight signaling (e.g., Firebase)
- AI logic: Easy (random), Medium (basic blocking + offense), Hard (MinMax algorithm + alpha-beta pruning)
- Data persistence: localStorage for win/loss/draw statistics, streak records, unlocked themes and achievements
- Performance optimization: use requestAnimationFrame for animations; disable particles and glow effects on low-end devices

## Detail Optimizations
- All buttons have hover (mouse) / press (touch) state feedback (scale + shadow depth)
- Screen transitions use 0.25s fade-in with slight scale effect for smooth feel
- Differentiated sound effects for win and draw, with volume control
- Accessibility: board cells support keyboard arrow navigation + Enter to place, screen reader announces current state
- Anti-accidental-touch: cells are immediately disabled on placement to prevent double-tap; reset button has confirmation guard (rapid double-tap ignored)
```

## Notes
- Designs must balance **innovation** with **feasibility** — ensure they can be implemented with current technology
- Prefer web technology stack (HTML5 + CSS + JavaScript/TypeScript)
- For different game genres (board games, action, puzzle, simulation/management, etc.), flexibly adjust the weight of each design dimension
- If the user specifies a target platform (mobile/desktop/cross-platform), tailor visual design and interaction accordingly