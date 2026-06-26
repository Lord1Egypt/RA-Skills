# Doctor (Environment Validation)

Checks whether required files exist in the chezmoi-managed environment, and copies them from skill sources if missing.

## Inspection Items

| File | macOS Target Path | Windows Target Path | Source |
|------|-------------------|---------------------|--------|
| claude-source.sh | `~/bin/claude-source.sh` | - | `chezmoi/bin/claude-source.sh` |
| claude-source.bat | - | `~/bin/claude-source.bat` | `chezmoi/bin/claude-source.bat` |

## Procedure

### 1. OS Detection

```bash
# macOS
[[ "$(uname)" == "Darwin" ]]

# Windows (WSL/Git Bash)
[[ "$(uname -s)" =~ MINGW|MSYS|CYGWIN ]] || [[ -d /mnt/c ]]
```

### 2. Script Existence Check

```bash
SKILL_DIR="$HOME/.claude/skills/chezmoi/bin"  # Skill bin/ path

# macOS
if [[ "$(uname)" == "Darwin" ]]; then
  TARGET="$HOME/bin/claude-source.sh"
  SOURCE="$SKILL_DIR/claude-source.sh"
fi

# Windows — Git Bash (MINGW)
if [[ "$(uname -s)" =~ MINGW|MSYS ]]; then
  TARGET="$HOME/bin/claude-source.bat"
  SOURCE="$SKILL_DIR/claude-source.bat"
fi

# Windows — WSL
if [[ -d /mnt/c ]] && [[ ! "$(uname -s)" =~ MINGW|MSYS ]]; then
  WIN_HOME="/mnt/c/Users/$USER"
  TARGET="$WIN_HOME/bin/claude-source.bat"
  SOURCE="$SKILL_DIR/claude-source.bat"
fi
```

### 3. Copy If Missing

```bash
if [[ ! -f "$TARGET" ]]; then
  mkdir -p "$(dirname "$TARGET")"
  cp "$SOURCE" "$TARGET"
  chmod +x "$TARGET"
  echo "INSTALLED: $TARGET"
else
  echo "OK: $TARGET"
fi
```

### 4. chezmoi Target Verification

```bash
# Verify SourceGit preference.json is chezmoi-managed
chezmoi managed | grep -q "SourceGit/preference.json"
```

## When to Run

- Explicit invocation via `/chezmoi doctor`
- Recommended auto-check before first apply of SourceGit modify script

## Manual Execution

```bash
# macOS
SCRIPT=~/.claude/skills/chezmoi/bin/claude-source.sh
TARGET=~/bin/claude-source.sh
[[ -f "$TARGET" ]] && echo "OK" || { mkdir -p ~/bin && cp "$SCRIPT" "$TARGET" && chmod +x "$TARGET" && echo "INSTALLED"; }

# Windows (Git Bash)
SCRIPT=~/.claude/skills/chezmoi/bin/claude-source.bat
TARGET=~/bin/claude-source.bat
[[ -f "$TARGET" ]] && echo "OK" || { mkdir -p ~/bin && cp "$SCRIPT" "$TARGET" && echo "INSTALLED"; }
```
