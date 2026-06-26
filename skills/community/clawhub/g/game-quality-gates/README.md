# 🎮 Game Quality Gates

> **Stop shipping games with phantom timers, memory leaks, and double-spend exploits.** A battle-tested quality standard for H5/Canvas/WebGL games.

[![ClawHub](https://img.shields.io/badge/ClawHub-game--quality--gates-blue?style=flat-square)](https://clawhub.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)
[![Wiki](https://img.shields.io/badge/📖_Wiki-8_pages-purple?style=flat-square)](https://github.com/abczsl520/game-quality-gates/wiki)
[![OpenClaw Skill](https://img.shields.io/badge/OpenClaw-Agent_Skill-orange?style=flat-square)](https://github.com/openclaw/openclaw)

---

## 💀 The Problem

Every feature works fine alone. They break **in combination**:

| Feature A | + Feature B | = Bug |
|-----------|-------------|-------|
| Slow powerup | Paddle collision | Speed value overwritten |
| Multi-ball | Main ball death | Orphan sub-balls still scoring |
| Power-up falling | Player dies | Ghost objects after game over |
| Game over | Buff timers | Phantom timer modifies destroyed object 💥 |

These aren't edge cases — they're the **#1 cause of game bugs**. After fixing **70+ of these bugs** in production H5 games, we encoded the prevention patterns into 12 universal rules.

## 📋 The 12 Universal Rules

| # | Rule | Prevents |
|---|------|---------|
| 1 | 🔄 Single Cleanup Entry Point | "Fixed in A, forgot in B" |
| 2 | ⚡ Respect Active Buffs | Buff silently overwritten |
| 3 | 📦 Cache Before Destroy | Reading dead object props |
| 4 | ⏰ Timers Follow Lifecycle | Phantom timers after game over |
| 5 | 🖥️ Frame-Rate Independent | 30fps device = half speed |
| 6 | 🚪 Scene Switch = Full Cleanup | Memory grows per restart |
| 7 | 🔊 Audio Lifecycle | iOS silent, background still playing |
| 8 | 👆 Input Safety | Double-buy, rapid-fire exploits |
| 9 | 💾 Save State Versioning | Broken saves after update |
| 10 | 🌐 Network Fault Tolerance | Game freezes on bad network |
| 11 | 📦 Asset Loading Strategy | White screen, missing textures |
| 12 | 🛡️ Anti-Cheat Baseline | Score injection, payment bypass |

👉 **[Read full details in the Wiki →](https://github.com/abczsl520/game-quality-gates/wiki/Universal-Rules)**

## 🎯 Engine-Specific Guides

### [Phaser 3](https://github.com/abczsl520/game-quality-gates/wiki/Phaser-Guide) (Arcade Physics)
- Multi-touch `pointer.id` tracking (the finger-swap bug)
- `physics.pause()` ≠ `time` pause (the phantom timer gotcha)
- `OVERLAP_BIAS` tuning (3-4 recommended)
- Physics group `clear(true, true)` between levels

### [Three.js](https://github.com/abczsl520/game-quality-gates/wiki/Threejs-Guide) (WebGL/3D)
- The dispose trio: geometry + material + texture (VRAM leak prevention)
- GLB compression pipeline: **14MB → 800KB** (94% reduction)
- `gltf-transform prune` Skin deletion pitfall on rigged models
- Animation crossfade state machine

### [Anti-Cheat](https://github.com/abczsl520/game-quality-gates/wiki/Anti-Cheat-Patterns)
- One-time raid tokens (link start → submit)
- Duration + score sanity checks
- Atomic purchase endpoints (no split deduct/grant)

## ⚡ Install

**OpenClaw users:**
```bash
clawhub install game-quality-gates
```

**Manual:**
```bash
git clone https://github.com/abczsl520/game-quality-gates.git ~/.openclaw/skills/game-quality-gates
```

**Not using OpenClaw?** The wiki is pure knowledge — useful for any game developer. Just [read the docs](https://github.com/abczsl520/game-quality-gates/wiki).

## ✅ Pre-Deploy Checklist (Quick)

```
🔴 Universal (every game)
  □ New objects in cleanupGameState()?
  □ New timers cancelled in cleanup?
  □ Buffs respected when modifying attributes?
  □ Data cached before destroy()?
  □ Delta time used for movement?
  □ No memory leaks across scenes?
  □ Audio pauses on background?
  □ Purchase has click-lock?
  □ Saves have version + migration?
  □ Network has timeout + fallback?
  □ Asset failure degrades gracefully?
  □ Critical ops server-validated?

🟡 Mobile: multi-touch IDs, iOS audio resume, WeChat WebView compat
🔵 Phaser: clear(true,true), OVERLAP_BIAS, time+physics pause sync
🟣 Three.js: dispose trio, Draco loader, fadeIn/fadeOut transitions
```

👉 **[Full checklist with details →](https://github.com/abczsl520/game-quality-gates/wiki/Pre-Deploy-Checklist)**

## 📚 Documentation

📖 **[Full Wiki →](https://github.com/abczsl520/game-quality-gates/wiki)**

| Page | What You'll Learn |
|------|-------------------|
| [Universal Rules](https://github.com/abczsl520/game-quality-gates/wiki/Universal-Rules) | The 12 core rules with code examples |
| [Phaser Guide](https://github.com/abczsl520/game-quality-gates/wiki/Phaser-Guide) | Phaser 3 specific patterns |
| [Three.js Guide](https://github.com/abczsl520/game-quality-gates/wiki/Threejs-Guide) | WebGL/3D specific patterns |
| [Anti-Cheat Patterns](https://github.com/abczsl520/game-quality-gates/wiki/Anti-Cheat-Patterns) | Server-side validation |
| [Pre-Deploy Checklist](https://github.com/abczsl520/game-quality-gates/wiki/Pre-Deploy-Checklist) | Copy-paste before every release |
| [Real Bug Examples](https://github.com/abczsl520/game-quality-gates/wiki/Real-Bug-Examples) | Actual production bugs & fixes |
| [Installation](https://github.com/abczsl520/game-quality-gates/wiki/Installation) | Setup guide |

## 📁 Skill Structure

```
game-quality-gates/
├── SKILL.md                    # 12 rules + checklists (auto-loaded by OpenClaw)
└── references/
    ├── phaser.md               # Phaser-specific (loaded on demand)
    ├── threejs.md              # Three.js-specific (loaded on demand)
    └── anti-cheat.md           # Anti-cheat patterns (loaded on demand)
```

## 📊 Origin

- **Source:** [Pixel Bounce](https://game.weixin-vip.cn/bounce/) (像素弹球王) — 70+ bugs across 10 audit rounds
- **Source:** [Tripo 3D Demo](https://game.weixin-vip.cn/dog/) (柯基跑酷3D) — GLB compression + animation
- **References:** Phaser forum best practices, Three.js dispose docs, web game anti-cheat literature (2024-2025)

## 🔗 Related

- [Browser-Use Skill](https://github.com/abczsl520/browser-use-skill) — AI browser automation for OpenClaw
- [Bug Audit](https://github.com/abczsl520/bug-audit-skill) — Dynamic bug hunting (200+ patterns)
- [Debug Methodology](https://github.com/abczsl520/debug-methodology) — Root-cause debugging
- [OpenClaw](https://github.com/openclaw/openclaw) — The AI agent platform

## 🔗 Part of the AI Dev Quality Suite

| Skill | Purpose | Install |
|-------|---------|---------|
| [bug-audit](https://github.com/abczsl520/bug-audit-skill) | Dynamic bug hunting, 200+ pitfall patterns | `clawhub install bug-audit` |
| [codex-review](https://github.com/abczsl520/codex-review) | Three-tier code review with adversarial testing | `clawhub install codex-review` |
| [debug-methodology](https://github.com/abczsl520/debug-methodology) | Root-cause debugging, prevents patch-chaining | `clawhub install debug-methodology` |
| [nodejs-project-arch](https://github.com/abczsl520/nodejs-project-arch) | AI-friendly architecture, 70-93% token savings | `clawhub install nodejs-project-arch` |
| **game-quality-gates** (this) | 12 universal game dev quality checks | `clawhub install game-quality-gates` |

## 🤝 Contributing

Found a missing pattern? Have engine-specific rules for PixiJS, Babylon.js, or Unity WebGL? [Open an issue](https://github.com/abczsl520/game-quality-gates/issues) or submit a PR!

## 📄 License

[MIT](LICENSE) — Use freely, attribution appreciated.

---

<p align="center">
  <b>⭐ If this saved you from a production bug, star the repo — help other game devs find it!</b>
</p>
