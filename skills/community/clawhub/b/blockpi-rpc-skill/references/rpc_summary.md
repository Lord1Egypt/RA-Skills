# BlockPI Protocol Catalog Summary

Total chains indexed: 48

| Chain | Methods | Protocols | RU Table |
|---|---:|---|---|
| aptos | 25 | jsonrpc (25) | aptos-movement-ru-table.md |
| arbitrum | 37 | jsonrpc (37) | evm-ru-table.md |
| artela | 34 | jsonrpc (34) | evm-ru-table.md |
| avalanche | 37 | jsonrpc (37) | evm-ru-table.md |
| base | 40 | jsonrpc (40) | evm-ru-table.md |
| berachain | 35 | jsonrpc (35) | evm-ru-table.md |
| bitcoin | 17 | jsonrpc (17) | evm-ru-table.md |
| blast | 35 | jsonrpc (35) | evm-ru-table.md |
| blockpi | 4 | jsonrpc (4) | N/A |
| bsc | 43 | jsonrpc (43) | evm-ru-table.md |
| celo | 36 | jsonrpc (36) | evm-ru-table.md |
| celo-1 | 32 | jsonrpc (32) | evm-ru-table.md |
| conflux | 23 | jsonrpc (23) | evm-ru-table.md |
| cosmos-hub | 121 | jsonrpc (121) | cosmos-zetachain-ru-table.md |
| cronos | 39 | jsonrpc (39) | evm-ru-table.md |
| ethereum | 115 | jsonrpc (115) | evm-ru-table.md |
| fantom-and-sonic | 43 | jsonrpc (43) | evm-ru-table.md |
| gnosis | 32 | jsonrpc (32) | evm-ru-table.md |
| kaia | 63 | jsonrpc (63) | evm-ru-table.md |
| linea | 40 | jsonrpc (40) | evm-ru-table.md |
| mantle | 34 | jsonrpc (34) | evm-ru-table.md |
| merlin | 39 | jsonrpc (39) | evm-ru-table.md |
| meter | 28 | jsonrpc (28) | evm-ru-table.md |
| meter-1 | 28 | jsonrpc (28) | evm-ru-table.md |
| metis | 32 | jsonrpc (32) | evm-ru-table.md |
| movement | 25 | jsonrpc (25) | aptos-movement-ru-table.md |
| near | 25 | jsonrpc (25) | near-ru-table.md |
| oasys | 40 | jsonrpc (40) | evm-ru-table.md |
| op | 45 | jsonrpc (45) | evm-ru-table.md |
| polygon | 49 | jsonrpc (49) | evm-ru-table.md |
| scroll | 40 | jsonrpc (40) | evm-ru-table.md |
| scroll-1 | 38 | jsonrpc (38) | evm-ru-table.md |
| solana | 59 | grpc (7), jsonrpc (52) | solana-eclipse-ru-table.md |
| starknet | 22 | jsonrpc (22) | N/A |
| story | 31 | jsonrpc (31) | evm-ru-table.md |
| story-1 | 22 | jsonrpc (22) | evm-ru-table.md |
| story-2 | 30 | jsonrpc (30) | evm-ru-table.md |
| story-3 | 25 | jsonrpc (25) | evm-ru-table.md |
| story-4 | 36 | jsonrpc (36) | evm-ru-table.md |
| sui | 79 | graphql (1), grpc (22), jsonrpc (56) | N/A |
| taiko | 42 | jsonrpc (42) | evm-ru-table.md |
| ton | 29 | jsonrpc (29) | N/A |
| unichain | 36 | jsonrpc (36) | evm-ru-table.md |
| viction | 39 | jsonrpc (39) | evm-ru-table.md |
| zetachain | 135 | jsonrpc (135) | evm-ru-table.md |
| zetachain-evm | 38 | jsonrpc (38) | evm-ru-table.md |
| zkfair | 30 | jsonrpc (30) | evm-ru-table.md |
| zksync-era-and-abstract | 45 | jsonrpc (45) | evm-ru-table.md |

## Notes
- Protocol is inferred from official doc layout such as sui/json, sui/grpc, solana/json-rpc, and solana/yellowstone-grpc.
- Sui gRPC and Sui GraphQL are marked with higher preference than deprecated Sui JSON-RPC.
- Solana Yellowstone gRPC is cataloged so routing can prefer it for streaming or low-latency designs.