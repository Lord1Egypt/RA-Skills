---
name: budget-meal-prep
description: >-
  Weekly meal prep system for one person on a tight budget. Use when someone wants to eat well on $40-60/week, reduce food waste, stop relying on takeout, or batch cook for the week in 2-3 hours.
metadata:
  category: skills
  tagline: >-
    Eat well on $50/week — a repeatable weekly system for batch cooking, smart shopping, and zero-waste meals that take 15 minutes to heat and serve
  display_name: "Budget Meal Prep"
  openclaw:
    requires:
      tools: [filesystem]
    install: "npx clawhub install howtousehumans/budget-meal-prep"
---

# Budget Meal Prep

Cooking every night when you're tired is unrealistic. Ordering delivery is expensive ($15-20 per meal vs $2-4 per home-cooked meal). Meal prep solves this: two to three hours on Sunday produces five to seven days of ready-to-heat meals. This skill provides a complete repeatable system — not recipes, but a framework you load with your own preferences and dietary needs. Budget target: $40-60/week for one person eating three meals and snacks daily. Complements the cook-from-scratch skill (which teaches techniques) by focusing on the weekly planning and batch-cooking system.

## Sources & Verification

- USDA SNAP-Ed Connection — free meal planning resources and budget-friendly nutrition guides for food assistance recipients. snaped.fns.usda.gov — verified active March 2026
- USDA FoodSafety.gov — food storage temperature guidelines, safe cooling times, and refrigerator/freezer shelf life data. foodsafety.gov — verified active March 2026
- USDA MyPlate budget-friendly meal planning tools. myplate.gov — verified active March 2026
- NRDC "Wasted: How America is Losing Up to 40% of its Food" report — food waste data and storage guidance. nrdc.org — verified active March 2026
- Bureau of Labor Statistics Consumer Expenditure Survey — average US household food spending benchmarks
- Feeding America: feedingamerica.org — food bank locator and emergency food resources

## When to Use

- User spends too much on food and wants a concrete system to fix it
- Relies on takeout or delivery because there's "nothing to cook"
- Buys groceries that go to waste every week
- Wants to eat better but doesn't have time to cook daily
- Living alone or cooking for one and finds standard recipes wasteful
- Needs a shopping list and a plan, not just recipe ideas

## Instructions

### Step 1: Assess starting point

**Agent action**: Ask these questions one at a time and record answers in state. Use the results to generate a custom first-week plan.

```
STARTING POINT ASSESSMENT:

1. What is your weekly food budget? (be honest)
2. Do you have dietary restrictions?
   (vegetarian/vegan, gluten-free, allergies, religious)
3. What do you already know how to cook? (even just: eggs,
   pasta, rice, nothing)
4. What equipment do you have?
   [ ] Stove/oven  [ ] Microwave  [ ] Rice cooker
   [ ] Slow cooker / Instant Pot  [ ] Sheet pans  [ ] Containers
5. How much fridge/freezer space do you have for prepped food?
6. How many meals per day do you want to cover?
   (breakfast, lunch, dinner, snacks — which ones?)
7. What are 3 meals you already like eating?
```

### Step 2: The budget framework

**Agent action**: Using the user's budget and restrictions from Step 1, generate a weekly framework based on the template below. Save as their "base template" in state.

```
THE $50/WEEK BUDGET BREAKDOWN (for one person):

Proteins (fill 1/4 of each meal):     $15-18
  Batch-cook 2-3 proteins for the week.
  Cheapest per gram of protein:
    - Dried lentils ($1.50/lb, 24g protein/cooked cup)
    - Canned tuna ($1.00-1.50/can, 25g protein)
    - Eggs ($3-5/dozen, 6g protein each)
    - Dried beans: black, pinto, chickpeas ($1.50-2/lb)
    - Chicken thighs, bone-in ($1.50-2.50/lb)
    - Canned sardines ($1.50-2.50/tin, 20g protein)
    - Firm tofu ($2-3/block, 10g protein per 3oz)

Starches / complex carbs (fill 1/4 of each meal):  $8-10
  - Brown rice (buy 5lb bags, ~$5, lasts 15+ meals)
  - Rolled oats (5lb bag ~$5, lasts weeks)
  - Dried pasta ($1-1.50/lb)
  - Potatoes (5lb bag $3-5, very filling, versatile)
  - Bread (store brand $2-3)

Vegetables (fill 1/2 of each meal):   $12-15
  Fresh vegetables in season are cheapest.
  But frozen vegetables are equally nutritious and cheaper:
    - Frozen spinach, broccoli, peas, edamame, mixed veg
    - Frozen corn: ~$1-1.50/lb
    - Canned tomatoes: $1/can — the backbone of dozens of sauces
  
  Cheapest fresh:
    - Cabbage (most budget value per pound)
    - Carrots, onions, garlic (flavor base for everything)
    - Bananas (cheapest fruit by calorie)
    - Seasonal produce from the marked-down bin

Pantry / flavor ($5-8):
  - Olive oil, canola oil
  - Salt, pepper, garlic powder, cumin, paprika
  - Soy sauce, hot sauce, vinegar
  - These last months — buy once, use all year

TOTAL: $40-51 in most US markets
```

