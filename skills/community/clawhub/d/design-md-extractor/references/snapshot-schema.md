# Design Snapshot Schema

The extractor produces a `DesignSnapshot` with:

- `meta`: title, url, hostname, analyzedAt, and optional favicon.
- `raw.cssVariables`: sampled CSS custom properties from root, body, and key elements.
- `raw.elementCounts`: visible element summary counts.
- `raw.colorTokens`: observed color tokens with evidence.
- `tokens.colors`: semantic roles such as primary, background, surface, textPrimary, textSecondary, border, and status colors.
- `tokens.typography`: font families, size/weight/line-height clusters, and semantic roles.
- `tokens.spacing`: clustered spacing values and xs/sm/md/lg/xl scale.
- `tokens.radius`: clustered radius values and sm/md/lg/xl/full scale.
- `tokens.shadows`: box/text shadow candidates and semantic shadow scale.
- `components`: basic button, card, and input style candidates.
- `designSystem`: optional shadcn, Bootstrap, Material, Ant Design, Primer, or Generic signal.

The `DESIGN.md` front matter serializes the most important normalized tokens, then the body explains how to use them in AI-assisted frontend implementation.
