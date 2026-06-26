# Preview Stage Reference

## When to Use

- Inspect the current drop settings
- Inspect the current design
- Inspect current prereveal media status

## Minimum Required Parameters

- `chainName`
  - A user-facing chain name
  - Examples: `base`, `arbitrum`, `bsc`
  - The script resolves it internally to the corresponding chain configuration
- `slug`
  - The user-facing Element drop or collection slug
  - The script resolves it internally to the matching `contractAddress`

## Run

First enter the installed skill's `scripts` directory:

```bash
cd <skill-directory>/scripts
npx tsx src/cli.ts preview-drop /tmp/element-drop-preview.json
```

## Example Payload

```json
{
  "chainName": "base",
  "slug": "ffffff-510bce"
}
```

## Output Focus

- `slug`
- resolved `contractAddress`
- availability state: draft, live, or paused
- `dropBeginTime`
- `edition`
- `maxSupply`
- resolved `paymentToken`
- full stage summary for each stage
- whether design exists
- design preview images
- prereveal image status
