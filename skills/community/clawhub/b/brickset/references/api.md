# Brickset API v3 quick reference

Base endpoint: `https://brickset.com/api/v3.asmx`

Common methods used by this skill:

- `checkKey` — validate the API key
- `getKeyUsageStats` — inspect 30-day usage
- `getSets` — search sets or retrieve one set by number/setID
- `getThemes` — list themes
- `getSubthemes` — list subthemes for a theme
- `getYears` — list years, optionally filtered by theme
- `getInstructions2` — fetch instructions by set number, no setID lookup needed
- `getAdditionalImages` — fetch extra image URLs by setID

## getSets params JSON

Pass a JSON object string in the `params` field.

Useful fields:

- `query`
- `theme`
- `subtheme`
- `setNumber` like `6876-1`
- `year`
- `tag`
- `owned`
- `wanted`
- `orderBy`
- `pageSize` up to `500`
- `pageNumber`
- `extendedData` = `1`

Examples:

```json
{"theme":"Space","year":"1979,1980","pageSize":25}
```

```json
{"setNumber":"6990-1","extendedData":1}
```

```json
{"query":"Blacktron","orderBy":"YearFromDESC","pageSize":10}
```

## Notes

- All calls require `apiKey`.
- `getSets` counts against daily usage limits.
- `owned`/`wanted` set queries require `userHash`.
- Brickset returns JSON with a top-level `status` field.
