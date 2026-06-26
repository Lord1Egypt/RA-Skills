# Query Normalization

Use this reference before calling local All Routes APIs or MCP tools when the user gives natural phrasing instead of exact codes.

## Normalization Order

1. Extract intent first: airport lookup, routes from an origin, routes between origin/destination, airline route map, timetable context, or dataset health.
2. Normalize aliases into canonical query fields before choosing an endpoint.
3. Preserve user filters separately from location or airline text so they can be acknowledged later.
4. If a term can mean multiple entities, ask one focused disambiguation question instead of guessing.

## Airport and City Aliases

Treat common city or airport phrasing as candidates, not final truth, unless the API lookup confirms the code.

| User phrase | Try first | Notes |
| --- | --- | --- |
| `nyc`, `New York`, `New York City` | `JFK`, `LGA`, `EWR` | Ambiguous city cluster. Ask which airport or search all NYC-area airports if the user asks broadly. |
| `London` | `LHR`, `LGW`, `STN`, `LCY`, `LTN` | Ask for airport unless the user says Heathrow/Gatwick/etc. |
| `Paris` | `CDG`, `ORY` | City route searches may need both candidates. |
| `Tokyo` | `HND`, `NRT` | Ask for airport unless the user says Haneda/Narita. |
| `LA`, `Los Angeles`, `LAX` | `LAX` | Usually safe to normalize to LAX for airport route queries. |
| `SF`, `San Francisco`, `SFO` | `SFO` | Usually safe to normalize to SFO for airport route queries. |
| `DC`, `Washington DC` | `DCA`, `IAD`, `BWI` | Ambiguous metro area; ask or search all if broad. |
| `Bay Area` | `SFO`, `OAK`, `SJC` | Region phrase; keep as a multi-airport candidate set. |
| `South Florida`, `Miami area` | `MIA`, `FLL`, `PBI` | Region phrase; keep as a multi-airport candidate set. |

## Airline and Alliance Aliases

Normalize airline names and alliance wording before calling airline-specific or filtered route endpoints.

| User phrase | Canonical candidate | Notes |
| --- | --- | --- |
| `American`, `American Airlines` | `AA` | Airline route map or route filter. |
| `United`, `United Airlines` | `UA` | Airline route map or route filter. |
| `Delta`, `Delta Air Lines` | `DL` | Airline route map or route filter. |
| `British Airways`, `BA` | `BA` | Airline route map or route filter. |
| `Qatar`, `Qatar Airways` | `QR` | Airline route map or route filter. |
| `Emirates` | `EK` | Airline route map or route filter. |
| `Singapore Airlines`, `SIA` | `SQ` | Airline route map or route filter. |
| `Lufthansa` | `LH` | Airline route map or route filter. |
| `Star Alliance`, `star` | `star` | Use the `alliance` query parameter when supported. |
| `oneworld`, `one world` | `oneworld` | Use the `alliance` query parameter when supported. |
| `SkyTeam`, `sky team` | `skyteam` | Use the `alliance` query parameter when supported. |

## Ambiguity Fallback Guidance

When ambiguity remains after lookup candidates are identified, do not silently pick one. Use a concise fallback like:

- `“London can mean several airports (LHR, LGW, STN, LCY, LTN). Should I search Heathrow only, or all London-area airports?”`
- `“NYC spans JFK, LGA, and EWR. I can search all three for city-level coverage, or focus on one airport.”`
- `“Washington DC could be DCA, IAD, or BWI. Which airport should I use?”`

If the user asks a broad city/region question, it is acceptable to query multiple candidate airports, but say that a city/region candidate set was applied.

## Applied Filter Acknowledgement

When normalized terms affect the query, include a short `Applied:` line in the answer. Examples:

- `Applied: origin city “NYC” expanded to JFK/LGA/EWR; nonstop only.`
- `Applied: airline “American” normalized to AA; alliance filter left as all.`
- `Applied: city pair London → Tokyo expanded to London-area and Tokyo-area airport candidates; live endpoint availability may require per-airport follow-up.`

## Safe Failure Mode

If local airport or airline lookup cannot confirm an alias:

1. State the unresolved phrase.
2. Offer the most likely exact-code reformulation.
3. Ask for one clarification only.

Example: `“I couldn’t confirm ‘Portland’ from local data. Did you mean PDX (Portland, Oregon) or PWM (Portland, Maine)?”`
