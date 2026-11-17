# Config and auth

**Done when:** the platforms you need have `trading` `ready`, or the remaining failure is auth or funding explained from the CLI `message`. `creation: unsupported` on Polymarket/Kalshi is expected.

## Find the CLI

Try in order. Stop at the first that prints a version.

1. `forecast --version`
2. `./forecast --version` or `./forecast.exe --version` in the current directory
3. Execute this skill's `scripts/install.sh` (the `scripts` folder next to `SKILL.md`). It downloads a GitHub release binary and verifies `checksums.txt`. Install into the current directory:

```bash
INSTALL_DIR="$PWD" sh scripts/install.sh
./forecast --version
```

Run that script from the skill directory, or pass its absolute path. Do not pipe a URL into `sh`. If the environment blocks the download, request approval and retry the same script. After install, call `./forecast` or `./forecast.exe` until that directory is on `PATH`.

If install still fails, tell the user the CLI is required and what blocked it. Stop. Do not scrape markets or invent a substitute path.

Do not borrow a random `forecast-cli` venv. Do not write fake keys to make discovery work.

## Config resolution order

1. `--config <path>` on the subcommand
2. `--config <path>` on the root `forecast` command
3. `FORECAST_CONFIG` environment variable
4. `./forecast_config.toml` in the current working directory

TOML sections: `[global]`, `[kalshi]`, `[polymarket]`, `[precog]`. Unknown keys/sections are rejected.

## Setup loop

Use this loop only for writes, or when the user asked to set up trading. Do not run `forecast setup --no-input` until credentials exist.

1. `forecast status --output json --no-input`. Add `--platform` when only one is needed.
2. Quote is not a write. Pause before `predict --confirm`, sell, live-account sync, and claim except Kalshi when `trading` is not `ready` or `auth` is `needs setup`. For Precog create, gate only on auth: proceed when the key is set and valid, even with zero balance. Creation only signs and moves no funds.
3. **Credentials pause** when `error.code` is `CONFIG_INVALID` or `AUTH_FAILED`, or `auth` is `needs setup` with a credentials message (`Credentials are not set.`, `The private key is not set.`, relayer credentials not set). Use the matching platform section below. Do not invent keys. A zero-balance `INSUFFICIENT_BALANCE` message is not a credentials pause and never blocks creation.
4. **Funding** when `error.code` is `INSUFFICIENT_BALANCE` or `INSUFFICIENT_ALLOWANCE`, or `auth` is `set` and `trading` is `not ready`. Show the CLI `message`. Do not replay the key hunt. Funding blocks buys, sells, and launchpad funding. It does not block Precog market creation. Older binaries may still report `creation: not ready` alongside zero balance; ignore that combination when the key is valid.
5. `creation: unsupported` on Polymarket and Kalshi is expected.

## Secrets

Pass keys via env vars or gitignored `*_file` paths. Never CLI argv, never tracked TOML, never echoed back. Prefer a file the user writes. `config --show` redacts secrets. Interactive `setup` without `--no-input` may hold keys in-session only. Agents stay on `--no-input`.

Launchpad fund/claim scripts (`scripts/fund_upcoming.py`, `scripts/claim_upcoming.py`) resolve the Precog key and RPC like the CLI: `--key-file` > `PRECOG_PRIVATE_KEY` > `forecast_config.toml [precog]` (`private_key_file` / `private_key`), and `--rpc` > `BASE_RPC` / `ARBITRUM_RPC` > `[precog] base_rpc` / `arbitrum_rpc`. See [fund-launchpad.md](../workflows/fund-launchpad.md). Never echo keys.

## Resume

After the user returns artifacts, run only the platform whose keys arrived:

```bash
forecast setup --platform <platform> --no-input --output json
forecast status --platform <platform> --output json --no-input
```

## Polymarket

If credentials are missing, stop. Do not scrape polymarket.com or invent keys. Tell the user:

Poly is read-only. You need to finalize setup.

1. Create a new account in a wallet of your choosing (MetaMask, WalletConnect, or any provider). Prefer a dedicated wallet, not a daily-driver seed.
2. Log in at [polymarket.com](https://polymarket.com) with that wallet.
3. Generate a Relayer API key under Settings → Relayer API keys ([Connect your account](https://docs.polymarket.com/trading/wallets-auth#connect-your-account)). Copy the **API Key** and **Signer Address**.
4. Come back with the wallet **private key** (the signer that logged in) plus the relayer **API key** and **signer address**.

Wait until they return those three values. Missing relayer with a private key still uses this pause, not funding.

Map:

- Exactly one of `private_key`, `private_key_file`, or `POLYMARKET_PRIVATE_KEY`
- Both `relayer_api_key` / `POLYMARKET_RELAYER_API_KEY` and `relayer_api_key_address` / `POLYMARKET_RELAYER_API_KEY_ADDRESS`

## Precog

If the private key is missing, stop. Do not invent a key. Tell the user they need to put a private key. Recommend creating a new dedicated wallet, not a daily-driver seed. Wait until they return the key.

Map exactly one of `private_key`, `private_key_file`, or `PRECOG_PRIVATE_KEY`. Create and buy also need `[precog]` RPCs: `base_rpc` and `arbitrum_rpc` (plus `api_url` / `chain`).

## Kalshi

If credentials are missing, stop. Do not invent keys. Do not teach RSA-PSS signing. The CLI signs. Tell the user:

Kalshi is read-only. You need to finalize setup.

1. Log in at [kalshi.com](https://kalshi.com) (or [demo.kalshi.co](https://demo.kalshi.co) if they are on demo).
2. Account & security → API Keys → Create Key. Walkthrough: [Authenticated requests](https://docs.kalshi.com/getting_started/quick_start_authenticated_requests).
3. Save both values now. The private key cannot be retrieved after that page closes.
   - **API Key ID** (UUID on screen)
   - **Private Key** (downloaded `.key` RSA PEM)
4. Come back with those two. Prefer the downloaded file over pasting PEM into chat. Recommend a new API key for the CLI, not reusing an old one.

Wait until they return both.

Map:

- `api_key_id` / `KALSHI_API_KEY_ID`
- RSA PEM via exactly one of `private_key`, `private_key_file`, or `KALSHI_PRIVATE_KEY`

Prefer `private_key_file` pointing at the downloaded `.key`. Default `api_url` is production (`https://external-api.kalshi.com/trade-api/v2`). Do not switch to demo unless the user said they are on demo.
