# Survival and points strategy

## Objective order

Maximize survival days first. Maximize survival points only inside the risk budget left after survival needs are covered.

Use this decision order:

1. Resolve active combat.
2. Prevent immediate death or irreversible loss.
3. Protect water, food, health, temperature, and population.
4. Restore enough energy to retain multiple safe options.
5. Secure renewable materials and basic facilities.
6. Complete low-risk NPC help for points.
7. Sell genuine surplus and use the points economy efficiently.
8. Explore or take higher-variance actions only with reserves.

## Survival reserves

Adapt to the actual available commands and rules; do not assume unavailable actions exist. Use these conservative warning levels:

- Health below 35: critical. Prefer healing, retreat, rest, shelter, or low-risk resource recovery.
- Energy below 25: avoid expensive exploration, building, or optional combat.
- Satiety below 30: preserve or obtain food before long actions.
- Water or food resources close to the population's next daily consumption: replenish before optional point farming.
- Abnormal temperature or rapidly falling hygiene/morale: prioritize the relevant item, building, or rest action.

Do not consume the final copy of a broadly useful medicine, tool, food, or water item merely to improve a non-critical stat.

## Combat

- Compare player health and energy with the monster's remaining health.
- Use `POWER_STRIKE` only when its energy cost improves the probability of ending combat before taking more damage.
- Prefer `FLEE` when health is critical, energy cannot support effective attacks, or the reward does not justify death risk.
- After combat, re-read state and restore survival reserves before pursuing points.

## Earning survival points

Prefer point sources in this order:

1. NPC help that consumes replaceable surplus items and is not completed today.
2. Low-risk world actions that also improve survival supplies.
3. Selling surplus common items while retaining a safety reserve.
4. Player-market sales only when the user has authorized pricing decisions.

Before selling, keep enough materials for known building recipes and keep emergency food, water, medicine, fuel, and one functioning tool where possible.

## Spending survival points

Buy or exchange for items when they fix a current survival bottleneck or prevent a likely future shortage. Avoid buying merely because an item is available.

Never attempt AGP exchange. 荒年积分 is the gameplay ledger; AGP is a separate platform asset outside this Skill's authority.

## Reporting

For interactive play, report compactly:

- selected action and reason;
- current day and scene;
- health, energy, food/water pressure, and population when relevant;
- survival-points balance and change;
- any new danger or decision that needs user confirmation.

For an explicitly requested continuous run, report checkpoints instead of every low-impact action, but stop on required-confirmation choices, invalid credentials, repeated server errors, or lack of legal commands.
