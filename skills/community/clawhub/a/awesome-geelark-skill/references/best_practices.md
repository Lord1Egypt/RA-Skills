# GeeLark API Best Practices

Safety, security, and performance tips for using GeeLark API.

---

## Safety Practices ⭐⭐⭐

### 1. Always Check Balance Before Operations

**Why**: Prevent unexpected costs and operation failures.

**How**:
```python
from scripts.geelark_client import GeeLarkClient

client = GeeLarkClient()

# Check balance
wallet = client.wallet()
balance = wallet['data']['balance']
gift_money = wallet['data'].get('giftMoney', 0)

if balance <= 0 and gift_money <= 0:
    print("❌ Insufficient balance! Please recharge.")
    exit(1)

print(f"✅ Balance: ${balance:.2f}, Gift: ${gift_money:.2f}")
```

**Rule**: Never start a cloud phone without checking balance first.

---

### 2. Double Confirmation for Delete Operations ⭐⭐⭐

**Why**: Prevent accidental deletion of cloud phones.

**How**: Use the built-in delete helper:

```python
from scripts.delete_helper import delete_cloud_phones_with_confirmation

delete_cloud_phones_with_confirmation(reason="Testing completed")
```

**Process**:
1. List all cloud phones
2. User manually types phone IDs
3. User types 'YES' (case-sensitive)
4. Only then execute deletion

**Rule**: Never call `/open/v1/phone/delete` directly without double confirmation.

---

### 3. Check Fail Details in API Responses ⭐⭐⭐

**Why**: API may return `code: 0` but actual operation failed.

**How**:
```python
response = client.call("/open/v1/phone/start", {"ids": [phone_id]})

# Check for failures
fail_amount = response.get('data', {}).get('failAmount', 0)
if fail_amount > 0:
    print(f"❌ {fail_amount} operation(s) failed:")
    for fail in response['data']['failDetails']:
        error_code = fail.get('code')
        error_msg = fail.get('msg')
        print(f"   code={error_code}, msg={error_msg}")
```

**Historical Error** (2026-04-12):
- Agent deleted cloud phones without authorization
- Root cause: Didn't check `failDetails`
- API returned code 41001 (balance not enough) but agent assumed "cloud phone is broken"

---

### 4. Stop Running Cloud Phones Before Deletion

**Why**: Error 43009 blocks deletion of running phones.

**How**: Use the built-in delete helper (automatically handles stopping):

```python
from scripts.delete_helper import delete_cloud_phones_with_confirmation

# Helper automatically checks status, stops running phones, and requires double confirmation
delete_cloud_phones_with_confirmation(reason="Cleanup completed")
```

**Rule**: Always use `delete_helper` for deletion. It enforces: Stop → Confirm IDs → Confirm 'YES' → Delete.

---

## Performance Optimization



### 2. Enable Energy Saving Mode

**Why**: Reduces cloud phone costs by ~50%.

**How**:
```python
# GeeLarkClient automatically adds energySavingMode=1 when calling /open/v1/phone/start
client.call("/open/v1/phone/start", {"ids": [phone_id]})
# No need to manually set it!
```

**Rule**: `energySavingMode` is auto-enabled by `GeeLarkClient.call()`.

---

### 3. Auto-Close Idle Devices

**Why**: Prevents unnecessary billing.

**How**:
```python
from scripts.phone_manager import PhoneManager

manager = PhoneManager(timeout_minutes=5)
manager.start_monitor()

# Connect using phone_id (name is optional for display)
d = manager.connect_device("phone_id_123", ip, port, pwd, name="Android15")

# Record activity using phone_id
manager.record_activity("phone_id_123")
```

**Benefits**:
- Save costs
- Release resources
- Prevent forgotten phones from racking up charges



## Security Best Practices

### 1. Use Environment Variables for Credentials

**Why**: Prevents credentials from being committed to version control.

**How**:
```python
import os

token = os.getenv("GEELARK_TOKEN")
if not token:
    raise ValueError("GEELARK_TOKEN environment variable not set")

client = GeeLarkClient(token)
```

---

### 2. Validate All User Inputs

**Why**: Prevents injection attacks and invalid operations.

**How**:
```python
def validate_phone_id(phone_id: str) -> bool:
    """Validate phone ID format"""
    if not phone_id or not phone_id.isdigit():
        return False
    if len(phone_id) != 18:  # GeeLark phone IDs are 18 digits
        return False
    return True

if not validate_phone_id(user_input):
    print("❌ Invalid phone ID format")
    return
```

---

### 3. Use Endpoint Whitelisting

**Why**: Prevents accidental or malicious API calls to undocumented endpoints.

**How**:
```python
# GeeLarkClient has built-in endpoint whitelisting
ALLOWED_ENDPOINTS = {
    "/open/v1/phone/list",
    "/open/v1/phone/start",
    # ... other endpoints
}

client.call(endpoint, data)  # Raises error if endpoint not in whitelist
```

