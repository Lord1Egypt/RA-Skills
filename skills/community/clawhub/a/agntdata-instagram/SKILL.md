---
name: instagram-data
description: "Instagram profiles, posts, reels, and hashtags for agents — influencer and brand research with no Instagram login, Business account, or Meta app."
version: 2.0.14
author: superagnt
license: MIT-0
platforms: [macos, linux, windows]
required_environment_variables:
  - SUPERAGNT_API_KEY
metadata:
  hermes:
    tags: [instagram-data, influencer-research, social-media]
  openclaw:
    requires:
      env:
        - SUPERAGNT_API_KEY
      bins:
        - curl
    primaryEnv: SUPERAGNT_API_KEY
    emoji: "⚡"
    homepage: https://superagnt.com/r/ch-instagram-data-docs
---

# Instagram Data

The superagnt Instagram API wraps Instagram surface areas into a single integration. Instead of managing multiple keys, proxies, and rate limits yourself, you call superagnt with one credential and consume structured JSON optimized for downstream AI and analytics. Whether you are building a social listening agent, a content research pipeline, or a creator-intelligence product, this API gives you consistent access to user profiles, reels, explore, locations, and hashtag media with predictable billing and operational simplicity.

## Alternative install: the scoped MCP server

If this client speaks MCP, you can connect the Instagram Data facet
server instead of using this skill's curl calls — the same endpoints below as
native MCP tools with structured parameters and OAuth sign-in, scoped to this
capability:

```
https://mcp.superagnt.com/mcp/instagram
```

That URL publishes full OAuth discovery: an MCP-capable client needs the URL
and nothing else (approve once in the browser). On clients that hold a bearer
instead, add it as an `Authorization: Bearer` header. Per-client setup lines:
https://www.superagnt.com/install?facet=instagram

This skill document stays fully usable on curl-only environments — everything
below works with just the API key.

## Authentication

Get an API key from the [superagnt app](https://superagnt.com/r/ch-instagram-data-key) and export it as
`SUPERAGNT_API_KEY`. Every request sends it as a Bearer token:

```
Authorization: Bearer $SUPERAGNT_API_KEY
```

If the variable is not set, ask the user for their key or point them at
https://superagnt.com/r/ch-instagram-data-key.

## Verify the install (do this first)

One call proves the key, the credit balance, and this source end to end:

```bash
curl -s https://api.superagnt.com/v1/credits \
  -H &#x27;Authorization: Bearer $SUPERAGNT_API_KEY&#x27;
```

A JSON result means you are live. A 401 means the key is wrong or missing; a
402 means the workspace is out of credits — the superagnt app shows both.

## Base URL

```
https://api.superagnt.com/v1/data/instagram
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

The following JSON defines every operation with its parameters. Each tool maps
to an API endpoint under the base URL.

```json
[
  {
    "name": "superagnt_instagram_Search_users_by_keyword",
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
    "name": "superagnt_instagram_Media_by_explore_section_ID",
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
    "name": "superagnt_instagram_Explore_sections_list",
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
    "name": "superagnt_instagram_Cities_by_country_code",
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
    "name": "superagnt_instagram_Media_by_location_ID",
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
    "name": "superagnt_instagram_Download_link_by_media_ID_or_URL",
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
    "name": "superagnt_instagram_Media_info_by_URL",
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
    "name": "superagnt_instagram_Related_profiles_by_user_ID",
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
    "name": "superagnt_instagram_Reels_by_user_ID",
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
    "name": "superagnt_instagram_Media_list__V2__by_user_ID",
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
    "name": "superagnt_instagram_Media_list_by_user_ID",
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
    "name": "superagnt_instagram_User_info__V2__by_username",
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
    "name": "superagnt_instagram_User_info_by_user_ID",
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
    "name": "superagnt_instagram_Media_shortcode_from_media_ID",
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
    "name": "superagnt_instagram_Username_from_user_ID",
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
    "name": "superagnt_instagram_Tagged_media_by_user_ID",
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
    "name": "superagnt_instagram_Reposts_by_user_ID",
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
    "name": "superagnt_instagram_Locations_by_city_ID",
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
    "name": "superagnt_instagram_Location_info_by_location_ID",
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
    "name": "superagnt_instagram_Web_profile_info_by_username",
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
    "name": "superagnt_instagram_Music_info_by_music_ID",
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
    "name": "superagnt_instagram_Media_by_hashtag",
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
curl -X GET &#x27;https://api.superagnt.com/v1/data/instagram&#x27; \
  -H &#x27;Authorization: Bearer $SUPERAGNT_API_KEY&#x27; \
  -H &#x27;Content-Type: application/json&#x27;
```

## Use Cases

- Social and creator intelligence agents using Instagram
- Marketing and research teams monitoring accounts and content
- Product teams building alerts, digests, and dashboards
- Developers prototyping LLM tools that need live network data
- Data teams joining Instagram signals with CRM or warehouse data

## Scope

This skill covers Instagram Data only — the endpoints listed above,
nothing else. The same API key also works with superagnt's other data sources
and platform tools, but those are separate listings that the user installs or
enables themselves; this skill does not add or enable anything beyond what is
documented here. The public catalog is at `https://api.superagnt.com/v1/platforms`.

## Links

- [Documentation](https://superagnt.com/r/ch-instagram-data-docs)
- [superagnt app / API keys](https://superagnt.com/r/ch-instagram-data-key)
- [This listing](https://clawhub.ai/superagnt/skills/instagram-data)
