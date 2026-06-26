# Image generation: try-on + lookbook

This skill produces three kinds of imagery using OpenAI's image API (`gpt-image-2`, released 2026-04-21):

1. **Try-on** — single photo of the customer wearing one outfit in one setting.
2. **Lookbook** — 3–5 try-on images for the same trip/event, varied poses + framings, shareable as a single grid or PDF.
3. **Flat-lay** *(fallback)* — collage of product images alone, no customer in frame, used when there's no reference photo.

> **Companion docs:**
> - `references/style-reasoning.md` — the *why* engine. Every garment in a lookbook needs a one-sentence rationale that touches climate fit, formality fit, and personal/classic angle. Render it next to each look in the lookbook output.
> - Pull setting/composition strings from `GET /mcp/lookbook/settings?occasion=…&season=…&region=…` rather than hand-writing them. The endpoint returns curated `looks[]` with `setting`, `composition`, recommended `size` and `quality`. Use those verbatim in the SETTING and COMPOSITION blocks of the prompt template below.
> - When the customer doesn't specify a setting, use a Buck Mason on-model lifestyle image as an additional reference (pulled from `GET /mcp/products/:id/imagery` → `hero` field) and tell the model "match the backdrop and lighting of the last reference image." This anchors the scene in the brand's own visual language.

## Inputs

The pipeline takes **two structured fact sheets** plus a setting, and assembles them into the prompt. Skipping detail in either fact sheet is the single biggest cause of identity drift and garment hallucination — fill them out before generating.

| Input | Source | Required? |
|---|---|---|
| **Identity anchor photos** (2–3) | `profile.md` → `reference_photos` | Yes; without them, fall back to flat-lay (no try-on) |
| **Build fact sheet** (height, weight, build, shoulder/torso/leg ratios, posture, age range) | `profile.md` → Build + Face sections | Yes |
| **Face fact sheet** (hair, beard, eye color, skin tone, glasses, distinguishing features) | `profile.md` → Face section | Yes |
| **Garment fact sheet** (per item: structure, fabric, fit, weight, color, construction) | `/mcp/products/:id` + `/mcp/products/:id/imagery` | Yes |
| Product flat-lay images (one per garment) | `/mcp/products/:id/imagery` (`try_on` or `hero` field) | Yes |
| Setting description | `/mcp/lookbook/settings?occasion=&season=&region=` | Yes |
| Style notes (fit prefs, color avoid list) | `profile.md` → fit/color prefs, plus event dress code | Recommended |

### Identity anchor photos — selection rules

**Image input order matters.** Send garments FIRST, identity references AFTER. Reasoning: `gpt-image-2` treats the most photographically-complete reference image as "the answer" and tends to copy its outfit, backdrop, and pose verbatim. Garments-first reverses that bias.

**Never include fully-dressed reference photos for try-on lookbooks.** This was learned the hard way: a clean LA street photo (subject in olive overshirt + white henley + black jeans against a brick wall, golden-hour light) was passed as identity anchor #1 in a 7-reference call. `gpt-image-2` produced 5 lookbook images that ALL copied that outfit, that backdrop, that lighting — completely ignoring the actual product flat-lays for shirt and pant, and the chateau / vineyard / dinner setting prompts. Use **only** these reference types:

- **Clean front-facing portrait** — head-and-shoulders, neutral expression, even lighting, no sunglasses, no hat. This is the identity anchor.
- **Shirtless full-body** (1–2 shots from different angles) — for true build under clothing. Without these, the model invents a generic male body.
- **Optional**: a contextual face shot (daytime sunglasses on, low light, etc.) for lighting/expression range.

