---
version: "1.0.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
description: "Manage a local key-value cache store using bash and Python. Use when caching API responses, session data, or computed results with TTL support."
---

# Cache — Local Key-Value Cache Manager

A lightweight, file-backed key-value cache with TTL (time-to-live) support, search, bulk import/export, and statistics. Ideal for caching API responses, computed results, or any ephemeral data that benefits from quick local retrieval.

## Prerequisites

- Python 3.6+
- Bash 4+

## Data Storage

Cache entries are stored in `~/.cache-tool/data.jsonl` (note: uses `cache-tool` to avoid conflicts with `~/.cache`). Each line is a JSON object with fields: `key`, `value`, `ttl`, `created_at`, `expires_at`, `tags`, etc.

Configuration lives in `~/.cache-tool/config.json`.

## Commands

Run via: `bash scripts/script.sh <command> [options]`

| Command | Description |
|---|---|
| `set` | Store a key-value pair with optional TTL and tags |
| `get` | Retrieve the value for a given key |
| `delete` | Remove a key from the cache |
| `list` | List all cache entries (with optional tag filter) |
| `flush` | Delete all cache entries or those matching a pattern |
| `ttl` | Check or update the TTL for an existing key |
| `stats` | Show cache statistics (size, hit/miss ratio, memory) |
| `export` | Export the cache to a JSON file |
| `import` | Import cache entries from a JSON file |
| `search` | Search keys or values by substring or regex |
| `config` | View or update cache settings (default TTL, max size) |
| `help` | Show usage information |
| `version` | Print the tool version |

## Usage Examples

```bash
# Set a simple key-value pair
bash scripts/script.sh set --key api_response --value '{"status":"ok"}' --ttl 3600

# Set with tags
bash scripts/script.sh set --key user:42 --value '{"name":"Kelly"}' --tags user,profile

# Get a value
bash scripts/script.sh get --key api_response

# Delete a key
bash scripts/script.sh delete --key old_data

# List all entries
bash scripts/script.sh list

# List entries by tag
bash scripts/script.sh list --tag user

# Check remaining TTL
bash scripts/script.sh ttl --key api_response

# Update TTL
bash scripts/script.sh ttl --key api_response --set 7200

# Flush all entries
bash scripts/script.sh flush

# Flush by pattern
bash scripts/script.sh flush --pattern "user:*"

# Search by key pattern
bash scripts/script.sh search --query "api_" --field key

# Show cache stats
bash scripts/script.sh stats

# Export cache
bash scripts/script.sh export --output cache_backup.json

# Import cache
bash scripts/script.sh import --input cache_backup.json

# Configure defaults
bash scripts/script.sh config --set default_ttl=3600 --set max_entries=10000
```

## Notes

- Expired entries are lazily cleaned: they are skipped on `get` and purged during `flush` or `stats`.
- The `search` command supports both simple substring matching and Python regex patterns.
- `import` merges entries; existing keys are overwritten.
- `stats` reports total entries, expired count, active count, and approximate data size.

## Output Format

`get` returns the raw value to stdout. All other commands return JSON objects with status and metadata.

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
