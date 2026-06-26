# Filter Intelligence

Use this reference after query normalization when the user adds constraints like nonstop preference, alliance preference, region preference, or route direction.

## Filter Extraction Order

1. Identify route intent first: routes from an origin, routes between origin/destination, airline route map, or timetable context.
2. Extract filters separately from entity text so aliases still normalize cleanly.
3. Convert supported filters into local API query parameters where possible.
4. Preserve unsupported or ambiguous filters as visible limitations instead of silently dropping them.
5. Acknowledge every applied filter in the final answer.

## Supported Filter Patterns

| User phrasing | Canonical filter | Local surface guidance |
| --- | --- | --- |
| `nonstop`, `direct`, `no connections` | `maxStops=0` | Use on `/api/routes`; say nonstop-only was applied. |
| `one stop`, `up to one stop` | `maxStops=1` | Use on `/api/routes` when supported by the route search surface. |
| `any stops`, `include connections` | omit `maxStops` unless the user gives a limit | Do not force nonstop defaults unless the task asks for nonstop. |
| `Star Alliance`, `oneworld`, `SkyTeam` | `alliance=star|oneworld|skyteam` | Use on route search when the endpoint supports `alliance`; otherwise state that alliance was interpreted but not applied live. |
| `not alliance-specific`, `all airlines` | `alliance=all` | Use explicit `all` when constructing route URLs that expect an alliance value. |
| `to Europe`, `within Asia`, `US routes` | region preference | Use airport/country/route result fields if available; otherwise describe as a post-filter or limitation. |
| `from X to Y`, `X → Y`, `outbound from X` | direction: origin then destination | Use `/api/routes?origin=X&dest=Y...`. |
| `to X from Y`, `inbound to X from Y` | direction: origin Y, destination X | Do not reverse accidentally; restate direction in `Applied:`. |
| `either direction`, `both ways`, `round trip coverage` | bidirectional check | Query or inspect both origin→dest and dest→origin when possible, or say only one direction was checked. |

## Direction Handling

Route data may be directional. When the user phrase contains both endpoints, preserve the requested direction and echo it back:

- `Applied: direction LAX → JFK; nonstop only; alliance all.`
- `Applied: inbound direction SFO → LHR based on “to London from San Francisco”; Star Alliance filter.`

If the user says `between A and B` without a direction, treat direction as ambiguous. Either ask one concise clarification or check both directions if the user expects broad coverage.

## Region Preference Handling

Region words are filters, not exact airports. Keep them separate from city aliases:

- `Europe`, `EU`, `Schengen`: destination or origin region preference depending on phrasing.
- `Asia`, `Southeast Asia`, `Middle East`, `US`, `domestic`: region/country grouping preference.
- `Bay Area`, `South Florida`, `London area`: location candidate sets from query normalization, not route-result regions.

If the local endpoint cannot enforce a region parameter, apply it as a result interpretation step only when returned fields make that safe. Otherwise include a limitation note such as: `Region preference “Europe” was recognized, but this local route surface does not expose a region filter in the request URL.`

## Applied Filter Acknowledgement

Always include a short `Applied:` line when filters change the lookup. Include unsupported filters too, clearly marked.

Good examples:

- `Applied: origin LAX; nonstop only (maxStops=0); alliance Star Alliance (star).`
- `Applied: direction NYC-area → Tokyo-area; max one stop; region preference destination Asia handled through candidate airports/results.`
- `Applied: alliance oneworld; “either direction” checked as LHR → HND and HND → LHR.`
- `Applied: region preference “Europe” recognized; not enforced in the local request because this surface has no region parameter.`

## Safe Failure Mode

If filters conflict or cannot be safely applied:

1. State the conflict or unsupported filter.
2. Run the closest supported query only if it is still faithful to the user's intent.
3. Ask one focused clarification when the result would otherwise be misleading.

Examples:

- `“Nonstop” and “up to one stop” conflict. Should I restrict to nonstop only, or include one-stop options?`
- `I can search routes from LAX to Europe, but the local route endpoint does not accept a Europe parameter directly. I can start with LAX routes and flag European destinations from returned airport metadata.`