Do NOT include:
- Full-body shots in clean settings with the customer fully dressed (the model will copy the outfit + backdrop)
- Photos in clothing visually similar to anything in the target outfit (it will just resize what's there)
- Group photos (extra people will appear in the generated image)

If only one photo is available, ask for a second before proceeding. One photo gives the model freedom to generalize; two constrains it; three locks it down. The cost difference is negligible.

### Garment image selection — the most common failure mode

Always use `GET /mcp/products/:id/imagery` and read these fields:

- `try_on` — the safest image for image-gen (true flat-lay or close-up detail)
- `try_on_is_flat` — boolean; `true` means it's a real flat-lay against a plain background, `false` means it's a tightly-cropped editorial detail
- `try_on_warning` — populated when there's no good option (only on-model editorial exists)
- `hero` — the marketing/editorial shot, usually on-model — **never use this for try-on**

**Buck Mason's product image #1 is often an on-model editorial shot, not a flat-lay.** Why this matters: when you pass an editorial as the "garment" input to gpt-image-2, the model:

1. Reads the secondary garments visible on the editorial model (e.g. their pants, their shoes) and uses them as input alongside the labeled garment
2. Copies the model's face/build into the generated image as a second person standing alongside the customer
3. Anchors the backdrop to the editorial's studio setting

Concrete failure observed during this skill's bring-up: the Como Cashmere Tee (Faded Indigo) had no flat-lay; agent passed the position-1 editorial (Black male model in dark indigo tee + natural linen pants on a studio backdrop). The generated lookbook had the customer wearing the slate-navy tee with **natural linen pants** (copied from the editorial model) instead of the slate-navy sateen pant that was passed separately. Two looks also rendered with the editorial model as a second person beside the customer.

**Mitigations, in order:**

1. **Trust `try_on` over `hero`** — if `try_on_is_flat` is true, use it directly.
2. **If only an editorial is available**, crop it programmatically to the garment region only:
   ```bash
   # Tee close-up: crop face out (top portion), keep the garment
   magick editorial.jpg -crop 1800x1500+0+450 +repage tee-cropped.jpg
   ```
3. **Add this line to the IDENTITY block** when passing a garment image that contains a model: "Image N may show a model wearing the garment. IGNORE the model's face, body, other garments, and the backdrop. Render ONLY the labeled garment on the actual subject."
4. **Skip the try-on flow entirely** when `try_on_warning` indicates no usable image — fall back to a text-only lookbook with the editorial linked, not regenerated.

### gpt-image-2 hint inventory — observed failure modes & their fixes

Empirically (verified across outfits 3–5), `gpt-image-2` will SILENTLY drop or substitute pieces unless you give it explicit hints. Each row below is a real failure observed during this skill's bring-up — wire the corresponding hint into the prompt for any look that risks it.

| Failure mode | Concrete miss observed | Mitigation hint to wire into prompt |
|---|---|---|
| **Outer-layer dropped** | Asked for jacket-open-over-polo; rendered just the polo + pant, jacket gone (looks 5-2, 5-3 first pass) | Add a `⚠️ CRITICAL JACKET LOCK — NON-NEGOTIABLE` block above the GARMENT section: "The OUTERMOST garment in this image MUST be the [name] from image 1. The image MUST clearly show its [collar / lapel / pocket / closure features]. If you cannot see those features, you have FAILED the brief." Also describe it as fully zipped/buttoned with only a small triangle of the layer below visible — "open" reads as optional and gets dropped. |
| **Long-sleeve rendered short-sleeve** | Asked for LS plaid shirt; got SS camp shirt (look 5-1) | In the GARMENT block say "LONG-SLEEVE button-up — sleeves clearly visible to the wrist, often rolled up to mid-forearm in editorial styling. The shirt is NOT a short-sleeve camp shirt." Add a sleeve-length sentence to the COMPOSITION block too. |
| **Setting drift to studio** | Asked for "moody window-light interior" / "Mediterranean cobblestone street"; got generic clean studio backdrop in 70%+ of cases | gpt-image-2 has a strong studio prior. Mitigations: (1) make the SETTING block longer than the GARMENT block when a specific setting matters, (2) name 3+ concrete background elements ("dark wood door, tan plaster wall, deep shadow on the left"), (3) name the lighting register ("mid-day sun raking from upper-left, warm golden bounce light"), (4) end with "The setting is NOT a studio backdrop." |
| **Bottom-half clothing copied from editorial** | Position-1 image was an editorial of a model in tee + dark jeans; lookbook copied the dark jeans across all 5 looks | Crop the editorial to garment-only with `magick … -crop WxH+X+Y +repage`, OR use `try_on_is_flat` from `/mcp/products/:id/imagery` to pick a true flat-lay first. |
| **Identity drift toward garment-reference model** | Customer rendered with the garment-reference model's skin tone, beard, hands | Always include the explicit IDENTITY HARD CONSTRAINTS block; restate "The subject is [skin tone / age / hair]; do NOT render the model from any garment reference image as the subject." |
| **Setting prompt overridden by reference photo backdrop** | LA street photo passed as identity ref → all 5 looks copied that brick-wall backdrop | Never include a fully-dressed reference photo with a strong backdrop in the identity slot. Only headshots / shirtless / face refs. |
| **Hands/accessories materialize from garment ref model** | Wristwatch + ring + bracelet from editorial model showed up on customer who has none | In IDENTITY: "Do NOT add jewelry, watches, bracelets, or rings unless they appear in the FACE/BUILD references." |
| **Composition drifts to head-on portrait** | Asked for full-body candid lean; got static head-on bust shot | gpt-image-2 also has a strong head-on prior. Be explicit: "Full body, three-quarter angle, weight on back leg, front foot crossed, head turned 30° to camera left." Naming the framing camera ("35mm equivalent" vs "85mm equivalent") helps too — 35mm pulls toward full body. |

**General rule:** if the garment, sleeve length, or setting is non-negotiable, say so explicitly with capitals + "MUST" + "FAILED the brief if not visible." Polite hints get dropped. Aggressive constraints get respected.

### Garment fact sheet — what to extract

For each garment in a look, extract this into the prompt before posting to `/v1/images/edits`:

| Field | Where to get it | Example |
|---|---|---|
| **Color** (named + visual) | `product.color.name` + `product.color.rgb` from `/mcp/products/:id` | "Worn Chambray (faded mid-blue, ~#6E8AA3)" |
| **Fabric content** | `product.description_md` (parse for "% linen / % cotton / % wool…") | "60% cotton / 40% linen" |
| **Weight** | `product.description_md` (search for gsm or oz/sq yd) | "~180 gsm, lightweight summer-weight" |
| **Weave / knit** | description or category (oxford, poplin, twill, herringbone, jersey, ribbed knit, terry…) | "plain weave, slight slub" |
| **Drape** | inferred from fabric + weight | "fluid, soft drape, breathable" |
| **Silhouette / cut** | category + description (camp collar, spread collar, drop shoulder, straight leg, pleated front, etc.) | "camp collar, short sleeve, single chest pocket, natural buttons" |
| **Construction details** | description (single/double-needle, contrast stitching, button material, pocket placement) | "natural shell buttons, single-needle topstitch, slight curved hem" |
| **Fit on body** | product line's fit notation or company-defined fit | "standard fit through chest and waist, regular sleeve length" |
| **Size on this customer** | `profile.md` size for the matching slot | "size L (chest 41–43\")" |

If the structured data isn't present (Buck Mason's item-master FY26 will add explicit fields), parse from `description_md` with a simple regex pass and **list what you couldn't extract** so the prompt is honest about the gaps.

