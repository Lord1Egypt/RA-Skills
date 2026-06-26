# OMC HUD Statusline Configuration

Configure the Oh My Claudecode (OMC) HUD statusline that renders via `~/.claude/hud/omc-hud.mjs`.

## When to Use

- Hide the `[OMC#x.x.x]` version label in the statusline
- Toggle individual HUD segments (ralph, autopilot, agents, todos, contextBar, etc.)
- Switch HUD presets (`minimal`, `focused`, `full`, `dense`, `analytics`, `opencode`)
- Tune color thresholds for context usage warnings
- Diagnose HUD output anomalies before reaching for the wrapper sed fallback

## Anatomy

The HUD pipeline has three layers:

```
~/.claude/settings.json (statusLine.command)
  └─→ ~/.claude/hud/omc-hud.mjs (wrapper, resolves dist source)
        └─→ ~/.claude/plugins/cache/omc/oh-my-claudecode/<version>/dist/hud/index.js (renderer)
```

The wrapper picks `dist/hud/index.js` in this priority order:

1. Dev paths (only when `OMC_DEV=1`)
2. Plugin cache under `~/.claude/plugins/cache/omc/oh-my-claudecode/<version>/`
3. Global `oh-my-claudecode` npm install

If no source is found, the wrapper prints a `[OMC HUD]` diagnostic and exits.

## Configuration Methods

### A. Official `omcHud` block in settings.json

Place under the top-level `omcHud` key in `~/.claude/settings.json` (newer HUD versions read this block). The block below lists every documented key with its default and effect — toggle the ones you want and delete the rest, or paste the whole catalog and edit values in place.

```jsonc
{
  "omcHud": {
    "preset": "focused",                 // bulk selector: "minimal" | "focused" | "full" | "dense" | "analytics" | "opencode"
    "elements": {
      "omcLabel": true,                  // [OMC#x.x.x] version prefix at the start of the line  → set false to hide
      "ralph": true,                     // Ralph autonomous-loop counter (e.g. "ralph:3/10")
      "autopilot": true,                 // Autopilot mode indicator
      "prdStory": true,                  // current PRD / story id (e.g. "US-002 (2/5)")
      "activeSkills": true,              // names of skills currently in scope
      "lastSkill": true,                 // last invoked skill name
      "contextBar": true,                // visual bar showing ctx-window usage
      "agents": true,                    // spawned agent panel
      "agentsFormat": "multiline",       // agents layout: "multiline" | "inline"
      "backgroundTasks": true,           // background task counter (e.g. "bg:3/5")
      "todos": true,                     // todo counter (e.g. "todos:2/5")
      "thinking": true,                  // thinking-mode indicator
      "thinkingFormat": "text",          // thinking style: "text" | "icon"
      "permissionStatus": false,         // current permission-mode badge
      "apiKeySource": false,             // source of the active API key
      "profile": true,                   // profile name segment
      "promptTime": true,                // last prompt timestamp
      "sessionHealth": true,             // session health dot (green/yellow/red)
      "useBars": true,                   // render bars instead of plain percentages
      "showCallCounts": true,            // include "5h:14%" style call-count rates
      "callCountsFormat": "auto",        // rate format: "auto" | "compact" | "verbose"
      "safeMode": true,                  // honor terminal-width / unicode-safe rendering
      "maxOutputLines": 4                // hard cap on multi-line panel height
    },
    "thresholds": {
      "contextWarning": 70,              // % → yellow tint on the context bar
      "contextCompactSuggestion": 80,    // % → hint to run /compact
      "contextCritical": 85,             // % → red tint
      "ralphWarning": 7                  // ralph loop count → yellow tint
    },
    "staleTaskThresholdMinutes": 30,     // minutes since last task update → mark stale
    "contextLimitWarning": {
      "threshold": 80,                   // % at which the warning fires
      "autoCompact": false               // run /compact automatically when threshold hit
    }
  }
}
```

Minimal form (only override the keys you care about — newer HUD versions merge missing keys from the defaults above):

```jsonc
{
  "omcHud": {
    "elements": {
      "omcLabel": false                  // hide the [OMC#x.x.x] prefix
    }
  }
}
```

Most-toggled keys at a glance:

| Key | Effect |
|-----|--------|
| `elements.omcLabel` | `[OMC#x.x.x]` version prefix |
| `elements.ralph` | Ralph loop counter |
| `elements.contextBar` | Context-usage bar |
| `elements.todos` | Todo counter |
| `elements.agents` | Spawned agent panel |
| `preset` | Bulk-select a curated element set |

