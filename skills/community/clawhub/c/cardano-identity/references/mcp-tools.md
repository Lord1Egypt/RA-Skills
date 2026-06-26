# Identity MCP Tools Reference

## get_adahandles

Retrieve all ADAHandles (https://handle.me/) for the connected wallet.

**Input:** None

**Output:**

| Field | Type | Description |
|-------|------|-------------|
| `adaHandles` | `string[]` | List of ADAHandle names owned by the wallet |

ADAHandles are Cardano native tokens under policy ID `f0ff48bbb7bbe9d59a40f1ce90e9e9d0ff5002ec48f232b49ca0fb9a`. The tool decodes hex asset names to human-readable strings.
