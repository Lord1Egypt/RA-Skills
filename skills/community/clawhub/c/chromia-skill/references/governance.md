# Governance & Provider Staking Reference

## Table of Contents

- [Governance Overview](#governance-overview)
- [Governance Tool for EVM](#governance-tool-for-evm)
- [Provider Types](#provider-types)
- [Staking Requirements](#staking-requirements)
- [User Delegation](#user-delegation)
- [dApp Deployment & Providers](#dapp-deployment--providers)
- [Configuration Relevance](#configuration-relevance)

---

## Governance Overview

Chromia governance operates at two levels:

1. **Network governance**: Providers vote on proposals affecting the network (adding providers, protocol changes)
2. **dApp governance**: Individual dApps can implement on-chain voting using the Governance Tool

A Governance Module for native CHR stakers (nominating providers, proposing grants) is on the roadmap.

---

## Governance Tool for EVM

A pre-built, on-chain voting solution for EVM-based projects, built on Chromia with EIF integration.

### Features

- Gas-free voting on Chromia
- EVM tokens (ERC-20) as voting power (staked or held)
- Customizable framework: proposal creation, voting phases, veto rights
- Auto-executable commands via extendable functions
- Roles: citizens, administrators, councilors

### Governance Lifecycle

1. **Citizen registration**: On-chain onboarding
2. **Proposal creation**: Draft with title, category, duration
3. **Voting phase**: Citizens cast votes during designated period
4. **Veto process**: Councilors/admins can block harmful proposals
5. **Execution**: Approved proposals execute automatically

### Configuration

The Governance Tool uses EIF libraries for EVM integration:

```yaml
libs:
  eif:
    registry: https://gitlab.com/chromaway/eif-lib
    path: rell/src/lib/eif
    tagOrBranch: <version>
  eif_event_receiver:
    registry: https://gitlab.com/chromaway/eif-lib
    path: rell/src/lib/eif_event_receiver
    tagOrBranch: <version>
  eif_event_connector:
    registry: https://gitlab.com/chromaway/eif-lib
    path: rell/src/lib/eif_event_connector
    tagOrBranch: <version>
```

EIF config tracks `Transfer` and `StakeUpdate` events from EVM governance contracts.

---

## Provider Types

### System Providers

- Operate nodes in the **system cluster**
- Manage core infrastructure and system chains
- Vote on critical network proposals (adding new system providers, cluster creation)
- Can run nodes in both system and dApp clusters

### Node Providers

- Run nodes in **dApp clusters** only
- Supply infrastructure for deployed dApps
- Can be promoted to system provider via system provider vote

---

## Staking Requirements

| Provider Type | Total Stake Required | Minimum Self-Stake |
|---|---|---|
| System Provider | 600,000 CHR per node | 60,000 CHR (10%) |
| Node Provider | 300,000 CHR per node | 30,000 CHR (10%) |

- Self-stake must be **native CHR** on Chromia Mainnet
- Delegated stake can come from native CHR, ERC-20 CHR, or BEP-20 CHR
- Each node has a unique key pair for identification

### Provider Compensation

- Providers receive compensation from hosting fees paid by dApps
- Providers can share rewards with delegators (configurable percentage)
- Managed via PMC CLI commands:
  - `pmc economy set-provider-staking-account`
  - `pmc economy update-provider-staking-reward-share`

---

## User Delegation

Any CHR holder can stake by delegating to a provider:

- **Reward rate**: 3% APR in native CHR + share of network fees
- **Unbonding period**: 14 days (336 hours) — no rewards during unbonding
- **Access**: Via Chromia Vault UI
- Delegate once — future stakes auto-assign to selected provider

### Choosing a Provider

Consider: uptime/performance, commission rates, total stake level.

---

## dApp Deployment & Providers

When deploying a dApp to mainnet:

1. dApp developer **leases a container** from the network
2. Container is hosted across multiple provider nodes in a dApp cluster
3. dApp pays **hosting fees** (predictable, similar to cloud hosting)
4. No per-transaction gas fees for end users

### Container Leasing

- Select required extensions (Stork Oracle, Vector DB, AI Inference, etc.)
- Specify resource requirements
- Managed through Chromia deployment tooling

---

## Configuration Relevance

Governance modules interact with `chromia.yml` through:

- **moduleArgs**: Admin pubkeys, governance parameters
- **EIF config**: For tracking EVM-based voting tokens
- **Extension config**: For oracle feeds used in governance decisions

### Example: Governance dApp Config

```yaml
blockchains:
  governance:
    module: governance_module
    moduleArgs:
      governance:
        admin_pubkey: "PLACEHOLDER_PUBKEY"
        voting_period_blocks: 1000
        veto_period_blocks: 500
    config:
      eif:
        chains:
          ethereum:
            network_id: 1
            contracts:
              - "0x..."  # Governance token contract
            events: !include ./config/events.yaml
      gtx:
        modules:
          - "net.postchain.eif.EifGTXModule"
      sync_ext:
        - "net.postchain.eif.EifSynchronizationInfrastructureExtension"
```

---

## Key Points for Agents

- Never hardcode provider staking amounts — they may change through governance
- dApp hosting fees are paid to the network, not individual providers
- Governance proposals can change network parameters — always check current state
- The Governance Tool is EVM-focused; native CHR governance module is forthcoming
