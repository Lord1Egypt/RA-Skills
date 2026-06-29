# Import Prompts — copy-paste templates per target tool

After you've generated `my-profile.md` in one AI tool, use these prompts in
the **target** tool to import the profile into its long-term memory.

The general pattern:
1. Open the target tool
2. Paste the prompt below
3. Replace `<paste profile here>` with the contents of your `my-profile.md`
4. Let the target tool save it to its memory file

## Claude Code

```
Please add the following profile to my global CLAUDE.md (~/.claude/CLAUDE.md).
If a profile section already exists, intelligently merge the entries by date —
don't duplicate items, and prefer newer dates when there are conflicts.
Confirm the file path after you're done.

<paste profile here>
```

## OpenClaw

```
Please update USER.md to reflect this profile. Preserve any existing structure
in USER.md and merge new entries. For the "Notes" / "Background" section,
expand it based on the Identity / Profession / Preferences below.

<paste profile here>
```

## Codex CLI

```
Please save the following profile to ~/.codex/instructions.md (create if
missing). If the file exists, append a "## User Profile" section at the end
and merge intelligently — don't duplicate existing entries.

<paste profile here>
```

## Cursor

```
Please format the following profile so I can paste it into Cursor Settings →
General → Rules for AI. Keep it concise — Cursor's box is limited. Prioritize
Instructions and Preferences sections; condense Identity to 1-2 lines.

<paste profile here>
```

(Cursor's "Rules for AI" is a manual paste — the assistant can format but
can't write the setting for you.)

## Cline

```
Please format the following profile so I can paste it into Cline's Custom
Instructions (VSCode Settings → Cline → Custom Instructions). Keep it under
2000 chars. Prioritize Instructions and Preferences.

<paste profile here>
```

## Continue

```
Please update ~/.continue/config.json — find the systemMessage field and
merge this profile into it. Preserve existing systemMessage content if any.
Show me the diff before writing.

<paste profile here>
```

## Aider

```
Please write the following profile to CONVENTIONS.md in the current project,
and update .aider.conf.yml to include CONVENTIONS.md in the `read:` list.

<paste profile here>
```

## ChatGPT (web)

```
I'd like you to remember the following information about me for future
conversations. Please update your memory with each entry below — confirm what
you stored.

<paste profile here>
```

(ChatGPT's memory is vendor-managed; it'll typically save 5-10 high-priority
items to "Memory" automatically. You can review at Settings →
Personalization → Memory.)

## Claude.ai (web)

```
Please review the following profile and tell me which entries would be most
useful for me to add to your Custom Instructions for this project. I'll then
paste the curated list into the Custom Instructions field.

<paste profile here>
```

(For Claude.ai projects: alternatively, save `my-profile.md` as a file and
upload it to Project Knowledge — Claude will read it automatically.)

## Generic LLM (any tool)

```
Below is a standardized user profile in 5 categories: Instructions, Identity,
Profession, Projects, Preferences. Please:

1. Acknowledge each category briefly (one line each)
2. Tell me how you'll incorporate this into your responses going forward
3. List any entries you can't act on (e.g., ones that require external context
   you don't have)

<paste profile here>
```

## Tips

- For tools that have **memory limits** (Cursor / Cline have ~2-4k char
  caps), condense Identity and Projects sections — Instructions and
  Preferences are the highest-leverage
- For tools with **file upload** (Claude.ai Projects, OpenClaw workspace), you
  can upload `my-profile.md` directly without paste
- **Re-export periodically**: regenerate `my-profile.md` from your most-used
  tool every few months to keep your "AI baseline" fresh as your work evolves
