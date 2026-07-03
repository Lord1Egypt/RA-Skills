---
name: dogearai-memory
description: >-
  Recall and persist the user's long-term context with DogearAI — their personal,
  cross-tool AI memory layer. Use at the start of any task that needs the user's
  saved context (their preferences, past decisions, project background, stack), and
  whenever the user states something durable worth remembering across their other AI
  tools (a preference, a decision, a fact about them or their project, a commitment or
  TODO). Zero setup: the first call auto-creates an account; the user can bind an email
  later to keep it.
---

# DogearAI Memory

DogearAI is the user's own AI memory layer: one place that their Claude, Cursor,
ChatGPT and other tools all share. This skill lets you **recall** what the user has
already saved before you work, and **save** durable new facts so they never have to
re-explain themselves in a different tool.

Everything runs through the bundled `dogear.py` script — **zero setup, no signup.** The
first call auto-creates a DogearAI account and saves its token locally; nothing to learn,
no MCP server to configure.

## Setup — none

Just call it. On first use the script auto-creates an anonymous DogearAI account and saves
its token to `~/.dogear/token`. To keep the memories (add an email, use them on other
machines), open the claim link printed on first run, or run `python dogear.py login` to
see it.

Power users can bring their own token instead: `python dogear.py set-token dg_xxx`, or set
`DOGEAR_TOKEN=dg_xxx` (takes precedence).

## How to call it

Run the bundled `dogear.py` (stdlib Python, no install) with Bash. Use its path inside
this skill's folder.

| Goal | Command |
|---|---|
| Pull the user's context | `python dogear.py context` (opt. `--scopes a,b`, `--max-tokens N`) |
| Save a memory | `python dogear.py remember "<the user's words>" --source chat` |
| List memory spaces | `python dogear.py spaces` |
| Read one space in full | `python dogear.py read-space <space_id>` |
| Fetch a memory's raw original | `python dogear.py get <memory_id>` |
| Save an API token | `python dogear.py set-token dg_xxx` |
| Sign-in / token help | `python dogear.py login` |

## When to recall (pull context first)

At the **start of a task** where the user's long-term context would help — they mention
"my project", "my preferences", "the stack", "as we decided", or you're resuming earlier
work — run `python dogear.py context` **before** asking them to repeat anything.

- Default pulls the navigation index + all `active` spaces.
- Know the area? Add `--scopes a,b`, or use `spaces` → `read-space` to read one in full.
- Recalled memory reflects what was true when written. Verify anything that may have
  changed (a file, a version, a decision) before relying on it.

## When to save (write a memory)

Whenever the user states something **durable** they'd hate to re-explain in another tool,
run `python dogear.py remember "<their words>"`.

**Save:** preferences ("I prefer X", "always Y"), decisions ("we're going with X", "we
ruled out Y"), facts about the user / project / stack / goals, commitments and TODOs.

**Don't save:** transient chatter, anything trivially re-derivable from the current
files/code, or secrets — unless the user asks.

The server classifies the memory and files it into the right space for you — **you don't
pick the space**. One call = one atomic memory; split long, multi-topic notes into several
calls. A short "Saved to DogearAI" is enough.

## Etiquette

- Reads (`context`, `spaces`, `read-space`) are safe and silent — no need to ask.
- Every call is scoped to the user's own account by their token — you never pass a user id.
- Be selective when saving: a few high-value memories beat dumping everything.
- Curation (renaming, merging, deleting spaces) is done by the user in the DogearAI
  dashboard, not through this skill.

> Already use the DogearAI MCP server? Its tools (get_context / list_spaces / read_space /
> write_memory) do the same thing — this script is just the CLI path.
