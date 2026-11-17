# Trip Data Contract

Use this contract when filling `tripMeta` and `tripDays` in an HTML route artifact or when validating a generated artifact.

## Runtime Minimum

Every artifact must include:

- `tripMeta.title`, `tripMeta.intro`, and `tripMeta.timezone`.
- `tripDays[]` with one object per travel day.
- Per day: `id`, `title`, `date`, `strategy`, `weather`, `drive`, and ordered `stops`.
- Per stop: `name`, `lat`, `lng`, `address`, `priority`, `why`, and `tip`.
- At least two stops per day, in the exact driving order used by map links and calendar notes.

## Recommended Quality Fields

Golden examples and real user-facing HTML should also include:

- `mainObjective`: the one real objective for the day.
- `cutRules[]`: what to remove first when timing or body battery drops.
- `tickets[]`: official venue or ticket actions.
- `parking`: practical parking or arrival note.
- `medicalBackup[]`: concise regional backup logistics when useful.
- `sourceProvenance[]`: dated source records for weather, road, ticket, restaurant, image, venue, parking, medical, or map facts.

## Weather

The template still accepts legacy string arrays:

```js
weather: ["Monterey 16-20°C", "Big Sur windy near the coast"]
```

Prefer object form for reusable artifacts:

```js
weather: {
  summary: ["Monterey 16-20°C, cloudy", "Big Sur 15-22°C, windy"],
  checkedAt: "2026-07-05",
  source: "National Weather Service",
  appliesToDate: "2026-06-15",
  note: "Refresh the week of travel."
}
```

## Images

Prefer `images[]` for swipeable galleries:

```js
images: [
  {
    src: "https://example.com/photo.jpg",
    alt: "Short image alt text",
    title: "Classic viewpoint",
    caption: "Why this camera spot matters, and when to skip it.",
    credit: "Official venue or photographer",
    link: "https://example.com/source"
  }
]
```

Compatibility fields `image` and `imageAlt` are still accepted. If photos are not yet available, include `imageQuery` and optionally `imageNote` so the HTML shows a useful fill prompt.

## Source Provenance

Use `sourceProvenance[]` for facts likely to change:

```js
sourceProvenance: [
  {
    type: "weather",
    label: "NWS Monterey forecast",
    url: "https://www.weather.gov/",
    checkedAt: "2026-07-05",
    appliesToDate: "2026-06-15",
    note: "Refresh before departure."
  }
]
```

Do not fabricate live checks. If a source was not checked, mark it as a planning placeholder in notes instead of presenting it as current truth.

## Privacy Boundary

Public examples must not include home addresses, hotel confirmation numbers, room numbers, traveler names, private calendar names, personal medical status, direct phone numbers, emails, or payment details. Use public city/venue/hotel names and generalized comfort constraints instead.
