---
name: agntdata-reddit
description: "Use one API key to pull Reddit data (subreddits, posts, and community data) for agents, automations, and analytics. Structured JSON, credit-based pricing, no se"
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
    homepage: https://agnt.mintlify.app/apis/social/reddit
---

# Reddit API

The agntdata Reddit API wraps Reddit surface areas into a single integration. Instead of managing multiple keys, proxies, and rate limits yourself, you call agntdata with one credential and consume structured JSON optimized for downstream AI and analytics. Whether you are building a social listening agent, a content research pipeline, or a creator-intelligence product, this API gives you consistent access to subreddit metadata, post threads, user activity, and search with predictable billing and operational simplicity.

## Recommended: Install the Plugin

**For the best experience, install the OpenClaw plugin for Reddit API instead of this skill.** The plugin provides native MCP tools, automatic authentication, and structured parameter validation.

Skill (this document):

```bash
clawhub install agntdata-reddit
```

Plugin (native tools; npm package matches `package.json`):

```bash
openclaw plugins install @agntdata/openclaw-reddit
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
  -d '{"intendedApis": ["reddit"], "useCase": "Brief description of your use case"}'
```

Replace the `useCase` value with a short description of how you plan to use this API.

## Discovery Endpoints

These public endpoints (no API key required) let you explore this platform's capabilities:

```bash
curl https://api.agntdata.dev/v1/platforms/reddit
```

Returns: full endpoint list, OpenAPI spec, features, and use cases.

## Base URL

```
https://api.agntdata.dev/v1/data/reddit
```

## Available Endpoints

| Method | Path | Summary |
|--------|------|---------|
| `GET` | `/getSimilarSubreddits` | Similar Subreddits |
| `GET` | `/getPostDuplicates` | Post Duplicates |
| `GET` | `/getSubredditModerators` | Subreddit Moderators |
| `GET` | `/getSubredditRules` | Subreddit Rules |
| `GET` | `/getUserOverview` | User Overview |
| `GET` | `/getSearchUsers` | Search Users |
| `GET` | `/getBestPopularPosts` | Best Popular Posts |
| `GET` | `/getControversialPostsBySubreddit` | Controversial Posts By Subreddit |
| `GET` | `/getUserPostRankInSubreddit` | User Post Rank In Subreddit |
| `GET` | `/getSubredditInfo` | Subreddit Info |
| `GET` | `/getCommentsBySubreddit` | Comments By Subreddit |
| `GET` | `/getPostCommentsWithSort` | Post Comments With Sort |
| `GET` | `/getProfile` | Profile |
| `GET` | `/getPostComments` | Post Comments |
| `GET` | `/getUserStats` | User Stats |
| `GET` | `/getSearchPosts` | Search Posts |
| `GET` | `/getSearchSubreddits` | Search Subreddits |
| `GET` | `/getNewSubreddits` | New Subreddits |
| `GET` | `/getPopularSubreddits` | Popular Subreddits |
| `GET` | `/getPostDetails` | Post Details |
| `GET` | `/getPostsBySubreddit` | Posts By Subreddit |
| `GET` | `/getTopCommentsByUsername` | Top Comments By Username |
| `GET` | `/getPopularPosts` | Popular Posts |
| `GET` | `/getTopPostsBySubreddit` | Top Posts By Subreddit |
| `GET` | `/getCommentsByUsername` | Comments By Username |
| `GET` | `/getTopPostsByUsername` | Top Posts By Username |
| `GET` | `/getPostsByUsername` | Posts By Username |
| `GET` | `/getRisingPopularPosts` | Rising Popular Posts |
| `GET` | `/getTopPopularPosts` | Top Popular Posts |

## Tool Schemas

The following JSON defines all available tools with their parameters. Each tool maps to an API endpoint.

