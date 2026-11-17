# Easy mode: Theme and Outfit presets

When the user describes a location or outfit in plain words (a cafe, goth clothes, the gym, the beach), prefer the curated presets over a long hand-written prompt. They are platform-tuned and generally produce better results.

```bash
fannabe ai options --filter topic  --media-type image   # Themes (e.g. mirror-selfie, dubai)
fannabe ai options --filter outfit --media-type image   # Outfits (e.g. casual, gym)

fannabe generate create <aiId> \
  --model <modelId> --media-type image --concept-type single-image \
  --set locationPrompt=<themeId> --set outfitPrompt=<outfitId> \
  --set aspectRatio=9:16 --set resolution=1k \
  --wait --download ./output
```

Using a `locationPrompt` or `outfitPrompt` automatically switches the request to simple mode so the preset actually applies. The ids come from the `ai options` listing.
