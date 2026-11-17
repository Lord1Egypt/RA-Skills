# Food Safety — Temperatures, the Clock, and Allergens

Food safety is arithmetic, not intuition. The organisms that cause illness do not change how food smells, looks, or tastes — spoilage organisms do that, and they are mostly harmless. Every rule here is a temperature or a duration, and the reason to use them is that the senses give no signal at all.

**Read `~/Clawic/data/health/profile.md` before cooking for anyone**: allergies with their severity, conditions, pregnancy, and immunosuppression all change which of the numbers below are advisory and which are hard limits. Reading it is the first Output Gate in `SKILL.md` for exactly this reason.

**Contents:** [The Danger Zone and Its Clock](#the-danger-zone-and-its-clock) · [Cooking Temperatures](#cooking-temperatures) · [Pasteurization Is Time × Temperature](#pasteurization-is-time--temperature) · [Cooling and Reheating](#cooling-and-reheating) · [Storage Times](#storage-times) · [Cross-Contamination](#cross-contamination) · [Allergens](#allergens) · [Higher-Risk Foods and Who Should Avoid Them](#higher-riREDACTED-SECRET) · [When to Throw It Out](#when-to-throw-it-out)

## The Danger Zone and Its Clock

**4-60°C (40-140°F).** Bacteria multiply fastest around 30-40°C, and the time spent in that band is **cumulative across the food's whole life** — shopping, prep, cooling, storage, transport, reheating, and the buffet table.

| Ambient | Total budget outside refrigeration |
|---|---|
| Normal room, below 32°C | **2 hours** |
| Above 32°C (hot day, car, outdoor table) | **1 hour** |

The clock does not reset by reheating. Food that spent three cumulative hours in the zone is not made safe by being brought back to 74°C, because several relevant toxins — *Staphylococcus aureus* and *Bacillus cereus* among them — are heat-stable and survive cooking. That is the reason a "safe" reheated rice dish still makes people ill.

## Cooking Temperatures

| Food | Minimum internal |
|---|---|
| Poultry, whole or ground; stuffing; any casserole containing poultry | 74°C / 165°F |
| Ground meat of any other species | 71°C / 160°F |
| Whole cuts of beef, pork, lamb, veal | 63°C / 145°F **plus a 3-minute rest** |
| Fish and shellfish | 63°C / 145°F |
| Egg dishes, cooked eggs held for service | 71°C / 160°F |
| Leftovers and anything reheated | 74°C / 165°F, throughout |
| Sauces and gravies reheated | Rolling boil |
| Rice, held after cooking | Above 60°C, or cooled fast and refrigerated within 1 hour |

Measure in the thickest part, away from bone and away from the pan, and check more than one spot in an irregular piece. Calibrate the thermometer in ice water: it should read 0°C ± 1.

## Pasteurization Is Time × Temperature

The single-number minimums above are instant-kill figures. Real lethality is a curve — the same reduction in *Salmonella* is achieved by holding food lower for longer, which is what makes sous vide chicken at 60°C both legitimate and safe. Representative hold times for chicken breast, once the *whole piece* is at temperature:

| Temperature | Approximate hold for equivalent lethality |
|---|---|
| 74°C | Instant |
| 68°C | Under a minute |
| 63°C | ~5 minutes |
| 60°C | ~35 minutes |
| 57°C | ~1.5-2 hours |

This is the basis of `doneness_policy: time-temp`. It requires an accurate thermometer, a genuinely stable temperature, and the whole piece at that temperature for the full hold — a roast that merely passed through 60°C on its way up has held nothing. With `usda` set, quote the instant-read minimum and mention the trade-off; with `time-temp`, state the hold explicitly, and defer to the conservative figure for pregnancy, immunosuppression, young children, and older adults.

## Cooling and Reheating

Cooling is where more home food goes wrong than anywhere else, because a large pot cools far more slowly than intuition suggests.

- **Two-stage rule**: 60°C → 21°C within **2 hours**, then 21°C → 4°C within **4 more**. Six hours total, and the first stage is the one that fails.
- A 4-litre pot on the counter can sit above 21°C most of the night. Divide into shallow containers no more than 5 cm deep, or use an ice bath with stirring, or a frozen bottle in the pot.
- Do not put a large hot pot straight in the fridge: it warms everything around it and cools slowly anyway. Divide first.
- Refrigerate within 2 hours of cooking, 1 hour if the room is above 32°C.
- Reheat to 74°C throughout, once. Reheating the same portion repeatedly walks it through the danger zone every time; take out only what will be eaten.
- Microwaves heat unevenly: stir halfway, rest 1-2 minutes to let the temperature even out, and check with a thermometer in more than one place.

## Storage Times

| Item | Refrigerated at 4°C |
|---|---|
| Cooked leftovers, rice, pasta | 3-4 days |
| Raw poultry, mince, fish | 1-2 days |
| Raw whole cuts of meat | 3-5 days |
| Soups and stocks | 3-4 days (or freeze) |
| Hard-boiled eggs, in shell | 1 week |
| Opened deli meat | 3-5 days |
| Cut fruit and vegetables | 3-4 days |
| Homemade fresh pasta | 1-2 days |
| Opened canned goods, transferred to a container | 3-4 days |

Fridge at 4°C or below, freezer at −18°C, verified with a thermometer rather than the dial. Raw meat goes on the **bottom shelf**, in a container, so nothing can drip onto anything below it.

Rice deserves its own note: *Bacillus cereus* spores survive cooking, and germinate in rice left at room temperature, producing a heat-stable toxin. Cool cooked rice within an hour, refrigerate, keep no more than a day or two, and reheat thoroughly once.

## Cross-Contamination

- Separate boards and knives for raw meat and everything ready-to-eat, or do all the ready-to-eat work first.
- Wash hands for 20 seconds with soap after handling raw meat, eggs, or unwashed produce, and after touching the bin, the phone, or a pet.
- **Do not rinse raw poultry.** Rinsing aerosolizes bacteria across roughly a metre of sink, counter, and anything drying there. Pat dry with paper towel and bin it.
- The plate that carried raw meat to the grill does not carry the cooked food back. This is the most common outdoor mistake (`grilling.md`).
- A basting brush or marinade that touched raw meat is contaminated. Boil marinade for a full minute before using it as a sauce, or reserve some before it ever meets the meat.
- Sanitize surfaces after raw-meat work; hot soapy water, or a dilute bleach solution left wet for a minute.
- Wash produce under running water even if it will be peeled — the knife carries the surface inward. Bagged salad marked ready-to-eat has already been washed, and re-washing it in a home sink adds risk rather than removing it.

## Allergens

Severity decides the protocol, and severity is a field in `health/profile.md` for exactly this reason.

- **Anaphylactic allergy**: no shared oil, no shared fryer, no shared board or knife, no shared grill surface, no garnish that touched it. Cook the allergen-free food first, on cleaned equipment. Wash with soap and water — heat and sanitizer do not destroy protein allergens, only physical removal does.
- **Intolerance**: trace amounts and shared equipment are usually acceptable; the quantity matters rather than the contact.
- **Celiac disease is not an intolerance.** Shared toasters, shared fryer oil, shared pasta water, wooden boards and flour dust in the air are all real exposures.
- Read labels every time: manufacturers reformulate, and "may contain" is a real statement about a shared production line.
- The fourteen most commonly regulated allergens: cereals containing gluten, crustaceans, eggs, fish, peanuts, soybeans, milk, tree nuts, celery, mustard, sesame, sulphites, lupin, molluscs. Peanut and tree nut are separate categories.
- When cooking for someone else, state the allergens present rather than asking them to trust that a dish is safe.

## Higher-Risk Foods and Who Should Avoid Them

Pregnancy, immunosuppression, chemotherapy, age under 5 or over 65: raw or lightly cooked eggs, unpasteurized milk and its soft cheeses, raw fish and shellfish, raw sprouts, undercooked meat, unpasteurized juice, and pâté. Listeria in particular grows at refrigerator temperatures, which is why ready-to-eat chilled foods appear on that list at all.

Also worth knowing: raw or undercooked kidney beans contain phytohaemagglutinin and must be boiled hard for 10 minutes before simmering — a slow cooker alone does not get hot enough (`vegetables.md`). Green potatoes and potato sprouts contain solanine; cut it away generously or discard. Raw flour has been a source of *E. coli* outbreaks, so raw dough and batter are not safe to taste.

## When to Throw It Out

Discard without tasting: anything left in the danger zone past its budget; any bulging, leaking, or spurting can or jar; home-canned low-acid food that was not pressure-canned; mouldy soft food (mould in a high-moisture food runs far deeper than what is visible — hard cheese and firm vegetables are the exception, where cutting 2-3 cm around the spot is accepted); food with pink or orange slime; and anything whose refrigeration failed for more than four hours.

Tasting to check is not a test. The organisms that matter are invisible, odourless, and tasteless, and a small taste is enough for several of them.

**Write anything with a safety consequence**: an allergy, intolerance, or condition goes to `~/Clawic/data/health/profile.md` with its severity and who confirmed it; a guest's constraint goes to their row in `~/Clawic/data/contacts/contacts.md` under `Context`; and a fridge or freezer that measured warmer than its dial claims is a `## Kitchen` line in `~/Clawic/data/cooking/memory.md`, because every storage time above shifts with it (`memory-template.md`).
