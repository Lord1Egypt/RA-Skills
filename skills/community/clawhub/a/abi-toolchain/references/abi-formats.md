# ABI Formats Reference

The ABI (Application Binary Interface) is the specification that tells callers how to encode/decode data for a smart contract. Every function call, event, and error on-chain is encoded according to the ABI.

## JSON ABI Format

An ABI is a JSON array of entry objects. Each entry describes one callable item.

```json
[
  { "type": "constructor", "inputs": [...], "stateMutability": "nonpayable" },
  { "type": "function",    "name": "transfer", "inputs": [...], "outputs": [...], "stateMutability": "nonpayable" },
  { "type": "event",       "name": "Transfer", "inputs": [...], "anonymous": false },
  { "type": "error",       "name": "InsufficientBalance", "inputs": [...] },
  { "type": "receive",     "stateMutability": "payable" },
  { "type": "fallback",    "stateMutability": "nonpayable" }
]
```

## Entry Types

### function
```json
{
  "type": "function",
  "name": "transfer",
  "inputs": [
    { "name": "to",     "type": "address" },
    { "name": "amount", "type": "uint256" }
  ],
  "outputs": [
    { "name": "", "type": "bool" }
  ],
  "stateMutability": "nonpayable"
}
```

### constructor
```json
{
  "type": "constructor",
  "inputs": [
    { "name": "initialSupply", "type": "uint256" }
  ],
  "stateMutability": "nonpayable"
}
```

### event
```json
{
  "type": "event",
  "name": "Transfer",
  "inputs": [
    { "name": "from",  "type": "address", "indexed": true  },
    { "name": "to",    "type": "address", "indexed": true  },
    { "name": "value", "type": "uint256", "indexed": false }
  ],
  "anonymous": false
}
```

### error (custom errors, Solidity 0.8+)
```json
{
  "type": "error",
  "name": "InsufficientBalance",
  "inputs": [
    { "name": "available", "type": "uint256" },
    { "name": "required",  "type": "uint256" }
  ]
}
```

### receive and fallback
```json
{ "type": "receive",  "stateMutability": "payable" }
{ "type": "fallback", "stateMutability": "nonpayable" }
```

## stateMutability Values

| Value | Meaning |
|-------|---------|
| `pure` | Does not read or modify state. No `msg.value`. |
| `view` | Reads state but does not modify it. No `msg.value`. |
| `nonpayable` | Modifies state. Reverts if ETH is sent with the call. |
| `payable` | Modifies state. Accepts ETH (`msg.value` may be nonzero). |

## Common ABI Types

| Solidity Type | ABI Type | Notes |
|---------------|----------|-------|
| `uint256` | `"uint256"` | Also matches bare `uint` |
| `int256` | `"int256"` | Also matches bare `int` |
| `address` | `"address"` | 20 bytes, padded to 32 in calldata |
| `bool` | `"bool"` | Encoded as uint256 (0 or 1) |
| `bytes` | `"bytes"` | Dynamic-length byte array |
| `bytes32` | `"bytes32"` | Fixed 32-byte array |
| `string` | `"string"` | Dynamic UTF-8 string |
| `uint256[]` | `"uint256[]"` | Dynamic array |
| `uint256[3]` | `"uint256[3]"` | Fixed-size array |
| `(address,uint256)` | `"tuple"` + components | Struct / tuple |

### Tuples (Structs)

Solidity structs become tuples in the ABI. The `type` is `"tuple"` and the fields are in `components`:

```json
{
  "name": "order",
  "type": "tuple",
  "components": [
    { "name": "tokenIn",  "type": "address" },
    { "name": "tokenOut", "type": "address" },
    { "name": "amount",   "type": "uint256" }
  ]
}
```

In Solidity: `struct Order { address tokenIn; address tokenOut; uint256 amount; }`

### uint vs uint256

`uint` and `uint256` are identical in Solidity. In the ABI, they always appear as `"uint256"`. Same for `int`/`int256`.

## Function Selectors

A function selector is the first 4 bytes of `keccak256(functionSignature)`.

**Signature format:** `functionName(type1,type2)` — no spaces, no parameter names.

