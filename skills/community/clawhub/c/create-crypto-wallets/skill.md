---
name: create-crypto-wallets
version: 1.0.1
description: Generate and manage Hierarchical Deterministic (HD) crypto wallets for 200+ cryptocurrencies (Bitcoin, Ethereum, and many more) using the Python `hdwallet` library, via either its CLI or its Python API.
metadata: {"crypto":{"category":"wallets","library":"hdwallet"}}
---

# Create Crypto Wallets

# Overview

[`hdwallet`](https://github.com/hdwallet-io/python-hdwallet) is a Python library and CLI for generating
Hierarchical Deterministic (HD) wallets. It supports 200+ cryptocurrencies and lets you go from
entropy/mnemonic/seed all the way down to derived private keys, public keys, and addresses,
following standard protocols (BIP32/39/44/49/84/86/141, SLIP10, Cardano, Monero, Electrum, etc.)
so keys stay compatible with other wallets and services.


## Setup Instructions
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install python-dotenv hdwallet[cli]
```

## Usage Instructions

There are two ways to use `hdwallet`: the `hdwallet` CLI (fastest for one-off wallet generation)
or the Python API (`from hdwallet import HDWallet`, best when the result needs to be consumed by other code).

### Core concepts

A wallet is derived from one of these "master key" sources (pick exactly one):

- **Entropy** — random bytes (hex), e.g. `-e/--entropy`
- **Mnemonic** — human-readable seed phrase, e.g. `-m/--mnemonic`
- **Seed** — raw seed bytes (hex), e.g. `-s/--seed`
- **Extended key** — `-xprv/--xprivate-key` or `-xpub/--xpublic-key`
- **Raw private/public key** — `-prv/--private-key` / `-pub/--public-key`
- **WIF** — `-w/--wif`

From the master key, `hdwallet` derives keys/addresses using an **HD standard** (`-h/--hd`, default `BIP44`)
for a given **cryptocurrency** (`-sym/--symbol`, default `BTC`) and **network** (`-n/--network`, default `mainnet`),
following a derivation path controlled by `-ac/--account`, `-ch/--change`, `-ad/--address`
(or a raw `-d/--derivation` path).

### CLI: discovering options

```bash
hdwallet --help
hdwallet list cryptocurrencies      # list all supported cryptocurrency symbols
hdwallet list languages             # list supported mnemonic languages
hdwallet list strengths             # list valid entropy strengths (e.g. 128, 160, 192, 224, 256)
```

### CLI: generating a new mnemonic and entropy

```bash
# Generate raw entropy (hex)
hdwallet generate entropy --client BIP39 --strength 128

# Generate a BIP39 mnemonic phrase (12 words for 128-bit strength)
hdwallet generate mnemonic --client BIP39 --words 12 --language english

# Generate a seed from a mnemonic
hdwallet generate seed --client BIP39 --mnemonic "abandon abandon ... about"
```

### CLI: creating a wallet (`hdwallet dump`)

`hdwallet dump` derives and prints one wallet's keys/address as JSON. Supply exactly one master-key
source flag plus the cryptocurrency/HD/network/derivation options you want:

```bash
# New Bitcoin wallet from a freshly generated mnemonic
MNEMONIC=$(hdwallet generate mnemonic --client BIP39 --words 12)
hdwallet dump --symbol BTC --hd BIP44 --network mainnet --mnemonic "$MNEMONIC"

# Ethereum wallet, account 0, address index 0, from an existing mnemonic
hdwallet dump --symbol ETH --hd BIP44 --mnemonic "$MNEMONIC" --account 0 --address 0

# Derive multiple addresses for the same wallet by changing --address
hdwallet dump --symbol BTC --mnemonic "$MNEMONIC" --address 1
```

Key `dump` flags:

| Flag | Purpose |
|------|---------|
| `-sym, --symbol` | Cryptocurrency ticker (default `BTC`) |
| `-h, --hd` | HD standard: `BIP32`, `BIP44`, `BIP49`, `BIP84`, `BIP86`, `BIP141`, `Cardano`, `Electrum-V1`, `Electrum-V2`, `Monero`, `Algorand` (default `BIP44`) |
| `-n, --network` | `mainnet` / `testnet` / etc. (default `mainnet`) |
| `-e, --entropy` / `-ec, --entropy-client` | Master key from entropy hex |
| `-m, --mnemonic` / `-mc, --mnemonic-client` | Master key from mnemonic words |
| `-s, --seed` / `-sc, --seed-client` | Master key from seed hex |
| `-pp, --passphrase` | Optional BIP39 passphrase ("25th word") |
| `-xprv, --xprivate-key` / `-xpub, --xpublic-key` | Master key from an extended key |
| `-prv, --private-key` / `-pub, --public-key` / `-w, --wif` | Master key from a raw private/public key or WIF |
| `-ac, --account` | Account index (default `0`) |
| `-ch, --change` | Change index (default `0`) |
| `-ad, --address` | Address index (default `0`) |
| `-d, --derivation` | Explicit derivation path/name (overrides account/change/address) |
| `-pkt, --public-key-type` | `compressed` (default) or `uncompressed` |
| `-ex, --exclude` | Field names to omit from the output |

The output JSON typically includes fields such as `cryptocurrency`, `symbol`, `network`, `hd`,
`entropy`, `mnemonic`, `seed`, `root_xprivate_key`, `root_xpublic_key`, `xprivate_key`, `xpublic_key`,
`private_key`, `wif`, `public_key`, `chain_code`, `address`, and the derivation `path`.

### CLI: batch export (`hdwallet dumps`)

`hdwallet dumps` is like `dump` but designed for deriving many addresses/rows at once and exporting
as CSV or JSON — useful for generating a range of addresses for one wallet:

```bash
hdwallet dumps --symbol BTC --mnemonic "$MNEMONIC" --format json
hdwallet dumps --symbol BTC --mnemonic "$MNEMONIC" --format csv --include-header --delimiter ","
```

Extra flags vs. `dump`: `-f/--format` (`csv` default or `json`), `-in/--include` and `-ex/--exclude`
(pick/drop output fields), `-inh/--include-header` (CSV header row), `-de/--delimiter` (CSV delimiter).

### Python API

For programmatic wallet generation, use the `HDWallet` class:

```python
from hdwallet import HDWallet
from hdwallet.hds import BIP44HD
from hdwallet.cryptocurrencies import Bitcoin
from hdwallet.entropies.bip39 import BIP39Entropy, BIP39_ENTROPY_STRENGTHS
from hdwallet.mnemonics.bip39 import BIP39Mnemonic

# 1. Generate fresh entropy, then a mnemonic from it
entropy = BIP39Entropy.generate(strength=BIP39_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT)
mnemonic = BIP39Mnemonic.from_entropy(entropy=entropy)  # 12-word phrase

# 2. Build the HD wallet for Bitcoin using BIP44 derivation
wallet: HDWallet = HDWallet(
    cryptocurrency=Bitcoin,
    hd=BIP44HD,
    network="mainnet",
).from_mnemonic(mnemonic=BIP39Mnemonic(mnemonic=mnemonic))

# 3. Read the derived keys/address
print(wallet.mnemonic())        # the mnemonic phrase — BACK THIS UP, it recovers the whole wallet
print(wallet.private_key())     # derived private key (hex)
print(wallet.public_key())      # derived public key (hex)
print(wallet.address())         # derived address for the configured account/change/address index
print(wallet.xprivate_key())    # extended private key (xprv...)
print(wallet.xpublic_key())     # extended public key (xpub...)
```

Other `HDWallet` constructors for recovering/loading an existing wallet instead of generating a new
one: `HDWallet.from_entropy(entropy)`, `HDWallet.from_seed(seed)`, `HDWallet.from_xprivate_key(...)`,
`HDWallet.from_xpublic_key(...)`, `HDWallet.from_private_key(...)`, `HDWallet.from_public_key(...)`,
`HDWallet.from_wif(...)`, `HDWallet.from_derivation(...)`.

To enumerate supported cryptocurrencies in code:

```python
from hdwallet.cryptocurrencies import CRYPTOCURRENCIES
print(CRYPTOCURRENCIES.classes())  # list of all supported Cryptocurrency classes
```

## Security

- **The mnemonic/entropy/seed/private key is the wallet.** Anyone with it has full control of funds.
  Never print these to shared logs, commit them to version control, or send them over an insecure channel.
- Prefer deriving from a mnemonic you generate once and store securely, rather than regenerating
  entropy per-session — regenerating creates a brand-new, unrelated wallet each time.
- If writing wallet material to disk, restrict file permissions (e.g. `chmod 600`) and keep the
  file out of any directory tracked by git (add it to `.gitignore`).
- Use a dedicated wallet with a minimal balance for agentic/automated use to limit exposure if the
  key is ever leaked.

## Resources

- Clawhub skill: **[keepass-cli](https://clawhub.ai/beocca/skills/keepass-cli)** — store the mnemonic/private keys generated here in a
  local, password-protected KeePass (`.kdbx`) database instead of plaintext files. Use it to create
  an entry per wallet (e.g. title `hdwallet:<symbol>:<address>`) with the mnemonic/private key in
  the password/notes field, so secrets are encrypted at rest rather than left in shell history or
  loose JSON files.
  Directly install via `openclaw skills install @beocca/keepass-cli`



