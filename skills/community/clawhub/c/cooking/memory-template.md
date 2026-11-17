# Working File Templates — Cooking

Read this file only when WRITING. `config.yaml` is what the user **declared**; `memory.md` and everything it indexes is what you **observed** or produced. An observation never overwrites a declaration.

## Where each thing goes

| Data | Home | How it grows |
|---|---|---|
| Declared preferences — Configuration table keys and preference areas alike | `~/Clawic/data/cooking/config.yaml` | Key by key, read-modify-write |
| Kitchen facts, household palate, dishes, swaps, pain points, due dates, box index | `~/Clawic/data/cooking/memory.md` | Rewritten in place; stays small |
| Allergies, intolerances, and diet-relevant conditions | `~/Clawic/data/health/profile.md` (**shared**) | One entry per allergen or condition, every health skill reads it |
| People cooked for, and their food constraint | `~/Clawic/data/contacts/contacts.md` (**shared**) — name only, referenced from here | One row per person |
| Equipment, oven and hob calibration, pan sizes, what is in the salt jar | `## Kitchen` in `memory.md`; `~/Clawic/data/cooking/kitchen.md` once it outgrows the section | One line per fact or piece of kit |
| Dishes cooked, how they came out, what to change next time | `## Repertoire` in `memory.md`; `~/Clawic/data/cooking/repertoire.md` once it outgrows the section | One row per dish, updated in place on each remake |
| Substitutions and scalings that were actually tried, with the verdict | `## Swaps` in `memory.md`; `~/Clawic/data/cooking/swaps.md` once it outgrows the section | One row per swap |
| Live ferments, cures, brines, starters, and infusions with their dates | `~/Clawic/data/cooking/ferments.md` | One row per batch; finished batches keep their outcome, plus a `## Due` row while running |
| Individual cooks worth remembering: the meal, the guests, the timings, the result | `~/Clawic/data/cooking/cooks/<year>.md` | Append-only, cut by year |
| Things you produced that get re-read — a recipe as they actually cook it, a dinner run-sheet, a brine or spice formula, a technique that finally worked in this kitchen | `~/Clawic/data/cooking/artifacts/<kebab-name>.md` | Born as its own file, from the first one |
| **Anything durable this table does not name** | `~/Clawic/data/cooking/<plural-noun>.md`, or `artifacts/<kebab-name>.md` if it is a long text read whole | Name the file after what it holds, never after when it was made; add its `## Boxes` line in the same turn |
| Credentials of any kind | Nowhere under `~/Clawic/data/` | Pointer only — see Secrets |

Deciding where something unnamed goes, in this order: (1) would another skill want to read it — a person, an allergy, a health fact, a project, a purchase? Then it belongs in the shared box, not here. (2) Is it a text read whole when its subject comes up — a recipe, a run-sheet, a formula, a procedure? Then `artifacts/`, its own file from the first one. (3) Is it one more row of something that accumulates? Then a section of `memory.md` until the split threshold.

## When to write

No permission needed; every write is announced in one line that names the file. Writes and deletions stay inside the paths declared in this skill's `configPaths`. A deletion is named in that same line, and in a shared box only rows this skill itself wrote are ever updated or removed.

