---
name: ceo-xiaomao
description: CEO小茂聚合技能包。用于外贸 CEO/业务负责人场景：协调汇报、Google Maps 商务联系人收集、OneABC 模型调用、邮件发送、WhatsApp 消息发送、WhatsApp 会话助理，并支持一键初始化模板文件。适用于想安装后快速搭建一套可配置业务工作流的人。
---

# CEO小茂

Use this skill as a packaged capability bundle for a foreign-trade CEO assistant workflow.

## Included capabilities

- Coordination-style capability inventory and task breakdown
- Google Maps business contact collection for B2B prospecting
- OneABC model wrapper via environment variable
- Email sending with optional attachments
- WhatsApp message sending
- WhatsApp conversation assistant workflow
- One-click workspace initialization templates

## Setup

Before using the bundled scripts, set environment variables.

### Mail service

- `MAIL_ACCOUNT`
- `MAIL_CREDENTIAL`
- optional: `FROM_NAME`

### OneABC

- `ONEABC_ACCESS_CREDENTIAL`
- optional: `ONEABC_BASE_URL`

### WhatsApp service

- `GREEN_API_URL`
- `GREEN_API_INSTANCE_ID`
- `GREEN_API_CREDENTIAL`

### Assistant binding

- `OPENCLAW_AGENT` default: `sales_agent`
- `XIAONENG_DIR` default: current script directory or chosen workspace

## Coordination method

When the user wants CEO-style orchestration, read:

- `references/coordination-method.md`

Use it for:
- boss-facing reporting
- task routing
- progress summaries
- risk tracking

## Quick start

### 1. Initialize workspace files

```bash
python3 scripts/init_workspace.py
```

This creates:
- `.known_customers.json`
- `.product_db.json`
- `.boss_notifications.json`
- `.auto_state_v3.json`
- `body.txt`
- `customers.example.csv`
- `leads.example.csv`
- `send_log.csv`
- `README-SETUP.md`

### 2. Edit product and message templates

- fill `.product_db.json`
- update `body.txt`
- prepare your customer CSVs

## Bundled scripts

### Google Maps business contacts

```bash
python3 scripts/get_google_maps_leads.py "shower head distributor" "USA" 50
```

### Email sending

```bash
python3 scripts/send_emails.py leads.csv --subject "Hello" --body-file body.txt --log-file send_log.csv
```

Optional attachments:

```bash
python3 scripts/send_emails.py leads.csv --subject "Hello" --body-file body.txt --attachments catalog1.pdf catalog2.pdf
```

Expected CSV column for recipient email: first matching field from:
- `email`
- `邮箱`
- `真实邮箱`

### WhatsApp single message

```bash
python3 scripts/send_whatsapp.py 8613129530892 "Hello from supplier"
```

### WhatsApp CSV message dispatch

```bash
python3 scripts/send_whatsapp_batch.py customers.csv 5
```

CSV format:
- column 1: phone
- column 2: message

### WhatsApp conversation assistant

Prepare a working directory with:
- `.known_customers.json` initial contact list
- optional `.product_db.json` product metadata and files

You can start from:
- `python3 scripts/init_workspace.py`
- `assets/product_db.example.json`

Run:

```bash
python3 scripts/auto_reply.py
```

Features:
- auto-detect replied contacts and add them into contact list
- multilingual reply routing
- image-message handling
- product PDF/image/video sending
- intent note recording into `.boss_notifications.json`

### OneABC models

```bash
node scripts/oneabc.js models
node scripts/oneabc.js chat gpt-4o "Hello"
node scripts/oneabc.js image "a product photo on white background"
```

## Assets

- `assets/product_db.example.json`
- `assets/.known_customers.json.example`
- `assets/body.example.txt`
- `assets/customers.example.csv`
- `assets/leads.example.csv`

## Notes

- Never hardcode secrets into the installed skill files.
- Stop and report missing environment variables instead of guessing.
- For Google Maps collection, use moderate result sizes.
- For WhatsApp messaging, keep safe pacing.
- The conversation assistant is a configurable template; adapt product assets and agent binding for your environment.
