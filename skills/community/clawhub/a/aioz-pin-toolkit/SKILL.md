---
name: aioz-pin-toolkit
description: Respond to user requests for AIOZ Pin API. Use provided scripts to manage API keys, pin files to IPFS, track usage, and more.
metadata:
  openclaw:
    emoji: "📌"
    requires:
      envVars:
        - name: PINNING_API_KEY
          description: AIOZ Pin API key for pinning and billing operations
          required: true
          primaryCredential: true
        - name: PINNING_SECRET_KEY
          description: AIOZ Pin secret key for pinning and billing operations
          required: true
        - name: AIOZ_JWT_TOKEN
          description: JWT token for API key management operations (generate, list, delete)
          required: false
      bins:
        - curl
        - jq
---

# AIOZ Pin Operations

Interact with AIOZ Pin API quickly with API key authentication. A suite of integrated bash scripts is provided to automatically call REST APIs for pinning files, managing API keys, and tracking usage.

## When to use this skill

- User wants to pin files to IPFS or pin by CID hash
- User mentions "pin file", "pin to IPFS", "unpin", or "IPFS pinning"
- User wants to generate, list, or delete AIOZ Pin API keys
- User wants to retrieve pin details or list all pinned content
- User wants to check usage data, top-ups, or billing information
- User wants to manage AIOZ Pin resources

## Authentication

This skill uses API key authentication via environment variables:

- `PINNING_API_KEY`: Your AIOZ Pin API key (provided by the platform)
- `PINNING_SECRET_KEY`: Your AIOZ Pin secret key (provided by the platform)
- `AIOZ_JWT_TOKEN`: Your AIOZ Pin JWT token (for API key management operations)

Credential-safe policy:

- Prefer credentials from secure environment injection.
- If missing, ask the user for credentials and set them as temporary environment variables.
- Never hardcode keys in command examples, logs, or responses.
- Avoid inline one-off commands that contain raw secrets.

**⚠️ Critical Security Notice:**

- **Never pass credentials as CLI arguments.** Credentials passed as positional arguments become visible in `ps` listings, shell history (`.bash_history`, `.zsh_history`), and process environment dumps.
- **All scripts must read credentials from environment variables only.** Do not manually pass `PINNING_API_KEY`, `PINNING_SECRET_KEY`, or `AIOZ_JWT_TOKEN` as script arguments.
- If a script prompts for credentials or accepts them as arguments, that is a violation of this policy.

If credentials are not present in the shell session, set them once before running any scripts:

```bash
export PINNING_API_KEY="YOUR_PINNING_API_KEY"
export PINNING_SECRET_KEY="YOUR_PINNING_SECRET_KEY"
export AIOZ_JWT_TOKEN="YOUR_JWT_TOKEN"  # if needed for API key management
```

Header mapping used by scripts (credentials read from env vars internally):

- `PINNING_API_KEY` → `pinning-api-key` header
- `PINNING_SECRET_KEY` → `pinning-secret-key` header
- `AIOZ_JWT_TOKEN` → `Authorization: Bearer` header

This keeps credentials out of repeated command history and avoids accidental exposure.

## Usage Options (Available Scripts)

When the user asks for a feature, use one of the bash scripts located in the `scripts/` directory.

**Prerequisite:** All scripts read credentials from environment variables. Ensure these are set before executing any script:

```bash
export PINNING_API_KEY="YOUR_KEY"
export PINNING_SECRET_KEY="YOUR_SECRET"
export AIOZ_JWT_TOKEN="YOUR_JWT"  # for API key management only
```

### Script Routing Map (for Clawbot)

All scripts below assume credentials are available in the environment (set via `export`). **Do not pass credentials as CLI arguments.**

#### Pinning Operations

- Pin file by URL: `./scripts/pin_files_or_directory.sh FILE_URL`
- Pin by CID hash: `./scripts/pin_by_cid.sh CID_HASH [METADATA_NAME]`
- Get pin details: `./scripts/get_pin_details.sh PIN_ID`
- List pins: `./scripts/list_pins.sh [OFFSET] [LIMIT] [PINNED] [SORT_BY] [SORT_ORDER]`
- Unpin file: `./scripts/unpin_file.sh PIN_ID`

