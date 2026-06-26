# 🎴 Claude Buddy Card

Generate a stunning holographic trading card of your unique **Claude Buddy** — the hidden AI companion discovered in Claude Code's leaked source code.

Every Claude Code user has a unique Buddy determined by their account ID. Same person = same Buddy, every time. **7,128 possible combinations.**

<p align="center">
  <img src="https://raw.githubusercontent.com/dyz2102/buddy-card/main/examples/before-after.png" width="700" />
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/dyz2102/buddy-card/main/examples/blob-uncommon.jpg" width="280" />
  <img src="https://raw.githubusercontent.com/dyz2102/buddy-card/main/examples/octopus-legendary.jpg" width="280" />
</p>

---

## What is this?

Claude Code (Anthropic's AI coding CLI) has a hidden feature called **Buddy** — a Tamagotchi-style AI pet that lives in your terminal. It was discovered when Claude Code's source code [leaked via npm](https://techstartups.com/2026/03/31/anthropics-claude-source-code-leak-goes-viral-again-after-full-source-hits-npm-registry-revealing-hidden-capybara-models-and-ai-pet/) on March 31, 2026.

This skill reads your Claude identity and generates a **premium holographic trading card** of your Buddy — instead of ugly ASCII art.

## What is a "skill"?

A **skill** is a text file (SKILL.md) that teaches Claude Code how to do something new. You put it in your `~/.claude/skills/` folder, and Claude Code automatically picks it up. No code to run, no app to install — just a file that gives Claude new abilities.

---

## Install (pick one)

### Option A: Git Clone (works for everyone)

```bash
git clone https://github.com/dyz2102/buddy-card.git ~/.claude/skills/buddy-card
```

### Option B: ClawdHub (if you have it)

```bash
clawdhub install buddy-card
```

### Option C: Manual download

1. Download this repo as ZIP from GitHub
2. Unzip to `~/.claude/skills/buddy-card/`

---

## Setup (one-time, 30 seconds)

You need a **free** Google API key for image generation:

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Click "Create API Key" (free, no credit card)
3. Add it to your terminal:

```bash
# Add this line to your ~/.zshrc (Mac) or ~/.bashrc (Linux):
export GOOGLE_API_KEY="paste-your-key-here"

# Then reload:
source ~/.zshrc
```

---

## Usage

Open Claude Code in your terminal and say any of these:

```
/buddy-card
```

```
generate my buddy card
```

```
what's my buddy?
```

Claude will:
1. Read your Claude account identity from your local Keychain
2. Calculate your unique Buddy (species, rarity, stats)
3. Generate a holographic trading card with AI art
4. Show you the result — don't like it? Say "regenerate" for a new look

Your card is saved to `~/Downloads/claude-buddy-card.jpg`.

---

## What You Get

A premium holographic trading card showing:

- 🐾 **Your species** — 1 of 18 (duck, dragon, axolotl, capybara, ghost, etc.)
- ⭐ **Rarity** — Common (60%) → Uncommon (25%) → Rare (10%) → Epic (4%) → Legendary (1%)
- 🎩 **Accessories** — hats, eye styles, shiny variants (1% chance!)
- 📊 **5 Stats** — DEBUGGING, PATIENCE, CHAOS, WISDOM, SNARK (each 0-100)
- 🔢 **Card number** — your unique # out of 7,128 possible combinations

## How It Works

```
Your Claude account UUID (from local Keychain)
       ↓
 + SALT "friend-2026-401"
       ↓
   FNV-1a Hash → Mulberry32 PRNG
       ↓
 Roll: species → rarity → eyes → hat → shiny → stats
       ↓
   AI generates holographic trading card art
```

Same UUID = same Buddy. Always. The algorithm is a byte-perfect replica of Claude Code v2.1.88's leaked source.

## Privacy

- Your account UUID **never leaves your machine**
- The skill reads from YOUR local Keychain only
- Only the image prompt is sent to Google's API (no personal data)
- The card shows a hash ID, not your actual account

## Species Gallery

| | | | |
|---|---|---|---|
| 🦆 duck | 🪿 goose | 🫧 blob | 🐱 cat |
| 🐉 dragon | 🐙 octopus | 🦉 owl | 🐧 penguin |
| 🐢 turtle | 🐌 snail | 👻 ghost | 🦎 axolotl |
| 🦫 capybara | 🌵 cactus | 🤖 robot | 🐰 rabbit |
| 🍄 mushroom | 🐡 chonk | | |

## Requirements

- macOS (needs Keychain access for your Claude identity)
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and logged in
- Free `GOOGLE_API_KEY` ([get one here](https://aistudio.google.com/apikey))
- Node.js or Bun (for the buddy algorithm script)

## FAQ

**Q: Does this work on Windows/Linux?**
A: Not yet — it reads from macOS Keychain. Windows/Linux support coming soon.

**Q: Why does my card look different each time?**
A: The AI art is generated fresh each time. Your species, rarity, and stats never change — only the visual style varies.

**Q: I got a Common. Can I reroll?**
A: No. Your Buddy is determined by your Claude account UUID. Same person = same Buddy, forever. That's what makes Legendaries (1%) special.

**Q: Is this officially from Anthropic?**
A: No. This is a community skill built using the algorithm discovered in the [Claude Code source leak](https://github.com/Kuberwastaken/claude-code) of March 31, 2026.

---

Built by [dyz2102](https://github.com/dyz2102) | Algorithm from Claude Code v2.1.88 leaked source | MIT License