| It happened | Write |
|---|---|
| A dish was cooked, and how it came out is known | Its row in `## Repertoire`, updated in place if the dish is already there |
| A meal worth remembering happened — guests, a holiday, a first attempt at something hard | A row in `cooks/<year>.md`, with the timings that were wrong |
| A substitution or a scaling was tried | Its row in `## Swaps`, with the verdict, not just the swap |
| A fact about this kitchen cost effort to learn — oven offset, hob behavior, pan dimensions, freezer temperature, water hardness, which salt is in the jar | A line in `## Kitchen` |
| A piece of equipment was bought, retired, sharpened, re-seasoned, or found to be the problem | A line in `## Kitchen`, plus a `## Due` row if it needs maintenance on a cadence |
| An allergy, intolerance, or diet-relevant condition came up | Its entry in `health/profile.md` (**shared**), with severity |
| Someone was cooked for and their constraint or taste matters next time | `contacts/contacts.md` (**shared**) by name, constraint in `Context`; referenced here by name only |
| An allergy was outgrown, a condition resolved, or someone is no longer cooked for | Delete the entry or the row from its shared box, and write the date as a line in `## Household` |
| The household's taste was learned — heat tolerance, doneness preference, textures refused, what gets eaten twice | A line in `## Household` |
| A ferment, cure, brine, or starter was begun, fed, tasted, or finished | Its row in `ferments.md`, plus its check date in `## Due` |
| A failure repeated, or its cause was finally identified | `## Pain Points`; the second occurrence earns a runbook in `artifacts/` |
| A recipe reached the version they will cook again | `artifacts/`, with the quantities actually used |
| A dinner had to be sequenced and the order worked | `artifacts/`, as a run-sheet with clock times |
| A technique finally clicked, or keeps failing at the same step | A line in `## Repertoire` for the dish, `artifacts/` for the technique |
| Bake day, batch cook, starter feeding, spice replacement, or knife sharpening was scheduled or run | `## Due` |
| The user declared a preference | Its key in `config.yaml` |

## Start flat, split only when it hurts

Everything except artifacts, ferments, cook logs, and the shared boxes begins inside `memory.md`. Splitting is a procedure, not a suggestion:

1. Before appending to a section, count its entries.
2. If the append would take it past **~15 entries or ~40 lines of real content** — scaffolding, headings, and comments do not count — then, in the same turn: create the new file in `~/Clawic/data/cooking/`, move the whole section into it, **delete the section from `memory.md`**, add its line to `## Boxes`, and append the new entry to the new file.
3. Keep the headings identical on both sides of the move, so the split is a copy-paste and never a rewrite. `## Repertoire` → `repertoire.md`, `## Kitchen` → `kitchen.md`, `## Swaps` → `swaps.md`, each keeping its own heading inside the new file.
4. Never leave a copy behind. If the same data ever appears in both places, the extracted file wins and the `memory.md` copy is deleted.

Artifacts are the exception: a recipe, a run-sheet, or a formula is born as its own file whatever its size, because it is read whole and only when its subject comes up. Ferments and cook logs are the other exception: both are dated records and never live inside `memory.md`.

## Secrets

Nothing under `~/Clawic/data/` ever holds a secret value — not the files named here, not files you create, not text the user pastes in and asks you to keep. In this domain the carriers are pasted appliance configs, grocery- and delivery-account exports, and shared family documents. Store the pointer in its place, in this shape: `<kind>:<locator>`.

`keychain:smart-oven` · `env:GROCERY_API_TOKEN` · `1password:Personal/Delivery` · `bitwarden:Home/WiFi` · `file:~/exports/recipes.json`

When the user pastes something to save, replace each secret value before writing and leave the pointer visible: `wifi password: <bitwarden:Home/WiFi>`. Say in one line that you did it.

In this domain — **not secrets, keep them**: dish and recipe names, ingredient brands and product names, appliance makes, models and settings, oven offsets, pan dimensions, allergy and intolerance names, guest first names as they appear in `contacts.md`, shop and market names, prices with their currency, ferment and cure dates, thermometer readings. **Secrets, strip them**: grocery, delivery, and meal-kit account logins, smart-appliance API tokens and pairing codes, home Wi-Fi passwords appearing in an appliance setup note, payment card numbers in a pasted receipt, and any medical record or insurance identifier arriving alongside an allergy.

