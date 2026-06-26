---
name: Multi-API Data Pipeline to Google Sheets
description: Connects multiple REST APIs, fetches and transforms data, and pushes it to a live Google Sheets dashboard that auto-updates on a schedule.
version: 1.0.2
tags: [python, api, automation, google-sheets, pipeline, dashboard, data]
author: neo1307
requires: [python3, requests, pandas, gspread, google-auth-oauthlib]
---

# Multi-API Data Pipeline to Google Sheets

## Overview
Automated data pipeline that pulls from multiple REST APIs, transforms and
merges the data, and pushes it to a Google Sheets dashboard that updates
automatically on your chosen schedule (every 15 minutes, hourly, daily).
Replaces hours of manual copy-paste work.

## What It Does
- Connects to up to 10 REST APIs simultaneously
- Handles authentication: API keys, Bearer tokens, OAuth2
- Transforms and merges data across sources
- Pushes clean, formatted data to Google Sheets in real time
- Sends alert if any API call fails
- Logs all pipeline runs with success/failure status

## Required Environment Variables
Set these in OpenClaw's Secrets manager before running:

| Variable | Description |
|----------|-------------|
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Google Service Account key (full JSON string) |
| `TARGET_SHEET_ID` | Google Sheets document ID (from the sheet URL) |
| `[SERVICE]_API_KEY` | One secret per connected API, e.g. `SHOPIFY_API_KEY`, `HUBSPOT_TOKEN` |

## Setup
1. Create a Google Service Account, download the JSON key, paste it as `GOOGLE_SERVICE_ACCOUNT_JSON`
2. Share your target Google Sheet with the service account email
3. Set `TARGET_SHEET_ID` from the sheet URL
4. Add one secret per API you want to connect
5. Set update schedule: `every 15 minutes` / `hourly` / `daily at 06:00`

## Usage
> "Connect Shopify and HubSpot APIs and sync sales data to my Google Sheet every hour"
> "Pull weather data and stock prices into a live dashboard"
> "Set up a pipeline from our internal API to Google Sheets, update every 15 minutes"
> "Add Stripe revenue data to the existing pipeline"

## Output
- Live Google Sheets dashboard with latest data
- Pipeline run log: `logs/pipeline_YYYY-MM-DD.txt`
- Alert on failure with error details

## Rules
- Never store raw API credentials in output files or logs
- Always validate API response schema before writing to Sheets
- If Google Sheets write fails, buffer data locally and retry up to 3 times
- Respect API rate limits — add delays per API documentation
- Each pipeline run must write a summary row to a `_run_log` tab in the Sheet
