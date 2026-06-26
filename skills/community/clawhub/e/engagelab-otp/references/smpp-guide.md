# OTP SMPP Integration Guide

SMPP (Short Message Peer-to-Peer) protocol integration for OTP services via TCP connections.

## Table of Contents

1. [Connection Setup](#connection-setup)
2. [Message Sending](#message-sending)
3. [Delivery Reports](#delivery-reports)
4. [Connection Keep-Alive](#connection-keep-alive)
5. [Status Codes](#status-codes)

---

## Connection Setup

### SMPP Address

Obtain the following from EngageLab sales or technical support:

- **IP Address**: `{ ip }`
- **Port**: `{ port }`
- **Account**: `{ system_id }`
- **Password**: `{ password }`

### Authentication

After establishing a TCP connection, send the `BindTransceiver` command (`0x00000009`) as the first data packet:

- **system_id**: Client system account for identity verification
- **password**: Access password for authentication

### Server Response

- **Success**: `BindTransceiverResp` (`0x80000009`) with the `system_id` echoed back
- **Failure**: TCP connection is disconnected and the reason is logged

---

## Message Sending

Uses the `SUBMIT_SM` command (`0x00000004`).

### Client Data Packet Fields

| Field | Values | Description |
|-------|--------|-------------|
| `service_type` | `MSG` / `CODE` / `MRKT` | Message type. Default: `MSG` |
| `source_addr` | (blank) | Not used in OTP currently |
| `destination_addr` | e.g., `+6581234567` | International phone number format |
| `data_coding` | `UCS2` recommended | Use UCS2 to properly parse `{}` characters |
| `header status` | `0x00000000` | Fixed value |

### Message Content (`short_message`)

JSON format inside the `short_message` field:

```json
{
  "id": "template-id",
  "language": "default",
  "code": "123456",
  "params": {
    "key1": "val1"
  }
}
```

| Field | Description |
|-------|-------------|
| `id` | Template ID |
| `language` | Language, default is `"default"` |
| `code` | Verification code (when `service_type` is `CODE`) |
| `params` | Custom key-value pairs (values must be strings) |

Use `UCS2` encoding (`data_coding`) to ensure `{}` characters are properly parsed. If `{}` can be sent directly, default encoding (`0x00`) may be used.

### Server Response (`SUBMIT_SM_RESP` — `0x80000004`)

**Success**:
- `header status`: `0x00000000`
- `MESSAGE_ID`: Message ID for delivery report association

**Failure status codes**:

| Status Code | Value | Description |
|-------------|-------|-------------|
| `ESME_RINVPARAM` | `0x00000032` | Invalid parameters |
| `ESME_RSYSERR` | `0x00000008` | Internal server error, retry later |
| `ESME_RSUBMITFAIL` | `0x00000045` | Delivery failed (possibly template issues) |
| `ESME_RINVNUMMSGS` | `0x00000055` | Invalid `short_message` format |
| `ESME_RUNKNOWNERR` | `0x000000FF` | Unknown error, contact support |

---

## Delivery Reports

The server reports delivery results via `DELIVER_SM` (`0x00000005`).

### Fields

| Field | Value | Description |
|-------|-------|-------------|
| `service_type` | `MSG` | Fixed |
| `source_addr` | (blank) | — |
| `destination_addr` | — | Matches `SUBMIT_SM` destination |
| `data_coding` | `0x00` | Default encoding |
| `esm_class` | `0x00` | — |
| `short_message` | delivery receipt | Contains `stat` field |
| `ReceiptedMessageID` (TLV) | — | Message ID for association |
| `MessageState` (TLV) | `0x0427` | Message state |

### Delivery Status

| Status | Meaning |
|--------|---------|
| `DELIVRD` | Delivered successfully |
| `UNDELIV` | Delivery failed |

---

## Connection Keep-Alive

Send `EnquireLink` (`0x00000015`) every **30 seconds** (±5 seconds) to maintain the connection.

---

## Supported Commands

The server only accepts these SMPP commands:

| Command | Code |
|---------|------|
| `EnquireLink` | `0x00000015` |
| `Unbind` | `0x00000006` |
| `SubmitSM` | `0x00000004` |
| `DeliverSMResp` | `0x80000005` |
| `BindTransceiver` | `0x00000009` |

Invalid commands receive `GENERIC_NACK` (`0x80000000`).

---

## Status Codes Summary

| Status Code | Meaning |
|-------------|---------|
| `ESME_RINVPARAM` | Invalid parameters |
| `ESME_RINVNUMMSGS` | Invalid `short_message` format |
| `ESME_RSUBMITFAIL` | Delivery failed (template issues) |
| `ESME_RSYSERR` | Internal server error |
| `ESME_RUNKNOWNERR` | Unknown error |
| `DELIVRD` | Successfully delivered |
| `UNDELIV` | Delivery failed |
