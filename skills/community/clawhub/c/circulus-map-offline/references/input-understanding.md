# Input understanding guide

Use this guide before calling `map.solve_query` or authoring `MapSpecV1` when the user's route wording is casual, ambiguous, or malformed.

## Normalize common route phrasing

Prefer converting user wording into a compact route query only after preserving the user's intended endpoints and modifiers.

| User phrasing | Normalize toward | Notes |
| --- | --- | --- |
| `JFK to LHR`, `JFK-LHR`, `JFK/LHR` | `JFK-LHR` | Treat airport-pair punctuation as route separators. |
| `from New York to London` | search first, then likely `JFK-LHR` or city candidates | City names are ambiguous; search before choosing airports. |
| `show me SFO via HNL to Tokyo` | `SFO-HNL-TYO` or resolved airport sequence | Keep explicit via points in order. |
| `800nm around DEN`, `800 nm @ Denver` | `800nm@DEN` after resolving Denver | Preserve range unit and center. |
| `polar route ORD to DEL` | `ORD-DEL` plus polar/dateline note if solver output indicates it | Do not force projection manually unless asked. |

## Airport codes vs city names

- Treat three-letter uppercase tokens as possible IATA airport/city codes, but verify with `map.search_locations` if the code is uncommon, overloaded, or used in a sentence as a word.
- For city names with multiple major airports, call `map.search_locations` and either:
  - choose the best match only when the user named a specific airport/city code, or
  - ask one concise clarification when multiple airports would materially change the route.
- Preserve user-visible names in the response: "I resolved London to LHR" is better than silently changing the request.

## Malformed or ambiguous input feedback

When route parsing fails, do not just say the route is invalid. Give the user the smallest fix that would make it solvable.

Good feedback patterns:

- "I need at least two route points. Try `JFK-LHR` or `New York to London`."
- "`LON` can mean the London city area rather than a single airport. Should I use LHR, LGW, or LCY?"
- "I found `800nm` but no center airport. Try `800nm@DEN`."
- "I can keep the via point, but I need it in route order: origin → via → destination."

## Solve order

1. Extract route intent: airport pair, multi-stop route, range ring, ETOPS/projection/export modifier.
2. Normalize separators and units without changing endpoints.
3. Use `map.search_locations` for ambiguous city names or uncertain codes.
4. Use `map.solve_query` for simple route/range requests.
5. Use `map.solve_spec` only when the user asks for projection, ETOPS, labels, markers, or multiple paths.
6. Echo important resolution choices before final export or SVG rendering.
