# Costume Size Chef — Reference

Recipe database design, sizing/safety rules, and group-coordination
logic behind `scripts/costume_chef.py`.

## 1. Recipe schema

Each costume recipe:

```python
{
  "name": "where's waldo",
  "occasions": ["halloween", "book-character", "party"],
  "wearers": ["kid", "adult"],
  "minutes": 10,
  "core": [  # required, each with have/substitute/buy hints
    ("red striped shirt", "striped shirt of any warm color"),
    ("beanie", "any knit hat + tape a paper brim"),
  ],
  "optional": [("round glasses", "paper circles on sunglasses")],
  "safety": [],          # context-specific notes
  "group_themes": ["puzzle", "storybook"],
}
```

Ranking = fraction of core items matched in the user inventory
(substitutes count 0.75, buy-able cheap items 0.4), tie-broken by
build minutes ascending.

## 2. Occasion taxonomy

- **halloween** — spooky/fun, outdoor night conditions apply
- **book-character** — school-safe: no masks (most schools), no
  weapon-look props, character identifiable from a picture book
- **decade-day / spirit-week** — 50s/60s/70s/80s/90s + inside-out
  day, twin day, career day
- **party (adult theme)** — 80s, pirates, movie/canon characters
- **school play** — role-driven; usually coordinated with teacher
  (out of scope for auto-recipes except basics)

## 3. Sizing rules (kid ↔ adult adaptation)

- Oversize-then-cinch: adult recipes on kids = belt/pins/rolled
  cuffs; kid items on adults rarely work — swap to DIY base layer.
- Box costumes: kid box = small moving box (shoulder width +10 cm);
  adult = wardrobe box cut down; arm holes 10 cm circles at rest
  position, NOT shoulder height.
- No-sew joins for kids take 2× the abuse: hot glue + duct tape
  both, stitch-witchery if it must survive a school day.
- Comfort floor: kid costumes must pass the "sit in a car seat"
  test and the "toilet without help" test. If either fails, the
  costume fails at 4 PM.

## 4. Safety rules (context-keyed)

### trick-or-treat
1. Visibility beats theme: reflective tape on ankles (motion
   visibility) + treat bag; glowstick necklace inside a translucent
   costume element = theme-compatible light.
2. Masks vs paint: under 8 → face paint (sightlines); if a mask is
   non-negotiable, widen eye holes and do a 10-step walk test in a
   dark hallway.
3. Flame radius: synthetic fur/polyester melts and sticks — 1 m
   from jack-o-lanterns/candles or LED-only. Cotton burns fast but
   doesn't melt; wool is most flame-resistant of the commons.
4. Cape/fabric length: hem above ankle bone; no trailing pieces on
   stairs/escalators.
5. Cold plan (northern hemisphere): costume sized over a coat, or
   costume = warm base (the classic failure: princess dress +
   parka = sad princess).
6. Props: soft/flexible only; schools commonly confiscate
   weapon-look props including cardboard.

### school events
- No masks (most schools), no face coverage, props per policy.
- Book characters must be recognizable from the FRONT in a class
   photo: the chest/sign/prop carries the identity, not details.

### adult parties
- Mobility check: you will sit, dance, hug; test the costume
  standing AND sitting.
- Driving: capes/box costumes off before driving (sightlines +
  seatbelt geometry).

## 5. Group coordination algorithm

Input: theme + people (ages). Strategy:
1. Theme sets are pre-defined families (wizarding world, superhero
   universe, fruit/vegetables, crayon box, Star-faring saga,
   storybook animals, rock band).
2. Each person gets a distinct member; recipe independence
   maintained — every member works alone if someone's costume
   falls apart.
3. Load balance: the lowest-effort member goes to the least
   crafty/least available person; build minutes distribute across
   households.
4. Photo rule: group reads best with one unifying element
   (matching color base, matching prop class) — the recipe set
   marks that element per theme.

## 6. The BUY discipline

- Consolidated list across all chosen recipes, one store run.
- Priority order: base garment (thrift) > colored accessories >
   face paint > specialty (last resort).
- Wig rule: wigs are the #1 regret purchase (itch, kids remove,
   one-wear). Hat/headband styling replaces them in 80% of
   recipes; mark wig items LAST RESORT on any list.
- Thrift windows: the week BEFORE Halloween is picked over;
   for-next-year buying happens Nov 1 at 50-75% off — the tool
   suggests this when a date is far out.

## 7. Time-budget honesty

Crunch-time recipes are ranked by minutes as a hard filter:
- ≤15 min: assembled entirely from worn/carried items
- ≤30 min: + paper/cardboard elements
- ≤60 min: + paint/glue steps (drying matters — add 20 min pad
  for paint on kids who touch everything)
- 2 h+: construction projects — only sane when NOT the night
  before. The find command refuses to rank these at crunch.
