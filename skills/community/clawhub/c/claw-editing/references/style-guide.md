# Style guide: the OpenClaw "fresco" look

Everything lives in `scripts/render.py` (core) and `scripts/overlays.py`. The values below are the ones already tuned there; reuse them instead of re-deriving.

## Palette (RGB)
| Token | Value | Use |
|---|---|---|
| BG | (14, 9, 8) | base of the fresco texture |
| RED | (150, 42, 32) | fills (bars, hexagon fills) |
| RED_LIT | (196, 70, 52) | lines, rules, roads, dividers |
| GLOW | (255, 86, 52) | glow halos, connection lines |
| EMBER | (255, 138, 88) | spark core, bullets, highlight text |
| BONE | (228, 216, 194) | titles, icons, primary linework |
| BONE_DIM | (168, 154, 136) | subtitles, secondary lines |
| KICK | (232, 92, 64) | small tracked kicker text |

## Type (macOS system fonts)
- Titles: **Baskerville SemiBold** (`TF_TITLE`). Cards use 104–132 px; lower-third titles 74; name tags 58; section overlays 66; explainer heads 50; items 36.
- Subtitles: **Baskerville Italic** (`TF_ITAL`), 27–42 px, BONE_DIM.
- Kickers: **Avenir Next Condensed DemiBold** (`TF_KICK`), 22–30 px, UPPERCASE, tracked 6–9 px, KICK color, often with short red rules on either side and a spark at the rule's end.
- Kicker conventions: "01 · OPENCLAW 10.1", "03 – 05 · OPENCLAW 10.1", "07 · OPENCLAW ENTERPRISE", "GET INVOLVED", "AVAILABLE NOW".

## Texture and atmosphere
- `make_fresco()`: multi-octave value noise, red blotches, plaster pits, hairline cracks and a vignette. Render it once per card, slightly oversized, with a slow push-in of about 3–3.5% over the card.
- Animated film grain (σ ≈ 3.2, 6 cycling frames). Use 60–70 drifting embers per card.
- The **spark**: a radial red-orange glow, a thin horizontal flare and a white-hot core with a subtle flicker. It's the brand's recurring "point of contact"; put one wherever something connects or ignites.
- The **claw** (`draw_claw`): a procedural lobster claw with segmented arm, serrated fingers and noise texture, pointing right with its tips at the origin. Use it on the title card, the end card and journey/"what's next" cards, reaching toward a spark. Scale 0.6–0.8, entering from off-screen left.

## Clip types and layouts (1920×1080)
| Clip | Layout | Motion |
|---|---|---|
| Title card (`Card` + `em_bookend`) | claw + spark at y≈400, kicker/title/sub centered around y≈790 | claw slides in 0–1.3 s, spark ignites ~0.9 s, kicker 0.35 s, title 0.55 s, sub 0.85 s. Opaque, then a 0.4–0.5 s dissolve into footage |
| End card | same, title "OpenClaw Foundation" only (118 px) | dissolves in over the last 0.3 s of footage, then fades to black over 0.6 s; about 3.3 s long |
| Full-screen section card (shorts / updates) | emblem centered at y≈430, kicker/title/sub at y≈800 | 0.25–0.35 s fade in and out; 2.5–4 s |
| List card ("New in 10.1", "What's Next") | title at top (y≈250–300), a glowing line across the middle with nodes; labels alternate below and above when there are 5 | each node lights up with a spark on the word onset |
| Lower third (`LowerThird`) | bottom-left at x=120: vertical red rule with a spark on top, kicker, title (74), italic sub; dark blurred-oval "smoke" behind for legibility | rule grows 0.1–0.65 s, kicker 0.3 s, title wipes in 0.4 s, sub 0.6 s; out over the last 0.55 s; 3.5–6.5 s |
| Name tag (`PanelTag`) | as a lower third but clipped to one half of a split-screen (panel 0/1), x0 = panel + 64 | same timing, about 6 s |
| Section overlay (`SectionOverlay`) | centered bottom: kicker with rules and sparks either side, title 66 px (+ optional sub), wide smoke oval | 6 s; 8 s for a call-to-action |
| Explainer (`Explainer`) | kicker + title at top (title 78 px at y≈175), drawing centered at y≈620 | every element appears on its word: `beats_src={key: source_seconds}` |

## Explainer vocabulary (reuse these)
- **Columns with a divider** for comparisons (trusted vs untrusted).
- **Boxes with bulleted items** for components (control plane: provisioning, configuration…).
- A **glowing wall** for an isolation boundary; dashed rounded rects for "containers", double outlines with node dots for "clusters".
- A **wandering agent spark** inside a dashed sandbox, with small tool icons.
- A **hub ring** with labeled nodes that "plug in" via glowing lines, for ecosystems and contracts.
- A **tree from one box to icon circles** for drivers and options; dashed placeholder circles for "your own".
- **Two stair-stepped boxes** for "start here → go further"; ember stat text for a punchline number.
- **Horizontal bars plus a dashed gap bracket** for capability and overhang comparisons.
- Earlier emblems in `render.py`: people around a ring linked to a spark (multiplayer), panel with bars and a pin (dashboards), embers converging into a hexagon gem (memory → skills), waveform with radiating arcs (voice), laptop with checklist and incoming dots (setup), road with waypoints and the claw (roadmap), radar sweep lighting hexagon skills (skill discovery, in `examples/short_update_graphics.py`).

## Checks that have caught real problems
- Labels too close together, or within about 60 px of the frame edge: widen spacing or alternate labels above and below.
- Small kickers crowding big titles: kicker y = title_y − 0.95 × title_size.
- Text sitting on a face, or the smoke backing bleeding across a split-screen seam: clip to the panel.
- Labels overflowing their boxes: size boxes to the text plus about 40 px.
