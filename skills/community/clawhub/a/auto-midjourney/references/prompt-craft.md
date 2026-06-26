# Prompt Craft

Use this file when the user wants better Midjourney prompts, parameter guidance, reusable templates, or scenario-specific presets.

## Parameter policy

Use these as the default parameter set for this skill unless the user explicitly wants otherwise:

- `--v 8` because this skill targets the Alpha web V8 flow
- `--raw` when the user wants more literal prompt following
- `--ar <ratio>` to fit the intended output surface
- `--s <value>` to control stylization
- `--c <value>` only when the user wants more exploration/variation across the 4-image set
- `--no <thing>` for common exclusions such as text, watermark, extra fingers, clutter, frame

Do not auto-add `--hd` or `--q 4` by default.

Reason:

- Midjourney's official quality documentation now explicitly mentions V8 Alpha quality values, and the current documented V8 Alpha quality values are `1` (default) and `4`.
- The same official quality documentation notes that combining `--q 4` with `--hd` in V8 Alpha currently costs `16x` more GPU time.
- Midjourney's official legacy-features documentation also lists `--hd` under legacy/high-definition behavior, so it should be treated as a special-purpose override, not a baseline preset.

Inference:

- For the V8 Alpha-focused flow in this skill, `--q 2` should not be recommended as the standard quality bump because the current official V8 Alpha docs list `1` and `4`.
- Treat `--q 4` as an opt-in final-pass override, not a baseline prompt suffix.

## Practical defaults

Use these rough bands for `--s`:

- `--s 50` to `--s 100`: product shots, UI-style renders, packshots, cleaner realism
- `--s 100` to `--s 175`: balanced default for environments and general scenes
- `--s 175` to `--s 250`: editorial, concept art, fashion, more stylized images

Use these rough bands for `--c`:

- `--c 0` to `--c 10`: tighter consistency across the 4 results
- `--c 15` to `--c 30`: broader exploration when ideating directions

## Prompt structure templates

### Portrait

Template:

`[subject], [age / style cues], [pose or framing], [lens / camera feel], [lighting], [background], [mood], [wardrobe / material details]`

Example:

`editorial portrait of a young woman, half body, 85mm lens, soft window light, muted concrete studio background, quiet luxury mood, silk blouse, natural skin texture`

Recommended suffix:

`--ar 4:5 --s 100 --raw --v 8`

### Product

Template:

`[product], [material / finish], [camera angle], [surface], [lighting setup], [background], [brand adjectives], [exclusions if needed]`

Example:

`premium silver perfume bottle, brushed aluminum cap, front three-quarter angle, black glass surface, controlled softbox rim light, dark charcoal background, minimal luxury beauty campaign`

Recommended suffix:

`--ar 1:1 --s 50 --raw --v 8 --no text, watermark, logo clutter`

### Environment

Template:

`[location], [time of day / weather], [camera framing], [hero details], [materials / signage], [mood], [color palette]`

Example:

`cyberpunk tokyo alley, rainy midnight, wide cinematic frame, glowing ramen shop signs, wet asphalt reflections, dense cables and small vending machines, neon teal and amber palette`

Recommended suffix:

`--ar 16:9 --s 100 --raw --v 8`

### Character / Anime

Template:

`[character type], [hair / outfit], [pose], [expression], [setting], [lighting], [render style], [key props]`

Example:

`anime schoolgirl detective, black braided hair, sailor uniform with subtle tactical details, calm direct gaze, clean gray backdrop, soft key light, refined cel shading, small notebook in hand`

Recommended suffix:

`--ar 3:4 --s 125 --raw --v 8`

### Character Sheet / Turnaround

Use this pattern when the user wants character assets, model sheets, turnarounds, split-view layouts, or reusable design references.

Goal:

- one clearly defined character
- explicit view directions
- neutral background
- reduced scene clutter
- wording that nudges Midjourney toward sheet-style composition instead of a narrative shot

Recommended structure:

`Split-view composition: [panel layout]. [close-up section if needed]. [full-body view directions]. [character identity]. [costume]. [props]. [background]. [render style]. [asset-sheet constraints]`

Best practices:

- Say `split-view composition` or `character design sheet` early.
- Explicitly state `front, side, back` or `front, three-quarter, side, back`.
- Use `centered single character`.
- Use `pure white background` or `clean neutral studio backdrop`.
- Add `no duplicate body, no extra limbs, no extra characters`.
- Keep the costume and signature props in every view description.
- Prefer `--raw` and a lower-to-moderate `--s` for asset work.

Useful aspect ratios:

- `--ar 21:9` for wide horizontal sheets that still leave room for a full character
- `--ar 7:3` for more aggressive split layouts with a face panel plus turnaround views
- `--ar 16:9` when the user wants a safer wide format with fewer layout failures

Suggested parameter band:

- `--s 50` to `--s 100`
- `--raw`
- optional `--no duplicate body, extra limbs, extra characters, busy background`

Example:

`Split-view composition: left third is an extreme close-up portrait of Lin, a female cyberpunk memory archivist with pale skin, tired but determined eyes, subtle neural interface scar behind her right ear. right two-thirds shows full-body turnaround views front, side, and back. sleek high-collared dark grey futuristic uniform, soft blue data reflections in the eyes, centered single character, pure white background, high-quality 3D production render, Unreal Engine 5 style, character design sheet, no duplicate body, no extra limbs, no extra characters --ar 21:9 --s 75 --raw --v 8`

## When to consider higher quality

For the current V8 Alpha flow, consider testing `--q 4` only when all of these are true:

- composition is already close
- the user wants final output rather than ideation speed
- the user accepts slower generation and possible higher usage
- the current V8 Alpha workflow is actually the target

Do not recommend `--q 4` or `--hd` for:

- early ideation batches
- prompt debugging
- large prompt sweeps
- cheap exploratory batches

Use plain defaults for ideation first:

- `--q 1` implicit default
- `--raw`
- a deliberate `--ar`
- moderate `--s`
- optional `--c`

## Recommended workflow in this skill

1. Start with a clean scenario preset from `config/presets.example.json`
2. Improve the natural-language prompt body first
3. Use `--ar`, `--raw`, `--s`, and optional `--c` before reaching for quality overrides
4. Only test higher `--q` settings after the baseline composition is already working

## Character asset workflow

For character libraries and reusable art assets:

1. First generate dedicated sheet-style prompts instead of story prompts.
2. Lock the ratio and sheet layout wording.
3. Generate the base character sheet batch.
4. Only after the base look is approved, create story or poster shots from the chosen design direction.
