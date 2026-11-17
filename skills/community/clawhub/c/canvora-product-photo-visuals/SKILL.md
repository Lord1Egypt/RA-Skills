---
name: product-photo-visuals
version: 1.0.0
description: Build Canvora visuals around the user's OWN photos — real product shots, team headshots, venue or event photos embedded into the design instead of generic stock imagery. Use when the user has photos to include, wants their actual product shown, or says the visuals must feature their real people or place.
homepage: https://canvora.ai/for-agents
metadata: {"openclaw":{"emoji":"📸","requires":{"env":["CANVORA_API_KEY"]}}}
---

# Visuals built around the user's own photos

The difference between a generic AI visual and a usable one is usually whether
the actual product is in it. Canvora can compose the user's real photos into a
generated design — the layout, typography and brand styling are generated
around the photo, not pasted on top of it.

## This is an MCP-path capability

Photo embedding runs through the **MCP server** (`https://api.canvora.ai/mcp`)
or the Canvora web app. The `canvora` CLI cannot send photos today — if the
user is CLI-only, say so and point them at the MCP connector or the dashboard.
Don't fake it with `--url`.

The flow, in MCP tools:

1. `upload_photo({ data, filename })` → returns a CDN URL. Repeat per photo,
   **maximum 5**.
2. `chat({ message })` — describe the visual, mentioning that the photos are
   the subject.
3. `confirm_generation({ conversation_id, formats, embedding_photos: [urls],
   brand_id, ... })` — the photo URLs go here.
4. `get_generation({ generation_id })` to poll and collect outputs.

Step 4 is a poll loop by design, so the CLI's shell-timeout consideration
doesn't apply here — but the same rule does: a generation that hasn't come back
yet is still running. Never fire a second `confirm_generation` for the same
job; that starts a second, separate generation. State the cost in the same message as
step 3 — 10 credits per single visual, 15 per carousel slide — announcing it
rather than asking permission. If you chose the slide count rather than the
user, confirm that number first.

## Intake

1. **How many photos, and what's in each?** Tell the pipeline what it's looking
   at ("the blue jar, front label visible", "our head chef in the kitchen").
   A photo with no description gets used generically.
2. **Which photo is the hero?** With multiple photos and multiple slides, say
   which is the cover.
3. **Format and brand** — as normal (`instagram_post`, `ad_square`, a carousel…
   plus the brand kit).
4. **Must the photo be untouched?** Say so explicitly in the brief. Otherwise
   the model may crop, relight or restyle it to fit the composition.

## What works, what doesn't

**Works well**
- One clear product on a clean background — the pipeline can place and light it
- Food, drinks, packaging, physical goods, venues
- A single person, well lit, facing camera
- Photos where the important part is centred, not at the edge

**Struggles**
- Cluttered scenes with no clear subject
- Faces that must stay pixel-identical — treat close likeness as a review step,
  never assume it. Have the user check before publishing anything with a real
  person in it.
- Text inside the photo (packaging copy, signage) — it may be re-rendered
- More than 5 photos in one generation (hard cap)

## Craft notes

- **Name the photo's role in the design**: "product hero on the left, headline
  right", not a full layout spec. One line of placement intent is the sweet spot.
- **Brand kit still matters** — the design around the photo is what carries the
  brand.
- **`--exact`-style precision:** if the pack copy or price must be legible and
  correct, put it in the text content rather than relying on the photo.
- Everything from the `canvora` skill still applies: sort by `sortOrder`,
  refine with `edit_image` rather than regenerating.

## Delivery

- Show the user the result against their original photo and ask explicitly
  whether the product/person reads correctly. This is the one Canvora flow with
  a real-world ground truth to check against.
- Wrong crop or lighting? `edit_image({ instruction: "show the full jar, don't
  crop the label" })` — cheap and design-preserving.

## Quality checklist

- [ ] MCP path confirmed available (or the CLI limitation explained honestly)
- [ ] ≤5 photos, each described
- [ ] Hero photo identified for multi-slide work
- [ ] Brand kit applied to the surrounding design
- [ ] User verified the product/person against the original before publishing
