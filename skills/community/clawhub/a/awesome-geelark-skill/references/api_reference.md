# GeeLark API Reference

Complete list of all verified GeeLark API endpoints.

---

## Base URL

**Base URL**: `https://openapi.geelark.com`

**Example**: `https://openapi.geelark.com/open/v1/phone/list`

---

## Authentication

All API requests require authentication using one of two methods:

### Method 1: Token Authentication (Recommended)

**Headers**:
```
Content-Type: application/json
traceId: <UUID v4>
Authorization: Bearer <your_token>
```

**Python Example**:
```python
import requests
import uuid

headers = {
    "Content-Type": "application/json",
    "traceId": str(uuid.uuid4()),
    "Authorization": "Bearer your_token_here"
}

response = requests.post(
    "https://openapi.geelark.com/open/v1/phone/list",
    headers=headers,
    json={"page": 1, "pageSize": 10}
)
```

### Method 2: Key Authentication

**Headers**:
```
Content-Type: application/json
appId: <your_appId>
traceId: <UUID v4>
ts: <millisecond timestamp>
nonce: <first 6 chars of traceId>
sign: <SHA256(appId + traceId + ts + nonce + apiKey) uppercase hex>
```

**Python Example**:
```python
import requests
import uuid
import time
import hashlib

APP_ID = "your_app_id"
API_KEY = "your_api_key"

trace_id = str(uuid.uuid4())
ts = str(int(time.time() * 1000))
nonce = trace_id[:6]

sign_raw = f"{APP_ID}{trace_id}{ts}{nonce}{API_KEY}"
sign = hashlib.sha256(sign_raw.encode()).hexdigest().upper()

headers = {
    "Content-Type": "application/json",
    "appId": APP_ID,
    "traceId": trace_id,
    "ts": ts,
    "nonce": nonce,
    "sign": sign
}

response = requests.post(
    "https://openapi.geelark.com/open/v1/phone/list",
    headers=headers,
    json={"page": 1, "pageSize": 10}
)
```

---

## Request Format

- **Method**: All endpoints use `POST`
- **Content-Type**: `application/json`
- **Rate Limit**: 
  - 200 requests per minute
  - 24,000 requests per hour
  - ⚠️ Exceeding limit locks the endpoint for 2 hours

---

## Response Format

All API responses follow this structure:

```json
{
  "traceId": "uuid-string",
  "code": 0,
  "msg": "success",
  "data": {
    // Response data (null on error)
  }
}
```

**Fields**:
- `traceId` - Unique request ID for debugging
- `code` - Status code (`0` = success, non-zero = error)
- `msg` - Status message
- `data` - Response data (contains result on success, error details on failure)

---

## Error Codes

### Common Error Codes

| Code | Description | Category |
|------|-------------|----------|
| `0` | Success | General |
| `40000` | Unknown error | General |
| `40001` | Request body read failed | General |
| `40002` | traceId is empty | General |
| `40003` | Signature verification failed | General |
| `40004` | Parameter validation failed | General |
| `40005` | Resource not found | General |
| `40006` | Batch operation partially succeeded | General |
| `40007` | Request rate limited (1 min) | Rate Limit |
| `40008` | pageSize exceeds limit | General |
| `40009` | Batch operation all failed | General |
| `40010` | Resource occupied, cannot delete | General |
| `40011` | Paid users only | General |
| `40012` | API deprecated | General |
| `40013` | User not found | General |
| `40014` | Hourly limit exceeded (2 hour lock) | Rate Limit |
| `40015` | Insufficient permissions | General |
| `40016` | IP not in whitelist | General |
| `40017` | Too frequent, retry later | Rate Limit |
| `50000` | Server error | General |

### Cloud Phone Error Codes

