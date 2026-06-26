<div align="center">

# Готовка.skill

> Если не знаешь, что готовить, сначала честно скажи, чего хочется и что есть в холодильнике.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Agent Skill](https://img.shields.io/badge/Skill-Cooking-green)](#)
[![Status](https://img.shields.io/badge/status-v0.1.0-orange)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`cooking.skill` — это кулинарный skill, который задает минимум полезных вопросов, а потом выдает рецепт, который реально можно приготовить.

</div>

Базовый фокус:

- домашняя китайская кухня
- практичные техники для обычной кухни
- живой, но нормальный человеческий тон

## Что умеет

- подсказывает, что приготовить
- работает как от желания, так и от набора продуктов
- прямо отвечает на вопросы по блюдам и техникам
- дает замены, предупреждения о типичных ошибках и способы спасти блюдо

## Базовый сценарий

Автоматически различает три типа запроса:

- `что я хочу съесть`
- `что у меня есть дома`
- `как приготовить или исправить это блюдо`

При необходимости задает максимум два вопроса:

1. `на сколько человек`
2. `есть ли ограничения по еде, навыкам или ингредиентам`

## Стандартный ответ

- что готовить
- почему это подходит
- что понадобится
- как готовить
- ключевые моменты
- где чаще всего ошибаются
- замены или способы исправить

## Установка

Универсальная установка:

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

Глобальная установка:

```bash
git clone https://github.com/zning1994/cooking-skill ~/.claude/skills/cooking-skill
```
