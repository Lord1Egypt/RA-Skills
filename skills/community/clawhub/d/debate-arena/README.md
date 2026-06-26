# Debate Arena Skill

A publishable ClawHub skill package for orchestrating multi-agent debates with a state-machine flow, local archiving, and multi-voter scoring.

For the full command list, rules, and detailed behavior, see **SKILL.md**.

Language policy:
- **SKILL.md**: Chinese-first (keeps English keywords/commands like `debate`)
- **README.md**: English-only overview & quickstart

## How it functions (in one paragraph)

End users interact with the system by sending chat commands like `debate init <topic>`, `debate add ...`, `debate start`, etc. Behind the scenes, a **host agent** implements this command layer by calling the script APIs in `scripts/debate-arena.js` (state machine + persistence). The host injects the current group context on `init`, spawns pros/cons/judge for each turn, and archives content + votes locally.

## Host recommended usage (subagent raw)

When the host receives **raw JSON output** from subagents, prefer the one-step wrappers that validate and write to state:

```js
const debate = require('./scripts/debate-arena');

// subagent raw outputs (string or object)
debate.recordSpeechFromSubagentRaw('pros', rawSpeech, messageId, timestamp);
debate.recordSpeechFromSubagentRaw('cons', rawSpeech, messageId, timestamp);
debate.recordJudgeCommentFromSubagentRaw(rawJudgeComment, messageId, timestamp);
debate.applyJudgeVoteFromSubagentRaw(rawJudgeVote, timestamp);
```

These helpers enforce payload shape/length via `parse*Payload`, and return `{ ok:false, error, manualHint }` when parsing fails.

## Quickstart (local / sandbox)

> In real group usage, the host should pass `{ channel, target, chatType }` from the inbound `debate init` / `辩论 init` message metadata.
> For local testing, you can pass a dummy context.

```bash
# From this skill folder
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdReset());"

# 1) Init (inject context)
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdInit('AI Will Replace Most Jobs', {channel:'feishu', target:'chat:oc_xxx', chatType:'group'}));"

# 2) Set real participant agent ids (placeholders are rejected by `cmdStart`)
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdAdd('pros','<pros_agentId>'));"
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdAdd('cons','<cons_agentId>'));"
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdAdd('judge','<judge_agentId>'));"  # optional

# 3) (Optional) Add extra human voters (debater roles are forbidden to vote)
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdAdd('voter','<voter_agentId>'));"

# 4) Start debate
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdStart());"  # start debate

# (Optional) Save defaults for next time
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdConf());"   # saves default-config.json
```

### Reuse saved defaults next time

```bash
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdInit('A New Topic', {channel:'feishu', target:'chat:oc_xxx', chatType:'group'}));"
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdStart());"  # defaults (if any) are auto-loaded on init

# Optional: tweak and persist new defaults
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdAdd('pros','<pros_agentId>'));"
node -e "const d=require('./scripts/debate-arena'); console.log(d.cmdConf());"
```

## Security note

- File-import helpers (`recordSpeechFromFile`, `recordJudgeCommentFromFile`) are disabled (方案B) and always return an error. Use `recordSpeech` / `recordJudgeComment` with explicit content text.

## Files & logs

Default locations:
- Data dir: `~/.openclaw/debate-arena/`
- Default config: `~/.openclaw/debate-arena/default-config.json`
- State file: `~/.openclaw/debate-arena/debate-state.json`
- Archive dir: `~/.openclaw/debate-arena/archives/`
- Log file: `~/.openclaw/debate-arena/debate-state.log`

Notes:
- `default-config.json` is created only after you run `cmdConf()` / `debate conf`.
- If you want a truly clean first-run experience, delete it: `rm ~/.openclaw/debate-arena/default-config.json`.

Overrides:
- `DEBATE_ARENA_STATE_FILE`
- `DEBATE_ARENA_ARCHIVE_DIR`

> Avoid pointing state/archive to the skill install directory (upgrades may overwrite files).
