# Cavepony 🐴🦄🏰

_why use many token when pony do trick_

**Cavepony** is a pony-themed token compression ecosystem for AI agents. Based on the viral [Caveman](https://github.com/JuliusBrussee/caveman) compression, but now with **pony vocabulary** built in. Talk less, think big, but make it equine.

## ✨ Features

- **Five compression modes** from light to ultra-aggressive
- **Pony word substitution** — 50+ human→pony mappings
- **Canterlot mode** — Fancy pony speech expansion (opposite of compression!)
- **CLI tool** — Compress files directly
- **AI agent integration** — Works with Claude Code, OpenClaw, and more
- **Token savings** — ~75% fewer tokens, same technical accuracy

---

## 🚀 Quick Start

### Install CLI
```bash
# Using npx (no install needed)
npx cavepony demo --mode=pony
```

### Try it Out
```bash
# Demo all modes
npx cavepony demo --mode=canterlot

# Compress a file
npx cavepony compress CLAUDE.md --mode=pony

# Transform text
npx cavepony text "Hello human!" --mode=pony
```

### For AI Agents
Add to your system prompt:
```
Terse like cavepony. Technical substance exact. Only fluff die.
Drop: articles, filler (just/really/basically), pleasantries, hedging.
Fragments OK. Short synonyms. Code unchanged.
Pattern: [thing] [action] [reason]. [next step].
Pony substitutions: human/people -> pony/ponies, man/woman -> stallion/mare, etc.
ACTIVE EVERY RESPONSE. No revert after many turns. No filler drift.
Code/commits/PRs: normal. Off: "stop cavepony" / "normal mode".
```

---

## 🎭 Modes

### Lite
`/cavepony lite` — Drop filler words only. Keep grammar intact.
> Original: "I'd be happy to help you with that."  
> **Lite:** "Help you with that."

### Full  
`/cavepony full` — Default cavepony. Drop articles, fragments.
> Original: "The issue is caused by authentication middleware."
> **Full:** "Issue caused by authentication middleware."

### Ultra
`/cavepony ultra` — Maximum compression. Telegraphic speech.
> Original: "The authentication middleware has validation issues."
> **Ultra:** "Auth middleware validation broken."

### Pony 🦄
`/cavepony pony` — Full compression + pony word substitutions.
> Original: "Hello human! The man helped the woman and children."
> **Pony:** "Hello pony! Stallion helped mare and foals."

### Canterlot 🏰
`/cavepony canterlot` — **Fancy pony speech expansion** (opposite of compression!)
> Original: "All the trolls are butthurt."
> **Canterlot:** "By the by, all the parasprites are saddle-sore, as it were."

---

## 🌟 Examples

### Before
> "Sure! I'd be happy to help you with that. The issue you're experiencing is most likely caused by your authentication middleware not properly validating the token expiry. Let me take a look and suggest a fix."

### After Cavepony (Full)
> "Issue: auth middleware not validating token expiry. Fix: use <= not <"

### After Cavepony (Pony Mode) 🦄
> "Issue: auth wing not validating token expiry. Fix: use <= not <"

### After Cavepony (Canterlot Mode) 🏰
> "I daresay, the authentication wing appears to have a most unfortunate malfunction regarding token expiry validation. One might consider employing the <= operator rather than the < operator, if I may be so bold."

---

## 🦄 Pony Dictionary

Cavepony includes 50+ pony word substitutions:

| Human Word | Pony Word |
|------------|-----------|
| human / humans | pony / ponies |
| man / men | stallion / stallions |
| woman / women | mare / mares |
| boy / girl | colt / filly |
| child / children | foal / foals |
| people | ponies |
| person | pony |
| anybody / anyone | anypony |
| everybody / everyone | everypony |
| nobody / no one | nopony |
| hands / feet | hooves |
| hand / foot | hoof |
| hey | hay |
| hell / heck | hay |
| troll / trolls | parasprite / parasprites |
| butthurt | saddle-sore |
| New York | Manehattan |
| Philadelphia | Fillydelphia |
| Christmas | Heartswarming |
| Halloween | Nightmare Night |

*(See `cavepony-compress/pony-dict.json` for full list)*

---

## 🛠️ CLI Usage

### Installation
```bash
npm install -g cavepony
```

### Commands
```bash
# Demo all modes
cavepony demo --mode=canterlot

# Compress a file (creates .original backup)
cavepony compress CLAUDE.md --mode=pony

# Transform text directly
cavepony text "Hello human!" --mode=pony

# Help
cavepony --help
```

### File Compression
```bash
# Compress memory files for AI agents
cavepony compress CLAUDE.md --mode=pony

# Result:
# CLAUDE.md → Compressed version (agent reads this)
# CLAUDE.original.md → Human-readable backup
```

---

## 🔌 Integration

### Claude Code
Auto-activation via hooks:
```bash
bash <(curl -s https://raw.githubusercontent.com/cavepony/cavepony/main/hooks/install.sh)
```

### OpenClaw
Copy to skills directory:
```bash
cp -r cavepony /home/node/.openclaw/workspace/skills/
```

### Any AI Agent
Add the system prompt snippet from [Quick Start](#-quick-start).

---

## 📊 Benchmarks

| Task | Normal | Cavepony | Saved |
|------|--------|----------|-------|
| Explain React re-render | 1,180 tokens | 159 tokens | 87% |
| Fix auth middleware | 704 tokens | 121 tokens | 83% |
| Explain git rebase | 702 tokens | 292 tokens | 58% |
| Docker multi-stage | 1,042 tokens | 290 tokens | 72% |

**Average**: ~75% token reduction, same technical accuracy.

---

## 📁 Project Structure

```
cavepony/
├── README.md                 # This file
├── SKILL.md                  # OpenClaw skill documentation
├── package.json              # Node module config
├── cavepony-compress/        # Core compression engine
│   ├── compress.js           # Main compression logic
│   ├── pony-dict.json        # 50+ pony word mappings
│   ├── canterlot-dict.json   # Fancy vocabulary
│   ├── bin/cavepony          # CLI tool
│   └── test-compress.js      # Test suite
├── skills/CAVEPONY.md        # AI agent skill instructions
├── hooks/                    # Claude Code auto-activation
│   ├── install.sh
│   └── install.ps1
└── memory/example.md         # Example compressed memory
```

---

## 🏹 Ecosystem

- **Cavepony** — Talk less (you are here) 🐴
- **Haymem** — Remember more (pony memory - coming soon) 💾
- **Pasturekit** — Build better (pony workflow - coming soon) 🏗️

---

## 📝 License

MIT. Pony magic included free of charge.

---

_Everypony deserves to be heard. Even if that chance is 75% fewer tokens. 🦄✨_

---

**Created with love by Baud & sun**  
🐴 *stomps hooves proudly* 🏍️