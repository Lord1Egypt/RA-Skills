---
name: encrytion-decryption-toolkit
description: "Encrytion Decryption Toolkit: Cryptographic toolkit: generate secure randoms, compute hashes (MD5, SHA, SHA3). Use when an agent needs encrytion decryption toolkit, generating secure api keys or access tokens for authentication systems, creating unique uuids for database record identifiers, computing file checksums to verify data integrity during transfers, validating webhook payloads by computing and comparing hmac signatures, decrypt, value, key through AgentPMT-hosted remote tool calls."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/encrytion-decryption-toolkit
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/encrytion-decryption-toolkit"}}
---
# Encrytion Decryption Toolkit

## Freshness
Last updated: `2026-06-23`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
This function supports six core actions: generate for creating secure random values in ASCII, BASE64, HEX, or UUID formats with configurable lengths from 4 to 256 characters; hash for computing cryptographic digests using MD5, SHA256, SHA384, SHA512, and SHA3 family algorithms; hmac for generating keyed-hash message authentication codes with a secret key; sign for creating digital signatures using RSA (RS256, RS512) or ECDSA (ES256, ES384, ES512) algorithms with PEM-encoded private keys; and encrypt/decrypt for AES-256-GCM authenticated encryption with support for initialization vectors and optional additional authenticated data. Users can provide input as plain text or base64-encoded binary data, and all cryptographic outputs can be encoded in either hexadecimal or base64 format for flexibility across different system integrations. The toolkit handles the underlying cryptographic complexity while exposing a straightforward interface, making it ideal for agent workflows that require secure token generation, data integrity verification, or sensitive information protection.

## Product Instructions
### Encryption Decryption Toolkit

Cryptographic utility for generating random values, hashing data, computing HMACs, creating digital signatures, and performing AES-256-GCM encryption/decryption.

---

#### Actions

##### generate

Generate a cryptographically secure random value.

**Required fields:**
- `generation_type` (string) — Type of value to generate: `ASCII`, `BASE64`, `HEX`, or `UUID`
- `property_name` (string) — Name for the output property containing the generated value

**Optional fields:**
- `length` (integer, 4-256, default 32) — Length of the generated value (ignored for UUID)

**Example — Generate a hex API key:**
```json
{
  "action": "generate",
  "property_name": "api_key",
  "generation_type": "HEX",
  "length": 64
}
```

**Example — Generate a UUID:**
```json
{
  "action": "generate",
  "property_name": "session_id",
  "generation_type": "UUID"
}
```

**Example — Generate a base64 token:**
```json
{
  "action": "generate",
  "property_name": "refresh_token",
  "generation_type": "BASE64",
  "length": 48
}
```

---

##### hash

Compute a cryptographic hash of text or binary data.

**Required fields:**
- `hash_algorithm` (string) — Hash algorithm: `MD5`, `SHA256`, `SHA384`, `SHA512`, `SHA3-256`, `SHA3-384`, or `SHA3-512`
- `value` (string) — Text to hash (required unless `binary_file` is true)

**Optional fields:**
- `property_name` (string) — Output property name (defaults to `hash_result`)
- `encoding` (string) — Output encoding: `hex` (default) or `base64`
- `binary_file` (boolean, default false) — Set to true to hash binary data instead of text
- `binary_value_base64` (string) — Base64-encoded binary data (required when `binary_file` is true)
- `binary_property_name` (string) — Metadata label for the binary input

**Example — SHA-256 hash of text:**
```json
{
  "action": "hash",
  "hash_algorithm": "SHA256",
  "value": "hello world"
}
```

**Example — Hash binary data with base64 output:**
```json
{
  "action": "hash",
  "hash_algorithm": "SHA512",
  "binary_file": true,
  "binary_value_base64": "SGVsbG8gV29ybGQ=",
  "encoding": "base64"
}
```

**Example — MD5 hash with custom property name:**
```json
{
  "action": "hash",
  "hash_algorithm": "MD5",
  "value": "check this content",
  "property_name": "content_checksum"
}
```

---

##### hmac

Compute a keyed-hash message authentication code.

**Required fields:**
- `hash_algorithm` (string) — Hash algorithm: `MD5`, `SHA256`, `SHA384`, `SHA512`, `SHA3-256`, `SHA3-384`, or `SHA3-512`
- `secret` (string) — The secret key for HMAC computation
- `value` (string) — Text to authenticate (required unless `binary_file` is true)

