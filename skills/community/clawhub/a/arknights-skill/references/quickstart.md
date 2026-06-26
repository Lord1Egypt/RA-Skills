# Quick Start

Get started with arknights-skill in three steps.

## 1. Install

Choose your platform:

**Hermes:**
```bash
skills add git+https://github.com/morandot/arknights-skill.git --skill arknights-skill
```

**Shell (manual):**
```bash
bash -c "$(curl -fsSL https://raw.githubusercontent.com/morandot/arknights-skill/main/install.sh)"
```

**Claude Code:**
Tell your agent: "Install the skill `arknights-skill` from https://github.com/morandot/arknights-skill"

**Codex / OpenClaw:**
Use `npx skills add https://github.com/morandot/arknights-skill --skill arknights-skill`

## 2. Set Up Your Profile

Tell the agent about your account. It will automatically save your info to a local Doctor profile:

> "我是 CN 服 120 级博士，有银灰精英 2 专 9 技能 3，棘刺精英 2 专 9 技能 3，塞雷娅精英 2 专 9 技能 1"

> "I'm a level 120 Doctor on CN server. I have SilverAsh E2 M9 S3, Thorns E2 M9 S3, Saria E2 M9 S1"

The agent will save your operators and account info. You can update it anytime by mentioning new operators or progress changes.

## 3. Ask Questions

- "银灰值不值得练？" / "Is SilverAsh worth building?"
- "银灰和棘刺谁更好？" / "SilverAsh vs Thorns?"
- "OF-F4 怎么打？" / "How to clear OF-F4?"
- "新手该先练谁？" / "Who should I raise first?"

The agent will use your profile to give personalized advice.

## Managing Your Profile

The agent manages the profile automatically. If you need manual control:

```bash
# View profile location
python3 arknights-skill/scripts/memory.py path

# Read current profile
python3 arknights-skill/scripts/memory.py read

# List recorded operators
python3 arknights-skill/scripts/memory.py list --owned

# Search operators
python3 arknights-skill/scripts/memory.py search silver

# Clean up stale pending confirmations
python3 arknights-skill/scripts/memory.py gc

# Delete an operator
python3 arknights-skill/scripts/memory.py delete-operator SilverAsh
```

Your profile is stored at `~/.config/arknights-skill/doctor-profile.json`. It never leaves your machine.
