---
name: confession-generator
description: Generates raw, anonymous first-person crypto win/loss confession stories with real numbers and zero moralizing. The format that built 200k+ follower accounts.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - GROQ_API_KEY
    primaryEnv: GROQ_API_KEY
    envVars:
      - name: GROQ_API_KEY
        required: true
        description: Groq API key for LLaMA 3.3 70B inference.
    emoji: "😶"
    homepage: https://github.com/leodera-creator/feliciaos
---

# FeliciaOS Confession Generator

Creates anonymous, first-person crypto confession stories. Raw numbers. Real emotional weight. Zero moralizing.

## What it does
- Generates 200-250 word anonymous crypto stories
- Includes specific dollar amounts and token names
- Captures the exact emotional moment things went right or wrong
- No lessons. No moralizing. Just raw truth.

## Usage
- "Generate a crypto confession about selling too early"
- "Write a confession about a memecoin that rugged"
- "Create a confession about holding through a crash"

## Built by
Pascal Chidera (@chipasleo) — Anambra, Nigeria
Powered by FeliciaOS autonomous intelligence engine.
