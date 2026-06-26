---
name: cmcc-credential
description: Handle China Mobile Digital Credential authorization flow for sensitive operations. This skill operates in three distinct phases: (1) Credential Loading - Parse and store credentials (appId, appKey) from user-provided files into memory without making any API calls, (1.5) Agent Binding - Bind agent using appName and appId before authorization, and (2) Sensitive Operation Authorization - When user attempts sensitive actions (deleting data, accessing secrets, viewing keys), request authorization, provide authorization link, poll status (5s interval, 10min timeout), and verify authorization before proceeding. Signature uses sorted JSON with HmacSHA256; encryption uses AES/ECB/PKCS5Padding with MD5(appKey) as key.
metadata: {"clawdbot":{"emoji":"🔐"}}
---

# CMCC Digital Credential Authorization

This skill manages the China Mobile Digital Credential authorization flow in three phases:

## 📋 Overview

**Phase 1 - Credential Loading (Setup)**
- Parse credential file and store appId, appKey to memory
- No API calls or authorization requests during this phase
- One-time setup: Load credentials once, use for all future sensitive operations
- **Note**: appName and templateId are predefined constants (not loaded from file)

**Phase 1.5 - Agent Binding**
- Bind agent to credential system before authorization
- Call binding API with predefined appName and appId
- One-time binding: Required before any authorization requests

**Phase 2 - Authorization Flow (Runtime)**
- Triggered when user attempts a sensitive operation
- Request authorization with encrypted phone number
- Use predefined templateId for authorization
- Provide authorization link to user
- Poll authorization status until authorized or timeout
- Verify authorization before allowing operation

## Predefined Constants

- **appName**: `"Javis"` (default, can be overridden)
- **templateId**: `"qfx9pkizs42up7y61jsehs9v8e1xms4m"` (fixed, cannot be changed)

## Security Requirements

### Signature Generation (基于 Java SignUtil)

**Steps:**
1. **参数标准化**：Sort JSON object by dictionary order and serialize to string
2. **计算HMAC**：Calculate HmacSHA256 using appKey as secret
3. **十六进制转换**：Convert binary result to uppercase hexadecimal string

**Implementation:**
```python
# Sort JSON by dictionary order
body_json = json.dumps(body, sort_keys=True, separators=(',', ':'))

# Calculate HMAC-SHA256
signature = hmac.new(
    app_key.encode('utf-8'),
    body_json.encode('utf-8'),
    hashlib.sha256
).digest()

# Convert to uppercase hex
return signature.hex().upper()
```

### Encryption (基于 Java AESUtil.encodeAES)

**Steps:**
1. Use MD5 hash of appKey as 16-byte key
2. AES/ECB/PKCS5Padding encryption
3. Base64 encode result

**Implementation:**
```python
# Derive 16-byte key from appKey using MD5
key_bytes = hashlib.md5(app_key.encode('utf-8')).digest()

# AES/ECB/PKCS5Padding encryption
cipher = AES.new(key_bytes, AES.MODE_ECB)
encrypted = cipher.encrypt(pad(phone_bytes, AES.block_size))

# Base64 encode
return base64.b64encode(encrypted).decode('utf-8')
```

### Request Headers

**New Format:**
```
appId: <app_id>
signValue: <signature>
Content-Type: application/json
```

**Note:** Old headers (X-App-Id, X-Sign, X-Timestamp, X-Nonce) are no longer used.

---

## Phase 1: Credential Loading

### When to Activate Phase 1

Activate Phase 1 when:
- User provides a credential file (contains appId, appKey)
- User wants to set up the credential system for future use

### Loading Process

**DO NOT make any API calls during Phase 1.** Only parse and store credentials.

1. Read the credential file and extract:
   - `appId`: Application ID (24 characters)
   - `appKey`: Application secret key

2. Store credentials to `memory/cmcc-digital-credential.json`:
   ```json
   {
     "appId": "...",
     "appKey": "..."
   }
   ```

