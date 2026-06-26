# Fleece — Credit Card Research CLI

Fleece is a CLI for live US credit card research and award redemption. Use it whenever the user asks about credit cards, rewards, transfer partners, MCC codes, or award flights/hotels.

## Install

```bash
pip install fleece-cli
export BRAVE_API_KEY=<key>   # required for research commands
```

## When to invoke Fleece

- "What are the benefits of [card]?" → `fleece card "<name>" --json`
- "Which card earns most on [category]?" → `fleece rates "<name>" --category <cat> --json`
- "What cards can I transfer Chase points to?" → `fleece partners "<name>" --json`
- "What credits does [card] have?" → `fleece credits "<name>" --json`
- "Compare [card A] vs [card B]" → `fleece compare "<A>" "<B>" --json`
- "Analyze my wallet" → `fleece wallet --json`
- "Is [card] worth it for me?" → `fleece roi "<name>" --json`
- "What's the best card for my spending?" → `fleece recommend "<profile>" --json`
- "What card should I use at [merchant]?" → `fleece mcc <code> --wallet --json`
- "Find business class flights JFK to NRT" → `fleece flights JFK NRT --date <YYYY-MM-DD> --cabin business --open`
- "Search hotels in Tokyo" → `fleece hotels "Tokyo" --checkin <date> --checkout <date> --open`
- "What is my spending profile?" → `fleece profile show --json`

## Key facts

- All commands output JSON with `--json` — parse `result` field, check `ok` before using
- `mcc`, `flights`, `hotels`, and `profile` work **offline** — no API key needed
- `fleece wallet` auto-loads saved cards from `fleece.db` with no arguments
- Spending profile auto-enriches `wallet`, `roi`, and `recommend` once set

## Common MCCs

| MCC | Category |
|---|---|
| 5411 | Grocery Stores |
| 5812 | Restaurants |
| 5541 | Gas Stations |
| 4511 | Airlines |
| 7011 | Hotels |
| 4111 | Transit |
| 5912 | Drugstores |