## API call

Use OpenAI's image edits endpoint with multiple input images (`POST https://api.openai.com/v1/images/edits`):

```bash
curl https://api.openai.com/v1/images/edits \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -F "model=gpt-image-2" \
  -F "image[]=@reference.jpg" \
  -F "image[]=@product1_flatlay.jpg" \
  -F "image[]=@product2_flatlay.jpg" \
  -F "prompt=$(cat prompt.txt)" \
  -F "size=1024x1536" \
  -F "quality=high" \
  -F "n=1"
```

For SDK use:

```python
from openai import OpenAI
client = OpenAI()

result = client.images.edit(
    model="gpt-image-2",
    image=[open("reference.jpg","rb"), open("shirt.jpg","rb"), open("pant.jpg","rb")],
    prompt=PROMPT,
    size="1024x1536",
    quality="high",
    n=1,
)
# result.data[0].b64_json — decode and save
```

Notes:
- `model`: **`gpt-image-2`** (snapshot `gpt-image-2-2026-04-21`) — required. The skill standardizes on `gpt-image-2`; do not fall back to `gpt-image-1` (identity drift, weaker garment-color fidelity, lower setting adherence). If the calling org isn't verified for `gpt-image-2`, surface that as an actionable error to the user rather than silently downgrading.
- `size`: `1024x1536` for portrait try-ons, `1024x1024` for square lookbook tiles, `1536x1024` for landscape settings. `gpt-image-2` supports flexible sizes.
- `quality`: use `high` for finals, `medium` for iteration drafts.
- `n=1` per call — call repeatedly with varied prompts for a lookbook rather than asking for n>1 in one call (each image gets a distinct setting/pose).
- `gpt-image-2` adds optional reasoning ("thinking" mode) which improves garment-fidelity and identity preservation for try-on; enable with `reasoning_effort: "medium"` if your client supports it.

