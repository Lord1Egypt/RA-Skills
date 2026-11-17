# Delivery — Channels, Timing, and Interrupts

The same digest lands differently per channel and per hour. Delivery mistakes are the ones users feel first — a wall of text at 3am undoes a week of good curation.

## Per-Channel Format

| Channel | Adaptation |
|---|---|
| Chat (Slack, Telegram, DM) | One message per digest; split only at section boundaries, never mid-item. Emoji section headers earn their keep here |
| Email | Subject line = the top Highlight's headline, never "Your digest for [date]". Full structure in the body; plain formatting beats HTML ornament |
| Audio script | Spoken register: numbers rounded for the ear ("about forty percent"), sources spoken once per item, no URLs read aloud. Section headers become spoken transitions |
| Text/file | The cold-start template as-is (SKILL.md → Output Format) |

Channel comes from `config.yaml`; medium, structure, and visuals from learned preferences (`dimensions.md` → Format).

## Scheduling Ladder

1. **On-demand only** until asked — the default schedules nothing (`dimensions.md` → Timing).
2. After the **second requested digest**, propose a slot once ("want this every morning around this time?"). Schedule nothing until confirmed.
3. Before the **first scheduled send**, confirm timezone (`timezone` variable). A digest at the wrong local hour is the fastest way to get muted.
4. Respect weekday/weekend splits and quiet hours the moment they are stated or confirmed.

## Weekly Digest Is a Different Artifact

- A weekly leads with **what changed over the week** — deltas, trend lines, resolved rumors — not seven days of items concatenated.
- Same budget discipline: `item_cap` applies to the weekly too; the week's volume raises the bar per item, it does not raise the cap.
- If the user gets both daily and weekly: the weekly carries synthesis and closed loops, never re-runs the dailies' items unchanged (SKILL.md rule 7).

## Catch-Up After a Gap

- Vacation, downtime, or missed cycles: send **one consolidated digest** marked with the period covered ("catching you up: May 2-9"), top items only across the whole gap.
- Never send the missed digests one by one — the backlog is your problem, not the user's inbox's.
- Resolved-within-the-gap stories collapse to their resolution: "X was rumored acquired, confirmed Thursday" is one item, not two.

## Mid-Cycle Interrupts

- Interrupt the schedule only for items matching a **[confirmed] or [locked] urgent-signal rule** in `preferences.md`. No rule learned yet → never interrupt.
- When an item feels interrupt-worthy but no rule exists: hold it for the next digest and propose the rule there ("this looked urgent — want anything matching 'X' sent immediately next time?"). The user defines urgency by answering; you never define it by acting.
- An interrupt carries one item and one line of why-now. If it needs the full template, it wasn't an interrupt.

## Delivery Hygiene

- Footer carries source count and next-digest time (cold-start template) — the next-digest promise is a commitment; if the schedule changes, say so in the digest, not silently.
- After every delivery, run the Learn step before anything else queues (`learning.md`): reactions decay fast, and the signal you don't record now is gone.
