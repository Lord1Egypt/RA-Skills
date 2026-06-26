# YouTube API Reference

**App name:** `youtube`
**Base URL:** `https://api.agntdata.dev/v1/data/youtube`
**Endpoints:** 24

Unified access to video metadata, channel discovery, comments, subtitles, and recommendations. Built for LLMs and automation — not one-off scraping.

## Authentication

All requests require the agntdata API key:

```
Authorization: Bearer $AGNTDATA_API_KEY
```

---

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
| `POST` | `/channel/email` | Get Channel Email by URL |
| `GET` | `/channel/{channel_id}/email` | Get Channel Email by Channel ID |

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
curl -X GET "https://api.agntdata.dev/v1/data/youtube/video/screenshot?param=value" \
  -H "Authorization: Bearer $AGNTDATA_API_KEY"
```

## Links

- [Documentation](https://agnt.mintlify.app)
- [API Reference](https://agnt.mintlify.app/apis/social/youtube)
- [Dashboard](https://app.agntdata.dev/dashboard)
