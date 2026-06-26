<div align="center">

# dining.skill

> *「Before you starve or scroll — let the algorithm decide」*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Claude Skill](https://img.shields.io/badge/Claude-Skill-blueviolet)](https://claude.ai)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-green)](https://skills.sh)
[![Version](https://img.shields.io/badge/version-2.1-blue)](SKILL.md)
[![Cuisines](https://img.shields.io/badge/cuisines-10-orange)](references/cuisine-profiles.md)
[![GitHub](https://img.shields.io/badge/GitHub-ChenChen913%2Fdining--skill-black?logo=github)](https://github.com/ChenChen913/dining-skill)

<br>

**An AI skill that decides what you should eat today.**

<br>

[Quick Start](#quick-start) · [The Problem It Solves](#the-problem-it-solves) · [What It Can Do](#what-it-can-do) · [Install](#install) · [File Structure](#file-structure)

<br>

**其他语言 / Other Languages：** [中文](README.md)

</div>

---

## Quick Start

Once installed, just say:

```
what should I eat
3 people, cooking at home, no lamb
```

That's it.

---

## The Problem It Solves

Everyone faces the same question every single day: what should I eat.

Cooking at home: what dishes to make? Ordering delivery: scrolling for 30 minutes, still can't decide. Hosting a dinner: how many dishes? Which ones? Trying to eat healthy: you're hungry but scared of calories, so you end up eating nothing or something boring.

This isn't you being indecisive. Behavioral economists call it the "paradox of choice" — too many options, brain shuts down.

This skill fixes that. Tell it how many people, cooking or delivery, any dietary restrictions, any special needs. It gives you concrete answers. Not more options. Just what to eat.

---

## What It Can Do

**Everyday meals**

Tell it the basics — headcount, home cooking or delivery, what you don't eat. It gives you two complete meal plans with clear dish names. If you're cooking, it also tells you what to cook first, what can run in parallel, and how to time everything.

**Special situations**

Hot pot night? It recommends broth bases and a shopping list organized by cooking time. Full vegetarian? It swaps meat with a plant-protein chain and picks dishes that feel substantial. Cutting weight? It gives you low-cal, high-protein options with calorie estimates. Camping? It picks portable, no-refrigeration-needed dishes.

**Hosting and gatherings**

Family dinner, business banquet, old friends reunion — it adjusts the style automatically. Family meals lean warm and homey. Business dinners lean refined and impressive. Friend gatherings lean bold and shareable. Kids at the table? It automatically adds a sweet or sweet-and-sour dish they'll actually eat.

**Remembers what you like**

Tell it once "I'm from Sichuan, I love spicy food." It remembers. Tell it "red-braised pork only at family dinners, don't suggest it otherwise." It adjusts. The more you use it, the more it feels like it knows you.

**Four perspectives on every meal**

Every recommendation gets reviewed from four angles: health safety (like "no seafood for gout"), nutritional balance, fitness goals, and emotional satisfaction. They give you different takes on the same meal plan — one might say "Plan B is better for your cut," another might say "but Plan A is what you actually need after a rough day."

**Delivery-smart**

Not all dishes survive delivery. Steamed fish gets cold. Fried chicken goes soggy. Noodles clump together. This skill knows which dishes travel well and which don't. When you're ordering delivery, it automatically avoids the risky ones.

---

## Install

### Method 1: npx (Recommended)

```bash
npx skills add ChenChen913/dining-skill
```

### Method 2: Git Clone

```bash
git clone https://github.com/ChenChen913/dining-skill.git
cp -r dining-skill ~/.claude/skills/dining
```

Or download ZIP from [GitHub Releases](https://github.com/ChenChen913/dining-skill/releases), extract to your AI assistant's skills directory:
- Claude Code: `~/.claude/skills/dining/`
- Reasonix Code: `~/.reasonix/skills/dining/`

### Method 3: Ask Your AI to Do It

Send the repo URL to your AI assistant:

```
Clone https://github.com/ChenChen913/dining-skill and install it to my skills directory
```

---

## File Structure

```
dining-skill/
├── SKILL.md                     # Main file
├── references/                  # Rules and templates
│   ├── mode-routing.md
│   ├── algorithm-engine.md
│   ├── cuisine-profiles.md      # 10 cuisines database
│   ├── expert-cabinet.md
│   ├── memory-system.md
│   ├── output-schema.md
│   └── heuristics.md
├── assets/
│   └── dishes-reference.md      # 74-dish lookup table
├── README.md
└── README_EN.md
```

---

## License

MIT