```bash
# Compute with cast (Foundry):
cast sig "transfer(address,uint256)"
# → 0xa9059cbb

cast sig "balanceOf(address)"
# → 0x70a08231

cast sig "getUserAccountData(address)"
# → 0xbf92857c
```

**In calldata:** The first 4 bytes of any transaction `data` field are the selector. The remaining bytes are ABI-encoded arguments.

```
0xa9059cbb                              ← selector (transfer)
000000000000000000000000deadbeef...     ← address (padded to 32 bytes)
0000000000000000000000000000000000000000000000000de0b6b3a7640000  ← uint256 (1e18 = 1 ETH)
```

## Event Topics

Events are identified by a 32-byte topic (full keccak256, no truncation):

```bash
cast keccak "Transfer(address,address,uint256)"
# → 0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef
```

- `topics[0]` = event signature hash
- `topics[1..3]` = indexed params (up to 3), each padded to 32 bytes
- `data` = non-indexed params, ABI-encoded

`anonymous: true` events do not emit a signature topic — they cannot be filtered by event name.

## Foundry Artifact Structure

Foundry's `forge build` outputs artifacts to `out/<ContractName>.sol/<ContractName>.json`:

```json
{
  "abi": [ ... ],                     ← ABI array
  "bytecode": {
    "object": "0x608060...",          ← creation bytecode
    "sourceMap": "...",
    "linkReferences": {}
  },
  "deployedBytecode": {
    "object": "0x608060...",          ← runtime bytecode
    "sourceMap": "...",
    "immutableReferences": {}
  },
  "methodIdentifiers": {              ← selector → function name map
    "transfer(address,uint256)": "a9059cbb",
    "balanceOf(address)": "70a08231"
  },
  "metadata": { ... }                 ← compiler metadata
}
```

**Extract ABI from Foundry artifact:**
```bash
jq '.abi' out/MyToken.sol/MyToken.json
jq '.abi' out/MyToken.sol/MyToken.json > frontend/src/abis/MyToken.json
```

**Extract all selectors:**
```bash
jq '.methodIdentifiers' out/MyToken.sol/MyToken.json
```

## Hardhat Artifact Structure

Hardhat outputs to `artifacts/contracts/<ContractName>.sol/<ContractName>.json`:

```json
{
  "contractName": "MyToken",
  "abi": [ ... ],
  "bytecode": "0x608060...",
  "deployedBytecode": "0x608060...",
  "linkReferences": {},
  "deployedLinkReferences": {}
}
```

Same `jq '.abi'` extraction works identically.

## Common Gotchas

**1. Tuple types in ABI vs Solidity syntax**

In a function signature string (for selector computation), tuples use parentheses:
- Solidity: `function foo(MyStruct s)` where `MyStruct` has fields `(address a, uint256 b)`
- Selector signature: `foo((address,uint256))` — inner type, no field names

```bash
cast sig "foo((address,uint256))"   # correct
cast sig "foo(MyStruct)"            # WRONG — won't match on-chain
```

**2. uint vs uint256 in signatures**

Always use the canonical form in selector signatures:
```bash
cast sig "transfer(address,uint256)"  # ✅ correct
cast sig "transfer(address,uint)"     # ❌ wrong — won't match
```

**3. Indexed event params**

Indexed params appear in `topics`, not `data`. When decoding logs:
- `indexed: true` → decode from `log.topics[1+]`
- `indexed: false` → decode from `log.data`
- Dynamic types (`string`, `bytes`, arrays) when indexed are stored as their keccak256 hash — you cannot recover the original value

**4. as const for TypeScript ABI types**

```typescript
// Without as const: TypeScript sees string[], loses all type info
const abi = [{ type: "function", name: "transfer", ... }];

// With as const: TypeScript infers exact literal types → full autocomplete
const abi = [{ type: "function", name: "transfer", ... }] as const;
```

Viem and Wagmi both require `as const` for type inference to work.

**5. ABI vs interface**

An ABI is machine-readable encoding format. A Solidity `interface` is source code. You can generate an ABI from an interface with `forge build`, but they are different things. ABIs do not include implementation details.
