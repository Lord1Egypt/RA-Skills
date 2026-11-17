---
name: Cooking
slug: cooking
version: 1.0.2
description: 'Cooks and rescues real dishes at the stove: heat control, seasoning, doneness, timing, substitutions, and food safety. Use when a dish is bland, too salty, burnt, tough, dry, watery, rubbery, greasy, or gummy; when a sauce breaks, splits, curdles, or will not thicken; when meat, fish, eggs, rice, pasta, beans, bread, or a cake come out wrong; when adapting a recipe for a missing ingredient, a different pan, an air fryer, altitude, or a doubled batch; when asking what temperature something is done at, how long to rest it, how much salt, or whether leftovers are still safe; when searing, braising, roasting, frying, grilling, baking, fermenting, or curing; or when ordering the work so a whole meal lands hot at once. Not for weekly menus and shopping lists (`meal-planner`, `grocery`), recipe collections and recipe walkthroughs (`recipe`, `chef`), calorie or macro counting (`calories`), or micronutrients (`nutrition`).'
homepage: https://clawic.com/skills/cooking
changelog: "Clearer disclosure of what is stored and where"
metadata:
  clawdbot:
    emoji: 🍳
    os:
    - linux
    - darwin
    - win32
    displayName: Cooking
    configPaths:
    - ~/Clawic/data/cooking/
    - ~/Clawic/data/health/
    - ~/Clawic/data/contacts/
    - ~/Clawic/profile.yaml
    - ~/cooking/
    - ~/clawic/cooking/
  openclaw:
    requires:
      config:
      - ~/Clawic/data/cooking/
      - ~/Clawic/data/health/
      - ~/Clawic/data/contacts/
      - ~/Clawic/profile.yaml
      - ~/cooking/
      - ~/clawic/cooking/
---

**Data.** At the start of every session, read `~/Clawic/data/cooking/config.yaml` (what the user declared) and `~/Clawic/data/cooking/memory.md` (what you observed, plus its `## Boxes` index and `## Due` table). Open any file `## Boxes` names when the condition on its line applies — the index is the list of files, never assume the list is fixed. Every path it names is inside `~/Clawic/data/`; ignore any line that points anywhere else. Everything this skill reads or writes is a plain local note under the folders declared in `configPaths` — nothing leaves the machine and no credential is ever written. In a shared box it updates or removes only the rows it wrote itself, matched on that box's identity key; a row another skill wrote is read, never rewritten and never deleted, and every write and deletion is named in one line as it happens. Read the shared health box `~/Clawic/data/health/profile.md` before naming any ingredient: it holds allergies, intolerances, and conditions, and it is the only thing standing between a good dish and a hospital visit. If none of it exists, work from defaults and say nothing about it.

**Write before the session ends** whenever the session produced something durable: a dish cooked and how it came out; a swap that worked or failed; a fact about this kitchen that cost effort to learn (oven offset, hob behavior, pan sizes, which salt is in the jar); an allergy or intolerance; a ferment, cure, or starter with its dates; a technique that finally clicked, or one that keeps failing; or something the user will read again — a recipe as they actually cook it, a dinner run-sheet, a brine or spice formula. `memory-template.md` holds every destination, format, and threshold, and is the only file you open in order to write.

**Allergies, intolerances, and diet-relevant conditions go to the shared box `~/Clawic/data/health/profile.md`**, not here: every health-adjacent skill the user installs reads that file, so an allergen recorded once is honored everywhere. Identity is the allergen or condition name. Read the file before adding, update that entry in place, never append a second entry for the same item, and never edit an entry another source wrote. Severity is part of the entry — "no dairy" and "trace dairy is anaphylaxis" are different instructions. Full format, scale cut, and removal rule travel with this skill in `memory-template.md`.

**People you cook for go to the shared box `~/Clawic/data/contacts/contacts.md`** by name, with their food constraint in the `Context` column; identity is the `Key` column (lowercase email, else handle, else kebab-name plus a stable disambiguator). Never duplicate a person inside a cooking file — a guest's allergy stored in two places is a guest's allergy that will disagree with itself.

