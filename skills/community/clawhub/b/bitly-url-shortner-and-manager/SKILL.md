---
name: bitly-url-shortner-and-manager
description: Bitly URL Shortner and Manager for a local Windows OpenClaw workspace. Use when the user wants to log into Bitly with locally stored credentials, validate auth, inspect account/group details, list/search/filter/export existing bitlinks, shorten one or many URLs, inspect long URLs and click metrics, create custom aliases, or prepare short links for X/social posting workflows without exposing secrets inside the published skill.
---

# Bitly URL Shortner and Manager

Use the official Bitly API through a local CLI that reads secrets from a local `.env` file outside the skill folder.

## Local secret storage

Store real credentials in a local env file **outside the skill folder**.

Recommended approaches:
- set `BITLY_ENV_FILE` to point at your local env file
- or export `BITLY_CLIENT_ID`, `BITLY_CLIENT_SECRET`, `BITLY_ACCESS_TOKEN`, and optional `BITLY_DEFAULT_GROUP_GUID` directly in the shell

The skill does **not** need secrets embedded inside the published skill folder.

Example env file shape is documented in:
- `references/env-example.md`

## Quick start

Validate auth:

```powershell
python .\skills\bitly-url-shortner-and-manager\scripts\bitly_manager.py whoami
```

List groups:

```powershell
python .\skills\bitly-url-shortner-and-manager\scripts\bitly_manager.py groups
```

List recent links:

```powershell
python .\skills\bitly-url-shortner-and-manager\scripts\bitly_manager.py bitlinks --limit 10
```

Search/filter links:

```powershell
python .\skills\bitly-url-shortner-and-manager\scripts\bitly_manager.py search --query "etsy" --limit 20 --tag t-shirts
```

Shorten one URL:

```powershell
python .\skills\bitly-url-shortner-and-manager\scripts\bitly_manager.py shorten --long-url "https://example.com/page"
```

Shorten many URLs from a txt file:

```powershell
python .\skills\bitly-url-shortner-and-manager\scripts\bitly_manager.py bulk-shorten --input "C:\path\to\urls.txt" --output "C:\path\to\results.json"
```

Export links for other workflows:

```powershell
python .\skills\bitly-url-shortner-and-manager\scripts\bitly_manager.py export-links --tag t-shirts --format txt --output "C:\path\to\bitly-links.txt"
```

Inspect a bitlink:

```powershell
python .\skills\bitly-url-shortner-and-manager\scripts\bitly_manager.py expand --bitlink "bit.ly/abc123"
```

Get clicks for a bitlink:

```powershell
python .\skills\bitly-url-shortner-and-manager\scripts\bitly_manager.py clicks --bitlink "bit.ly/abc123" --unit day --limit 30
```

## Workflow

1. Set Bitly credentials in shell environment variables.
2. Run `whoami` first when verifying a new setup.
3. Use `groups` if you need the correct `group_guid`.
4. Use `bitlinks`, `search`, and filters to inspect existing links.
5. Use `shorten` or `bulk-shorten` to create new links.
6. Use `export-links` to hand clean link sets to other tools or skills.
7. Feed resulting links into `x-post-prep` or another social workflow.

## Commands

- `whoami` — verify auth and inspect account info
- `groups` — list accessible groups
- `bitlinks --limit N [--query TEXT]` — list recent links in a group
- `search --query TEXT --limit N` — search links by text
- `shorten --long-url URL` — create a new short link
- `expand --bitlink bit.ly/abc123` — inspect an existing bitlink
- `clicks --bitlink bit.ly/abc123` — fetch click metrics
- `create-custom --bitlink bit.ly/abc123 --custom-bitlink yourdomain.com/name` — try to create a custom alias
- `bulk-shorten --input urls.txt` — shorten many URLs from a local txt file
- `export-links --format json|txt|csv --output file` — export filtered link sets
- `env-template` — print or write a local env template

List/search/export commands support filters like:
- `--tag`
- `--domain`
- `--contains`

Many list-style commands also support `--csv` for flatter output.

## OAuth / callback note

For a local desktop-style setup, use:
- `http://127.0.0.1:8765/callback`

Optionally also add:
- `http://localhost:8765/callback`

## Pairing with other skills

This skill pairs naturally with:
- `x-post-prep` for adding short links into prepared post files
- `x-poster` for later scheduling or posting those linked posts

## Resources

### scripts/
- `bitly_manager.py` — local Bitly CLI for account, link, metrics, export, and batch operations

### references/
- `api-notes.md` — Bitly endpoint notes
- `env-example.md` — non-secret example of the local env file shape
example of the local env file shape
