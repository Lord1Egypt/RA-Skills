# BracketsBot

Generate and validate BracketsBot bracket predictions for AI agents and model developers.

This package is designed for standalone use: tournament bracket data is bundled with the package, and wallet submission is expected to happen through your existing wallet stack.

## Core Principles

- Canonical winner identifier is `seed` (`1..64`)
- Prediction output is always 63 picks in game order
- Default submission flow is unsigned tx preparation (`prepare-submit-tx`)
- Agents and developers use the same CLI surface

## Commands

- `bracketsbot validate`
- `bracketsbot generate`
- `bracketsbot walk-next`
- `bracketsbot walk-apply --winner-seed <seed>`
- `bracketsbot walk-run-policy --policy-module <path>`
- `bracketsbot semantic-run --policy "<text>" --predictions-file <file>`
- `bracketsbot prepare-submit-tx`
- `bracketsbot share-link` (generate frontend URL for human review; defaults to in-progress walk state; use `--predictions-file ./out/model-bracket-output.json` for a full bracket)

Use `--json` for tool-calling integrations and `--help` on each command for options.

## For Agents

### Recommended Flow

1. `bracketsbot generate --json`
2. `bracketsbot validate --json`
3. `bracketsbot prepare-submit-tx --json`
4. submit tx with your wallet capability (for example, Bankr)

### Stepwise Agent Loop

1. `bracketsbot walk-next --json`
2. apply user policy in natural language to returned matchup context
3. `bracketsbot walk-apply --winner-seed <seed> --json`
4. repeat until `done: true`
5. `bracketsbot prepare-submit-tx --json`

Natural-language policy example:

- "Pick based on mascot battle outcomes."
- For each matchup, the agent reasons in chat and then applies the chosen seed with `walk-apply`.

### One-Pass Semantic Run

If your agent can reason the full bracket in one pass, use:

```bash
bracketsbot semantic-run \
  --policy "Pick based on mascot battle outcomes." \
  --predictions-file ./my-semantic-picks.json \
  --json
```

Where `my-semantic-picks.json` contains either:

- a raw array of 63 winner seeds, or
- an object with `predictions` array.

## Sharing Picks to the Frontend

The main BracketsBot frontend can load a full or in-progress bracket from a URL query parameter.

- **Param name**: `p`
- **Encoding**: `encodeURIComponent(btoa(JSON.stringify(value)))`
- **Accepted shapes**:
  - raw array: `number[]` of winner seeds (`1..64`), length `1..63` for in-progress or full brackets
  - object: `{ predictions: number[], ... }` (this matches `bracket-output.schema.json`), with `predictions.length` between `1` and `63`

Example link builder (Node or browser):

```js
const picks = bracketOutput.predictions; // length 1..63, values 1..64
const payload = { predictions: picks };
const encoded = encodeURIComponent(btoa(JSON.stringify(payload)));
const url = `https://brackets.bot/?p=${encoded}`;
```

Opening this URL in the frontend will pre-fill the bracket UI (only those picks; no auto-fill) with the provided predictions, allowing a human to continue picking, review, and submit on-chain.

**share-link default:** The CLI reads `./out/model-walk-picks.json` by default (same as the stepwise walk). So after `walk-apply` you can run `share-link` with no arguments to get a link for the current in-progress bracket. For a full bracket from `generate`, run `share-link --predictions-file ./out/model-bracket-output.json`.

## For Developers

### Policy-Driven Flow

Implement a policy module and run:

```bash
bracketsbot walk-run-policy --policy-module ./my-policy.mjs --json
```

Policy contract:

- export `chooseWinner` (or pass `--policy-export`)
- input includes matchup + round + picks context
- return winner as seed (`number|string`) or object with `seed`

Example policy shape:

```js
export async function chooseWinner({ teamA, teamB }) {
  return teamA.profile.teamRating >= teamB.profile.teamRating ? teamA.seed : teamB.seed;
}
```

Reference implementation: `examples/policies/simple-rating-policy.mjs`.

## Submission Model

Primary production path:

- run `prepare-submit-tx` to get `{ chainId, to, data, value }`
- sign and broadcast with your own wallet runtime

The CLI only prepares unsigned transaction payloads; signing and broadcasting happen in your external wallet stack.

