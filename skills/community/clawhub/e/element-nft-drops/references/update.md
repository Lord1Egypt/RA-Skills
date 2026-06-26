# Update Stage Reference

## When to Use

- Update settings on an existing drop
- Update design copy or media
- Adjust mint stages

## Minimum Required Parameters

- `chainName`
  - A user-facing chain name
  - Examples: `base`, `arbitrum`, `bsc`
  - The script resolves it internally to the corresponding chain configuration
- `slug`
  - The user-facing Element drop or collection slug
  - The script resolves it internally to `contractAddress`

## Patch Semantics

- The script fetches current remote `settings` and `design` first
- It only overwrites fields the user explicitly provides
- Any omitted field keeps its current remote value
- If the current drop is live and the patch changes `settings` or `preReveal`, `update-drop` does not stop at offchain modification
- In that case it forcibly continues into the publish flow after the modification step
- If the current drop is already paused, the same patch stays offchain and does not force republish
- If the patch only changes `design`, design assets, or collection profile fields, no republish is triggered
- The settings- or prereveal-changing case becomes an onchain-affecting flow and must be confirmed as such

## Common Patchable Fields

### Settings

- `preReveal`
  - Pre-reveal media absolute path
- `edition`
  - `limited` = limited edition
  - `open` = open edition
  - Switching to open edition uses the platform default supply behavior automatically
  - Switching to limited edition requires an explicit `maxSupply`
- `maxSupply`
  - Supply cap for limited edition
- `dropBeginTime`
- `paymentToken`
  - Accepts token `name`, `symbol`, or token address
- `stages`

### Design

- `previewMedia`
  - Design preview image path array
  - The workflow uploads each file, then stores the resulting URLs as design preview images
- `name`
- `description`
- `website`
  - Must be a complete URL
- `twitter`
  - Accepts either suffix or full link; backend payload uses suffix only
- `instagram`
  - Accepts either suffix or full link; backend payload uses suffix only
- `discord`
  - Accepts either suffix or full link; backend payload uses suffix only
- `telegram`
  - Accepts either suffix or full link; backend payload uses suffix only
- `medium`
  - Accepts either suffix or full link; backend payload uses suffix only
- `dropFeaturedImage`

### Design Assets

- `bannerFilePath`
  - Banner image absolute path

Notes:

- `previewMedia` is the user-facing input field for design preview images
- If `preReveal` is uploaded and `previewMedia` is not explicitly provided, the workflow also uses the uploaded prereveal image as the initial design preview image
- Element stages also support whitelist mode on web
- This skill does not support configuring whitelist mode
- Design detail sections are web-only
- If any web-only feature is needed, edit it in the web UI instead, replacing `your-slug` with the actual drop slug:
  - [https://element.market/collections/your-slug/edit/drop](https://element.market/collections/your-slug/edit/drop)

## Stage Rules

- If `stages` is omitted, the current remote stage config is preserved
- If `stages` is provided, it replaces the full current stage array
- `stageID` is never user-controlled
- The script always rewrites stage IDs to `256 + index`

## Execution Preview

First enter the installed skill's `scripts` directory:

```bash
cd <skill-directory>/scripts
npx tsx src/cli.ts update-drop --preview /tmp/element-drop-update.json
```

Current preview behavior:

- show the current values that matter for the requested patch
- show the merged result that would be applied
- show whether the update remains offchain or requires republish
- if republish is required, include the onchain transaction preview

## Execute

```bash
cd <skill-directory>/scripts
npx tsx src/cli.ts update-drop /tmp/element-drop-update.json
```

## Output Focus

- `slug`
- resolved `contractAddress`
- fields actually updated
- settings summary, if settings were updated
- design summary, if design was updated
- whether republish was triggered
- `Drop URL`
- `Collection URL`
- `Edit URL`

## Example Payload

```json
{
  "chainName": "base",
  "slug": "ffffff-510bce",
  "maxSupply": 999,
  "paymentToken": "WETH",
  "description": "updated description"
}
```

## Example Payload With Media Updates

```json
{
  "chainName": "base",
  "slug": "ffff",
  "paymentToken": "0x4200000000000000000000000000000000000006",
  "preReveal": "/absolute/path/to/image.png",
  "bannerFilePath": "/absolute/path/to/banner.png",
  "previewMedia": [
    "/absolute/path/to/image.png"
  ],
  "description": "updated description"
}
```

## Payment Token Guidance

- Use `list-chains` if the user needs the currently supported payment token list for a chain
- Prefer token address when there is any ambiguity between display names or symbols
- If `paymentToken` is omitted during `update-drop`, the current remote payment token setting is preserved
