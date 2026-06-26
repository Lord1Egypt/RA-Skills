# GeeLark API Error Codes

Complete list of GeeLark API error codes and their solutions.

---

## Error Code Reference

| Code | Description | Severity | Action |
|------|-------------|----------|--------|
| `0` | Success | ✅ | - |
| `40004` | Parameter validation failed | 🔴 | Check request parameters |
| `40005` | Resource not found | 🔴 | Verify resource exists |
| `41001` | Balance not enough | 🔴 | Recharge account |
| `42001` | Cloud phone does not exist | 🔴 | Verify phone ID |
| `42002` | Cloud phone is not running | 🟡 | Start cloud phone first |
| `42006` | App not installed | 🟡 | Install app first |
| `43002` | Pro plan required | 🟡 | Upgrade to Pro plan |
| `43009` | Cloud phone is started | 🔴 | Stop before deleting |
| `43020` | Cloud phone currently unavailable | 🔴 | Try again later |
| `43029` | Device model under maintenance | 🟡 | Try again later |
| `44001` | Cannot batch create | 🔴 | Upgrade to Pro plan |
| `44002` | Reached max creation limit | 🔴 | Upgrade plan or wait |
| `44004` | Reached daily max creation limit | 🟡 | Wait until tomorrow |
| `45006` | Wrong argument | 🔴 | Check parameter format |
| `47002` | Cloud phone resource shortage | 🔴 | Try again later |

---

## Critical Error Codes ⭐⭐⭐

### 41001 - Balance Not Enough

**Description**: Account balance is insufficient to perform the operation.

**Cause**:
- Account balance ≤ 0
- Gift money ≤ 0
- Available time add-on ≤ 0

**Action**:
1. Recharge account at https://open.geelark.com/billing
2. Use `/open/v1/pay/wallet` to check balance
3. Wait for recharge to process

**Example**:
```python
# Check balance
wallet = client.wallet()
balance = wallet['data']['balance']
gift_money = wallet['data'].get('giftMoney', 0)

if balance <= 0 and gift_money <= 0:
    print("❌ Insufficient balance! Please recharge.")
    exit(1)
```

**Historical Error** (2026-04-12):
- Agent deleted cloud phones without authorization
- Root cause: Didn't check `failDetails` in API response
- API returned code 41001 but agent assumed "cloud phone is broken"

---

### 43009 - Cloud Phone Is Started

**Description**: Cannot delete a running cloud phone.

**Cause**:
- Trying to delete a cloud phone that is still running
- API returns `code: 0` but `failAmount > 0` with error 43009

**Action**:
1. Stop the cloud phone first
2. Wait 30-60 seconds for shutdown
3. Then delete

**Example**:
```python
# Step 1: Stop running phones
client.phone_stop([phone_id])

# Step 2: Wait for shutdown
time.sleep(60)

# Step 3: Then delete
client.call("/open/v1/phone/delete", {"ids": [phone_id]})
```

**Correct Order**: Stop → Wait → Delete

---

### 45006 - Wrong Argument

**Description**: Parameter format or value is incorrect.

**Common Causes**:
- `proxyNumber` is string, should be int
- Proxy format is invalid
- Missing required parameters

**Action**:
1. Check parameter types
2. Verify proxy format: `socks5://user:pass@host:port`
3. Ensure all required parameters are present

**Example**:
```python
# ❌ Wrong (proxyNumber as string)
data = {"mobileType": "Android 13", "data": [{"profileName": "phone", "proxyNumber": "6"}]}

# ✅ Correct (proxyNumber as int)
data = {"mobileType": "Android 13", "data": [{"profileName": "phone", "proxyNumber": 6}]}
```

---

## Common Error Patterns

### Fail Details Not Checked ⭐⭐⭐

**Problem**: API returns `code: 0` but operation actually failed.

**Solution**: Always check `failAmount` and `failDetails` in response:

```python
response = client.call("/open/v1/phone/start", {"ids": [phone_id]})

# Check for failures
fail_amount = response.get('data', {}).get('failAmount', 0)
if fail_amount > 0:
    for fail in response['data']['failDetails']:
        error_code = fail.get('code')
        error_msg = fail.get('msg')
        print(f"❌ Failed: code={error_code}, msg={error_msg}")

        # Handle specific errors
        if error_code == 41001:
            print("   → Balance not enough, recharge required")
        elif error_code == 43009:
            print("   → Cloud phone is running, stop first")
```

---

### Cloud Phone Not Ready

**Problem**: Trying to operate on a stopped or unavailable cloud phone.

**Solution**: Use `ensure_cloud_phone_ready()` function:

```python
from scripts.geelark_boot_helper import boot_and_connect

# This function handles:
# - Balance check
# - Cloud phone status check
# - Start cloud phone (if stopped)
# - Enable ADB (if disabled)
# - Return ADB connection info

adb_info = boot_and_connect(phone_id, token)

if not adb_info:
    print("❌ Failed to boot cloud phone")
    exit(1)
```

---

### App Not Installed

**Problem**: Trying to start an app that is not installed.

**Solution**:
1. List installed apps: `/open/v1/app/list`
2. Install app if needed: `/open/v1/app/install`
3. Then start: `/open/v1/app/start`

```python
# Check if app is installed
apps = client.call("/open/v1/app/list", {
    "envId": phone_id,
    "page": 1,
    "pageSize": 100
})

app_found = any(app['packageName'] == target_package for app in apps['data']['items'])

if not app_found:
    print(f"⚠️  App not installed, installing...")
    # Install app
    client.call("/open/v1/app/install", {
        "envId": phone_id,
        "appVersionId": app_version_id
    })
```

---

## Error Handling Best Practices

### 1. Always Check Response Code

```python
response = client.call(endpoint, data)

if response['code'] != 0:
    error_msg = response.get('msg', 'Unknown error')
    print(f"❌ API Error: {error_msg}")
    exit(1)
```

### 2. Check Fail Details

```python
if response.get('data', {}).get('failAmount', 0) > 0:
    for fail in response['data']['failDetails']:
        error_code = fail.get('code')
        # Handle specific error codes
```

### 3. Implement Retry Logic

```python
import time

max_retries = 3
for attempt in range(max_retries):
    response = client.call(endpoint, data)

    if response['code'] == 0:
        break

    if response['code'] in [42006, 47002]:  # Transient errors
        print(f"⚠️  Retrying ({attempt + 1}/{max_retries})...")
        time.sleep(10)
    else:
        break
```

### 4. Use Context Managers

```python
from scripts.geelark_client import GeeLarkClient

# Auto-closes started phones
with GeeLarkClient() as client:
    client.phone_start([phone_id])
    # Your operations here

# Automatically stops all started phones
```

---

## Debugging Tips

### Enable Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Log API Calls

```python
from scripts.cloudphone_logger import CloudPhoneLogger

with CloudPhoneLogger("task_name", phone_id) as log:
    log.api_call(endpoint, data, response_code, response_data)
    # All operations logged automatically
```

### Check Balance Before Operations

```python
wallet = client.wallet()
balance = wallet['data']['balance']

if balance <= 0:
    print("❌ Insufficient balance")
    # Handle low balance
```

---

## Last Updated

2026-04-10

**Related Documents**:
- [API Reference](api_reference.md) - Complete endpoint list
- [Best Practices](best_practices.md) - Safety and performance tips