# Booking Hotel Search — OpenClaw Skill

Search Booking.com in real time for hotel availability, prices, rooms, and deals in any destination worldwide.

## What It Does

This skill lets an OpenClaw agent search for hotels and check availability on your behalf by calling the Booking Live API. It supports:

- **Destination search** — Find hotels in any city or region with dates and guest count
- **24+ filters** — Free cancellation, breakfast, star rating, amenities, review scores, and more
- **Budget filtering** — Set a max budget per night
- **Hotel details** — Get detailed room types, meal plans, and pricing for a specific hotel
- **Bulk comparison** — Compare up to 5 hotels side-by-side in one request
- **Name resolution** — Look up any hotel by name to get its Booking.com ID

The agent will ask for your travel details, call the API, and present the results in a clear, comparable format with direct Booking.com links.

## Requirements

You need a **RapidAPI key** with an active subscription to the [Booking Live API](https://rapidapi.com/mtnrabi/api/booking-live-api).

A **free tier** is available — no credit card required to get started.

### Setup

1. Go to [Booking Live API on RapidAPI](https://rapidapi.com/mtnrabi/api/booking-live-api)
2. Click **Subscribe** and select the Free plan (or a paid plan for higher limits)
3. Copy your RapidAPI key from the dashboard
4. Configure it in OpenClaw:

```json5
// ~/.openclaw/openclaw.json
{
  "skills": {
    "entries": {
      "booking-hotel-search": {
        "enabled": true,
        "apiKey": "YOUR_RAPIDAPI_KEY_HERE"
      }
    }
  }
}
```

Or set the `RAPIDAPI_KEY` environment variable.

## How to Use

Just ask your OpenClaw agent to search for hotels in natural language:

- *"Find me a hotel in Paris for May 1-5"*
- *"Search hotels in Tokyo with breakfast included, under $150/night"*
- *"Compare the Ritz Paris, Four Seasons George V, and Le Meurice for next weekend"*
- *"What rooms are available at the Ritz Paris for June 10-14?"*

The agent will determine the right endpoint, build the request, call the API, and present results with booking links.

## Examples

### Destination search

> **You:** Find hotels in Rome for June 10-14, 2 adults, with free cancellation and breakfast
>
> **Agent:** Searching for hotels in Rome...
>
> Here are the top results:
> | Hotel | Price (4 nights) | Per Night | Rating | Location |
> |-------|-----------------|-----------|--------|----------|
> | Hotel Artemide | €520 | €130 | 9.1 (3,204 reviews) | Via Nazionale |
> | Hotel Raphael | €680 | €170 | 8.8 (1,856 reviews) | Piazza Navona |
> | Roma Luxus Hotel | €440 | €110 | 9.0 (2,100 reviews) | Via Cavour |

### Hotel comparison

> **You:** Compare the Ritz Paris and Four Seasons George V for May 1-5
>
> **Agent:** Comparing hotels...
>
> | | Ritz Paris | Four Seasons George V |
> |---|---|---|
> | Price (4 nights) | €3,200 | €2,800 |
> | Rating | 9.3 (1,245 reviews) | 9.1 (987 reviews) |
> | Room | Deluxe Room | Superior Room |

## Permissions

This skill requires **`network:outbound`** to make HTTPS POST requests to the Booking Live API hosted on RapidAPI. This is the only external communication the skill performs. No other network access is needed or used.

| Permission | Reason |
|------------|--------|
| `network:outbound` | Required to call `booking-live-api.p.rapidapi.com` (the only endpoint this skill contacts) |

## Security

- **Single endpoint only.** This skill communicates exclusively with `https://booking-live-api.p.rapidapi.com`. No other external services, domains, or IPs are contacted.
- **No data storage.** Hotel search results are returned directly to the agent and presented to the user. No data is stored, cached, logged, or forwarded anywhere.
- **No code execution.** This skill contains only instructions for the AI agent — no scripts, no `eval`, no dynamic code execution.
- **API key handling.** Your RapidAPI key is read from the `RAPIDAPI_KEY` environment variable (or `skills.entries.booking-hotel-search.apiKey` in config) and sent only in the `x-rapidapi-key` header to RapidAPI's servers. It is never logged, stored, or sent elsewhere.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `403 Forbidden` | Your RapidAPI key is missing or invalid. Check the `RAPIDAPI_KEY` env var. |
| `429 Too Many Requests` | You've exceeded your plan's rate limit. Upgrade your RapidAPI plan or wait. |
| `No hotels found` | Try a different destination spelling, or broaden your filters/budget. |
| `Hotel not found by name` | The hotel name may not match Booking.com's listing. Try a more specific or official name. |
| `502 error` | Temporary issue with the API backend. Retry after a moment. |

## Support

- API issues: [Booking Live API on RapidAPI](https://rapidapi.com/mtnrabi/api/booking-live-api)
- Skill issues: Open an issue on the skill's ClawHub page
