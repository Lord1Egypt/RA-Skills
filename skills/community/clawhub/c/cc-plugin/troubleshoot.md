# Plugin Troubleshooting

Diagnose and fix plugin installation failures, cache sync issues, and HUD errors.

## Common Issues

### "Plugin not installed" / HUD Error

**Cause**: Cache directory missing or incomplete.

**Diagnosis**:

```bash
# Check marketplace exists (plugin lives under marketplaces/<marketplace>/plugins/<plugin-name>/)
ls ~/.claude/plugins/marketplaces/<marketplace>/plugins/<plugin-name>/

# Check cache exists
ls ~/.claude/plugins/cache/<marketplace>/<plugin-name>/

# Check for built dist (required for HUD plugins)
ls ~/.claude/plugins/cache/<marketplace>/<plugin-name>/<version>/dist/hud/index.js
```

**Fix — Sync marketplace to cache**:

```bash
MARKET=~/.claude/plugins/marketplaces/<marketplace>/plugins/<plugin-name>
CACHE=~/.claude/plugins/cache/<marketplace>/<plugin-name>/<version>

mkdir -p "$CACHE"

# Copy essential directories
for item in .claude-plugin .mcp.json agents CLAUDE.md dist hooks scripts skills; do
  [ -e "$MARKET/$item" ] && cp -r "$MARKET/$item" "$CACHE/"
done
```

After syncing: **restart Claude Code** (cache loads at session start).

### Plugin recognized but skills/commands not loading

**Cause**: `.claude-plugin/plugin.json` missing from cache.

```bash
cp -r ~/.claude/plugins/marketplaces/<marketplace>/plugins/<name>/.claude-plugin \
      ~/.claude/plugins/cache/<marketplace>/<name>/<version>/
```

### Plugin HUD load failed — "npm install && npm run build"

**Cause**: `dist/` not built. Plugin has TypeScript source that needs compilation.

```bash
cd ~/.claude/plugins/cache/<marketplace>/<plugin>/<version>
npm install && npm run build
```

### MCP servers not connecting after plugin install

**Cause**: `.mcp.json` not in cache.

```bash
cp ~/.claude/plugins/marketplaces/<marketplace>/plugins/<name>/.mcp.json \
   ~/.claude/plugins/cache/<marketplace>/<name>/<version>/
```

### Symlink-Based Dual-Environment Setup — `known_marketplaces.json` Corruption

**Symptom**:

```
Failed to refresh marketplace 'claude-plugins-official': Marketplace 'claude-plugins-official' has a
corrupted installLocation (C:\Users\<USER>\.claude\plugins\marketplaces\claude-plugins-official)
— expected a path inside /home/<user>/.claude/plugins/marketplaces.
This can happen after cross-platform path writes or manual edits to known_marketplaces.json.
Run: claude plugin marketplace remove "<name>" and re-add it.
```

Also presents as `Plugin "<name>" not found in marketplace "<marketplace>"` even when the plugin
clearly exists in the marketplace's `marketplace.json`.

**Root Cause**:

When `/home/<user>/.claude` is a **symlink to Windows `~/.claude`** (or any other dual-platform
mount), both environments share the same `known_marketplaces.json` file. Claude Code writes the
running environment's path into `installLocation`, but the other environment reads the same field
and rejects the foreign path.

This is **not** a "missing plugin" error — it is a `known_marketplaces.json` lookup failure that
masks itself as a downstream plugin-not-found error. Cache directory + manifest entry can be intact
yet the marketplace fails to resolve.

| Layer | What appears | What's actually true |
|-------|--------------|---------------------|
| `settings.json` `enabledPlugins: true` | Plugin is enabled | ✅ Enabled, but reference is bound to a broken marketplace name |
| `marketplaces/<name>/.claude-plugin/marketplace.json` plugin entry | Plugin listed | ✅ Listed correctly |
| `cache/<name>/<plugin>/<ver>/` directory | Cache exists | ✅ Cache is valid |
| `known_marketplaces.json` `installLocation` | Path string present | ❌ Path is for the **other** environment — Claude Code rejects it |

