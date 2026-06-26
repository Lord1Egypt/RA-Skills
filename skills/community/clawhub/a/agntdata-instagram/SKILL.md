---
name: agntdata-instagram
description: "Use one API key to pull Instagram data (profiles, media, and discovery) for agents, automations, and analytics. Structured JSON, credit-based pricing, no separa"
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
    homepage: https://agnt.mintlify.app/apis/social/instagram
---

# Instagram API

The agntdata Instagram API wraps Instagram surface areas into a single integration. Instead of managing multiple keys, proxies, and rate limits yourself, you call agntdata with one credential and consume structured JSON optimized for downstream AI and analytics. Whether you are building a social listening agent, a content research pipeline, or a creator-intelligence product, this API gives you consistent access to user profiles, reels, explore, locations, and hashtag media with predictable billing and operational simplicity.

## Recommended: Install the Plugin

**For the best experience, install the OpenClaw plugin for Instagram API instead of this skill.** The plugin provides native MCP tools, automatic authentication, and structured parameter validation.

Skill (this document):

```bash
clawhub install agntdata-instagram
```

Plugin (native tools; npm package matches `package.json`):

```bash
openclaw plugins install @agntdata/openclaw-instagram
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
  -d '{"intendedApis": ["instagram"], "useCase": "Brief description of your use case"}'
```

Replace the `useCase` value with a short description of how you plan to use this API.

## Discovery Endpoints

These public endpoints (no API key required) let you explore this platform's capabilities:

```bash
curl https://api.agntdata.dev/v1/platforms/instagram
```

Returns: full endpoint list, OpenAPI spec, features, and use cases.

## Base URL

```
https://api.agntdata.dev/v1/data/instagram
```

## Available Endpoints

| Method | Path | Summary |
|--------|------|---------|
| `GET` | `/search` | Search users by keyword |
| `GET` | `/section` | Media by explore section ID |
| `GET` | `/sections` | Explore sections list |
| `GET` | `/cities` | Cities by country code |
| `GET` | `/location-feeds` | Media by location ID |
| `GET` | `/post-dl` | Download link by media ID or URL |
| `GET` | `/post` | Media info by URL |
| `GET` | `/related-profiles` | Related profiles by user ID |
| `GET` | `/reels` | Reels by user ID |
| `GET` | `/user-feeds2` | Media list (V2) by user ID |
| `GET` | `/user-feeds` | Media list by user ID |
| `GET` | `/profile2` | User info (V2) by username |
| `GET` | `/profile` | User info by user ID |
| `GET` | `/id-media` | Media shortcode from media ID |
| `GET` | `/id` | Username from user ID |
| `GET` | `/user-tags` | Tagged media by user ID |
| `GET` | `/user-reposts` | Reposts by user ID |
| `GET` | `/locations` | Locations by city ID |
| `GET` | `/location-info` | Location info by location ID |
| `GET` | `/web-profile` | Web profile info by username |
| `GET` | `/music` | Music info by music ID |
| `GET` | `/tag-feeds` | Media by hashtag |

## Tool Schemas

The following JSON defines all available tools with their parameters. Each tool maps to an API endpoint.