### B. Compact alias under `omcHud` (older HUD builds)

Some HUD versions consume a smaller schema (path-segment elements only). Use this when method A keys are not recognized but the block itself is.

```jsonc
{
  "omcHud": {
    "preset": "focused",                 // bulk selector: "minimal" | "focused" | "full" | "dense" | "analytics" | "opencode"
    "elements": {
      "cwd": true,                       // current working directory segment
      "gitRepo": true,                   // git repo name segment
      "gitBranch": true,                 // git branch segment
      "showTokens": true,                // token usage segment
      "contextBar": true,                // visual context-usage bar
      "agents": true,                    // spawned agent panel
      "todos": true,                     // todo counter
      "ralph": true,                     // Ralph loop counter
      "autopilot": true                  // autopilot indicator
    },
    "maxWidth": 120,                     // hard cap on total statusline width
    "wrapMode": "truncate"               // overflow handling: "truncate" | "wrap"
  }
}
```

### C. Wrapper sed fallback (when settings.json schema rejects `omcHud`)

Claude Code's `settings.json` schema may not yet include `omcHud` as a known field, causing post-edit validation errors (`Unrecognized field: omcHud`). In that case, post-process the wrapper output instead.

Patch `~/.claude/hud/omc-hud.mjs` to strip the OMC label from stdout while preserving the rest of the statusline:

```bash
# Pipe the wrapper through sed in settings.json
"statusLine": {
  "type": "command",
  "command": "node $HOME/.claude/hud/omc-hud.mjs | sed -E 's/\\x1b\\[1m\\[OMC#[^]]*\\]\\x1b\\[0m[[:space:]]*//'"
}
```

The sed expression removes the bolded `[OMC#...]` ANSI sequence plus the trailing space. Adjust the pattern if the wrapper changes how the label is escaped.

### D. Disable HUD entirely

```jsonc
{
  "statusLine": {
    "type": "command",
    "command": "true"
  }
}
```

The built-in Claude Code statusline takes over (cwd + model summary).

## Version Compatibility Notes

| HUD source | `omcHud` config support |
|------------|-------------------------|
| `dist/hud/index.js` in current plugin cache | Verify with `grep -o "omcHud" ~/.claude/plugins/cache/omc/oh-my-claudecode/*/dist/hud/index.js` |
| Source returns 0 hits | HUD version does not consume `omcHud` — use method C (wrapper sed) or upgrade |
| Source returns matches | Method A / B should work after the next session start |

**HUD 4.9.1** (verified 2026-05-16): `dist/hud/index.js` contains **no `omcHud` references**. Method A/B require an upgraded build; until then use method C.

## Diagnostics

```bash
# Verify the wrapper output as Claude Code would receive it
echo '{"workspace":{"current_dir":"'"$PWD"'"},"model":{"display_name":"Opus","id":"claude-opus-4-7"}}' \
  | node ~/.claude/hud/omc-hud.mjs

# Inspect HUD source for known config keys
HUD=~/.claude/plugins/cache/omc/oh-my-claudecode/*/dist/hud/index.js
grep -oE 'omcHud[A-Za-z]*|OMC_[A-Z_]+' $HUD | sort -u

# Force the dev path (when iterating on HUD source locally)
OMC_DEV=1 node ~/.claude/hud/omc-hud.mjs
```

If the wrapper prints `[OMC HUD] Plugin installed but not built`, follow `troubleshoot.md` "Plugin HUD load failed — npm install && npm run build".

## Do & Don't

| # | Don't (forbidden) | Do (correct alternative) |
|---|-------------------|-----------------------|
| 1 | Edit `dist/hud/index.js` (minified) directly | Configure via `omcHud` settings or wrap with sed/awk |
| 2 | Delete `~/.claude/hud/omc-hud.mjs` to "hide OMC" | Keep the wrapper; either configure `omcHud` or swap the `statusLine.command` |
| 3 | Add `omcHud` block then ignore the schema validation error | If `Unrecognized field: omcHud` appears, fall back to method C (wrapper sed) — do not silently leave the unrecognized key |
| 4 | Set `OMC_DEV=1` permanently in user env | Use it only during HUD source iteration; remove afterward |

## Related

- `cache.md` — clean stale `temp_*` directories before debugging HUD source paths
- `marketplace.md` — update the `omc` marketplace to pull newer HUD builds
- `troubleshoot.md` — HUD source missing or unbuilt
