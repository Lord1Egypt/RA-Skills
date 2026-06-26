# Frameo Cloud API Endpoints

Base URL: `https://api.frameo.net`
Auth URL: `https://auth.frameo.net/auth/realms/frameo/protocol/openid-connect/token`

## Authentication

### Login (OAuth2 Password Grant)
```
POST https://auth.frameo.net/auth/realms/frameo/protocol/openid-connect/token
Content-Type: application/x-www-form-urlencoded

client_id=frameo-app
grant_type=password
username=<email>
password=<password>
scope=offline_access email profile
```

Response includes `access_token` and `refresh_token`.

**Note:** Tokens expire in ~5 minutes. Use refresh_token or capture fresh token from Proxyman.

## API Endpoints

### List Frames
```
GET /v1/managed-pairings/frames
Authorization: Bearer <token>
```

Response:
```json
{
  "frames": [
    {
      "peerId": "8cac94fdd6249557...",
      "name": "Living Room",
      "placement": "Office",
      "protocolVersion": 14
    }
  ]
}
```

### Register Client
```
POST /v1/managed-pairings/client
Authorization: Bearer <token>
Content-Type: application/json

{"deviceId": "<uuid>", "peerId": "<hex>"}
```

### Get User Account
```
GET /v1/useraccount
Authorization: Bearer <token>
```

## Required Headers

```
Authorization: Bearer <token>
client_application_id: net.frameo.app
client_platform: iOS
client_type: frameo_client
client_software_version_name: 1.36.20
User-Agent: Frameo/1.36.20 (net.frameo.app; build:3914; iOS 26.4.0) Alamofire/5.10.2
```

## Photo Upload

Photo upload uses **Firebase Cloud Messaging (FCM)** for peer-to-peer delivery, not REST API.
Direct upload endpoints return 403 Forbidden.

For photo upload, use **ADB method** instead (see adb-commands.md).
