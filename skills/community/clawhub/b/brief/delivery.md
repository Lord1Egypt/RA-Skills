# Delivery — Channels, Register, Timing

A right brief on the wrong channel or at the wrong hour goes unread. Defaults below; `default_channel` and `emoji_markers` in config override, and the **Timing** preference area records the user's cadence.

## By Channel

| Channel | Rules |
|---------|-------|
| Chat message | One screen, hard cap. Bottom line is literally the first line — no greeting, no "quick update:". No attachments the reader must open to get the point |
| Email | The subject line carries the bottom line or the ask: "Decision needed by Fri: vendor A vs B" — not "Project update". Brief lives in the body; an attachment may add depth but never holds the takeaway |
| Doc | Full template plus a header block: audience, as-of date, status, sources. Docs get forwarded — write assuming readers you didn't pick |
| Slides | A deck is not a brief. Send the doc as pre-read, present the slides; one idea per slide, the bottom-line slide first, never last |
| Verbal readout | 30-60 seconds: bottom line, one supporting point, the ask. Write it out first even if nobody sees the text — improvised readouts bury ledes at the same rate as written ones |

Length by channel: chat = one screen; email = `default_length` capped at one-page; doc = `default_length`. When material genuinely exceeds the channel, move channels ("full brief in the doc, bottom line here") rather than overrunning.

## Register

- Emoji section markers (⚡📊🎯): internal informal channels only, and only while `emoji_markers` is true.
- Formal channels — exec email, external docs, anything a client or the board sees — always plain headers, regardless of config. Same structure, same content.
- External register drops internal names, codenames, and candor (`audiences.md`); formality never adds words, only removes markers.

## Timing

| Brief type | When to deliver |
|------------|-----------------|
| Meeting brief | The day before, not the morning of — morning-of pre-reads get skimmed in the hallway or not at all |
| Board brief | With the agenda, days before the meeting, not hours; late board material reads as either disorganization or concealment |
| Recurring status | Same day, same time, every edition — the cadence itself carries information (`recurring.md`) |
| Incident brief | Cadence set by severity and committed in each edition's "next update" line; the commitment outranks completeness (`templates.md` → Incident) |
| Decision brief | While the decision is still open: deadline minus the reader's realistic turnaround, not deadline minus zero |
| Handoff brief | Before the overlap window starts, so questions land while you can still answer them |

The general principle: deliver when the reader can still act, not when the writing happens to finish. A perfect brief after the decision is documentation.
