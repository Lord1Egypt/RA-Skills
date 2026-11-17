# Costume Size Chef

**Book-character day is TOMORROW and the notice is crumpled in a
backpack.**

Store costumes sell out and cost $30-60 for one night. This tool
assembles costumes from a closet inventory + household items,
filtered by the time you actually have, ranked by what you already
own, and safety-checked for trick-or-treat, school, and party
contexts. 16 recipes, group themes (wizarding world, crayon box,
farm set, 80s crew), and a consolidated one-store-run BUY list that
flags wigs as the #1 regret purchase.

## What it does

- **inventory** — declare clothes/craft items once; every recipe
  re-checks against it
- **find** — occasion × wearer × minutes → ranked recipes with
  HAVE / SUBSTITUTE / BUY per item
- **build** — step list for the chosen recipe
- **groups** — coordinated family/couple sets where each costume
  also stands alone
- **safety** — context-keyed checklists: sightlines vs face paint,
  reflective-tape placement, cape length, flame radius, prop
  policies
- **list** — consolidated shopping list across recipes

## Quick start

```bash
python3 scripts/costume_chef.py inventory --item "red striped shirt" --item "beanie"
python3 scripts/costume_chef.py find --occasion book-character --wearer kid --minutes 20
python3 scripts/costume_chef.py build --recipe "where's waldo"
python3 scripts/costume_chef.py safety --context trick-or-treat
```

Stdlib-only Python 3, offline, local JSON inventory.

## License

MIT
