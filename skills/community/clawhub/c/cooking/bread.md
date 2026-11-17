# Bread — Yeast Doughs, Sourdough, Pizza

Bread is four numbers: hydration, salt, leavening, and dough temperature. Time is the *output* of those numbers, not an input — which is why every recipe that says "prove for one hour" produces different bread in different kitchens, and why judging by volume and feel is not a mystical skill but the only correct method.

**Read `ferments.md` and `## Kitchen` in `~/Clawic/data/cooking/memory.md` before any sourdough work**: the starter's feeding ratio, its peak time in this kitchen, the water hardness, and the flour brand actually in use are recorded there, and all four move the schedule.

**Contents:** [Baker's Percentage](#bakers-percentage) · [Dough Temperature](#dough-temperature) · [The Process](#the-process) · [Judging the Proof](#judging-the-proof) · [Sourdough](#sourdough) · [Shaping and Scoring](#shaping-and-scoring) · [Baking](#baking) · [Pizza](#pizza) · [Enriched Doughs](#enriched-doughs) · [Flatbreads](#flatbreads) · [Diagnostics](#diagnostics)

## Baker's Percentage

Everything is expressed as a percentage of flour weight, and flour is always 100%. This is what lets any recipe scale to any batch size in one multiplication.

| Bread | Water | Salt | Instant yeast | Other |
|---|---|---|---|---|
| Basic white loaf | 62-65% | 2% | 0.6-1% | — |
| Ciabatta, focaccia | 75-85% | 2% | 0.4-0.6% | Olive oil 3-5% |
| Sourdough boule | 70-78% | 2% | — | Levain 15-20% |
| Neapolitan pizza | 58-62% | 2.5-3% | 0.1-0.3% | Long cold ferment |
| New York pizza | 62-65% | 2% | 0.4% | Oil 2-3%, sugar 1-2% |
| Bagel | 52-57% | 2% | 0.5% | Malt 1-2% |
| Brioche | 50-55% (mostly egg) | 2% | 1-1.5% | Butter 30-60%, sugar 8-15% |
| Sandwich loaf | 65% | 2% | 1% | Milk, butter 5-8%, sugar 4-6% |

Yeast conversions: **1 instant : 1.25 active dry : 3 fresh**. Instant goes straight into the flour; active dry is hydrated first in water below 43°C; above ~50°C yeast starts to die.

Hydration is not comparable across flours. Whole wheat and high-protein flours absorb more, so the same 70% can feel slack in one bag and stiff in another. Adjust by feel and record the hydration that worked, named against the flour actually in the cupboard, in `## Kitchen`.

## Dough Temperature

Final dough temperature is the single strongest control over fermentation speed, and almost no home recipe mentions it. Target **24-26°C** for most doughs.

`Water temp = (DDT × 3) − (flour temp + room temp + friction factor)`

DDT is the desired dough temperature; the friction factor is roughly 1-3°C for hand mixing and 5-10°C for a stand mixer. Example: DDT 25°C, flour 21°C, room 22°C, hand mixing (2) → water = 75 − 45 = **30°C**.

A dough at 21°C ferments roughly half as fast as one at 27°C. A schedule that fails "for no reason" in winter is nearly always this.

## The Process

1. **Mix** flour and water, hold back the salt and yeast if autolysing.
2. **Autolyse** 20-60 minutes: flour and water only. Hydrates the flour and lets enzymes begin, so less kneading is needed and the dough is more extensible.
3. **Add salt and yeast**, mix in fully. Salt slows fermentation and tightens gluten — that is a feature, and omitting it produces a slack, fast, bland dough.
4. **Develop the gluten**: knead 8-12 minutes by hand, 5-8 in a mixer, or use stretch-and-folds — four sets, 30 minutes apart, during the first two hours. Folds do the same job with no kneading and suit wet doughs.
5. **Bulk ferment** until the dough has risen **50-75%** and feels aerated and domed. Not "double" — that is over-fermented for most sourdough, and standard only for straight commercial-yeast doughs.
6. **Pre-shape**, rest 20-30 minutes, **shape** with tension.
7. **Final proof**: 1-2 h at room temperature, or 8-16 h in the fridge (cold retard, which also deepens flavor and makes scoring far easier).
8. **Bake** into steam.

The **windowpane test** ends the kneading question: stretch a piece thin enough to see light through it without tearing. If it tears, keep going.

## Judging the Proof

- **Poke test**: press a floured finger 1 cm into the dough. Springs back fast — under-proofed. Springs back slowly and leaves a slight dent — ready. Does not spring back at all and the dough sighs — over-proofed.
- Under-proofed bread bakes dense, with a tight crumb and often a burst side where the dough tore looking for somewhere to expand.
- Over-proofed bread spreads flat, has a pale crust (the yeast ate the sugars that would have browned it), and can smell sharply alcoholic.
- Over-proofed dough can be rescued once: degas, reshape, and give it a short second proof. Twice is a loss.

## Sourdough

- **Starter**: equal flour and water by weight, kept at 24-26°C. A 1:5:5 feed (1 part starter, 5 flour, 5 water) peaks in 4-8 hours; 1:1:1 peaks in 3-4. Peak — domed, bubbly, just before it recedes — is when it goes into the dough. A starter used past its peak makes slack, sour, weak dough.
- Float test as a rough check, not gospel: high-hydration starters sink even when active.
- **Levain** is the portion built for a specific bake; the mother starter is what is kept. Building a levain lets the mother stay small.
- **Fridge storage**: feed weekly. A starter neglected for months usually revives with two or three daily feeds; the dark liquid on top ("hooch") means hungry, not dead — pour it off and feed.
- **Sourness** is controllable: cooler and longer favors acetic acid (sharp, vinegary), warmer and faster favors lactic (mild, yogurt-like). Whole grain and rye ferment faster and sour more.
- Sourdough schedules are temperature-dependent, so a written schedule only transfers within the same kitchen at the same time of year. Record what worked in `## Kitchen`, with the dough temperature next to it.

## Shaping and Scoring

- Shaping builds surface tension, which is what makes a loaf rise up instead of out. Drag the dough on an unfloured patch of counter to tighten the skin.
- Flour the *outside* of the dough and the banneton, never the working surface where tension is being built.
- Score with a blade at a shallow angle (about 30°) and 5-10 mm deep. The cut is where the loaf is told to expand; without it, it bursts along a random seam.
- Cold dough scores cleanly; room-temperature high-hydration dough drags. Another argument for the overnight fridge proof.

## Baking

- **Steam for the first 10-15 minutes** is what gives oven spring and a glossy, crackling crust: it keeps the surface elastic so the loaf can expand before the crust sets. A preheated Dutch oven with the lid on is the most reliable home method; the lid comes off for the last third.
- Preheat properly: 30-45 minutes at 230-250°C for lean bread with the vessel inside. Thermal mass in the base is what gives the burst of bottom heat.
- Internal temperature: **96-99°C for lean breads, 88-91°C for enriched**. Enriched dough at 99°C is dry.
- Cool completely on a rack before cutting. The crumb is still setting and steam is still redistributing; a hot-cut loaf is gummy and goes stale faster.
- Staling is starch retrogradation, not moisture loss, and it is **fastest at fridge temperature**. Keep bread at room temperature in paper or a bread box for two or three days, or freeze it sliced. Refreshing a stale loaf: sprinkle with water, 5-8 minutes at 180°C.

## Pizza

- Home ovens top out around 250-290°C where a Neapolitan oven runs at 430-480°C, so the home strategy is maximum thermal mass: a stone or steel preheated for 45-60 minutes at the oven's maximum, on a high rack, with the grill element for the top.
- Steel transfers heat faster than stone and gives a better base in a domestic oven; stone gives a more forgiving, drier bake.
- Cold ferment 24-72 hours: better flavor, better extensibility, easier handling.
- Stretch by hand from the centre out, leaving the rim untouched. A rolling pin destroys the gas in the cornicione.
- Sauce lightly, cheese moderately. Excess moisture is the entire cause of a soggy centre — drain fresh mozzarella, and pre-cook wet toppings like mushrooms.
- Launch on semolina, not flour: flour burns, semolina rolls.

## Enriched Doughs

Fat, sugar, and eggs all interfere with gluten and slow yeast, so enriched doughs need more yeast, more time, and more mixing.

- Add butter **after** the gluten is developed, a piece at a time, and keep mixing until it is fully incorporated and the dough is smooth again.
- Above ~20% butter, the dough must stay cool or it becomes unworkable; brioche is nearly always mixed cold and proofed cold.
- Sugar above ~10% of flour weight is osmotically stressful to normal yeast — use more yeast, or osmotolerant yeast, and expect slow proofs.
- Enriched loaves brown early because of the sugar and milk: tent with foil once the colour is right and finish to 88-91°C internal.

## Flatbreads

The fastest bread in the repertoire and the answer when there is no oven or no time.

- **No-yeast flatbread**: flour, water or yogurt, salt, a little oil; rest 20 minutes; dry, very hot pan. Ten minutes total.
- **Tortillas**: corn masa harina plus hot water for corn, flour plus fat plus hot water for wheat; the rest is what makes them pliable.
- **Naan and pita**: yeasted, high heat, and pita puffs only when the oven or pan is hot enough to flash the interior moisture into steam — under 230°C it stays flat.
- **Roti and paratha**: laminated with fat between layers, cooked dry then finished with ghee.

## Diagnostics

| Symptom | Cause | Fix |
|---|---|---|
| Dough did not rise | Dead yeast, water too hot, too cold a room, or too much salt in direct contact with the yeast | Proof the yeast in warm water with a pinch of sugar; check dough temperature |
| Dense, tight crumb | Under-proofed, under-developed gluten, or too little water | Windowpane test; judge proof by volume, raise hydration 2-3% |
| Flat, spread-out loaf | Over-proofed, weak shaping, or hydration beyond what the flour holds | Shorter bulk, tighter shaping, stronger flour |
| Burst side, no ear | Under-proofed or unscored | Longer proof; score deeper at a shallower angle |
| Pale, soft crust | No steam, oven too cool, or over-proofed (sugars consumed) | Steam the first 12 minutes; verify the oven |
| Gummy interior | Cut hot, or underbaked | 96-99°C internal, cool completely |
| Huge irregular hole under the crust | Trapped gas from loose shaping | Degas more at pre-shape, shape tighter |
| Sour when it should not be | Over-fermented, or a starter used past peak | Cooler bulk, shorter time, feed the starter and use it at peak |
| Crust too thick and hard | Baked too long, or steam for too much of the bake | Shorter bake at a higher temperature; lid off earlier |

**Write the schedule that worked, with its temperatures**: the starter's feeding ratio and peak time go to `ferments.md` and its feeding cadence to `## Due`; the flour brand, water hardness, and the dough temperature that produced a good loaf go to `## Kitchen`; and a loaf formula in baker's percentages that this kitchen will repeat is an `artifacts/` file with its `## Boxes` line written in the same turn (`memory-template.md`).
