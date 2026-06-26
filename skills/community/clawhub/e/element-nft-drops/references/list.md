# List Stage Reference

## When to Use

- Show the user's current Element Drop list on a supported chain
- Look up existing drop `name` and `slug` values before preview, update, or publish
- Confirm which collections on a chain are actual Element Drops

## Minimum Required Parameters

- `chainName`
  - A user-facing chain name
  - Examples: `base`, `arbitrum`, `bsc`
  - The script resolves it internally to the corresponding chain configuration

## Common Optional Parameters

- `walletAddress`
  - Optional override
  - If omitted, the script derives the address from `ELEMENT_WALLET_PRIVATE_KEY`
- `first`
  - Forward pagination size
- `after`
  - Forward pagination cursor
- `last`
  - Backward pagination size
- `before`
  - Backward pagination cursor

## Run

First enter the installed skill's `scripts` directory:

```bash
cd <skill-directory>/scripts
npx tsx src/cli.ts list-user-drops /tmp/element-drop-list.json
```

## Example Payload

```json
{
  "chainName": "base"
}
```

## Output Focus

- `drops[].name`
- `drops[].slug`
- `drops[].isVerified`
- `pageInfo`