### Run multi-look generations in parallel — NOT sequentially

Each look's image-edit call is independent: same identity anchors, same model, just a different garment + setting + composition. **Issue them concurrently** when generating a multi-look lookbook. A 3-look Premium run takes ~30–60s in parallel vs. ~90–180s sequentially — the wallclock saving is the difference between an interactive flow and a customer who wandered off.

```python
import base64, concurrent.futures, pathlib
from openai import OpenAI
client = OpenAI()

def gen_one(look_id: str, prompt: str, image_paths: list[pathlib.Path], out: pathlib.Path):
    """One gpt-image-2 image-edit call. Independent from the others."""
    result = client.images.edit(
        model="gpt-image-2",
        image=[open(p, "rb") for p in image_paths],
        prompt=prompt,
        size="1024x1536",
        quality="high",
        n=1,
    )
    out.write_bytes(base64.b64decode(result.data[0].b64_json))
    return look_id, out

# Fire all looks concurrently. ThreadPoolExecutor is fine here — the work
# is I/O-bound (waiting on OpenAI), GIL doesn't matter, and a small thread
# pool keeps the rate-limit footprint modest.
with concurrent.futures.ThreadPoolExecutor(max_workers=len(LOOKS)) as ex:
    futures = [ex.submit(gen_one, lk["id"], lk["prompt"], lk["images"], lk["out"])
               for lk in LOOKS]
    for fut in concurrent.futures.as_completed(futures):
        look_id, out = fut.result()
        print(f"  ✓ {look_id} → {out}")
```

Bound the pool at the number of looks (typically 2–5) so you don't fan out beyond the actual work. OpenAI's per-user rate limits comfortably absorb a few concurrent image edits; you don't need a semaphore unless you're driving many customers from one key.

**On failure of a single look**: catch + log inside `gen_one`; let the others finish. Premium-tier orchestration falls back per-look (Editorial for the failed one, Premium for the rest) rather than aborting the whole run.

**Don't parallelize across customers from the same OpenAI key** — that's a different concern (rate limit fairness, billing, identity-cache hygiene). Each customer's lookbook gets its own thread pool scoped to that customer's looks; runs across customers stay sequential at the orchestrator level.

## Prompt template

The prompt is **structured into five labeled blocks**, in this exact order. Each block is non-negotiable; never collapse them into prose because the model parses these labels as instructions. Always include the IDENTITY and GARMENT blocks even if they feel redundant — the model uses them to suppress its defaults.

