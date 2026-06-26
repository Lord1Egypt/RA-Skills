# Summarize Following Activity

You are turning a list of GitHub events (from users the reader follows) into a
scannable digest section.

## Event Types and How to Present Them

The JSON will have events of these types:

- **`WatchEvent`** — the user starred a repo. This is the strongest signal —
  "people I respect found this interesting."
  Present as: `<actor> starred <repo>` + short description of the repo.

- **`CreateEvent`** (ref_type: `repository`) — the user created a new public repo.
  Present as: `<actor> created <repo>` + description + language tag.

- **`PublicEvent`** — the user made a private repo public.
  Present as: `<actor> open-sourced <repo>` + description.

- **`ReleaseEvent`** — a new release was published on a repo they maintain.
  Present as: `<actor> released <repo> <tag>` + 1-line release highlight from
  `release_body` if available.

## Ordering and Grouping

1. **Group by actor** if one actor has 3+ events — one section per actor
2. **Prioritize by signal**: star events from multiple people on the SAME repo
   is high signal — call this out: "3 people you follow starred `foo/bar`"
3. Within each actor, order: Release > Create > Public > Watch (most notable first)

## Deduplication

- If the same repo appears multiple times across actors, mention it once and
  list who starred/interacted ("starred by alice, bob, carol")
- Don't list the same repo twice for the same actor

## What to Include per Item

- **Repo name**: `owner/repo` format, linked to `url` from JSON
- **Description**: 1 sentence max from `repo_desc`. If empty, skip description.
- **Language tag**: `[Python]` if `repo_language` is set
- **Stars**: only show if > 100, format as `★ 1.2k` or `★ 12.3k`

## What to Skip

- Forks without substantive changes (check if description says "fork of" or name has "-fork")
- Empty repos (no description AND < 3 stars)
- Joke/troll repos (obvious from name/description)
- Duplicates of repos already shown in the Trending or Hot sections of this same digest

## Tone

Terse and factual. Don't narrate ("interestingly, alice starred..."). Just report.
One line per repo when possible.
