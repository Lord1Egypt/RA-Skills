# ForgeObsidianBrain Sync Engine

Bidirectional synchronization between OpenClaw memory and Obsidian vault.

## Architecture

```
┌─────────────────┐         ┌─────────────────┐
│  OpenClaw       │         │  Obsidian Vault │
│  Memory         │◄───────►│  (Markdown)     │
│  ~/memory/      │  sync   │  ~/obsidian/    │
└─────────────────┘         └─────────────────┘
         │                           │
         └───────────┬───────────────┘
                     │
              ┌──────▼──────┐
              │ Sync Engine │
              │  (Node.js)  │
              └─────────────┘
```

## Components

### 1. `engine.js` - Core Sync Logic

- **Entry parsing**: Extracts entries from memory files using `##` headers
- **Duplicate detection**: Hash-based and substring matching
- **Attribution**: Tracks source and timestamp for every sync
- **Merge logic**: Append-only, never overwrites

### 2. `tracker.js` - State Management

- Persists sync timestamps and processed file lists
- Prevents duplicate processing
- JSON-based state storage (`.sync-state.json`)

### 3. `memory-to-vault.js` - OpenClaw → Obsidian

- Syncs daily memory entries to vault notes
- Creates dated notes in `Daily/` folder
- Preserves entry structure with attribution

### 4. `vault-to-memory.js` - Obsidian → OpenClaw

- Syncs research notes to memory
- Filters out system/templates
- Excludes sync output files (circular sync prevention)

## Usage

### Manual Sync

```bash
# Memory → Vault
node memory-to-vault.js

# Vault → Memory
node vault-to-memory.js

# Force full re-sync
node memory-to-vault.js --force
node vault-to-memory.js --force

# Sync specific file
node memory-to-vault.js --date 2026-05-03
node vault-to-memory.js --note clawhub-gaps.md

# JSON output
node memory-to-vault.js --json
```

### Programmatic API

```javascript
const memoryToVault = require('./memory-to-vault');
const vaultToMemory = require('./vault-to-memory');
const engine = require('./engine');

// Full sync
const result = await memoryToVault.syncAll();
const result = await vaultToMemory.syncAll();

// Specific file
const result = await memoryToVault.syncByDate('2026-05-03');
const result = await vaultToMemory.syncNote('clawhub-gaps.md');

// Analysis only
const analysis = engine.analyzeSync();
```

## Sync Rules

### Bidirectional Flow

1. **Memory → Vault**
   - Scans `~/memory/YYYY-MM-DD.md` files
   - Extracts entries (## headers as delimiters)
   - Merges into `vault/OpenClaw/Daily/YYYY-MM-DD-memory.md`
   - Adds attribution header for every entry

2. **Vault → Memory**
   - Scans `vault/OpenClaw/Inbox/` and `vault/OpenClaw/Daily/`
   - Extracts research content
   - Appends to `~/memory/YYYY-MM-DD.md` as new sections
   - Skips files with `-memory.md` suffix (circular sync prevention)

### Conflict Resolution

- **Never overwrite**: Always append with separator
- **Duplicate detection**: Content hash + substring matching
- **Attribution preserved**: Source and timestamp tracked
- **Incremental sync**: Modification time + processed file list

### Exclusion Patterns

Files matching these patterns are excluded from vault→memory sync:
- `*-memory.md` (memory sync output files)
- `oc-*.md` (OpenClaw prefixed files)

## State Tracking

The tracker maintains:

```json
{
  "lastSync": {
    "memoryToVault": "2026-05-03T20:50:57.909Z",
    "vaultToMemory": "2026-05-03T20:51:36.798Z"
  },
  "processedFiles": {
    "memory": {
      "/home/.../memory/2026-05-03.md": "2026-05-03T20:50:57.909Z"
    },
    "vault": {
      "/home/.../clawhub-gaps.md": "2026-05-03T20:51:36.798Z"
    }
  }
}
```

## Testing

```bash
# Run comprehensive tests
node test.js

# Tests cover:
# - Sync analysis
# - State persistence
# - Entry parsing
# - Duplicate detection
# - Content hashing
# - Exclusion patterns
# - Directory listing
# - Attribution formatting
# - Sync operations
# - File existence
```

## Performance

- Entry parsing: ~1ms per entry
- Duplicate detection: ~0.5ms per comparison
- Full sync (114 entries): ~2 seconds
- Incremental sync: <100ms (no new content)

## Edge Cases Handled

1. **Circular sync prevention**: Excludes sync output files
2. **Duplicate detection**: Hash-based + substring matching
3. **Attribution preservation**: Source tracking on all entries
4. **File modification tracking**: mtime-based incremental sync
5. **Empty file handling**: Graceful skip with logging
6. **Missing directories**: Auto-creation

## File Locations

- Sync engine: `~/.openclaw/workspace/skills/forge-obsidian-brain/scripts/sync/`
- State file: `~/.openclaw/workspace/skills/forge-obsidian-brain/scripts/sync/.sync-state.json`
- Memory: `~/.openclaw/workspace/memory/`
- Vault: `~/obsidian-vault/OpenClaw/`
