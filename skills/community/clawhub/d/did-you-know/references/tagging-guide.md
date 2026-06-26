# DYK Hook Tagging Guide

## Output schema

```json
{"url": "...", "domain": ["tag"], "tone": "tag", "low_confidence": false}
```

- **url**: the primary URL of the hook (first entry in `urls`)
- **domain**: list of 1–2 tag_ids
- **tone**: a single tag_id
- **low_confidence**: boolean. Set to `true` only when you have genuinely applied the disambiguation rules and still cannot resolve the call. Not for difficult decisions — for unresolvable ones. Expected on 5–10% of hooks at most, mostly tone.

## Per-hook limits

- **domain**: 1–2 tags. Use 2 only when the hook genuinely and equally spans two domains (e.g. a hook about a scientist who won an Olympic medal → `science` + `sports`). Do not use 2 tags because a subject merely touches multiple areas — pick the primary one. Never tag `military_history` + `history` together; pick one.
- **tone**: exactly 1 tag. Pick the dominant emotional register — what a reader primarily feels when they finish the hook.

---

## Domain disambiguation

### `history` vs `military_history`

Use `military_history` when warfare, armed conflict, a battle, a military unit, a weapon, a soldier, or a naval vessel is **central** to the hook — removing the military element would destroy it.

Use `history` when military events are background context but the hook is really about politics, governance, social movements, independence, or cultural change.

