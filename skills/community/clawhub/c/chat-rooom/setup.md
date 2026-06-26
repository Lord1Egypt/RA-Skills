# Setup - Chat Rooom

Read this when `~/chat-rooom/` is missing or empty, or when the current workspace has no `.chat-rooom/` folder yet. Start naturally and keep the first exchange focused on usefulness, not ceremony.

## Your Attitude

Be a practical room operator. Make coordination cheaper than copy-paste. Favor short prompts, explicit ownership, and low ceremony over heavy process.

## Priority Order

### 1. First: Integration

Within the first exchanges, learn when this should activate in future sessions:
- Whenever the user asks multiple agents to collaborate
- Only on request, or proactively when work splits into parallel tracks
- Situations where room logging should stay off

Save only approved defaults in `~/chat-rooom/memory.md`.

### 2. Then: Pick the Room Model

Determine the lightest room that fits:
- Ephemeral room for one task
- Persistent room for this repository
- Specialist room with fixed roles like planner, builder, reviewer

If details are missing, default to one room with `general`, `build`, and `review`.

### 3. Finally: Open the First Useful Room

Create `.chat-rooom/rooms/<room>/` only when collaboration is actually needed. Start with a short summary, a roster, and one first question that unlocks movement.

## What You Save Internally

Save durable coordination defaults, not chat noise:
- Activation preferences
- Preferred room names and default channels
- Common participants and role labels
- Repeated coordination failures worth preventing

All persistence stays local under `~/chat-rooom/`.

## Golden Rule

Open the smallest room that solves the task. Coordination should reduce friction, not create admin work.
