---
name: fuelwatch
description: Build, deploy, and extend the FuelWatch crowdsourced fuel availability tracker for South Africa. Use when working on FuelWatch features, fixing bugs, deploying updates, or extending the app with a backend, new UI features, or social sharing.
---

# FuelWatch — Crowdsourced SA Fuel Tracker

## Overview

FuelWatch is a mobile-first web app for tracking diesel/petrol prices and availability at SA fuel stations. Built during the 2026 Iran war / diesel shortage crisis when diesel prices jumped from ~R21 to R28+ and many stations ran dry.

**Live URL:** http://161.97.110.234:8080  
**Files:** `/root/fuelwatch/` (index.html, style.css, app.js)  
**Service:** `systemctl status fuelwatch` (auto-restarts, survives reboots)

## Architecture

- Pure HTML + vanilla JS + CSS (no build step, no framework)
- Data in `localStorage` (prototype — no backend yet)
- Served by Python HTTP server via systemd

## Key Features

- Station list/cards: name, suburb, fuel type, price/L, availability status
- Availability: 🟢 Has Fuel / 🟡 Low Stock / 🔴 Out of Stock
- Reports older than 2 hours flagged ⚠️ Unverified
- ➕ Report form (no login required)
- 📤 Share button (native share or clipboard)
- Search by suburb/station, filter by fuel type, sort by recent/price
- 8 seed reports pre-loaded (clears if localStorage has data)
- XSS-safe (user input escaped before render)

## Extending the app

See `references/backend-plan.md` for the planned Supabase backend.

### Add a new feature

Edit `/root/fuelwatch/app.js` for logic, `style.css` for styling, `index.html` for structure. No build step — changes are live immediately.

### Deploy updates

```bash
# Files are served directly — edit and refresh browser
systemctl status fuelwatch   # check service is running
systemctl restart fuelwatch  # if needed
```

### Add real backend (Phase 2)

- Supabase (free tier): Postgres + REST API + real-time
- Replace localStorage read/write in app.js with fetch() calls
- Add Supabase JS client via CDN script tag
- See references/backend-plan.md

## WhatsApp Reporting Channel (Phase 3)

**Number:** +27822209212 (Stef's spare WhatsApp)

**Concept:** People send WhatsApp text or voice notes to report fuel availability. OpenClaw receives, parses/transcribes, and submits to FuelWatch DB automatically.

**Flow:**
1. User sends: "Shell Edenvale diesel R27.50 has fuel" (or voice note)
2. OpenClaw parses structured data: station / suburb / fuel type / price / availability
3. Auto-inserts into Supabase reports table
4. Web UI updates in real time

**Why:** Truckers + road users → voice note while driving. Zero friction. No app needed.

**Requirements:**
- WhatsApp channel connected to OpenClaw (wacli or WAHA)
- Supabase backend live (Phase 2 first)
- NLP parser for free-text reports (can use LLM extraction)
- Voice transcription: OpenAI Whisper or Groq Whisper

**See:** references/whatsapp-reporting.md (to be written when building Phase 3)

## Marketing plan (when ready to go public)

- Register domain (fuelwatch.co.za or similar)
- Deploy to Vercel (free, `vercel --prod` from /root/fuelwatch)
- Post to: SA Facebook groups (Arrive Alive, Joburg/CT/DBN community groups, trucker groups)
- Tweet: #DieselShortage #FuelCrisis #SouthAfrica — tag @ArrivAlive @MyBroadband
- Comment on IOL/MyBroadband articles about diesel crisis
- Email MyBroadband/CarMag for coverage ("local tool built in response to crisis")

## Competitive context

**myTank.co.za** — existing competitor. Has price comparison, rewards calc. Missing: availability status, no crowdsourcing, requires account to see prices, no crisis mode.

**Our edge:** availability (Has Fuel / Low Stock / Out of Stock) is the killer feature — what people actually need during a shortage.
