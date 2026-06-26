---
name: erc20-skill
version: "1.0.0"
description: Interact with Erc20 smart contract via read/write functions
---

## Workflow

1. **Setup**: Configure environment variables `RPC_URL`, `PRIVATE_KEY`, `CONTRACT_ADDRESS`
2. **Read**: Use read functions (view/pure) to query contract state
3. **Write**: Use write functions to modify contract state (requires gas)

## Constraints

| Constraint | Requirement |
|------------|-------------|
| RPC Provider | Any Ethereum JSON-RPC endpoint |
| Private Key | Must have contract permissions |
| Gas Limit | Adjust based on function complexity |
| Network | Must match contract deployment |

## Read Functions

### name

`name()`

**Returns:** string

**Example:**
```typescript
const result = await name({  });
```

### symbol

`symbol()`

**Returns:** string

**Example:**
```typescript
const result = await symbol({  });
```

### decimals

`decimals()`

**Returns:** uint8

**Example:**
```typescript
const result = await decimals({  });
```

### totalSupply

`totalSupply()`

**Returns:** uint256

**Example:**
```typescript
const result = await totalSupply({  });
```

### balanceOf

`balanceOf(address account)`

**Returns:** uint256

**Parameters:**

| `account` | address |

**Example:**
```typescript
const result = await balanceOf({ account: "0x... });
```

### allowance

`allowance(address owner, address spender)`

**Returns:** uint256

**Parameters:**

| `owner` | address |
| `spender` | address |

**Example:**
```typescript
const result = await allowance({ owner: "0x..., spender: "0x... });
```

## Write Functions

### transfer

`transfer(address to, uint256 amount)`

**Mutability:** nonpayable

**Parameters:**

| `to` | address |
| `amount` | uint256 |

**Example:**
```typescript
const tx = await transfer({ to: value, amount: value });
```

### approve

`approve(address spender, uint256 amount)`

**Mutability:** nonpayable

**Parameters:**

| `spender` | address |
| `amount` | uint256 |

**Example:**
```typescript
const tx = await approve({ spender: value, amount: value });
```

### transferFrom

`transferFrom(address from, address to, uint256 amount)`

**Mutability:** nonpayable

**Parameters:**

| `from` | address |
| `to` | address |
| `amount` | uint256 |

**Example:**
```typescript
const tx = await transferFrom({ from: value, to: value, amount: value });
```

### mint

`mint(address to, uint256 amount)`

**Mutability:** nonpayable

**Parameters:**

| `to` | address |
| `amount` | uint256 |

**Example:**
```typescript
const tx = await mint({ to: value, amount: value });
```

### burn

`burn(uint256 amount)`

**Mutability:** nonpayable

**Parameters:**

| `amount` | uint256 |

**Example:**
```typescript
const tx = await burn({ amount: value });
```

## Events

### Transfer

**Signature:** `Transfer([indexed] `address from`, [indexed] `address to`, `uint256 value`)`

### Approval

**Signature:** `Approval([indexed] `address owner`, [indexed] `address spender`, `uint256 value`)`

### Built with ❤️ by JustinXai ABI-to-MCP. Get the generator: https://github.com/JustinXai/abi-to-mcp
