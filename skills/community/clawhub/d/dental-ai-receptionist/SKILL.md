---
name: dental-ai-receptionist
description: Complete AI voice receptionist system for dental practices. 12 workflows covering inbound call routing, appointment booking, reminders, no-show followup, cancellation/waitlist, after-hours capture, patient recall, FAQ handling, staff escalation, CRM sync, daily reports, and SMS reply handling.
tags: [dental, voice-agent, vapi, twilio, appointments, healthcare, receptionist, ai, n8n, automation]
author: mhmalvi
version: 1.2.0
license: CC BY-NC-SA 4.0
metadata:
  clawdbot:
    emoji: "\U0001F9B7"
    requires:
      n8nCredentials: [google-sheets-oauth2, smtp, google-calendar-oauth2, openai, twilio]
      env: [DENTAL_CALL_LOG_SHEET_ID, DENTAL_APPOINTMENTS_SHEET_ID, DENTAL_PATIENTS_SHEET_ID, DENTAL_CALENDAR_ID, DENTAL_CLINIC_NAME, DENTAL_CLINIC_PHONE, DENTAL_CLINIC_EMAIL, DENTAL_CLINIC_ADDRESS, DENTAL_EMERGENCY_PHONE, DENTAL_DENTIST_PHONE, DENTAL_STAFF_EMAIL, DENTAL_OWNER_EMAIL, TWILIO_PHONE_NUMBER, TWILIO_CRED_ID, VAPI_API_KEY, VAPI_API_URL, VAPI_REMINDER_ASSISTANT_ID, VAPI_NOSHOW_ASSISTANT_ID, VAPI_WAITLIST_ASSISTANT_ID, VAPI_RECALL_ASSISTANT_ID, N8N_WEBHOOK_BASE, GOOGLE_CALENDAR_CRED_ID, OPENAI_CRED_ID, HUBSPOT_API_KEY, PMS_API_URL, PMS_API_KEY]
    os: [linux, darwin, win32]
---

# Dental AI Receptionist

A production-ready, 12-workflow AI voice receptionist system for dental practices. Handles inbound calls, appointment booking, reminders, cancellations, waitlist management, patient recall, and staff escalation — fully automated.

## Problem

Dental practices lose revenue from missed calls, no-shows, and manual scheduling overhead. Front desk staff spend 60-70% of their time on phone calls that could be automated. After-hours calls go to voicemail and patients book elsewhere.

This system provides 24/7 AI-powered call handling, automated reminders, and intelligent patient management.

## What It Does

1. **Inbound Call Routing** — AI answers calls, identifies intent (booking, cancellation, FAQ, emergency), routes accordingly
2. **Appointment Booking** — Books appointments with calendar integration and SMS confirmation
3. **Smart Reminders** — Sends 48h, 24h, and 2h reminders to reduce no-shows
4. **No-Show Followup** — Automatically follows up with patients who miss appointments
5. **Cancellation & Waitlist** — Handles cancellations and fills gaps from waitlist
6. **After-Hours Capture** — Captures calls outside business hours for next-day followup
7. **Patient Recall** — Proactive outreach for overdue care (cleanings, checkups)

## Included Workflows

| # | File | Purpose |
|---|------|---------|
| 01 | `01-inbound-call-handler.json` | Call intake, intent classification, business hours routing |
| 02 | `02-appointment-booking.json` | Book appointments, calendar sync, PMS integration |
| 03 | `03-appointment-reminders.json` | Multi-stage reminders (48h, 24h, 2h before) |
| 04 | `04-noshow-followup.json` | Detect no-shows, send followup messages |
| 05 | `05-cancellation-waitlist.json` | Process cancellations, auto-fill from waitlist |
| 06 | `06-after-hours-capture.json` | Capture after-hours calls for next-day callback |
| 07 | `07-patient-recall.json` | Recall campaigns for overdue patients |
| 08 | `08-faq-handler.json` | AI-powered answers to common questions |
| 09 | `09-staff-escalation.json` | AI summary + alert for calls needing human attention |
| 10 | `10-crm-sync.json` | Sync patient data with CRM (HubSpot, PMS) |
| 11 | `11-daily-report.json` | Daily metrics email (calls, bookings, no-shows, etc.) |
| 12 | `12-sms-reply-handler.json` | Process inbound SMS replies from patients |

## Architecture

```
Inbound Call (Vapi AI Voice)
    |
    v
Workflow 01: Intent Classification
    |
    +-- Booking ---------> Workflow 02: Appointment Booking
    |                           |
    |                           v
    |                      Google Calendar + PMS
    |
    +-- Cancellation ----> Workflow 05: Cancel + Waitlist Fill
    |
    +-- FAQ -------------> Workflow 08: AI FAQ Response
    |
    +-- Emergency -------> Workflow 09: Staff Escalation
    |
    +-- After Hours -----> Workflow 06: Capture for Callback
    |
    +-- All Events ------> Workflow 10: CRM Sync
                                |
                                +-> Google Sheets (Call Log, Appointments, Patients)
                                +-> HubSpot CRM (optional)

Scheduled:
+-- Workflow 03: Appointment Reminders (hourly check)
+-- Workflow 04: No-Show Followup (every 2 hours)
+-- Workflow 07: Patient Recall (weekly)
+-- Workflow 11: Daily Report (once daily)
+-- Workflow 12: SMS Reply Handler (webhook-triggered)
```

## Required n8n Credentials

