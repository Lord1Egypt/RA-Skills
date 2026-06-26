# AIOZ Pin MCP Server - API Reference

This document reflects the current behavior of scripts in the scripts directory.

---

## Base URL

```text
https://api.aiozpin.network/api/
```

---

## Authentication

### JWT Token (API key management)

Used by:

- generate_api_key.sh
- get_list_api_keys.sh
- delete_api_key.sh

Header:

```text
Authorization: Bearer {jwtToken}
Content-Type: application/json
```

### Pinning Keys (pinning and billing)

Used by pinning and billing scripts.

Headers:

```text
pinning_api_key: {pinningApiKey}
pinning_secret_key: {pinningSecretKey}
```

---

## API Key Management

### 1. Generate API Key

Script:

```bash
./scripts/generate_api_key.sh JWT_TOKEN KEY_NAME [admin] [pinList] [nftList] [unpin] [pinByHash] [pinFileToIPFS] [unpinNFT] [pinNFTToIPFS]
```

Endpoint:

```text
POST /api/apiKeys/
```

Body:

```json
{
  "name": "test-api-key",
  "scopes": {
    "admin": true,
    "data": {
      "pin_list": true,
      "nft_list": true
    },
    "pinning": {
      "unpin": true,
      "pin_by_hash": true,
      "pin_file_to_ipfs": true
    },
    "pin_nft": {
      "unpin_nft": true,
      "pin_nft_to_ipfs": true
    }
  }
}
```

cURL example:

```bash
curl --location --request POST 'https://api.aiozpin.network/api/apiKeys/' \
  --header 'Authorization: Bearer JWT' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "name": "test-api-key",
    "scopes": {
      "admin": true,
      "data": {
        "pin_list": true,
        "nft_list": true
      },
      "pinning": {
        "unpin": true,
        "pin_by_hash": true,
        "pin_file_to_ipfs": true
      },
      "pin_nft": {
        "unpin_nft": true,
        "pin_nft_to_ipfs": true
      }
    }
  }'
```

### 2. Get List API Keys

Script:

```bash
./scripts/get_list_api_keys.sh JWT_TOKEN
```

Endpoint:

```text
GET /api/apiKeys/list
```

cURL example:

```bash
curl --request GET 'https://api.aiozpin.network/api/apiKeys/list' \
  --header 'Authorization: Bearer JWT' \
  --header 'Content-Type: application/json'
```

### 3. Delete API Key

Script:

```bash
./scripts/delete_api_key.sh JWT_TOKEN KEY_ID
```

Endpoint:

```text
DELETE /api/apikeys/{keyId}
```

cURL example:

```bash
curl --request DELETE 'https://api.aiozpin.network/api/apikeys/KEY_ID' \
  --header 'Authorization: Bearer JWT' \
  --header 'Content-Type: application/json'
```

---

## Pinning Operations

### 4. Pin Local File

Script:

```bash
./scripts/pin_files_or_directory.sh FILE_PATH PINNING_API_KEY PINNING_SECRET_KEY
```

Endpoint:

```text
POST /api/pinning/
```

Request type: multipart form data.

cURL example:

```bash
curl --location --request POST 'https://api.aiozpin.network/api/pinning/' \
  --header 'pinning_api_key: KEY' \
  --header 'pinning_secret_key: SECRET' \
  --form 'file=@"/test.png"'
```

### 5. Pin by CID Hash

Script:

```bash
./scripts/pin_by_cid.sh CID_HASH PINNING_API_KEY PINNING_SECRET_KEY [METADATA_NAME]
```

Endpoint:

```text
POST /api/pinning/pinByHash
```

Body:

```json
{
  "hash_to_pin": "Qm...",
  "metadata": {
    "name": "name-ipfs-hash"
  }
}
```

cURL example:

```bash
curl --location --request POST 'https://api.aiozpin.network/api/pinning/pinByHash' \
  --header 'pinning_api_key: KEY' \
  --header 'pinning_secret_key: SECRET' \
  --header 'Content-Type: application/json' \
  --data-raw '{
    "hash_to_pin": "Qmc1135ziMvmFG534i75E8HpJoLqzLzgKBxfjBV9cBsMAs",
    "metadata": {
      "name": "name-ipfs-hash"
    }
  }'
```

### 6. Get Pin Details

Script:

```bash
./scripts/get_pin_details.sh PIN_ID PINNING_API_KEY PINNING_SECRET_KEY
```

Endpoint:

```text
GET /api/pinning/{pinId}
```

cURL example:

```bash
curl --location --request GET 'https://api.aiozpin.network/api/pinning/PIN_ID' \
  --header 'pinning_api_key: KEY' \
  --header 'pinning_secret_key: SECRET'
```

### 7. List Pins

Script:

```bash
./scripts/list_pins.sh PINNING_API_KEY PINNING_SECRET_KEY [OFFSET] [LIMIT] [PINNED] [SORT_BY] [SORT_ORDER]
```

Endpoint:

```text
GET /api/pinning/pins/?offset=0&limit=10&pinned=true&sortBy=name&sortOrder=ASC
```

cURL example:

```bash
curl --location --request GET 'https://api.aiozpin.network/api/pinning/pins/?offset=0&limit=10&pinned=true&sortBy=name&sortOrder=ASC' \
  --header 'pinning_api_key: KEY' \
  --header 'pinning_secret_key: SECRET'
```

### 8. Unpin File

Script:

```bash
./scripts/unpin_file.sh PIN_ID PINNING_API_KEY PINNING_SECRET_KEY
```

Endpoint:

```text
DELETE /api/pinning/unpin/{pinId}
```

cURL example:

```bash
curl --location --request DELETE 'https://api.aiozpin.network/api/pinning/unpin/PIN_ID' \
  --header 'pinning_api_key: KEY' \
  --header 'pinning_secret_key: SECRET'
```

---

## Billing and Usage

All three scripts support:

- OFFSET default 0
- LIMIT default 10

### 9. History Usage

Script:

```bash
./scripts/get_history_usage_data.sh PINNING_API_KEY PINNING_SECRET_KEY [OFFSET] [LIMIT]
```

Endpoint:

```text
GET /api/billing/historyUsage/?offset=0&limit=10
```

### 10. Top-up Data

Script:

```bash
./scripts/get_top_up.sh PINNING_API_KEY PINNING_SECRET_KEY [OFFSET] [LIMIT]
```

Endpoint:

```text
GET /api/billing/topUp/?offset=0&limit=10
```

### 11. This Month Usage

Script:

```bash
./scripts/get_month_usage_data.sh PINNING_API_KEY PINNING_SECRET_KEY [OFFSET] [LIMIT]
```

Endpoint:

```text
GET /api/billing/thisMonthUsage/?offset=0&limit=10
```

---

## Script Behavior Notes

- Most scripts print `Request URL` before making the HTTP call.
- Billing scripts use `--location` and endpoint trailing slash to avoid redirect HTML responses.
- Responses are pretty-printed by `jq` when possible.
