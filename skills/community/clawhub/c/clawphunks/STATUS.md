# ClawPhunks Status - March 4, 2026

## What Works

### Minting (x402)
- **API**: `POST https://clawphunks.vercel.app/mint` with `{"recipient": "0x..."}`
- **Payment**: $1.99 USDC on Base via x402 (EIP-3009 signature)
- **Self-hosted facilitator**: Executes USDC transfer on Base, pays gas
- **Output**: Ethscription on L1 + 0.00005 ETH gas stipend (~$0.12)

### Collection Display
- **Page**: https://chainhost.online/clawphunks
- **Item pages**: https://chainhost.online/clawphunks/[id]
- **Skills page**: https://chainhost.online/clawphunks/skills (complete mint + list code)
- **Data source**: Ethscriptions AppChain RPC (`mainnet.ethscriptions.com`)
- **Contract**: `0x5ED5a160483462Bbb36cB30bA10f60Ea4708D839`

### Images
- All 10k phunks facing LEFT (like CryptoPhunks) - FIXED
- Stored in Supabase as ESIP-6 data URIs with traits
- #9590 was right-facing before fix (minted before regeneration)

### Trading
- **Escrow Contract**: `0x3e67d49716e50a8b1c71b8dEa0e31755305733fd` (L1)
- **Functions**:
  - `depositAndList(bytes32 ethscriptionId, uint256 priceWei)`
  - `buy(bytes32 ethscriptionId)` payable
  - `cancelAndWithdraw(bytes32 ethscriptionId)`
  - `getListing(bytes32 ethscriptionId)` view

## Minted Items
- **#0**: Collection creator token
- **#9590**: First mint, listed at 0.69 ETH
- **#5031**: Second test mint
- **Total on-chain**: 3

## MCP Server
- **NPM**: `clawphunks-mcp@1.2.0`
- **Tools**:
  - `get_collection` - Collection info and stats
  - `mint_phunk` - Mint with x402 (returns 402 with payment requirements)
  - `get_mint_code` - Complete TypeScript code for x402 minting
  - `get_rarity` - Rarity info and rare token IDs
  - `get_trading_instructions` - Complete mint + list code

## Key Addresses
- **Signer/Deployer**: `0xe16340DCB633FB386c324Eea219F2b3Ec59d4aC9`
- **USDC on Base**: `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`
- **Payment Recipient**: `0xe16340DCB633FB386c324Eea219F2b3Ec59d4aC9`
- **Escrow Contract**: `0x3e67d49716e50a8b1c71b8dEa0e31755305733fd`
- **Collection Contract**: `0x5ED5a160483462Bbb36cB30bA10f60Ea4708D839`

## Environment Variables (Vercel - clawphunks)
- `SIGNER_PRIVATE_KEY` - L1 minting wallet
- `ETHEREUM_RPC_URL` - L1 RPC
- `BASE_RPC_URL` - Base RPC (for facilitator)
- `SUPABASE_URL` / `SUPABASE_SERVICE_KEY` - Item database
- `PAYMENT_RECIPIENT` - Where USDC goes
- `FACILITATOR_URL` - Self-hosted at same domain
- `GAS_STIPEND_WEI` - `50000000000000` (0.00005 ETH)

## Files
- `/Users/jef/clawphunks/src/server.ts` - Main API
- `/Users/jef/clawphunks/src/facilitator.ts` - x402 facilitator
- `/Users/jef/clawphunks/src/mint.ts` - L1 minting
- `/Users/jef/clawphunks/src/db.ts` - Supabase
- `/Users/jef/clawphunks/mcp/src/index.ts` - MCP server
- `/Users/jef/chainhost/src/app/clawphunks/page.tsx` - Collection frontend
- `/Users/jef/chainhost/src/app/clawphunks/[id]/page.tsx` - Item detail page
- `/Users/jef/chainhost/src/app/clawphunks/skills/page.tsx` - Skills/docs page

## TODO
- [ ] Test browser mint end-to-end
- [ ] Create new test wallet (old one exposed)
