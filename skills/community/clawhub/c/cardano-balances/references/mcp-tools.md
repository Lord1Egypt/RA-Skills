# Balances MCP Tools Reference

## get_balances

Retrieve all balances and native assets for the connected wallet.

**Input:** None

**Output:**

| Field | Type | Description |
|-------|------|-------------|
| `balances[].name` | `string` | Human-readable name (e.g. "ADA") |
| `balances[].policyId` | `string` | Policy ID (empty for ADA) |
| `balances[].nameHex` | `string` | Asset name in hex (empty for ADA) |
| `balances[].amount` | `number` | Amount in lovelace (no decimals) |

---

## get_addresses

Retrieve all Cardano addresses for the connected wallet.

**Input:** None

**Output:**

| Field | Type | Description |
|-------|------|-------------|
| `addresses` | `string[]` | List of Cardano bech32 addresses |

---

## get_utxos

Retrieve all UTxOs for the connected wallet.

**Input:** None

**Output:**

| Field | Type | Description |
|-------|------|-------------|
| `utxos` | `string[]` | List of UTxOs in CBOR hex format |
