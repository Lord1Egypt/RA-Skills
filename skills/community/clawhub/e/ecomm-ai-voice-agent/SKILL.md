---
name: ecomm-ai-voice-agent
description: Complete AI voice agent system for eCommerce order confirmation, customer support, and outbound campaigns. 12 production-ready n8n workflows with Vapi AI voice, Twilio SMS, Shopify/WooCommerce integration, and Google Sheets CRM.
tags: [ecommerce, voice-agent, vapi, twilio, shopify, woocommerce, order-confirmation, customer-support, n8n, automation]
author: mhmalvi
version: 1.2.0
license: CC BY-NC-SA 4.0
metadata:
  clawdbot:
    emoji: "📞"
    requires:
      n8nCredentials: [google-sheets-oauth2, smtp]
      env: [VAPI_API_KEY, VAPI_API_URL, VAPI_COD_ASSISTANT_ID, TWILIO_ACCOUNT_SID, TWILIO_PHONE_NUMBER, TWILIO_AUTH_HEADER, TWILIO_API_URL, ECOMM_ORDERS_SHEET_ID, ECOMM_CALL_LOG_SHEET_ID, ECOMM_CUSTOMERS_SHEET_ID, N8N_WEBHOOK_BASE, WHATSAPP_API_URL, WHATSAPP_API_TOKEN, SHOPIFY_STORE_URL, SHOPIFY_ACCESS_TOKEN, WOOCOMMERCE_STORE_URL, WOOCOMMERCE_AUTH_HEADER, HUBSPOT_API_KEY, OPENAI_API_KEY, ECOMM_FROM_EMAIL, ECOMM_OWNER_EMAIL, ECOMM_STAFF_EMAIL, ECOMM_CONFIRM_BASE_URL]
    os: [linux, darwin, win32]
---

# eComm AI Voice Agent 📞

A production-ready, 12-workflow AI voice agent system for eCommerce businesses. Handles order confirmation calls, customer support, returns, retries, and outbound campaigns — fully automated.

## Problem

eCommerce businesses (especially COD-heavy markets) lose 20-40% of orders to fake orders, no-shows, and unconfirmed deliveries. Manual confirmation calls are expensive and don't scale.

This system automates the entire confirmation and support lifecycle using AI voice calls.

## What's Included

### 12 Production Workflows

| # | Workflow | Function |
|---|----------|----------|
| 01 | **Order Intake** | Webhook receives new orders, validates, routes by payment type |
| 02 | **COD Confirmation Call** | AI voice call to confirm cash-on-delivery orders |
| 03 | **Prepaid Confirmation** | SMS confirmation + optional high-value voice call |
| 04 | **Call Result Handler** | Processes Vapi callbacks, routes by outcome |
| 05 | **Retry Engine** | Auto-retries unanswered calls on schedule |
| 06 | **WhatsApp/SMS Fallback** | Multi-channel fallback for unreachable customers |
| 07 | **Returns & FAQ Handler** | Intent-based routing for support queries |
| 08 | **Order Status Updater** | Syncs status back to Shopify/WooCommerce |
| 09 | **CRM & Sheet Logger** | Central event logging + HubSpot sync |
| 10 | **Outbound Campaign** | Proactive engagement for unconfirmed orders |
| 11 | **Daily Report** | Automated metrics email to admin |
| 12 | **Customer Callback** | Inbound call queue management |

## Architecture

```
Shopify/WooCommerce Order
    │
    ▼
Workflow 01: Order Intake & Routing
    │
    ├── COD Order ──► Workflow 02: AI Voice Call
    │                     │
    │                     ▼
    │               Workflow 04: Parse Call Result
    │                     │
    │                     ├── Confirmed → Fulfill
    │                     ├── Declined → Cancel
    │                     └── No Answer → Workflow 05: Retry
    │                                         │
    │                                         └── Max retries → Workflow 06: SMS/WhatsApp
    │
    ├── Prepaid ──► Workflow 03: SMS + Optional Call
    │
    └── All Events ──► Workflow 09: Central Logger
                            │
                            ├── Google Sheets (Orders, Call Log, Customers)
                            └── HubSpot CRM (optional)

Scheduled:
├── Workflow 05: Retry Engine (configurable intervals)
├── Workflow 08: Status Sync (periodic)
├── Workflow 10: Outbound Campaigns (2-hourly, 9AM-7PM)
└── Workflow 11: Daily Report (once daily)
```

