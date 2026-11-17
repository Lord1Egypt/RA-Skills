# Equipment, Appliance Conversions, and Timing a Meal

Equipment answers two questions: what can this kitchen actually do, and in what order does the work have to happen so everything arrives hot at once. Both are more often the limiting factor than skill.

**Read `## Kitchen` in `~/Clawic/data/cooking/memory.md` and `tooling` in `config.yaml` before proposing any method**: what exists, its measured quirks (oven offset, hob behaviour, pan sizes, whether there is an extractor), and what is deliberately absent are all recorded there. Proposing a method for equipment that is not in the kitchen is the most avoidable failure in this skill.

## The Short List That Actually Matters

| Item | Why it earns its space | Buying note |
|---|---|---|
| Instant-read thermometer | Converts every "cook until done" into a number; the highest-value object in the kitchen | Thermocouple types read in 2-4 s; cheap probes take 10-20 s and drift |
| One 26-30 cm heavy skillet | Searing, roasting, pan sauces | Cast iron or carbon steel; stainless if a pan sauce is the priority |
| One 24 cm nonstick | Eggs, fish, pancakes | Treat as a consumable — 2-5 years |
| A heavy 5-6 L pot with a lid | Braises, stock, soup, pasta, deep frying | Enamelled cast iron or a thick-based stainless pot |
| A chef's knife, 20-21 cm | 90% of all cutting | Comfort in the hand beats brand; it must be kept sharp |
| A paring knife and a serrated knife | Detail work and bread | Serrated knives cannot be sharpened easily — replace them |
| Digital scale, 1 g resolution | Every ratio in this skill | A 0.1 g scale as well if curing (`preserving.md`) |
| Two sheet pans | Roasting, traybakes, cooling rack support | Heavy gauge; thin ones warp with a bang |
| A cooling rack that fits inside a sheet pan | Draining fried food, air-drying skin, resting meat | — |
| Oven thermometer | Tells you what the oven is really doing (`baking.md`) | Cheap, and it changes every bake |
| Fine sieve, box grater, microplane, tongs, fish slice, bench scraper | Small tools with no substitute | — |

What is genuinely optional: stand mixer (only for bread and volume baking), food processor, mandoline, pressure cooker, sous vide circulator, air fryer, blender. Each is excellent at a narrow job.

## Pans

- **Cast iron**: enormous thermal mass, slow to heat (5-8 min), holds temperature under cold food. Seasoning is polymerized oil, formed above ~200°C — a thin wipe of neutral oil after drying maintains it. Soap does not destroy modern seasoning; standing water does, and rust is removed with steel wool and re-seasoning.
- **Carbon steel**: cast iron's responsiveness upgrade — lighter, heats in 2-3 minutes, seasons the same way. The professional default for a sauté pan.
- **Stainless (clad)**: no seasoning, oven-safe, and it builds the best fond, which makes it the right pan for a sauce. Food sticks when the pan is not hot enough, not because stainless sticks — preheat until a water drop beads and skitters (`heat.md`).
- **Nonstick**: 180-230°C working range and degrading above ~260°C. Never preheat empty, never use metal tools, never put it in a hot oven or a dishwasher. Replace when the coating is scratched, flaking, or food starts to catch.
- **Copper**: the fastest response of all, and the only real argument for it is sugar work and delicate sauces.
- **Enamelled cast iron**: braising, stews, bread. Do not use it for a hard sear — the enamel stains and can craze.

Pan size matters more than pan brand: food should sit in one layer with about a third of the floor visible. A 24 cm pan will not sear 600 g of anything.

## Knives

- **Sharpening angle**: ~15° per side for Japanese knives, ~20° for German and other Western ones. A whetstone (1000 grit to sharpen, 3000-6000 to refine) is the only method that removes metal correctly; pull-through sharpeners work and take life off the blade.
- **Honing is not sharpening.** A steel realigns a rolled edge and should be used every few uses; sharpening actually removes metal, and a home cook needs it every 2-6 months. That cadence is a `## Due` row.
- A dull knife is more dangerous than a sharp one: it requires force and slips off skins instead of biting.
- Never put a knife in a dishwasher, never leave it in the sink, and dry it immediately. Wooden or end-grain boards are kinder to edges than bamboo, glass, or stone — the last two destroy them.
- Board discipline: one for raw meat, one for everything else, or do the ready-to-eat work first (`safety.md`).

## Appliance Conversions

Every conversion is a temperature offset plus a time factor. Check early the first time and record the offset and time factor that actually worked in `## Kitchen`.