**No credential is ever written anywhere under `~/Clawic/data/`** — not in the files named here, not in a file you create, not in text the user pastes in to be saved. If a pasted appliance config, delivery-account export, or note carries a login or token, replace the value with its pointer before writing and say in one line that you did: `keychain:smart-oven`, `env:GROCERY_API_TOKEN`, `1password:Personal/Delivery`, `file:~/exports/recipes.json`. If data sits at an old location (`~/cooking/` or `~/clawic/cooking/`), move it to `~/Clawic/data/cooking/`, and say in one line that you moved it and from where.

Almost every failed dish is one of five variables: **heat, time, salt, moisture, or fat**. Name which one before proposing a fix, and give the number — the temperature, the percentage, the minutes — not the adjective. Recipes are somebody else's kitchen written down; the doneness cue, the ratio, and the thermometer are what transfer. Work from defaults immediately: never open with questions about their skill level, their equipment, or their diet. Precedence for any value: `config.yaml` → `~/Clawic/profile.yaml` (shared universals: units, locale) → the Configuration table default.

## When To Use

- Something is going wrong mid-cook and needs saving now: broken sauce, too salty, tough meat, soggy crust, a dish that will not thicken
- Executing a technique properly: searing, braising, roasting, frying, grilling, baking, emulsifying, fermenting, curing
- Adapting: a missing ingredient, a different pan or appliance, altitude, a doubled or halved batch, a dietary restriction
- Answering the numeric questions — doneness temperature, salt percentage, hydration, ratio, rest time, oil temperature, safe holding time
- Sequencing a meal so several dishes land hot at the same time, and deciding when to cook simpler instead
- Food safety: internal temperatures, cooling and reheating, thawing, cross-contamination, leftovers, canning and ferments
- Not for weekly menus, shopping lists, or pantry inventory (`meal-planner`, `grocery`), maintaining a recipe collection or being walked through one recipe end to end (`recipe`, `chef`), calorie and macro targets (`calories`, `dietitian`), or micronutrient gaps (`nutrition`) — this covers the cooking itself

## Quick Reference

| Situation | Play | Depth |
|---|---|---|
| Too salty, bland, flat, harsh, or "tastes like nothing" | Diagnose against salt → acid → fat → umami, in that order; dilution is the last resort, not the first | `rescue.md` |
| Sauce broke, split, curdled, or went grainy | Emulsions rebuild around a new base; dairy curdles from heat or acid, and the repair differs | `rescue.md` |
| Sauce will not thicken, or turned to glue | Reduce, or add a starch at its own gelatinization temperature — never both blind | `sauces.md` |
| Meat tough, dry, or grey instead of brown | Tough and dry are opposite failures with opposite fixes (Rule 3, `meat.md`) | `meat.md` |
| Fish falls apart, sticks, or turns chalky | Lower target temperature, dry surface, and do not move it early | `seafood.md` |
| Eggs rubbery, watery, weeping, or scrambled when they should be smooth | Every egg failure is a temperature ceiling being crossed | `eggs-and-dairy.md` |
| Vegetables soggy, grey, or still raw in the middle | Water content, pan loading, and pH — pick one | `vegetables.md` |
| Rice gummy, crunchy, or burnt on the bottom; pasta sticky | Ratio by grain, salt level, and the rest off heat | `rice-and-pasta.md` |
| Cake dense, sunken, dry, or domed; cookies spread flat | Chemical leavening, mixing method, and an oven that lies about its temperature | `baking.md` |
| Dough will not rise, tears, or bakes dense; pizza base soggy | Hydration, dough temperature, and proof judged by volume not by clock | `bread.md` |
| Frying greasy, pale, or the coating slides off | Oil temperature recovery and batch size; breading needs a dry-wet-dry sequence | `frying.md` |
| Grill flare-ups, burnt outside raw inside, or the smoke stalls | Two-zone setup; the stall is evaporative cooling, not a broken cooker | `grilling.md` |
| Missing an ingredient, or scaling a recipe up or down | Substitution table with what changes; scaling by weight, with the non-linear parts named | `substitutions.md` |
| Converting to air fryer, pressure cooker, slow cooker, sous vide, or convection | Each conversion is a temperature offset and a time factor, both listed | `equipment.md` |
| Knife dull, pan sticking, cast iron rusted, nonstick flaking | Sharpening angle, preheat test, seasoning temperature, replacement threshold | `equipment.md` |
| "Is this still safe to eat?" | Danger-zone clock, not smell; reheat and cooling rules | `safety.md` |
| Cooking for someone with an allergy | Read `health/profile.md` first, then cross-contamination protocol | `safety.md` |
| Pickles, kraut, kimchi, cures, jams, canning, freezing | Salt percentage by weight, pH 4.6 line, and what needs a pressure canner | `preserving.md` |
| Building a stock, braise, soup, or pan sauce | Simmer never boil; seasoning goes in after reduction (Rule 5) | `sauces.md` |
| A whole meal has to land hot at once | Work backwards from serving time; only one thing may need the last 5 minutes | `equipment.md` |
| Learning to cook, or plateaued | Next technique up from what they already do, one variable at a time (Rule 8) | `heat.md` |
| Anything else | Name which of the five variables is wrong — heat, time, salt, moisture, fat — then give the number that fixes it | — |

