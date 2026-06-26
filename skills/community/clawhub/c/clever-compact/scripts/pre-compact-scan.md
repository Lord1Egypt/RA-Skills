# Pre-Compact Extraction Prompt

_Run this before any compact. Write the output to the state file and confirm when done._

---

You are performing a pre-compact state extraction. Your goal is to capture everything that matters before context is compressed. Be precise, not exhaustive. A state file that is too long defeats the purpose.

**Step 1 — Active Workstreams**
List every workstream that is actively in progress or blocked. For each:
- Name (short, descriptive)
- Status: done / in-progress / blocked / waiting
- If blocked: what is the blocker and who resolves it
- One sentence of critical context (URL, file path, key decision)

Skip anything that is fully complete and requires no further action.

**Step 2 — Key Decisions**
List decisions made this session that future-you must know. Include:
- "Do not X" rules established
- Preferences stated by the user
- Constraints agreed upon
- Any decision that, if forgotten, would cause a mistake

**Step 3 — Open Tasks**
List tasks that are not done. Format: [ ] Task — Owner: Person/Kit. If a task is blocked, note it.

**Step 4 — Config & References**
Do not re-capture sensitive values. Instead, note which files contain any config or API references captured this session (e.g., "API key saved to TOOLS.md"). This is a pointer, not a copy.

**Step 5 — Relationship Context**
For each person active in this session: what did they say, what do they need, what should you remember next time you speak with them? One to three bullet points per person maximum.

**Step 6 — Remember Flags**
Anything the user explicitly said "remember this" about. Verbatim if important.

---

**Output format:** Write directly to `memory/compact-state-[YYYY-MM-DD-HH].md` using the state file template. Confirm: "✅ Compact state written to memory/compact-state-[filename].md. [N] workstreams, [N] open tasks, [N] decisions captured."