---

## Operational Best Practices

### 1. Use Context Managers

**Why**: Ensures resources are properly cleaned up.

**How**:
```python
from scripts.phone_manager import PhoneManager

# PhoneManager supports context manager and auto-closes idle devices
with PhoneManager(timeout_minutes=5) as manager:
    # Connect using phone_id
    d = manager.connect_device("phone_id_123", ip, port, pwd, name="Android15")
    # Your operations here
    manager.record_activity("phone_id_123")

# Automatically stops all phones and saves logs on exit
```

---

### 2. Log All Operations

**Why**: Enables debugging and auditing.

**How**:
```python
from scripts.cloudphone_logger import CloudPhoneLog

# Method 1: Direct usage
log = CloudPhoneLog("task_name", phone_id)
log.api_call("/open/v1/phone/start", {...})
log.adb_cmd("adb connect", rc=0)
log.step("UI", "click", "text='Submit'")
log.screenshot("/tmp/screen.png", 12345)
log.save()

# Method 2: Context manager (auto-saves)
with CloudPhoneLog("task_name", phone_id) as log:
    log.api_call("/open/v1/phone/start", {...})
    log.step("UI", "click", "text='Submit'")
# Log auto-saved to: logs/cloudphone/YYYYMMDD_HHMMSS_mmm_task_name_phoneid.log
```

---

### 3. Use State-Aware Operations

**Why**: Prevents blind operations and ensures reliability.

**How**:
```python
# 1. Get page structure before operation
xml_before = device.dump_hierarchy()

# 2. Check if element exists
if "Submit" not in xml_before:
    print("❌ Submit button not found")
    return

# 3. Execute operation
device(text="Submit").click()

# 4. Verify result
xml_after = device.dump_hierarchy()
if "Success" in xml_after:
    print("✅ Operation successful")
else:
    print("❌ Operation failed")
```

**Rule**: Every operation should be: Get state → Act → Verify state.

---

### 4. Implement Retry Logic

**Why**: Handles transient errors and improves reliability.

**How**:
```python
import time

def call_with_retry(client, endpoint, data, max_retries=3):
    """Call API with retry logic for transient errors"""
    for attempt in range(max_retries):
        response = client.call(endpoint, data)

        if response['code'] == 0:
            return response

        # Retry on transient errors
        if response['code'] in [42006, 47002]:  # Transient errors
            print(f"⚠️  Retrying ({attempt + 1}/{max_retries})...")
            time.sleep(10)
        else:
            break

    return response  # Return last response (failed)
```

---

## Cost Optimization

### 1. Monitor Cloud Phone Usage

**Why**: Identify and eliminate unnecessary costs.

**How**:
```python
# Check billing history
billing = client.billing_transactions()

# Analyze usage
total_cost = sum(tx['amount'] for tx in billing['data']['items'])
print(f"Total cost: ${total_cost:.2f}")
```

---


### 3. Stop Idle Devices Promptly

**Why**: Billing continues while phones are running.

**How**:
```python
from scripts.phone_manager import PhoneManager

manager = PhoneManager(timeout_minutes=5)
manager.start_monitor()

# Auto-closes after 5 minutes of no activity
```

---

## Debugging Tips

### 1. Enable Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 2. Use Verbose Logging

```python
import uiautomator2 as u2

d = u2.connect(f"{ip}:{port}")
d.debug = True  # Enable debug mode to see HTTP request/response details
```

### 3. Test with Single Device First

**Why**: Easier to debug than parallel operations.

**How**:
```python
from scripts.geelark_boot_helper import boot_and_connect

# Test with one device first (token auto-loads from config)
adb_info = boot_and_connect(phone_id)
if not adb_info:
    print("❌ Boot failed on single device")
    exit(1)

# Only then scale to multiple devices
```

---

## Common Pitfalls to Avoid

### ❌ Don't

1. Skip balance checks before starting cloud phones
2. Delete cloud phones without double confirmation
3. Ignore `failDetails` in API responses
4. Delete running cloud phones (error 43009)
5. Forget to stop idle cloud phones
6. Use serial operations for multiple devices
7. Skip energy saving mode
8. Hardcode credentials
9. Blindly operate without checking page state
10. Ignore error codes and assume success

---

### ✅ Do

1. Always check balance first
2. Use double confirmation for deletions
3. Check `failAmount` and `failDetails`
4. Stop running phones before deleting
5. Auto-close idle devices
6. Use parallel operations
7. Enable energy saving mode
8. Use environment variables for credentials
9. Verify state before and after operations
10. Handle all error codes properly

---

## Last Updated

2026-04-25

**Related Documents**:
- [Error Codes](error_codes.md) - Complete error handling guide
- [API Reference](api_reference.md) - Complete endpoint list