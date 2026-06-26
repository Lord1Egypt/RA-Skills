# Node types — when to choose which

`--type` at install time.

| Type | Role | Services | Rewards | Storage footprint |
|---|---|---|---|---|
| `dev` | Local development | node only; hardhat fake L1 | none | minimal, everything in memory |
| `fullnode` | Verifier + relay | node + agent | marginal (relay fees) | 256 MiB – several GiB |
| `validator` | BFT block production + verification | node + agent | high (block rewards + fees) | 256 MiB – TB (archive-grade optional) |
| `archive` | Historical state serving | node + agent + archive mode | moderate (PoSe service fees) | TB-scale |
| `gateway` | JSON-RPC / IPFS fan-out for clients | node + relayer | moderate (gateway fees) | 256 MiB – GiB |

## Choosing

- **First time, just want to poke around** → `dev` + `--network local` (hardhat). No chain identity, no gas.
- **Run a node that contributes storage to testnet** → `fullnode` + `--network testnet`. Minimum viable participant.
- **Become a validator** → requires stake + peer approval. `--type validator` installs the role; staking happens on-chain afterward.
- **Mirror full history** → `archive`. Expensive disk-wise; appropriate for block explorers and analytics.
- **Edge ingress for end-users** → `gateway`. Accepts RPC / IPFS from clients; no block production.

Validator selection is stake-weighted and rotates deterministically. See the [COC whitepaper §XII](https://github.com/NGPlateform/COC/blob/main/docs/COC_whitepaper.en.md) for the consensus model.
