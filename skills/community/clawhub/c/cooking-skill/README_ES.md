<div align="center">

# Cocina.skill

> Si no sabes qué cocinar, empieza por decir qué te apetece y qué tienes en casa.

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![Agent Skill](https://img.shields.io/badge/Skill-Cooking-green)](#)
[![Status](https://img.shields.io/badge/status-v0.1.0-orange)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

`cooking.skill` es una skill de cocina que hace pocas preguntas útiles y luego te da una receta realmente ejecutable.

</div>

Enfoque por defecto:

- cocina casera china
- técnicas prácticas para cocina doméstica
- tono vivo pero normal, sin exageración

## Qué hace

- recomienda qué cocinar
- funciona tanto desde antojos como desde ingredientes disponibles
- responde directamente preguntas sobre platos o técnicas
- incluye sustituciones, errores comunes y formas de corregirlos

## Flujo básico

Detecta automáticamente tres tipos de entrada:

- `qué quiero comer`
- `qué tengo en casa`
- `cómo hago / arreglo este plato`

Cuando hace falta, pregunta como máximo dos cosas:

1. `para cuántas personas`
2. `si hay restricciones, falta de ingredientes o límites de habilidad`

## Respuesta por defecto

- qué cocinar
- por qué encaja
- qué necesitas
- cómo hacerlo
- puntos clave
- riesgos de fallo
- sustituciones o rescates

## Instalación

Instalación universal:

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

Instalación global:

```bash
git clone https://github.com/zning1994/cooking-skill ~/.claude/skills/cooking-skill
```

## Ejemplos

```text
¿Qué cocino esta noche?
Tengo muslos de pollo, patatas y cebolla
¿Cómo hago para que la ternera quede tierna?
¿Qué hago si no tengo vino de cocina?
```
