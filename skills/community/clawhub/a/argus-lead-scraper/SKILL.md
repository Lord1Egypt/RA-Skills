---
name: B2B Lead Generation Scraper
description: Extracts verified B2B leads (name, email, company, LinkedIn, job title) from target sources and exports them as CRM-ready CSV files.
version: 1.0.2
tags: [python, scraping, lead-generation, b2b, linkedin, csv, crm, automation]
author: neo1307
requires: [python3, selenium, webdriver-manager, pandas, requests, chromium]
---

# B2B Lead Generation Scraper

## Overview
Automated lead extraction tool that collects verified B2B contact data from
target sources and delivers clean, CRM-ready CSV files. Delivers 500-2,000+
leads per run depending on target criteria.

## What It Does
- Extracts: Full name, job title, company name, LinkedIn URL, email (when available)
- Filters by: industry, job title keywords, company size, location
- Deduplicates records automatically
- Outputs clean CSV ready for HubSpot, Salesforce, Pipedrive import
- Validates and removes junk/incomplete rows before delivery

## Required Environment Variables
Set these in OpenClaw's Secrets manager before running:

| Variable | Description |
|----------|-------------|
| `LI_SESSION` | LinkedIn session cookie (`li_at` value from your browser) |

## Setup
1. Log into LinkedIn in your browser, copy the `li_at` cookie value
2. Set `LI_SESSION` in OpenClaw Secrets
3. Define target criteria in OpenClaw chat (industry, job title, location, company size)
4. Chromium must be available on the host for Selenium headless mode

## Usage
> "Find 500 B2B leads: SaaS CEOs in the United States"
> "Scrape marketing directors at companies with 50-200 employees in London"
> "Generate a lead list of HR managers in healthcare companies"
> "Export leads to CSV formatted for HubSpot import"

## Output
- `leads_YYYY-MM-DD_[criteria].csv` with columns:
  - first_name, last_name, full_name, job_title, company, linkedin_url, email, location
- Summary: total found, duplicates removed, validation pass rate

## Rules
- Never scrape more than 200 profiles per hour to avoid detection
- Always deduplicate by LinkedIn URL before saving
- Mark rows with missing email as `email_status: not_found` — do not fabricate
- Save raw data before cleaning in `data/raw/`
- Output CSV must be UTF-8 encoded for CRM compatibility
