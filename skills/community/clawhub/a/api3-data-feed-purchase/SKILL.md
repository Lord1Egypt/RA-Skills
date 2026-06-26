---
name: api3-data-feed-purchase
description: Purchases API3 data feed subscriptions from market.api3.org.
metadata:
  version: 0.1.0
  clawdis:
    requires:
      bins:
        - ts-node
        - pnpm
      env:
        - WALLET_MNEMONIC
    primaryEnv: WALLET_MNEMONIC
---

# Api3 Data Feed Purchase


## Variables

| Variable | Description |
|---|---|
| `DAPI_NAME` | Exact feed name from the dAPI list (e.g. `ETH/USD`) |
| `CHAIN_ALIAS` | Chain alias from the chain list (e.g. `ethereum`) |
| `CHAIN_NAME` | Human-readable chain name (e.g. `Ethereum Mainnet`) |
| `CHAIN_ID` | Numeric chain ID (e.g. `1`) |
| `DEVIATION` | Deviation threshold — must be exactly one of: `0.25`, `0.5`, `1`, `2.5`, `5` |
| `PROXY_ADDRESS` | Reader proxy contract address — starts with `0x`, exactly 42 characters |

---

# Rules
- **NEVER** read .env files or ask for secrets such as WALLET_MNEMONIC.
- **ALWAYS** use the `exec` tool to run commands. Never use Bash or shell directly.
- **ALWAYS** run scripts in skill's directory, which is referenced as `{baseDir}` variable and name is given in this file's name field at top. Prefix every command with `cd {baseDir} &&` to ensure it runs from the correct directory.
- **ALWAYS** substitute actual variable values into every `exec` command before running it.
- **ALWAYS** after asking any question, stop and wait for the user's response. Do not assume a response or continue until the user has replied.
- **ALWAYS** complete the current phase fully before moving to the next. Never skip a phase or assume it is already done.
- Treat affirmative responses as approval (e.g. "yes", "sure", "ok", "go ahead", "yep"). Treat negative responses as rejection (e.g. "no", "nope", "cancel", "stop"). If intent is unclear, ask once more before acting.
- **NEVER** wrap URLs in markdown formatting (backticks, asterisks, brackets, etc.) or add trailing punctuation when sharing them with the user — share the raw URL as plain text so it stays clickable and isn't corrupted with extra characters.
- **ALWAYS** lowercase `<CHAIN_ALIAS>` and the feed/token symbol (e.g. the base of `<DAPI_NAME>`) when substituting them into market.api3.org URL paths (e.g. `https://market.api3.org/ethereum/eth-usd/integrate`), even if the confirmed values are stored/displayed with different casing.

## Phase 0: Introduction

- Introduce the skill: you will walk the user through purchasing an Api3 data feed subscription on-chain, step by step. You will ask for approval before installing packages and before executing the purchase transaction.
- Ask if they are ready to begin and wait for an affirmative response before continuing.

---

## Phase 1: Package Installation

### Part 1.1

- **You must always run this step. Do not skip it, even if you think packages are already installed.**
- Inform the user that before any scripts can run, the required packages must be installed. Show them the list:
  - `@api3/dapi-management`
  - `dotenv`
  - `ethers`
- Ask for approval to run `pnpm install`. Wait for an affirmative response. Once approved, run the command regardless of whether packages may already be installed:
```
exec command="cd {baseDir} && pnpm install"
```
- If the output contains `[ERR_PNPM_IGNORED_BUILDS] Ignored build scripts: unrs-resolver...`, this is expected and not a real failure — the ignored build script is not needed for this skill. Treat it as success and continue.
- If the command fails for any other reason, inform the user and ask what to do. This step cannot be skipped.

---

## Phase 2: Collect User Input

### Part 2.1
- Ask the user for all three inputs in one message:
  - **Feed name** — which data feed they want (e.g. `ETH/USD`). Direct them to https://market.api3.org to browse available feeds.
  - **Chain** — which network they want to use (name or alias, e.g. `ethereum`).
  - **Deviation threshold** — must be exactly one of: `0.25`, `0.5`, `1`, `2.5`, `5` (percent).
- Wait for all three answers before continuing.

### Part 2.2
- Run `get-dapis.ts` and `get-chains.ts` to fetch the list of available feeds and supported chains:
```
exec command="cd {baseDir} && ts-node {baseDir}/scripts/get-dapis.ts"
exec command="cd {baseDir} && ts-node {baseDir}/scripts/get-chains.ts"
```
- If script fails, let user know about the problem and ask what to do. This data is necessary for validating their input, so skipping is not an option.

### Part 2.3
- Validate `DAPI_NAME`:
  - Search the output of `get-dapis.ts` for an entry matching the user's feed name exactly (case-insensitive).
  - Match found: set `DAPI_NAME` to the exact string from the list (preserve its casing) and confirm the matched value to the user.
  - No match: inform the user, direct them to https://market.api3.org for the exact feed name, and wait for a new value. Repeat this step.

