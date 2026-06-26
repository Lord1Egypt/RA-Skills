<div align="center">

# Cooking.skill

> If you do not know what to cook, start by being honest about your cravings and your fridge.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Agent Skill](https://img.shields.io/badge/Skill-Cooking-green)](#)
[![Status](https://img.shields.io/badge/status-v0.1.0-orange)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A cooking skill that asks only a couple of useful questions, then gives you a recipe you can actually execute.

</div>

Default focus:

- Chinese home cooking
- practical household techniques
- lively but normal human phrasing

## What it does

- Helps users decide what to cook
- Works from either cravings or available ingredients
- Answers dish-specific or technique-specific questions directly
- Includes substitutions, failure warnings, and rescue tips

## Default interaction

The skill tries to route the request automatically:

- `what do I want to eat`
- `what do I have at home`
- `how do I make / fix this dish`

When needed, it asks at most two questions:

1. `How many people are eating`
2. `Any dietary limits, skill limits, or missing ingredients/tools`

## Output shape

The default answer includes:

- what to cook
- why it fits
- what you need
- how to cook it
- key technique notes
- likely failure points
- substitutions or rescue options

## Installation

Universal:

```bash
npx skills add zning1994/cooking-skill
```

OpenClaw / ClawHub:

```bash
openclaw skills install cooking-skill
```

For the current project:

```bash
mkdir -p .claude/skills
git clone https://github.com/zning1994/cooking-skill .claude/skills/cooking-skill
```

Global install:

```bash
git clone https://github.com/zning1994/cooking-skill ~/.claude/skills/cooking-skill
```

## Example prompts

```text
What should I cook tonight?
I have chicken thighs, potatoes, and onions
How do I keep beef tender in a stir-fry?
What can I do if I do not have cooking wine?
```

## Project structure

```text
cooking.skill/
├── SKILL.md
├── agents/openai.yaml
└── references/
    ├── style-guide.md
    ├── cooking-framework.md
    └── techniques.md
```

## Principles

- usefulness before performance
- answer first, explanation second
- minimal questions
- practical home-kitchen logic
