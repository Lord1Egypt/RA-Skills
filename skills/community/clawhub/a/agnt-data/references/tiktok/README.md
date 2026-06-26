# TikTok API Reference

**App name:** `tiktok`
**Base URL:** `https://api.agntdata.dev/v1/data/tiktok`
**Endpoints:** 12

Unified access to video details, creator profiles, and search across accounts and videos. Built for LLMs and automation — not one-off scraping.

## Authentication

All requests require the agntdata API key:

```
Authorization: Bearer $AGNTDATA_API_KEY
```

---

## Available Endpoints

| Method | Path | Summary |
|--------|------|---------|
| `GET` | `/video/details` | Video Details |
| `POST` | `/video/details` | Video Details |
| `GET` | `/user/videos` | User's Videos |
| `POST` | `/user/videos` | User's Videos |
| `GET` | `/collection/` | Collection Videos/Details |
| `GET` | `/user/videos/continuation` | User's Videos Continuation |
| `GET` | `/user/details` | User's Details |
| `POST` | `/user/details` | User's Details |
| `GET` | `/search/accounts/query` | Search Accounts |
| `POST` | `/search/accounts/query` | Search Accounts |
| `GET` | `/search/general/query` | Search Videos |
| `POST` | `/search/general/query` | Search Videos |

## Tool Schemas

The following JSON defines all available tools with their parameters. Each tool maps to an API endpoint.

```json
[
  {
    "name": "agntdata_tiktok_Video_Details_get",
    "description": "Video Details",
    "method": "GET",
    "path": "/video/details",
    "parameters": {
      "type": "object",
      "properties": {
        "video_id": {
          "type": "string",
          "description": "video_id"
        }
      },
      "required": [
        "video_id"
      ]
    }
  },
  {
    "name": "agntdata_tiktok_Video_Details_post",
    "description": "Video Details",
    "method": "POST",
    "path": "/video/details",
    "parameters": {
      "type": "object",
      "properties": {
        "video_id": {
          "type": "string",
          "description": "video_id"
        }
      },
      "required": [
        "video_id"
      ]
    }
  },
  {
    "name": "agntdata_tiktok_User_s_Videos_get",
    "description": "User's Videos",
    "method": "GET",
    "path": "/user/videos",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_tiktok_User_s_Videos_post",
    "description": "User's Videos",
    "method": "POST",
    "path": "/user/videos",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_tiktok_Collection_Videos_Details",
    "description": "Collection Videos/Details",
    "method": "GET",
    "path": "/collection/",
    "parameters": {
      "type": "object",
      "properties": {
        "collection_id": {
          "type": "string",
          "description": "collection_id"
        },
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "collection_id",
        "username"
      ]
    }
  },
  {
    "name": "agntdata_tiktok_User_s_Videos_Continuation",
    "description": "User's Videos Continuation",
    "method": "GET",
    "path": "/user/videos/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "username": {
          "type": "string",
          "description": "username"
        },
        "secondary_id": {
          "type": "string",
          "description": "secondary_id"
        }
      },
      "required": [
        "continuation_token",
        "username",
        "secondary_id"
      ]
    }
  },
  {
    "name": "agntdata_tiktok_User_s_Details_get",
    "description": "User's Details",
    "method": "GET",
    "path": "/user/details",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_tiktok_User_s_Details_post",
    "description": "User's Details",
    "method": "POST",
    "path": "/user/details",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        }
      },
      "required": [
        "username"
      ]
    }
  },
  {
    "name": "agntdata_tiktok_Search_Accounts_get",
    "description": "Search Accounts",
    "method": "GET",
    "path": "/search/accounts/query",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "query"
        }
      },
      "required": [
        "query"
      ]
    }
  },
  {
    "name": "agntdata_tiktok_Search_Accounts_post",
    "description": "Search Accounts",
    "method": "POST",
    "path": "/search/accounts/query",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "query"
        }
      },
      "required": [
        "query"
      ]
    }
  },
  {
    "name": "agntdata_tiktok_Search_Videos_get",
    "description": "Search Videos",
    "method": "GET",
    "path": "/search/general/query",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "query"
        }
      },
      "required": [
        "query"
      ]
    }
  },
  {
    "name": "agntdata_tiktok_Search_Videos_post",
    "description": "Search Videos",
    "method": "POST",
    "path": "/search/general/query",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "query"
        }
      },
      "required": [
        "query"
      ]
    }
  }
]
```

## Example

```bash
curl -X GET "https://api.agntdata.dev/v1/data/tiktok/video/details?param=value" \
  -H "Authorization: Bearer $AGNTDATA_API_KEY"
```

## Links

- [Documentation](https://agnt.mintlify.app)
- [API Reference](https://agnt.mintlify.app/apis/social/tiktok)
- [Dashboard](https://app.agntdata.dev/dashboard)