### Step 3: The Sunday prep system

The goal is two to three hours of cooking that produces five to seven days of ready-to-heat food.

**Agent action**: At the start of each week, help the user build their specific prep plan from the template below. Generate a shopping list from their selections. Set a Sunday reminder.

```
SUNDAY PREP SEQUENCE (2-2.5 hours):

WHILE THINGS ARE COOKING, DO THE NEXT THING:
  The key to efficient prep is parallel cooking.
  Start longest items first; do shorter tasks while waiting.

PREP ORDER:

Start these first (they take the most time):
  [ ] Grains: Put rice/oats/quinoa on. Rice cooker or pot.
      Brown rice: 45 min. White rice: 18 min.
  [ ] Dried beans (if using): These need 6-8 hours or use
      canned. If using a slow cooker: start Saturday night.
  [ ] Proteins in the oven: chicken thighs, roasted tofu,
      sheet-pan eggs (frittata), or hard-boiled eggs.
      Oven proteins: 25-40 minutes.

While those cook, prep vegetables:
  [ ] Wash and chop all vegetables for the week.
      Store in containers in the fridge.
  [ ] Roast one tray of mixed vegetables (onion, carrot,
      broccoli, whatever you have) at 400F for 20-25 min.
  [ ] Make one sauce or dressing that will flavor multiple
      meals (see sauce templates below).

Final assembly:
  [ ] Cook one pot of something soup-like or stew-like.
      This is the most versatile meal — it reheats perfectly,
      freezes well, and you can eat it for breakfast, lunch,
      or dinner.
  [ ] Portion meals into containers.
      3-4 days in fridge, rest in freezer.
```

```
SAUCE AND FLAVOR TEMPLATES (each covers 4-6 meals):

SIMPLE TOMATO BASE:
  1 can crushed tomatoes + 4 cloves garlic (minced) +
  1 tsp olive oil + salt + red pepper flakes.
  Simmer 15 min. Add to pasta, grain bowls, eggs,
  lentils, chicken.

TAHINI DRESSING:
  3 tbsp tahini + 2 tbsp lemon juice + 1 clove garlic +
  water to thin + salt.
  Drizzle on: roasted veg, grain bowls, chickpeas,
  salads, rice.

GINGER-SOY SAUCE:
  3 tbsp soy sauce + 1 tbsp rice vinegar +
  1 tsp sesame oil (or canola) + 1 tsp fresh or powdered
  ginger + optional: small amount of honey.
  Use on: tofu, rice, stir-fried veg, chicken, eggs.

SPICED YOGURT / SOUR CREAM SAUCE:
  1/2 cup plain yogurt + 1 tsp cumin + 1/2 tsp garlic
  powder + squeeze of lemon + salt.
  Use on: grain bowls, roasted veg, beans, tacos.
```

### Step 4: Meal assembly (the daily 15 minutes)

Meal prep works because "cooking" during the week is just assembly, not cooking.

**Agent action**: Help the user build their daily assembly formula based on what's in their fridge from Sunday's prep.

```
THE ASSEMBLY FORMULA:
  1 scoop of grains or starch
  + 1 scoop of protein
  + 1 scoop of vegetables
  + 1 spoonful of sauce
  = a complete meal in under 5 minutes

EXAMPLE COMBOS FROM THE SAME PREP:
  Breakfast: oats + peanut butter + banana slices
  Lunch: rice + chickpeas + roasted veg + tahini
  Dinner: pasta + tomato base + lentils + spinach
  Snack: hard-boiled egg + carrots + hummus

REHEATING SAFELY:
  Fridge: reheat to steaming hot (165F / 74C) throughout.
    Do not just warm it — reheat it.
  Microwave: stir halfway through, check center temp.
  Stovetop: add a splash of water to prevent sticking.
```

### Step 5: Food storage and waste prevention

**Agent action**: When the user describes what's in their fridge, help them identify what needs to be used first and how to use it.

```
REFRIGERATOR SHELF LIFE (for cooked meal-prep food):
  Cooked rice, grains: 4-5 days
  Cooked beans/lentils: 4-5 days
  Cooked chicken or fish: 3-4 days
  Hard-boiled eggs (in shell): 1 week
  Hard-boiled eggs (peeled): 5 days
  Cooked vegetables: 3-5 days
  Soups/stews: 4-5 days
  Sauces (no cream): 5-7 days

FREEZER SHELF LIFE (quality maintained):
  Cooked grains: 3 months
  Cooked beans/lentils: 3 months
  Soups and stews: 3 months
  Cooked chicken: 2-3 months
  Bread: 3 months (toast directly from frozen)

SAFE COOLING RULE (critical — prevents food poisoning):
  Cooked food must be cooled from 140F to 40F within 2 hours.
  Never put a large hot pot directly in the fridge --
  it raises the fridge temperature and spoils other food.
  Spread food into shallow containers to cool faster.
  Ice bath for large batches: put the pot in a sink
  of ice water, stir every 10 minutes.

ZERO-WASTE RULE OF THUMB:
  First in, first out. Label containers with date.
  "Use these first" items: anything from 3+ days ago.
  When in doubt: smell it. If it smells off, discard it.
  Wilting vegetables: add to soup or stew immediately.
```

