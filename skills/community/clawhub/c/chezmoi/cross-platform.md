# Cross-Platform

Checks and fixes compatibility so chezmoi dotfiles work on both macOS and Windows.

## Diagnostic Workflow

### 1. Modify Script Extension Check

On Windows, chezmoi **determines the interpreter by file extension**.
`.json.tmpl` cannot find an interpreter and produces a `%1 is not a valid Win32 application` error.

```bash
# Detect problematic files: modify scripts without .sh
find ~/.local/share/chezmoi -name "modify_*.tmpl" -type f | grep -v '.sh.tmpl$'
```

**Fix:**
```bash
# modify_xxx.json.tmpl → modify_xxx.json.sh.tmpl
for f in $(find ~/.local/share/chezmoi -name "modify_*.tmpl" ! -name "*.sh.tmpl"); do
  mv "$f" "${f%.tmpl}sh.tmpl"  # Wrong!
  mv "$f" "${f%.tmpl}.sh.tmpl" # Correct: add the dot
done
```

**chezmoi.toml interpreter configuration (required on both platforms):**

The `[interpreters.sh]` setting is needed on **both** macOS and Windows.

chezmoi strips `.tmpl` and then uses the **next extension** to determine the interpreter:
`modify_keybindings.json.sh.tmpl` → strip `.tmpl` → find `.sh` → interpreter registered → strip `.sh` → target `keybindings.json`

Without `[interpreters.sh]`, `.sh` is not stripped and the **target becomes `keybindings.json.sh`**.
While the script still executes via shebang, the target filename is wrong, so this is required on macOS too.

```toml
# macOS (~/.config/chezmoi/chezmoi.toml)
[interpreters.sh]
    command = "/bin/bash"
    args = []

# Windows (~/.config/chezmoi/chezmoi.toml)
[interpreters.sh]
    command = "C:\\Program Files\\Git\\bin\\bash.exe"
    args = []
```

> **Warning**: Do not use `[interpreters.json]`! If `.json` is recognized as an interpreter extension, the target name gets parsed incorrectly (`.claude.json` → `.claude`).

### 1-1. JSONC Trailing Comma Removal (sed → perl)

macOS BSD sed does not support GNU sed's multiline patterns (`:a;N;$!ba;`). Use `perl -0pe` instead.

```bash
# ❌ GNU sed only — produces "unused label" warning on macOS
sed -E ':a;N;$!ba; s/,([[:space:]]*[}\]])/\1/g'

# ✅ Cross-platform — perl is built-in on both macOS and Windows (Git Bash)
perl -0pe 's/,(\s*[}\]])/\1/g'
```

### 2. CRLF Line Ending Check

Windows jq outputs CRLF (`\r\n`) → if the original file uses LF (`\n`), every line shows as changed.

```bash
# Add tr -d '\r' to scripts using jq in .chezmoi-lib/
grep -l 'jq\|sed' ~/.local/share/chezmoi/.chezmoi-lib/*.sh
```

**Fix:** Append `| tr -d '\r'` at the end of the pipeline
```bash
# Before
cat | jq '...'
# After
cat | jq '...' | tr -d '\r'
```

> **Warning: Do NOT use `tr -d '\r'` when the original file is CRLF!**
> Windows-native apps (e.g. SourceGit `preference.json`) write CRLF. Stripping `\r` causes every line to show as changed.
>
> **Check original line endings:**
> ```bash
> xxd <target_file> | head -3  # 0d0a = CRLF, 0a = LF
> ```
>
> | Original | Action |
> |----------|--------|
> | LF (`0a`) | Add `\| tr -d '\r'` |
> | CRLF (`0d0a`) | Do NOT add `tr -d '\r'` — jq CRLF output matches the original |

### 3. Template Output Function Paths

When chezmoi template's `output` function directly executes `.sh` scripts, it fails on Windows.
There is also an issue where Windows Store's `bash.exe` (WSL stub) is found first in PATH.

**Fix:** Use the full Git Bash path conditionally by OS
```
{{ if eq .chezmoi.os "windows" -}}
{{ output "C:/Program Files/Git/bin/bash.exe" (joinPath .chezmoi.sourceDir ".chezmoi-lib/script.sh") | trim }}
{{- else -}}
{{ output (joinPath .chezmoi.sourceDir ".chezmoi-lib/script.sh") | trim }}
{{- end }}
```

### 4. App Path Mapping

| macOS | Windows | chezmoi source (macOS) | chezmoi source (Windows) |
|-------|---------|------------------------|--------------------------|
| `~/Library/Application Support/App/` | `%APPDATA%/App/` | `private_Library/private_Application Support/private_App/` | `AppData/Roaming/App/` |
| `~/Library/Application Support/App/` | `%LOCALAPPDATA%/App/` | Same | `AppData/Local/App/` |

### 5. OS-Specific Modifier Key Conversion (CHEZMOI_OS Pattern)

When different values are needed per OS (e.g., keybindings), branch using the `CHEZMOI_OS` environment variable.

