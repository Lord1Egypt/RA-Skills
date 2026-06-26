# Publish Stage Reference

## When to Use

- The drop has already been created and configured, and is now ready to publish
- The drop is currently paused and should be switched back to live state
- The drop is already live and should be switched into paused state

## Minimum Required Parameters

- `chainName`
  - A user-facing chain name
  - Examples: `base`, `arbitrum`, `bsc`
  - The script resolves it internally to the corresponding chain configuration
- `slug`
  - The user-facing Element drop or collection slug
  - The script resolves it internally to the identifiers required by the backend

## Preconditions

- The drop has already been created
- Settings and design have already been configured
- A valid prereveal asset has already been configured on the drop
- Publish uses the configured prereveal image and resolves the publish-ready prereveal URI automatically
- If prereveal readiness times out, ask the user to re-upload the prereveal image and retry
- If the user needs to change the sale currency first, use `update-drop` with `paymentToken` before publishing
- `publish-drop` can be used for first publish, for resuming a paused drop, and for pausing an already live drop

## Optional Behavior

- By default, publish makes the drop live
- If the user explicitly asks to keep the drop paused, the agent uses the internal paused publish mode
- A paused drop can be resumed by running `publish-drop` without paused mode
- An already live drop can be paused by running `publish-drop` in paused mode

## Execution Preview

First enter the installed skill's `scripts` directory:

```bash
cd <skill-directory>/scripts
npx tsx src/cli.ts publish-drop --preview /tmp/element-drop-publish.json
```

The preview should be treated as a transaction preview for the publish step:

- It should confirm a prereveal image is configured and can become publish-ready
- It should warn that confirmed execution sends a real onchain publish transaction
- It should show the transaction summary when available
- It should make clear that preview mode does not broadcast the transaction

## Execute

```bash
cd <skill-directory>/scripts
npx tsx src/cli.ts publish-drop /tmp/element-drop-publish.json
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
- publish transaction hash
- whether platform synchronization completed
- final availability state
- final `dropBeginTime`
- final `edition`
- final `maxSupply`
- final resolved `paymentToken`
- final full stage summary
- final `Drop URL`
- final `Collection URL`
- final `Edit URL`
