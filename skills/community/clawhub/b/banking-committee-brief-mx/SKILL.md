---
name: banking-committee-brief-mx
version: 1.0.0
description: Genera un brief ejecutivo para Comite de Riesgos bancario en Mexico. Recibe indicadores CNBV y contexto de mercado via Telegram y devuelve un PDF estructurado listo para presentar al Comite.
author: Ricardo-Mendoza-Rodriguez
tags:
  - banking
  - finance
  - risk
  - compliance
  - cnbv
  - mexico
  - telegram
  - pdf
license: MIT
requires:
  env:
    - name: TELEGRAM_BOT_TOKEN
      description: Token del bot de Telegram obtenido via BotFather
      required: true
---

# Banking Committee Brief — Mexico (Comite de Riesgos)

Brief ejecutivo para Comite de Riesgos bancario en Mexico.
Recibe indicadores CNBV y contexto de mercado via Telegram.
Devuelve PDF estructurado con semaforos regulatorios, agenda del Comite
y senales de alerta basadas en umbrales CNBV / Basilea III Mexico.

## Instalacion
pip install reportlab python-telegram-bot
export TELEGRAM_BOT_TOKEN=tu_token
python3 telegram_handler.py

## Indicadores soportados
ICAP, TIER1, IMOR, CCL, ROE, ROA
