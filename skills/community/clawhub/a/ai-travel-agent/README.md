# AI Travel Agent

A personal travel planning assistant for OpenClaw. Searches real flights and hotels, plans multi-stop itineraries, and integrates with your calendar.

## What it does

- Searches flights via Google Flights (through SerpAPI)
- Searches hotels via Google Hotels (through SerpAPI)
- Searches ground transport/trains/ferries via Google Maps Directions (through SerpAPI)
- Plans multi-stop itineraries with day-by-day routes
- Suggests destinations based on season and vibe
- Checks your calendar for free windows (optional)
- Creates calendar events when your trip is confirmed (optional)
- **Does NOT book travel** — provides results and booking links only

## Requirements

### SerpAPI key (required)

This skill uses [SerpAPI](https://serpapi.com) to query Google Flights, Google Hotels, and Google Maps Directions. You need your own API key.

- **Free tier:** 100 searches/month (enough for light use; multi-stop trips use more)
- **Sign up:** https://serpapi.com

Store your key in one of these files:

```
~/.serpapi_credentials   →  SERPAPI_KEY=your_key_here
~/.travel_agent_config   →  SERPAPI_KEY=your_key_here
```

These are the **only** local files the skill reads. If neither exists, the skill will ask you where to find the key.

### Calendar skill (optional)

If you have `google-calendar`, `outlook-calendar`, or a similar calendar skill installed, the travel agent can:
- Check your availability when you don't have fixed travel dates
- Add confirmed trip events to your calendar

Calendar access is **never used silently** — it's only triggered when you ask for date suggestions or want to save your trip.

## External services

| Service | Purpose | Domain |
|---------|---------|--------|
| SerpAPI | Flight, hotel, and transport search | `serpapi.com` |

No other external requests are made. Your SerpAPI key is used directly and is not transmitted anywhere else.

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Full instructions for the AI agent |
| `scripts/search_flights.py` | Queries Google Flights via SerpAPI |
| `scripts/search_hotels.py` | Queries Google Hotels via SerpAPI |
| `scripts/search_transport.py` | Queries Google Maps Directions via SerpAPI |
| `references/serpapi.md` | SerpAPI parameter reference |
| `references/seasonal-destinations.md` | Destination/season guidance |
| `references/multi-stop-routes.md` | Regional multi-stop itinerary templates |

## License

MIT-0 — free to use, modify, and redistribute. No attribution required.