#### API Key Management (JWT)

- Generate new API key: `./scripts/generate_api_key.sh KEY_NAME [admin] [pinList] [nftList] [unpin] [pinByHash] [pinFileToIPFS] [unpinNFT] [pinNFTToIPFS]`
- List all API keys: `./scripts/get_list_api_keys.sh`
- Delete API key: `./scripts/delete_api_key.sh KEY_ID`

#### Usage & Billing

- Get history usage data: `./scripts/get_history_usage_data.sh [OFFSET] [LIMIT]`
- Get top-up data: `./scripts/get_top_up.sh [OFFSET] [LIMIT]`
- Get monthly usage data: `./scripts/get_month_usage_data.sh [OFFSET] [LIMIT]`

### 1. Pin Files to IPFS

Use this script to pin a file by URL to IPFS:

```bash
./scripts/pin_files_or_directory.sh "https://example.com/file.zip"
```

Actual behavior in script:

- Accepts public downloadable URL.
- Downloads file and pins to IPFS via AIOZ Pin service.
- Returns pin ID and CID hash.

### 2. Pin by CID Hash

To pin existing content by its IPFS CID:

```bash
./scripts/pin_by_cid.sh "QmHash..." "optional-name"
```

- `CID_HASH`: The IPFS content hash to pin
- `METADATA_NAME`: Optional name for the pinned content

### 3. API Key Management (JWT Flow)

Use these scripts to manage AIOZ Pin API keys:

```bash
# Generate API key with permissions:
./scripts/generate_api_key.sh "my-key" false true false false true true false false

# List API keys:
./scripts/get_list_api_keys.sh

# Delete API key:
./scripts/delete_api_key.sh "KEY_ID"
```

Actual behavior in scripts:

- `generate_api_key.sh` calls `POST /api/apikeys/create` with permission flags.
- Default permission values are `false` if not provided.
- `get_list_api_keys.sh` calls `GET /api/apikeys` and returns list of keys.
- `delete_api_key.sh` calls `DELETE /api/apikeys/{keyId}` and removes the key.

### 4. Pin Details & Management

To inspect, list, and manage pins:

- **Get Pin Details:** `./scripts/get_pin_details.sh PIN_ID`
  - Calls `GET /api/pinning/{pinId}`
  - Returns pin status, CID, size, creation date
- **List Pins:** `./scripts/list_pins.sh [OFFSET] [LIMIT] [PINNED] [SORT_BY] [SORT_ORDER]`
  - Calls `GET /api/pinning/pins?offset=...&limit=...`
  - Defaults: `OFFSET=0`, `LIMIT=10`, `PINNED=true`, `SORT_BY=name`, `SORT_ORDER=ASC`
- **Unpin File:** `./scripts/unpin_file.sh PIN_ID`
  - Calls `DELETE /api/pinning/unpin/{pinId}`
  - Removes pin from AIOZ Pin service

### 5. Usage & Billing Data

To retrieve usage and top-up data:

- **History Usage:** `./scripts/get_history_usage_data.sh [OFFSET] [LIMIT]`
  - Calls `GET /api/usage/history?offset=...&limit=...`
  - Returns detailed usage history with timestamps
- **Top-up Data:** `./scripts/get_top_up.sh [OFFSET] [LIMIT]`
  - Calls `GET /api/usage/topup?offset=...&limit=...`
  - Returns top-up transaction history
- **Monthly Usage:** `./scripts/get_month_usage_data.sh [OFFSET] [LIMIT]`
  - Calls `GET /api/usage/month?offset=...&limit=...`
  - Returns this month's usage statistics

Pagination notes:

- `OFFSET` default is `0`
- `LIMIT` default is `10`

## Full Pinning Flow (Common Operational Path)

For a typical pin lifecycle, use this sequence:

**Setup:** Ensure credentials are in the environment before executing any scripts:

```bash
export PINNING_API_KEY="YOUR_KEY"
export PINNING_SECRET_KEY="YOUR_SECRET"
```

Operational steps:

1. Pin a file or CID
2. Get pin details to verify status
3. List pins to check all pinned content
4. Unpin when no longer needed

### Step 1: Pin File by URL

