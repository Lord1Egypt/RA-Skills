# Automation Roadmap

## Current practical scope

This skill is strongest today in a **review-first** workflow:
- import comment batch
- classify intent
- generate public replies
- generate optional DM follow-up copy
- separate safe replies from manual-review replies

## Recommended automation maturity levels

### Level 1: Draft-only
- export comments manually
- run batch draft generation
- review and paste replies manually

### Level 2: Semi-automatic
- export comments
- generate reply JSON / sheet
- operator reviews high-risk items
- approved replies are pasted through browser automation

### Level 3: Controlled auto-reply
- only for low-risk FAQs and engagement comments
- use approval rules and keyword blacklist
- keep sent-reply logs
- sample replies regularly to avoid robotic drift

## Must-have safeguards before execution automation

- keyword blacklist
- escalation list
- manual review queue for skepticism / support / pricing conflict
- duplicate reply suppression
- per-video rate limits
- sent reply log with timestamp and comment id

## Good first integration points

- CSV export from comment management tool
- browser automation for approved replies
- Google Sheets / Airtable approval layer
- CRM tagging for lead comments

## Current browser execution layer

This skill now includes a basic executor:
- `scripts/browser_reply_runner.py`

It expects:
- a drafts JSON file
- comment management URL
- one selector for the reply box
- one selector for the submit button

It is intentionally conservative:
- skips `public_reply_review` unless forced
- supports `--dry-run`
- writes a sent log after execution

Use it as a semi-automatic layer first, not blind full automation.
