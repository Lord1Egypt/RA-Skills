<div align="center">

# Kochen.skill

> Wenn du nicht weißt, was du kochen sollst, sag einfach ehrlich, worauf du Lust hast und was im Kühlschrank liegt.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Agent Skill](https://img.shields.io/badge/Skill-Cooking-green)](#)
[![Status](https://img.shields.io/badge/status-v0.1.0-orange)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`cooking.skill` ist ein Koch-Skill, der nur die nötigsten Fragen stellt und dann ein Rezept liefert, das man wirklich kochen kann.

</div>

Standardfokus:

- chinesische Hausmannskost
- praktikable Techniken für normale Küchen
- lebendige, aber normale Sprache

## Was es kann

- Gerichte empfehlen
- mit vorhandenen Zutaten arbeiten
- konkrete Fragen zu Gerichten oder Techniken direkt beantworten
- Ersatzoptionen, Fehlstellen und Rettungen mitgeben

## Standardablauf

Die Skill unterscheidet automatisch zwischen:

- `worauf habe ich Lust`
- `was habe ich zu Hause`
- `wie mache oder rette ich dieses Gericht`

Wenn nötig, fragt sie höchstens zwei Dinge:

1. `für wie viele Personen`
2. `ob es Einschränkungen, fehlende Zutaten oder Technikgrenzen gibt`

## Standardausgabe

- was du kochen solltest
- warum das passt
- was du brauchst
- wie du es machst
- die wichtigsten Knackpunkte
- wahrscheinliche Fehler
- Ersatz- oder Rettungsoptionen

## Installation

Universell:

```bash
npx skills add zning1994/cooking-skill
```

OpenClaw / ClawHub:

```bash
openclaw skills install cooking-skill
```

```bash
mkdir -p .claude/skills
git clone https://github.com/zning1994/cooking-skill .claude/skills/cooking-skill
```

Global:

```bash
git clone https://github.com/zning1994/cooking-skill ~/.claude/skills/cooking-skill
```
