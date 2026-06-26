# Upcoming events

Optional. Lets the agent suggest event-appropriate outfits without you re-explaining the context every time.

Add new events at the top. Mark past events as `archived: true` (or just delete them — the agent only reads upcoming).

## Format

```yaml
events:
  - name: Sarah & James wedding
    date: 2026-05-30
    location: Sonoma County, CA
    setting: outdoor vineyard ceremony, dinner under string lights
    dress_code: smart casual / cocktail
    notes: "ceremony 4pm, photos before dinner; daytime golden hour"
    days_on_site: 2

  - name: Q2 board offsite
    date: 2026-06-12
    location: Boston, MA
    setting: hotel meeting rooms + group dinners
    dress_code: business casual
    notes: "client-facing on day 1; smart-casual dinner day 2"
    days_on_site: 3

  - name: Aspen ski week
    date: 2026-12-15
    location: Aspen, CO
    setting: mountain town, après-ski dinners, one cocktail event
    dress_code: casual + one smart-casual look
    notes: "altitude — layers; one collared shirt for the cocktail night"
    days_on_site: 7
```

## Fields

- `name` — short label, used in lookbook filenames
- `date` — ISO date (YYYY-MM-DD), used to determine season
- `location` — city + state/region, used for regional weather rules
- `setting` — free text describing the venue/scene; the agent uses this for image-gen settings
- `dress_code` — the agent maps this to garment categories (see `references/seasons.md`)
- `notes` — anything else (timing, multi-event splits, weather concerns)
- `days_on_site` — how many distinct outfits you might need

## How the agent uses this

When you say "build me a lookbook for the wedding", the agent:

1. Picks the matching event by name (or by date if you say "for May 30").
2. Reads `setting` + `dress_code` + `location` → infers season/weather/style.
3. Cross-references your `wardrobe.md` for what you already have.
4. Proposes an outfit list, then builds the lookbook (per `references/image-generation.md`).
5. Saves the lookbook under `lookbook/<date>-<event-slug>/`.
