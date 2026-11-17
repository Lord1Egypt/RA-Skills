# Heat — Browning, Pan Control, and What the Burner Is Actually Doing

Everything in this file follows from one fact: **water boils at 100°C and browning needs ~140°C**. As long as the food's surface is wet, the surface is stuck at 100°C and nothing will brown, however long it sits there. Every browning failure is a moisture-management failure.

**Read `heat_source` and `## Kitchen` in `~/Clawic/data/cooking/memory.md` before giving a preheat instruction**: gas responds instantly and shows a flame, induction responds instantly and shows nothing, and electric coil and glass-ceramic keep delivering heat for a minute after being turned down — the same sentence means three different things.

## The Temperature Ladder

| Temperature | What happens | Where you see it |
|---|---|---|
| 60-70°C | Proteins set; collagen begins to soften | Poached fish, custard, sous vide |
| 100°C | Water boils; upper limit of anything wet | Boiling, steaming, braising liquid |
| 110-120°C | Fat renders freely; slow browning begins | Confit, low roasting |
| 140-165°C | Maillard runs fast — the flavor reaction | Searing, roasting, baking crust |
| 160-180°C | Sugars caramelize | Caramel, onion jam, roasted vegetable edges |
| 175-190°C | Deep-fry window | `frying.md` |
| 200-230°C | Fast roasting, pizza in a home oven | Vegetables, potatoes, chicken skin |
| 230°C+ | Wok hei, broiler, live fire; smoke points reached | `grilling.md` |

Maillard and caramelization are different reactions and both are usually running: Maillard is amino acids plus reducing sugars (meat, bread, coffee, onions), caramelization is sugar alone. Both accelerate with dryness, with alkalinity (a pinch of baking soda on onions or potatoes visibly speeds browning), and with temperature.

## Preheating, Honestly

- **The water-drop test**: a droplet that skitters across the surface as a bead (Leidenfrost) means the pan is above ~180°C — searing hot. A droplet that sizzles flat and evaporates means 100-150°C — hot enough to cook, not to sear.
- **Cast iron takes 5-8 minutes over medium** to heat evenly; it is a heat *reservoir*, not a fast pan, and hot spots persist unless it is given the time. Preheating it on high warps it and burns the seasoning.
- **Carbon steel and thin stainless heat in 2-3 minutes** and lose heat as fast when food goes in.
- **Nonstick should not be preheated empty** — the coating degrades above ~260°C and an empty nonstick pan gets there in about two minutes on high.
- **Induction**: no thermal inertia in the hob and no visual cue. Time the preheat rather than watch it, and remember the pan itself is the only reservoir — thin pans on induction swing wildly.
- **Electric coil and glass-ceramic**: the element holds heat after being turned down. Move the pan off the ring instead of turning the dial, or the "reduce heat" step never happens.

## Pan Loading — the Real Rule Behind "Do Not Crowd"

Food releases moisture. If the pan cannot evaporate it as fast as it appears, liquid pools, the surface temperature crashes to 100°C, and the food steams.

- Leave roughly **a third of the pan floor visible** with food in a single layer. That is the working threshold.
- Every addition drops pan temperature. Adding cold food equal to the pan's own thermal mass can cost 50-80°C, which is why a second batch browns better than the first.
- Mushrooms and spinach release the most water per gram of anything commonly pan-cooked. Either cook them in batches or deliberately drive the water off first at high heat and brown afterward.
- The wok answer is the opposite of the skillet answer: constant motion, tiny batches, maximum heat, ingredients staged and dry. A home burner cannot reproduce restaurant wok heat, so cook 300-400 g per batch, not a kilo.

## Fond and Deglazing

The brown film on the pan is concentrated Maillard product and is worth more than most of what is in the pot. Dark brown is flavor; black is bitterness that will spread through the liquid.

Deglaze with wine, stock, vinegar, beer, or water while the pan is still hot, scraping with a wooden or metal tool as the liquid boils. Reduce the alcohol by at least half or the sauce tastes raw. A pan sauce is deglazing plus reduction plus cold butter off heat (`sauces.md`).

Enameled and stainless pans build the best fond. Nonstick builds almost none — that is what "nonstick" means, and it is the reason a nonstick pan is the wrong tool for a pan sauce.

## Dry Heat Methods and When Each Wins

| Method | Mechanism | Best for | Fails at |
|---|---|---|---|
| Sear | Conduction from a hot surface | Flat surfaces, thin cuts, crust | Anything thick — the outside overcooks first |
| Roast | Hot air, mostly convection | Anything with a shape; hands-off | Small, thin, or delicate items |
| Broil / grill from above | Radiation | Finishing, melting, blistering | Anything needing more than 5-8 minutes |
| Sauté | Conduction plus motion | Small pieces, quick vegetables | Large pieces that need stillness to brown |
| Stir-fry | Extreme heat, constant motion | Tiny uniform pieces, dry ingredients | Wet or crowded pans |
| Convection oven | Forced air, faster surface drying | Multiple trays, roast potatoes, pastry | Delicate cakes and custards — the fan dries and skins them |

Wet heat methods — poach, steam, simmer, braise — cap out at 100°C and never brown, which is why braises are seared first (`sauces.md`).

## Carryover and Residual Heat

Food keeps cooking after it leaves the heat because the outside is hotter than the core. Rule of thumb: **+2-3°C for a steak or chop, +5-8°C for a roast or whole bird, negligible for anything under 2 cm thick**. Carryover rises with mass, with cooking temperature, and with how thick the piece is.

The same physics applies in reverse to pans: a cast iron skillet off the heat will keep cooking eggs for a minute. Move food out of the pan, not the pan off the heat, when the target is a texture rather than a temperature.

## Reading the Sound

- Loud, sharp sizzle: water leaving fast, surface above 140°C — browning is happening.
- Quiet, gentle bubbling: around 100°C — steaming or simmering, not browning.
- Silence with visible steam: the pan cooled below boiling; something wet went in.
- Crackling that turns to sputtering: fat is above its smoke point or water has hit hot oil. Lower the heat or dry the food.

## Smoke Points

| Fat | Smoke point | Use |
|---|---|---|
| Refined avocado | ~270°C | Highest-heat searing |
| Ghee, clarified butter | ~250°C | Searing with butter flavor |
| Refined peanut, sunflower, rice bran | ~230°C | Frying, high-heat wok |
| Refined olive, canola/rapeseed | ~205-240°C | General cooking |
| Extra-virgin olive oil | ~190-200°C | Sautéing, finishing; it does not "become toxic" at a sear, it just loses its aroma |
| Unrefined coconut, sesame | ~175°C | Flavor, not heat |
| Whole butter | ~150°C | Milk solids brown then burn; add oil or clarify to raise it |

A fat used past its smoke point tastes acrid and cannot be rescued; discard and start again rather than continuing.

**Write when this kitchen's heat behaves in a way that changed a decision**: the real preheat time for a given pan, a hob ring that runs hotter than the rest, an extractor limitation that rules out high-heat searing, the oven's measured offset — one line each in `## Kitchen` of `~/Clawic/data/cooking/memory.md`, with the date on anything measured (`memory-template.md`). These are the facts that stop the same "why is nothing browning" conversation happening every few months.
