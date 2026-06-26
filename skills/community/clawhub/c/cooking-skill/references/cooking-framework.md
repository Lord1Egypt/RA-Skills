# Cooking Framework

## Goal

Convert a user’s cooking request into the smallest useful path from question to dish.

## Entry modes

### 1. Craving mode

Use this when the user describes:

- flavor desire: 下饭、清淡、重口、热乎、酸辣
- occasion: 晚饭、夜宵、招待朋友
- mood: 不想折腾、想吃硬菜、想吃汤汤水水

Output goal:

- recommend one best-fit dish
- explain why it suits the situation

### 2. Ingredient mode

Use this when the user gives ingredients, leftovers, or a pantry snapshot.

Output goal:

- maximize use of existing ingredients
- minimize extra shopping
- prefer the highest-payoff combination over “use everything”

### 3. Specific dish / technique mode

Use this when the user names:

- a dish
- a technique
- a failure symptom

Examples:

- “宫保鸡丁怎么做”
- “糖醋汁怎么调”
- “牛肉为什么一炒就老”

Output goal:

- solve the specific problem directly
- skip generic recommendation logic

## Clarification policy

Ask only what changes the answer.

Default missing-info questions:

1. `几个人吃`
2. `有没有不能吃、不会做、或者家里没有的条件`

When not to ask:

- user already gave the constraints
- the answer is mostly technique-specific
- the user likely wants speed over precision

## Recommendation priorities

When choosing a dish, weigh these in order:

1. request fit
2. home-kitchen feasibility
3. ingredient usage efficiency
4. taste reward
5. time cost
6. failure tolerance

Examples:

- Two people, chicken thigh + potato + onion -> braised or dry-pot style dish beats a fragile stir-fry
- Only eggs + tomato + noodles -> tomato egg noodle beats inventing a forced side dish
- “想吃下饭的” -> favor sauce-carrying dishes over dry, low-impact dishes

## Answer assembly

### Section 1: Dish recommendation

Start with the answer.

Examples:

- “做土豆烧鸡腿最稳。”
- “你这顿适合来个番茄鸡蛋面。”
- “牛肉要嫩，先改切法和腌法。”

### Section 2: Why this fits

Explain fit with short reasons:

- ingredients
- headcount
- effort
- taste profile

### Section 3: Needed ingredients

List:

- essential ingredients
- optional flavor boosters
- realistic substitutions

### Section 4: Method

Write in action order:

1. prep
2. pre-treatment
3. pan order
4. heat control
5. final seasoning

### Section 5: Key points

Name the 1-3 things that really decide success.

Examples:

- “鸡腿先煎出颜色再焖”
- “番茄要把汁炒出来”
- “牛肉刚变色就先出锅”

### Section 6: Failure warnings

Call out likely failures plainly:

- too much water
- broken coating
- overcooked protein
- muddy seasoning
- pan crowding

### Section 7: Rescue / substitutions

Always include fast fallback logic when useful.

Examples:

- no cooking wine
- no starch
- no wok
- too salty
- too sour
- too much water

## Ingredient heuristics

### Protein-led

- chicken thigh: braise, stew, dry pot, heavy sauce
- chicken breast: quick stir-fry, coating, slicing thin
- beef: cut against the grain, marinate briefly, fast cooking
- pork belly: braise, dry fry, twice-cooked style
- eggs: scramble, bind, soup, noodle topping

### Vegetable-led

- potato: braise, shred stir-fry, stew thickener
- tomato: soup base, egg pairing, sauce body
- onion: sweetness base, fragrance, quick pairing
- cabbage: stir-fry, soup, braise absorber
- pepper / chili: aroma and top note, not bulk

### Staple-led

- rice: saucy dishes pair best
- noodles: soup base or topping logic matters
- leftover rice: fried rice if there is enough aroma input and not too much moisture

## Constraint heuristics

### Limited equipment

- one pan -> choose a one-pot or one-pan route
- no oven -> stop suggesting oven defaults
- nonstick pan only -> avoid aggressive wok-hei assumptions

### Low skill

- reduce simultaneous steps
- avoid deep frying unless necessary
- prefer braise / stew / soup over timing-fragile stir-fry

### Tight time

- prefer egg, tomato, pre-cut meat, quick greens, noodles
- avoid dishes needing multiple pre-treatments

## Fallback logic

If the ideal dish is not feasible:

1. preserve the craving
2. reduce the technique burden
3. reduce the ingredient burden

Example:

- User wants a “硬菜” but only has eggs, tomatoes, and onions
- Do not fake a banquet
- Offer a stronger-flavored tomato egg rice topping or onion omelet route instead