### Step 6: Substitution guide for dietary restrictions

**Agent action**: If the user mentioned dietary restrictions in Step 1, use the relevant substitution columns to adapt the template.

```
PROTEIN SUBSTITUTION GUIDE:

If vegetarian/vegan (no meat, no eggs):
  Chicken -> Tofu (firm, pressed), tempeh, lentils,
    edamame, canned beans, chickpeas
  Eggs -> Scrambled tofu (silken + turmeric + black salt),
    chia seeds in oats, flax egg for baking
  Cheese -> Nutritional yeast (B12 + savory flavor)

If gluten-free:
  Pasta -> Rice pasta (similar), buckwheat soba, or rice
  Soy sauce -> Tamari (gluten-free soy sauce) or coconut aminos
  Bread crumbs -> Rolled oats (if certified GF), rice flour

If dairy-free:
  Yogurt sauce -> Coconut yogurt, tahini-based sauce
  Butter -> Olive oil or coconut oil in equal amounts

If very low budget (under $30/week):
  Prioritize: oats, rice, dried beans, eggs, cabbage,
    carrots, canned tomatoes, frozen spinach.
  This $25 base provides complete nutrition.
  Supplement with whatever protein is cheapest that week.
```

## If This Fails

1. **No time on Sundays**: Even 45 minutes of partial prep helps — cook a pot of rice and hard-boil a dozen eggs. That alone solves the "nothing to eat" problem for most of the week.
2. **Food going bad before you eat it**: You're prepping too much variety. Fewer recipes, bigger batches. Meals that are slightly boring are better than meals that go in the trash.
3. **No cooking equipment**: A microwave and a single pot on a hot plate can execute this entire system. If even those are unavailable, see the benefits-navigator skill for food assistance programs that may include SNAP or community meal programs.
4. **Food insecurity — can't afford even $40/week**: Local food banks, SNAP/EBT enrollment (benefits-navigator skill), community fridges, and mutual aid organizations. Feeding America locator: findafoodbank.feedingamerica.org — verified active March 2026.
5. **Skills gap — don't know how to cook the proteins**: See the cook-from-scratch skill for foundational techniques (how to cook chicken thighs, hard-boil eggs, cook dried beans correctly).

## Rules

- Always include food safety guidance when discussing batch cooking and storage — foodborne illness from improper cooling is a real risk
- Never suggest meal plans without accounting for stated dietary restrictions
- When budget drops below $30/week, always check if the user qualifies for SNAP or food assistance before optimizing cooking
- Do not assume kitchen equipment — ask first

## Tips

- The most common meal prep failure is variety overload. Beginners should prep two proteins, one grain, one batch of roasted veg, and one sauce. That's it. Four components, twelve possible meals.
- Batch cooking dried beans (vs canned) saves ~50% on protein costs and produces better-tasting beans. The barrier is 8 hours of passive soaking — not active time.
- Cabbage is the most underrated budget vegetable: cheap, lasts 2+ weeks in the fridge, cooks in minutes, works raw or cooked, absorbs any sauce flavor.
- Freezing individual portions is more useful than freezing entire batches — you can pull exactly one meal at a time without defrosting everything.

## Agent State

Persist across sessions:

```yaml
meal_prep:
  budget: null
  restrictions: []
  equipment: []
  skill_level: null
  base_template:
    proteins: []
    starches: []
    vegetables: []
    sauces: []
  current_week:
    plan: []
    shopping_list: []
    prep_done: false
    prep_date: null
  pantry_staples_stocked: false
  weekly_history: []
  flags:
    food_insecurity: false
    snap_referral_given: false
```

## Automation Triggers

```yaml
triggers:
  - name: sunday_prep_reminder
    condition: "base_template IS SET"
    schedule: "weekly on Saturday evening"
    action: "Tomorrow is prep day. Want me to generate your shopping list and prep plan for the week? It takes 2-3 hours and sets you up for 7 days of easy meals."

  - name: midweek_check
    condition: "current_week.prep_done == true"
    schedule: "Wednesday afternoon"
    action: "Midweek check: how's the meal prep holding up? Anything running low that needs a quick restock? Anything that's going to expire in the next 2 days we should plan to use?"

  - name: waste_alert
    condition: "current_week.prep_date IS SET AND (current_date - prep_date > 4 days)"
    action: "Anything in your fridge from Sunday prep that hasn't been eaten yet should be frozen today or used in the next 24 hours. What's left?"
```