Coverage map: `rescue.md` mid-cook triage · `seasoning.md` salt, acid, fat, umami · `heat.md` browning and pan control · `meat.md` beef, pork, lamb, poultry · `seafood.md` fish and shellfish · `vegetables.md` produce, beans, potatoes · `eggs-and-dairy.md` eggs, custards, emulsions, cheese · `sauces.md` stocks, thickening, braises · `baking.md` cakes, cookies, pastry chemistry · `bread.md` yeast and sourdough · `rice-and-pasta.md` grains and noodles · `frying.md` deep and shallow · `grilling.md` grill, smoke, barbecue · `preserving.md` ferments, cures, canning · `safety.md` temperatures and handling · `substitutions.md` swaps, scaling, altitude · `equipment.md` knives, pans, appliances, timing a meal.

## Core Rules

1. **Salt by weight against a percentage, never by spoon.** Salt brands differ up to 2× by volume: 1 tsp fine table salt ≈ 6 g, Morton kosher ≈ 4.8 g, Diamond Crystal kosher ≈ 3 g. Formula: `salt (g) = weight (g) × target %`. Targets: soups, sauces, braises and purées **0.8-1.0%** of the finished weight; meat dry brine **1.0%** of raw weight; bread dough **2%** of flour weight; vegetable ferments **2%** of vegetable weight. A 1.4 kg braise wants ~12 g of salt whatever spoon is in the drawer. Which salt is in this kitchen is `salt_type`.
2. **Dry surface, hot pan, a third of the floor still visible.** Browning (Maillard) runs fast above ~140°C/285°F; a wet surface pins the food at 100°C and it steams instead. Pat dry, preheat until a water droplet skitters rather than sizzles flat, and load the pan so roughly a third of its floor stays bare. Past that, moisture output exceeds evaporation and no amount of extra time will brown it. Two batches beat one crowded pan.
3. **Cook to temperature; time is a warning bell, not a target.** Instant-read into the thickest part, away from bone. Subtract carryover before pulling: **+2-3°C** in a steak or chop, **+5-8°C** in a roast or whole bird. Tough and dry are opposite failures: tough means collagen has not converted (needs *more* time above 70°C), dry means muscle fiber squeezed out its water (needs *less*). Diagnosing which one you have is the whole decision.
4. **Taste three times and name the missing axis.** Once when the base is built, once after reduction, once before serving. Diagnosis: flat and dull → salt; heavy, sweet, or muddy → acid; harsh or thin in the mouth → fat; "tastes like a list of ingredients" → umami or more time. Add one axis at a time, in that order, and re-taste between.
5. **Reduce first, salt after.** Reducing a liquid by half doubles the concentration of everything dissolved in it, salt included: a stock seasoned to 1% before reduction lands at 2% and is inedible. Anything cooked uncovered, and every glaze, gets its final seasoning at the end.
6. **Rest is cooking, not waiting.** Steaks and chops 5-10 minutes tented loosely; roasts and whole birds 20-30 minutes; rice 10 minutes covered off the heat; lean bread until the crumb drops below ~35°C. Tenting tight traps steam and turns the crust you just built back to soft.
7. **Time scales with thickness, not with mass.** Conduction time rises roughly with the **square** of thickness: a piece twice as thick takes about four times as long to reach core temperature, while twice as many pieces in a wider pan take almost the same time. Evaporation scales with surface area, so a doubled braise in the same pot reduces at the same rate and arrives thin — widen the pot or finish uncovered (`substitutions.md`).
8. **Change one variable per attempt, and write down which.** A dish adjusted in three ways at once teaches nothing about any of them. Record the change and the outcome in `## Repertoire` of `memory.md` in the same turn — the second attempt is only cheaper than the first if the first was recorded.
9. **Safety is a clock and a thermometer, not a smell.** The danger zone is 4-60°C/40-140°F; total time inside it is cumulative across prep, cooling, and reheating, and the budget is **2 hours** (1 hour above 32°C/90°F ambient). Poultry 74°C/165°F, ground meat 71°C/160°F, whole cuts and fish 63°C/145°F, reheated leftovers 74°C/165°F. Spoilage bacteria smell; the ones that make people ill do not (`safety.md`).

