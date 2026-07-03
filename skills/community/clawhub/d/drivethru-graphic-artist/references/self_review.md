# Self-review loop — critique your own mockup before returning it

The compose pipeline is deterministic: it places the decoration by ratio
rules against the detected garment bbox. Those rules are a *starting guess*.
For a specific garment/decoration pair the guess can land wrong — too high,
too small, off-center — and nothing in the deterministic path can notice,
because it has no eyes.

**You do.** You are the model running this skill, and your `Read` tool
renders a PNG visually. So after every compose, look at the mockup you just
produced, judge it against what the placement is *supposed* to look like, and
if it's off, re-compose with corrective deltas — up to **3** total compose
attempts — before you return anything to the user. The user should see the
good result, not the first draft.

This is not generative work: no pixels are model-made. The compose stays
100% deterministic; you are only *judging* the output and adjusting the same
numeric flags a human would ("move it down, a bit bigger").

## The loop

1. **Compose** with the current flags. Note the `output` path from the receipt.
2. **Read the output PNG** (the `Read` tool renders it — actually look at it).
3. **Score it** against the placement intent below. Decide: acceptable, or not?
4. If **acceptable** → return the PNG to the user. Done.
5. If **not acceptable** and you have attempts left → derive deltas (below),
   re-compose *layering them on the previous run's flags*, go to step 2.
6. **Hard cap: 3 compose attempts.** If attempt 3 still isn't great, return
   the best of the three and tell the user in one line what's still off and
   offer to keep tuning. Never loop past 3 silently.

## What "correct" means per placement

Judge the rendered image against these. They're distilled from the real print
spec in [`decoration_spec.md`](decoration_spec.md) (with the canonical diagram
at `assets/decoration_guide.png`) — open those when you need the exact inches or
to see where a location sits. The size column is anchored to a full front (the
biggest chest print), so the key relationships are: **a chest logo is
pocket-sized, ~¼ the width of a full front**, and **a full back equals a full
front**.

| Placement | Horizontally | Vertically | Size (spec) |
|---|---|---|---|
| `full_front` | centered | top of print ~1/4 down the chest, below the collar/seams | 13″ adult ≈ fills the chest, ~50–55% of garment width |
| `left_chest` / `right_chest` | over the pec, ~1/4 in from center | high on the pec, below the collar | 3–4″, pocket-sized (~¼ of a full front) |
| `full_back` | centered | upper-to-mid back, below the yoke seam | 13″, same size as a full front |
| `back_yoke` / upper back | centered | high, just below the collar seam | 10–13″, nearly full-back width |
| `sleeve` | centered on the sleeve | mid-forearm area | 3–4″, narrow, follows the sleeve |
| `front` (generic) | centered | centered in the available panel | ~45–55% |
| hoodie `full_front` | centered | on the chest, **above the pocket** | fills width but capped ~9″ tall to clear the pocket |

Sanity floor from the spec: embroidery lettering must be ≥ 0.25″ high — if text
in the mockup is so small it would be illegible/unsewable, it's too small
regardless of the table.

Also check, regardless of placement:

- **Not clipped or bleeding** off the garment edge, collar, or seams.
- **Not crooked** unless rotation was intended.
- **Legible** — text/marks aren't so small they disappear or so large they
  distort.
- **Right panel** — a front print isn't riding up onto the collar or shoulder.

## From critique to deltas

Translate what's wrong into flags, layered on the previous run's args. These
are the *same* flags the iterative-feedback table uses — you're just the one
deciding them now instead of the user.

| What you see | Delta to add |
|---|---|
| Sitting too high (up on the collar/seams) | `--offset-y-pct +6` to `+10` |
| Sitting too low | `--offset-y-pct -6` to `-10` |
| Too far left | `--offset-x-pct +4` to `+8` |
| Too far right | `--offset-x-pct -4` to `-8` |
| Too small / weak | `--width-delta-pct +10` to `+15` |
| Too big / distorting / bleeding off edges | `--width-delta-pct -10` to `-15` |
| Crooked (and shouldn't be) | `--rotate-deg 0` |

Use a **small** correction when it's slightly off and a **larger** one when
it's clearly off. Don't stack more than two or three deltas in one attempt —
fix the biggest problem first.

## Stop conditions (don't loop forever)

- **Accept early.** "Good enough for a customer to approve" is the bar, not
  pixel perfection. If attempt 1 already looks right, return it — don't burn
  attempts chasing marginal gains.
- **Hard cap at 3 composes.** Always.
- **Oscillation guard.** If a delta's sign flips between attempts (you moved
  it down, now you want it up), you overshot — you're already close. Halve the
  correction, or just accept the better of the two. Do not ping-pong.
- **No-progress guard.** If an attempt didn't visibly improve things, don't
  repeat the same delta harder — stop and hand back to the user with a note.

## When the same correction keeps recurring — fix the rule, not the mockup

The loop patches each mockup individually, but if you find yourself applying
the *same* delta in the *same direction* for a given `(category, placement)`
across different jobs, that's not a per-mockup quirk — the **default rule is
systematically off** and every future mockup will start wrong and cost a
correction pass.

Example: hoodie `full_front` ships with `y_top_ratio 0.22`, but the detected
bbox includes the hood, which pulls the top reference up, so the print
consistently lands high and review keeps adding `--offset-y-pct +8`
(≈ `y_top 0.30`). When you notice that pattern, offer to bake the correction
into the catalog so the loop rarely has to fire:

```bash
python3 scripts/edit_placement_rule.py update hoodie full_front --y-top-ratio 0.30
```

Promote from the *effective* ratios in the last good compose receipt's
`applied` block (see `references/iterative_feedback.md` → "Promoting a tuned
result to a default"). Ask before writing — a default change affects every
future mockup for that category/placement, so confirm the user wants it.

## What to tell the user

Lead with the final PNG. Then one line: what placement, and — only if you
iterated — that you auto-adjusted it (e.g. "nudged it down onto the chest and
sized it up ~10% after review"). If you hit the 3-attempt cap without nailing
it, say what's still off and offer to keep tuning. Keep the internal critique
to yourself; the user wants the result and a short summary, not a play-by-play.