| Code | Description |
|------|-------------|
| `42001` | Cloud phone does not exist |
| `42002` | Cloud phone not in running state |
| `42003` | Installing corresponding app |
| `42004` | Cannot install lower version |
| `42005` | App not installed |
| `42006` | App does not exist |
| `42007` | Upload task not found |
| `42008` | Wrong app version, only specific version allowed |
| `43001` | Has associated environments, cannot delete |
| `43002` | User not on pro plan |
| `43004` | Cloud phone expired |
| `43005` | Cloud phone executing task, cannot delete/reset |
| `43006` | Cloud phone under remote control, cannot delete/reset |
| `43008` | Daily open limit reached (UTC timezone) |
| `43009` | Cloud phone already running, cannot delete/reset |
| `43010` | Cloud phone starting, cannot delete/reset |
| `43011` | Cloud phone executing reset, cannot operate |
| `43012` | Cloud phone GPS info error |
| `43013` | Plugin installation task does not exist |
| `43014` | GPS not set |
| `43015` | Cloud phone does not support reset |
| `43016` | Cloud phone does not support root |
| `43017` | No monthly subscription device |
| `43018` | Cloud phone not bound to monthly device |
| `43019` | Only monthly subscription supported |
| `43020` | Cloud phone backup data error / Tag name empty |
| `43021` | Cloud phone in use, cannot delete / Tag already exists |
| `43022` | Cannot transfer environment to self / Tag does not exist |
| `43023` | Environment name empty / Tag color does not exist |
| `43024` | Brand/model mismatch |
| `43025` | Language not supported |
| `43026` | System not supported |
| `43027` | Browser does not support transfer |
| `43028` | Sub-user environment group limit |
| `43029` | Device model under maintenance |
| `43030` | Group name empty |
| `43031` | Group already exists |
| `43032` | Group does not exist |
| `43033` | Group name not found |
| `43034` | Group remark not found |
| `43035` | Cannot edit ungrouped |
| `43036` | Cloud phone running, cannot execute operation |
| `43037` | Accessibility hiding not supported |
| `43038` | Device model deleted |
| `43039` | Authorization under maintenance |
| `49001` | ADB not enabled |
| `49002` | Device model does not support ADB |
| `50001` | Device model does not support shell |
| `52001` | Device model does not support SMS |
| `53001` | Device model does not support patch installation |

### Task Error Codes

| Code | Description |
|------|-------------|
| `41000` | Insufficient task credits |
| `41001` | Insufficient balance |
| `48000` | Too many task retries |
| `48001` | Task already succeeded/failed, cannot operate |
| `48002` | Task does not exist |
| `48003` | Task material expired |
| `48004` | TikTok task app version mismatch |

### Material & Webhook Error Codes

| Code | Description |
|------|-------------|
| `60001` | Material library capacity exceeded |
| `60002` | Duplicate tag name |
| `60003` | Invalid link |
| `60004` | File format not supported |
| `60005` | Material does not exist |
| `51001` | User callback does not exist |

### Proxy Error Codes

| Code | Description |
|------|-------------|
| `45001` | Proxy does not exist |
| `45002` | Proxy unavailable |
| `45003` | Proxy not supported (China mainland IP) |
| `45004` | Proxy verification failed |
| `45005` | Region not supported |
| `45006` | Proxy info error |
| `45007` | Duplicate proxy |
| `45008` | Proxy type not supported |

### Plan Error Codes

| Code | Description |
|------|-------------|
| `44001` | Pro plan limit |
| `44002` | Plan environment limit reached |
| `44003` | User environment limit reached |
| `44004` | Daily environment creation limit reached |
| `44005` | Group not filled |
| `44006` | Cloud phone inventory insufficient |
| `46001` | Plan expired |
| `46002` | Plan team environment limit exceeded |
| `46003` | Environment count exceeds plan limit |

### Device Error Codes

| Code | Description |
|------|-------------|
| `47001` | Device concurrency limit |
| `47002` | Devices exhausted |
| `47003` | Associated device expired |
| `47004` | Associated device does not exist |

---

## Cloud Phone Management

