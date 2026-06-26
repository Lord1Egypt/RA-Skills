# Wardrobe inventory

Optional. Helps the agent suggest gaps rather than duplicates. Doesn't need to be exhaustive — the categories matter more than the count.

You can also auto-seed this from your Pima order history by logging in (`POST /api/login`); the agent will pull `GET /api/order_history` and merge.

## Format

```yaml
items:
  - category: shirt              # tops / shirts / pants / shorts / outerwear / shoes / accessories
    style: oxford
    color: white
    fit: standard
    source: buck-mason           # buck-mason / other
    sku: OXF-WHT-L               # optional, only if Buck Mason
    notes: "go-to interview shirt"
```

## Example

```yaml
items:
  - category: shirt
    style: oxford
    color: white
    fit: standard
    source: buck-mason
    sku: OXF-WHT-L

  - category: shirt
    style: oxford
    color: blue
    fit: standard
    source: buck-mason

  - category: shirt
    style: chambray
    color: indigo
    fit: standard
    source: buck-mason

  - category: pant
    style: chino
    color: olive
    fit: standard
    source: other
    notes: "another brand, fits same as Buck Mason 32x32 standard"

  - category: pant
    style: jean
    color: indigo
    fit: standard
    source: buck-mason
    sku: JEAN-INDIGO-32x32

  - category: outerwear
    style: sport_coat
    color: navy
    fit: standard
    source: buck-mason

  - category: shoes
    style: chukka
    color: tobacco_suede
    source: buck-mason

  - category: shoes
    style: sneaker
    color: white
    source: other
```

## Gaps the agent will look for

Given the example above and a "spring NorCal wedding" event, the agent would identify:

- **Dress shirt** (have oxford/chambray casual; need a finer cotton in white or pale blue for under a sport coat).
- **Dress trouser** (have chino + jean; need a wool or wool-blend in stone or charcoal).
- **Dress shoe** (have suede chukka, can pass for smart-casual; suggest a leather option for upgrade).
- **Tie or pocket square** (no formal accessories listed).

The agent will then run a stock check on each gap and produce recommendations.
