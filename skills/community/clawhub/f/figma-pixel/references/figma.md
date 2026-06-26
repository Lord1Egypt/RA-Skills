# Figma input layer

## Required input

The skill should trigger when:
- the user shares a Figma URL
- and asks to build, compare, match, or adjust implementation

## Scripts

### `scripts/parse-figma-url.cjs`
Parse a Figma URL and extract:
- file key
- node id
- raw pathname

### `scripts/fetch-figma-api.cjs`
Fetch Figma API data using:
- `FIGMA_TOKEN`

It stores:
- `figma-file.json`
- `figma-node.json` when a node id is present

### `scripts/export-figma-image.cjs`
Export the target Figma node as PNG using:
- `FIGMA_TOKEN`

It stores:
- `reference-image.png` when the Figma image export endpoint succeeds for the target node

## Notes

- Use the exact frame/node the user points to.
- Do not guess the intended frame when the link already contains `node-id`.
- Figma screenshots and Figma API metadata should be treated as the design source of truth.