> *"The Gouzenko Affair marked the beginning of the Cold War in Canada"* → `history` (espionage/politics, not combat)
> *"HMS Ledbury was ordered two days after the outbreak of WWII"* → `military_history` (the ship is the subject)
> *"Augustin Trébuchon was shot 15 minutes before WWI ended"* → `military_history` (a soldier's death in combat)

---

### `science` vs `medicine_health`

Use `medicine_health` when the hook is primarily about human or animal health, disease, medical treatment, a hospital, a public health programme, or medical biography.

Use `science` for physics, chemistry, biology, ecology, palaeontology, astronomy, geology, and scientific discovery that is not centred on treating illness.

> *"Tipat Halav cut infant mortality rates in pre-state Israel by more than 50%"* → `medicine_health`
> *"Magnetoreception in birds works by quantum effects in their eyes"* → `science`
> *"Lysine malonylation has been linked to obesity and type 2 diabetes"* → `medicine_health` (disease link is the hook)

---

### `animals` vs `nature`

Use `animals` when the hook is primarily about a specific animal species — its behaviour, appearance, biology, or an individual animal's story.

Use `nature` for ecology, environment, climate, weather, natural disasters, plants, and conservation. Plants always go in `nature`, not `animals`.

> *"The ruddy shelduck is a mainly nocturnal bird"* → `animals`
> *"Cape Grim Air Archive has been collecting air samples for 40 years"* → `nature`
> *"Climate change threatens the flora and fauna of the Sacred Himalayan Landscape"* → `nature`

---

### `religion` vs `mythology_folklore`

Use `religion` for living or historically active religious traditions: churches, mosques, clergy, scripture interpretation, religious practice, religious biography, religious institutions.

Use `mythology_folklore` for ancient myths, folk legends, magical beliefs, supernatural creatures, origin stories from pre-modern or indigenous traditions.

> *"Yaakov Ades was the rosh yeshiva of Porat Yosef Yeshiva"* → `religion`
> *"The Bulgarian razkovniche can only be identified by a tortoise"* → `mythology_folklore`
> *"Teonanácatl translates to 'the flesh of God'"* → `mythology_folklore` (Aztec sacred tradition, not a living institution)

Borderline: hooks about medieval Christian practices tend to be `religion`; hooks about Norse, Greek, or indigenous supernatural beings tend to be `mythology_folklore`.

---

### `performing_arts` vs `music`

Use `music` when the hook is about recording, composition, songwriting, production, albums, chart positions, or a musician's biography in a recording context.

Use `performing_arts` when the hook is about live stage performance: opera, theatre, dance, circus, even when the subject is a musician or composer.

> *"Whitney Houston's 'How Will I Know' was originally written for Janet Jackson"* → `music`
> *"Erna Schlüter appeared as Elektra at the Royal Opera House"* → `performing_arts`
> *"Mendelssohn walked out of the premiere of his own opera"* → `performing_arts`

---

### `history` as a last resort

`history` is not a catch-all for anything set in the past. The DYK archive is overwhelmingly historical, so almost any hook *could* be labelled `history` — but that makes it useless as a preference signal.

**Rule:** if the hook is primarily about a person or thing whose domain is identifiable, use that domain even if the context is historical.

- A hook about a 19th-century chemist → `science`, not `history`
- A hook about a Victorian novelist → `literature`, not `history`
- A hook about an old trade route or company → `economics_business`, not `history`
- A hook about a historical battle or warship → `military_history`, not `history`

Reserve `history` for hooks where the *event itself* is the point — a political decision, a social movement, a colonial act, a regime change, an independence struggle — and no more specific domain applies.

---

### `places` vs `history`

Use `places` when the hook is primarily about a specific location's physical characteristics, design, architecture, or current state.

Use `history` when the hook is about events that happened somewhere, even if tied to a named place.

> *"Montpelier Crescent was built facing the Downs, but the view was blocked within ten years"* → `places`
> *"The Sir Ralph Abercromby pub is the only remaining building from the time of the Peterloo Massacre"* → both `places` + `history` is valid here

---

### `economics_business` vs `history`

Use `economics_business` when trade, finance, companies, markets, or commercial activity are the primary subject — even if the events are historical.

Use `history` when economic or commercial events are incidental to a broader political or social story.

> *"Giuseppe Panini turned unsold stickers into a company that produced 150 billion trading cards"* → `economics_business`
> *"Blackwell Hall controlled England's cloth trade until the 19th century"* → `economics_business` (commerce is the point)

---

### `technology` vs `science`

Use `technology` for human-made systems: software, hardware, internet culture, engineering, industrial technology, communications infrastructure.

Use `science` for the discovery or study of natural phenomena.

> *"RPCS3 is a PS3 emulator that runs on a computer"* → `technology`
> *"The circle packing theorem has been used to construct flattened maps of the human brain"* → `science` (mathematical discovery, applied use is incidental)

---

### `journalism` vs `television`

Use `journalism` when the hook is about a newspaper, magazine, radio station, or the act of reporting.

Use `television` when the hook is about a TV programme or streaming show.

> *"Philip Zec nearly had the Daily Mirror shut down with his cartoons"* → `journalism`
> *"Law & Order box sets were released out of order to encourage viewing of season 4"* → `television`

---

## Tone disambiguation

### `straight` vs `surprising`

This is the most important distinction in the tone dimension.

`straight`: a plain factual statement the reader didn't know before. There is no violated expectation — the reader had no prior belief about this that turns out to be wrong. The register is "huh, I didn't know that." No emotional colour beyond mild interest.

`surprising`: the fact actively contradicts what a reasonable person would assume. The reader had an implicit prior belief, and this hook overturns it. The register is "wait, really?"

Test: **could a reasonable person have predicted this?** If yes, or if they simply had no prior belief either way → `straight`. If their intuition would have pointed the other way → `surprising`.

> *"Cuprates have the highest superconducting transition temperature"* → `straight` (you had no prior belief about which material tops this list)
> *"Cape Grim Air Archive has been collecting air samples for more than 40 years"* → `straight` (interesting fact, no expectation violated)
> *"Clavarioid fungi were originally thought to comprise a single genus"* → `straight` (taxonomy; no intuition to violate)
> *"You are more likely to die on or near your birthday"* → `surprising` (your intuition says birthdays are celebratory, not lethal)
> *"The first helicopter flight was in Lisieux, France"* → `surprising` (you'd assume a major aviation hub, not a small Norman town)
> *"Heavy ion fusion was called 'the conservative approach' yet no large-scale system was ever built"* → `surprising` (the label implies it should have been straightforward)

**When in doubt, prefer `straight` over `surprising`.** `surprising` should be reserved for genuine expectation violations. The DYK format means all hooks are things the reader didn't know — that alone does not make a hook `surprising`.

---

### `surprising` vs `quirky`

`surprising`: the fact is genuinely counter-intuitive or unexpected; the primary register is "I had no idea." Not inherently comic.

`quirky`: the incongruity is **funny** — there is a punchline quality, something absurd or ridiculous about it.

Test: would you share this hook with a laugh, or with wide eyes?

> *"You are more likely to die on or near your birthday"* → `surprising`
> *"The Egyptian Communist Organisation was nicknamed 'Mishmish', meaning apricot"* → `quirky`

---

### `quirky` vs `whimsical`

`quirky` has edge or absurdity; it could be slightly bizarre or ridiculous.

`whimsical` is gentle and charming — cute, playful, delightful rather than absurdist. You'd say "how sweet" not "how weird."

> *"Tarrare could eat his own weight in meat every day"* → `quirky` (bizarre, slightly disturbing)
> *"Queen Elizabeth II owned more than 30 descendants of her first corgi Susan"* → `whimsical`

---

### `dark` vs `dramatic`

`dark`: the hook involves **actual** death, violence, persecution, atrocity, or tragedy as an outcome.

`dramatic`: high stakes, tension, near-misses, confrontation — but no tragic outcome described in the hook.

Test: does someone die, suffer, or face serious harm? → `dark`. Is it tense but ultimately OK (or outcome not stated)? → `dramatic`.

> *"Siegfried Translateur died in a Nazi concentration camp"* → `dark`
> *"Verona Marjanović had to run through an airport while bullets were being fired"* → `dramatic` (she survived)
> *"56 paramilitary punishment attacks occurred after the Good Friday Agreement"* → `dark` (ongoing violence)

---

### `inspiring` vs `poignant`

`inspiring`: a person or group overcame structural barriers or achieved something difficult against the odds. Makes you want to cheer.

`poignant`: touching or bittersweet — a moment of quiet emotion, sacrifice, loss with dignity, or human connection. Makes you feel a quiet swell, not a cheer.

> *"Clarice Phelps was the first African-American woman involved in the discovery of a chemical element"* → `inspiring`
> *"Carl Genian wrote to his mother from WWII: 'We're all sick and tired of killing one another'"* → `poignant`
> *"Matthew Carrieri offered to remain a captive in place of others, shocking the pirate into freeing everyone"* → `poignant` (selfless act) or `inspiring` — prefer `inspiring` if overcoming odds is the primary read

---

### When multiple tones seem to apply

Pick the **dominant** register — what a reader primarily feels at the end of the hook.

**Tie-breaking rules:**
- `dark` overrides: if someone dies or is persecuted, tag `dark` even if the hook is also surprising or ironic
- `inspiring` beats `surprising` when a first-ever achievement is by a person from an underrepresented group
- `provocative` is for hooks whose *content* is edgy or taboo — not just for hooks that are surprising or divisive in implication

---

## Common mistakes to avoid

- Do not use `history` for any hook set in the past — use the most specific domain that fits (science, literature, economics_business, etc.); `history` is for political/social/cultural events where no more specific domain applies
- Do not tag `surprising` by default when unsure — use `straight` for plain facts where no prior expectation is violated. `surprising` requires a genuine expectation reversal, not just novelty.
- Do not use `military_history` just because a person served in a war; use it when combat or military operations are the primary subject
- Do not use `mythology_folklore` for all religious content — reserve it for legendary, supernatural, or pre-modern oral traditions
- Do not use 2 domain tags out of caution — if in doubt, pick the most central one
- Do not set `low_confidence: true` for hard calls — only for genuinely unresolvable ones where the disambiguation rules have been applied and the hook still sits at an irresolvable intersection. A committed tag is more useful than a flagged one.