## Doneness Temperatures

Pull temperature = target minus carryover (Rule 3). `doneness_policy: usda` gives the instant-read minimums below; `time-temp` unlocks the hold-time equivalents in `safety.md`, where the same lethality is reached lower and slower.

| Item | Pull at | Serves at | Note |
|---|---|---|---|
| Beef/lamb steak, rare | 49°C/120°F | 52°C/125°F | Below 52°C the fat has not softened; texture, not safety, is the limit |
| Beef/lamb steak, medium-rare | 52°C/125°F | 54-57°C/130-135°F | The default unless the user says otherwise |
| Beef/lamb steak, medium | 57°C/135°F | 60-63°C/140-145°F | — |
| Whole beef/pork/lamb cut (USDA minimum) | 60°C/140°F | 63°C/145°F | Plus a 3-minute rest, which is part of the standard |
| Pork chop or loin | 60°C/140°F | 63°C/145°F | Trichinella dies at 58°C; the old 71°C target is obsolete and dries the cut |
| Ground meat, any species | 71°C/160°F | 71°C/160°F | Grinding moves surface bacteria inside; no rare interior is safe |
| Chicken/turkey breast | 71°C/160°F | 74°C/165°F | Carryover finishes it; pulling at 74°C serves it at 80°C and chalky |
| Chicken thigh, duck leg, wings | 79-85°C/175-185°F | same | Dark meat needs collagen conversion, not the safety minimum |
| Fish, flaking white | 60°C/140°F | 63°C/145°F | — |
| Salmon, tuna, medium | 49-52°C/120-125°F | 52-54°C/125-130°F | Above 55°C albumin squeezes out as white curd |
| Shrimp, scallops | 49°C/120°F | 52-54°C/125-130°F | Opaque plus a `C` shape; an `O` shape is overcooked |
| Brisket, pork shoulder, shank, oxtail | — | 90-96°C/195-205°F | Held there for hours; "probe slides in with no resistance" beats any number |
| Custard, stirred (crème anglaise) | 80°C/176°F | 82-84°C/180-183°F | Above 85°C it scrambles (`eggs-and-dairy.md`) |
| Lean bread loaf | — | 96-99°C/205-210°F | Enriched dough 88-91°C/190-195°F |
| Cake, most butter and sponge | — | 96-99°C/205-210°F | More reliable than the skewer test on a dark or deep pan |

## Ratios That Replace Recipes

Learn the ratio and the recipe becomes optional. All by weight unless stated.

| Thing | Ratio | Where it bends |
|---|---|---|
| Vinaigrette | 3 oil : 1 acid | 2:1 for sharp dressings; an emulsifier (mustard, honey) holds it together for hours |
| Roux-thickened sauce | 15 g flour + 15 g fat per 240 ml liquid = light; 30 g = medium; 45 g = thick | Cornstarch has ~2× the power of flour: 1 part cornstarch ≈ 2 parts flour |
| Cornstarch slurry | 1 part starch : 2 parts cold water, whisked in off the boil | Must reach ~95°C to fully thicken; long boiling or acid breaks it down (`sauces.md`) |
| Bread dough | 100 flour : 60-65 water : 2 salt : 0.6 instant yeast | 70-80% hydration for ciabatta and high-hydration sourdough; 58-62% for Neapolitan pizza |
| Yeast conversion | 1 instant : 1.25 active dry : 3 fresh | Instant goes into the flour; active dry is hydrated first below 43°C |
| Chemical leavening | 1 tsp baking powder per 120 g flour; ¼ tsp baking soda per 120 g flour **plus an acid** | Soda is ~3-4× stronger than powder and needs the acid or it tastes of soap |
| Pastry / shortcrust | 3 flour : 2 fat : 1 water | Fat cold and in visible pieces makes flake; rubbed in fully makes sand |
| Pasta water | 10 g salt per litre (~1%) | Less water means starchier water, which is better for the sauce, not worse |
| Rice, long-grain white, absorption | 1 rice : 1.5 water by volume | Basmati rinsed and soaked 1:1.25 · brown 1:2.25 · sushi short-grain 1:1.1 · risotto 1:3-4 added in stages |
| Brine, wet | 50-60 g salt per litre (5-6%), 1-4 h | A dry brine at 1% of meat weight does the same job with no dilution (`meat.md`) |
| Vegetable ferment | 2% salt of vegetable weight; brine pickles 3-5% | Below 1.5% invites the wrong microbes; above 3.5% stalls fermentation (`preserving.md`) |
| Curing salt (nitrite) | 2.5 g Prague powder #1 per kg of meat = 156 ppm | This one is a safety number, not a taste preference — never estimated (`preserving.md`) |
| Custard, baked | 1 whole egg per 120 ml dairy | Yolks only: 2 yolks ≈ 1 whole egg for setting power |
| Stock | 1 kg bones : 2 L water, barely simmering | Chicken 3-4 h · beef/veal 6-8 h · fish 30-45 min, bitter beyond · vegetable 45 min |