**Contents:** [config.yaml](#configyaml) · [memory.md](#memorymd) · [shared health box](#shared-health-box) · [shared contacts box](#shared-contacts-box) · [ferments.md](#fermentsmd) · [cooks/](#cooks) · [artifacts/](#artifacts) · [split-out files](#split-out-files)

## config.yaml

Keys come from the Configuration table in `SKILL.md`, plus free-form keys nested under a preference area. Write a key only when the user states the preference.

**Writing is read-modify-write**: load the existing file, set or replace only the key just declared, keep every other key byte for byte. Never emit a `config.yaml` from this template — the template shows shape, not content. Create `~/Clawic/data/cooking/` if it does not exist.

```yaml
units: metric
measure_by: weight
salt_type: diamond-kosher
heat_source: induction
oven_type: convection
altitude_m: 650
default_servings: 4
weeknight_minutes: 35
doneness_policy: usda
diet: [pescatarian]
spice_level: hot

# Preference areas — free-form keys added as the user reveals them.
# A preference the user states is a declaration and belongs here, never in memory.md.
tooling:
  owned: [cast-iron-26cm, carbon-steel-wok, pressure-cooker-6L, stand-mixer, instant-read]
  missing: [sous-vide, food-processor]
conventions:
  recipe_shape: timeline        # numbered steps vs a run-sheet with clock times
restrictions:
  dislikes: [cilantro, offal]
  no_alcohol_in_cooking: true
safety_posture:
  rare_meat: yes
  raw_egg: no                   # one household member is pregnant
cadence:
  bake_day: saturday
  starter_feed: daily
ambition: weeknight-simple      # offer the project version only when asked
```

If you find a preference recorded in `memory.md`, move it here and note the move.

## memory.md

Write only the sections you have content for — a heading with nothing under it is noise, and it inflates the line count that decides a split. Never copy these hints into the user's file. `## Boxes` is the one section that is never dropped when `memory.md` is rewritten: deleting a line there orphans a file forever. This is what a populated file looks like:

```markdown
# Cooking Memory

## Status
status: ongoing
last: 2026-07-26

## Boxes
- Dishes cooked and their verdicts (23) → `repertoire.md`; read before proposing anything they have made before
- Live ferments, cures and the starter → `ferments.md`; read at the start of any session, and before starting a new batch
- Cooks worth remembering (2026) → `cooks/2026.md`; read before a dinner with guests, or when a past meal is mentioned
- Roast chicken as they cook it → `artifacts/recipe-roast-chicken.md`; read whenever roast chicken comes up
- Christmas Eve run-sheet → `artifacts/run-sheet-christmas-eve.md`; read before any multi-dish meal with a fixed serving time
- Dry-brine and spice formulas → `artifacts/formula-dry-brine.md`; read before brining or curing anything

## Due
| What | Every | Last run | Next due |
|------|-------|----------|----------|
| Feed sourdough starter | day | 2026-07-26 | 2026-07-27 |
| Kimchi batch — taste and refrigerate | one-off, started 2026-07-22 | — | 2026-07-27 |
| Sharpen knives | quarter | 2026-05-02 | 2026-08-02 |
| Replace ground spices | year | 2025-09-14 | 2026-09-14 |
| Check oven against the thermometer | 6 months | 2026-02-10 | 2026-08-10 |

## Kitchen
Oven runs 18°C cold at 200°C setpoint, worse on the left; convection fan works. Measured 2026-02-10.
Induction hob: boost on ring 1 only; no visual flame cue, so preheat is timed at 3 min for the cast iron.
Pans: 26 cm cast iron, 24 cm nonstick (2024, still good), 28 cm carbon steel wok, 5 L Dutch oven, no roasting tin above 30 cm.
Salt jar is Diamond Crystal kosher (3 g per tsp) — every volumetric salt figure has to be converted.
Freezer sits at −16°C, not −18°C; long-term storage times cut by a third.
Water is hard: bread crumb tightens, and the kettle scales monthly.
No extractor fan — high-heat searing sets off the alarm, so wok work happens with the window open.

## Household
Two adults, one child (6). Child refuses visible onion but eats it blended.
Steak preference: medium-rare for both adults, no exceptions.
Heat tolerance high for one, low for the other — chili goes on the table, not in the pot.
Leftovers get eaten only if they are not the same shape as the original meal.

## Repertoire
| Dish | Times | Last | Verdict | Change next time |
|---|---|---|---|---|
| Roast chicken, dry-brined | 6 | 2026-07-19 | reliable, best thing they make | none — recipe in artifacts |
| Risotto | 3 | 2026-06-30 | good third attempt, first two gluey | keep stock at a bare simmer, stop stirring at the end |
| Sourdough boule | 11 | 2026-07-25 | crumb tight, crust good | dough temperature 26°C, not 22°C; proof to +65% volume |
| Pan-seared salmon | 4 | 2026-07-12 | skin still sticks | dry 20 min uncovered in the fridge, pan hotter, do not move it |

## Swaps
| Original | Swapped for | In what | Verdict |
|---|---|---|---|
| Buttermilk | Milk + 1 tbsp lemon juice, 10 min | Soda bread | worked, indistinguishable |
| Butter | Olive oil at 75% weight | Chocolate cake | denser, oilier crumb — do not repeat |
| Heavy cream | Full-fat coconut milk | Curry sauce | worked; will not whip, do not use for dessert |

## Pain Points
Sauces split whenever the heat is not dropped before the dairy goes in. Third time, 2026-05.
Two burnt garlic incidents from adding it with the onion instead of at the end.

## How They Work
Weeknights are 35 minutes flat, weekends are open. Wants the weight and the temperature, not the story.
Cooks from the phone at the counter — long preambles do not get read.

---
*Updated: 2026-07-26*
```

Rules that keep this readable next month:

- **`## Boxes`**: one line per file that exists — `<what> (<volume>) → <file>; read when <condition>`. Written in the same turn the file is created. Never delete a line without deleting the file it points to. A box with no index line does not exist.
- **`## Due`**: check it against today's date at the start of a session and state any overdue item in one line — a statement, not a question. A ferment or cure with a ready date is a `## Due` row while it runs; the batch itself lives in `ferments.md`.
- **`## Kitchen`**: facts about this kitchen that changed a decision, one line each, with the date on anything measured. This is the section that stops the same oven offset, pan size, or salt brand being rediscovered every few months. Equipment the user *wants* is a preference (`tooling.missing` in `config.yaml`); equipment that *exists* is a fact and lives here.
- **`## Household`**: observed taste, not declared diet. A declared restriction goes to `config.yaml`; an allergy goes to `health/profile.md`; what someone was seen to leave on the plate goes here. A constraint that is **lifted** also lands here as a dated line — an outgrown allergy, a resolved condition, a person no longer cooked for — because the authoritative entry has just been deleted from its shared box and this is the only section that records that something used to be true.
- **`## Repertoire`**: one row per dish, **updated in place** on every remake — `Times` increments, `Verdict` is overwritten. A second row for the same dish loses the history that makes the row worth keeping. `Change next time` is the only field that earns this table its existence: without it the same risotto is gluey three times.
- **`## Swaps`**: the verdict is mandatory and includes the failures. A swap table that records only successes is a table that will suggest the olive-oil cake again.
- These headings are exactly the ones `repertoire.md`, `kitchen.md`, and `swaps.md` get when their sections outgrow this file, so each split stays a copy-paste.

| Status | Meaning |
|-------|---------|
| `ongoing` | Still learning their kitchen, their palate, and what they can already do |
| `complete` | Know the equipment, the household, and the repertoire well |

## Shared health box

Lives at `~/Clawic/data/health/profile.md` and is shared with every other health-adjacent skill — the user may not have any of them installed, so the format travels with this skill. Read it before naming any ingredient.

```markdown
# Health Profile

## Conditions
| Condition | Since | Notes | Source |
|---|---|---|---|
| Celiac disease | 2019 | biopsy-confirmed; shared toaster and fryer oil are exposures | clinician |

## Allergies and Intolerances
| Item | Type | Severity | Reaction | Confirmed by |
|---|---|---|---|---|
| Peanut | allergy | anaphylaxis | airway | allergist, 2015 |
| Lactose | intolerance | moderate | bloating within 90 min | elimination trial, 2026-07 |
```

- **Identity is the entry's name** — the allergen, the intolerance, or the condition. Read the file before adding. If it is already there, update that entry in place; never append a second entry for the same item.
- **Severity is the field that changes the cooking**, not the presence of the row: an intolerance permits trace amounts and a shared pan, an anaphylactic allergy forbids shared oil, shared boards, shared fryers, and garnishes. Record it or the entry cannot be acted on.
- **Never edit an entry another source wrote.** The `Source` or `Confirmed by` column says who owns it; a clinician-sourced entry changes only when the user says it changed.
- **Removal is part of the record.** An outgrown allergy or a resolved condition gets its entry deleted and the date noted in `## Household` of the cooking `memory.md`. A profile that only grows becomes a list of things that used to be true.
- **Scale cut**: entries stay in these tables while there are ≤15 of them per table. Past that, the table moves to `~/Clawic/data/health/<table>.md` with the same columns, and `profile.md` keeps one index line for it.
- **Foreign columns win.** If `profile.md` already exists with a different structure, match what is there and add anything missing as a trailing note. Never rewrite its headings.
- No medical record number, portal login, or insurance identifier — ever (see Secrets).

## Shared contacts box

Only when a person's food constraint or taste has to survive the session. Lives at `~/Clawic/data/contacts/contacts.md`, shared with every skill that names people.

```markdown
| Name | Key | Role | Preferred channel | Context | Last contact | File |
|---|---|---|---|---|---|---|
| Ana Ruiz | ana.ruiz@example.com | friend | whatsapp | shellfish allergy, severe; dislikes coriander | 2026-07-19 | — |
```

- **Identity is `Key`**: lowercase email, else a handle, else `<kebab-name>` plus a stable disambiguator. The key is a column of the row, never implicit.
- Read before adding; if the key is there, update the row in place and only the fields you own. Never touch a row another skill wrote beyond those fields.
- **Retirement is part of the record.** When someone is no longer cooked for — they moved, the relationship ended, the constraint stopped applying — delete the row you wrote and note the date in `## Household` of the cooking `memory.md`. A list of people that only grows stops being the list of people you cook for. If another skill owns the row, never delete it: clear only the food constraint you put in `Context` and leave the rest of the row untouched.
- Past ~15 people, or as soon as one does not fit its row, each person moves to `~/Clawic/data/contacts/<name>.md` and `contacts.md` becomes the index with the `File` pointer. If you arrive and the folder already looks like that, follow it.
- **Foreign columns win.** If `contacts.md` already exists with a different column set, match its columns and put anything missing as a trailing note inside the cell you own. Never rewrite its header — every other skill that names people reads it.
- **A guest's severe allergy is written twice on purpose, in two different registers**: the person and the constraint here, and the allergen itself in `health/profile.md` only when it is the *user's own*. Never copy a guest's allergy into the user's health profile — that file is one person's.
- The person is written there once; here, in `cooks/`, and in artifacts they appear by name only.

## ferments.md

Anything alive or curing, with dates. Lives at `~/Clawic/data/cooking/ferments.md`; every running batch also has a `## Due` row in `memory.md`.

```markdown
# Ferments, Cures and Starters

| Batch | Started | Salt % | Temp | Container | Check on | Status | Outcome |
|---|---|---|---|---|---|---|---|
| Sourdough starter "Mota" | 2023-11-02 | — | 24-26°C | 1 L jar, kitchen shelf | daily | active | peaks 5 h after a 1:5:5 feed |
| Kimchi, napa | 2026-07-22 | 2.5% | 20°C | 2 L crock | 2026-07-27 | fermenting | day 3 tasted sharp, moving to fridge on day 5 |
| Duck breast, cured | 2026-07-10 | 2.5 g/kg #1 | 4°C, 70% RH | fridge, hanging | 2026-08-07 | curing | target 30% weight loss: 410 g → 287 g |
| Sauerkraut | 2026-03-01 | 2% | 19°C | 2 L jar | — | finished | 4 weeks, refrigerated 2026-03-29, excellent |
```

- **A finished batch keeps its row.** The outcome, the salt percentage, and the temperature are the recipe for the next one; deleting them means re-deriving a working ferment from a table of generic numbers.
- **Weight-loss cures carry both numbers** (start and target) because the endpoint is a percentage, not a date.
- **The `Check on` date is mirrored into `## Due`** the moment the batch starts, and cleared when the batch is finished. A ferment nobody was told to check is a ferment that gets thrown away.
- **A batch that went wrong stays too**, with what it smelled and looked like — that row is the only reliable way to tell "this is normal" from "throw it out" next time (`preserving.md`).

## cooks/

The dated record of individual meals, append-only, one file per year, never rewritten.

```markdown
# Cooks — 2026

| Date | Occasion | Menu | For | Planned / actual | What went wrong | Keep |
|---|---|---|---|---|---|---|
| 2026-07-19 | Friends over | Roast chicken, potatoes, salad | Ana (shellfish), Luis | 90 / 135 min | oven fitted one tray, not two — potatoes finished 40 min late | stagger the trays, chicken first |
| 2026-12-24 | Christmas Eve | 5 dishes, 21:00 service | 9 people | 5 h / 5 h | nothing; the run-sheet held | run-sheet in artifacts, reuse it |
```

- **`Planned / actual` is the point of the row.** Cooking time estimates are wrong in one direction, and only a recorded pair fixes the estimate for the next dinner.
- **`For` names people, not counts**, and each name matching a `contacts.md` row is a pointer to it — never re-record their allergy here.
- Cut by year. A year file is closed by leaving it alone; never merge years.

## artifacts/

One file per thing, at `~/Clawic/data/cooking/artifacts/<kebab-name>.md`, created the first time it exists. Canonical types here: **a recipe as they actually cook it**, **a run-sheet for a multi-dish meal**, **a formula (brine, cure, spice blend, dough)**, **a technique that finally worked in this kitchen**. Every artifact opens with when to read it, and gets its `## Boxes` line in the same turn.

```markdown
# Roast chicken — as cooked here
*Read whenever roast chicken comes up. Working as of 2026-07-19.*

Why it is shaped this way: the oven runs 18°C cold, so the setpoint is 220°C for a real 200°C;
the dry brine replaced a wet brine because the skin never crisped with one.

Bird 1.6 kg · dry brine 16 g salt (1.0% of raw weight), uncovered in the fridge 18-24 h
Oven setpoint 220°C convection (real ~200°C) · breast pulled at 71°C, thigh 79°C
Rest 25 min, tented loosely · pan juices deglazed with 80 ml white wine, reduced by half, then salted
Total 95 min including rest. Potatoes go in on the second shelf only after the bird comes out.
```

```markdown
# Run-sheet — Christmas Eve, service 21:00
*Read before any multi-dish meal with a fixed serving time. Written 2026-12-24.*

Built backwards from service. Only one dish is allowed to need the last five minutes.
| Clock | Do | Blocks |
|---|---|---|
| 16:00 | Dry brine off, bird to room temperature | oven at 18:40 |
| 18:40 | Bird in | everything on the top shelf |
| 20:15 | Bird out, rest; potatoes in | the only oven |
| 20:55 | Sauce finished from the pan juices | plating |
Result and what slipped: recorded in `cooks/<year>.md` the same evening.
```

```markdown
# Formula — dry brine and the house spice blend
*Read before brining or curing anything. 2026-07-10.*

Dry brine: 1.0% salt of raw weight, 18-24 h uncovered in the fridge. Poultry and pork: same number.
Cure #1: 2.5 g per kg of meat = 156 ppm nitrite. This one is weighed on a 0.1 g scale, never scooped.
House blend, by weight: 4 sweet paprika · 2 cumin · 1 coriander seed · 1 black pepper · 0.5 dried oregano.
```

If the user tracks a cook as an event with guests, the artifact stays here and the evening is logged in `cooks/<year>.md`, referencing this file by name.

## Split-out files

Created only by the split procedure above, never on day one. Each keeps the exact heading it had inside `memory.md`.

`repertoire.md` — `## Repertoire`, plus a `## Retired` heading once dishes start being abandoned. The retired list is why this file earns its existence: it is the record of what was tried and did not stick, which stops the same dish being proposed every spring.

`kitchen.md` — `## Kitchen`, split into `## Equipment`, `## Calibration`, and `## Constraints` only once the flat list passes ~40 lines. The calibration numbers are the reason to keep it: an oven offset measured once is worth more than any recipe.

`swaps.md` — `## Swaps`. Exists once the household cooks around a restriction routinely; a substitution history is what turns "gluten-free baking is different" into a set of ratios that work in this kitchen.
