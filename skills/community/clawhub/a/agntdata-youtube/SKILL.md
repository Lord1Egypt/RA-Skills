---
name: agntdata-youtube
description: "Use one API key to pull YouTube data (channels, videos, search, and trends) for agents, automations, and analytics. Structured JSON, credit-based pricing, no se"
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
    homepage: https://agnt.mintlify.app/apis/social/youtube
---

# YouTube API

The agntdata YouTube API wraps YouTube surface areas into a single integration. Instead of managing multiple keys, proxies, and rate limits yourself, you call agntdata with one credential and consume structured JSON optimized for downstream AI and analytics. Whether you are building a social listening agent, a content research pipeline, or a creator-intelligence product, this API gives you consistent access to video metadata, channel discovery, comments, subtitles, and recommendations with predictable billing and operational simplicity.

## Recommended: Install the Plugin

**For the best experience, install the OpenClaw plugin for YouTube API instead of this skill.** The plugin provides native MCP tools, automatic authentication, and structured parameter validation.

Skill (this document):

```bash
clawhub install agntdata-youtube
```

Plugin (native tools; npm package matches `package.json`):

```bash
openclaw plugins install @agntdata/openclaw-youtube
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
  -d '{"intendedApis": ["youtube"], "useCase": "Brief description of your use case"}'
```

Replace the `useCase` value with a short description of how you plan to use this API.

## Discovery Endpoints

These public endpoints (no API key required) let you explore this platform's capabilities:

```bash
curl https://api.agntdata.dev/v1/platforms/youtube
```

Returns: full endpoint list, OpenAPI spec, features, and use cases.

## Base URL

```
https://api.agntdata.dev/v1/data/youtube
```

## Available Endpoints

| Method | Path | Summary |
|--------|------|---------|
| `GET` | `/video/screenshot` | Video Screenshot |
| `GET` | `/channel/search/continuation` | Channel Search Continuation |
| `GET` | `/channel/search` | Channel Search |
| `GET` | `/channel/shorts` | Channel Shorts |
| `GET` | `/channel/videos/continuation` | Channel Videos Continuation |
| `GET` | `/channel/details` | Channel Details |
| `GET` | `/channel/id` | Youtube Channel ID |
| `GET` | `/channel/videos` | Channel Videos |
| `POST` | `/channel/videos` | POST Channel Videos |
| `GET` | `/audio/videos/continuation` | Audio Videos Continuation |
| `GET` | `/audio/videos` | Audio Videos |
| `GET` | `/audio/details` | Audio Details |
| `GET` | `/video/recommendations/continuation` | Video Recommendation Continuation |
| `GET` | `/video/recommendations` | Video Recommendation |
| `GET` | `/video/comments` | Video Comments |
| `GET` | `/video/subtitles` | Video Subtitles |
| `GET` | `/video/details` | Video Details |
| `GET` | `/video/data` | Video Data |
| `GET` | `/search/continuation` | Youtube Search Continuation |
| `GET` | `/search/` | Youtube Search |
| `GET` | `/trending/` | Trending Videos |
| `GET` | `/video/comments/continuation` | Video Comments Continuation |

## Tool Schemas

The following JSON defines all available tools with their parameters. Each tool maps to an API endpoint.

