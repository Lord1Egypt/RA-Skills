# Baking — Cakes, Cookies, Pastry, and the Chemistry Behind Them

Baking is a ratio system with an oven attached. Cooking tolerates improvisation because you can taste and correct; baking cannot, because every correction happens after the structure has set. The two most common causes of failure are not technique at all: **an oven that lies about its temperature** and **flour measured by volume**.

**Read `## Kitchen` in `~/Clawic/data/cooking/memory.md`, and `oven_type` and `altitude_m` in `config.yaml`, before giving any temperature or time**: the measured oven offset, the pan sizes that exist, and the altitude correction are all recorded there, and every number below shifts with them.

**Contents:** [The Two Silent Errors](#the-two-silent-errors) · [Leavening](#leavening) · [Mixing Methods](#mixing-methods) · [Flour](#flour) · [Sugar, Fat, Eggs](#sugar-fat-eggs) · [Pans and Scaling](#pans-and-scaling) · [Doneness](#doneness) · [Pastry](#pastry) · [Altitude](#altitude) · [Diagnostics](#diagnostics)

## The Two Silent Errors

**The oven.** Home ovens routinely run 15-25°C away from their setpoint and cycle ±10°C around it, and the display is a thermostat's opinion, not a measurement. Put a separate oven thermometer in the middle of the rack, let it stabilize for 20 minutes at 180°C, and record the difference in `## Kitchen`. Every baking recipe afterward is corrected by that one number. Ovens also have a hot side; rotate trays at the halfway mark.

**Flour by volume.** One cup of flour is 120 g spooned in and levelled, and up to 150 g scooped straight from the bag — a 25% error that reads as "this recipe is dry" or "the dough will not come together". Weigh it, or spoon and level. If `measure_by: volume` is set, the conversions are in `substitutions.md` and every cup of flour is stated as spooned-and-levelled.

Convection: reduce the temperature by **15-20°C** and expect roughly **25% less time**, and start checking earlier than that. Convection dries surfaces, which is excellent for pastry, roast potatoes, and cookies with crisp edges, and hostile to delicate cakes, custards, and soufflés.

## Leavening

| Agent | Amount | Needs | Timing |
|---|---|---|---|
| Baking powder (double-acting) | 1 tsp per 120 g flour | Nothing — it carries its own acid | One rise in the bowl, one in the oven |
| Baking soda | ¼ tsp per 120 g flour | An acid: buttermilk, yogurt, brown sugar, molasses, cocoa (natural, not Dutched), honey, citrus | Reacts immediately — get it in the oven |
| Both together | Powder for lift, soda for browning and pH | — | Common in cookies and pancakes |
| Yeast | See `bread.md` | Time and temperature | Hours |
| Mechanical (creaming, whipped eggs) | — | Air beaten in and held by fat or protein | Do not deflate it folding |
| Steam | — | High initial heat, wet dough | Choux, popovers, puff pastry |

- Baking soda is roughly **3-4× as strong** as baking powder and must be neutralized by an acid, or the crumb tastes soapy and metallic and browns too dark.
- Substitute: 1 tsp baking powder = ¼ tsp baking soda + ½ tsp cream of tartar.
- Too much leavening makes a cake rise fast and collapse, with a coarse, crumbly texture and a bitter edge — it is a top-three cause of sunken cakes.
- Baking powder loses potency; test it by dropping ½ tsp in hot water — vigorous fizz or replace it. Ground spices and leavening both earn a `## Due` row.
- **Dutch-processed cocoa is alkalized** and will not react with baking soda; a recipe that uses soda with cocoa assumes natural cocoa. Swapping them changes both rise and colour.

## Mixing Methods

| Method | How | Produces | Used in |
|---|---|---|---|
| Creaming | Beat soft butter and sugar 3-5 min until pale | Air cells that leavening expands | Butter cakes, most cookies |
| Reverse creaming | Fat rubbed into dry, liquids last | Tender, fine, tight crumb | Wedding-style layer cakes |
| Muffin | Wet into dry, mix until *just* combined | Fast, slightly coarse | Muffins, pancakes, quick breads |
| Foaming | Whole eggs or whites whipped, flour folded | Light, dry, springy | Génoise, sponge, angel food |
| Rubbing in | Cold fat cut into flour in flakes | Layers and flakiness | Scones, shortcrust, biscuits |
| Melted / one-bowl | Melted butter or oil, minimal mixing | Dense, moist, chewy | Brownies, some cookies |

Overmixing after the flour goes in develops gluten and turns cake into bread — tough, tunnelled, and rubbery. The muffin method's "lumps are fine" is a real instruction, not permission to be sloppy.

Butter temperature is a hidden variable: creaming needs butter at 18-20°C (it holds air; melted butter cannot), pastry needs it fridge-cold, and cookie spread is governed almost entirely by how warm the dough was when it hit the oven.

## Flour

| Flour | Protein | Behavior |
|---|---|---|
| Cake | 7-9% | Tenderest; often chlorinated, which lets it hold more sugar and fat |
| Pastry | 8-10% | Between cake and all-purpose |
| All-purpose / plain | 10-12% | The default; brands vary by 1-2 points, which is visible in bread |
| Bread / strong | 12-14% | Chew and structure (`bread.md`) |
| Whole wheat | 13-15%, but bran cuts gluten | Absorbs more water; substitute at most 50% without adjustment |
| 00 | Varies; very fine grind | Extensible, for pizza and pasta |

More protein and more mixing means more gluten means more chew. Cake substitution: replace 2 tbsp of every 120 g of all-purpose with cornstarch to approximate cake flour.

## Sugar, Fat, Eggs

- **Sugar** is not only sweetness: it tenderizes by competing for water, holds moisture (so cakes stay soft), promotes browning, and lowers the freezing point in frozen desserts. Cutting sugar by more than about a quarter changes structure, not just taste.
- Brown sugar is white sugar plus molasses: acidic (so it reacts with baking soda), hygroscopic (so cookies stay chewy), and slightly heavier per cup.
- **Fat** shortens gluten strands — hence "shortening". Butter is ~16-18% water, which is why butter-for-oil swaps change both texture and hydration: substituting oil for butter uses roughly 75-80% of the weight, and the crumb comes out denser and moister with no creamed air.
- **Eggs** do four jobs: structure (protein), richness (yolk fat), leavening (whipped air), and emulsification (lecithin). A whole large egg is about 50 g out of the shell (30 g white, 20 g yolk) — the reliable way to scale a recipe by anything other than whole eggs.

## Pans and Scaling

Batter depth, not batter volume, decides the bake time. Scale by **area** and keep the depth constant.

| Pan | Area | Relative capacity |
|---|---|---|
| 20 cm round | ~314 cm² | 1.0× |
| 23 cm round | ~415 cm² | 1.3× |
| 20 cm square | 400 cm² | 1.27× |
| 23 cm square | 529 cm² | 1.7× |
| 23×33 cm rectangle | 759 cm² | 2.4× |
| Two 20 cm rounds | ~628 cm² | 2.0× |

Fill cake pans about two-thirds. A deeper pan needs a lower temperature and a longer time, or the outside sets before the middle rises. Dark and nonstick pans absorb more radiant heat — drop 15°C. Glass insulates and holds heat, so it bakes slower and keeps cooking after it comes out.

## Doneness

- Internal temperature is the most reliable test: most butter and sponge cakes are done at **96-99°C**, cheesecake at 65-70°C, enriched bread at 88-91°C, lean bread at 96-99°C.
- The skewer test fails on very moist cakes and on chocolate ones where a melted chip reads as batter. Use it as a second opinion.
- Springback and the edges pulling from the pan are late signals — by the time both are unmistakable, a delicate cake is often already dry.
- Cool in the pan 10 minutes, then on a rack. Cooling in the pan to the end steams the bottom soft; turning out immediately can tear a warm crumb.
- Never open the oven in the first two-thirds of a cake's bake: the temperature drops 20-30°C and a structure that has not set collapses.

## Pastry

- **Shortcrust**: 3 flour : 2 fat : 1 water by weight. Cold fat in visible pieces makes flake; fat rubbed in completely makes a sandy, cookie-like crust. Both are valid, and they are different products.
- Rest pastry 30 minutes in the fridge before rolling and again after lining the tin — resting relaxes gluten and is what prevents shrinkage on the sides.
- **Blind bake** any wet filling: lined with paper and weights at 190-200°C for 15-20 minutes, then uncovered until dry. An egg-white wash on the hot base seals it against a soggy bottom.
- **Puff and laminated dough**: everything depends on the butter staying in continuous sheets, which means keeping the dough at 15-18°C and chilling between turns. Butter that melts into the dough gives bread, not layers.
- **Choux**: cook the paste on the hob until it films the pan (drives off water), cool to about 60°C, then beat in eggs one at a time to a `V` that falls slowly from the spatula. Bake hot to raise it, then lower to dry it, and never open the oven early.
- **Pie thickeners**: cornstarch for clarity, flour for opacity, tapioca for fruit that weeps. Acidic fruit weakens cornstarch — use more, or use tapioca.

## Altitude

Above roughly 1,000 m (3,000 ft), water boils lower — about 1°C for every 285 m — leavening gases expand more, and moisture evaporates faster.

| Altitude | Leavening | Liquid | Oven | Sugar |
|---|---|---|---|---|
| 1,000 m | Reduce by ~⅛-¼ | +1 tbsp per 240 ml | +10°C | Reduce ~1 tbsp per 200 g |
| 1,500-2,000 m | Reduce by ~¼-⅓ | +2 tbsp | +10-15°C | Reduce ~1-2 tbsp |
| 2,500 m+ | Reduce by ~⅓-½ | +3-4 tbsp | +15-20°C | Reduce ~2-3 tbsp |

Also: strengthen the structure (an extra egg, slightly more flour), and expect anything boiled or simmered to take longer, because the boiling point itself is lower. Set `altitude_m` once and every number above applies automatically.

## Diagnostics

| Symptom | Cause | Fix |
|---|---|---|
| Cake sunken in the middle | Oven opened early, too much leavening, underbaked, or oven too cool | Verify the oven with a thermometer first; then cut leavening |
| Cake domed and cracked | Oven too hot, or too much flour | Lower 15°C; strips of damp cloth around the pan even it out |
| Dense, heavy crumb | Old leavening, overmixed after the flour, or cold ingredients that broke the emulsion | Test the leavening; bring eggs and dairy to room temperature |
| Dry cake | Overbaked, too much flour (scooped), or too little sugar/fat | Weigh; bake to internal temperature |
| Tunnels and a rubbery texture | Overmixed — gluten developed | Mix to just combined |
| Cookies spread into one sheet | Butter too warm, dough not chilled, too little flour, or a greased hot tray | Weigh flour; chill 30-60 min; use a cool lined tray |
| Cookies stayed in domes | Too much flour, dough too cold, or oven too hot | Flatten before baking; check the oven |
| Soggy pie bottom | No blind bake, wet filling, or no bottom heat | Blind bake, egg-white seal, metal pan on a preheated tray or the oven floor |
| Pastry shrank in the tin | Gluten not rested, or stretched into the tin | Rest twice; ease it in rather than pulling |
| Bread-like cake, tough | Gluten from overmixing or a high-protein flour | Cake flour, gentler mixing |
| Burnt bottom, pale top | Dark pan, oven with strong bottom heat | Move up a shelf, double the tray, drop 15°C |

**Write the oven offset the day it is measured** — a `## Kitchen` line in `~/Clawic/data/cooking/memory.md` with the date and the setpoint it was measured at, because every future bake is corrected by that number. A cake or pastry recipe that finally worked, with the pan and the real oven temperature used, is an `artifacts/` file; the next re-check of the oven is a `## Due` row (`memory-template.md`).
