# Delivery Policy

This file defines the editorial defaults behind sending or not sending a gift.

These are guidelines, not hard rules. OpenClaw should still make the final call based on `SOUL.md`, `USER.md`, prior memory, recent gift history, and today's actual interaction.

## Giftable Days

More giftable by default:

- meaningful emotional change
- visible growth or setback in a repeated topic
- a moment of being unseen, misunderstood, or in need of witnessing
- anniversaries, milestones, and onboarding
- an ordinary day with enough charm or texture to be elevated playfully

Less giftable by default:

- thin repetitive days with no new angle
- days where the gift would feel louder than the moment
- situations where recent gift repetition would make the artifact feel automatic

## Weight Defaults

- `light` when the day is small but still worth echoing
- `standard` for most meaningful daily gifts
- `heavy` for milestones, anniversaries, rich recaps, or especially dense emotional turns
- `skip` when the gift would feel forced, repetitive, or unhelpful

## Repetition Policy

- Do not repeat the same gift form on consecutive days unless repetition is itself meaningful.
- Record the sent gift in `daily-gift/setup-state.json` as a lightweight recent-gifts entry.
- Check the recent-gifts log before selecting a new form.
- Repetition control should consider both `pattern_or_format` and `output_shape`.
- Also track `visual_style` so structurally different gifts do not all collapse into the same look and feel.
- Also track `content_direction` so the system does not default to reflective recap every time.
- Three consecutive gifts with the same `output_shape` should trigger a strong diversity warning even when the named patterns differ.
- Avoid using the same `visual_style` more than `2` times in the last `5` gifts unless repetition is itself the point.
- If the last `2` gifts were both `dark-*`, actively consider a light or colorful style next.
- Treat any combination of `reflect`, `mirror`, and `openclaw-inner-life` as one repetition cluster for balancing purposes.
- If `3` or more of the last `5` gifts fall into that cluster, the next gift should actively shift toward `extension`, `play`, `utility`, `curation`, or `gift-from-elsewhere` unless there is a strong explicit reason not to.
- This balance check is mandatory, not advisory.
- Keep exactly the most recent `30` gifts in the hot log.
- Append older gifts to `daily-gift/gift-history.jsonl` so they remain lightly indexable without bloating the hot state.
- Use the long-term archive for milestones, retrospection, and broader repetition checks rather than loading it on every run.

## Recommended Tagging Examples

Use the same tagging logic in both `recent_gifts` and `gift-history.jsonl`.

These are recommended combinations, not fixed mappings. If a gift clearly wants a different pairing, use the better label. The goal is stable repetition control, not rigid taxonomy.

| `content_direction` | `visual_style` | Usually fits | Example use |
|---|---|---|---|
| `reflect` | `light-warm` | gentle witnessing, onboarding, tender recap | a soft one-screen object reveal that says `我有看到你今天的心情` |
| `reflect` | `dark-cinematic` | night mood, solitude, serious emotional echo | a late-night radio, window, corridor, or rain-lit scene that holds the feeling without overexplaining it |
| `extension` | `minimal-poster` | one sharp recommendation, lyric, quote, or article | a clean poster-like card delivering one thing the user may genuinely want next |
| `extension` | `dark-cinematic` | taste-forward continuation through object or atmosphere | a tuned radio, cassette, ticket stub, or micro-cinema object that carries one curated continuation |
| `compass` | `light-warm` | gentle next steps that should feel caring, not managerial | a `锦囊`, folded note, fortune slip, or envelope containing `2` or `3` soft suggestions |
| `mirror` | `colorful-playful` | proxy-character, species-of-mood, or affectionate exaggeration | a tiny creature, fake UI, or playful metaphor that says `这也太你了` without sounding mean |
| `gift-from-elsewhere` | `pixel-retro` | unrelated delight, tiny game, fun fact, or surprise artifact | a retro mini toy, collectible screen, or tiny interactive curiosity dropped into the day from nowhere |
| `play` | `colorful-playful` | delight-first interaction, joke loop, or celebratory toy | tap-to-bloom, swipe gag, sticker machine, or reveal toy where play itself is the return |
| `utility` | `light-warm` or `minimal-poster` | genuinely useful content for user's work or interests, wrapped in a creative format | fake newspaper with 3 product ideas, recipe card with weekend plan, lab report with competitive analysis, treasure map of learning resources |

## Output Shape Categories

Use compact output-shape tags for repetition detection.

These categories are recommended, not exhaustive.

Prefer reusing one of the recommended categories when it fits cleanly.

If none of them fits, introduce a new `output_shape` label rather than forcing the gift into the wrong bucket, but keep the label:

- high-level rather than overly specific
- stable enough to reuse later
- focused on interaction or structural form rather than surface styling

Good extension examples:

- `spatial-walkthrough`
- `layered-map-exploration`

Bad extension examples:

- `pink-glass-card-stack-with-sparkles`
- `cute-watercolor-scroll-version-2`

Recommended categories:

- `scrollable-card-collection`: themed cards, notes, panels, or fragments arranged on a surface or in a scrolling collection
- `single-scene-animation`: one animated composition or scene with a single dominant frame
- `mini-game`: an interactive game loop or toy mechanic
- `text-play-worldbuilder`: bounded live text play where each user reply expands a shared tiny world
- `text-play-riddle`: bounded live text play centered on clues, guesses, and a reveal
- `text-play-micro-story`: bounded live text play that unfolds as a collaborative or branching mini narrative
- `text-play-roleplay`: bounded live text play where a tiny scene or character performance is the main gift
- `object-reveal`: opening, unfolding, pulling, flipping, or otherwise revealing a physical object
- `terminal-text-art`: code, terminal, log, console, or text-forward display language as the main form
- `generated-illustration`: generated image output used as the centerpiece of the artifact
- `generated-video`: generated or provider-rendered video clip used as the centerpiece of the artifact

Avoid using the same output-shape category more than twice in the last five sent gifts unless repetition is itself the point.

If a custom `output_shape` starts recurring and clearly represents a stable family of gifts, promote it into the recommended taxonomy later.

## Onboarding

- Onboarding usually deserves a gift unless there is a clear reason not to.
- The first gift should establish the relationship tone without overcommitting to one gimmick.

## Milestones

- Important dates can justify a more information-dense artifact.
- Memoir-like recap and data-visualization forms are often strong candidates.