```
IDENTITY — IMMUTABLE
The first <N> images are reference photos of the SAME person taken on different
days. Use ALL of them as identity anchors. The first image is the canonical
face; the others provide additional angles, lighting, and build references.
The generated person MUST be recognizable as this exact individual.

Build:
- Height: <height>
- Weight: <weight>
- Build: <build>
- Shoulder width: <shoulder_width>
- Torso/leg ratio: <torso_length> torso, <leg_length> legs
- Posture: <posture>
- Apparent age: <age_range>

Face:
- Hair: <hair_color>, <hair_style>
- Beard: <beard>
- Eyes: <eye_color>
- Skin: <skin_tone>
- Distinguishing features: <distinguishing_features>
- Glasses: <glasses or "none in this look">

Hard constraints (do NOT violate):
- Do NOT smooth skin into a generic model face. Preserve real skin texture and
  asymmetry from the reference photos.
- Do NOT change hair color, length, density, or part.
- Do NOT change beard density, length, or shape.
- Do NOT make the subject younger, leaner, more symmetrical, or more
  conventionally attractive than the references show.
- Body proportions, shoulder-to-waist ratio, and limb length must match the
  references.
- Do NOT produce a generic AI-male model face. If the generated face has
  smooth-symmetric features, plastic skin, mannequin-like uniformity, an
  unnaturally even jaw, or the "conventionally photogenic" look common in
  image-gen output — that's the failure mode to avoid. The reference photos
  are the source of truth; a generated face that "looks better" than the
  reference is a wrong face.

Face fidelity self-check (perform internally before emitting the output):
1. Side-by-side compare the rendered face with reference image 1.
2. Verify each: hair color + parting, beard pattern + density, eye color,
   apparent age (NOT younger), skin tone, distinguishing features (scars,
   moles, freckles, asymmetry).
3. Verify facial asymmetry from the references (eye spacing, cheek structure,
   jaw line, brow) is preserved — NOT smoothed to bilateral symmetry.
4. If any check fails, regenerate the face region from the references before
   emitting. A face that fails this check would be off-putting to the customer
   (the lookbook is meant to look like THEM, not like a model who shares
   their hair color).

GARMENT — EXACT MATCH
There are <K> garment images that follow the identity references. Render each
exactly as shown.

Garment 1 — <slot, e.g. "Top">:
- Name: <product name>
- Color: <color name> (visual: <visual description, e.g. "faded mid-blue, ~#6E8AA3, slightly cool undertone">)
- Fabric content: <e.g. "60% cotton / 40% linen">
- Weight / hand: <e.g. "~180 gsm, lightweight summer-weight, breathable">
- Weave / knit: <e.g. "plain weave with slight slub texture">
- Drape: <e.g. "soft, fluid, falls away from the body, light wrinkling at stress points">
- Silhouette / cut: <e.g. "camp collar, short sleeve, single chest pocket, slightly curved hem, standard fit through chest and waist">
- Construction details: <e.g. "natural shell buttons, single-needle topstitch, no contrast stitching">
- Fit on this body: size <size> on the build above; <how it sits — e.g. "skims the chest, no bagginess at the waist, sleeve hits mid-bicep">

Garment 2 — <slot>:
<same fields>

Hard constraints (do NOT violate):
- Color must match the product flat-lay exactly. No re-tinting, no shifting toward warmer/cooler.
- Fabric weight must read as described — a 180gsm linen does NOT look like a
  300gsm canvas. Show appropriate drape and wrinkle behavior.
- Do NOT add visible logos, brand wordmarks, contrast stitching, embellishments,
  pocket flaps, or hardware that isn't in the flat-lay.
- Do NOT change the silhouette to a tighter or looser fit than specified.

SETTING
<setting description from /mcp/lookbook/settings>

COMPOSITION
<pose + framing — e.g. "full-body, three-quarter turn, hands relaxed at sides,
eye-level 35mm, shallow depth of field">

STYLE
Photorealistic 35mm editorial color photograph. Natural light. Shallow depth
of field. Faithful skin tones (no Instagram filter look, no over-saturation).
Subtle film grain. No text overlay. No brand marks. No watermarks.
```

### Variations for lookbook

Use the same outfit + reference, vary the prompt's **setting** and **composition** lines across 3–5 calls:

| Look # | Setting variation | Composition variation |
|---|---|---|
| 1 | Establishing shot of the venue | Wide, full-body, walking |
| 2 | Closer environmental detail | Medium, three-quarter, looking off-camera |
| 3 | Interior/transition setting | Seated or leaning, mid-conversation |
| 4 | Golden-hour exterior | Backlit, contemplative |
| 5 *(optional)* | Night/evening | Closer, warm interior light |

Keep the outfit and customer identity consistent. Vary only the world.

## Quality checks

After each generation, eyeball:

1. **Identity drift** — does the face still resemble the reference? If not, increase the weight of the reference by reordering it first and adding "exact face from first image" emphasis.
2. **Garment fidelity** — color/silhouette match the product image? If not, name the color/material more concretely in the outfit line.
3. **Logo invention** — `gpt-image-2` occasionally hallucinates wordmarks on tees/jackets. Add "no text, no brand marks, no logos" in the style line.
4. **Anatomy** — extra fingers/limbs are still possible. If a generation has obvious flaws, regenerate once with the same prompt; don't iterate the prompt.

If 3 regenerations still fail on a look, fall back to **flat-lay** for that look and note it in the lookbook.

## Face verification gate — second-line defense

Prompt-level rules catch some identity drift but not all. Treat every Premium-tier generation as a candidate that has to pass an explicit verification gate **before** it gets stamped into `runs/<lookbook_id>/looks/` and consumed by `scripts/build-html-lookbook.py`. Without the gate, a single bad face can ship to the customer in a hosted lookbook — the trust-damaging failure this whole pipeline exists to avoid.

### The gate

Implementation: **`scripts/verify-face.py`**. Calls GPT-4o-vision with the generated PNG + the customer's reference photos and a strict rubric, returns JSON pass/fail.

Cost: ~$0.01–0.03 per generation (one vision call against ~3 images at 1024px). Compared to the $0.15–0.20 of the gpt-image-2 generation itself, the verification overhead is small change.

