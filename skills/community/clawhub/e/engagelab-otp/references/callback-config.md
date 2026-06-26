# OTP Callback Configuration Reference

Configure webhook URLs to receive real-time events from the EngageLab OTP platform.

## Table of Contents

1. [Callback URL Setup](#callback-url-setup)
2. [Security Mechanisms](#security-mechanisms)
3. [Event Types](#event-types)
   - [Message Status Events](#message-status-events)
   - [Notification Events](#notification-events)
   - [Message Response Events](#message-response-events)
   - [System Events](#system-events)

---

## Callback URL Setup

After configuring the callback URL in the EngageLab console, the platform sends an HTTP POST request to validate availability. Your service must return HTTP 200 within 3 seconds.

**Firewall whitelist**: Add `119.8.170.74` and `114.119.180.30` to your server's firewall.

**Validation request**:

```bash
curl -X POST https://your-callback-url.com -d ''
```

**Required response**: HTTP 200 with empty body.

---

## Security Mechanisms

### Username and Secret Validation (Optional)

When configured, EngageLab includes an `X-CALLBACK-ID` header:

```
X-CALLBACK-ID: timestamp={timestamp};nonce={nonce};username={username};signature={signature}
```

**Signature verification** (Python):

```python
import hashlib, hmac

def verify(username, secret, timestamp, nonce, signature):
    return signature == hmac.new(
        key=secret.encode(),
        msg=f'{timestamp}{nonce}{username}'.encode(),
        digestmod=hashlib.sha256
    ).hexdigest()
```

### Authorization Authentication (Optional)

If your callback endpoint requires authentication (Basic Auth, Bearer Token), provide the Authorization info during configuration. EngageLab automatically includes it in callback requests.

---

## Event Types

All callbacks use this outer structure:

```json
{
  "total": 1,
  "rows": [{ /* event object */ }]
}
```

### Message Status Events

Track the lifecycle of each message with real-time delivery status updates.

| Event Identifier | Description |
|------------------|-------------|
| `plan` | Message scheduled and added to sending queue |
| `target_valid` | Target number is valid |
| `target_invalid` | Target number is invalid |
| `sent` | Message successfully sent |
| `sent_failed` | Message sending failed |
| `delivered` | Message delivered to user's device |
| `delivered_failed` | Message sent but failed to deliver |
| `verified` | User completed OTP verification |
| `verified_failed` | User verification failed |
| `verified_timeout` | User did not verify within the time limit |

**ReportLifecycle Object**:

| Field | Type | Description |
|-------|------|-------------|
| `message_id` | string | Unique message ID |
| `to` | string | Recipient phone number |
| `server` | string | Service type (e.g., `otp`) |
| `channel` | string | Channel type |
| `itime` | int64 | Callback timestamp (seconds) |
| `custom_args` | object | Custom parameters (returned if provided) |
| `status` | object | Status details |

**Status Object**:

| Field | Type | Description |
|-------|------|-------------|
| `message_status` | string | Current status (see event identifiers above) |
| `status_data` | object | Contains `msg_time`, `message_id`, `current_send_channel`, `template_key`, `business_id` |
| `billing` | object | Billing info: `cost` (float64) and `currency` ("USD"). Included for `sent` stage |
| `error_code` | int | Error code, 0 = no error |
| `error_detail` | object | Contains `message` field with error description |

**Example — Message Sent Successfully**:

```json
{
  "total": 1,
  "rows": [{
    "message_id": "123456789",
    "to": "+6581234567",
    "server": "sms",
    "channel": "sms",
    "itime": 1701234567,
    "custom_args": { "order_id": "ORDER123" },
    "status": {
      "message_status": "sent",
      "status_data": {
        "msg_time": 1701234560,
        "message_id": "123456789",
        "current_send_channel": "CHANNEL_A",
        "template_key": "verify_code",
        "business_id": "1001"
      },
      "billing": { "cost": 0.005, "currency": "USD" },
      "error_code": 0
    }
  }]
}
```

**Example — Message Failed**:

```json
{
  "total": 1,
  "rows": [{
    "message_id": "123456790",
    "to": "+6581234568",
    "server": "sms",
    "channel": "sms",
    "itime": 1701234568,
    "status": {
      "message_status": "sent_fail",
      "status_data": {
        "msg_time": 1701234561,
        "message_id": "123456790",
        "current_send_channel": "CHANNEL_B",
        "template_key": "verify_code",
        "business_id": "1001"
      },
      "error_code": 4001,
      "error_detail": { "message": "Invalid phone number" }
    }
  }]
}
```

### Notification Events

System-level alerts for service status and account management.

| Event Identifier | Description |
|------------------|-------------|
| `insufficient_verification_rate` | Verification rate below threshold |
| `insufficient_balance` | Insufficient account balance |
| `template_audit_result` | Template audit result notification |

**Example — Insufficient Balance**:

```json
{
  "total": 1,
  "rows": [{
    "server": "otp",
    "itime": 1712458844,
    "notification": {
      "event": "insufficient_balance",
      "notification_data": {
        "business_id": "1744569418236633088",
        "remain_balance": -0.005,
        "balance_threshold": 2
      }
    }
  }]
}
```

### Message Response Events

Callback events for user interactions (e.g., uplink messages).

| Event Identifier | Description |
|------------------|-------------|
| `uplink_message` | User-sent SMS or other uplink message |

**Example**:

```json
{
  "total": 1,
  "rows": [{
    "server": "otp",
    "itime": 1741083306,
    "message_id": "0",
    "business_id": "0",
    "response": {
      "event": "uplink_message",
      "response_data": {
        "message_sid": "SM1234567890",
        "account_sid": "AC1234567890",
        "from": "+1234567890",
        "to": "+0987654321",
        "body": "Reply message content"
      }
    }
  }]
}
```

### System Events

Operations related to accounts, templates, API calls, and key management.

| Event Identifier | Description |
|------------------|-------------|
| `account_login` | Account login operations |
| `key_manage` | Key changes and management |
| `msg_history` | Message history queries |
| `template_manage` | Template creation, updates, deletions |
| `api_call` | API call operations |

**System Event Structure**:

```json
{
  "total": 1,
  "rows": [{
    "server": "otp",
    "itime": 1694012345,
    "system_event": {
      "event": "event_identifier",
      "data": {
        "business_id": "123",
        "org_id": "org-abc",
        "operator": {
          "email": "user@example.com",
          "api_key": "api-xxxx",
          "ip_address": "1.2.3.4"
        }
      }
    }
  }]
}
```

#### Account Login Events

| Field | Type | Description |
|-------|------|-------------|
| `action` | string | `login_success`, `login_failed`, or `logout` |
| `fail_reason` | string | Only for `login_failed` |

#### Template Management Events

| Field | Type | Description |
|-------|------|-------------|
| `action` | string | `create`, `update`, or `delete` |
| `template_id` | string | Template ID |
| `template_name` | string | Template name |

#### Key Management Events

| Field | Type | Description |
|-------|------|-------------|
| `action` | string | `create`, `update`, `delete`, or `view` |
| `api_key` | string | API Key |
| `description` | string | Description (optional) |

#### API Call Events

| Field | Type | Description |
|-------|------|-------------|
| `api_path` | string | API endpoint path |
| `method` | string | HTTP method |
