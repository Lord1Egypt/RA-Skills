# Production Pipeline (P0 upgrade, v2.5)

Batching is where good demos get exposed. This module adds a pre-flight batch,
drift labeling, and retry rules so the template scales from one-off images to a
production series.

## Step 1 — Pre-flight batch (12 images)

Run this before the real batch. A character that cannot survive 12 will not
survive 120.

| # | Type | Purpose |
|---|---|---|
| 1-3 | Close portraits | Face / identity stability |
| 4-6 | Half-body scenes | Outfit + upper-body consistency |
| 7-9 | Full-body scenes | Proportions / head-to-body ratio |
| 10-12 | Style-stress scenes | Extreme lighting / angles / backgrounds |

## Step 2 — Drift labels (one primary + optional secondary per output)

| Label | Meaning | Verdict |
|---|---|---|
| pass | Usable without edit | ✅ |
| minor edit | Usable after crop / cleanup / color adjust | ✅ |
| face drift | Identity changed | ❌ |
| outfit drift | Clothing / accessories changed | ❌ |
| pose failure | Body, hands, or interaction failed | ❌ |
| style drift | Visual language changed | ❌ |
| brand mismatch | Correct character, wrong project feel | ❌ |
| unusable artifact | Distortion, extra limbs, broken object, bad text | ❌ |

Never write only "bad" or "weird" — every failure must carry a label so the
next step is actionable.

## Step 3 — Retry rules (written before the batch starts)

| Trigger | Action |
|---|---|
| Face drift in 2 of first 12 | Tighten identity reference before scaling |
| Outfit drift in 3 of first 12 | Add outfit-detail reference + stronger locked block |
| Pose failure only in action scenes | Separate pose control from identity reference |
| Style drift across otherwise correct images | Lock style block; reduce scene adjectives |
| 2 failed retries for the same scene | Route to a different model or mark for manual edit |

## Step 4 — Versioned reference pack

The reference pack lives in version control, not a downloads folder:

```
character-vXX/
  hero-face.png      # identity anchor
  full-body.png      # proportions & outfit
  outfit-detail.png  # costume lock
  style-frame.png    # render language
  negative-cases.png # drift boundaries
```

## Step 5 — Log everything

Save every output with its label into `GenerationIterationLog.csv`. The model
does not learn from rejected outputs automatically — but you and your team do.
