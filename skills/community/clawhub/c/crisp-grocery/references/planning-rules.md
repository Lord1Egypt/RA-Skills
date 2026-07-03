# Planning Rules

## Meal Planning

Use Crisp account data as evidence, not as an absolute instruction.

1. Read recent order history and count repeated products/recipes.
2. Read `/yourShop` for currently personalized categories and repeated purchases.
3. Read `/promo/current` for current offers.
4. Read `/basket/main` for minimum order value, service fees, delivery windows, and current basket state.
5. For selected recipes, fetch `/recipe/:id` and inspect ingredient groups.

When planning multiple days:

- Match portion counts to the household schedule.
- Prefer meals that scale cleanly.
- Avoid too many similar meals in a row unless the user asks for it.
- Use promotions as a tiebreaker, not the only criterion.
- Keep the basket above the live minimum order value.

## Dietary Handling

Do not rely only on tags such as `lactoseFree`.

Inspect:

- recipe ingredients;
- nested product allergens;
- ingredient role in the dish;
- whether a dairy ingredient is central or easily replaced;
- the user's stated household preference.

For mixed households, distinguish:

- must be dairy-free for everyone;
- dairy can be served separately;
- dairy is acceptable for some family members;
- the user has dairy replacements at home.

Examples of easy substitutions:

- cream or creme fraiche -> plant cream, oat cuisine, soy cuisine, or coconut cream if flavor fits;
- grated cheese -> dairy-free pasta cheese or omit;
- yoghurt sauce -> plant yoghurt with lemon, garlic, salt, herbs;
- butter -> olive oil or plant butter.

## Promotion Ranking

Rank promotions by more than discount percentage.

Useful fields:

- `price`
- `basePrice`
- `promotion.descr`
- `promotion.percent`
- `promotion.discount`
- `promotion.fixedPrice`
- repeated purchase count from `/order/history`
- match to current menu ingredients;
- match to `/yourShop`;
- dietary suitability;
- storage life and waste risk.

Suggested scoring:

1. Exact menu ingredient match.
2. Repeated historical purchase.
3. Strong household preference inferred from order history.
4. High euro savings.
5. High percentage savings.
6. Shelf-stable or freezer-friendly.
7. Dietary fit or easy substitution.

Avoid presenting dairy promos as irrelevant when only part of the household avoids milk products. Instead, label them as "serve separately" or "for dairy-eaters".

## Delivery And Fees

Use live `/basket/main` values.

Summarize:

- minimum order value (`mov`);
- amount still needed (`neededForMOV`);
- service fee (`servicePrice`, `serviceFaqContent`);
- cheapest slot per date;
- free slots;
- cutoff time;
- selected delivery slot if any.

Do not assume fee thresholds are stable.

## Basket Changes

Before a mutation, show a diff:

- action: add, update, or remove;
- item id and item title;
- current quantity if known;
- requested quantity;
- expected price impact when known;
- endpoint and payload shape, without token.

Require exact confirmation. Example:

> Confirm: add product 6339 quantity 1

After mutation:

1. Fetch `/basket/main` again.
2. Report the updated item count, basket total, minimum-order gap, and whether a delivery slot is selected.
3. Do not proceed to checkout.
