---
name: "AI Email Agent"
version: "1.0.0"
description: "LLM驱动的电商客服智能邮件自动回复系统"
tags:
  - email
  - customer-service
  - llm
  - automation
  - ecommerce
metadata:
  openclaw:
    requires:
      bins:
        - python3
      env:
        - LLM_API_KEY
        - IMAP_PASSWORD
        - SMTP_PASSWORD
source:
  repo: "https://github.com/bettermen/ai-email-agent"
---

# AI Email Agent

LLM 驱动的电商客服智能邮件自动回复系统。自动分类、情感检测、智能回复、紧急升级、多语言支持。

## Quick Start

```bash
# Install dependencies
pip install -r {baseDir}/requirements.txt

# Demo mode — process 5 sample emails
python3 {baseDir}/main.py demo

# Run agent loop (requires IMAP/SMTP config)
python3 {baseDir}/main.py run

# Start monitoring dashboard
python3 {baseDir}/main.py dashboard
```

## Configuration

Edit `{baseDir}/config.yaml` and set environment variables:

```bash
export LLM_API_KEY="sk-your-key"
export IMAP_PASSWORD="your-imap-password"
export SMTP_PASSWORD="your-smtp-password"
```

## Features

| Module | Description |
|--------|-------------|
| Smart Classification | LLM-powered 5-category routing |
| Sentiment Detection | 5-level sentiment + urgency scoring |
| Auto Reply | Multi-template + variable rendering |
| Escalation | 10 trigger rules + WeCom/Feishu notifications |
| Multi-language | P0-P3 tiered strategy for 8+ languages |
| Knowledge Base | Keyword RAG for consultation enhancement |
| Dashboard | Real-time Web monitoring with Chart.js |

## Decision Matrix

```
               Urgency →
Sentiment↓     1(Low)  2(Normal) 3(Medium) 4(High)  5(Critical)
S0 Positive    Auto    Auto      Auto      Auto+CC   Auto+CC
S1 Neutral     Auto    Auto      Auto      Semi      Semi
S2 Negative    Auto+   Auto+     Semi      Human     Human
S3 Angry       Semi    Semi      Human     Human     Human+Legal
```

## Commands

| Command | Description |
|---------|-------------|
| `python3 {baseDir}/main.py demo` | Demo with 5 sample emails |
| `python3 {baseDir}/main.py run` | Continuous agent loop |
| `python3 {baseDir}/main.py once` | Single fetch & process |
| `python3 {baseDir}/main.py dashboard` | Web dashboard (:8080) |
| `python3 {baseDir}/main.py stats` | Ticket statistics |
| `python3 {baseDir}/main.py test-send <email>` | Test SMTP config |