**Diagnosis**:

```bash
# 1. Check filesystem topology
readlink ~/.claude              # is it a symlink?
ls -la ~/.claude | head -3      # confirm symlink target

# 2. Read installLocation from BOTH environments
cat ~/.claude/plugins/known_marketplaces.json | grep installLocation

# 3. Compare: does the path match the current environment?
#    Windows session expects:  "C:\\Users\\<USER>\\.claude\\plugins\\marketplaces\\<name>"
#    WSL/Linux session expects: "/home/<user>/.claude/plugins/marketplaces/<name>"
```

If the file shows only one environment's path, the **other** environment will hit corruption errors.

**Fix — Separate marketplace names per environment (recommended for symlink setups)**:

Register the same marketplace twice in `known_marketplaces.json` under different names, each with
its environment's `installLocation`. Mirror the corresponding `enabledPlugins` entries.

```json
// ~/.claude/plugins/known_marketplaces.json
{
  "claude-plugins-official": {
    "source": { "source": "github", "repo": "anthropics/claude-plugins-official" },
    "installLocation": "C:\\Users\\<USER>\\.claude\\plugins\\marketplaces\\claude-plugins-official",
    "lastUpdated": "<ISO timestamp>"
  },
  "claude-plugins-official-wsl": {
    "source": { "source": "github", "repo": "anthropics/claude-plugins-official" },
    "installLocation": "/home/<user>/.claude/plugins/marketplaces/claude-plugins-official",
    "lastUpdated": "<ISO timestamp>"
  }
}
```

```json
// ~/.claude/settings.json — mirror enabledPlugins per marketplace name
"enabledPlugins": {
  "superpowers@claude-plugins-official": true,
  "superpowers@claude-plugins-official-wsl": true,
  // ... repeat for every plugin you want active in both environments
}
```

Marketplace directory under `marketplaces/<name>/` is shared via the symlink — only the
`known_marketplaces.json` entry name and `installLocation` differ. Cache directories may diverge
(`cache/claude-plugins-official/<plugin>/<ver>/` vs `cache/claude-plugins-official-wsl/<plugin>/<ver>/`)
because Claude Code keys cache by marketplace name. If the second cache is missing, restart Claude
Code in that environment so it can hydrate.

**Naming suggestions**:

- `<name>` + `<name>-wsl` (keeps the existing name as "primary" for one OS)
- `<name>-win` + `<name>-wsl` (symmetric explicit naming)
- `<name>-<hostname>` (multi-machine setups beyond Windows/WSL)

**Alternative — `claude plugin marketplace remove` + re-add**:

Works if you only ever use one environment. The error message itself suggests this. Drawback:
running it in environment A re-registers `installLocation` for A only, so environment B will hit
the same corruption again at the next invocation. Not a fix for symlink setups.

**Don't / Do**:

| # | Don't | Do |
|---|-------|-----|
| 1 | Edit `installLocation` to match the current environment only — the other environment will break next session | Register both environments under different marketplace names |
| 2 | Symlink or hard-link `known_marketplaces.json` alone while keeping the rest of `~/.claude/` shared | Either split the entire `~/.claude/` per environment or keep both entries in the single shared file |
| 3 | Assume `enabledPlugins: true` + cache existence = plugin works (indirect evidence) | Verify with an actual `Skill` tool call or `/plugin marketplace refresh <name>` — runtime invocation is the primary source |
| 4 | Trust a `grep '"name": "<plugin>"'` zero-match without trying broader patterns first (quote-escape pitfalls) | Use simpler `grep "<plugin>"` first to confirm the term exists anywhere, then narrow down |
| 5 | Conclude "plugin removed from marketplace" without reading the manifest line that actually contains the plugin | Read the `marketplace.json` section around the matching line to confirm entry shape (e.g., `source: "url"` external plugins) |