## Required n8n Credentials

You must create these credentials in your n8n instance before importing:

| Credential Type | Used For | Placeholder in JSON |
|----------------|----------|---------------------|
| Google Sheets OAuth2 | Order tracking, call logs, customer CRM | `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` |
| SMTP (Gmail or custom) | Daily report emails | `YOUR_SMTP_CREDENTIAL_ID` |

All other API keys are configured via n8n environment variables (see below).

## Quick Start

### 1. Prerequisites
- n8n v2.4+ (self-hosted)
- Vapi.ai account (AI voice calls)
- Twilio account (SMS + phone numbers)
- Google Sheets OAuth2 credentials
- Shopify or WooCommerce store

### 2. Environment Variables
```bash
# Google Sheets
ECOMM_ORDERS_SHEET_ID=your-sheet-id
ECOMM_CALL_LOG_SHEET_ID=your-sheet-id
ECOMM_CUSTOMERS_SHEET_ID=your-sheet-id

# Vapi AI Voice
VAPI_API_URL=https://api.vapi.ai
VAPI_API_KEY=your-vapi-key
VAPI_COD_ASSISTANT_ID=your-assistant-id

# Twilio
TWILIO_ACCOUNT_SID=your-sid
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_AUTH_HEADER=Basic base64encoded
TWILIO_API_URL=https://api.twilio.com/2010-04-01

# Inter-workflow routing
N8N_WEBHOOK_BASE=https://your-n8n-instance.com/webhook

# Email addresses
ECOMM_FROM_EMAIL=orders@yourbusiness.com
ECOMM_OWNER_EMAIL=owner@yourbusiness.com
ECOMM_STAFF_EMAIL=staff@yourbusiness.com

# Optional
HUBSPOT_API_KEY=your-key
OPENAI_API_KEY=your-key
SHOPIFY_STORE_URL=https://your-store.myshopify.com
SHOPIFY_ACCESS_TOKEN=your-shopify-access-token
WOOCOMMERCE_STORE_URL=https://your-store.com
WOOCOMMERCE_AUTH_HEADER=Basic base64encoded
WHATSAPP_API_URL=https://graph.facebook.com/v17.0/YOUR_PHONE_ID
WHATSAPP_API_TOKEN=your-whatsapp-token
ECOMM_CONFIRM_BASE_URL=https://your-store.com/confirm
```

### 3. Sheet Setup
Create 3 Google Sheets with these tabs:
- **Orders**: order_id, customer_name, phone, email, amount, payment_type, status, created_at
- **Call Log**: call_id, order_id, phone, outcome, transcript, duration, created_at
- **Customers**: customer_id, name, phone, email, total_orders, last_order_date

### 4. Import Workflows
Import all 12 workflow JSON files into n8n. Update webhook paths (all prefixed `ecomm-ai/`).

### 5. Configure Vapi Assistant
Create a Vapi assistant for COD confirmation with your business script, voice, and language settings.

## Use Cases

1. **COD-heavy eCommerce** (South Asia, Middle East, Africa) — Confirm orders before shipping
2. **High-ticket items** — Voice confirmation for orders above threshold
3. **Subscription businesses** — Renewal confirmation calls
4. **B2B order confirmation** — Verify large purchase orders
5. **Appointment businesses** — Confirm bookings (dentists, salons, clinics)

## Revenue Potential

- **For store owners**: Reduce fake orders by 30-50%, saving $1,000-10,000+/month
- **As a service**: Charge $500-2,000/month per client for managed voice confirmation
- **Per-call pricing**: $0.50-2.00 per successful confirmation call

## Customization

- **Voice**: Change Vapi assistant for different languages/accents
- **Script**: Customize confirmation dialogue in Vapi dashboard
- **Channels**: Enable/disable WhatsApp, SMS, Email fallbacks
- **Retry logic**: Configure max attempts and intervals
- **Reporting**: Customize daily report metrics and recipients

## Requirements

- n8n v2.4+ (self-hosted recommended for webhook reliability)
- Vapi.ai account ($0.05-0.10 per minute of voice)
- Twilio account ($0.0075 per SMS)
- Google Sheets API credentials
- Shopify/WooCommerce webhook access