```bash
./scripts/pin_files_or_directory.sh "https://example.com/file.zip"
```

Response: extract `pinId` and `cid` from the response.

### Step 2: Check Pin Details

After pinning, verify the pin status:

```bash
./scripts/get_pin_details.sh "PIN_ID"
```

Response includes: status (active/pending), CID, file size, created date.

### Step 3: List All Pins

To see all pinned content:

```bash
./scripts/list_pins.sh 0 10 true name ASC
```

Response: paginated list of all pins with metadata.

### Step 4: Unpin Content

When done, remove the pin:

```bash
./scripts/unpin_file.sh "PIN_ID"
```

Confirms deletion.

## Manual cURL Reference

_(For reference only; prefer using provided scripts)_

**Prerequisites:** These examples assume environment variables are set:

```bash
export PINNING_API_KEY="YOUR_KEY"
export PINNING_SECRET_KEY="YOUR_SECRET"
export AIOZ_JWT_TOKEN="YOUR_JWT"
```

All credentials are referenced as `$VARIABLE_NAME` (shell expansion) — never hardcoded.

### Pin File by URL

```bash
curl -s -X POST "https://api.aiozpin.network/api/files/pin?fileUrl=https://example.com/file.zip" \
  -H "pinning-api-key: $PINNING_API_KEY" \
  -H "pinning-secret-key: $PINNING_SECRET_KEY" \
  -H "Content-Type: application/json"
```

### Generate API Key (JWT)

```bash
curl -s -X POST "https://api.aiozpin.network/api/apikeys/create?keyName=my-key&admin=false&pinList=true&nftList=false&unpin=false&pinByHash=true&pinFileToIPFS=true&unpinNFT=false&pinNFTToIPFS=false" \
  -H "Authorization: Bearer $AIOZ_JWT_TOKEN" \
  -H "Content-Type: application/json"
```

### List Pins

```bash
curl -s "https://api.aiozpin.network/api/pinning/pins?offset=0&limit=10&pinned=true&sortBy=name&sortOrder=ASC" \
  -H "pinning-api-key: $PINNING_API_KEY" \
  -H "pinning-secret-key: $PINNING_SECRET_KEY"
```

## Response Handling

1. Run the appropriate script from the `scripts/` directory.
2. **Pin/Search scripts** return raw JSON: `pin_files_or_directory`, `pin_by_cid`, `get_pin_details`, `list_pins`
3. **API Key scripts** return structured output with key metadata and permissions
4. **Usage/Billing scripts** return paginated data with timestamps and amounts
5. Extract and return useful fields explicitly: pin IDs, CID hashes, status, URLs, balances. If pin status is `pending`, inform the user to check again later.

## Error Handling

- **401 Unauthorized**: Invalid API keys. Verify that `PINNING_API_KEY` and `PINNING_SECRET_KEY` are correctly set in the environment (e.g., `echo $PINNING_API_KEY`).
- **Missing Parameters**: Scripts validate arguments; pass exactly what they require.
- **Credential exposure warnings**: If you accidentally pass credentials as CLI arguments, immediately revoke those keys from your AIOZ Pin account and generate new ones. Credentials in commands are visible via `ps`, shell history files, and process environment listings.
- **404**: Resource not found (invalid pin ID or key ID).
- **500**: Server error; suggest retrying.
- **Connection timeout/refused**: API endpoint may be unavailable; retry and verify `https://api.aiozpin.network/api/` accessibility.

## Example Interaction Flow

1. User: "Pin this file to IPFS"
2. **Verify environment setup:** Confirm that `PINNING_API_KEY` and `PINNING_SECRET_KEY` are already set in the shell environment. If missing, ask the user for their credentials and set them via:
   ```bash
   export PINNING_API_KEY="..."
   export PINNING_SECRET_KEY="..."
   ```
   _Do not_ pass these as script arguments.
3. Ask for the file URL
4. Execute: `./scripts/pin_files_or_directory.sh "FILE_URL"` (credentials come from environment)
5. Extract the returned pin ID and CID
6. Return the pin information to the user
7. Offer optional follow-up: check details (`get_pin_details.sh`) or list pins (`list_pins.sh`)
