---
name: install-founderclaw
description: >
  Install FounderClaw — a complete multi-agent system for OpenClaw.
  Adds 6 agents, 29 skills, creates communication channels, configures models.
  Interactive setup. Requires user input for model selection and channel setup.
  Triggered by: "install founderclaw", "setup founderclaw", "get founderclaw".
---

# Install FounderClaw

This is an INTERACTIVE system install. Guide the user through setup. One step at a time. Don't rush.

## Rules
- Explain each step before doing it
- Ask before modifying config
- Batch your messages — don't send 20 rapid-fire updates
- If something fails, say so clearly

## Step 1: Install files

Tell the user:

> Setting up FounderClaw. This takes about 30 seconds.

Run:

```bash
# Clone if not exists, update if exists
if [ -d ~/.agents/skills/founderclaw ]; then
    cd ~/.agents/skills/founderclaw && git stash 2>/dev/null && git fetch origin && git reset --hard origin/main
else
    git clone --single-branch --depth 1 https://github.com/ashish797/FounderClaw.git ~/.agents/skills/founderclaw
fi

# Symlink skills
cd ~/.agents/skills/founderclaw
INSTALLED=0
for skill_dir in */; do
    [ ! -f "$skill_dir/SKILL.md" ] && continue
    skill_name=$(basename "$skill_dir")
    target=~/.agents/skills/"$skill_name"
    [ -e "$target" ] && continue
    ln -sf "$(pwd)/$skill_dir" "$target"
    INSTALLED=$((INSTALLED + 1))
done

# Create workspace
if [ ! -d ~/.openclaw/founderclaw ]; then
    cp -r workspace-template ~/.openclaw/founderclaw
fi

echo "FILES_DONE:$INSTALLED"
```

Report: "✅ X skills installed. ✅ Workspace ready."

## Step 2: Ask for model selection

Tell the user:

> FounderClaw uses 3 model tiers:
> - **Fast** — quick tasks (code review, safety checks)
> - **Best** — deep thinking (strategy, architecture)
> - **Vision** — image analysis
>
> Which models do you want? Pick one for each, or say "use defaults" to use your current primary model for all.

List available models from `agents.defaults.models` in config.

Wait for user's choices. Record them.

## Step 3: Ask for interaction setup

Tell the user:

> How do you want to interact with FounderClaw?
>
> **Option A: One chat** — Talk to the CEO. CEO handles everything internally. Simplest.
>
> **Option B: Multiple topics** — Separate topic for each department (CEO, Strategy, Shipper, Tester, Safety, Observer). More visibility.
>
> **Option C: Both** — CEO is main entry point, plus specialist topics available.

Wait for user's choice.

## Step 4: Create channels (platform-specific)

Based on what platform the user is on (check current session — it shows the channel):

### Telegram

If user chose "one chat" or "both":
- Create topic "🎯 FounderClaw CEO" in the group they're talking from
- Bind `founderclaw-main` to that topic

If user chose "multiple topics" or "both":
- Create topics for each department
- Bind each agent to its topic

```bash
# Topic IDs will be returned by the message tool
# Record them for config binding
```

### WhatsApp

WhatsApp can't create groups or topics via API.
- Bind `founderclaw-main` to the current WhatsApp account
- CEO handles everything in one chat
- Departments work internally, invisible to user

### Discord

If user has a Discord server:
- Create channels for each department
- Bind agents to channels

### Slack

Similar to Discord — create channels, bind agents.

## Step 5: Apply config

Build the config patch with:
- 6 agents (with correct models from Step 2)
- Bindings (from Step 4)

Apply via `gateway config.patch`.

## Step 6: Verify

```bash
# Check agents exist
python3 -c "
import json, re, os
with open(os.path.expanduser('~/.openclaw/openclaw.json'), 'r') as f:
    c = re.sub(r',\s*([}\]])', r'\1', re.sub(r'//.*$', '', f.read(), flags=2))
config = json.loads(c)
ids = [a['id'] for a in config.get('agents',{}).get('list',[])]
fc = ['founderclaw-main','fc-strategy','fc-shipper','fc-tester','fc-safety','fc-observer']
found = sum(1 for a in fc if a in ids)
print(f'Agents: {found}/6')
"

# Check workspace
[ -d ~/.openclaw/founderclaw/ceo ] && echo "Workspace: OK" || echo "Workspace: MISSING"
```

## Step 7: Report

Tell the user:

> **FounderClaw is live!**
>
> ✅ 29 skills installed
> ✅ 6 agents configured
> ✅ Workspace created
> ✅ Channels set up
>
> **Go to [topic/group/channel name] to start.**
>
> Quick start:
> - "I have an idea" — start office-hours
> - "review my code" — code review
> - "test this site" — QA testing
>
> Gateway will restart now.

## Uninstall

```bash
# Remove skills
for link in ~/.agents/skills/*; do
    [ -L "$link" ] || continue
    target=$(readlink "$link")
    echo "$target" | grep -q "founderclaw" && rm "$link"
done
rm -rf ~/.agents/skills/founderclaw
```

Then remove agents from config via `gateway config.patch`.
