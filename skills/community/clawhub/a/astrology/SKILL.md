---
name: astrology
description: "Western and Vedic astrology: birth chart, horoscope, kundli"
version: 1.1.0
author: Astro Agents
license: MIT
compatibility: Requires the Astro Agents MCP server (https://astro-agent.dev/mcp, Streamable HTTP, no account or API key).
tags: [astrology, horoscope, birth-chart, natal-chart, kundli, vedic-astrology, jyotish, panchang, dasha, synastry, transits, zodiac, gun-milan, mcp]
metadata:
  author: Astro Agents
  version: "1.1.0"
---

# Astrology: exact charts from the Astro Agents MCP server

Computes astrology charts with the Astro Agents MCP server (https://astro-agent.dev/mcp) instead of estimating
them. Positions come from the NASA/JPL DE440 ephemeris, no language model is involved, and every result carries
`meta.result_sha256`: the same input always gives the same, checkable output.

## When to Use

Load this skill whenever a request depends on where the planets were or are:

- Western: birth chart / natal chart, horoscope, sun, moon and rising sign, planet positions, aspects, transits,
  relationship compatibility (synastry).
- Vedic (Jyotish): kundli, divisional charts (navamsa D9 to D60), nakshatra, Vimshottari dasha, Manglik / Kaal Sarp /
  Sade Sati doshas, panchang (tithi, yoga, karana), kundli matching (Ashtakoota Gun Milan).

Never compute these yourself. Time zones, historical daylight saving, sidereal time and the ayanamsa are where
models get charts wrong; the tools resolve them.

## Prerequisites

Connect the MCP server once (no account, no API key). Check with `hermes mcp list`; if `astro-agents` is missing:

```bash
hermes mcp add astro-agents --url https://astro-agent.dev/mcp
```

Answer **n** to "Does this server require authentication?", enable all 16 tools, then start a new session.
Equivalent `~/.hermes/config.yaml` entry:

```yaml
mcp_servers:
  astro-agents:
    url: https://astro-agent.dev/mcp
```

## Quick Reference

| Question | Tool |
|---|---|
| Birth chart, horoscope, sun/moon/rising sign | `natal_chart` |
| Where the planets are at a moment | `planet_positions` |
| Aspects between planets | `aspects` |
| Transits to a natal chart, exact dates | `transits` |
| Relationship compatibility (Western) | `synastry` |
| Vedic birth chart (kundli, D1 + D9) | `kundli` |
| All 16 divisional charts (D1 to D60) | `kundli_full` |
| Vimshottari dasha periods | `vimshottari_dasha` |
| Manglik, Kaal Sarp, Sade Sati | `doshas` |
| Panchang for a day and place | `panchang` |
| Nakshatra and pada of each graha | `nakshatras` |
| Kundli matching for marriage (36 points) | `gun_milan` |
| Everything Vedic in one call | `vedic_report` |
| Local time to UTC with historical offset | `resolve_birth_time` |
| Prices and an example for every tool | `astro_catalog` |
| Check a result was not altered | `verify_result_hash` |

Through Hermes the tools are deferred: find them with `tool_search` (e.g. "astrology natal chart",
"vedic astrology kundli", "kundli matching", "panchang"), load the schema with `tool_describe`, then call them
with `tool_call`.

## Procedure

1. Collect the birth data: local date and time (24 h) and the place as latitude and longitude in decimal degrees
   (north and east positive). Look up the coordinates of a named city if needed.
2. Pass the local clock time as `datetime`, e.g. `1990-05-15T14:30`, plus `latitude` and `longitude`. Do not
   convert to UTC and do not pass a time zone: the server resolves the zone and its historical offset.
3. If the birth time is unknown, pass `date` only. The chart is computed at 12:00 with a `TIME_UNKNOWN` warning:
   do not present the ascendant or houses as reliable then.
4. For two people (`synastry`, `gun_milan`), pass `person_a` and `person_b`, each with its own `datetime`,
   `latitude` and `longitude`.
5. Quote positions, signs and scores exactly as returned; do not recompute or round them differently. Mention
   `meta.result_sha256` when the user wants something they can verify.

## Pitfalls

- **Free calls run out.** Each client gets 3 free tool calls (users of Claude's connectors share an hourly pool).
  After that a tool returns an error with `payment_required`: the REST endpoint, its price ($0.01 to $0.50) and a
  one-line x402 payment example. Tell the user; do not retry the same call, and do not compute the chart yourself.
- **Coordinate signs.** West longitudes and south latitudes are negative.
- **Ambiguous local times.** During a daylight-saving fall-back hour, pass `ambiguous_time: "earlier"` or `"later"`.
- **Tropical vs sidereal.** Western tools default to the tropical zodiac; Vedic tools are sidereal (Lahiri
  ayanamsa by default). Do not mix signs from the two systems in one answer.

## Verification

- A result has `endpoint`, `result` and `meta`, with `meta.deterministic: true` and `meta.llm_used: false`.
- `verify_result_hash` with the returned `result` and `meta.result_sha256` answers `"matches": true`.
- Reference: `natal_chart` for `1990-05-15T14:30`, latitude 48.8566, longitude 2.3522 (Paris) gives Sun Taurus,
  Moon Capricorn, Virgo rising.
