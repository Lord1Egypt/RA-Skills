# Create Stage Reference

## When to Use

- Create a new Element Drop
- Deploy the contract and complete the initial media, settings, and design setup
- Explicitly stop before publish

## Minimum Required Parameters

When the user starts a create flow, proactively collect these fields first. If any are missing, ask for the missing required fields and state the defaults below before preparing the preview.

- `chainName`
  - A user-facing chain name
  - Example values: `base`, `bsc`, `arbitrum`
  - Do not guess whether a chain is supported
  - If the user is unsure, run `list-chains` before continuing
  - The script resolves it internally to the corresponding chain configuration
- `name`
  - Collection name shown as the contract name onchain
  - Usually the project or collection name users will recognize
  - This value cannot be changed after the contract is deployed
- `symbol`
  - Short onchain identifier for the contract
  - Usually an uppercase shorthand, such as `AZUKI` or `BAYC`
  - This value cannot be changed after the contract is deployed
- `preReveal`
  - Pre-reveal image path
  - Must be a local absolute path
  - The workflow uploads this prereveal asset during create
  - The workflow also uses this image as the default initial design preview media unless explicit design preview assets are provided

If the user is unsure which chains are currently supported, run:

```bash
cd <skill-directory>/scripts
npx tsx src/cli.ts list-chains
```

## Create Defaults

If the user does not override these fields, create uses:

- Mint start time: next day
- Edition: limited edition
- Total supply: `999`
- Sale currency: native chain currency
- Stage set: one public stage
- Default stage name: `Public`
- Default stage sale price: `0`
- Default stage duration: `3 days`
- Default phase supply: same as the collection supply
- Default max mints per wallet: `1`
- Default mint interval: `0`
- Default stage mode: public
- Default banner: prereveal image
- Default preview image: same image as `preReveal`, unless `previewMedia` is provided

Do not describe these as facts if you have not read this reference in the current operation.

## Common Optional Parameters

- `previewMedia`
  - Optional preview image path or path array
  - Must use local absolute path(s)
  - If omitted, defaults to the same image as `preReveal`
  - The workflow uploads these files and stores them as the preview images
- `bannerFilePath`
  - Optional design banner image path
  - If omitted, the prereveal image is used as the initial banner
- `description`
  - Drop description
- `desc`
  - Alias for `description`; accepted for user convenience and normalized before sending to the backend
- `website`
  - Collection website URL; must be a complete URL
- `twitter`
  - Twitter/X suffix or full link; normalized to suffix before backend write
- `instagram`
  - Instagram suffix or full link; normalized to suffix before backend write
- `discord`
  - Discord invite suffix or full link; normalized to suffix before backend write
- `telegram`
  - Telegram suffix or full link; normalized to suffix before backend write
- `medium`
  - Medium suffix or full link; normalized to suffix before backend write
- `dropFeaturedImage`
  - Optional featured image URL for the drop design payload
- `paymentToken`
  - Sale currency
  - Defaults to native chain currency
  - Accepts token `name`, `symbol`, or token address
  - Do not guess the supported token list; use `list-chains` when the user asks what is supported or provides an ambiguous token
- `edition`
  - `limited` = limited edition
  - `open` = open edition
  - Defaults to `limited`
  - Open edition uses the platform default supply behavior automatically
- `maxSupply`
  - Total supply cap for the collection
  - Defaults to `999` for limited edition
- `dropBeginTime`
  - Mint start time
  - Unix timestamp in seconds
  - If omitted, defaults to the next day
- `stages`
  - Stage array
  - If provided, it defines the full mint stage set
  - If omitted, the default public stage above is used

## Stage Rules

Each stage may include:

- `stageName`
- `price`
- `duration`
- `maxSupplyAtThisStage`
- `maxMintedPerWallet`
- `interval`
- `stageMode`

Notes:

- `stageID` is never user-controlled
- If the user does not provide stages, do not ask for stage fields unless they want custom mint phases
- The script always assigns stage IDs in order:
  - first stage `256`
  - second stage `257`
  - third stage `258`
  - and so on
- Element stages also support whitelist mode on web
- This skill does not support configuring whitelist mode
- Design detail sections are web-only
- If any web-only feature is needed, edit it in the web UI instead, replacing `your-slug` with the actual drop slug:
  - [https://element.market/collections/your-slug/edit/drop](https://element.market/collections/your-slug/edit/drop)

## Execution Preview

First enter the installed skill's `scripts` directory:

```bash
cd <skill-directory>/scripts
npx tsx src/cli.ts create-drop --preview /tmp/element-drop-create.json
```

The preview should be treated as a transaction preview for the deployment step:

- It should repeat the selected chain and symbol
- It should warn that confirmed execution deploys a real onchain contract
- It should show the transaction summary when available
- It should make clear that preview mode does not broadcast anything

## Execute

```bash
cd <skill-directory>/scripts
npx tsx src/cli.ts create-drop /tmp/element-drop-create.json
```

## Output Focus

- `slug`
- selected chain
- `symbol`
- resolved `contractAddress`
- `Drop URL`
- `Collection URL`
- `Edit URL`
- settings summary
- design summary
- next step: preview publishing this same chain and slug, then publish only after confirmation

## Example Payload

```json
{
  "chainName": "base",
  "name": "ffffff",
  "symbol": "F",
  "paymentToken": "ETH",
  "preReveal": "/absolute/path/to/image.png"
}
```

## Recovery Note

If contract deployment succeeds but later setup fails or times out, do not immediately rerun `create-drop`: that may deploy another contract. Preview the new slug, then use `update-drop` to complete missing settings, prereveal, design, or stage configuration.
If deployment or setup fails, repeat the selected chain and symbol in the error summary. Do not switch to another chain unless the user explicitly asks for that chain.
