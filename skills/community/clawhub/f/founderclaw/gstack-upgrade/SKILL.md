---
name: founderclaw-upgrade
description: >
  Upgrade founderclaw to the latest version. Detects install location,
  pulls updates, and shows what's new.
  Use when: "upgrade founderclaw", "update founderclaw", "get latest version",
  "update skills".
---

# Upgrade founderclaw

Pull the latest version and show what's new.

## Step 1: Detect Install Location

```bash
SKILL_DIR=""
# Check symlink target
for link in ~/.agents/skills/*/; do
    target=$(readlink "$link" 2>/dev/null)
    if echo "$target" | grep -q "founderclaw"; then
        SKILL_DIR=$(dirname "$target")
        break
    fi
done

# Fallback: direct check
[ -z "$SKILL_DIR" ] && [ -d ~/.agents/skills/founderclaw ] && SKILL_DIR=~/.agents/skills/founderclaw
[ -z "$SKILL_DIR" ] && [ -d founderclaw ] && SKILL_DIR=$(pwd)/founderclaw

if [ -z "$SKILL_DIR" ] || [ ! -d "$SKILL_DIR/.git" ]; then
    echo "founderclaw not found. Install it first."
    exit 1
fi

echo "Install dir: $SKILL_DIR"
```

## Step 2: Save Old Version

```bash
OLD_VERSION=$(cd "$SKILL_DIR" && git rev-parse --short HEAD 2>/dev/null || echo "unknown")
echo "Current version: $OLD_VERSION"
```

## Step 3: Upgrade

```bash
cd "$SKILL_DIR"
STASH_OUTPUT=$(git stash 2>&1)
git fetch origin
git reset --hard origin/main

if echo "$STASH_OUTPUT" | grep -q "Saved working directory"; then
    echo "Note: local changes were stashed. Run 'git stash pop' to restore them."
fi
```

## Step 4: Re-symlink Skills

```bash
SKILLS_DIR=~/.agents/skills
for skill_dir in "$SKILL_DIR"/*/; do
    skill_name=$(basename "$skill_dir")
    [ ! -f "$skill_dir/SKILL.md" ] && continue
    
    target="$SKILLS_DIR/$skill_name"
    if [ -L "$target" ] && [ "$(readlink "$target")" = "$skill_dir" ]; then
        : # already linked
    elif [ ! -e "$target" ]; then
        ln -sf "$skill_dir" "$target"
        echo "  + $skill_name (new)"
    else
        echo "  ~ $skill_name (exists, not overwriting)"
    fi
done
```

## Step 5: Rebuild Browse (if needed)

```bash
BROWSE_BIN="$SKILL_DIR/browse/dist/browse"
if [ ! -x "$BROWSE_BIN" ] && command -v bun >/dev/null 2>&1; then
    echo "Rebuilding browse binary..."
    cd "$SKILL_DIR/browse"
    bun install --silent 2>/dev/null
    bun build src/cli.ts --compile --outfile dist/browse 2>/dev/null
    [ -x "$BROWSE_BIN" ] && echo "  ✓ browse rebuilt" || echo "  ⚠ browse build failed"
fi
```

## Step 6: Show What's New

```bash
cd "$SKILL_DIR"
NEW_VERSION=$(git rev-parse --short HEAD)
echo ""
echo "founderclaw upgraded: $OLD_VERSION -> $NEW_VERSION"
echo ""
echo "Recent commits:"
git log --oneline "$OLD_VERSION..HEAD" 2>/dev/null | head -10
```

## Done

Skills are updated. No restart needed — changes take effect immediately.
