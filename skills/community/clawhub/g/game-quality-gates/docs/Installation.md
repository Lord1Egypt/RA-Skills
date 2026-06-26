# Installation

## For OpenClaw Users

### Quick Install

```bash
git clone https://github.com/abczsl520/game-quality-gates.git ~/.openclaw/skills/game-quality-gates
```

Then restart OpenClaw Gateway:
```bash
openclaw gateway restart
```

### How It Works

Once installed, the skill **auto-triggers** whenever you work on game-related tasks:
- Building new games
- Reviewing game code
- Debugging game bugs
- Deploying game projects

The AI agent will automatically:
1. Load the 12 universal rules
2. Load engine-specific references (Phaser/Three.js) when relevant
3. Run the pre-deploy checklist before deployment

### Updating

```bash
cd ~/.openclaw/skills/game-quality-gates && git pull
```

### Uninstalling

```bash
rm -rf ~/.openclaw/skills/game-quality-gates
```

---

## For Non-OpenClaw Users

The rules and checklists are just Markdown files — useful for any game developer:

1. **[SKILL.md](../blob/main/SKILL.md)** — All 12 rules + checklists in one file
2. **[references/phaser.md](../blob/main/references/phaser.md)** — Phaser-specific guide
3. **[references/threejs.md](../blob/main/references/threejs.md)** — Three.js-specific guide
4. **[references/anti-cheat.md](../blob/main/references/anti-cheat.md)** — Anti-cheat patterns

Bookmark them, print them, paste them into your project's `CONTRIBUTING.md` — whatever works for your workflow.

---

## Supported Engines & Platforms

| Engine/Platform | Coverage |
|----------------|----------|
| **Any H5/Canvas game** | 12 universal rules |
| **Phaser 3** | Universal + 4 Phaser-specific rules |
| **Three.js** | Universal + 4 Three.js-specific rules |
| **WeChat WebView** | Mobile checklist items |
| **iOS Safari** | Audio lifecycle rules |

Future: Unity WebGL, PixiJS, Babylon.js guides welcome as PRs!