| From → to | Temperature | Time | Watch |
|---|---|---|---|
| Conventional oven → convection | −15 to −20°C | ~−25% | Drying effect: great for pastry and roast potatoes, hostile to custards and delicate cakes |
| Conventional oven → air fryer | −15 to −25°C | ~−20% | Small basket, one layer only; superb for reheating fried food (`frying.md`) |
| Oven braise → pressure cooker | Full pressure ≈ 121°C | ~⅓ of the time | No evaporation, so reduce the liquid by about a third and finish uncovered |
| Oven braise → slow cooker | Low ≈ 90°C, high ≈ 100°C | 6-8 h low, 3-4 h high | No evaporation and no browning; sear separately and hold back liquid |
| Slow cooker → pressure cooker | — | 8 h low ≈ 45-60 min at pressure | Both need the reduction done afterwards |
| Hob simmer → oven | 140-160°C oven | Similar | The oven heats from all sides, so nothing scorches on the base — better for long braises |
| Sous vide → conventional | The bath temperature *is* the doneness | Bath, then a 60-90 s sear | Sous vide cannot brown; the sear is a separate step (`meat.md`) |
| Microwave → oven for reheating | 150-180°C | 3-5× longer | The microwave is faster; the oven is the only one that restores crispness |

Pressure-cooker specifics: it needs at least ~250 ml of liquid to come to pressure, it does not brown (use the sauté function first), and the pressure release method matters — natural release for meat and pulses so they do not seize, quick release for vegetables so they do not overcook. Time starts when pressure is reached, not when the lid goes on.

Slow-cooker specifics: it never boils, never reduces, and never browns. Sear meat and sweat aromatics in a pan first, cut the liquid to roughly half the stovetop amount, add dairy and delicate herbs in the last 30 minutes, and reduce the sauce separately at the end. Raw kidney beans must be boiled hard for 10 minutes before they go in (`safety.md`).

Sous vide specifics: the bath temperature is the final temperature, so it cannot overcook on doneness — it can overcook on *texture*, since enzymes keep working over hours. Steak 54°C for 1-4 h; chicken breast 60-65°C for 1-4 h; pork shoulder 74°C for 18-24 h; eggs 63-65°C for 45-60 min. Dry the surface hard before searing, or the sear steams (`safety.md` has the pasteurization table that makes the low temperatures legitimate).

## Small Kitchens and Missing Kit

- **No oven**: hob braises, one-pan dishes, flatbreads in a dry pan (`bread.md`), a covered pan as a makeshift oven for small bakes, and a grill or air fryer for anything that needs radiant heat.
- **Two burners**: build the menu around one dish that holds (a braise, a traybake) plus one that is finished last. Anything needing three simultaneous pans is out.
- **No extractor**: high-heat searing and wok work set off alarms and coat the room. Braise, roast, or open a window and accept the trade — this is a `## Kitchen` constraint, not a preference.
- **One good pan**: choose the metal one. Eggs are learnable in stainless or carbon steel; a sear is impossible in nonstick.
- **No thermometer**: everything gets harder and less repeatable. If one purchase can be recommended, it is this one.

## Timing a Meal

Work **backwards from the serving time**, and let exactly one dish need the final five minutes.

1. Write the serving time at the bottom of the list.
2. Place each dish by its finish time, counting back through its total time — including resting, which is real time in the plan (`meat.md`).
3. Mark every **contended resource**: the oven at one temperature, the number of burners, the sink, the one large pot, and your own attention. Contention, not cooking time, is what makes meals arrive late.
4. Move everything possible earlier. Dishes that hold well: braises, soups, roast vegetables (reheat hot and fast), grains, dressings, sauces, desserts, anything cold. Dishes that do not hold: fried food, green vegetables, pasta, fish, anything with a crust, soufflés.
5. Identify the one dish that must be finished at the last moment and protect the time it needs.
6. Prep everything cuttable in advance. *Mise en place* is not tidiness; it is what makes a five-minute finish possible at all.
7. Warm the plates. It buys several minutes of tolerance at the end and costs nothing.

Two forecasting rules from experience: a first attempt at a dish takes roughly **1.5× its stated time**, and oven capacity is the constraint that surprises people — two trays that both need 220°C convection with airflow will not both cook to plan.

**Write the timing you actually achieved**: `Planned / actual` in the row in `cooks/<year>.md`, because the estimate for the next dinner comes from that pair and nowhere else. Equipment bought, retired, sharpened, re-seasoned, or found to be the problem goes in `## Kitchen` of `~/Clawic/data/cooking/memory.md`, with its maintenance cadence as a `## Due` row; a run-sheet that held for a multi-dish meal is an `artifacts/` file with its `## Boxes` line in the same turn (`memory-template.md`).
