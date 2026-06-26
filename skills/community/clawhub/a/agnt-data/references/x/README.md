# X (Twitter) API Reference

**App name:** `x`
**Base URL:** `https://api.agntdata.dev/v1/data/x`
**Endpoints:** 52

Unified access to tweets, user profiles, followers, search, and hashtag streams. Built for LLMs and automation — not one-off scraping.

## Authentication

All requests require the agntdata API key:

```
Authorization: Bearer $AGNTDATA_API_KEY
```

---

## Available Endpoints

| Method | Path | Summary |
|--------|------|---------|
| `GET` | `/user/medias/continuation` | Continuation User's Media |
| `POST` | `/user/medias/continuation` | Continuation User's Media |
| `GET` | `/user/medias` | User's Media |
| `POST` | `/user/medias` | User's Media |
| `GET` | `/user/likes/continuation` | Continuation User's Likes |
| `POST` | `/user/likes/continuation` | Continuation User's Likes |
| `GET` | `/user/likes` | User's Likes |
| `POST` | `/user/likes` | User's Likes |
| `GET` | `/user/followers/continuation` | Continuation User's Followers |
| `POST` | `/user/followers/continuation` | Continuation User's Followers |
| `GET` | `/user/followers` | User's Followers |
| `POST` | `/user/followers` | User's Followers |
| `GET` | `/user/following/continuation` | User's Following Continuation |
| `POST` | `/user/following/continuation` | User's Following Continuation |
| `GET` | `/user/tweets` | User's Tweets |
| `POST` | `/user/tweets` | User's Tweets |
| `GET` | `/user/tweets/continuation` | User's Tweets Continuation |
| `POST` | `/user/tweets/continuation` | User's Tweets Continuation |
| `GET` | `/user/details` | User Details |
| `POST` | `/user/details` | User Details |
| `GET` | `/user/about` | User About |
| `GET` | `/tweet/replies/continuation` | Tweet Replies Continuation |
| `POST` | `/tweet/replies/continuation` | Tweet Replies Continuation |
| `GET` | `/tweet/favoriters/continuation` | Tweet User Favoriters Continuation |
| `GET` | `/tweet/retweets/continuation` | Tweet User Retweets Continuation |
| `GET` | `/tweet/details` | Tweet Details |
| `POST` | `/tweet/details` | Tweet Details |
| `GET` | `/tweet/favoriters` | Tweet User Favoriters |
| `GET` | `/tweet/retweets` | Tweet User Retweets |
| `GET` | `/tweet/replies` | Tweet Replies |
| `POST` | `/tweet/replies` | Tweet Replies |
| `GET` | `/user/following` | User's Following |
| `POST` | `/user/following` | User's Following |
| `GET` | `/lists/tweets/continuation` | Lists Tweets Continuation |
| `GET` | `/search/search/continuation` | Search Continuation |
| `POST` | `/search/search/continuation` | Search Continuation |
| `GET` | `/ai/topic-classification` | Topic Classification |
| `POST` | `/translate/detect` | Detect |
| `GET` | `/ai/named-entity-recognition` | Named Entity Recognition |
| `GET` | `/ai/sentiment-analysis` | Sentiment Analysis |
| `POST` | `/translate` | Translate |
| `GET` | `/trends/available` | Available Locations (Beta) |
| `GET` | `/trends/` | Get trends near a location (Beta) |
| `GET` | `/search/geo` | Geo Search (Beta) |
| `GET` | `/lists/tweets` | Lists Tweets |
| `GET` | `/lists/details` | Lists Details |
| `GET` | `/search/search` | Search |
| `POST` | `/search/search` | Search |
| `GET` | `/hashtag/hashtag` | Hashtag |
| `POST` | `/hashtag/hashtag` | Hashtag |
| `GET` | `/hashtag/hashtag/continuation` | Hashtag Continuation |
| `POST` | `/hashtag/hashtag/continuation` | Hashtag Continuation |

## Tool Schemas

The following JSON defines all available tools with their parameters. Each tool maps to an API endpoint.