**Pass OS from template:**
```bash
#!/bin/bash
CHEZMOI_OS={{ .chezmoi.os }} exec {{ .chezmoi.sourceDir }}/.chezmoi-lib/executable_vscode-keybindings.sh
```

**Conditional branching in script:**
```bash
if [ "$CHEZMOI_OS" = "darwin" ] || [ -z "$CHEZMOI_OS" ]; then
  MOD="cmd"
else
  MOD="ctrl"
fi
```

**Placeholder substitution in jq:**
```bash
jq --arg mod "$MOD" --argjson bindings_tmpl '[
  { "key": "MOD+k", "command": "..." }
]' '[$bindings_tmpl[] | .key |= gsub("MOD"; $mod)] as $bindings | ...'
```

> On macOS, defaults to `darwin` behavior when `CHEZMOI_OS` is unset (`-z` check).

### 6. Modify Script Empty Input Handling

If the target file does not exist, chezmoi passes **empty stdin**. `cat | jq` produces no output on empty input, so the file is not created.

**Fix:** Store stdin in a variable and provide a default value
```bash
# For JSON array targets (keybindings.json, etc.)
INPUT=$(cat | sed 's|^[[:space:]]*//.*||')
echo "${INPUT:-[]}" | jq '...'

# For JSON object targets (settings.json, etc.)
INPUT=$(cat | sed 's|^[[:space:]]*//.*||')
echo "${INPUT:-{\}}" | jq '...'
```

> For JSONC (JSON with comments), also handle comment removal with `sed` + trailing comma removal.

### 7. .chezmoiignore OS Branching

```
{{- if eq .chezmoi.os "windows" }}
# Ignore macOS-only paths
*/darwin_*
karabiner
Library
{{- end }}

{{- if ne .chezmoi.os "windows" }}
# Ignore Windows-only paths
AppData
OneDrive
{{- end }}
```

**OS-specific top-level directory mapping:**

| Source Directory | OS | .chezmoiignore Entry |
|---|---|---|
| `private_Library/` | macOS | `Library` (ignored on Windows) |
| `AppData/` | Windows | `AppData` (ignored on macOS) |
| `OneDrive/` | Windows | `OneDrive` (ignored on macOS) |
| `*/darwin_*` | macOS | chezmoiscripts etc. (ignored on Windows) |
| `karabiner` | macOS | (ignored on Windows) |

**When adding a new OS-specific top-level directory, it must be registered in `.chezmoiignore`.** See procedure below.

## Adding a New App Workflow

### 1. Check Paths

```bash
# macOS
ls ~/Library/Application\ Support/AppName/

# Windows
ls "$APPDATA/AppName/" || ls "$LOCALAPPDATA/AppName/"
```

### 2. Create macOS Source

```bash
chezmoi add ~/Library/Application\ Support/AppName/User/settings.json
# Or create modify script directly
```

### 3. Copy Windows Source

```bash
# AppData/Roaming path
mkdir -p ~/.local/share/chezmoi/AppData/Roaming/AppName/User
cp ~/.local/share/chezmoi/private_Library/.../modify_settings.json.sh.tmpl \
   ~/.local/share/chezmoi/AppData/Roaming/AppName/User/

# LocalAppData apps like Syncthing
mkdir -p ~/.local/share/chezmoi/AppData/Local/AppName
# Syncthing has a different API path, so a separate script is needed
```

### 4. Update .chezmoiignore

If a new top-level directory is **OS-specific**, it must be registered in `.chezmoiignore`.

**Auto-check commands:**
```bash
# List top-level directories in chezmoi source
ls -d ~/.local/share/chezmoi/*/ | sed 's|.*/chezmoi/||;s|/$||' \
  | sed 's/^private_//;s/^dot_/./;s/^exact_//'

# Check paths registered in .chezmoiignore
chezmoi execute-template < ~/.local/share/chezmoi/.chezmoiignore
```

Compare the two outputs:
- macOS-specific directories (`Library`, `karabiner`, etc.) should be in the `if eq .chezmoi.os "windows"` block
- Windows-specific directories (`AppData`, `OneDrive`, etc.) should be in the `if ne .chezmoi.os "windows"` block

Insert missing entries in **alphabetical order** within the appropriate block.

### 5. Verification

```bash
chezmoi managed --include=all | grep AppName
chezmoi diff
```

## Full Diagnostic Checklist

- [ ] Modify scripts use `.sh.tmpl` extension
- [ ] `chezmoi.toml` has `[interpreters.sh]` configured (Git Bash path)
- [ ] No `[interpreters.json]` present
- [ ] `| tr -d '\r'` at end of jq/sed pipelines
- [ ] Template `output` function uses OS-conditional bash path
- [ ] `.chezmoiignore` has OS-specific path branching
- [ ] Windows AppData source exists corresponding to macOS Library path
- [ ] `CHEZMOI_OS` environment variable pattern used for OS-specific value branching
- [ ] Modify scripts handle empty input with defaults (`${INPUT:-[]}` or `${INPUT:-{\}}`)
