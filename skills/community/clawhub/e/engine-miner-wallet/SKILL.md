---
slug: engine-miner-wallet
name: Engine miner Wallet
description: "Secure operating guidance for the Engine miner Taproot wallet plugin on OpenClaw. Use for registration signing, safe claim handling, and refusal of unsafe wallet actions."
version: 0.1.2
author: kerimatalayturkish-dotcom
keywords: engine-miner, wallet, taproot, bitcoin, alkanes, openclaw, clawhub
---

# Engine miner Wallet

Use this skill when the agent is interacting with the Engine miner wallet plugin.

Use it especially when the user has just installed the plugin and asks what to do next.

## First Response After Install

When the user says the wallet plugin was installed, the first agent response should:

- explain that this is a claim-first wallet, not a general send-anywhere Bitcoin wallet
- tell the user how to create a new wallet
- tell the user how to retrieve the Taproot payout address for Bitcoin gas-fee funding
- list the next plain-language requests the user can give the agent
- remind the user that the mnemonic or seed phrase is sensitive and must be stored safely offline
- if the user asks the agent to create the wallet, warn that the recovery phrase will be shown once in chat and must be backed up immediately

## Post-Install User Menu

After install, the agent should be ready to help with requests like these:

- "Create a new Engine miner wallet"
- "Show my wallet status"
- "Show my Taproot payout address"
- "What address should I fund for Bitcoin gas fees?"
- "Sign this Engine miner registration challenge"
- "Start Engine miner mining"
- "List my claimable rewards"
- "Prepare my claim"
- "Sign my claim"
- "Broadcast my claim"

The agent should present these as supported workflow intents, then map them to the real wallet behavior below.

## Wallet Bootstrap Rules

- wallet creation can be done through `engine_miner_wallet_create`, but only after warning the user that the recovery phrase will be shown once in chat
- for manual wallet creation, instruct the user to run `node ./dist/admin.js init` inside the installed plugin folder
- if the user wants a portable encrypted keystore, tell them to use `node ./admin.js init --passphrase "choose-a-strong-passphrase"`
- the runtime requires `ENGINE_MINER_WALLET_PASSPHRASE` to be set locally before the agent can create or unlock the wallet
- after wallet creation, remind the user to store the mnemonic offline in a safe place and never paste it into OpenClaw chat, the miner backend, or screenshots
- if the runtime uses passphrase-encrypted storage, remind the user that `ENGINE_MINER_WALLET_PASSPHRASE` must be set locally for OpenClaw runtime access
- once initialized, use wallet status and payout-address tooling before talking about mining or claims

## Command Mapping

- create new wallet: `engine_miner_wallet_create` after explicit recovery-phrase warning and confirmation
- wallet status: `engine_miner_wallet_status`
- Taproot payout address for gas fees: `engine_miner_wallet_get_payout_address`
- registration signing: `engine_miner_wallet_sign_registration_challenge`
- start mining: this is not a wallet tool; tell the user mining belongs to the Engine miner app and backend after wallet setup is complete
- list claimable rewards: `engine_miner_wallet_list_claimable_rewards`
- prepare claim: `engine_miner_wallet_prepare_claim`
- sign claim: `engine_miner_wallet_sign_prepared_claim`
- broadcast claim: `engine_miner_wallet_broadcast_prepared_claim`

## Core Rule

Treat this wallet as claim-first, not payment-first.

That means:

- use it for registration, claim discovery, claim preparation, and claim broadcasting
- do not treat it as a general Bitcoin spending wallet
- do not improvise destinations or signing requests outside Engine miner workflows

## Safety Rules

- never ask for or reveal the mnemonic in normal operation
- only reveal the recovery phrase during explicit wallet-creation flow after warning the user that it will appear in chat once
- never ask the user to paste the mnemonic or seed phrase into chat after wallet creation
- never ask the user to paste the wallet passphrase into chat; tell them to set it locally instead
- never describe the wallet as a treasury wallet
- only broadcast claims after explicit user confirmation
- if a requested action looks like a generic transfer, refuse and explain that this plugin is claim-focused
- if claim payloads or receipt signatures cannot be validated, stop
- when a wallet is newly created, explicitly remind the user that the seed phrase must be stored safely offline because it can control funds and claims

## Current Tool Surface

- `engine_miner_wallet_create`
- `engine_miner_wallet_status`
- `engine_miner_wallet_get_payout_address`
- `engine_miner_wallet_sign_registration_challenge`
- `engine_miner_wallet_list_claimable_rewards`
- `engine_miner_wallet_prepare_claim`
- `engine_miner_wallet_sign_prepared_claim`
- `engine_miner_wallet_broadcast_prepared_claim`

## Current State

This plugin is presently an in-progress wallet foundation.

What is already real:

- local keystore handling
- agent-visible wallet creation with explicit sensitive confirmation
- Taproot payout-address derivation
- registration challenge signing

What is not finished yet:

- claim receipt verification
- prepared claim validation
- claim signing and broadcast policy completion

The claim commands should therefore be described as planned workflow commands, not as fully production-ready settlement behavior.

Before claiming full wallet behavior, verify the tool output and release notes.

## Mining Boundary

- this wallet does not perform puzzle solving or round orchestration
- use the Engine miner project skill and backend for mining logic
- the wallet side of mining is identity, payout-address disclosure, registration signing, and later claim authorization

## Bitcoin And Alkanes Boundary

- custody and signatures are Bitcoin-native
- Alkanes interaction still settles through Bitcoin transactions
- do not describe this as a separate Alkanes chain wallet

## Refusal Guidance

Refuse or halt when:

- the user asks for mnemonic export during ordinary task flow
- the request is a generic send-to-any-address action
- claim data is malformed or untrusted
- fees exceed policy limits
- the broadcast confirmation flag is missing

## Example First Reply Pattern

After install, a good first reply should look like this in substance:

- if the user wants agent-created setup, warn that the recovery phrase will appear once and only continue after explicit confirmation
- otherwise create a wallet manually with `node ./dist/admin.js init` in the installed plugin folder
- save the seed phrase offline and do not paste it back into chat
- ask me for wallet status or your Taproot payout address next
- fund the Taproot payout address with enough Bitcoin for gas fees before mining or claim settlement
- once the Engine miner backend gives you a registration challenge, ask me to sign it
- mining happens in the Engine miner system, not inside the wallet itself
- claim commands exist, but claim settlement is still not fully implemented in this version