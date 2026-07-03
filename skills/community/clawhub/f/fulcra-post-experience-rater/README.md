# post-experience-rater

Turn your agent into your **personal Yelp**. 15-second "how was it?" check-ins after a restaurant, hotel, event, or meeting. Each rating (scores, would-return, tags, companions) compounds into a personal taste graph that powers the recommender.

- **Writes:** `Post-Experience Rating` (Fulcra annotation)
- **Reads:** nothing required
- **Prerequisites:** Fulcra account + `uv tool run fulcra-api` authenticated
- **Pairs with:** [restaurant-recommender](../restaurant-recommender) (reads these ratings as your taste graph)

## Use

Ask your agent ("rate that dinner — food 5, vibe 4, service 3"). Or run directly:

```
uv run --python 3.12 scripts/post_experience.py --help
```

Needs the shared `/lib` (auto-resolved by `concierge_bootstrap.py`). See `SKILL.md`.