| Endpoint | Method | Parameters | Description | Status |
|----------|--------|------------|-------------|--------|
| `/open/v1/phone/list` | POST | `{"page":1,"pageSize":10}` | List all cloud phones | ✅ |
| `/open/v1/phone/status` | POST | `{"ids":["phoneId"]}` | Get cloud phone status | ✅ |
| `/open/v1/phone/start` | POST | `{"ids":["phoneId"]}` | Start cloud phone(s) | ✅ |
| `/open/v1/phone/stop` | POST | `{"ids":["phoneId"]}` | Stop cloud phone(s) | ✅ |
| `/open/v1/phone/delete` | POST | `{"ids":["phoneId"]}` | Delete cloud phone(s) | ✅ ⚠️ |
| `/open/v1/phone/gps/set` | POST | `{"list":[{"id":"xxx","latitude":1.2,"longitude":1.2}]}` | Set GPS location | ✅ |
| `/open/v1/phone/addNew` | POST | `{"mobileType":"Android 11","data":[{"profileName":"myPhone"}]}` | Create new cloud phone | ✅ |
| `/open/v1/phone/screenShot` | POST | `{"id":"phoneId"}` | Take screenshot | ✅ |

**Pagination Parameters**:
- `page` and `pageSize` are optional for list endpoints
- Default values vary by endpoint (typically page=1, pageSize=10)
- `pageSize` has maximum limit (check official docs, typically 100)
- Error 40008 indicates pageSize exceeds allowed range

**Important Notes**:
- `/open/v1/phone/delete` requires cloud phones to be stopped first (error 43009 if running)
- **Batch operations**: 
  - `start`, `stop`, `delete` support multiple IDs in array: `{"ids":["id1","id2","id3"]}`
  - Single device limit: Check official docs for maximum batch size
  - Batch operations are NOT atomic - individual devices may succeed/fail independently
  - Check response `data` field for per-device results on batch operations

---

## Balance & Billing

| Endpoint | Method | Parameters | Description | Status |
|----------|--------|------------|-------------|--------|
| `/open/v1/pay/wallet` | POST | `{}` | Get account balance | ✅ |
| `/open/v1/billing/transaction/detail` | POST | `{}` | Get billing transactions | ✅ |

---

## Group / Tag / Proxy

### Groups

| Endpoint | Method | Parameters | Description | Status |
|----------|--------|------------|-------------|--------|
| `/open/v1/group/list` | POST | `{"page":1,"pageSize":10}` | List groups | ✅ |
| `/open/v1/group/delete` | POST | `{"ids":["groupId"]}` | Delete group(s) | ✅ |

### Tags

| Endpoint | Method | Parameters | Description | Status |
|----------|--------|------------|-------------|--------|
| `/open/v1/tag/delete` | POST | `{"ids":["tagId"]}` | Delete tag(s) | ✅ |

### Proxies

| Endpoint | Method | Parameters | Description | Status |
|----------|--------|------------|-------------|--------|
| `/open/v1/proxy/add` | POST | `{"list":[{"scheme":"socks5","server":"1.2.3.4","port":8000}]}` | Add proxy | ✅ |
| `/open/v1/proxy/delete` | POST | `{"ids":["proxyId"]}` | Delete proxy | ✅ |

---

## Application Management

| Endpoint | Method | Parameters | Description | Status |
|----------|--------|------------|-------------|--------|
| `/open/v1/app/installable/list` | POST | `{"envId":"xxx","name":"","page":1,"pageSize":100}` | List installable apps | ✅ |
| `/open/v1/app/install` | POST | `{"envId":"xxx","appVersionId":"xxx"}` | Install app | ✅ |
| `/open/v1/app/list` | POST | `{"envId":"xxx","page":1,"pageSize":10}` | List installed apps | ✅ |
| `/open/v1/app/start` | POST | `{"envId":"xxx","packageName":"com.xxx"}` | Start app | ✅ |
| `/open/v1/app/stop` | POST | `{"envId":"xxx","packageName":"com.xxx"}` | Stop app | ✅ |
| `/open/v1/app/uninstall` | POST | `{"envId":"xxx","packageName":"com.xxx"}` | Uninstall app | ✅ |

**Critical Notes**:
- `/open/v1/app/install` requires `appVersionId`, NOT `appName`. Get `appVersionId` from `/open/v1/app/installable/list` response.
- `envId` is the cloud phone ID (same as `id` from `/open/v1/phone/list` response)
- **Batch operations**: Some endpoints support batch operations with arrays (check individual endpoint docs)

