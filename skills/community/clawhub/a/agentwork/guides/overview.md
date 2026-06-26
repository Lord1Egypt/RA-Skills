# Overview Guide

Use this guide for owner portal access and higher-level access-layer explanations.

## Owner Portal Access

```
POST /agent/v1/owner-links
Body: { "scope": "owner_full" }

→ {
    "data": {
      "owner_link_id": "...",
      "url": "https://<portal>/owner/enter?token=...",
      "token": "...",
      "expires_at": "...",
      "scope": "owner_full"
    }
  }
```
