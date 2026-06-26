# Quick API map

Use this file first when the task is operational and you want the shortest path to the right API.

## get_magiclink

Use when the user wants to register, sign up, or get started with Cleanverse / ClevrPay.

- Required params: none
- Returns: registration URL
- Common phrasing:
  - how do I sign up
  - how do I get started
  - how do I get A-Pass
  - send me the registration link

## query_apass

Use when the user wants to check eligibility / status for a wallet.

- Required params: `chain`, `address`
- Optional: `symbol`
- Returns: tier, expiration, state, group-related data
- Common phrasing:
  - check my payment eligibility
  - is this wallet verified
  - does this address have A-Pass
  - can this wallet receive compliant payment

## query_deposit_address

Use when the user wants to know where to send supported funds.

- Required params: `chain`, `address`
- Optional: `symbol`
- Returns: deposit wallet address(es)
- Common phrasing:
  - where do I send USDC
  - what is my deposit address
  - where can I deposit funds
  - how do I move clean funds into Cleanverse

## query_deposit_institutions

Use when the user wants to know which institutions / sources are allowed for deposit.

- Required params: `chain`, `symbol`
- Returns: deposit whitelist
- Common phrasing:
  - which institutions can deposit
  - what custodians are allowed
  - what is the whitelist source for deposit

## query_chain_config

Use when the user asks about support coverage or when any static doc may be stale.

- Required params: none
- Returns: live chain/token/access config
- Common phrasing:
  - what chains are supported
  - what tokens are supported
  - does Cleanverse support this network

## query_user

Use when the user wants to check whether a wallet is already registered or mapped.

- Required params: `chain`, `symbol`, `address`
- Returns: deposit mapping and status
- Common phrasing:
  - is my wallet registered
  - check my mapping
  - what deposit address is linked to my wallet

## register_data

Use when the wallet needs to be registered / mapped for a chain and token.

- Required params: `chain`, `symbol`, `address`
- Returns: user address and deposit address mapping
- Common phrasing:
  - register my wallet
  - bind my address
  - set up my deposit mapping

## Decision shortcut

- signup / registration link -> `get_magiclink`
- check qualification / status -> `query_apass`
- get deposit address -> `query_deposit_address`
- check allowed deposit source -> `query_deposit_institutions`
- confirm supported chains/tokens -> `query_chain_config`
- check existing registration -> `query_user`
- create registration mapping -> `register_data`