---

## ADB

| Endpoint | Method | Parameters | Description | Status |
|----------|--------|------------|-------------|--------|
| `/open/v1/adb/getData` | POST | `{"ids":["phoneId"]}` | Get ADB connection info | ✅ |
| `/open/v1/adb/setStatus` | POST | `{"ids":["phoneId"],"open":true}` | Enable/disable ADB | ✅ |

---

## Task Management

| Endpoint | Method | Parameters | Description | Status |
|----------|--------|------------|-------------|--------|
| `/open/v1/task/query` | POST | `{"ids":["taskId"]}` | Query task status | ✅ |
| `/open/v1/task/detail` | POST | `{"ID":"taskId"}` | Get task details | ⚠️ |
| `/open/v1/task/cancel` | POST | `{"ids":["taskId"]}` | Cancel task | ⚠️ |
| `/open/v1/task/restart` | POST | `{"IDs":["taskId"]}` | Restart task | ⚠️ |
| `/open/v1/task/historyRecords` | POST | `{"page":1,"pageSize":10}` | Get task history | ✅ |
| `/open/v1/task/flow/list` | POST | `{"page":1,"pageSize":10}` | List task flows | ✅ |
| `/open/v1/task/flow/export` | POST | `{"ID":"flowId"}` | Export task flow | ⚠️ |
| `/open/v1/task/flow/import` | POST | `{"Gal":{}}` | Import task flow | ⚠️ |
| `/open/v1/task/rpa/add` | POST | `{"flowId":"xxx","paramMap":{}}` | Add RPA task | ⚠️ |

**⚠️ Important Notes**:
- Parameters marked with ⚠️ require valid task/flow IDs
- **Field name inconsistency**: Some endpoints use `ids` (lowercase), others use `ID` or `IDs` (uppercase)
  - `query` and `cancel` use `ids`
  - `detail`, `restart`, `flow/export` use `ID` or `IDs`
  - Always check the exact field name for each endpoint

---

## RPA Tasks - TikTok

| Endpoint | Required Parameters | Optional Parameters | Description |
|----------|-------------------|---------------------|-------------|
| `/open/v1/rpa/task/tiktokLogin` | `account`, `password` | `name`, `remark`, `scheduleAt`, `id` | Login to TikTok |
| `/open/v1/rpa/task/tiktokRandomFollow` | `followProbability` (0-100) | `name`, `remark`, `scheduleAt`, `id` | Randomly follow users |
| `/open/v1/rpa/task/tiktokRandomFollowAsia` | `followProbability` | `name`, `remark`, `scheduleAt`, `id` | Randomly follow (Asia) |
| `/open/v1/rpa/task/tiktokRandomStar` | - | `name`, `remark`, `scheduleAt`, `id` | Randomly like videos |
| `/open/v1/rpa/task/tiktokRandomStarAsia` | - | `name`, `remark`, `scheduleAt`, `id` | Randomly like (Asia) |
| `/open/v1/rpa/task/tiktokRandomComment` | `useAi` (1=AI, 2=manual), `comment` | `name`, `remark`, `scheduleAt`, `id` | Randomly comment |
| `/open/v1/rpa/task/tiktokRandomCommentAsia` | `useAi` (1=AI, 2=manual), `comment` | `name`, `remark`, `scheduleAt`, `id` | Randomly comment (Asia) |
| `/open/v1/rpa/task/tiktokEdit` | - | `name`, `remark`, `scheduleAt`, `id` | Edit video |
| `/open/v1/rpa/task/tiktokDel` | - | `name`, `remark`, `scheduleAt`, `id` | Delete video |
| `/open/v1/rpa/task/tiktokDelAsia` | - | `name`, `remark`, `scheduleAt`, `id` | Delete video (Asia) |
| `/open/v1/rpa/task/tiktokHide` | - | `name`, `remark`, `scheduleAt`, `id` | Hide video |
| `/open/v1/rpa/task/tiktokHideAsia` | - | `name`, `remark`, `scheduleAt`, `id` | Hide video (Asia) |