```json
[
  {
    "name": "agntdata_reddit_Similar_Subreddits",
    "description": "Similar Subreddits",
    "method": "GET",
    "path": "/getSimilarSubreddits",
    "parameters": {
      "type": "object",
      "properties": {
        "cursor": {
          "type": "string",
          "description": "Pagination cursor from previous response"
        },
        "subreddit": {
          "type": "string",
          "description": "Name of the subreddit (e.g. python)"
        }
      },
      "required": [
        "subreddit"
      ]
    }
  },
  {
    "name": "agntdata_reddit_Post_Duplicates",
    "description": "Post Duplicates",
    "method": "GET",
    "path": "/getPostDuplicates",
    "parameters": {
      "type": "object",
      "properties": {
        "cursor": {
          "type": "string",
          "description": "Pagination cursor from previous response"
        },
        "post_url": {
          "type": "string",
          "description": "Full Reddit post URL (e.g."
        }
      },
      "required": [
        "post_url"
      ]
    }
  },
  {
    "name": "agntdata_reddit_Subreddit_Moderators",
    "description": "Subreddit Moderators",
    "method": "GET",
    "path": "/getSubredditModerators",
    "parameters": {
      "type": "object",
      "properties": {
        "subreddit": {
          "type": "string",
          "description": "Name of the subreddit (e.g. askreddit)"
        }
      },
      "required": [
        "subreddit"
      ]
    }
  },
  {
    "name": "agntdata_reddit_Subreddit_Rules",
    "description": "Subreddit Rules",
    "method": "GET",
    "path": "/getSubredditRules",
    "parameters": {
      "type": "object",
      "properties": {
        "subreddit": {
          "type": "string",
          "description": "Name of the subreddit (e.g. askreddit)"
        }
      },
      "required": [
        "subreddit"
      ]
    }
  },
  {
    "name": "agntdata_reddit_User_Overview",
    "description": "User Overview",
    "method": "GET",
    "path": "/getUserOverview",
    "parameters": {
      "type": "object",
      "properties": {
        "sort": {
          "type": "string",
          "description": "Sort order: hot, new, top, controversial"
        },
        "time": {
          "type": "string",
          "description": "Required when sort is top or controversial: hour, day, week, month, year, all"
        },
        "cursor": {
          "type": "string",
          "description": "Pagination cursor from previous response"
        },
        "username": {
          "type": "string",
          "description": "Reddit username (e.g. spez)"
        }
      },
      "required": [
        "sort",
        "username"
      ]
    }
  },
  {
    "name": "agntdata_reddit_Search_Users",
    "description": "Search Users",
    "method": "GET",
    "path": "/getSearchUsers",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "Search keyword (e.g. spez)"
        },
        "cursor": {
          "type": "string",
          "description": "Pagination cursor from previous response"
        }
      },
      "required": [
        "query"
      ]
    }
  },
  {
    "name": "agntdata_reddit_Best_Popular_Posts",
    "description": "Best Popular Posts",
    "method": "GET",
    "path": "/getBestPopularPosts",
    "parameters": {
      "type": "object",
      "properties": {
        "cursor": {
          "type": "string",
          "description": "Pagination cursor from previous response"
        }
      }
    }
  },
  {
    "name": "agntdata_reddit_Controversial_Posts_By_Subreddit",
    "description": "Controversial Posts By Subreddit",
    "method": "GET",
    "path": "/getControversialPostsBySubreddit",
    "parameters": {
      "type": "object",
      "properties": {
        "cursor": {
          "type": "string",
          "description": "Pagination cursor from previous response"
        },
        "subreddit": {
          "type": "string",
          "description": "Name of the subreddit (e.g. askreddit)"
        },
        "time": {
          "type": "string",
          "description": "Time filter: hour, day, week, month, year, all"
        }
      },
      "required": [
        "subreddit",
        "time"
      ]
    }
  },
  {
    "name": "agntdata_reddit_User_Post_Rank_In_Subreddit",
    "description": "User Post Rank In Subreddit",
    "method": "GET",
    "path": "/getUserPostRankInSubreddit",
    "parameters": {
      "type": "object",
      "properties": {
        "sort": {
          "type": "string",
          "description": "Sort order: hot, new, rising, top"
        },
        "username": {
          "type": "string",
          "description": "Reddit username (e.g. spez)"
        },
        "time": {
          "type": "string",
          "description": "Required when sort is top: hour, day, week, month, year, all"
        },
        "subreddit": {
          "type": "string",
          "description": "Name of the subreddit (e.g. reddit)"
        },
        "max_pages": {
          "type": "number",
          "description": "Maximum pages to scan (1-10, default: 4)"
        }
      },
      "required": [
        "sort",
        "username",
        "subreddit"
      ]
    }
  },
  {
    "name": "agntdata_reddit_Subreddit_Info",
    "description": "Subreddit Info",
    "method": "GET",
    "path": "/getSubredditInfo",
    "parameters": {
      "type": "object",
      "properties": {
        "subreddit": {
          "type": "string",
          "description": "subreddit"
        }
      },
      "required": [
        "subreddit"
      ]
    }
  },
  {
    "name": "agntdata_reddit_Comments_By_Subreddit",
    "description": "Comments By Subreddit",
    "method": "GET",
    "path": "/getCommentsBySubreddit",
    "parameters": {
      "type": "object",
      "properties": {
        "subreddit": {
          "type": "string",
          "description": "subreddit"
        },
        "cursor": {
          "type": "string",
          "description": "cursor"
        }
      },
      "required": [
        "subreddit"
      ]
    }
  },
  {
    "name": "agntdata_reddit_Post_Comments_With_Sort",
    "description": "Post Comments With Sort",
    "method": "GET",
    "path": "/getPostCommentsWithSort",
    "parameters": {
      "type": "object",
      "properties": {
        "sort": {
          "type": "string",
          "description": "Valid options are: confidence, top, new, controversial, old, qa"
        },
        "cursor": {
          "type": "string",
          "description": "cursor"
        },
        "post_url": {
          "type": "string",
          "description": "post_url"
        }
      },
      "required": [
        "sort",
        "post_url"
      ]
    }
  },
  {
    "name": "agntdata_reddit_Profile",
    "description": "Profile",
    "method": "GET",
    "path": "/getProfile",
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
    "name": "agntdata_reddit_Post_Comments",
    "description": "Post Comments",
    "method": "GET",
    "path": "/getPostComments",
    "parameters": {
      "type": "object",
      "properties": {
        "post_url": {
          "type": "string",
          "description": "post_url"
        }
      },
      "required": [
        "post_url"
      ]
    }
  },
  {
    "name": "agntdata_reddit_User_Stats",
    "description": "User Stats",
    "method": "GET",
    "path": "/getUserStats",
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
    "name": "agntdata_reddit_Search_Posts",
    "description": "Search Posts",
    "method": "GET",
    "path": "/getSearchPosts",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "query"
        },
        "cursor": {
          "type": "string",
          "description": "cursor"
        },
        "sort": {
          "type": "string",
          "description": "you can just select one item from below:\n`relevance`\n`hot`\n`top`\n`new`\n`comments`"
        },
        "subreddit": {
          "type": "string",
          "description": "subreddit"
        },
        "time": {
          "type": "string",
          "description": "you can just select one item from below:\n`hour`\n`day`\n`week`\n`month`\n`year`\n`all`"
        }
      },
      "required": [
        "query"
      ]
    }
  },
  {
    "name": "agntdata_reddit_Search_Subreddits",
    "description": "Search Subreddits",
    "method": "GET",
    "path": "/getSearchSubreddits",
    "parameters": {
      "type": "object",
      "properties": {
        "cursor": {
          "type": "string",
          "description": "cursor"
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
  },
  {
    "name": "agntdata_reddit_New_Subreddits",
    "description": "New Subreddits",
    "method": "GET",
    "path": "/getNewSubreddits",
    "parameters": {
      "type": "object",
      "properties": {
        "cursor": {
          "type": "string",
          "description": "cursor"
        }
      }
    }
  },
  {
    "name": "agntdata_reddit_Popular_Subreddits",
    "description": "Popular Subreddits",
    "method": "GET",
    "path": "/getPopularSubreddits",
    "parameters": {
      "type": "object",
      "properties": {
        "cursor": {
          "type": "string",
          "description": "cursor"
        }
      }
    }
  },
  {
    "name": "agntdata_reddit_Post_Details",
    "description": "Post Details",
    "method": "GET",
    "path": "/getPostDetails",
    "parameters": {
      "type": "object",
      "properties": {
        "post_url": {
          "type": "string",
          "description": "post_url"
        }
      },
      "required": [
        "post_url"
      ]
    }
  },
  {
    "name": "agntdata_reddit_Posts_By_Subreddit",
    "description": "Posts By Subreddit",
    "method": "GET",
    "path": "/getPostsBySubreddit",
    "parameters": {
      "type": "object",
      "properties": {
        "subreddit": {
          "type": "string",
          "description": "example: reddit.com/r/`memes`"
        },
        "sort": {
          "type": "string",
          "description": "you can just select one item from below:\n`new`\n`hot`\n`rising`"
        },
        "cursor": {
          "type": "string",
          "description": "cursor"
        }
      },
      "required": [
        "subreddit",
        "sort"
      ]
    }
  },
  {
    "name": "agntdata_reddit_Top_Comments_By_Username",
    "description": "Top Comments By Username",
    "method": "GET",
    "path": "/getTopCommentsByUsername",
    "parameters": {
      "type": "object",
      "properties": {
        "time": {
          "type": "string",
          "description": "you can just select one item from below:\n`hour`\n`day`\n`week`\n`month`\n`year`\n`all`"
        },
        "username": {
          "type": "string",
          "description": "username"
        },
        "cursor": {
          "type": "string",
          "description": "cursor"
        }
      },
      "required": [
        "time",
        "username"
      ]
    }
  },
  {
    "name": "agntdata_reddit_Popular_Posts",
    "description": "Popular Posts",
    "method": "GET",
    "path": "/getPopularPosts",
    "parameters": {
      "type": "object",
      "properties": {
        "cursor": {
          "type": "string",
          "description": "cursor"
        },
        "sort": {
          "type": "string",
          "description": "you can just send `new `or `hot`"
        }
      },
      "required": [
        "sort"
      ]
    }
  },
  {
    "name": "agntdata_reddit_Top_Posts_By_Subreddit",
    "description": "Top Posts By Subreddit",
    "method": "GET",
    "path": "/getTopPostsBySubreddit",
    "parameters": {
      "type": "object",
      "properties": {
        "time": {
          "type": "string",
          "description": "you can just select one item from below:\n`hour`\n`day`\n`week`\n`month`\n`year`\n`all`"
        },
        "subreddit": {
          "type": "string",
          "description": "example: reddit.com/r/`memes`"
        },
        "cursor": {
          "type": "string",
          "description": "cursor"
        }
      },
      "required": [
        "time",
        "subreddit"
      ]
    }
  },
  {
    "name": "agntdata_reddit_Comments_By_Username",
    "description": "Comments By Username",
    "method": "GET",
    "path": "/getCommentsByUsername",
    "parameters": {
      "type": "object",
      "properties": {
        "sort": {
          "type": "string",
          "description": "you can just send `new `or `hot`"
        },
        "username": {
          "type": "string",
          "description": "username"
        },
        "cursor": {
          "type": "string",
          "description": "cursor"
        }
      },
      "required": [
        "sort",
        "username"
      ]
    }
  },
  {
    "name": "agntdata_reddit_Top_Posts_By_Username",
    "description": "Top Posts By Username",
    "method": "GET",
    "path": "/getTopPostsByUsername",
    "parameters": {
      "type": "object",
      "properties": {
        "cursor": {
          "type": "string",
          "description": "cursor"
        },
        "username": {
          "type": "string",
          "description": "username"
        },
        "time": {
          "type": "string",
          "description": "you can just select one item from below:\n`hour`\n`day`\n`week`\n`month`\n`year`\n`all`"
        }
      },
      "required": [
        "username",
        "time"
      ]
    }
  },
  {
    "name": "agntdata_reddit_Posts_By_Username",
    "description": "Posts By Username",
    "method": "GET",
    "path": "/getPostsByUsername",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        },
        "cursor": {
          "type": "string",
          "description": "cursor"
        },
        "sort": {
          "type": "string",
          "description": "you can just send `new `or `hot`"
        }
      },
      "required": [
        "username",
        "sort"
      ]
    }
  },
  {
    "name": "agntdata_reddit_Rising_Popular_Posts",
    "description": "Rising Popular Posts",
    "method": "GET",
    "path": "/getRisingPopularPosts",
    "parameters": {
      "type": "object",
      "properties": {
        "cursor": {
          "type": "string",
          "description": "cursor"
        }
      }
    }
  },
  {
    "name": "agntdata_reddit_Top_Popular_Posts",
    "description": "Top Popular Posts",
    "method": "GET",
    "path": "/getTopPopularPosts",
    "parameters": {
      "type": "object",
      "properties": {
        "time": {
          "type": "string",
          "description": "you can just select one item from below:\n`hour`\n`day`\n`week`\n`month`\n`year`\n`all`"
        },
        "cursor": {
          "type": "string",
          "description": "cursor"
        }
      },
      "required": [
        "time"
      ]
    }
  }
]
```

## Example

```bash
curl -X GET &#x27;https://api.agntdata.dev/v1/data/reddit&#x27; \
  -H &#x27;X-API-Key: your_api_key_here&#x27; \
  -H &#x27;Content-Type: application/json&#x27;
```

## Use Cases

- Social and creator intelligence agents using Reddit
- Marketing and research teams monitoring accounts and content
- Product teams building alerts, digests, and dashboards
- Developers prototyping LLM tools that need live network data
- Data teams joining Reddit signals with CRM or warehouse data

## Other Platforms

agntdata provides unified access to social data across multiple platforms. Explore other available APIs:

```bash
curl https://api.agntdata.dev/v1/platforms
```

Available platforms: LinkedIn, YouTube, TikTok, X, Instagram, Reddit, Facebook. Each uses the same API key and follows the same patterns.

## Links

- [Documentation](https://agnt.mintlify.app)
- [API Reference](https://agnt.mintlify.app/apis/social/reddit)
- [ClawHub skill](https://clawhub.ai/agntdata/agntdata-reddit)