**Optional fields:**
- `property_name` (string) — Output property name (defaults to `hmac_result`)
- `encoding` (string) — Output encoding: `hex` (default) or `base64`
- `binary_file` (boolean, default false) — Set to true to use binary data as input
- `binary_value_base64` (string) — Base64-encoded binary data (required when `binary_file` is true)

**Example — HMAC-SHA256:**
```json
{
  "action": "hmac",
  "hash_algorithm": "SHA256",
  "value": "message to authenticate",
  "secret": "my-secret-key"
}
```

**Example — HMAC-SHA512 with base64 output:**
```json
{
  "action": "hmac",
  "hash_algorithm": "SHA512",
  "value": "webhook payload content",
  "secret": "webhook-signing-secret",
  "encoding": "base64"
}
```

---

##### sign

Create a digital signature using a private key.

**Required fields:**
- `value` (string) — The text to sign
- `algorithm` (string) — Signing algorithm: `RS256`, `RS512` (RSA), or `ES256`, `ES384`, `ES512` (ECDSA)
- `private_key` (string) — PEM-encoded private key

**Optional fields:**
- `property_name` (string) — Output property name (defaults to `signature`)
- `encoding` (string) — Output encoding: `hex` (default) or `base64`

**Example — RSA SHA-256 signature:**
```json
{
  "action": "sign",
  "value": "data to sign",
  "algorithm": "RS256",
  "private_key": "-----BEGIN RSA PRIVATE KEY-----\n...\n-----END RSA PRIVATE KEY-----",
  "encoding": "base64"
}
```

**Example — ECDSA signature:**
```json
{
  "action": "sign",
  "value": "data to sign",
  "algorithm": "ES256",
  "private_key": "-----BEGIN EC PRIVATE KEY-----\n...\n-----END EC PRIVATE KEY-----"
}
```

---

##### encrypt

Encrypt plaintext using AES-256-GCM authenticated encryption.

**Required fields:**
- `value` (string) — Plaintext to encrypt
- `key` (string) — 32-byte AES key, encoded as hex or base64
- `iv` (string) — 12-byte nonce/initialization vector, encoded as hex or base64

**Optional fields:**
- `encoding` (string) — Encoding for key, iv, and output: `hex` (default) or `base64`
- `aad` (string) — Additional authenticated data (verified during decryption but not encrypted)

**Example — Encrypt with hex-encoded key and IV:**
```json
{
  "action": "encrypt",
  "value": "secret message",
  "key": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
  "iv": "0123456789abcdef01234567"
}
```

**Example — Encrypt with AAD:**
```json
{
  "action": "encrypt",
  "value": "confidential data",
  "key": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
  "iv": "0123456789abcdef01234567",
  "aad": "user-id:12345"
}
```

---

##### decrypt

Decrypt AES-256-GCM ciphertext back to plaintext.

**Required fields:**
- `value` (string) — Ciphertext to decrypt (hex or base64 encoded)
- `key` (string) — 32-byte AES key (same encoding used during encryption)
- `iv` (string) — 12-byte nonce (same value used during encryption)

**Optional fields:**
- `encoding` (string) — Encoding for key, iv, and ciphertext: `hex` (default) or `base64`
- `aad` (string) — Additional authenticated data (must match what was used during encryption)

**Example — Decrypt hex-encoded ciphertext:**
```json
{
  "action": "decrypt",
  "value": "a1b2c3d4e5f6...",
  "key": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
  "iv": "0123456789abcdef01234567"
}
```

---

#### Common Workflows

##### Generate a key, encrypt, then decrypt
1. Use `generate` with `generation_type: "HEX"` and `length: 64` to create a 32-byte key
2. Use `generate` with `generation_type: "HEX"` and `length: 24` to create a 12-byte IV
3. Use `encrypt` with the generated key, IV, and your plaintext
4. Use `decrypt` with the same key, IV, and the returned ciphertext

##### Verify data integrity with HMAC
1. Sender computes `hmac` on the message with a shared secret
2. Receiver computes `hmac` on the received message with the same secret
3. Compare the two HMAC values — if they match, the message is authentic and unaltered