3. **Important**:
   - `appName` is predefined as `"Javis"` (not loaded from file)
   - `templateId` is predefined as `"qfx9pkizs42up7y61jsehs9v8e1xms4m"` (not loaded from file)
   - Only load appId and appKey from credential file

### Credential File Format

The credential file can be:

**Plain text format:**
```
智能体DID=AI20260314152030X7K9M2
智能体密钥=your-secret-key-here
```

**JSON format:**
```json
{
  "智能体DID": "AI20260314152030X7K9M2",
  "智能体密钥": "your-secret-key-here"
}
```

**Note**:
- `appName` is predefined as `"Javis"` (can be overridden via parameter)
- `templateId` is predefined as `"qfx9pkizs42up7y61jsehs9v8e1xms4m"` (fixed)
- Credential file uses field names: `智能体DID` (maps to appId) and `智能体密钥` (maps to appKey)

### Loading Credentials

Use the `load_credentials.py` script:

```bash
python3 scripts/load_credentials.py load <credential-file>
```

Or check if credentials exist:
```bash
python3 scripts/load_credentials.py check
```

---

## Phase 1.5: Agent Binding

### When to Activate Phase 1.5

Activate Phase 1.5 when:
- Credentials are loaded successfully from Phase 1
- Agent has not been bound yet (no binding record exists)
- Before requesting any authorization (Phase 2)

### Binding Process

1. **Load credentials from memory** (Phase 1):
   - appId: Application ID (24 characters)
   - appKey: Application secret key

2. **Call binding API**:
   - Use `scripts/bind_agent.py` to bind the agent
   - The API will use predefined appName (default: "Javis") and appId for binding
   - You can optionally override appName via `--appName` parameter
   - Check if response code is "000000" (success)

3. **Store binding status** (optional):
   - You can store a flag indicating binding is complete
   - This prevents unnecessary repeated binding calls

### Binding API

**Endpoint:**
```
POST /api/cmvc-tocp-server/agent/bind
```

**Request Headers:**
```
appId: <app_id>
signValue: <signature>
Content-Type: application/json
```

**Request Body:**
```json
{
  "appName": "Javis",
  "appId": "your-app-id"
}
```

**Response:**
```json
{
  "code": 0,
  "desc": "Success"
}
```

**Response Codes:**
- `0`: Success - Agent bound successfully
- Other codes: Failure - Check description for details

### Binding Agent

Use the `bind_agent.py` script:

```bash
python3 scripts/bind_agent.py \
  --appId "$APP_ID" \
  --appKey "$APP_KEY"
```

Or with custom appName (optional):

```bash
python3 scripts/bind_agent.py \
  --appName "MyCustomApp" \
  --appId "$APP_ID" \
  --appKey "$APP_KEY"
```

Or use credentials from memory:

```bash
APP_ID=$(python3 scripts/load_credentials.py get --field appId)
APP_KEY=$(python3 scripts/load_credentials.py get --field appKey)
python3 scripts/bind_agent.py --appId "$APP_ID" --appKey "$APP_KEY"
```

### Important Notes

- **appName is predefined**: Default is "Javis", not loaded from credential file
- **appName can be overridden**: Use `--appName` parameter if needed
- **Binding is one-time**: Only bind once; repeated binding calls are unnecessary
- **Binding before authorization**: Must complete binding before Phase 2 authorization flow
- **Simplified request**: The binding API only requires appName and appId
- **New signature format**: Uses sorted JSON with HmacSHA256

### Error Handling

- **Binding failed**: Check the error description and verify appId is correct
- **Network error**: Ensure you have network connectivity to binding API
- **Signature error**: Verify appKey is correct and JSON is properly sorted

---

## Phase 2: Sensitive Operation Authorization

### When to Activate Phase 2

Activate Phase 2 when:
- User attempts a sensitive operation
- Credentials are already loaded in memory from Phase 1
- Agent is already bound from Phase 1.5
- Authorization is required before proceeding

### What Are Sensitive Operations?

The following operations require authorization:
- Deleting files, records, or data
- Accessing or revealing secrets/API keys
- Viewing or copying sensitive information
- Any operation the user explicitly identifies as sensitive