```json
[
  {
    "name": "agntdata_youtube_Video_Screenshot",
    "description": "Video Screenshot",
    "method": "GET",
    "path": "/video/screenshot",
    "parameters": {
      "type": "object",
      "properties": {
        "video_id": {
          "type": "string",
          "description": "video_id"
        },
        "timestamp_s": {
          "type": "number",
          "description": "timestamp_s"
        }
      },
      "required": [
        "video_id",
        "timestamp_s"
      ]
    }
  },
  {
    "name": "agntdata_youtube_Channel_Search_Continuation",
    "description": "Channel Search Continuation",
    "method": "GET",
    "path": "/channel/search/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "lang": {
          "type": "string",
          "description": "lang"
        },
        "country": {
          "type": "string",
          "description": "country"
        },
        "query": {
          "type": "string",
          "description": "query"
        },
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "channel_id": {
          "type": "string",
          "description": "channel_id"
        }
      },
      "required": [
        "query",
        "continuation_token",
        "channel_id"
      ]
    }
  },
  {
    "name": "agntdata_youtube_Channel_Search",
    "description": "Channel Search",
    "method": "GET",
    "path": "/channel/search",
    "parameters": {
      "type": "object",
      "properties": {
        "lang": {
          "type": "string",
          "description": "lang"
        },
        "query": {
          "type": "string",
          "description": "query"
        },
        "channel_id": {
          "type": "string",
          "description": "channel_id"
        },
        "country": {
          "type": "string",
          "description": "country"
        }
      },
      "required": [
        "query",
        "channel_id"
      ]
    }
  },
  {
    "name": "agntdata_youtube_Channel_Shorts",
    "description": "Channel Shorts",
    "method": "GET",
    "path": "/channel/shorts",
    "parameters": {
      "type": "object",
      "properties": {
        "channel_id": {
          "type": "string",
          "description": "channel_id"
        }
      },
      "required": [
        "channel_id"
      ]
    }
  },
  {
    "name": "agntdata_youtube_Channel_Videos_Continuation",
    "description": "Channel Videos Continuation",
    "method": "GET",
    "path": "/channel/videos/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "channel_id": {
          "type": "string",
          "description": "channel_id"
        }
      },
      "required": [
        "continuation_token",
        "channel_id"
      ]
    }
  },
  {
    "name": "agntdata_youtube_Channel_Details",
    "description": "Channel Details",
    "method": "GET",
    "path": "/channel/details",
    "parameters": {
      "type": "object",
      "properties": {
        "channel_id": {
          "type": "string",
          "description": "channel_id"
        }
      },
      "required": [
        "channel_id"
      ]
    }
  },
  {
    "name": "agntdata_youtube_Youtube_Channel_ID",
    "description": "Youtube Channel ID",
    "method": "GET",
    "path": "/channel/id",
    "parameters": {
      "type": "object",
      "properties": {
        "channel_name": {
          "type": "string",
          "description": "channel_name"
        }
      },
      "required": [
        "channel_name"
      ]
    }
  },
  {
    "name": "agntdata_youtube_Channel_Videos",
    "description": "Channel Videos",
    "method": "GET",
    "path": "/channel/videos",
    "parameters": {
      "type": "object",
      "properties": {
        "channel_id": {
          "type": "string",
          "description": "channel_id"
        }
      },
      "required": [
        "channel_id"
      ]
    }
  },
  {
    "name": "agntdata_youtube_POST_Channel_Videos",
    "description": "POST Channel Videos",
    "method": "POST",
    "path": "/channel/videos",
    "parameters": {
      "type": "object",
      "properties": {
        "channel_id": {
          "type": "string",
          "description": "channel_id"
        },
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        }
      }
    }
  },
  {
    "name": "agntdata_youtube_Audio_Videos_Continuation",
    "description": "Audio Videos Continuation",
    "method": "GET",
    "path": "/audio/videos/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "audio_id": {
          "type": "string",
          "description": "audio_id"
        }
      },
      "required": [
        "continuation_token",
        "audio_id"
      ]
    }
  },
  {
    "name": "agntdata_youtube_Audio_Videos",
    "description": "Audio Videos",
    "method": "GET",
    "path": "/audio/videos",
    "parameters": {
      "type": "object",
      "properties": {
        "audio_id": {
          "type": "string",
          "description": "audio_id"
        }
      },
      "required": [
        "audio_id"
      ]
    }
  },
  {
    "name": "agntdata_youtube_Audio_Details",
    "description": "Audio Details",
    "method": "GET",
    "path": "/audio/details",
    "parameters": {
      "type": "object",
      "properties": {
        "audio_id": {
          "type": "string",
          "description": "audio_id"
        }
      },
      "required": [
        "audio_id"
      ]
    }
  },
  {
    "name": "agntdata_youtube_Video_Recommendation_Continuation",
    "description": "Video Recommendation Continuation",
    "method": "GET",
    "path": "/video/recommendations/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "video_id": {
          "type": "string",
          "description": "video_id"
        }
      },
      "required": [
        "continuation_token",
        "video_id"
      ]
    }
  },
  {
    "name": "agntdata_youtube_Video_Recommendation",
    "description": "Video Recommendation",
    "method": "GET",
    "path": "/video/recommendations",
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
    "name": "agntdata_youtube_Video_Comments",
    "description": "Video Comments",
    "method": "GET",
    "path": "/video/comments",
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
    "name": "agntdata_youtube_Video_Subtitles",
    "description": "Video Subtitles",
    "method": "GET",
    "path": "/video/subtitles",
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
    "name": "agntdata_youtube_Video_Details",
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
    "name": "agntdata_youtube_Video_Data",
    "description": "Video Data",
    "method": "GET",
    "path": "/video/data",
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
    "name": "agntdata_youtube_Youtube_Search_Continuation",
    "description": "Youtube Search Continuation",
    "method": "GET",
    "path": "/search/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "query": {
          "type": "string",
          "description": "query"
        },
        "lang": {
          "type": "string",
          "description": "lang"
        },
        "country": {
          "type": "string",
          "description": "country"
        },
        "order_by": {
          "type": "string",
          "description": "Possible values: \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"last_hour\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"today\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"this_week\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"this_month\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"this_year\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\""
        }
      },
      "required": [
        "continuation_token",
        "query"
      ]
    }
  },
  {
    "name": "agntdata_youtube_Youtube_Search",
    "description": "Youtube Search",
    "method": "GET",
    "path": "/search/",
    "parameters": {
      "type": "object",
      "properties": {
        "lang": {
          "type": "string",
          "description": "lang"
        },
        "query": {
          "type": "string",
          "description": "query"
        },
        "order_by": {
          "type": "string",
          "description": "Possible values: \\\\\\\\\\\\\\\"last_hour\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\"today\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\"this_week\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\"this_month\\\\\\\\\\\\\\\", \\\\\\\\\\\\\\\"this_year\\\\\\\\\\\\\\\""
        },
        "country": {
          "type": "string",
          "description": "country"
        }
      },
      "required": [
        "query"
      ]
    }
  },
  {
    "name": "agntdata_youtube_Trending_Videos",
    "description": "Trending Videos",
    "method": "GET",
    "path": "/trending/",
    "parameters": {
      "type": "object",
      "properties": {
        "country": {
          "type": "string",
          "description": "country"
        },
        "lang": {
          "type": "string",
          "description": "lang"
        },
        "section": {
          "type": "string",
          "description": "Possible values: \\\\\\\"Now\\\\\\\", \\\\\\\"Music\\\\\\\", \\\\\\\"Movies\\\\\\\", \\\\\\\"Gaming\\\\\\\""
        }
      }
    }
  },
  {
    "name": "agntdata_youtube_Video_Comments_Continuation",
    "description": "Video Comments Continuation",
    "method": "GET",
    "path": "/video/comments/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "video_id": {
          "type": "string",
          "description": "video_id"
        }
      },
      "required": [
        "continuation_token",
        "video_id"
      ]
    }
  },
  {
    "name": "agntdata_youtube_Get_Channel_Email_By_URL",
    "description": "Get Channel Email by URL",
    "method": "POST",
    "path": "/channel/email",
    "parameters": {
      "type": "object",
      "properties": {
        "url": {
          "type": "string",
          "description": "Full YouTube channel URL (e.g. https://www.youtube.com/@theAIsearch)."
        }
      },
      "required": [
        "url"
      ]
    }
  },
  {
    "name": "agntdata_youtube_Get_Channel_Email_By_Id",
    "description": "Get Channel Email by Channel ID",
    "method": "GET",
    "path": "/channel/{channel_id}/email",
    "parameters": {
      "type": "object",
      "properties": {
        "channel_id": {
          "type": "string",
          "description": "channel_id"
        }
      },
      "required": [
        "channel_id"
      ]
    }
  }
]
```

## Example

```bash
curl -X GET &#x27;https://api.agntdata.dev/v1/data/youtube&#x27; \
  -H &#x27;X-API-Key: your_api_key_here&#x27; \
  -H &#x27;Content-Type: application/json&#x27;
```

## Use Cases

- Social and creator intelligence agents using YouTube
- Marketing and research teams monitoring accounts and content
- Product teams building alerts, digests, and dashboards
- Developers prototyping LLM tools that need live network data
- Data teams joining YouTube signals with CRM or warehouse data

## Other Platforms

agntdata provides unified access to social data across multiple platforms. Explore other available APIs:

```bash
curl https://api.agntdata.dev/v1/platforms
```

Available platforms: LinkedIn, YouTube, TikTok, X, Instagram, Reddit, Facebook. Each uses the same API key and follows the same patterns.

## Links

- [Documentation](https://agnt.mintlify.app)
- [API Reference](https://agnt.mintlify.app/apis/social/youtube)
- [ClawHub skill](https://clawhub.ai/agntdata/agntdata-youtube)