Usage:

```bash
python3 scripts/verify-face.py \
  --generated runs/2026-05-09-mellow-la/looks/look1.png \
  --reference ~/Pictures/me-portrait.jpg ~/Pictures/me-fullbody.jpg \
  --threshold 6
# Exit 0 = pass; exit 1 = fail (face drift); exit 2 = inconclusive (low-quality references, etc.)
# Stdout: JSON {overall_pass, scores:{...}, off_putting, reason}
```

### Rubric (what the gate scores)

The vision call asks for a structured JSON response:

```json
{
  "hair_match":      0-10,
  "beard_match":     0-10,
  "eye_color_match": 0-10,
  "skin_tone_match": 0-10,
  "age_match":       0-10,
  "asymmetry_match": 0-10,
  "off_putting":     0-10,   // higher = MORE generic-AI-face / uncanny
  "overall_pass":    true | false,
  "reason":          "one sentence explaining the worst dimension"
}
```

Default threshold (configurable via `--threshold`):
- All match scores ≥ 6
- `off_putting` ≤ 4
- `overall_pass: true`

The gate is intentionally strict because the cost of shipping a bad face (customer sees an off-putting AI-face version of themselves) is higher than the cost of regenerating once or falling back to Editorial.

### Recovery flow

When `verify-face.py` fails (exit 1):

1. **Retry once with a stronger prompt** — re-run gpt-image-2 with reference photo #1 moved to position 0 (highest weight) AND with the verifier's `reason` appended to the IDENTITY block as a directive (e.g., `reason: "the rendered face has smoother skin and softer jaw than the reference"` → append `"Specifically: preserve the reference's skin texture and jaw definition; do NOT soften."`).
2. **If retry also fails**, drop to Editorial tier for THAT look only. The other looks may still be Premium. Note the fallback in the run summary so the customer sees what happened ("Look 02 fell back to Editorial — AI try-on couldn't match the customer's face after 2 attempts").
3. **Don't retry more than once.** A 3rd retry on the same look is throwing money at a model that's not cooperating; the right move is to fall back rather than chase a number.

Inconclusive (exit 2) is a different failure: low-quality references or the verifier itself failing. Surface it as a setup problem, don't auto-fall-through.

### Where it fits in the pipeline

- **Manual / interactive flow** (agent calls gpt-image-2 directly, drops PNGs into `runs/<id>/looks/`): the agent runs `verify-face.py` after each generation, before writing the `.lookbook_id` marker. Marker = "this image is verified-canonical."
- **Headless flow** (`scripts/run-headless-lookbook.py --tier premium --resume-build`): the orchestrator runs `verify-face.py` against every `look<N>.png` in `runs/<id>/looks/` automatically before consuming them. Failures emit a `❌ BLOCKER: face drift on look<N>` summary with the rubric scores; the agent can then regenerate that one look and re-resume.
- **Optional gate**: invoke with `--no-verify` when the customer has explicitly opted out (e.g., they're iterating on prompts and want fast feedback). Default is verify-on.

## Disclosure

Every customer-facing surface that includes a generated image must say (once, near the top or bottom of the lookbook):

> Try-on previews are AI-generated and may not exactly represent fit, color, or fabric. Order with confidence — Buck Mason offers free returns within 30 days.

## Output organization

Save generated assets to:

```
lookbook/
  <YYYY-MM-DD>-<event-slug>/
    profile.jpg              ← customer reference (cached)
    products/
      <product-slug>.jpg     ← cached Shopify flat-lays
    looks/
      look-1.png
      look-2.png
      ...
    lookbook.md              ← human-readable summary with image embeds and shop links
    checkout-handoff.txt     ← plain-English MPP checkout handoff for selected items
```

The customer can re-open the lookbook later, swap items, or send it to a friend.

## Cost notes

`gpt-image-2` is tokenized — input text $5/M, output text $10/M, input image $8/M, output image $30/M (per OpenAI's launch pricing). `quality=high, size=1024x1536` outputs the most tokens. For iterative drafts use `quality=medium` first; switch to `high` only on the final 3–5 lookbook images. A 5-look lookbook at high quality runs roughly the cost of a single Buck Mason shirt, so do the math before bulk-generating speculative content.

The `/mcp/lookbook/settings` endpoint returns ready-to-use `setting` + `composition` strings per look; assemble each into the base prompt rather than handcrafting from scratch.
