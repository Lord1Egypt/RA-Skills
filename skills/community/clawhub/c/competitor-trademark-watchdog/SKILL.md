---
name: competitor-trademark-watchdog
description: Watch companies and brands at the USPTO and get alerted when a watched owner files a new trademark application. Use when the user wants trademark filing alerts, competitor brand monitoring, a heads-up before a rival launches a product name, or an ad-hoc check of a company's recent filings. Runs the magnova/uspto-trademark-search Actor through the Apify plugin for OpenClaw; each trademark record costs $0.004 on the user's own Apify account.
version: 1.0.0
homepage: https://apify.com/magnova/uspto-trademark-search
metadata:
  openclaw:
    requires:
      env:
        - APIFY_API_TOKEN
---

# Competitor Trademark Watchdog

Companies usually file a trademark months before a product,
brand, or rebrand becomes public. This skill keeps a watchlist
of owners at the USPTO and alerts the user when one of them
files a new application — the filing's name, class, and date,
with a link to the official record.

## Prerequisites

1. The Apify plugin for OpenClaw is installed and allowlisted:
   `openclaw plugins install @apify/apify-openclaw-plugin`
2. `APIFY_API_TOKEN` holds the user's own Apify API token. All
   runs bill to that account.
3. You call Actors through the plugin's `apify` tool: `start`
   (returns a runId), then `collect` (returns the results).

If the plugin or token is missing, stop and tell the user
exactly what to install or set. Do not search the USPTO website
yourself and do not substitute another source.

**Cost, stated plainly:** the Actor charges $0.004 per
trademark record returned, no start fee. A weekly check of a
10-company watchlist normally costs a few cents; a company
that filed nothing costs nothing for that check.

## Setup (first run only)

Ask the user for the watchlist: company or owner names exactly
as they appear on trademark filings (legal names work best,
e.g. "Nike, Inc."). Also ask one question:

- **Backfill or start fresh?** Default: start fresh — the
  baseline is today and only future filings alert. If they ask
  for backfill, run the first check with `filedAfter` 90 days
  back and present it as a one-time recent-filings report;
  those filings are then part of the seen list.

Save the answers in the state file.

## State

Keep one JSON file at `state/competitor-trademark-watchdog.json`
in the workspace:

```json
{
  "watchlist": ["Nike, Inc.", "Anthropic, PBC"],
  "lastCheckDate": "2026-11-17",
  "seenSerialNumbers": ["99711442"]
}
```

Keep at most the last 5,000 serial numbers; the filedAfter
cursor is the primary dedupe, the list is the backstop.

## Check procedure

1. Read the state file. If none exists, do Setup.
2. For each owner on the watchlist, start the Actor with the
   `apify` tool:
   - actorId: `magnova~uspto-trademark-search`
   - input: `owner`: the watchlist name, `filedAfter`: the
     day after `lastCheckDate`, `status`: "any",
     `maxResults`: 100.
3. Collect each run's results. Ignore rows whose `recordType`
   is not a trademark record (SUMMARY / ERROR rows are not
   filings).
4. Drop any record whose `serialNumber` is already in
   `seenSerialNumbers`.
5. Alert on what remains (format below) — one alert per new
   filing, sent before the state file is updated, so a crash
   can never lose an alert silently.
6. Only after all alerts are delivered, append the new serial
   numbers and set `lastCheckDate` to today. If any owner's
   run failed, do not advance that owner's window — note the
   failure in your summary and let the next check retry it.

## Alert format

```
™️ New trademark filing — <owner>
Mark: <wordmark>
Filed: <filedDate> · Status: <status> · Classes: <internationalClasses>
Covers: <goodsAndServices, trimmed to one line>
Official record: <tsdrUrl>
```

- If a whole check finds nothing new across the watchlist,
  send one line: "No new trademark filings from your
  watchlist this week." Nothing else.
- Report the filing exactly as returned. A new filing is a
  fact; what it means (a launch, a rebrand, a conflict with
  the user's own marks) is the user's call — do not present
  guesses as findings, and never call a mark "safe",
  "infringing", or "clear". This is public USPTO data, not
  legal advice.

## Ad-hoc checks

The same Actor answers one-off questions without touching the
watchlist or the schedule:

- "What has <company> filed recently?" — run an `owner`
  search with `filedAfter` set as the user asks.
- "Has anyone filed <brand name>?" — run a `wordmark` search.
- "Look up serial <8 digits>" — run a `serialNumber` search.

Present results in the same field order as the alert format.

## Scheduling

Offer a recurring weekly check (for example Mondays 09:00 in
the user's timezone) using OpenClaw's scheduler. Trademark
filings move slowly; daily checks are available on request
but rarely add anything. The user can add or remove watchlist
names in chat at any time; re-read the state file at the
start of every check.
