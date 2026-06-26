# Template Consolidation (Consolidate)

Detects duplicate chezmoi modify templates and consolidates them into shared scripts.

## Workflow

### 1. Detect Duplicates

```bash
# List modify templates
find ~/.local/share/chezmoi -name "modify_*.tmpl" -type f

# Check duplicates by hash
find ~/.local/share/chezmoi -name "modify_*.tmpl" -type f -exec md5 {} \;
```

### 2. Pattern Analysis

**VSCode family app patterns:**
- `settings.json` - Claude Code settings, themes, file exclusions
- `keybindings.json` - Keyboard shortcuts

**MCP configuration patterns:**
- `.claude.json`, `.cursor/mcp.json` - mcpServers object
- `.utcp_config.json` - manual_call_templates array

### 3. Create Shared Scripts

**Location:** `~/.local/share/chezmoi/.chezmoi-lib/`

**Naming convention:** `executable_<feature>.sh`

**Example:**
```bash
#!/bin/bash
# ~/.chezmoi-lib/executable_vscode-settings.sh

# Pass per-app additional settings via environment variable
if [[ -z "$EXTRA_SETTINGS" ]]; then
  EXTRA_SETTINGS='{}'
fi

# Merge common settings + additional settings
cat | jq --argjson extra "$EXTRA_SETTINGS" '. * {common_settings} * $extra'
```

### 4. Modify Templates

Change existing templates to call the shared script:

```bash
#!/bin/bash
# Antigravity: includes additional settings
export EXTRA_SETTINGS='{"app_specific": "settings"}'
exec {{ .chezmoi.sourceDir }}/.chezmoi-lib/executable_vscode-settings.sh
```

### 5. Verification

```bash
# Review results
chezmoi diff

# Apply
chezmoi apply
```

## Immediate Consolidation Principle

**When copying a modify script via `cp` to a cross-platform path, if the content is identical, immediately extract to `.chezmoi-lib/` and convert to a thin wrapper.**

- No "consolidate later" after `cp` — consolidate at the time of copy
- If no existing `.chezmoi-lib/` script exists, create a new one
- If already a wrapper calling a shared script, copy as-is

## Consolidation Checklist

- [ ] Compare template hashes for duplicates
- [ ] **If a newly copied file is identical to an existing file, immediately extract to shared script**
- [ ] Extract common parts
- [ ] Separate per-app differences via environment variables
- [ ] Verify shared script execution permissions
- [ ] Validate results with chezmoi diff

## Existing Consolidation Patterns

| Shared Script | Purpose | Environment Variable |
|---------------|---------|---------------------|
| `vscode-settings.sh` | VSCode settings | `EXTRA_SETTINGS` |
| `vscode-keybindings.sh` | VSCode keybindings | `EXTRA_KEYBINDINGS` |
| `mcp-servers.sh` | MCP server injection | - |
| `generate-utcp-config.sh` | UTCP config generation | - |
| `sourcegit-preference.sh` | SourceGit CustomActions | `SOURCEGIT_EXECUTABLE` |
| `powershell-profile.sh` | PowerShell profile (pwsh + WindowsPowerShell) | - |