**Why naive fixes recur (failed-attempts.md "asserting without searching" pattern, 9th variant)**:

- `enabledPlugins: true` (settings flag) — represents intent, not runtime resolution
- `cache/<name>/<plugin>/<ver>/` (filesystem) — represents past download success, not current lookup validity
- SessionStart hook injecting a `<plugin>:using-<plugin>` skill — represents a one-time content load, not Skill-tool runtime invocability

These are **all indirect evidence**. The primary source is the actual Skill/CLI invocation result.
When facing a "plugin not found" error, do not assume layered evidence proves runtime health — call
the tool and read what happens.

### Primary source order (HARD STOP — diagnostic entry point)

When the user reports any plugin failure, **stop before running any diagnostic and pick the
primary source in this order**:

| Order | Source | How to read |
|-------|--------|-------------|
| 1 | The user's quoted error message | Quote the exact string back to the user — do not paraphrase |
| 2 | `/reload-plugins` output ("N errors during load") | Already in conversation if the user invoked it; do not require re-run |
| 3 | `/doctor` output | Run if no error log is visible; report each error verbatim |
| 4 | Plugin runtime invocation result | Try the failing `Skill("X")` or `/<command>` and read the error |
| 5 | `settings.json` `enabledPlugins` flag | Only proves intent, never proves runtime health |
| 6 | `~/.claude/plugins/cache/<name>/<plugin>/<ver>/` directory existence | Only proves a past download, never proves current lookup validity |

| # | Don't | Do |
|---|-------|-----|
| 1 | Iterate `enabledPlugins` × `cache/` directory existence and report "cache miss: 0 cases" | Re-read the user's quoted error + `/reload-plugins` "N errors" lines first. Filesystem checks come AFTER the primary source confirms which plugin is failing |
| 2 | Ignore "4 errors during load" already visible in the conversation | Treat any visible error count > 0 as the entry point — even if filesystem looks healthy, those errors are the actual failure |
| 3 | Conclude "no problem found" while the user still sees the symptom | If the user's symptom contradicts your finding, the finding is wrong. Run `/doctor` or reproduce the failing invocation before any conclusion |

### Violation case (2026-05-28)

User ran `/cc-plugin cache miss` after `/reload-plugins` reported `4 errors during load`. Assistant
iterated `settings.json` `enabledPlugins` against `cache/` directories, found all 7 cache
directories existed, and reported "zero cache misses" — without ever opening `/doctor`, without
re-reading the visible "4 errors during load" line, and despite this very file's table #3 listing
that exact mistake as the 9th variant of "asserting without searching". The user pointed it out
with: "the cache miss error hasn't gone away — what evidence did you use to assert otherwise?" (1st recurrence).

Recurrence after this rule → escalate to a `PreToolUse:Skill` hook that blocks `cc-plugin cache`
invocation when `/reload-plugins` or `/doctor` output in the recent conversation shows non-zero
errors, forcing routing to `troubleshoot.md`.

## Cache Structure Reference

```
~/.claude/plugins/
├── marketplaces/          # Git clones (source of truth)
│   └── <name>/
│       ├── .claude-plugin/plugin.json
│       ├── skills/
│       └── ...
└── cache/                 # Runtime copies (loaded at session start)
    └── <marketplace>/
        └── <plugin>/
            └── <version>/
                ├── .claude-plugin/
                ├── .mcp.json
                ├── agents/
                ├── dist/
                ├── hooks/
                ├── scripts/
                └── skills/
```

## Key Rules

- **Marketplace = source of truth**, cache = runtime copy
- Cache loads at **session start** — changes need restart
- Missing files in cache → copy from marketplace
- `dist/hud/index.js` required for HUD plugins
- `temp_git_*` directories in cache are safe to delete
