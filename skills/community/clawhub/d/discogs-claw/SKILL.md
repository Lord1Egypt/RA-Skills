---
name: discogs-claw
description: Search for vinyl record prices on Discogs using curl. Retrieves Low, Median, and High price suggestions based on condition.
metadata: {"clawdbot":{"emoji":"💿","requires":{"bins":["jq","curl"]}}}
---

# Discogs Claw

Search for vinyl record prices on Discogs using the Discogs API.

## Setup

### Option 1: Environment Variable (Recommended)

```bash
export DISCOGS_TOKEN="your_discogs_token_here"
```

### Option 2: Config file
Located on ~/.openclaw/credentials/discogs.json or /data/.openclaw/credentials/discogs.json

```json
{
  "DISCOGS_TOKEN": "your_discogs_token_here"
}
```

## Usage

### Run the Skill

The skill accepts a JSON input containing the search query.

```bash
# Example search
echo '{"query": "Daft Punk - Random Access Memories"}' | ./scripts/discogs.sh
```

## Example Output
This is an example json output after running the script:

```json
{
  "title": "Daft Punk - Random Access Memories",
  "prices": {
    "low": "25.00 USD",
    "median": "35.00 USD",
    "high": "60.00 USD"
  },
  "marketplace": {
    "num_for_sale": 150,
    "lowest_price": "22.50 USD"
  }
}
```

With this data the agent should output a very objective response containing only the data abvoe and ignoring further historical details about the record. Just the title with artist and pricing information. It should ever use emojis.

## Requirements

- `curl`
- `jq`
- Discogs API Token (`DISCOGS_TOKEN`)