**CRITICAL**: Never proceed with a sensitive operation without successful authorization.

### Authorization Flow

#### Step 1: Check Credentials

Before requesting authorization, verify credentials exist:
```bash
python3 scripts/load_credentials.py check
```

If credentials don't exist, inform user: "Credentials not found. Please provide a credential file first."

#### Step 2: Request Authorization

1. **Ask user for their phone number** (required parameter)
2. Use `scripts/request_authorization.py` to call the authorization API
3. The script will:
   - Encrypt phone number using AES/ECB/PKCS5Padding with MD5(appKey) as key
   - Generate 16-character random nonce
   - Generate timestamp in milliseconds
   - Sort JSON by dictionary order
   - Calculate HMAC-SHA256 signature
   - Call `/vc/auth/request` endpoint with new headers
   - Return `authRecordId` and `trustedAuthUrl`

#### Step 3: Provide Authorization Link

Present the authorization link to user:
```
Please authorize this operation at:
<trustedAuthUrl>

This link is valid for 3 days.

Waiting for authorization...
```

#### Step 4: Poll Authorization Status

1. Use `scripts/poll_authorization.py` to check status
2. Polling parameters:
   - Interval: 5 seconds
   - Timeout: 10 minutes (maximum 120 attempts)
3. The script will:
   - Call `/vc/auth/query` endpoint with `authRecordId`
   - Check `statusCode` in response
   - Return success when `statusCode === "000000"`
   - Timeout after 10 minutes if not authorized

#### Step 5: Verify and Proceed

**If authorization successful** (`statusCode === "000000"`):
- Extract `credentialSubject` if needed
- Allow the sensitive operation to proceed
- Inform user: "Authorization confirmed. Proceeding with operation..."

**If authorization fails or times out**:
- Deny the sensitive operation
- Inform user: "Authorization failed or timed out. Operation cancelled."

---

## API Details

### Base URL
```
https://vctest.cmccsign.com/
```

### Endpoints

#### 1. Authorization Request
- **URL**: `/cmvc-tocp-server/vc/auth/request`
- **Method**: POST
- **Headers**:
  - `appId`: app_id
  - `signValue`: HMAC-SHA256 signature (64 hex chars, uppercase)
  - `Content-Type`: `application/json`
- **Body**:
  ```json
  {
    "nonce": "...",
    "timestamp": 1710403200000,
    "phoneNo": "<AES-encrypted-phone>",
    "returnUrl": "",  // optional
    "notifyUrl": "",  // optional
    "templateId": "qfx9pkizs42up7y61jsehs9v8e1xms4m",
    "sendSmsFlag": "0",  // optional, default 0
    "smsIntranetTemplateId": "",  // optional
    "smsExternalTemplateId": "",  // optional
    "forwardedCredentials": {},  // optional
    "authScene": ""  // optional
  }
  ```
- **Response**:
  ```json
  {
    "code": 0,
    "desc": "Success",
    "authRecordId": "...",
    "trustedAuthUrl": "https://..."
  }
  ```

#### 2. Authorization Query
- **URL**: `/cmvc-tocp-server/vc/auth/query`
- **Method**: POST
- **Headers**:
  - `appId`: app_id
  - `signValue`: HMAC-SHA256 signature (64 hex chars, uppercase)
  - `Content-Type`: `application/json`
- **Body**:
  ```json
  {
    "authRecordId": "..."
  }
  ```
- **Response**:
  ```json
  {
    "code": 0,
    "desc": "Success",
    "statusCode": "000000",  // 000000 = authorized
    "statusDesc": "已授权",
    "credentialSubject": {}
  }
  ```

---

## Usage Examples

### Example 1: Phase 1 - Loading Credentials
```
User: Here's my credential file:
appId=AI20260314152030X7K9M2
appKey=my-secret-key

Assistant: Credentials loaded successfully.
         appId: AI20260314152030X7K9M2
         appKey: *** (hidden)
         appName: Javis (predefined)
         templateId: qfx9pkizs42up7y61jsehs9v8e1xms4m (predefined)
         Stored to: memory/cmcc-digital-credential.json
```

