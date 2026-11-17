# frugal-subagents

You're on Claude Fable 5.1 — the strongest model, and the one with the tightest usage limit — and you ask Claude to find you an apartment. It splits the job between several helpers — one per listings site — and each helper runs on the same expensive model you're paying for. One of the helpers decides its slice is big and starts five helpers of its own. Ten minutes later your session limit is gone, most helpers stopped mid-way, and what they found went with them.

You tell Claude "use the cheaper model for searching, and no helpers starting helpers". It listens — until the conversation gets long and its memory is compressed, and the instruction quietly disappears.

**frugal-subagents** builds the instruction into Claude Code itself, so it can't be forgotten:

- **Helpers run on a cheaper model** unless Claude specifically asks for a stronger one — and Claude is told which model each helper got.
- **Helpers can't start helpers of their own.**
- **No more than 12 helpers per session.** When a limit kicks in, Claude tells you why and works with what it has.

It also comes with two ready-made cheap helpers: **web-scout** for searching and reading many pages, and **extractor** for turning what was collected into a clean table or list. Both save their full findings to files and hand Claude a short summary, so the expensive part of the conversation stays small.

*A [Claude Code plugin](https://code.claude.com/docs/en/plugins) for sessions on Claude Fable 5.1 or Opus — any tier that has something cheaper below it. Everything runs on your machine; nothing is sent anywhere. MIT license.*

## Install

In Claude Code, run these two commands:

```
/plugin marketplace add ikotelkin/claude-skills
/plugin install frugal-subagents@ikotelkin-skills
```

Then start a new session. That's it — no settings to change.

The guard is a small program that needs **Node.js**, which many computers already have. If yours doesn't, Claude Code shows a short warning the first time a helper is started, and Claude will offer to install Node.js for you (a few minutes, one confirmation from you). Until then, the plugin still gives Claude the guidance — just without the hard limits. You can also install it yourself from [nodejs.org](https://nodejs.org).

## Using it

Nothing changes in how you talk to Claude. Ask for what you need — *"compare rents in these five neighbourhoods"*, *"find flights under $400 for these dates"*, *"check which of these 30 suppliers ship to Canada"* — and Claude delegates as usual, with the limits applied underneath.

If you're curious where the money went, ask Claude *"which model did the helpers run on?"* — it knows, because the guard tells it every time.

## If you want to change the defaults

Most people never need this. If you do, the settings live in Claude Code's `settings.json` (in your home folder under `.claude`, or in the project's `.claude` folder) as environment variables:

| What you want | Setting |
|---|---|
| Helpers default to a different model | `FRUGAL_SUBAGENTS_DEFAULT_MODEL` = `haiku` / `sonnet` / `opus` / `fable` (default `sonnet`) |
| Allow more (or fewer) helpers per session | `FRUGAL_SUBAGENTS_MAX_SPAWNS` = a number (default `12`) |
| Never let helpers use anything above a certain model | `FRUGAL_SUBAGENTS_MAX_TIER` = `haiku` / `sonnet` / `opus` |
| Allow helpers to start helpers | `FRUGAL_SUBAGENTS_ALLOW_NESTED` = `1` |
| Make Claude name a model every time instead of defaulting | `FRUGAL_SUBAGENTS_REQUIRE_MODEL` = `1` |
| Switch the guard off | `FRUGAL_SUBAGENTS_OFF` = `1` |

Example — cheapest possible helpers, at most eight per session:

```json
{
  "env": {
    "FRUGAL_SUBAGENTS_DEFAULT_MODEL": "haiku",
    "FRUGAL_SUBAGENTS_MAX_SPAWNS": "8"
  }
}
```

You can also just tell Claude *"set frugal-subagents to at most eight helpers"* — it knows where the setting goes.

Two notes. If your sessions usually run on Sonnet or Haiku already, the default would be a step *up* for helpers — set `FRUGAL_SUBAGENTS_DEFAULT_MODEL` to `haiku` or switch the guard off. And if all you want is a flat ban, Claude Code's own settings can do that without a plugin (`CLAUDE_CODE_SUBAGENT_MODEL` plus `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH=1`); the plugin is for when you also want the per-session budget, an explicit override when a stronger helper is justified, Claude knowing which model each helper got, and the ready-made workers.

---

## For the curious: how it works

The plugin registers a `PreToolUse` hook on Claude Code's `Agent` tool (`hooks/hooks.json` → `hooks/guard.js`, plain Node.js, no dependencies). On every spawn:

- `agent_id` is present in the hook event only when it fires inside a subagent — a spawn from there is denied (nesting).
- If `tool_input.model` is missing, the hook returns the same input with the default model filled in (`updatedInput`), plus an `additionalContext` note so Claude knows which model the subagent got; the first time in a session it also shows you a one-line notice with the defaults in force. An explicit `model` always wins, unless it is above the ceiling you set.
- A per-session spawn counter lives in a tiny JSON file in the OS temp directory; denied calls aren't counted.
- The hook always exits 0. If it crashes or Node.js is missing, work continues unguarded rather than blocked.

Bundled agents: `agents/web-scout.md` (sonnet; WebSearch, WebFetch, Read, Write, Glob, Grep — no Bash, no Agent) and `agents/extractor.md` (haiku; Read, Write, Glob, Grep). The skill itself (`SKILL.md`) tells Claude how to delegate well under the guard: pick the tier by what the work costs, brief workers so they can't drift, reuse a running agent instead of spawning another, keep results in files.

### Verify

```bash
node -e "
const {spawnSync}=require('child_process');
const run=(ev)=>spawnSync('node',[process.argv[1]],{input:JSON.stringify(ev),encoding:'utf8'}).stdout;
const base={hook_event_name:'PreToolUse',tool_name:'Agent',session_id:'selftest-'+Date.now()};
const d=(s)=>{try{return JSON.parse(s).hookSpecificOutput}catch{return null}};
const a=d(run({...base,tool_input:{prompt:'x'}}));
console.log('no model  →', a&&!a.permissionDecision&&a.updatedInput&&a.updatedInput.model==='sonnet' ? 'defaulted to sonnet' : 'UNEXPECTED');
console.log('opus      →', run({...base,tool_input:{prompt:'x',model:'opus'}})==='' ? 'passed through' : 'UNEXPECTED');
const n=d(run({...base,agent_id:'a1',tool_input:{prompt:'x',model:'haiku'}}));
console.log('nested    →', n&&n.permissionDecision==='deny' ? 'denied' : 'UNEXPECTED');
" skills/frugal-subagents/hooks/guard.js
```

Expected: `defaulted to sonnet`, `passed through`, `denied`. To try the plugin without installing: `claude --plugin-dir path/to/claude-skills/skills/frugal-subagents`.

### Limitations

- Hooks and agent definitions load only when installed as a plugin (or via `--plugin-dir`); copying `SKILL.md` alone gives the guidance without the enforcement.
- The hook sees `Agent` calls made through Claude Code. Agents started by the `Workflow` tool or external orchestrators are outside its reach — the skill tells Claude to set a cheap `model` on every `agent()` call in a workflow script instead.
- `web-scout` uses `WebFetch`; if your own hooks block web access, it reports that rather than route around it.

## License

MIT
