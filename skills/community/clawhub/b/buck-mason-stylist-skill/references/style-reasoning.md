# Style reasoning — why a garment fits an occasion

The skill must surface a one-line **rationale** alongside every recommendation. "It's new and in stock" is not a rationale. The rationale should combine, in this order of priority:

1. **Climate fit** (dry vs humid heat, altitude, transitional weather)
2. **Formality fit** (where the garment lands on the formality scale vs. what the occasion calls for)
3. **Personal-style fit** (the customer's saved tastes from `profile.md` — favored colors, avoided silhouettes, lived-in vs new-school)
4. **Classic-vs-trend balance** (does this hold up beyond this season, or is it of-the-moment?)
5. **Wardrobe-gap fit** (does this fill a hole, or duplicate something they own?)

Surface the rationale as a single sentence per item, plus a short paragraph at the top of the lookbook explaining the overall thinking. Example output:

> **Breeze Cotton Linen S/S Shirt — Worn Chambray.** Cotton-linen blend (60/40) at ~170 gsm — breathes in humid coastal heat without sticking, drapes naturally so it photographs and moves well. Camp collar lands at smart-casual without being a dress shirt, which suits an outdoor vineyard ceremony with no jacket. Faded chambray reads like something you've already owned, which matches your stated preference for lived-in basics over of-the-moment colors.

## Climate matrix

Use this matrix to pick fabric weight, weave, and color per the destination's actual conditions, not just "summer."

| Climate | Fabric to favor | Fabric to avoid | Color guidance |
|---|---|---|---|
| **Dry heat** (LA, Phoenix, Texas Hill Country, Mediterranean inland, Mykonos midday) | linen, lightweight cotton-linen, light-gauge cotton, voile, technical-cotton blends | dense wool, thick chinos, polyester, anything lined | mid to light tones (off-white, oat, stone, faded indigo, sage); whites read as glare-defense, not white-out |
| **Humid heat** (Florida, Gulf Coast, Tokyo summer, Singapore, NYC July) | linen (any blend), seersucker, cambric, tencel/lyocell blends, terry cotton | tight knits, anything synthetic that traps moisture, heavy denim | mid tones over pure whites (sweat shows less); avoid pale beige under direct sun |
| **Coastal mild** (NorCal, Pacific Northwest summer, British Isles July, Mediterranean evening) | layerable cotton, lightweight wool, flannel-cotton, light knitwear | summer-only linen as a single layer | warm neutrals + a contrasting layer; rich blues and olives |
| **Transitional spring/fall** | mid-weight cotton, brushed cotton, light knit, unstructured blazer | summer linen (too light), heavy outerwear (too much) | autumnal mids: olive, tobacco, faded indigo, oat |
| **High-altitude** (Aspen, Santa Fe, mountain Italy) | layered: fine merino base + cotton mid + outer | single-layer summerwear | warm neutrals; avoid fine tropical wools at altitude (cold + sun-thin) |
| **Cold dry** (Mountain West winter) | merino, melton wool, waxed cotton, raw denim | linen, summer-weight anything | classic dark tones, charcoal, deep navy |
| **Cold wet** (PNW winter, NYC late fall) | water-resistant outer + wool base layers | unprotected linen / cotton | darker tones that hide rain marks |

## Formality scale (Buck Mason context)

Buck Mason's catalog covers casual through smart-casual cleanly; formal black-tie is out of scope. Use this scale to match dress code:

| Tier | Level | Buck Mason staples | Examples of when |
|---|---|---|---|
| 1 | **Beach / weekend casual** | tee, linen short, sweat short, slide | day on a boat, beach club, grocery run |
| 2 | **Casual** | henley, slub tee, chino short, denim | weekend brunch, casual social |
| 3 | **Smart casual** | camp-collar shirt, linen pant, suede chukka | outdoor dinner, casual office, Friday meeting |
| 4 | **Smart casual+** | dress shirt (poplin/oxford), wool trouser, leather chukka or loafer | hotel lounge, gallery opening, daytime wedding outdoor |
| 5 | **Cocktail / business** | sport coat or blazer + dress shirt + trouser + leather dress shoe | client dinner, evening wedding, board offsite |
| 6 | **Formal** | not Buck Mason's strength — pair with outsourced suit/tux; only the dress shirt + tie come from BM | black-tie, formal wedding |

When picking, **err one tier dressier** than the explicit dress code if the customer's history shows them upgrading — e.g., past orders include sport coats, profile mentions tucked shirts. Err one tier more casual if their wardrobe skews tee + jean.

## Classic vs trend filter

Every pick should self-identify as one of:
- **Classic** — would have been right for the same occasion 10 years ago and will still be right in 10 years (e.g., poplin oxford, suede chukka, indigo straight-leg jean)
- **Modern staple** — current cut/fabric on a classic shape (e.g., camp-collar shirt — classic 50s shape, rediscovered in 2010s, durable cycle)
- **Of the moment** — strong this season, may date in 2–3 years (e.g., extreme drop-shoulder, baggy pleat with low rise)
- **Personal classic** — what the customer specifically wears on repeat per their profile/order history

For a normal lookbook, mix at least 60% classic + modern staple. For a one-time event (vacation, festival, themed wedding), one "of the moment" piece is fine; never the whole look.

If the customer's `profile.md` includes a `style_ethos:` field (e.g., "lived-in basics, no logos, west-coast heritage workwear") use it to weight the mix — heritage/workwear customers reject of-the-moment pieces almost categorically.

## Pulling the rationale together

In code (or in the agent's narrative output), produce one sentence per pick that touches at least:
- the **climate** angle ("this fabric breathes in humid heat")
- the **formality** angle ("camp collar reads smart-casual without being a dress shirt")
- the **personal/classic** angle ("matches your stated preference for lived-in basics over of-the-moment colors")

Avoid filler like "this versatile piece will be a great addition to your wardrobe." If you can't write a real reason for an item, drop it from the lookbook.

## Worked example

> **Customer**: outdoor wedding in Mykonos in late June, smart-casual, no jacket required. Profile says they prefer linen, mid-tones, lived-in basics, dislike trend pieces.
>
> **Climate**: humid heat with dry sea breeze. Linen and linen-cotton blends are correct. Pure cotton oxford would stick by 6pm.
>
> **Formality**: smart-casual outdoor → tier 3–4. Camp-collar shirt or fine cotton-linen shirt over linen trouser, suede dress chukka.
>
> **Personal/classic**: customer's profile rules out trend pieces. Choose pieces that would have worked at the same wedding 10 years ago — camp collar, straight-leg linen trouser, suede dress chukka.
>
> **Why for each pick**:
> - **Camp-collar shirt, faded chambray** — cotton-linen blend breathes in humid heat without sticking; camp collar lands at smart-casual; faded color reads lived-in, matching your stated preference.
> - **Loomed linen straight trouser, oat** — pure linen handles 80°F+ humidity better than any cotton; oat photographs well at golden hour without competing with the chambray; mid-rise straight cut is the classic Mediterranean wedding pant, not a trend cut.
> - **Suede dress chukka, tobacco** — works as a smart-casual ankle boot with linen, takes a beating on cobblestone aisles, and bridges back to your existing wardrobe so you re-wear it.