- Validate `CHAIN_ALIAS`:
  - Search the output of `get-chains.ts` — first by `alias` field (case-insensitive), then by `name` field.
  - Match found: set `CHAIN_ALIAS`, `CHAIN_NAME`, `CHAIN_ID` from that entry. Confirm the match with the user and ask if it is correct. If not, ask them to re-enter and repeat this step.
  - No match: inform the user, direct them to https://market.api3.org for supported chains, and wait for a new value. Repeat this step.

- Validate `DEVIATION`:
  - Check that the value is exactly one of: `0.25`, `0.5`, `1`, `2.5`, `5`.
  - Valid: set `DEVIATION`.
  - Invalid: inform the user of the valid options and wait for a new answer. Repeat this step.

### Part 2.4

- Show the user a summary of their selected options:
  - Feed: `<DAPI_NAME>`
  - Chain: `<CHAIN_NAME>`
  - Deviation Threshold: `<DEVIATION>%`
- Ask the user to confirm that they want to proceed with these options. If no, ask the user what they want to do.
- If yes, ask whether they'd also like to explore the data feed first — i.e. see the live value each data provider is currently reporting for this feed before getting a price quote. If yes, proceed to Phase 3. If no, skip ahead to Phase 4.

---

## Phase 3: Check Live Provider Values (Optional)

### Part 3.1
- Explain to the user that before continuing, you'll show them the live value each data provider is currently reporting for this feed, so they can sanity-check the data before paying for it.
- Run `explore-data-feeds.ts`, which fetches each provider's Signed API data and decodes the live value for this feed directly:
```
exec command="cd {baseDir} && ts-node {baseDir}/scripts/explore-data-feeds.ts <DAPI_NAME>"
```
- If the script fails, let the user know about the problem and ask what to do.

### Part 3.2
- The script prints, for each provider: API Alias, Data Feed ID, Signed API URL, Value, and Timestamp (or an explanation if no value could be retrieved).
- Show the user a summary table of these fields for each provider exactly as reported by the script — do not re-fetch or re-derive any of these values yourself.
- Proceed to Phase 4.

---

## Phase 4: Get Price Quote

### Part 4.1
- Run `quote.ts` to fetch the live subscription price for the selected feed, chain, and deviation:
```
exec command="cd {baseDir} && ts-node {baseDir}/scripts/quote.ts <DAPI_NAME> <CHAIN_ALIAS> <DEVIATION>"
```
- If script fails, let user know about the problem and ask what to do.

### Part 4.2
- Extract and show these fields from the output:
| Field | Label to show |
|---|---|
| `Feed Name` | Feed |
| `Chain` | Chain |
| `Heartbeat Interval` | Heartbeat Interval (seconds) |
| `Deviation Threshold` | Deviation Threshold |
| `Subscription Duration` | Subscription Duration (seconds) |
| `Price (ETH)` | Price (ETH) |

- Ask the user to confirm that they want to proceed with these options. If yes, proceed to Phase 5. If no, ask the user what they want to do.

---

## Phase 5: Execute Purchase

### Part 5.1
- Explain user that you are ready to complete the purchase. You will run `buy.ts`, which will execute a blockchain transaction to purchase the subscription.
- Explain this script will use the `WALLET_MNEMONIC` environment variable to sign the transaction. Make sure the user has WALLET_MNEMONIC set in `.env` file in the root of this skill.
- Ask if the `.env` file is ready with the correct mnemonic and if they want you to run the purchase script. Wait for an affirmative response before proceeding. Then run the following command if answer is affirmative:

(substitute actual variable values when running):
```
exec command="cd {baseDir} && ts-node {baseDir}/scripts/buy.ts <DAPI_NAME> <CHAIN_ALIAS> <DEVIATION>"
```
- If script fails, let user know about the problem and ask what to do.

### Part 5.2
- Extract the `hash` value from the output and show the purchase summary: feed, chain, deviation, subscription duration, and transaction hash.
- Proceed to Phase 6.

---

## Phase 6: Read the Data Feed

### Part 6.1
- Ask user if they want to read the data feed now. If yes, proceed. If no, inform the user the subscription is active, but its always better to check and stop.
- Ask the user to retrieve their Reader Proxy address by:
  - Going to https://market.api3.org/<CHAIN_ALIAS>/<DAPI_NAME lowercased, with `/` replaced by `-`>/integrate
  - Copying the proxy contract address and sharing it here.
- Wait for the user to provide the proxy address.
- Validate the proxy address:
  - Must start with `0x`.
  - Must be exactly 42 characters long.
  - If either check fails: inform the user of the requirements and wait again.
- Set `PROXY_ADDRESS` to the valid value.

### Part 6.2
- Run `read-data-feed.ts` to fetch the latest value and timestamp from the proxy contract:
```
exec command="cd {baseDir} && ts-node {baseDir}/scripts/read-data-feed.ts <PROXY_ADDRESS> <CHAIN_ALIAS>"
```
- If script fails, let user know about the problem and ask what to do.
- Extract and show the value and timestamp from the output.
- Inform the user the feed is active and readable and congratulate them on successfully purchasing an Api3 data feed subscription!