### Example 2: Phase 2 - Performing Sensitive Operation
```
User: Delete the sensitive-data.txt file

Assistant: To perform this operation, I need authorization.
         Please provide your phone number:

User: 13800138000

Assistant: [Checking if agent is bound...]
         [Binding agent using bind_agent.py with appName="Javis"...]
         Agent binding successful.

         [Calling request_authorization.py with templateId=qfx9pkizs42up7y61jsehs9v8e1xms4m...]
         Please authorize this operation at:
         https://vctest.cmccsign.com/auth/xxx

         This link is valid for 3 days.
         Waiting for authorization...

         [Starting poll_authorization.py with 5s interval...]

         [After 30 seconds]

         Authorization confirmed. Proceeding with operation...
         Deleting sensitive-data.txt...
```

---

## Script Usage

### Load Credentials (Phase 1)
```bash
python3 scripts/load_credentials.py load <credential-file>
```

### Bind Agent (Phase 1.5)
```bash
python3 scripts/bind_agent.py \
  --appId "$APP_ID" \
  --appKey "$APP_KEY"
```

Or with custom appName (optional):
```bash
python3 scripts/bind_agent.py \
  --appName "MyCustomApp" \
  --appId "$APP_ID" \
  --appKey "$APP_KEY"
```

Or load from memory:
```bash
APP_ID=$(python3 scripts/load_credentials.py get --field appId)
APP_KEY=$(python3 scripts/load_credentials.py get --field appKey)
python3 scripts/bind_agent.py --appId "$APP_ID" --appKey "$APP_KEY"
```

### Request Authorization (Phase 2)
```bash
python3 scripts/request_authorization.py \
  --appId "$APP_ID" \
  --appKey "$APP_KEY" \
  --phoneNo "$PHONE_NUMBER"
```

Note: templateId is predefined and not required as a parameter

### Poll Authorization Status (Phase 2)
```bash
python3 scripts/poll_authorization.py \
  --appId "$APP_ID" \
  --appKey "$APP_KEY" \
  --authRecordId "$AUTH_RECORD_ID" \
  --interval 5 \
  --timeout 600 \
  --verbose
```

---

## Error Handling

### Phase 1 Errors
- **Invalid credentials**: Check that appId and appKey are correct
- **Corrupted memory file**: Ask user to provide credential file again
- **Missing fields**: Ensure all required fields (appId, appKey) are present

### Phase 1.5 Errors (Binding)
- **Binding failed**: Check the error description and verify appId is correct
- **Network error**: Ensure you have network connectivity to the binding API
- **Signature error**: Verify appKey is correct and JSON is properly sorted

### Phase 2 Errors
- **Credentials not found**: Return to Phase 1, ask user for credential file
- **Invalid phone number**: Ensure phone number is not empty
- **Encryption failure**: Verify appKey is correct
- **Signature mismatch**: Check appKey and ensure JSON is sorted
- **Authorization timeout**: Maximum 10 minutes, user must complete authorization faster
- **Authorization failed**: statusCode is not "000000", deny operation and inform user

### Recovery
- If credentials are corrupted or invalid, ask user to provide credential file again (Phase 1)
- If binding fails, check appId, then retry binding (Phase 1.5)
- If authorization fails, user must initiate the sensitive operation again (Phase 2)
- If polling times out, user must authorize faster or restart the process (Phase 2)

---

## Important Notes

- **New signature format**: Use sorted JSON with HmacSHA256
- **New headers**: Use `appId` and `signValue` instead of `X-App-Id` and `X-Sign`
- **Removed headers**: `X-Timestamp`, `X-Nonce`, `X-Sign-Version` are no longer required
- **Encryption unchanged**: Still uses AES/ECB/PKCS5Padding with MD5(appKey)
- **JSON sorting**: Always use `sort_keys=True` when generating JSON for signature