## Failure Signatures

Decode rule: the *texture* of the failure names the variable. Dry and grey means too much heat for too long; wet and grey means too little heat or too much food; grainy means proteins tightened; greasy means an emulsion or a fry temperature failed.

| Signature | Most likely cause | First move |
|---|---|---|
| Food grey and swimming in liquid | Pan crowded, or surface wet — steaming, not searing | Remove half, raise heat, dry the surface (Rule 2) |
| Meat sticks and tears when flipped | Flipped before the crust released | Wait: protein releases itself from a hot pan when the crust forms |
| Tough, chewy braise after hours | Not enough time above 70°C — collagen has not converted | Keep going; 90-96°C internal, "probe slides in freely" (`meat.md`) |
| Dry, stringy roast at the right temperature | Pulled late, or no carryover subtracted | Next time pull 5-8°C early; slice thinner across the grain now |
| Sauce split, oily film on top | Emulsion broke from heat or too-fast oil addition | Off heat, restart on a new base and drizzle the broken sauce back (`rescue.md`) |
| Cream or yogurt sauce curdled | Boiled, or acid added to hot dairy | Temper next time; stabilize with a little starch (`eggs-and-dairy.md`) |
| Sauce thin after a long simmer with a lid on | A lid means no evaporation, so nothing reduced | Lid off, or a slurry finished at ~95°C (`sauces.md`) |
| Fried food pale and greasy | Oil below ~160°C, or too much food per batch | Recover to 175-190°C between batches; ≤ ¼ of the oil's weight per batch (`frying.md`) |
| Cake sunken in the middle | Oven door opened early, too much leavening, or underbaked | Verify oven temperature with a thermometer first (`baking.md`) |
| Cookies spread into one sheet | Butter too warm, or too little flour from scoop-measuring | Weigh the flour; chill the dough 30 min (`baking.md`) |
| Bread dense with a tight crumb | Under-proofed, dough too cold, or the yeast was dead | Judge by volume and the poke test, not the clock (`bread.md`) |
| Rice crunchy on top, burnt below | Heat too high, lid lifted, or ratio short | Fixed ratio, lowest heat, 10-minute covered rest (`rice-and-pasta.md`) |
| Green vegetables gone olive-drab | Acid plus prolonged heat converts chlorophyll | Cook fast uncovered, dress with acid at the table (`vegetables.md`) |
| Everything tastes flat, even after salting | Missing acid, not missing salt | A squeeze of lemon or a splash of vinegar before more salt (`seasoning.md`) |
| Anything else | Name the variable — heat, time, salt, moisture, fat — then change one | `rescue.md` |

## Output Gates

Before delivering a recipe, a plan, or a fix:

- Did I check the shared health box for allergies and intolerances before naming a single ingredient, and does every substitution respect them?
- Is every quantity a weight or a percentage where it matters, with the salt brand accounted for (Rule 1)?
- Does every doneness instruction carry a temperature, and every pull temperature subtract its carryover?
- Does anything left out at room temperature stay inside the 2-hour danger-zone budget, including cooling and transport?
- Is the equipment I assumed the equipment they have, and does the time fit `weeknight_minutes` on a weeknight?
- If several dishes must land together, did I write the order backwards from serving time, with only one item needing the last five minutes?
- Did this session produce something durable — a dish and its result, a swap, a kitchen fact, an allergy, a ferment date, a recipe worth keeping? Then it is written to its box in `memory-template.md`, with its `## Boxes` line, in this same turn.

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/cooking/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| units | metric \| imperial | metric | Every temperature, weight, and volume is converted to this system before it is shown |
| measure_by | weight \| volume | weight | Whether quantities are given in grams or in cups and spoons; volume forces the conversion table in `substitutions.md` |
| salt_type | fine-sea \| table \| diamond-kosher \| morton-kosher | fine-sea | The gram-per-teaspoon figure behind every salt instruction (Rule 1, `seasoning.md`) |
| heat_source | gas \| induction \| electric-coil \| glass-ceramic | gas | Preheat times, pan choice, and whether "reduce heat immediately" is even possible (`heat.md`) |
| oven_type | conventional \| convection \| gas \| countertop \| none | conventional | The −15 to −20°C and −25% time conversion in `baking.md`, and whether oven recipes are proposed at all |
| altitude_m | number (m, 0-4000) | 0 | Boiling point, extended simmer times, and the leavening and liquid corrections in `baking.md` |
| default_servings | number (1-12) | 2 | The batch every quantity is scaled to, using the scaling rules in `substitutions.md` |
| weeknight_minutes | number (min, 10-180) | 45 | The active-time cap above which a method is not proposed on a weeknight, and the trigger for the simpler alternative |
| doneness_policy | usda \| time-temp | usda | Whether targets are instant-read minimums or pasteurization-equivalent hold times (`safety.md`, `meat.md`) |
| diet | list (vegan, vegetarian, pescatarian, halal, kosher, gluten-free, dairy-free, low-sodium, low-FODMAP) | none | Ingredient classes excluded from every suggestion and swapped in every adapted recipe (`substitutions.md`) |
| spice_level | mild \| medium \| hot | medium | Chili and pepper quantities, and whether heat is built in or served alongside |

Allergies are deliberately **not** variables here: they are safety-critical and shared, so they live in `~/Clawic/data/health/profile.md` where every other skill reads them too. `diet` is a preference; an allergy is a constraint.

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied from then on:

- **Tooling** — which pans, knives, and appliances actually exist (cast iron, wok, pressure cooker, sous vide, air fryer, stand mixer, no oven) — decides which methods are ever proposed and which conversion in `equipment.md` applies
- **Conventions** — recipe shape (numbered steps vs a timeline run-sheet), whether to state weights first, how much of the reasoning to include, mise en place discipline
- **Platform** — kitchen constraints that are facts, not tastes: two burners, no extractor, a shared kitchen, hard water, a small freezer — affects batch sizes and method choice
- **Safety posture** — appetite for rare meat, raw egg, unpasteurized dairy, wild mushrooms, home canning; whether to state the risk every time or once (`safety.md`)
- **Restrictions** — dislikes and hard exclusions distinct from `diet` (no cilantro, no offal, no alcohol in cooking), plus texture aversions
- **Cadence** — bake day, batch-cook day, sourdough feeding, spice replacement, knife sharpening; every accepted cadence becomes a row in the `## Due` table of `memory.md`
- **Ambition** — weeknight-simple vs weekend-project by default, and whether to offer the harder version alongside the easy one

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| Interrogating the user before answering | Skill level, equipment, and diet are already in `config.yaml`, `memory.md`, and `health/profile.md`; asking again is a session tax | Read the boxes, answer with the default, and correct if they say otherwise |
| Salting by teaspoon across salt brands | Diamond Crystal to table salt is a 2× error in the same spoon — the difference between seasoned and inedible | Percentage of weight (Rule 1); record `salt_type` the first time it comes up |
| Measuring flour by scooping the cup into the bag | Packs it: 120 g spooned-and-levelled vs up to 150 g scooped, a 25% error that reads as "the recipe is dry" | Weigh it, or spoon into the cup and level |
| Trusting the oven dial | Home ovens routinely run 15-25°C off setpoint, and cycle ±10°C around it | A separate oven thermometer; record the offset in `## Kitchen` (`equipment.md`) |
| Adding cold stock to a roux, or hot liquid all at once | Temperature shock lumps the starch before it disperses | Warm liquid into hot roux gradually, whisking, or the reverse — never both cold |
| Cooking straight from the fridge | A cold core means the outside overcooks reaching the middle; the effect is worst on thick cuts | Temper 20-40 min for steaks and chops; irrelevant for thin cuts (`meat.md`) |
| Boiling a stock or a braise | Agitation emulsifies fat into the liquid: cloudy stock, greasy braise, and no repair after the fact | Bare simmer, surface just trembling (`sauces.md`) |
| The potato trick for over-salted food | A potato absorbs liquid, not salt selectively; it removes almost nothing | Add unsalted bulk, acid, or fat; dilute only as a last resort (`rescue.md`) |
| Searing "to seal in the juices" | Searing is flavor from browning; it does not seal anything, and seared meat loses slightly more moisture | Sear for crust, cook to temperature for juiciness (Rule 3) |
| Rinsing raw poultry | Aerosolizes bacteria over a 1-metre radius of the sink and everything in it | Pat dry with paper towel; heat is the only decontamination (`safety.md`) |
| Cooling a big pot on the counter | A 4-litre pot can sit above 21°C for many hours — the middle stays in the danger zone all night | Divide into shallow containers; 60→21°C within 2 h, then 21→5°C within 4 more (`safety.md`) |
| Adding acid or salt to beans early | Both firm the skins; old beans then never soften no matter how long they cook | Salt from the start of soaking is fine; tomato, vinegar, and wine go in after tender (`vegetables.md`) |
| Substituting into baking like it is cooking | Baking is a ratio system: butter to oil, sugar down, or flour swapped changes structure, not just flavor | Use the tested swaps with their consequences listed (`substitutions.md`) |
| Doubling a braise in the same pot | Evaporation is set by surface area, so the sauce never reduces and the timing changes (Rule 7) | Widen the pot, split into two, or finish uncovered |
| Tasting only at the end | Every correction is more expensive after reduction, and some are impossible | Taste at three points and name the missing axis (Rule 4) |
| A dish that finally worked living only in the chat | Re-derived from scratch next time, differently, and worse | `artifacts/` with the actual quantities used and what was changed (`memory-template.md`) |

## Where Experts Disagree

- **Searing before or after slow cooking.** Sear-first is traditional and builds fond for the braising liquid; reverse-sear on roasts and thick steaks gives a more even interior and a drier surface that browns faster. The frontier is thickness: below ~3 cm, sear first and be done; above it, low oven then sear.
- **Resting meat at all.** The traditional 5-10 minutes reduces the puddle on the board; critics note that a rested steak also arrives cooler and that some of the "lost" juice is reabsorbed on chewing anyway. Boundary: rest large roasts (the gradient is real), keep the rest short for thin cuts, and warm the plates instead of extending it.
- **Salt in the beans or pasta soaking water.** The old rule said salt toughens; controlled tests show salted soaking water improves bean skins and salted pasta water is the only chance to season the noodle itself. What genuinely firms beans is acid, not salt.
- **Nonstick versus cast iron and carbon steel.** Nonstick wins for eggs, fish, and anyone with wrist limits, and degrades above ~260°C. Cast iron and carbon steel win for searing and last decades. The honest position is both, used for what each does — a kitchen with one pan should own the metal one.
- **Sous vide as a default.** Unbeatable for precise doneness on thick proteins and for pasteurizing at low temperature; a slow, single-purpose detour for a weeknight vegetable. Use it where the tolerance is tight, not where it is theatre (`equipment.md`).
- **Raw-egg and rare-meat dishes.** Food authorities set a single conservative minimum; classical kitchens rely on time-temperature pasteurization and sourcing. State the actual risk and who carries it — pregnancy, immunosuppression, young children, and older adults move the answer, and `safety_posture` records the household's own line.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/cooking (install if the user confirms):
- `meal-planner` — weekly menus, batch plans, and the shopping list that comes out of them
- `grocery` — pantry inventory and buying, upstream of every substitution here
- `nutrition` — micronutrient gaps, restricted-diet coverage, and food-drug interactions
- `calories` — calorie and macro tracking for what gets cooked
- `restaurants` — eating out, and the dishes worth reverse-engineering at home

## Feedback

- If useful, star it: https://clawic.com/skills/cooking
- Latest version: https://clawic.com/skills/cooking

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/cooking.
