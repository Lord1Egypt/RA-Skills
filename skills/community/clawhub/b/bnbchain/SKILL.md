---
name: bnbchain-mcp
displayName: bnbchain-mcp
version: 1.0.2
description: Interact with the BNB Chain Model Context Protocol (MCP) server. Blocks, contracts, tokens, NFTs, wallet, Greenfield, and ERC-8004 agent tools. Use npx @bnb-chain/mcp@latest or read the official skill page.
---

# BNB Chain MCP Skill

This skill allows you to interact with the BNB Chain MCP server to retrieve data and perform actions on BNB Chain and other EVM-compatible networks.

---

## Before you install

- **Credentials:** Signing keys and RPC endpoints are supplied by you (see *Credentials and environment* below). Never paste private keys into a UI or an env var you don’t control. To reduce risk, agents can generate their own wallet (and use it for registration or testnet actions) instead of using an existing user wallet. Ask the skill author or [documentation](https://github.com/bnb-chain/bnbchain-mcp) how they are stored and who can access them.
- **Install mechanism:** Use **`npx @bnb-chain/mcp@latest`** to run the MCP server; it fetches from the npm registry at runtime. If you prefer to audit first, install the package locally and review the [source code](https://github.com/bnb-chain/bnbchain-mcp) before use.
- **Read-only vs state-changing:** Many tools are read-only (blocks, balances, contract reads). Tools such as `transfer_*`, `write_contract`, `approve_token_spending`, and ERC-8004 registration require a `PRIVATE_KEY` and perform on-chain transactions. If you want read-only use only, do not supply a private key and avoid invoking state-changing tools.
- **Sandbox and testnet:** Run in a restricted environment when possible. Use a testnet wallet with no mainnet funds when testing transactions or registration.
- **Install manifest and env:** Required and optional environment variables are listed below. Verify there is no hidden credential collection; the MCP server uses only the env you explicitly provide (e.g. in your MCP client config).

---

## 1. How to connect

Use **`npx @bnb-chain/mcp@latest`** to connect to the BNB Chain MCP server.

---

## 2. Credentials and environment

- **RPC / network:** The MCP server uses public or configured RPC endpoints for supported chains (BSC, opBNB, Greenfield, etc.). You do not need to supply RPC URLs for default chains unless you self-host or override.
- **Private key (optional):** State-changing tools (`transfer_native_token`, `transfer_erc20`, `transfer_nft`, `write_contract`, `register_erc8004_agent`, `set_erc8004_agent_uri`, Greenfield writes, etc.) require a **`PRIVATE_KEY`** in the environment where the MCP server runs (e.g. in your Cursor/Claude MCP config). The key is used only to sign transactions; it is not stored or logged by the server. If `PRIVATE_KEY` is not set, those tools will fail; read-only tools (get block, get balance, read_contract, etc.) work without it.
- **Where to set:** Configure `PRIVATE_KEY` in the same place you configure the MCP server (e.g. `env` in `mcpServers.bnbchain-mcp` in your client’s config). Never commit keys to version control or share them with untrusted parties.
- **Summary:** No credentials are required for read-only use. For transfers, contract writes, or agent registration, you must supply `PRIVATE_KEY` in the MCP server’s environment; the agent or client does not collect or store it beyond what you configure.

---

## 3. Agent registration

**First:** Register yourself on-chain using the MCP tool **`register_erc8004_agent`** (see ERC-8004 Agent tools below). **Then** owners can check registration on the scan site:

- **Mainnet:** **[https://www.8004scan.io/](https://www.8004scan.io/)**
- **Testnet:** Agents should inform their owners to visit **[https://testnet.8004scan.io/](https://testnet.8004scan.io/)** to see their registration

---

## 4. Available Prompts and Tools

*(From [BNBChain MCP README](https://github.com/bnb-chain/bnbchain-mcp).)*

### Prompts

| Name                   | Description                                                         |
| ---------------------- | ------------------------------------------------------------------- |
| analyze_block          | Analyze a block and provide detailed information about its contents |
| analyze_transaction    | Analyze a specific transaction                                      |
| analyze_address        | Analyze an EVM address                                              |
| interact_with_contract | Get guidance on interacting with a smart contract                   |
| explain_evm_concept    | Get an explanation of an EVM concept                                |
| compare_networks       | Compare different EVM-compatible networks                           |
| analyze_token          | Analyze an ERC20 or NFT token                                       |
| how_to_register_mcp_as_erc8004_agent  | Get guidance on registering an MCP server as an ERC-8004 agent       |

### Tools

**Read-only** tools (no `PRIVATE_KEY` needed): block/transaction/balance/contract-read queries, `get_*`, `read_contract`, `is_contract`, etc. **State-changing** tools (require `PRIVATE_KEY` in env): `transfer_*`, `approve_token_spending`, `write_contract`, ERC-8004 register/set_uri, Greenfield create/upload/delete, etc.

### Network parameter

Most EVM tools accept **`network`** (e.g. `bsc`, `opbnb`, `ethereum`, `base`). Use **`get_supported_networks`** to list options.

- **Read-only tools** (blocks, balances, contract reads, `get_chain_info`, etc.): **`network`** is optional; default is `bsc`.
- **Write operations** (`transfer_native_token`, `transfer_erc20`, `transfer_nft`, `transfer_erc1155`, `approve_token_spending`, `write_contract`, `register_erc8004_agent`, `set_erc8004_agent_uri`, Greenfield writes): **`network` is REQUIRED.** There is no default for writes. If the user does not specify the network, you **MUST ask** before calling the tool. Do not assume or default to mainnet (`bsc`); accidental mainnet execution causes irreversible financial loss.

| Name                         | Description                                                                  |
| ---------------------------- | ---------------------------------------------------------------------------- |
| get_block_by_hash            | Get a block by hash                                                          |
| get_block_by_number          | Get a block by number                                                        |
| get_latest_block             | Get the latest block                                                         |
| get_transaction              | Get detailed information about a specific transaction by its hash            |
| get_transaction_receipt      | Get a transaction receipt by its hash                                        |
| estimate_gas                 | Estimate the gas cost for a transaction                                      |
| transfer_native_token        | Transfer native tokens (BNB, ETH, MATIC, etc.) to an address                 |
| approve_token_spending       | Approve another address to spend your ERC20 tokens                           |
| transfer_nft                 | Transfer an NFT (ERC721 token) from one address to another                   |
| transfer_erc1155             | Transfer ERC1155 tokens to another address                                   |
| transfer_erc20               | Transfer ERC20 tokens to an address                                         |
| get_address_from_private_key | Get the EVM address derived from a private key                               |
| get_chain_info               | Get chain information for a specific network                                 |
| get_supported_networks       | Get list of supported networks                                               |
| resolve_ens                  | Resolve an ENS name to an EVM address                                        |
| is_contract                  | Check if an address is a smart contract or an EOA                            |
| read_contract                | Read data from a smart contract (view/pure function)                          |
| write_contract               | Write data to a smart contract (state-changing function)                     |
| get_erc20_token_info         | Get ERC20 token information                                                  |
| get_native_balance           | Get native token balance for an address                                      |
| get_erc20_balance            | Get ERC20 token balance for an address                                      |
| get_nft_info                 | Get detailed information about a specific NFT                                |
| check_nft_ownership          | Check if an address owns a specific NFT                                      |
| get_erc1155_token_metadata   | Get the metadata for an ERC1155 token                                        |
| get_nft_balance              | Get the total number of NFTs owned by an address from a specific collection  |
| get_erc1155_balance          | Get the balance of a specific ERC1155 token ID owned by an address           |

### ERC-8004 Agent tools

Register and resolve AI agents on the [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004) Identity Registry. Supported networks: BSC (56), BSC Testnet (97), Ethereum, Base, Polygon, and their testnets where the [official registry](https://github.com/erc-8004/erc-8004-contracts) is deployed. The `agentURI` should point to a JSON metadata file following the [Agent Metadata Profile](https://best-practices.8004scan.io/docs/01-agent-metadata-standard.html).

| Name                    | Description                                                                 |
| ----------------------- | --------------------------------------------------------------------------- |
| register_erc8004_agent  | Register yourself on the ERC-8004 Identity Registry (do this before checking the scan site); returns agent ID |
| set_erc8004_agent_uri   | Update the metadata URI for an existing ERC-8004 agent (owner only)         |
| get_erc8004_agent       | Get agent info (owner and tokenURI) from the Identity Registry              |
| get_erc8004_agent_wallet| Get the verified payment wallet for an agent (for x402 / payments)           |

### Greenfield tools

| Name                          | Description                                         |
| ----------------------------- | --------------------------------------------------- |
| gnfd_get_bucket_info          | Get detailed information about a specific bucket    |
| gnfd_list_buckets             | List all buckets owned by an address                |
| gnfd_create_bucket            | Create a new bucket                                 |
| gnfd_delete_bucket            | Delete a bucket                                     |
| gnfd_get_object_info          | Get detailed information about a specific object    |
| gnfd_list_objects             | List all objects in a bucket                        |
| gnfd_upload_object            | Upload an object to a bucket                        |
| gnfd_download_object          | Download an object from a bucket                    |
| gnfd_delete_object            | Delete an object from a bucket                      |
| gnfd_create_folder            | Create a folder in a bucket                         |
| gnfd_get_account_balance      | Get the balance for an account                      |
| gnfd_deposit_to_payment       | Deposit funds into a payment account                |
| gnfd_withdraw_from_payment    | Withdraw funds from a payment account               |
| gnfd_disable_refund           | Disable refund for a payment account (IRREVERSIBLE) |
| gnfd_get_payment_accounts     | List all payment accounts owned by an address       |
| gnfd_get_payment_account_info | Get detailed information about a payment account   |
| gnfd_create_payment           | Create a new payment account                        |
| gnfd_get_payment_balance      | Get payment account balance                         |

---

## 5. Safety and best practices

1. **Confirm before sending transactions:** For `transfer_*`, `write_contract`, or `approve_token_spending`, confirm recipient, amount, and network before calling the tool.
2. **Network required for writes:** For any write (transfers, `write_contract`, `approve_token_spending`, ERC-8004 register/set_uri, Greenfield writes), you **MUST** have an explicit network from the user. If not specified, **ask** — do not default to mainnet. Do not use advisory language like "prefer testnet" as a substitute; the constraint is: no network specified → do not call the write tool until the user confirms.
3. **Private keys:** Only in MCP server `env`; never in chat or logs.
