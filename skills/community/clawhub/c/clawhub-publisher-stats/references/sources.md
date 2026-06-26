The bundled script combines two public sources:

1. `https://topclawhubskills.com/`
   - Used to parse the Top Authors table and retrieve publisher aggregate metrics:
     - rank
     - published skill count
     - total downloads
     - total stars

2. `https://topclawhubskills.com/api/search?q=<handle>&limit=<n>`
   - Used to retrieve searchable per-skill rows for a publisher.
   - Important: this result set may be capped and may not equal the aggregate author skill count.

3. `https://clawhub.ai/<handle>/<slug>`
   - Used to extract embedded per-skill stats from public skill pages:
     - downloads
     - installsCurrent
     - installsAllTime
     - stars
     - comments

Known limitation:
- A separate user rating score is not currently exposed on the public pages sampled for this skill.
