# Choosing an AI

List AI engines per media type, then read the chosen AI's schema before generating.

```bash
fannabe ai list --media-type image      # image | video | audio | lip-sync
fannabe ai schema <aiId>                # exact fields, defaults, and source slots
```

- The first column of `ai list` is the AI id you pass to `generate create`.
- AI ids are a stable public contract (e.g. `nano-banana-2-single-image`, `kling-2-6-motion-control`); prefer them over guessing.
- `ai schema <aiId> --concept-type <type>` shows fields for a specific concept (e.g. `single-image`, `carousel`, `video-from-image`, `talking-video`). `--simple` shows the simple-mode fields.
- `economyMode` (a `--set economyMode=true` flag on supported AI) trades priority for a lower price.

Pass `--concept-type <type>` on `generate create` so the request runs the intended concept rather than a generic default.