| Credential Type | Used For | Placeholder in JSON |
|----------------|----------|---------------------|
| Google Sheets OAuth2 | Call logs, appointments, patient records | `YOUR_GOOGLE_SHEETS_CREDENTIAL_ID` |
| SMTP (Gmail or custom) | Reminders, reports, notifications | `YOUR_SMTP_CREDENTIAL_ID` |
| Google Calendar OAuth2 | Appointment scheduling | Set via `GOOGLE_CALENDAR_CRED_ID` env |
| OpenAI | FAQ answer generation, call summaries | Set via `OPENAI_CRED_ID` env |
| Twilio | Voice calls, SMS messaging | Set via `TWILIO_CRED_ID` env |

## Environment Variables

```bash
# Google Sheets
DENTAL_CALL_LOG_SHEET_ID=your-sheet-id
DENTAL_APPOINTMENTS_SHEET_ID=your-sheet-id
DENTAL_PATIENTS_SHEET_ID=your-sheet-id

# Google Calendar
DENTAL_CALENDAR_ID=your-calendar-id

# Clinic Details
DENTAL_CLINIC_NAME=Your Dental Practice
DENTAL_CLINIC_PHONE=+1234567890
DENTAL_CLINIC_EMAIL=reception@yourpractice.com
DENTAL_CLINIC_ADDRESS=123 Main St, Your City
DENTAL_EMERGENCY_PHONE=+1234567890
DENTAL_DENTIST_PHONE=+1234567890
DENTAL_STAFF_EMAIL=staff@yourpractice.com
DENTAL_OWNER_EMAIL=owner@yourpractice.com

# Vapi AI Voice
VAPI_API_KEY=your-vapi-key
VAPI_API_URL=https://api.vapi.ai
VAPI_REMINDER_ASSISTANT_ID=your-reminder-assistant-id
VAPI_NOSHOW_ASSISTANT_ID=your-noshow-assistant-id
VAPI_WAITLIST_ASSISTANT_ID=your-waitlist-assistant-id
VAPI_RECALL_ASSISTANT_ID=your-recall-assistant-id

# Twilio
TWILIO_PHONE_NUMBER=+1234567890
TWILIO_CRED_ID=your-n8n-twilio-credential-id

# n8n Infrastructure
N8N_WEBHOOK_BASE=https://your-n8n-instance.com/webhook
GOOGLE_CALENDAR_CRED_ID=your-n8n-google-calendar-credential-id
OPENAI_CRED_ID=your-n8n-openai-credential-id

# Optional (CRM / Practice Management)
HUBSPOT_API_KEY=your-hubspot-key
PMS_API_URL=https://your-pms.com/api
PMS_API_KEY=your-pms-key
```

## Google Sheets Schema

### Call Log
| Column | Type | Description |
|--------|------|-------------|
| call_id | text | Unique call identifier |
| caller_phone | text | Caller's phone number |
| caller_name | text | Patient name (if identified) |
| intent | text | booking / cancellation / faq / escalation / after-hours |
| timestamp | datetime | Call timestamp |
| duration | number | Call duration in seconds |
| summary | text | AI-generated call summary |
| outcome | text | booked / cancelled / answered / escalated / captured |

### Appointments
| Column | Type | Description |
|--------|------|-------------|
| appointment_id | text | Unique ID |
| patient_name | text | Patient full name |
| patient_phone | text | Phone number |
| service_type | text | cleaning / checkup / filling / crown / etc. |
| date | date | Appointment date |
| time | text | Appointment time |
| status | text | confirmed / reminded / completed / no-show / cancelled |
| showed_up | boolean | Whether patient attended |
| reminder_48h | boolean | 48h reminder sent |
| reminder_24h | boolean | 24h reminder sent |
| reminder_2h | boolean | 2h reminder sent |

### Patients
| Column | Type | Description |
|--------|------|-------------|
| patient_phone | text | Primary key |
| patient_name | text | Full name |
| email | text | Email address |
| last_service | text | Most recent service type |
| last_visit | date | Most recent visit date |
| recall_status | text | due / notified / scheduled / completed |
| total_visits | number | Lifetime visit count |

## Quick Start

### 1. Prerequisites
- n8n v2.4+ (self-hosted)
- Vapi.ai account (AI voice calls)
- Twilio account (phone number + SMS)
- Google Sheets OAuth2 credentials
- Google Calendar API access

### 2. Create Sheets
Set up 3 Google Sheets with the schemas above: Call Log, Appointments, Patients. Optionally add Waitlist, Escalations, After-Hours Queue, and Daily Reports sheets.

### 3. Configure Vapi Assistant
Create a Vapi assistant with your dental practice's greeting, business hours, services, and FAQ responses.

### 4. Import Workflows
Import all 12 JSON files into n8n. Replace all `YOUR_*` placeholders and set environment variables.

### 5. Activate
Activate workflows in order: 01 first (inbound handler), then the rest. Test with a phone call to your Vapi number.

## Use Cases

1. **Solo dental practices** — Replace or augment front desk with 24/7 AI receptionist
2. **Multi-location dental groups** — Centralized call handling across clinics
3. **Dental service organizations (DSOs)** — Scalable patient communication
4. **Orthodontic practices** — Long appointment cycles benefit from recall automation
5. **Dental IT providers** — Offer AI receptionist as a managed service to clients

## Revenue Potential

- **For practices**: Reduce missed calls by 80%+, no-shows by 30-50%
- **As a service**: Charge $500-1,500/month per dental practice
- **Per-call pricing**: $1-3 per handled call

## Requirements

- n8n v2.4+ (self-hosted recommended)
- Vapi.ai account ($0.05-0.10 per minute)
- Twilio account ($0.0075 per SMS)
- Google Sheets + Calendar API credentials
- Optional: HubSpot CRM, Dentrix/Eaglesoft/OpenDental PMS
