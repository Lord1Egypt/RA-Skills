# Expected Output Notes

- Validates the approved card package before rendering.
- Selects a deterministic, generative, or mixed strategy based on factual and typography needs.
- Routes generative or mixed work through `resilient-imagegen` with `generation_backend=auto`.
- Uses `chatgpt-image-handoff` for Computer Use or manual fallback and rejoins only after a local file is imported.
- Creates real ordered image files at the platform dimensions.
- Opens and checks every image for text, clipping, order, dimensions, consistency, and factual alignment.
- Revises failed cards before marking visual QA as passed.
- Produces a `cards-manifest` with render strategy, generation backend, optional handoff run, QA, human-confirmation, asset-policy, and R2 states.
- Leaves human confirmation pending until the user approves the images.
- Stops before R2 upload, Markdown URL rewrite, or platform publishing.
