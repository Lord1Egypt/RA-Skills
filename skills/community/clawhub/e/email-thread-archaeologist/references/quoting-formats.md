# Quoting Formats, Strata, and Marker Vocabulary

## How the major clients mangle history

Each mail client buries quoted text in its own dialect. The excavator
recognizes the big four families:

### Gmail / Apple Mail / most webmail — inline `>` quoting

```
On Tue, Oct 14, 2026 at 3:12 PM Dana Whitfield <dana@example.com> wrote:
> Agreed — let's go with Signature.
> One open item: who owns the punch-list documentation?
>> On Tue, Oct 14, 2026 at 1:02 PM Marcus Lee wrote:
>> I can get approval from finance by Friday.
```

Depth = count of `> ` prefixes. The `On ... wrote:` line attributes
the stratum below it. This is the cleanest dialect: strata splitting
is exact.

### Outlook — header blocks instead of quotes

```
From: Chen, Robert
Sent: Monday, October 12, 2026 4:55 PM
To: facility-team@example.com
Subject: Q3 electrical vendor

Team — the old panel is failing inspection...
```

No `>` at all; the `From:/Sent:/To:/Subject:` block marks the start of
a buried message. The excavator treats each `From:` line as an
attribution and the header lines themselves as non-content (filtered
from output).

### Forwarded-message fences

```
---------- Forwarded message ---------
From: ...
Begin forwarded message:
```

Fences behave like `From:` blocks: they open a new stratum.

### Bottom-posters and mixed threads

Some participants reply below the quote, interleaving depths. The
strata splitter tracks max-depth transitions; mixed threads produce
more, smaller strata — attribution stays correct, but verify `layer-0`
(the newest voice) by eye.

## Strata model

A stratum = one buried message, with:

- `depth` — quote depth (proxy for age: deeper = older)
- `author` — parsed from the attribution line, or `None`
- `lines` — content lines, header rows excluded

Reconstruction sorts strata deepest-first and walks them; within a
stratum, original line order is kept.

## Dedup rules

- Exact match after quote/whitespace strip → duplicate
- Fuzzy match (difflib SequenceMatcher ≥ 0.90, with a length gate)
  → duplicate — this kills the same sentence re-quoted with slightly
  different wrapping
- First occurrence (oldest stratum) wins; later copies die
- Lines < 15 chars are deduped aggressively (short lines are usually
  "Thanks!" noise; keep at most one)

## Decision marker vocabulary

The ledger fires on these (case-insensitive, substring):

| Intent | Markers |
|---|---|
| Agreement | agreed, we agree, let's/lets/we'll/we will go with, so we're doing, it's/its settled |
| Formal decision | decided, decision:, final:, locked in, signed off, sign off |
| Approval | approved, green light, greenlit |
| Commitments | booked, ordered, confirmed, canceled/cancelled |
| Ownership | action item, owner:, i'll/i will take, assigned to |

False positives to expect: "decided" inside a question ("have we
decided?"), "confirmed" describing someone else's schedule. The ledger
is a reading aid, not a contract.

## Answer detection for open questions

A question line (ends in `?`) is considered answered if any of the
next ~12 timeline facts:

- starts with an answer starter: yes / no / done / answered /
  confirmed / here's / here is / to answer / good question
- contains "agreed" (settling a "shall we?" question)
- has "yes" within its first four words

Otherwise it's reported open. This heuristic errs on the side of
reporting open — better to re-check a settled question than to drop a
dropped one.

## .eml specifics

`load_text` parses .eml with `email.message_from_bytes` +
`email.policy.default`:

- multipart: first `text/plain` part wins; else the html body
  (rendered as text by get_content — tags visible but strata still
  parse if quoted with `>`)
- single-part: get_content directly

For HTML-quoted threads (Outlook inline images, Gmail quote bars),
export the thread as plain text or paste with quotes expanded —
quote-bar HTML carries no `>` characters and cannot be stratified.

## Limits (honesty section)

- Attribution is heuristic: it trusts the client's quoting, which
  participants can edit (snipping, re-attributing). Don't use as
  certified evidence.
- Snipped history is gone: if someone deleted the quote before
  replying, the buried message no longer exists in the artifact.
- Locale: `От:`/`Von:`/`De:` From-headers recognized; `On ... wrote:`
  translations are NOT — a fully non-English thread attributes by
  layer only.
