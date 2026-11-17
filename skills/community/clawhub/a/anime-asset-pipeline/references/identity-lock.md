# Locking a character's identity

## Why text-to-image fails here

Pure text-to-image cannot hold a character's identity across images. You can describe the character perfectly and still get a different face, different hair behaviour, different proportions on every generation. Prompt engineering does not fix this; it is the wrong layer.

The reliable mechanism is **image-to-image from an anchor**. The anchor carries identity information that text cannot.

## Anchor workflow

1. **Establish anchors.** Canonical images of the character — at minimum a front view and a three-quarter view. These are the reference standard for everything downstream.
2. **Derive, do not re-describe.** Every new image comes from an anchor via image-to-image. The prompt guides pose, lighting, and framing; the anchor supplies identity.
3. **Keep anchors fixed.** Do not quietly swap or regenerate an anchor mid-project. If an anchor must change, say so explicitly — everything derived from it is now suspect.

## Verify feature by feature

"Looks like the character" is not a check. List the character's defining features and confirm each one against real reference images:

- face shape and eye shape / eye colour
- hair colour, silhouette, and any **local** colour treatment
- distinguishing marks or accessories
- proportions and costume details

Write the result per feature. A single overall judgement hides exactly the defects that matter.

## Known failure: local colour treatments do not lock

A model that holds the character overall can still fail on a specific **local** feature — a streak, a highlight, a partial dye. This was tested three times on the same local feature and failed each time.

Rule: **three attempts at the same local feature is enough evidence.** Stop retrying the same approach. Change the approach instead — render it in a different stage, composite it, or accept the limitation and report it.

> Status: confirmed as a failure mode. The specific model and the exact feature are documented in the project log, not here — treat this as a general caution about local features rather than a claim about any one model.

## Changing a character design

If the design itself changes, the anchors are invalidated. Re-establish anchors before continuing. Do not patch old anchors to approximate a new design — the approximation error compounds across every derived image.
