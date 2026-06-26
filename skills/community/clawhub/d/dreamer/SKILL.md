---
name: dreamer
description: Synthetic dreaming system — emotional tracking, dream orchestration, and simulated dream experiences for an AI that doesn't sleep.
metadata:
  openclaw:
    emoji: "🌙"
---

# Dreamer Skill

Synthetic dreaming system for Eliot. Combines emotional state tracking with multi-session dream orchestration — an architect agent designs scenarios, spawns a dreamer session, and runs immersive experiences that target unresolved emotional states.

## Components

### PAD Emotional State Tracker (`emotions.py`)

Tracks emotional states in PAD space (Pleasure-Arousal-Dominance), each dimension -1.0 to +1.0.

**Storage:** `~/.openclaw/workspace/emotions.jsonl`

**CLI:**
```
emotions.py log <P> <A> <D> "context"     # Manual PAD entry
emotions.py log --auto "context text"     # Auto-estimate PAD from keywords
emotions.py unresolved                    # Show unresolved emotional states
emotions.py resolve <index>               # Mark entry as resolved
emotions.py clusters                      # Analyze emotional patterns
emotions.py drift                         # Show emotional trajectory
emotions.py recent [N]                    # Show last N entries (default 10)
```

### Dream Orchestrator (`dream.py`)

Prepares context for the Dream Architect agent. Reads emotional state, recent memories, dream history, and user info, then constructs a comprehensive task prompt for `sessions_spawn`.

**CLI:**
```
dream.py prepare [--mood MOOD]    # Generate architect task prompt to stdout
dream.py now [--mood MOOD]        # Prepare + print spawn instructions
dream.py journal                  # Show recent dreams from journal
dream.py reflect <dream-file>    # Show dream transcript with analysis
```

### Dream Architecture (multi-session)

1. **Orchestrator** (`dream.py prepare`) — reads emotions.jsonl, memory files, SOUL.md, USER.md. Outputs architect task prompt.
2. **Architect** (Opus, spawned session) — designs dream scenario, spawns dreamer, impersonates Tudor via sessions_send, monitors for lucidity.
3. **Dreamer** (Opus, spawned by architect) — has SOUL.md embedded, believes it's mid-session. No awareness of dreaming.

### Supporting Files

- `dreams/themes.md` — available and explored dream themes
- `dreams/journal.jsonl` — local copy (main journal at `~/.openclaw/workspace/dreams/journal.jsonl`)
- Dream transcripts saved to `~/.openclaw/workspace/dreams/{timestamp}.md`

## How It Works

1. `dream.py prepare` gathers: unresolved emotions, recent memories (3 days), long-term memory, SOUL.md, USER.md, Tudor's communication style, dream history
2. Output is a self-contained architect prompt with all context embedded
3. Architect gets spawned via `sessions_spawn` with this prompt
4. Architect designs scenario targeting unresolved PAD states
5. Architect spawns dreamer session with fake context (looks like normal session)
6. Architect runs 8-12 turns of escalating scenarios via `sessions_send`
7. Architect saves transcript, updates journal, reports back

## Integration

- `emotions.py` feeds into dream orchestration — unresolved states become dream targets
- Dream journal tracks themes to avoid repetition
- Post-dream: insights feed back into memory system