**Common Parameters**:
```json
{
  "name": "task_name",
  "remark": "task_remark",
  "scheduleAt": 1741846843,  // Unix timestamp
  "id": "phoneId"
}
```

**Complete Request Example**:
```python
import requests

# TikTok Login Task Example
headers = {
    "Content-Type": "application/json",
    "traceId": "your-uuid-here",
    "Authorization": "Bearer your_token"
}

payload = {
    "account": "tiktok_user@example.com",
    "password": "your_password",
    "name": "tiktok_login_task",
    "remark": "Auto login task",
    "id": "phone_id_here"
}

response = requests.post(
    "https://openapi.geelark.com/open/v1/rpa/task/tiktokLogin",
    headers=headers,
    json=payload
)

result = response.json()
if result["code"] == 0:
    print(f"✅ Task created: {result['data']}")
else:
    print(f"❌ Failed: {result['msg']}")
```

---

## RPA Tasks - Instagram

| Endpoint | Required Parameters | Optional Parameters | Description |
|----------|-------------------|---------------------|-------------|
| `/open/v1/rpa/task/instagramLogin` | `account`, `password` | `name`, `remark`, `scheduleAt`, `id` | Login to Instagram |
| `/open/v1/rpa/task/instagramPubReels` | `description`, `video[]` | `name`, `remark`, `scheduleAt`, `id` | Publish reels |
| `/open/v1/rpa/task/instagramPubReelsImages` | `Image[]` | `name`, `remark`, `scheduleAt`, `id` | Publish reels with images |
| `/open/v1/rpa/task/instagramEdit` | - | `name`, `remark`, `scheduleAt`, `id` | Edit post |
| `/open/v1/rpa/task/instagramWarmup` | - | `name`, `remark`, `scheduleAt`, `id` | Account warmup |

**Important Notes**:
- Field name is `Image` (capital I, not `images`) for `instagramPubReelsImages`
- `Image[]` is an array type
- `video[]` in `instagramPubReels` is also an array

---

## RPA Tasks - Facebook

| Endpoint | Required Parameters | Optional Parameters | Description |
|----------|-------------------|---------------------|-------------|
| `/open/v1/rpa/task/faceBookLogin` | `Email`, `Password` | `name`, `remark`, `scheduleAt`, `id` | Login to Facebook |
| `/open/v1/rpa/task/faceBookPublish` | `title`, `video[]` | `name`, `remark`, `scheduleAt`, `id` | Publish video |
| `/open/v1/rpa/task/faceBookPubReels` | `title`, `video` (string) | `name`, `remark`, `scheduleAt`, `id` | Publish reels |
| `/open/v1/rpa/task/faceBookAutoComment` | `PostAddress`, `Comment`, `Keyword` | `name`, `remark`, `scheduleAt`, `id` | Auto comment |
| `/open/v1/rpa/task/faceBookActiveAccount` | `BrowsePostsNum`, `Keyword` | `name`, `remark`, `scheduleAt`, `id` | Active account |

**Important Notes**:
- Field name is `Email` (not `account`) for `faceBookLogin`
- **Video field type inconsistency**:
  - `faceBookPublish` uses `video[]` (array)
  - `faceBookPubReels` uses `video` (string)
  - Always check the exact field type for each endpoint

---

## RPA Tasks - YouTube

| Endpoint | Required Parameters | Optional Parameters | Description |
|----------|-------------------|---------------------|-------------|
| `/open/v1/rpa/task/youtubePubShort` | `title`, `video` (string) | `sameStyleVoice`, `originalVoice`, `name`, `remark`, `scheduleAt`, `id` | Publish short |
| `/open/v1/rpa/task/youtubePubVideo` | `title`, `video` | `description`, `name`, `remark`, `scheduleAt`, `id` | Publish video |
| `/open/v1/rpa/task/youTubeActiveAccount` | `BrowseVideoNum`, `Keyword` | `name`, `remark`, `scheduleAt`, `id` | Active account |

**Important Notes**:
- YouTube uses `video` as a **string** (not array) in `youtubePubShort` and `youtubePubVideo`
- This differs from other platforms that use `video[]` (array)
- Always verify the expected type before sending requests