```json
[
  {
    "name": "agntdata_instagram_Search_users_by_keyword",
    "description": "Search users by keyword",
    "method": "GET",
    "path": "/search",
    "parameters": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
        "select": {
          "type": "string",
          "description": "select"
        },
        "query": {
          "type": "string",
          "description": "query"
        }
      },
      "required": [
        "select",
        "query"
      ]
    }
  },
  {
    "name": "agntdata_instagram_Media_by_explore_section_ID",
    "description": "Media by explore section ID",
    "method": "GET",
    "path": "/section",
    "parameters": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
        "max_id": {
          "type": "number",
          "description": "max_id"
        },
        "count": {
          "type": "number",
          "description": "count"
        },
        "id": {
          "type": "string",
          "description": "id"
        }
      },
      "required": [
        "count",
        "id"
      ]
    }
  },
  {
    "name": "agntdata_instagram_Explore_sections_list",
    "description": "Explore sections list",
    "method": "GET",
    "path": "/sections",
    "parameters": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        }
      }
    }
  },
  {
    "name": "agntdata_instagram_Cities_by_country_code",
    "description": "Cities by country code",
    "method": "GET",
    "path": "/cities",
    "parameters": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
        "country_code": {
          "type": "string",
          "description": "country_code"
        },
        "page": {
          "type": "number",
          "description": "page"
        }
      },
      "required": [
        "country_code"
      ]
    }
  },
  {
    "name": "agntdata_instagram_Media_by_location_ID",
    "description": "Media by location ID",
    "method": "GET",
    "path": "/location-feeds",
    "parameters": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
        "tab": {
          "type": "string",
          "description": "tab"
        },
        "id": {
          "type": "string",
          "description": "id"
        },
        "end_cursor": {
          "type": "string",
          "description": "end_cursor"
        }
      },
      "required": [
        "tab",
        "id"
      ]
    }
  },
  {
    "name": "agntdata_instagram_Download_link_by_media_ID_or_URL",
    "description": "Download link by media ID or URL",
    "method": "GET",
    "path": "/post-dl",
    "parameters": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
        "url": {
          "type": "string",
          "description": "url"
        }
      },
      "required": [
        "url"
      ]
    }
  },
  {
    "name": "agntdata_instagram_Media_info_by_URL",
    "description": "Media info by URL",
    "method": "GET",
    "path": "/post",
    "parameters": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
        "url": {
          "type": "string",
          "description": "url"
        }
      },
      "required": [
        "url"
      ]
    }
  },
  {
    "name": "agntdata_instagram_Related_profiles_by_user_ID",
    "description": "Related profiles by user ID",
    "method": "GET",
    "path": "/related-profiles",
    "parameters": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
        "id": {
          "type": "number",
          "description": "id"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "agntdata_instagram_Reels_by_user_ID",
    "description": "Reels by user ID",
    "method": "GET",
    "path": "/reels",
    "parameters": {
      "type": "object",
      "properties": {
        "max_id": {
          "type": "string",
          "description": "max_id"
        },
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
        "count": {
          "type": "number",
          "description": "count"
        },
        "id": {
          "type": "number",
          "description": "id"
        }
      },
      "required": [
        "count",
        "id"
      ]
    }
  },
  {
    "name": "agntdata_instagram_Media_list__V2__by_user_ID",
    "description": "Media list (V2) by user ID",
    "method": "GET",
    "path": "/user-feeds2",
    "parameters": {
      "type": "object",
      "properties": {
        "end_cursor": {
          "type": "string",
          "description": "end_cursor"
        },
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
        "count": {
          "type": "number",
          "description": "count"
        },
        "id": {
          "type": "number",
          "description": "id"
        }
      },
      "required": [
        "count",
        "id"
      ]
    }
  },
  {
    "name": "agntdata_instagram_Media_list_by_user_ID",
    "description": "Media list by user ID",
    "method": "GET",
    "path": "/user-feeds",
    "parameters": {
      "type": "object",
      "properties": {
        "count": {
          "type": "number",
          "description": "count"
        },
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
        "max_id": {
          "type": "string",
          "description": "max_id"
        },
        "allow_restricted_media": {
          "type": "boolean",
          "description": "allow_restricted_media"
        },
        "id": {
          "type": "number",
          "description": "id"
        }
      },
      "required": [
        "count",
        "id"
      ]
    }
  },
  {
    "name": "agntdata_instagram_User_info__V2__by_username",
    "description": "User info (V2) by username",
    "method": "GET",
    "path": "/profile2",
    "parameters": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
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
    "name": "agntdata_instagram_User_info_by_user_ID",
    "description": "User info by user ID",
    "method": "GET",
    "path": "/profile",
    "parameters": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
        "id": {
          "type": "number",
          "description": "id"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "agntdata_instagram_Media_shortcode_from_media_ID",
    "description": "Media shortcode from media ID",
    "method": "GET",
    "path": "/id-media",
    "parameters": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
        "id": {
          "type": "string",
          "description": "id"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "agntdata_instagram_Username_from_user_ID",
    "description": "Username from user ID",
    "method": "GET",
    "path": "/id",
    "parameters": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
        "id": {
          "type": "number",
          "description": "id"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "agntdata_instagram_Tagged_media_by_user_ID",
    "description": "Tagged media by user ID",
    "method": "GET",
    "path": "/user-tags",
    "parameters": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
        "count": {
          "type": "number",
          "description": "count"
        },
        "end_cursor": {
          "type": "string",
          "description": "end_cursor"
        },
        "id": {
          "type": "number",
          "description": "id"
        }
      },
      "required": [
        "count",
        "id"
      ]
    }
  },
  {
    "name": "agntdata_instagram_Reposts_by_user_ID",
    "description": "Reposts by user ID",
    "method": "GET",
    "path": "/user-reposts",
    "parameters": {
      "type": "object",
      "properties": {
        "max_id": {
          "type": "string",
          "description": "max_id"
        },
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
        "id": {
          "type": "number",
          "description": "id"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "agntdata_instagram_Locations_by_city_ID",
    "description": "Locations by city ID",
    "method": "GET",
    "path": "/locations",
    "parameters": {
      "type": "object",
      "properties": {
        "page": {
          "type": "number",
          "description": "page"
        },
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
        "city_id": {
          "type": "string",
          "description": "city_id"
        }
      },
      "required": [
        "city_id"
      ]
    }
  },
  {
    "name": "agntdata_instagram_Location_info_by_location_ID",
    "description": "Location info by location ID",
    "method": "GET",
    "path": "/location-info",
    "parameters": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
        "id": {
          "type": "number",
          "description": "id"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "agntdata_instagram_Web_profile_info_by_username",
    "description": "Web profile info by username",
    "method": "GET",
    "path": "/web-profile",
    "parameters": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
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
    "name": "agntdata_instagram_Music_info_by_music_ID",
    "description": "Music info by music ID",
    "method": "GET",
    "path": "/music",
    "parameters": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
        "max_id": {
          "type": "string",
          "description": "max_id"
        },
        "id": {
          "type": "number",
          "description": "id"
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "agntdata_instagram_Media_by_hashtag",
    "description": "Media by hashtag",
    "method": "GET",
    "path": "/tag-feeds",
    "parameters": {
      "type": "object",
      "properties": {
        "end_cursor": {
          "type": "string",
          "description": "end_cursor"
        },
        "fields": {
          "type": "string",
          "description": "Use the `fields` parameter to reduce bandwidth consumption and minimize response size by returning only the necessary data."
        },
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
curl -X GET &#x27;https://api.agntdata.dev/v1/data/instagram&#x27; \
  -H &#x27;X-API-Key: your_api_key_here&#x27; \
  -H &#x27;Content-Type: application/json&#x27;
```

## Use Cases

- Social and creator intelligence agents using Instagram
- Marketing and research teams monitoring accounts and content
- Product teams building alerts, digests, and dashboards
- Developers prototyping LLM tools that need live network data
- Data teams joining Instagram signals with CRM or warehouse data

## Other Platforms

agntdata provides unified access to social data across multiple platforms. Explore other available APIs:

```bash
curl https://api.agntdata.dev/v1/platforms
```

Available platforms: LinkedIn, YouTube, TikTok, X, Instagram, Reddit, Facebook. Each uses the same API key and follows the same patterns.

## Links

- [Documentation](https://agnt.mintlify.app)
- [API Reference](https://agnt.mintlify.app/apis/social/instagram)
- [ClawHub skill](https://clawhub.ai/agntdata/agntdata-instagram)
