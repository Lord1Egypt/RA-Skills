# Typography

## EVA-Specific Note

For Japanese title treatment, a strong reference is `Matisse EB` (`マティスEB`).

If `Matisse EB` is unavailable, use the closest available Japanese serif / Mincho fallback for title moments, for example:

- `Hiragino Mincho ProN`
- `Yu Mincho`
- `Noto Serif JP`
- another sharp, high-contrast Mincho face

Use it for:

- Japanese section titles
- chapter-like interstitial headings
- large warning or classification text
- high-ceremony labels that need unmistakable EVA flavor

Do not use it for:

- dense telemetry tables
- numeric readouts
- small UI labels
- data-heavy control panels

Reason:

EVA recognition comes partly from the Matisse-style Japanese title voice, but the in-screen UI language also depends heavily on technical sans, compressed Latin text, tabular numerals, and instrument-style diagram layout.

## Roles

### Display

Use for alert words, section titles, unit labels, command states, and Japanese title moments.

Traits:

- condensed
- technical
- uppercase-friendly
- strong at medium and large sizes
- when Japanese is used as a visual headline, Matisse EB is a preferred reference

### Data

Use for metrics, coordinates, counters, timestamps, and tables.

Traits:

- tabular numerals
- monospace or pseudo-monospace
- stable digit width
- legible at small sizes

### Body

Use for small notes and secondary descriptions.

Traits:

- compact
- neutral
- subordinate to display and data roles

## Rules

- Large alert words should feel like signage, not product headings.
- Japanese title moments may use `Matisse EB`, but data areas should not.
- Small labels should use increased tracking and strict casing.
- Numeric readouts should be visually stable when values change.
- Avoid friendly or overly rounded typefaces.
- A good EVA pairing is:
  - Japanese title layer: `Matisse EB`
  - data / metrics layer: condensed sans + monospace numerals
- Practical fallback stack for title Japanese:
  - `Matisse EB`
  - `Hiragino Mincho ProN`
  - `Yu Mincho`
  - `Noto Serif JP`
  - `serif`