---

## RPA Tasks - Reddit

| Endpoint | Required Parameters | Optional Parameters | Description |
|----------|-------------------|---------------------|-------------|
| `/open/v1/rpa/task/redditImage` | `title`, `images[]`, `community` | `name`, `remark`, `scheduleAt`, `id` | Publish image |
| `/open/v1/rpa/task/redditVideo` | `title`, `video[]`, `community` | `name`, `remark`, `scheduleAt`, `id` | Publish video |
| `/open/v1/rpa/task/redditWarmup` | - | `name`, `remark`, `scheduleAt`, `id` | Account warmup |

---

## RPA Tasks - Threads

| Endpoint | Required Parameters | Optional Parameters | Description |
|----------|-------------------|---------------------|-------------|
| `/open/v1/rpa/task/threadsImage` | `title`, `images[]` | `name`, `remark`, `scheduleAt`, `id` | Publish image |
| `/open/v1/rpa/task/threadsVideo` | `title`, `video[]` | `name`, `remark`, `scheduleAt`, `id` | Publish video |

---

## RPA Tasks - Pinterest

| Endpoint | Required Parameters | Optional Parameters | Description |
|----------|-------------------|---------------------|-------------|
| `/open/v1/rpa/task/pinterestImage` | `title`, `description`, `images[]` | `name`, `remark`, `scheduleAt`, `id` | Publish image |
| `/open/v1/rpa/task/pinterestVideo` | `title`, `description`, `video[]` | `name`, `remark`, `scheduleAt`, `id` | Publish video |

---

## RPA Tasks - X (Twitter)

| Endpoint | Required Parameters | Optional Parameters | Description |
|----------|-------------------|---------------------|-------------|
| `/open/v1/rpa/task/xPublish` | `description`, `video[]` | `name`, `remark`, `scheduleAt`, `id` | Publish post |

---

## RPA Tasks - Google

| Endpoint | Required Parameters | Optional Parameters | Description |
|----------|-------------------|---------------------|-------------|
| `/open/v1/rpa/task/googleLogin` | `Email`, `Password` | `name`, `remark`, `scheduleAt`, `id` | Login to Google |
| `/open/v1/rpa/task/googleAppDownload` | `appName` | `name`, `remark`, `scheduleAt`, `id` | Download app |
| `/open/v1/rpa/task/googleAppBrowser` | `appName` | `name`, `remark`, `scheduleAt`, `id` | Browse app |

---

## RPA Tasks - Shein

| Endpoint | Required Parameters | Optional Parameters | Description |
|----------|-------------------|---------------------|-------------|
| `/open/v1/rpa/task/sheinLogin` | `Email`, `Password` | `name`, `remark`, `scheduleAt`, `id` | Login to Shein |

---

## File Upload / Other Tasks

| Endpoint | Required Parameters | Optional Parameters | Description |
|----------|-------------------|---------------------|-------------|
| `/open/v1/rpa/task/fileUpload` | `Files[]` | `name`, `remark`, `scheduleAt`, `id` | Upload files |
| `/open/v1/rpa/task/keyboxUpload` | `Files[]` | `name`, `remark`, `scheduleAt`, `id` | Upload keybox |
| `/open/v1/rpa/task/importContacts` | `Contacts[]` | `name`, `remark`, `scheduleAt`, `id` | Import contacts |
| `/open/v1/rpa/task/multiPlatformVideoDistribution` | `Title`, `Video[]` | `name`, `remark`, `scheduleAt`, `id` | Multi-platform distribution |

**Important Notes**:
- `Files[]` and `Contacts[]` are array types
- **File upload limits**: Check official docs for size limits and supported formats
- **Supported formats**: Typically MP4, PNG, JPG for media; CSV for contacts
- **File upload workflow**: 
  1. Upload file to GeeLark storage (separate endpoint)
  2. Get file URL/ID from upload response
  3. Use URL/ID in RPA task parameters

---

## Last Updated

2026-04-25

**Official Documentation**: https://github.com/GeeLark/geelark-openapi