```json
[
  {
    "name": "agntdata_x_user_medias_continuation_get",
    "description": "Continuation User's Media",
    "method": "GET",
    "path": "/user/medias/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "number",
          "description": "limit"
        },
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "user_id": {
          "type": "string",
          "description": "user_id"
        }
      },
      "required": [
        "continuation_token",
        "user_id"
      ]
    }
  },
  {
    "name": "agntdata_x_user_medias_continuation_post",
    "description": "Continuation User's Media",
    "method": "POST",
    "path": "/user/medias/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "integer",
          "description": "user_id"
        },
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        }
      }
    }
  },
  {
    "name": "agntdata_x_User_s_Media_get__user_medias",
    "description": "User's Media",
    "method": "GET",
    "path": "/user/medias",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "number",
          "description": "limit"
        },
        "user_id": {
          "type": "string",
          "description": "user_id"
        }
      },
      "required": [
        "user_id"
      ]
    }
  },
  {
    "name": "agntdata_x_User_s_Media_post__user_medias",
    "description": "User's Media",
    "method": "POST",
    "path": "/user/medias",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "integer",
          "description": "user_id"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        }
      }
    }
  },
  {
    "name": "agntdata_x_user_likes_continuation_get",
    "description": "Continuation User's Likes",
    "method": "GET",
    "path": "/user/likes/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "limit": {
          "type": "number",
          "description": "limit"
        },
        "user_id": {
          "type": "string",
          "description": "user_id"
        }
      },
      "required": [
        "continuation_token",
        "user_id"
      ]
    }
  },
  {
    "name": "agntdata_x_user_likes_continuation_post",
    "description": "Continuation User's Likes",
    "method": "POST",
    "path": "/user/likes/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "integer",
          "description": "user_id"
        },
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        }
      }
    }
  },
  {
    "name": "agntdata_x_User_s_Likes_get__user_likes",
    "description": "User's Likes",
    "method": "GET",
    "path": "/user/likes",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "string",
          "description": "user_id"
        },
        "limit": {
          "type": "number",
          "description": "limit"
        }
      },
      "required": [
        "user_id"
      ]
    }
  },
  {
    "name": "agntdata_x_User_s_Likes_post__user_likes",
    "description": "User's Likes",
    "method": "POST",
    "path": "/user/likes",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "integer",
          "description": "user_id"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        }
      }
    }
  },
  {
    "name": "agntdata_x_user_followers_continuation_get",
    "description": "Continuation User's Followers",
    "method": "GET",
    "path": "/user/followers/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "string",
          "description": "user_id"
        },
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "limit": {
          "type": "number",
          "description": "limit"
        }
      },
      "required": [
        "user_id",
        "continuation_token"
      ]
    }
  },
  {
    "name": "agntdata_x_user_followers_continuation_post",
    "description": "Continuation User's Followers",
    "method": "POST",
    "path": "/user/followers/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "integer",
          "description": "user_id"
        },
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        }
      }
    }
  },
  {
    "name": "agntdata_x_User_s_Followers_get__user_followers",
    "description": "User's Followers",
    "method": "GET",
    "path": "/user/followers",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "number",
          "description": "limit"
        },
        "user_id": {
          "type": "string",
          "description": "user_id"
        }
      },
      "required": [
        "user_id"
      ]
    }
  },
  {
    "name": "agntdata_x_User_s_Followers_post__user_followers",
    "description": "User's Followers",
    "method": "POST",
    "path": "/user/followers",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "integer",
          "description": "user_id"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        }
      }
    }
  },
  {
    "name": "agntdata_x_user_following_continuation_get",
    "description": "User's Following Continuation",
    "method": "GET",
    "path": "/user/following/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "limit": {
          "type": "number",
          "description": "limit"
        },
        "user_id": {
          "type": "string",
          "description": "user_id"
        }
      },
      "required": [
        "continuation_token",
        "user_id"
      ]
    }
  },
  {
    "name": "agntdata_x_user_following_continuation_post",
    "description": "User's Following Continuation",
    "method": "POST",
    "path": "/user/following/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "integer",
          "description": "user_id"
        },
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        }
      }
    }
  },
  {
    "name": "agntdata_x_User_s_Tweets_get__user_tweets",
    "description": "User's Tweets",
    "method": "GET",
    "path": "/user/tweets",
    "parameters": {
      "type": "object",
      "properties": {
        "include_pinned": {
          "type": "boolean",
          "description": "include_pinned"
        },
        "limit": {
          "type": "number",
          "description": "limit"
        },
        "user_id": {
          "type": "string",
          "description": "user_id"
        },
        "include_replies": {
          "type": "boolean",
          "description": "include_replies"
        },
        "username": {
          "type": "string",
          "description": "username"
        }
      }
    }
  },
  {
    "name": "agntdata_x_User_s_Tweets_post__user_tweets",
    "description": "User's Tweets",
    "method": "POST",
    "path": "/user/tweets",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        },
        "user_id": {
          "type": "string",
          "description": "user_id"
        },
        "include_replies": {
          "type": "boolean",
          "description": "include_replies"
        },
        "include_pinned": {
          "type": "boolean",
          "description": "include_pinned"
        }
      }
    }
  },
  {
    "name": "agntdata_x_user_tweets_continuation_get",
    "description": "User's Tweets Continuation",
    "method": "GET",
    "path": "/user/tweets/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        },
        "limit": {
          "type": "number",
          "description": "limit"
        },
        "include_replies": {
          "type": "boolean",
          "description": "include_replies"
        },
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "user_id": {
          "type": "string",
          "description": "user_id"
        }
      },
      "required": [
        "continuation_token"
      ]
    }
  },
  {
    "name": "agntdata_x_user_tweets_continuation_post",
    "description": "User's Tweets Continuation",
    "method": "POST",
    "path": "/user/tweets/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "user_id": {
          "type": "string",
          "description": "user_id"
        },
        "include_replies": {
          "type": "boolean",
          "description": "include_replies"
        }
      }
    }
  },
  {
    "name": "agntdata_x_User_Details_get__user_details",
    "description": "User Details",
    "method": "GET",
    "path": "/user/details",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        },
        "user_id": {
          "type": "string",
          "description": "user_id"
        }
      }
    }
  },
  {
    "name": "agntdata_x_User_Details_post__user_details",
    "description": "User Details",
    "method": "POST",
    "path": "/user/details",
    "parameters": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "description": "username"
        }
      }
    }
  },
  {
    "name": "agntdata_x_User_About_get__user_about",
    "description": "User About",
    "method": "GET",
    "path": "/user/about",
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
    "name": "agntdata_x_tweet_replies_continuation_get",
    "description": "Tweet Replies Continuation",
    "method": "GET",
    "path": "/tweet/replies/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "tweet_id": {
          "type": "string",
          "description": "tweet_id"
        }
      },
      "required": [
        "continuation_token",
        "tweet_id"
      ]
    }
  },
  {
    "name": "agntdata_x_tweet_replies_continuation_post",
    "description": "Tweet Replies Continuation",
    "method": "POST",
    "path": "/tweet/replies/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "tweet_id": {
          "type": "string",
          "description": "tweet_id"
        },
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        }
      }
    }
  },
  {
    "name": "agntdata_x_tweet_favoriters_continuation_get",
    "description": "Tweet User Favoriters Continuation",
    "method": "GET",
    "path": "/tweet/favoriters/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "tweet_id": {
          "type": "string",
          "description": "tweet_id"
        }
      },
      "required": [
        "continuation_token",
        "tweet_id"
      ]
    }
  },
  {
    "name": "agntdata_x_tweet_retweets_continuation_get",
    "description": "Tweet User Retweets Continuation",
    "method": "GET",
    "path": "/tweet/retweets/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "tweet_id": {
          "type": "string",
          "description": "tweet_id"
        },
        "limit": {
          "type": "string",
          "description": "limit"
        }
      },
      "required": [
        "continuation_token",
        "tweet_id"
      ]
    }
  },
  {
    "name": "agntdata_x_Tweet_Details_get__tweet_details",
    "description": "Tweet Details",
    "method": "GET",
    "path": "/tweet/details",
    "parameters": {
      "type": "object",
      "properties": {
        "tweet_id": {
          "type": "string",
          "description": "tweet_id"
        }
      },
      "required": [
        "tweet_id"
      ]
    }
  },
  {
    "name": "agntdata_x_Tweet_Details_post__tweet_details",
    "description": "Tweet Details",
    "method": "POST",
    "path": "/tweet/details",
    "parameters": {
      "type": "object",
      "properties": {
        "tweet_id": {
          "type": "string",
          "description": "tweet_id"
        }
      }
    }
  },
  {
    "name": "agntdata_x_Tweet_User_Favoriters_get__tweet_favoriters",
    "description": "Tweet User Favoriters",
    "method": "GET",
    "path": "/tweet/favoriters",
    "parameters": {
      "type": "object",
      "properties": {
        "tweet_id": {
          "type": "string",
          "description": "tweet_id"
        }
      },
      "required": [
        "tweet_id"
      ]
    }
  },
  {
    "name": "agntdata_x_Tweet_User_Retweets_get__tweet_retweets",
    "description": "Tweet User Retweets",
    "method": "GET",
    "path": "/tweet/retweets",
    "parameters": {
      "type": "object",
      "properties": {
        "tweet_id": {
          "type": "string",
          "description": "tweet_id"
        },
        "limit": {
          "type": "string",
          "description": "limit"
        }
      },
      "required": [
        "tweet_id"
      ]
    }
  },
  {
    "name": "agntdata_x_Tweet_Replies_get__tweet_replies",
    "description": "Tweet Replies",
    "method": "GET",
    "path": "/tweet/replies",
    "parameters": {
      "type": "object",
      "properties": {
        "tweet_id": {
          "type": "string",
          "description": "tweet_id"
        }
      },
      "required": [
        "tweet_id"
      ]
    }
  },
  {
    "name": "agntdata_x_Tweet_Replies_post__tweet_replies",
    "description": "Tweet Replies",
    "method": "POST",
    "path": "/tweet/replies",
    "parameters": {
      "type": "object",
      "properties": {
        "tweet_id": {
          "type": "string",
          "description": "tweet_id"
        }
      }
    }
  },
  {
    "name": "agntdata_x_User_s_Following_get__user_following",
    "description": "User's Following",
    "method": "GET",
    "path": "/user/following",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "string",
          "description": "user_id"
        },
        "limit": {
          "type": "number",
          "description": "limit"
        }
      },
      "required": [
        "user_id"
      ]
    }
  },
  {
    "name": "agntdata_x_User_s_Following_post__user_following",
    "description": "User's Following",
    "method": "POST",
    "path": "/user/following",
    "parameters": {
      "type": "object",
      "properties": {
        "user_id": {
          "type": "integer",
          "description": "user_id"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        }
      }
    }
  },
  {
    "name": "agntdata_x_lists_tweets_continuation_get",
    "description": "Lists Tweets Continuation",
    "method": "GET",
    "path": "/lists/tweets/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "number",
          "description": "limit"
        },
        "list_id": {
          "type": "string",
          "description": "list_id"
        },
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        }
      },
      "required": [
        "list_id",
        "continuation_token"
      ]
    }
  },
  {
    "name": "agntdata_x_search_continuation_get",
    "description": "Search Continuation",
    "method": "GET",
    "path": "/search/search/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "end_date": {
          "type": "string",
          "description": "end_date"
        },
        "min_likes": {
          "type": "number",
          "description": "min_likes"
        },
        "start_date": {
          "type": "string",
          "description": "YYYY-MM-DD"
        },
        "min_replies": {
          "type": "number",
          "description": "min_replies"
        },
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "language": {
          "type": "string",
          "description": "language"
        },
        "limit": {
          "type": "number",
          "description": "limit"
        },
        "query": {
          "type": "string",
          "description": "query"
        },
        "min_retweets": {
          "type": "number",
          "description": "min_retweets"
        },
        "section": {
          "type": "string",
          "description": "section"
        }
      },
      "required": [
        "continuation_token",
        "query"
      ]
    }
  },
  {
    "name": "agntdata_x_search_continuation_post",
    "description": "Search Continuation",
    "method": "POST",
    "path": "/search/search/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "query"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "section": {
          "type": "string",
          "description": "section"
        },
        "language": {
          "type": "string",
          "description": "language"
        },
        "min_likes": {
          "type": "integer",
          "description": "min_likes"
        },
        "min_retweets": {
          "type": "integer",
          "description": "min_retweets"
        },
        "start_date": {
          "type": "string",
          "description": "start_date"
        },
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        }
      }
    }
  },
  {
    "name": "agntdata_x_Topic_Classification_get__ai_topic_classification",
    "description": "Topic Classification",
    "method": "GET",
    "path": "/ai/topic-classification",
    "parameters": {
      "type": "object",
      "properties": {
        "text": {
          "type": "string",
          "description": "text"
        }
      },
      "required": [
        "text"
      ]
    }
  },
  {
    "name": "agntdata_x_Detect_post__translate_detect",
    "description": "Detect",
    "method": "POST",
    "path": "/translate/detect",
    "parameters": {
      "type": "object",
      "properties": {
        "text": {
          "type": "string",
          "description": "text"
        }
      }
    }
  },
  {
    "name": "agntdata_x_ai_named_entity_recognition",
    "description": "Named Entity Recognition",
    "method": "GET",
    "path": "/ai/named-entity-recognition",
    "parameters": {
      "type": "object",
      "properties": {
        "text": {
          "type": "string",
          "description": "text"
        }
      },
      "required": [
        "text"
      ]
    }
  },
  {
    "name": "agntdata_x_Sentiment_Analysis_get__ai_sentiment_analysis",
    "description": "Sentiment Analysis",
    "method": "GET",
    "path": "/ai/sentiment-analysis",
    "parameters": {
      "type": "object",
      "properties": {
        "text": {
          "type": "string",
          "description": "text"
        }
      },
      "required": [
        "text"
      ]
    }
  },
  {
    "name": "agntdata_x_Translate_post__translate",
    "description": "Translate",
    "method": "POST",
    "path": "/translate",
    "parameters": {
      "type": "object",
      "properties": {
        "dest": {
          "type": "string",
          "description": "dest"
        },
        "text": {
          "type": "string",
          "description": "text"
        }
      }
    }
  },
  {
    "name": "agntdata_x_Available_Locations___Beta__get__trends_available",
    "description": "Available Locations (Beta)",
    "method": "GET",
    "path": "/trends/available",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "agntdata_x_Get_trends_near_a_location__Beta__get__trends",
    "description": "Get trends near a location (Beta)",
    "method": "GET",
    "path": "/trends/",
    "parameters": {
      "type": "object",
      "properties": {
        "woeid": {
          "type": "string",
          "description": "woeid"
        }
      },
      "required": [
        "woeid"
      ]
    }
  },
  {
    "name": "agntdata_x_Geo_Search___Beta__get__search_geo",
    "description": "Geo Search (Beta)",
    "method": "GET",
    "path": "/search/geo",
    "parameters": {
      "type": "object",
      "properties": {
        "section": {
          "type": "string",
          "description": "section"
        },
        "language": {
          "type": "string",
          "description": "language"
        },
        "limit": {
          "type": "string",
          "description": "limit"
        },
        "query": {
          "type": "string",
          "description": "query"
        },
        "range": {
          "type": "string",
          "description": "range"
        },
        "longitude": {
          "type": "string",
          "description": "longitude"
        },
        "latitude": {
          "type": "string",
          "description": "latitude"
        }
      },
      "required": [
        "query"
      ]
    }
  },
  {
    "name": "agntdata_x_Lists_Tweets_get__lists_tweets",
    "description": "Lists Tweets",
    "method": "GET",
    "path": "/lists/tweets",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "number",
          "description": "limit"
        },
        "list_id": {
          "type": "string",
          "description": "list_id"
        }
      },
      "required": [
        "list_id"
      ]
    }
  },
  {
    "name": "agntdata_x_Lists_Details_get__lists_details",
    "description": "Lists Details",
    "method": "GET",
    "path": "/lists/details",
    "parameters": {
      "type": "object",
      "properties": {
        "list_id": {
          "type": "string",
          "description": "list_id"
        }
      },
      "required": [
        "list_id"
      ]
    }
  },
  {
    "name": "agntdata_x_Search_get__search_search",
    "description": "Search",
    "method": "GET",
    "path": "/search/search",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "number",
          "description": "limit"
        },
        "language": {
          "type": "string",
          "description": "language"
        },
        "start_date": {
          "type": "string",
          "description": "YYYY-MM-DD"
        },
        "min_likes": {
          "type": "number",
          "description": "min_likes"
        },
        "min_retweets": {
          "type": "number",
          "description": "min_retweets"
        },
        "query": {
          "type": "string",
          "description": "query"
        },
        "end_date": {
          "type": "string",
          "description": "end_date"
        },
        "min_replies": {
          "type": "number",
          "description": "min_replies"
        },
        "section": {
          "type": "string",
          "description": "section"
        }
      },
      "required": [
        "query"
      ]
    }
  },
  {
    "name": "agntdata_x_Search_post__search_search",
    "description": "Search",
    "method": "POST",
    "path": "/search/search",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "query"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "section": {
          "type": "string",
          "description": "section"
        },
        "language": {
          "type": "string",
          "description": "language"
        },
        "min_likes": {
          "type": "integer",
          "description": "min_likes"
        },
        "min_retweets": {
          "type": "integer",
          "description": "min_retweets"
        },
        "start_date": {
          "type": "string",
          "description": "start_date"
        }
      }
    }
  },
  {
    "name": "agntdata_x_Hashtag_get__hashtag_hashtag",
    "description": "Hashtag",
    "method": "GET",
    "path": "/hashtag/hashtag",
    "parameters": {
      "type": "object",
      "properties": {
        "section": {
          "type": "string",
          "description": "section"
        },
        "hashtag": {
          "type": "string",
          "description": "hashtag"
        },
        "limit": {
          "type": "string",
          "description": "limit"
        }
      },
      "required": [
        "hashtag"
      ]
    }
  },
  {
    "name": "agntdata_x_Hashtag_post__hashtag_hashtag",
    "description": "Hashtag",
    "method": "POST",
    "path": "/hashtag/hashtag",
    "parameters": {
      "type": "object",
      "properties": {
        "hashtag": {
          "type": "string",
          "description": "hashtag"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "section": {
          "type": "string",
          "description": "section"
        },
        "language": {
          "type": "string",
          "description": "language"
        }
      }
    }
  },
  {
    "name": "agntdata_x_hashtag_continuation_get",
    "description": "Hashtag Continuation",
    "method": "GET",
    "path": "/hashtag/hashtag/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        },
        "hashtag": {
          "type": "string",
          "description": "hashtag"
        },
        "limit": {
          "type": "string",
          "description": "limit"
        },
        "section": {
          "type": "string",
          "description": "section"
        }
      },
      "required": [
        "continuation_token",
        "hashtag"
      ]
    }
  },
  {
    "name": "agntdata_x_hashtag_continuation_post",
    "description": "Hashtag Continuation",
    "method": "POST",
    "path": "/hashtag/hashtag/continuation",
    "parameters": {
      "type": "object",
      "properties": {
        "hashtag": {
          "type": "string",
          "description": "hashtag"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "section": {
          "type": "string",
          "description": "section"
        },
        "language": {
          "type": "string",
          "description": "language"
        },
        "continuation_token": {
          "type": "string",
          "description": "continuation_token"
        }
      }
    }
  }
]
```

## Example

```bash
curl -X GET "https://api.agntdata.dev/v1/data/x/user/medias/continuation?param=value" \
  -H "Authorization: Bearer $AGNTDATA_API_KEY"
```

## Links

- [Documentation](https://agnt.mintlify.app)
- [API Reference](https://agnt.mintlify.app/apis/social/x)
- [Dashboard](https://app.agntdata.dev/dashboard)
