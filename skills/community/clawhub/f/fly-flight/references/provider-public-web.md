# Public Web Provider Notes

Provider: Tongcheng public flight pages

- Site: `https://www.ly.com/flights/`
- Route URL shape: `https://www.ly.com/flights/itinerary/oneway/<FROM>-<TO>?date=<YYYY-MM-DD>`
- Example: `https://www.ly.com/flights/itinerary/oneway/BJS-SHA?date=2026-03-20`

How this skill works:

- Fetch the public HTML page
- Extract `window.__NUXT__`
- Read `state.book1.flightLists`
- Normalize public route, airport, time, and fare fields

Important limitations:

- No API key is required
- Prices are public-page reference prices, not guaranteed checkout prices
- The scraper depends on Tongcheng HTML and page payload structure
- If Tongcheng changes the page or adds stronger anti-bot checks, this skill can fail
- Public site availability and rate limits are outside the skill's control
