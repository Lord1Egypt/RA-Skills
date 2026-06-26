---
name: element-drop
description: Use when the user mentions Element plus drops, NFT creation, NFT collection launch, mint setup, sale stages, prereveal media, preview media, or publishing/pausing/resuming a drop. Also use when they want to create an NFT on Element, create an Element collection/drop, configure mint price/supply/payment token/stages, preview current drop settings/design, update drop media or description, publish a configured drop, or provide chainName, slug, contractAddress, paymentToken, or a local image path for drop work. Read-only preview/list actions may run immediately; every state-changing flow must show an execution preview first, clearly distinguish preview from real execution, then wait for confirmation.
requires: ["node", "jq"]
metadata: {"openclaw":{"requires":{"bins":["node","npm"],"env":["ELEMENT_WALLET_PRIVATE_KEY"]},"primaryEnv":"ELEMENT_WALLET_PRIVATE_KEY"}}
---

# Element Drop

Use this skill for Element Drop lifecycle work: create a drop, preview current configuration, update settings or design, publish a configured drop, resume a paused drop, or pause a live drop.
This skill is not for marketplace trading, collection analytics, wallet portfolio inspection, or generic Element protocol research.
Run the bundled lifecycle commands under `scripts/`; do not default to ad-hoc API calls.

## Runtime Setup

Required environment variable:

- `ELEMENT_WALLET_PRIVATE_KEY`

Example:

```bash
export ELEMENT_WALLET_PRIVATE_KEY="your_wallet_private_key_here"
```

The private key must only be provided through `ELEMENT_WALLET_PRIVATE_KEY`; do not paste it into chat, JSON payloads, files for this skill, or command arguments. The scripts validate it as a `0x`-prefixed 32-byte hex key, use it only for local message and transaction signing, and redact the configured key from known error output. The raw private key is never sent over the network. The scripts may upload media, call Element APIs, and broadcast signed transactions after confirmation, so use a dedicated low-risk wallet.

Only upload user-provided NFT media images. Do not upload secrets, keys, dotfiles, shell configs, environment files, source archives, or arbitrary local documents. The bundled scripts validate uploads as regular local image files and reject symlinks, unsupported extensions, oversized files, and files whose bytes do not match the declared image type.

## Routing Contract

First classify the task, then read the matching reference before you answer with field guidance, collect parameters, or run commands:

- `Create`: new Element NFT collection/drop, stopping before publish
- `List`: show current drops and their `name` / `slug`
- `Preview`: inspect existing settings, design, prereveal media, or public availability
- `Update`: change settings, prereveal image, design fields, design media, or stages
- `Publish`: publish, resume a paused drop, or pause a live drop
- `List chains`: inspect supported chains or payment tokens

- Create: [references/create.md](./references/create.md)
- List: [references/list.md](./references/list.md)
- Preview: [references/preview.md](./references/preview.md)
- Update: [references/update.md](./references/update.md)
- Publish: [references/publish.md](./references/publish.md)

Do not guess supported chains, supported payment tokens, lifecycle defaults, or field constraints from memory. If the user is doing a relevant operation and asks or implies uncertainty about those values, read the matching reference first, then use the read-only command when live data is needed.
Do not use this skill for buying, selling, bidding, canceling, floor price, volume, rankings, activity history, inventory, or portfolio queries.
If the user asks about field meaning or code behavior in the context of Element Drop lifecycle work, this skill may be used for explanation, but do not run lifecycle commands unless the user is actually performing a lifecycle action.

## Confirmation Rules

Read-only commands run immediately:

- `list-user-drops`
- `preview-drop`
- `list-chains`

State-changing commands require preview first:

- `create-drop`
- `update-drop`
- `publish-drop`

For any state-changing command:

1. Gather the minimum required parameters for the lifecycle stage.
2. Run preview mode first.
3. Show a concise execution preview using business language.
4. Wait for explicit positive confirmation.
5. Execute only after confirmation.

If execution includes an onchain transaction, also state that continuing will send a real blockchain transaction, identify the user-visible action that sends it, and make clear that preview mode does not broadcast.

Every preview, execution confirmation, and failure report must repeat the selected chain. For create/deploy flows, also repeat the contract `symbol`. Never silently switch chains after an RPC or network problem; if the requested chain fails, report that chain and ask for a new explicit user instruction before using another chain.

## User-Facing Parameters

General:

- Use `chainName`; do not ask users for chain IDs.
- Use `slug` as the main identifier for existing drops.
- Resolve backend identifiers internally.
- Do not ask for hidden backend IDs when `slug` is enough.
- Local media paths must be absolute.
- Local media paths must point to real image files (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`); never use paths to credentials or system files.
- `paymentToken` accepts token name, symbol, or address.

Settings:

- `edition`: `limited` or `open`
- `maxSupply`: required when switching to limited edition
- `dropBeginTime`: mint start time
- `paymentToken`: sale currency
- `stages`: full mint stage array replacement when provided
- `preReveal`: pre-reveal image path

Design:

- `previewMedia`: design preview image path array
- `name`
- `description` / `desc`
- `website`: must be a complete URL
- `twitter`, `instagram`, `discord`, `telegram`, `medium`: users may provide suffix or full link; send suffix to backend
- `bannerFilePath`
- `dropFeaturedImage`

Do not expose backend-only identifiers, status flags, or compatibility storage names in user-facing summaries. Use business language such as chain, slug, live/paused/draft, prereveal image, preview images, and availability.

## Lifecycle Rules

Create:

- Required: `chainName`, `name`, `symbol`, `preReveal`.
- When a create request starts, proactively state these required fields, ask for any that are missing, and then state the defaults that will be applied if the user does not override them.
- Optional overrides include settings, stages, design media, design copy, website/social links, and payment token.
- Default mint start time is the next day.
- Default edition is limited edition with total supply `999`.
- Default preview image is the same image as `preReveal`.
- Default stage is one public stage with sale price `0`, duration `3 days`, phase supply equal to the collection supply, max `1` mint per wallet, no interval, and public mode.
- Create deploys and configures the drop but does not publish by default.
- After create succeeds, tell the user the drop is configured but not live yet, then guide them to preview publishing the same `chainName` + `slug` before confirmed publish execution.

Update:

- Required: `chainName`, `slug`.
- Patch semantics: only explicitly provided fields change; omitted fields keep remote values.
- If `stages` is provided, it replaces the full stage array.
- Stage IDs are not user-controlled.
- Updating settings or prereveal on a live drop requires republish and therefore an onchain confirmation.
- Updating a paused drop, design-only fields, design media, or collection profile fields does not force republish.

Publish:

- Required: `chainName`, `slug`.
- Covers first publish, resuming a paused drop, and pausing a live drop.
- Default target is live.
- If the user asks to keep it paused or pause a live drop, use the paused publish target.
- Publish requires an existing configured prereveal image. The publish flow prepares that image for the live drop configuration automatically; if readiness times out, tell the user to re-upload the prereveal image and retry.

## Web-Only Features

Element Drop supports these features, but this skill does not currently configure them:

- Whitelist stage configuration
- Design detail sections

For those, use the web editor and replace `your-slug` with the actual drop slug:

- [https://element.market/collections/your-slug/edit/drop](https://element.market/collections/your-slug/edit/drop)

## Reporting Contract

For previews, clearly label the response as preview-only and say no changes were applied.
For execution, summarize only the user-visible result.

Include the relevant fields for the lifecycle stage:

- Create: chain, symbol, slug, contract address, collection URL, drop URL, edit URL, settings summary, design summary, recommended next publish action
- List: chain, wallet, drop names, slugs, returned count
- Preview: chain, slug, availability state, mint start time, edition, supply, payment token, stages, design/prereveal media status, links
- Update: chain, slug, fields changed, whether republish was needed, updated settings/design summaries, links
- Publish: chain, slug, transaction hash if sent, final availability state, settings summary, links

Use these business labels in user-facing output:

- `draft`, `live`, `paused` for availability
- `limited edition`, `open edition` for edition
- `prereveal image` for prereveal media
- `preview images` for design preview media
- `sale currency` for payment token

## Failure Reporting

Do not say only "failed".
State the failed lifecycle stage, the relevant error or response summary, and the actionable recovery.
If required parameters are missing, state exactly which user-facing parameters are missing.
For upload, API, or onchain failures, identify the segment in business language.
Always repeat the selected chain in the failure message. For create/deploy failures, repeat the symbol too.

## Absolute Do-Nots

- Do not request or echo the private key.
- Do not execute state-changing commands before confirmation.
- Do not interpret "create" as "create and publish" by default.
- Do not overwrite unspecified fields with defaults during `update-drop`.
- Do not show internal script choreography or backend-only identifiers in normal user-facing output.