##### Hash a file for checksums
1. Base64-encode the file contents
2. Use `hash` with `binary_file: true` and `binary_value_base64` set to the encoded content

---

#### Important Notes

- **Encoding consistency**: The `encoding` parameter applies to both input decoding (key, iv, ciphertext) and output encoding. Use the same encoding for encrypt and decrypt operations.
- **Key sizes**: AES-256-GCM requires exactly a 32-byte key (64 hex characters or 44 base64 characters).
- **IV/nonce**: Must be 12 bytes (24 hex characters). Never reuse an IV with the same key.
- **Hash algorithms**: SHA384 is supported directly (legacy SHA385 alias also accepted internally).
- **UUID generation**: The `length` parameter is ignored when generation_type is UUID; standard UUIDs are always returned.
- **property_name**: Controls the key name in the response JSON where the result appears. Useful for chaining outputs in workflows.

## When To Use
- Use this skill for `Encrytion Decryption Toolkit` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: encrytion decryption toolkit, generating secure api keys or access tokens for authentication systems, creating unique uuids for database record identifiers, computing file checksums to verify data integrity during transfers, validating webhook payloads by computing and comparing hmac signatures, decrypt, value, key.
- Supported action names: `decrypt`, `encrypt`, `generate`, `hash`, `hmac`, `sign`.

## Use Cases
- Generating secure API keys or access tokens for authentication systems
- creating unique UUIDs for database record identifiers
- computing file checksums to verify data integrity during transfers
- validating webhook payloads by computing and comparing HMAC signatures
- signing JWT tokens for stateless authentication in API workflows
- encrypting sensitive configuration values or credentials before storage
- decrypting stored secrets at runtime for secure credential injection
- generating session tokens or one-time codes for user verification flows
- creating content hashes for deduplication or caching key generation
- signing API requests to third-party services that require cryptographic authentication

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `6`.
x402 availability: not enabled for this product.

- `decrypt` (action slug: `decrypt`): Decrypt AES-256-GCM ciphertext back to plaintext. Price: `5` credits. Parameters: `aad`, `encoding`, `iv`, `key`, `value`.
- `encrypt` (action slug: `encrypt`): Encrypt plaintext using AES-256-GCM authenticated encryption. Price: `5` credits. Parameters: `aad`, `encoding`, `iv`, `key`, `value`.
- `generate` (action slug: `generate`): Generate a cryptographically secure random value in ASCII, BASE64, HEX, or UUID format. Price: `5` credits. Parameters: `generation_type`, `length`, `property_name`.
- `hash` (action slug: `hash`): Compute a cryptographic hash of text or binary data using MD5, SHA, or SHA3 algorithms. Price: `5` credits. Parameters: `binary_file`, `binary_property_name`, `binary_value_base64`, `encoding`, `hash_algorithm`, `property_name`, `value`.
- `hmac` (action slug: `hmac`): Compute a keyed-hash message authentication code (HMAC) using a secret key. Price: `5` credits. Parameters: `binary_file`, `binary_value_base64`, `encoding`, `hash_algorithm`, `property_name`, `secret`, `value`.
- `sign` (action slug: `sign`): Create a digital signature using RSA or ECDSA with a PEM-encoded private key. Price: `5` credits. Parameters: `algorithm`, `encoding`, `private_key`, `property_name`, `value`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "encrytion-decryption-toolkit"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "encrytion-decryption-toolkit"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "encrytion-decryption-toolkit"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "encrytion-decryption-toolkit"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "encrytion-decryption-toolkit"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "encrytion-decryption-toolkit"
  }
}
```

## Call This Tool
Product slug: `encrytion-decryption-toolkit`

Marketplace page: https://www.agentpmt.com/marketplace/encrytion-decryption-toolkit

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Encrytion-Decryption-Toolkit",
    "arguments": {
      "aad": "example aad",
      "action": "decrypt",
      "encoding": "hex",
      "iv": "example iv",
      "key": "example key",
      "value": "example value"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "encrytion-decryption-toolkit",
  "parameters": {
    "aad": "example aad",
    "action": "decrypt",
    "encoding": "hex",
    "iv": "example iv",
    "key": "example key",
    "value": "example value"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `decrypt` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/encrytion-decryption-toolkit
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
