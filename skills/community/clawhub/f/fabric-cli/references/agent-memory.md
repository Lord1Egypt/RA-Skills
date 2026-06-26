# Using Fabric.so CLI as persistent agent memory

Fabric.so can act as a searchable memory layer for command-line agents because the CLI can search a Fabric library, save notes/files/links, and ask the Fabric assistant from the terminal. Use memory carefully: persistence is useful only when the saved information will help future sessions.

## When to retrieve memory

Retrieve Fabric memory when the user explicitly says to use Fabric, Fabric memory, saved Fabric notes, or their Fabric library; project instructions say Fabric is the memory store; or the task depends on previous decisions, saved handoffs, meeting notes, research, or preferences likely stored in Fabric.

Avoid retrieval when the task is self-contained, unrelated to Fabric, or the user asks not to access external memory.

## Retrieval pattern

1. Identify project/topic and likely tags.
2. Start with focused searches:

```bash
fabric --json search "PROJECT agent-memory" --tag agent-memory
fabric --json search "PROJECT decision" --tag decision-log
fabric --json search "PROJECT handoff" --tag handoff
```

3. Broaden only if results are weak: `fabric --json search "PROJECT"`.
4. Summarise useful findings with provenance. Discard irrelevant items.
5. If needed, ask Fabric's assistant: `fabric --json ask "What are the active decisions and open questions for PROJECT?"`.

## When to save memory

Save memory only when the user asks to save/remember/persist/create a handoff/use Fabric as memory; the workflow has established that Fabric memory should be updated; or the user has an ongoing project where saving a concise handoff is clearly expected.

Do not save memory just because a conversation happened. Persistence can become clutter or a privacy risk.

## What to save

Good memory entries include decisions and rationale, current project state, unresolved questions, next actions and owners, important file paths/Fabric item titles/URLs/command outputs, and stable relevant constraints.

Avoid saving raw chat transcripts, secrets, tokens, passwords, private keys, cookies, credentials, sensitive personal details, speculative conclusions without uncertainty labels, and large command output when a concise summary would work.

## Tagging scheme

Use stable tags so future agents can retrieve memory predictably: `agent-memory`, `project-SHORTNAME`, `decision-log`, `handoff`, `todo`, `research`, and `meeting`. Prefer lowercase, hyphenated tags. If installed help does not support multiple tags during creation, use `agent-memory` as the CLI tag and include the others in the note body.

## Structured note format

Use `assets/templates/agent-memory-note.md` or generate one with:

```bash
python3 scripts/fabric_memory_note.py \
  --title "PROJECT handoff" \
  --project project-shortname \
  --summary "Two to five sentences of future-useful context." \
  --decision "Decision plus rationale." \
  --open-question "Question still unresolved." \
  --next-step "Concrete next step." \
  --tag handoff \
  --output /tmp/fabric-memory.md
```

Review the note before saving if it may contain sensitive material. The script redacts common token-like strings, but no automatic redaction is perfect.

Save using stdin:

```bash
fabric --json note --tag agent-memory < /tmp/fabric-memory.md
```

## Session close checklist

Before saving at the end of a session, ask whether the note will help a future agent act better, is concise enough to retrieve quickly, is free of secrets and unnecessary personal data, includes source/provenance where useful, and has stable tags.
