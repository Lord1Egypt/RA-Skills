# Breakcold branding

Visual style for anything the agent renders for the user — most importantly reports (`action-reports.md`), but also any chart, dashboard, or visual summary.

The goal: every deliverable should feel like it came **from Breakcold**, not from a generic AI. No exceptions.

## Brand color

| Token         | Hex       | Use                                                        |
|---------------|-----------|------------------------------------------------------------|
| Breakcold Blue | `#0059F7` | Primary brand color. Headers, key data, CTAs, icon backgrounds. **The single most important color — use it confidently.** |
| Ink           | `#0E0E10` | Body text, dark backgrounds.                               |
| Paper         | `#FFFFFF` | Default surface.                                           |
| Soft         | `#F4F6FB` | Section backgrounds, cards.                                |
| Hairline     | `#E5E8F0` | Borders, dividers.                                         |
| Muted        | `#6B7280` | Secondary text, captions, axis labels.                     |

## Tag palette (record colors)

Breakcold uses a saturated tag palette for categorizing records. Use these for categorical data series in reports (one color per category, in order):

| #   | Name        | Hex       |
|-----|-------------|-----------|
| 1   | Blue        | `#3B82F6` |
| 2   | Green       | `#10B981` |
| 3   | Amber       | `#F59E0B` |
| 4   | Red         | `#EF4444` |
| 5   | Violet      | `#8B5CF6` |
| 6   | Pink        | `#EC4899` |
| 7   | Indigo      | `#6366F1` |
| 8   | Cyan        | `#06B6D4` |
| 9   | Teal        | `#14B8A6` |
| 10  | Orange      | `#F97316` |
| 11  | Rose        | `#F43F5E` |
| 12  | Slate       | `#64748B` |

The **iconic Breakcold blue** (`#0059F7`) sits separately at the top of the visual hierarchy — it's always the primary accent, never just one of the categories. Categorical palette starts at #1 (`#3B82F6`).

## Status / signal colors

For win/loss, on-track/at-risk, positive/negative:

| Intent       | Hex       |
|--------------|-----------|
| Positive / won | `#10B981` |
| Negative / lost | `#EF4444` |
| Warning / at-risk | `#F59E0B` |
| Neutral / open | `#0059F7` |

## Typography

- **Sans-serif system stack:** `"Inter", "SF Pro Text", "Segoe UI", system-ui, -apple-system, sans-serif`.
- **Headings:** weight 600–700.
- **Body:** weight 400.
- **Numbers in charts:** tabular figures where supported (`font-variant-numeric: tabular-nums`).

If you have access to web fonts and the output supports them, use **Inter** (free, open-source — matches Breakcold's product UI feel).

## Layout principles

- **Density over decoration.** The user said no fluff. White space exists to separate ideas, not to fill space.
- **One headline KPI per section, large and confident.** Below it, the breakdown that explains it.
- **Cards on `Soft` background, separated by `Hairline` borders.** No drop shadows beyond a 1px hairline.
- **Charts are minimal:** no chart-junk gridlines, no 3D, no gradients on bars. Axes muted, data series in Breakcold Blue or the tag palette.
- **Always include the date range and the data source in the report footer.** "Data: Breakcold inbox & CRM, May 1 – May 23, 2026." Builds trust.

## Logo treatment

If you embed the Breakcold mark in a deliverable:

- The "Br" logo is a white wordmark on the Breakcold Blue (`#0059F7`) squircle. Don't recolor the mark or place it on a non-brand background.
- For documents, the mark sits in the top-left at modest size (about 24–32px tall).

## Real assets — use these, don't recreate them

The actual brand assets are bundled in the skill at `assets/`:

| File                              | What it is                                                  | Use it for                                              |
|-----------------------------------|-------------------------------------------------------------|---------------------------------------------------------|
| `assets/breakcold-mark.svg`       | The "Br" squircle mark alone                                | Compact footer marks, favicons, small accents           |
| `assets/breakcold-logo.svg`       | Full Breakcold wordmark (mark + "Breakcold" text)           | Top-of-report banner, document headers                  |
| `assets/report-template.html`     | A fully populated Breakcold-branded HTML report with the mascot embedded inline | Chassis for Action 3 reports — see `report-design-guide.md` |

When generating reports or any branded visual, **reference these directly** if the delivery surface supports relative paths. Inline the SVG XML when delivering inline. For the mascot, preserve the inline image already present in `assets/report-template.html`.

Do **not** approximate the mark with a "blue square with white Br text" — the real SVG is right there. Same for the mascot: don't generate an AI-image of "a friendly bear" — use the embedded image from the canonical report template.

## Mini design tokens block (for code-generated reports)

These are the exact CSS variables used in `assets/report-template.html`. If you're hand-rolling a report, paste this block — it keeps everything consistent with the canonical template.

```css
:root {
  /* core palette */
  --bc-blue:    #0059F7;   /* the iconic Breakcold blue */
  --bc-blue-l:  #2E7BFF;   /* lighter blue (hero gradient start, scrollbar) */
  --bc-blue-d:  #003BC4;   /* darker blue (hero gradient end) */
  --ink:        #0E0E10;   /* body text, dark surfaces */
  --ink2:       #17171C;   /* slightly lighter dark for layered surfaces */
  --paper:      #FFFFFF;   /* default surface */
  --soft:       #F4F6FB;   /* section backgrounds, cards-on-cards */
  --hair:       #E5E8F0;   /* borders, dividers */
  --muted:      #6B7280;   /* secondary text, captions, axis labels */

  /* signal colors */
  --pos:        #10B981;   /* won / positive */
  --neg:        #EF4444;   /* lost / negative */
  --warn:       #F59E0B;   /* at-risk / warning */

  /* categorical palette — for chart series */
  --c1: #3B82F6; --c2: #10B981; --c3: #F59E0B; --c4: #EF4444;
  --c5: #8B5CF6; --c6: #EC4899; --c7: #6366F1; --c8: #06B6D4;
  --c9: #14B8A6; --c10:#F97316; --c11:#F43F5E; --c12:#64748B;

  /* typography */
  --font: "Inter","SF Pro Text","Segoe UI",system-ui,-apple-system,sans-serif;

  /* shadows */
  --sh-sm:  0 1px 2px rgba(14,14,16,.04), 0 8px 20px -12px rgba(14,14,16,.16);
  --sh-md:  0 2px 6px rgba(14,14,16,.05), 0 22px 44px -22px rgba(14,14,16,.24);
  --sh-blue: 0 18px 40px -18px rgba(0,89,247,.5);   /* used on the hero */
}
```

The Breakcold blue (`#0059F7`) sits at the top of the visual hierarchy — it's always the primary accent. The categorical palette (`--c1` through `--c12`) is for chart series. The signal colors (`--pos` / `--neg` / `--warn`) are for win/loss/at-risk semantics.

The shadow tokens add depth without aggressive drops: `--sh-sm` for cards, `--sh-md` for elevated/hover states, `--sh-blue` reserved for the hero block.

## What to avoid

- Generic ChatGPT-flavored emoji-heavy headers.
- Rainbow gradients.
- "AI-assistant" badging on the report (no "Generated by AI" footer).
- Pie charts with more than 5 slices.
- Stacked bars when a grouped bar is clearer.
- Long paragraphs of recommendations — the report's job is the breakdown; if the breakdown is good, the reading does the recommending.
