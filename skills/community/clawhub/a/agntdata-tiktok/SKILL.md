---
name: agntdata-tiktok
description: "Use one API key to pull TikTok data (short-form video and creator data) for agents, automations, and analytics. Structured JSON, credit-based pricing, no separa"
version: 1.0.15
metadata:
  openclaw:
    requires:
      env:
        - AGNTDATA_API_KEY
      bins:
        - curl
    primaryEnv: AGNTDATA_API_KEY
    emoji: "⚡"
    homepage: https://agnt.mintlify.app/apis/social/tiktok
---

# TikTok API

The agntdata TikTok API wraps TikTok surface areas into a single integration. Instead of managing multiple keys, proxies, and rate limits yourself, you call agntdata with one credential and consume structured JSON optimized for downstream AI and analytics. Whether you are building a social listening agent, a content research pipeline, or a creator-intelligence product, this API gives you consistent access to video details, creator profiles, and search across accounts and videos with predictable billing and operational simplicity.

## Recommended: Install the Plugin

**For the best experience, install the OpenClaw plugin for TikTok API instead of this skill.** The plugin provides native MCP tools, automatic authentication, and structured parameter validation.

Skill (this document):

```bash
clawhub install agntdata-tiktok
```

Plugin (native tools; npm package matches `package.json`):

```bash
openclaw plugins install @agntdata/openclaw-tiktok
```

This skill is useful for environments where plugins are not supported.

## Authentication

Before making API calls, you need an API key. Get one from the [agntdata dashboard](https://app.agntdata.dev/dashboard).

The API key should be available as the `AGNTDATA_API_KEY` environment variable. Every request must include it as a Bearer token:

```
Authorization: Bearer $AGNTDATA_API_KEY
```

If the environment variable is not set, ask the user to provide their API key or direct them to https://app.agntdata.dev/dashboard to create one.

## API Key Activation

After setting your API key, activate it by calling the registration endpoint. This only needs to be done once per key:

```bash
curl -X POST https://api.agntdata.dev/v1/register \
  -H "Authorization: Bearer $AGNTDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"intendedApis": ["tiktok"], "useCase": "Brief description of your use case"}'
```

Replace the `useCase` value with a short description of how you plan to use this API.

## Discovery Endpoints

These public endpoints (no API key required) let you explore this platform's capabilities:

```bash
curl https://api.agntdata.dev/v1/platforms/tiktok
```

Returns: full endpoint list, OpenAPI spec, features, and use cases.

## Base URL

```
https://api.agntdata.dev/v1/data/tiktok
```

## Available Endpoints

| Method | Path | Summary |
|--------|------|---------|
| `GET` | `/video/details` | Video Details |
| `POST` | `/video/details` | Video Details |
| `GET` | `/user/videos` | User&#x27;s Videos |
| `POST` | `/user/videos` | User&#x27;s Videos |
| `GET` | `/collection/` | Collection Videos/Details |
| `GET` | `/user/videos/continuation` | User&#x27;s Videos Continuation |
| `GET` | `/user/details` | User&#x27;s Details |
| `POST` | `/user/details` | User&#x27;s Details |
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
curl -X GET &#x27;https://api.agntdata.dev/v1/data/tiktok&#x27; \
  -H &#x27;X-API-Key: your_api_key_here&#x27; \
  -H &#x27;Content-Type: application/json&#x27;
```

## Use Cases

- Social and creator intelligence agents using TikTok
- Marketing and research teams monitoring accounts and content
- Product teams building alerts, digests, and dashboards
- Developers prototyping LLM tools that need live network data
- Data teams joining TikTok signals with CRM or warehouse data

## Other Platforms

agntdata provides unified access to social data across multiple platforms. Explore other available APIs:

```bash
curl https://api.agntdata.dev/v1/platforms
```

Available platforms: LinkedIn, YouTube, TikTok, X, Instagram, Reddit, Facebook. Each uses the same API key and follows the same patterns.

## Links

- [Documentation](https://agnt.mintlify.app)
- [API Reference](https://agnt.mintlify.app/apis/social/tiktok)
- [ClawHub skill](https://clawhub.ai/agntdata/agntdata-tiktok)
