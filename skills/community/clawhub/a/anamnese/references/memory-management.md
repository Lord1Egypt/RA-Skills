# Memory Management Reference

Detailed guidance for storing and retrieving facts, moments, and notes in Anamnese.

## Facts (type="fact")

Stable truths that persist for months or years. Use `save_memory` with type="fact".

**Save when the user mentions:**
- Identity: name, location, job, employer, birthday
- Preferences: "I prefer...", "I always...", "I never..."
- Relationships: "My partner is...", "My team includes..."
- Health: allergies, conditions, medications
- Skills and habits: "I know Rust", "I run every morning"

## Moments (type="moment")

Time-bound events that happened at a specific point. Always include `occurred_at`.

**Save when the user mentions:**
- Decisions: "We decided to...", "I chose..."
- Achievements: "I finished...", "I got promoted..."
- Experiences: "I visited...", "Today I..."
- Health events: "I started taking...", "My doctor said..."
- Milestones: "We launched...", "I passed the exam..."

## Notes

Learned knowledge, procedures, and guidelines. Use `save_note`.

**Save when the user:**
- Teaches or explains something: "Here's how our deploy works..."
- Corrects you: "Actually, I prefer...", "Always use X here"
- Shares technical details: schemas, APIs, architecture
- Describes workflows or processes

Notes support full content -- use `search_notes` for summaries, `get_note` for full content.

### Self-Learning Notes

You have persistent memory across conversations via `save_note` with `scope: "ai_client"`. Use this to become better at helping this user over time. **Save as you go** — don't wait until the conversation ends.

**What to save:**
- Preferences discovered: "User wants brief answers, no preamble"
- Corrections received: "I suggested npm but user uses pnpm exclusively"
- Interaction patterns: "User gets frustrated when I ask too many questions — just do the task"
- What works: "Batching small tasks together works well for this user"
- What doesn't: "Suggesting refactors unprompted annoys this user"

Use `search_notes` with `scope: "ai_client"` to find your notes from previous sessions.

## Best Practices

1. **Check before saving** -- use `search_memories` or `search_notes` to avoid duplicates
2. **Update over create** -- if a memory or note exists on the topic, use `update_memory` or `update_note`
3. **Tag appropriately** -- free-form tags (any string, max 5 per item, max 50 chars each)
4. **Be selective** -- only save information useful in future sessions
5. **Prefer moments for events** -- when in doubt between fact and moment, choose moment (timestamped)
