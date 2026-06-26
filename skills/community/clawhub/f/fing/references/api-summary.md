# Fing Local API summary

Source: https://www.fing.com/integrations/local-api/ fetched 2026-05-01. Treat upstream documentation as authoritative.

## Overview

Fing exposes a local HTTP API from Fing Desktop, Fing Agent, and Fingbox for local network monitoring data. It is intended for real-time device presence, connection history, and network status without external cloud API calls.

Default documented URL:

```text
http://localhost:49090/1/<endpoint>?auth=<api_key>
```

For a remote/local LAN agent, replace `localhost` with the agent IP/hostname.

## Auth

All endpoints require the API key as query parameter:

```text
?auth=YOUR_API_KEY
```

Keep the key confidential; it grants access to local network device data.

## Endpoints

### GET /1/devices

Returns all discovered local-network devices.

200 response fields:

- `networkId`: network identifier.
- `devices`: array of device objects.

Device fields:

- `mac`: MAC address.
- `ip`: array of IP addresses.
- `state`: `UP` or `DOWN`.
- `name`: human-readable device name.
- `type`: device category, e.g. `STREAMING_DONGLE`.
- `make`: manufacturer.
- `model`: model.
- `contactId`: UUID reference to owning contact, if assigned.
- `first_seen`: ISO timestamp.
- `last_changed`: ISO timestamp.

### GET /1/people

Fing Desktop only. Not supported by Fing Agent or Fingbox; unsupported agents return service error.

Returns contacts and current online/offline presence state derived from assigned presence devices.

200 response fields:

- `networkId`: network identifier.
- `lastChangeTime`: ISO timestamp.
- `people`: array of contacts.

Contact fields:

- `stateChangeTime`: last online/offline change.
- `contactInfo`: human-readable details such as `contactId`, `displayName`, `contactType`.
- `currentState`: `ONLINE` or `OFFLINE`; may be absent if no presence device is assigned.
- `presenceDeviceDetails`: details of presence device.

## HTTP errors

- `400`: invalid input.
- `401`: unauthorized; invalid or missing API key.
- `503`: service error; agent unavailable, unsupported endpoint, or agent not running.

## Safety

Device lists expose private network inventory. Summarize by counts/type/state unless detailed device data is needed for troubleshooting.
