---
name: alibaba-store-analysis
description: Alibaba International Station weekly business report analysis skill. Retrieves store weekly report data via browser session, validates, and presents structured diagnostics with on-demand deep report access.
version: "1.0.0"
---


# Alibaba Store Analysis Skill

## Overview

This skill automates the retrieval and analysis of Alibaba International Station weekly business reports. It logs in via a browser, pulls summary data, validates it, displays key metrics and diagnostics, and optionally fetches the full report for on‑demand queries.

## Core Workflow (high‑level)
1. **Login Check** – Open `https://i.alibaba.com/`. If redirected to the login page, prompt the user to log in and wait until the session is authenticated.
2. **Fetch Summary Data** – Call `diagnoseData.json` API and obtain `encryptedReportId`, `receipt` and diagnostic arrays.
3. **Validate Data** – Silent checks for empty response, missing `encryptedReportId` or `receipt`. On failure, display a friendly fallback message and stop.
4. **Display Summary** – Render four sections in one output:
   - Store data overview (metrics table)
   - Diagnostic summary text
   - Merchant task list
   - Link to the weekly report using `encryptedReportId`.
5. **Full Report Retrieval** – Using the `receipt` token, call `queryWeekReportAllData.json` to obtain the detailed report. Validate silently; on success announce *"Full data analysis complete. Feel free to ask me any questions about your store data!"* and wait for user queries.

## Usage
```sh
openclaw run alibaba-store-analysis
```
The skill will guide the user through any required login steps and then output the analysis automatically.

For the complete step‑by‑step workflow, API payloads, error handling and module explanations, see `references/workflow.md`.


---

**Created by [Simon Cai](https://github.com/simoncai519) · More e-commerce skills: [github.com/simoncai519/open-accio-skill](https://github.com/simoncai519/open-accio-skill)**
