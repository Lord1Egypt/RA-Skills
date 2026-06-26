# Facebook API Reference

**App name:** `facebook`
**Base URL:** `https://api.agntdata.dev/v1/data/facebook`
**Endpoints:** 35

Unified access to page and group posts, marketplace listings, video content, and ad discovery. Built for LLMs and automation — not one-off scraping.

## Authentication

All requests require the agntdata API key:

```
Authorization: Bearer $AGNTDATA_API_KEY
```

---

## Available Endpoints

| Method | Path | Summary |
|--------|------|---------|
| `GET` | `/get_facebook_video_post_details` | Get Facebook Video Post Details |
| `GET` | `/get_facebook_post_comments_details` | Get Facebook Posts Comments |
| `GET` | `/get_facebook_post_details` | Get Facebook Post Details |
| `GET` | `/get_facebook_post_attachement_details` | Get Facebook Post Attachement Details |
| `GET` | `/get_facebook_post_comment_replies` | Get Facebook Posts Comment Replies |
| `GET` | `/fetch_archive_ad_details` | Fetch Archive Ad Details |
| `GET` | `/fetch_page_ad_details` | Fetch Page Ad Details |
| `GET` | `/fetch_search_ads_pages` | Fetch Search Ads Pages (GET) |
| `POST` | `/fetch_search_ads_pages` | Fetch Search Ads Pages (POST) |
| `GET` | `/download_media` | Download Media |
| `GET` | `/search_facebook_watch_videos` | Fetch Search Videos |
| `GET` | `/get_facebook_group_videos_details_from_id` | Get Group Videos |
| `GET` | `/get_listing_item_details` | Get Marketplace Listing Item Details |
| `GET` | `/get_facebook_group_posts_details_from_id` | Get Facebook Groups Posts |
| `GET` | `/get_facebook_group_details_from_id` | Get Facebook Group Details |
| `GET` | `/get_facebook_reels_details` | Get Page Reels |
| `GET` | `/get_facebook_page_videos_details` | Get Page Videos |
| `GET` | `/get_facebook_page_posts_details_from_id` | Get Facebook Pages Posts |
| `GET` | `/get_facebook_pages_details_from_link` | Get Facebook Page Details |
| `GET` | `/facebook_marketplace_rentals_listings` | Get Marketplace Rental Property Search Results |
| `GET` | `/find_city_coordinates` | Get Marketplace City Coordinates |
| `GET` | `/facebook_marketplace_vehicles_listings` | Get Marketplace Vehicles Search Results |
| `GET` | `/get_marketplace_categories` | Get Marketplace Categories |
| `GET` | `/fetch_search_posts` | Fetch Search Posts |
| `GET` | `/get_facebook_marketplace_items_listing` | Get Marketplace Search Results |
| `GET` | `/get_facebook_group_id` | Get Facebook Group ID |
| `GET` | `/get_facebook_group_metadata_details` | Get Facebook Group Metadata Details |
| `GET` | `/get_seller_details` | Get Seller Details |
| `GET` | `/get_supported_countries` | Get Supported Countries |
| `GET` | `/fetch_search_ads_keywords` | Fech Search Ads Keywords |
| `GET` | `/fetch_search_locations` | Fetch Search Locations |
| `GET` | `/fetch_search_people` | Fetch Search People |
| `GET` | `/fetch_search_pages` | Fetch Search Pages |
| `GET` | `/get_facebook_post_id` | Get Facebook Post ID |
| `GET` | `/get_facebook_page_id` | Get Facebook Page ID |

## Tool Schemas

The following JSON defines all available tools with their parameters. Each tool maps to an API endpoint.

```json
[
  {
    "name": "agntdata_facebook_Get_Facebook_Video_Post_Details",
    "description": "Get Facebook Video Post Details",
    "method": "GET",
    "path": "/get_facebook_video_post_details",
    "parameters": {
      "type": "object",
      "properties": {
        "video_id": {
          "type": "number",
          "description": "video_id"
        }
      }
    }
  },
  {
    "name": "agntdata_facebook_Get_Facebook_Posts_Comments",
    "description": "Get Facebook Posts Comments",
    "method": "GET",
    "path": "/get_facebook_post_comments_details",
    "parameters": {
      "type": "object",
      "properties": {
        "include_reply_info": {
          "type": "boolean",
          "description": "### `include_reply_info` *(boolean, optional, default: false)*\n\nWhen set to `true`, each comment in the response will include two additional fields:\n\n- **`comment_feedback_id`** — The feedback ID associated with the comment.\n- **`expansion_token`** — A token used to paginate through replies.\n\n> **Note:** This parameter does not return the replies themselves. To fetch the actual reply content, use the `GET /get_facebook_post_comment_replies` endpoint, passing the `comment_feedback_id` and `expansion_token` returned here."
        },
        "post_id": {
          "type": "string",
          "description": "Facebook Post ID. Used only if `link` is not provided. If both are given, `link` is prioritized."
        },
        "end_cursor": {
          "type": "string",
          "description": "end_cursor"
        },
        "link": {
          "type": "string",
          "description": "link"
        }
      }
    }
  },
  {
    "name": "agntdata_facebook_Get_Facebook_Post_Details",
    "description": "Get Facebook Post Details",
    "method": "GET",
    "path": "/get_facebook_post_details",
    "parameters": {
      "type": "object",
      "properties": {
        "link": {
          "type": "string",
          "description": "link"
        }
      }
    }
  },
  {
    "name": "agntdata_facebook_Get_Facebook_Post_Attachement_Details",
    "description": "Get Facebook Post Attachement Details",
    "method": "GET",
    "path": "/get_facebook_post_attachement_details",
    "parameters": {
      "type": "object",
      "properties": {
        "post_id": {
          "type": "string",
          "description": "Retrieve all attachments details.\n\nFYI: This works only with **public** pages."
        }
      }
    }
  },
  {
    "name": "agntdata_facebook_Get_Facebook_Posts_Comment_Replies",
    "description": "Get Facebook Posts Comment Replies",
    "method": "GET",
    "path": "/get_facebook_post_comment_replies",
    "parameters": {
      "type": "object",
      "properties": {
        "expansion_token": {
          "type": "string",
          "description": "**`expansion_token`** *(string, required)* — The pagination token for loading replies. To obtain this value, set `include_reply_info=true` in the `get_facebook_post_comments_details` endpoint."
        },
        "comment_feedback_id": {
          "type": "string",
          "description": "**`comment_feedback_id`** *(string, required)* — The feedback ID of the parent comment. To obtain this value, set `include_reply_info=true` in the `get_facebook_post_comments_details` endpoint."
        }
      },
      "required": [
        "expansion_token",
        "comment_feedback_id"
      ]
    }
  },
  {
    "name": "agntdata_facebook_Fetch_Archive_Ad_Details",
    "description": "Fetch Archive Ad Details",
    "method": "GET",
    "path": "/fetch_archive_ad_details",
    "parameters": {
      "type": "object",
      "properties": {
        "country": {
          "type": "string",
          "description": "country"
        },
        "ad_archive_id": {
          "type": "string",
          "description": "ad_archive_id"
        },
        "page_id": {
          "type": "string",
          "description": "page_id"
        },
        "is_ad_not_aaa_eligible": {
          "type": "boolean",
          "description": "is_ad_not_aaa_eligible"
        },
        "is_ad_non_political": {
          "type": "boolean",
          "description": "is_ad_non_political"
        }
      },
      "required": [
        "ad_archive_id"
      ]
    }
  },
  {
    "name": "agntdata_facebook_Fetch_Page_Ad_Details",
    "description": "Fetch Page Ad Details",
    "method": "GET",
    "path": "/fetch_page_ad_details",
    "parameters": {
      "type": "object",
      "properties": {
        "page_id": {
          "type": "string",
          "description": "page_id"
        }
      },
      "required": [
        "page_id"
      ]
    }
  },
  {
    "name": "agntdata_facebook_Fetch_Search_Ads_Pages__GET",
    "description": "Fetch Search Ads Pages (GET)",
    "method": "GET",
    "path": "/fetch_search_ads_pages",
    "parameters": {
      "type": "object",
      "properties": {
        "country": {
          "type": "string",
          "description": "country"
        },
        "after_time": {
          "type": "string",
          "description": "after_time"
        },
        "before_time": {
          "type": "string",
          "description": "before_time"
        },
        "ad_page_id": {
          "type": "string",
          "description": "Facebook AD Page ID. Used only if `query` is not provided."
        },
        "activeStatus": {
          "type": "string",
          "description": "activeStatus"
        },
        "end_cursor": {
          "type": "string",
          "description": "end_cursor"
        },
        "query": {
          "type": "string",
          "description": "query"
        }
      }
    }
  },
  {
    "name": "agntdata_facebook_Fetch_Search_Ads_Pages__POST",
    "description": "Fetch Search Ads Pages (POST)",
    "method": "POST",
    "path": "/fetch_search_ads_pages",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "Search query string"
        },
        "ad_page_id": {
          "type": "string",
          "description": "Facebook Ad Page ID. Used only if query is not provided."
        },
        "country": {
          "type": "string",
          "description": "Country filter (e.g. ALL, US, GB)"
        },
        "activeStatus": {
          "type": "string",
          "description": "Filter by active status (e.g. ALL, ACTIVE, INACTIVE)"
        },
        "end_cursor": {
          "type": "string",
          "description": "Pagination cursor for next page of results"
        },
        "after_time": {
          "type": "string",
          "description": "Filter ads created after this time"
        },
        "before_time": {
          "type": "string",
          "description": "Filter ads created before this time"
        },
        "sort_data": {
          "type": "string",
          "description": "Sort order for results"
        }
      }
    }
  },
  {
    "name": "agntdata_facebook_Download_Media",
    "description": "Download Media",
    "method": "GET",
    "path": "/download_media",
    "parameters": {
      "type": "object",
      "properties": {
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
    "name": "agntdata_facebook_Fetch_Search_Videos",
    "description": "Fetch Search Videos",
    "method": "GET",
    "path": "/search_facebook_watch_videos",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "query"
        },
        "fields": {
          "type": "string",
          "description": "Comma-separated list of keys to include in the response. Use dot notation to target specific sections (e.g. `videos.id,videos.title,page_info.end_cursor`). Invalid keys are silently ignored. If omitted, the full response is returned."
        },
        "end_cursor": {
          "type": "string",
          "description": "end_cursor"
        },
        "videos_live": {
          "type": "boolean",
          "description": "videos_live"
        },
        "most_recent": {
          "type": "boolean",
          "description": "most_recent"
        }
      },
      "required": [
        "query"
      ]
    }
  },
  {
    "name": "agntdata_facebook_Get_Group_Videos",
    "description": "Get Group Videos",
    "method": "GET",
    "path": "/get_facebook_group_videos_details_from_id",
    "parameters": {
      "type": "object",
      "properties": {
        "end_cursor": {
          "type": "string",
          "description": "end_cursor"
        },
        "group_id": {
          "type": "string",
          "description": "group_id"
        }
      }
    }
  },
  {
    "name": "agntdata_facebook_Get_Marketplace_Listing_Item_Details",
    "description": "Get Marketplace Listing Item Details",
    "method": "GET",
    "path": "/get_listing_item_details",
    "parameters": {
      "type": "object",
      "properties": {
        "listing_id": {
          "type": "string",
          "description": "listing_id"
        }
      },
      "required": [
        "listing_id"
      ]
    }
  },
  {
    "name": "agntdata_facebook_Get_Facebook_Groups_Posts",
    "description": "Get Facebook Groups Posts",
    "method": "GET",
    "path": "/get_facebook_group_posts_details_from_id",
    "parameters": {
      "type": "object",
      "properties": {
        "end_cursor": {
          "type": "string",
          "description": "end_cursor"
        },
        "group_id": {
          "type": "string",
          "description": "group_id"
        }
      },
      "required": [
        "group_id"
      ]
    }
  },
  {
    "name": "agntdata_facebook_Get_Facebook_Group_Details",
    "description": "Get Facebook Group Details",
    "method": "GET",
    "path": "/get_facebook_group_details_from_id",
    "parameters": {
      "type": "object",
      "properties": {
        "group_id": {
          "type": "string",
          "description": "group_id"
        }
      },
      "required": [
        "group_id"
      ]
    }
  },
  {
    "name": "agntdata_facebook_Get_Page_Reels",
    "description": "Get Page Reels",
    "method": "GET",
    "path": "/get_facebook_reels_details",
    "parameters": {
      "type": "object",
      "properties": {
        "end_cursor": {
          "type": "string",
          "description": "If **end_cursor** is empty, retrieve up to **ten** reels, utilizing the **newly generated** end_cursor from the **page_info** details in the response to fetch subsequent reels in the list."
        },
        "link": {
          "type": "string",
          "description": "link"
        },
        "profile_id": {
          "type": "string",
          "description": "Facebook profile ID. Used only if `link` is not provided."
        }
      }
    }
  },
  {
    "name": "agntdata_facebook_Get_Page_Videos",
    "description": "Get Page Videos",
    "method": "GET",
    "path": "/get_facebook_page_videos_details",
    "parameters": {
      "type": "object",
      "properties": {
        "profile_id": {
          "type": "string",
          "description": "Facebook profile ID. Used only if `link` is not provided."
        },
        "end_cursor": {
          "type": "string",
          "description": "end_cursor"
        },
        "link": {
          "type": "string",
          "description": "link"
        }
      }
    }
  },
  {
    "name": "agntdata_facebook_Get_Facebook_Pages_Posts",
    "description": "Get Facebook Pages Posts",
    "method": "GET",
    "path": "/get_facebook_page_posts_details_from_id",
    "parameters": {
      "type": "object",
      "properties": {
        "fields": {
          "type": "string",
          "description": "Comma-separated keys to filter the response. Supports dot notation and nested keys (e.g. `posts.details.post_id,posts.details.post_link,page_info.end_cursor`). Invalid keys are ignored. If omitted, the full response is returned."
        },
        "end_cursor": {
          "type": "string",
          "description": "end_cursor"
        },
        "before_time": {
          "type": "string",
          "description": "before_time"
        },
        "after_time": {
          "type": "string",
          "description": "after_time"
        },
        "profile_id": {
          "type": "string",
          "description": "profile_id"
        },
        "timezone": {
          "type": "string",
          "description": "timezone"
        }
      },
      "required": [
        "profile_id"
      ]
    }
  },
  {
    "name": "agntdata_facebook_Get_Facebook_Page_Details",
    "description": "Get Facebook Page Details",
    "method": "GET",
    "path": "/get_facebook_pages_details_from_link",
    "parameters": {
      "type": "object",
      "properties": {
        "page_section": {
          "type": "string",
          "description": "Page section to scrape: **default** (main page) or **about** (About section)"
        },
        "show_verified_badge": {
          "type": "boolean",
          "description": "show_verified_badge"
        },
        "proxy_country": {
          "type": "string",
          "description": "proxy_country"
        },
        "profile_id": {
          "type": "string",
          "description": "Facebook profile ID. Used only if `link` is not provided."
        },
        "exact_followers_count": {
          "type": "boolean",
          "description": "Retrieve exact follower count.\n\nFYI: This works only with **public** pages."
        },
        "link": {
          "type": "string",
          "description": "link"
        }
      }
    }
  },
  {
    "name": "agntdata_facebook_marketplace_rentals_listings",
    "description": "Get Marketplace Rental Property Search Results",
    "method": "GET",
    "path": "/facebook_marketplace_rentals_listings",
    "parameters": {
      "type": "object",
      "properties": {
        "filter_price_upper_bound": {
          "type": "number",
          "description": "filter_price_upper_bound"
        },
        "filter_location_latitude": {
          "type": "string",
          "description": "filter_location_latitude"
        },
        "sort_by": {
          "type": "string",
          "description": "sort_by"
        },
        "filter_location_longitude": {
          "type": "string",
          "description": "filter_location_longitude"
        },
        "filter_bathrooms_max": {
          "type": "number",
          "description": "filter_bathrooms_max"
        },
        "is_c2c_listing_only": {
          "type": "boolean",
          "description": "This field indicates whether the listings are from individual sellers only"
        },
        "filter_bathrooms_min": {
          "type": "number",
          "description": "filter_bathrooms_min"
        },
        "filter_bedrooms_max": {
          "type": "number",
          "description": "filter_bedrooms_max"
        },
        "filter_bedrooms_min": {
          "type": "number",
          "description": "filter_bedrooms_min"
        },
        "filter_price_lower_bound": {
          "type": "number",
          "description": "filter_price_lower_bound"
        },
        "end_cursor": {
          "type": "string",
          "description": "end_cursor"
        },
        "filter_radius_km": {
          "type": "number",
          "description": "filter_radius_km"
        }
      }
    }
  },
  {
    "name": "agntdata_facebook_Get_Marketplace_City_Coordinates",
    "description": "Get Marketplace City Coordinates",
    "method": "GET",
    "path": "/find_city_coordinates",
    "parameters": {
      "type": "object",
      "properties": {
        "exactly_one": {
          "type": "boolean",
          "description": "exactly_one"
        },
        "city": {
          "type": "string",
          "description": "city"
        },
        "country": {
          "type": "string",
          "description": "country"
        }
      },
      "required": [
        "city"
      ]
    }
  },
  {
    "name": "agntdata_facebook_Get_Marketplace_Vehicles_Search_Results",
    "description": "Get Marketplace Vehicles Search Results",
    "method": "GET",
    "path": "/facebook_marketplace_vehicles_listings",
    "parameters": {
      "type": "object",
      "properties": {
        "after_time": {
          "type": "string",
          "description": "after_time"
        },
        "end_cursor": {
          "type": "string",
          "description": "end_cursor"
        },
        "exact_match": {
          "type": "boolean",
          "description": "exact_match"
        },
        "before_time": {
          "type": "string",
          "description": "before_time"
        },
        "sort_by": {
          "type": "string",
          "description": "sort_by"
        },
        "filter_location_latitude": {
          "type": "string",
          "description": "filter_location_latitude"
        },
        "filter_price_upper_bound": {
          "type": "number",
          "description": "filter_price_upper_bound"
        },
        "proxy_country": {
          "type": "string",
          "description": "proxy_country"
        },
        "is_c2c_listing_only": {
          "type": "boolean",
          "description": "This field indicates whether the listings are from individual sellers only"
        },
        "filter_price_lower_bound": {
          "type": "number",
          "description": "filter_price_lower_bound"
        },
        "filter_location_longitude": {
          "type": "string",
          "description": "filter_location_longitude"
        },
        "filter_radius_km": {
          "type": "number",
          "description": "filter_radius_km"
        }
      }
    }
  },
  {
    "name": "agntdata_facebook_Get_Marketplace_Categories",
    "description": "Get Marketplace Categories",
    "method": "GET",
    "path": "/get_marketplace_categories",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "agntdata_facebook_Fetch_Search_Posts",
    "description": "Fetch Search Posts",
    "method": "GET",
    "path": "/fetch_search_posts",
    "parameters": {
      "type": "object",
      "properties": {
        "start_time": {
          "type": "string",
          "description": "start_time"
        },
        "recent_posts": {
          "type": "boolean",
          "description": "recent_posts"
        },
        "end_time": {
          "type": "string",
          "description": "end_time"
        },
        "query": {
          "type": "string",
          "description": "query"
        },
        "end_cursor": {
          "type": "string",
          "description": "end_cursor"
        },
        "location_uid": {
          "type": "number",
          "description": "location_uid"
        }
      },
      "required": [
        "query"
      ]
    }
  },
  {
    "name": "agntdata_facebook_Get_Marketplace_Search_Results",
    "description": "Get Marketplace Search Results",
    "method": "GET",
    "path": "/get_facebook_marketplace_items_listing",
    "parameters": {
      "type": "object",
      "properties": {
        "seo_url": {
          "type": "string",
          "description": "seo_url"
        },
        "posted_today": {
          "type": "boolean",
          "description": "posted_today **(boolean)** — If set to **true**, results are limited to items posted today, and the `after_time` and `before_time` filters **are ignored**."
        },
        "fields": {
          "type": "string",
          "description": "Comma-separated keys to filter the response. Supports dot notation and nested keys (e.g. `items.id,items.listingUrl,items.listing_price,page_info.end_cursor`). Invalid keys are ignored. If omitted, the full response is returned."
        },
        "commerce_search_and_rp_condition": {
          "type": "string",
          "description": "This field specifies the condition of items to search for. Choose from the following options:\n\n- new\n- used_like_new\n- used_good\n- used_fair\n\nTo include **multiple conditions**, separate them with commas without spaces. For example, use **new**, **used_like_new**, **used_good**, **used_fair** to search for both new items and items in good used condition. Any value not in this list will result in an error."
        },
        "timezone": {
          "type": "string",
          "description": "timezone"
        },
        "after_time": {
          "type": "string",
          "description": "after_time"
        },
        "before_time": {
          "type": "string",
          "description": "before_time"
        },
        "exact_match": {
          "type": "boolean",
          "description": "exact_match"
        },
        "proxy_country": {
          "type": "string",
          "description": "proxy_country"
        },
        "filter_radius_km": {
          "type": "number",
          "description": "filter_radius_km"
        },
        "filter_price_lower_bound": {
          "type": "number",
          "description": "filter_price_lower_bound"
        },
        "end_cursor": {
          "type": "string",
          "description": "If **end_cursor** is empty, retrieve up to **three** posts, utilizing the **newly generated** end_cursor from the **page_info** details in the response to fetch subsequent posts in the list."
        },
        "category_url": {
          "type": "string",
          "description": "Link should match this pattern `"
        },
        "filter_location_latitude": {
          "type": "string",
          "description": "filter_location_latitude"
        },
        "filter_price_upper_bound": {
          "type": "number",
          "description": "filter_price_upper_bound"
        },
        "commerce_search_sort_by": {
          "type": "string",
          "description": "commerce_search_sort_by"
        },
        "query": {
          "type": "string",
          "description": "query"
        },
        "filter_location_longitude": {
          "type": "string",
          "description": "filter_location_longitude"
        }
      }
    }
  },
  {
    "name": "agntdata_facebook_Get_Facebook_Group_ID",
    "description": "Get Facebook Group ID",
    "method": "GET",
    "path": "/get_facebook_group_id",
    "parameters": {
      "type": "object",
      "properties": {
        "link": {
          "type": "string",
          "description": "link"
        }
      },
      "required": [
        "link"
      ]
    }
  },
  {
    "name": "agntdata_facebook_Get_Facebook_Group_Metadata_Details",
    "description": "Get Facebook Group Metadata Details",
    "method": "GET",
    "path": "/get_facebook_group_metadata_details",
    "parameters": {
      "type": "object",
      "properties": {
        "group_id": {
          "type": "string",
          "description": "group_id"
        },
        "link": {
          "type": "string",
          "description": "link"
        }
      }
    }
  },
  {
    "name": "agntdata_facebook_Get_Seller_Details",
    "description": "Get Seller Details",
    "method": "GET",
    "path": "/get_seller_details",
    "parameters": {
      "type": "object",
      "properties": {
        "seller_id": {
          "type": "string",
          "description": "seller_id"
        }
      },
      "required": [
        "seller_id"
      ]
    }
  },
  {
    "name": "agntdata_facebook_Get_Supported_Countries",
    "description": "Get Supported Countries",
    "method": "GET",
    "path": "/get_supported_countries",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "agntdata_facebook_Fech_Search_Ads_Keywords",
    "description": "Fech Search Ads Keywords",
    "method": "GET",
    "path": "/fetch_search_ads_keywords",
    "parameters": {
      "type": "object",
      "properties": {
        "country": {
          "type": "string",
          "description": "country"
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
    "name": "agntdata_facebook_Fetch_Search_Locations",
    "description": "Fetch Search Locations",
    "method": "GET",
    "path": "/fetch_search_locations",
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
    "name": "agntdata_facebook_Fetch_Search_People",
    "description": "Fetch Search People",
    "method": "GET",
    "path": "/fetch_search_people",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "query"
        },
        "end_cursor": {
          "type": "string",
          "description": "end_cursor"
        },
        "location_uid": {
          "type": "string",
          "description": "location_uid"
        }
      },
      "required": [
        "query"
      ]
    }
  },
  {
    "name": "agntdata_facebook_Fetch_Search_Pages",
    "description": "Fetch Search Pages",
    "method": "GET",
    "path": "/fetch_search_pages",
    "parameters": {
      "type": "object",
      "properties": {
        "location_uid": {
          "type": "string",
          "description": "location_uid"
        },
        "query": {
          "type": "string",
          "description": "query"
        },
        "end_cursor": {
          "type": "string",
          "description": "end_cursor"
        }
      },
      "required": [
        "query"
      ]
    }
  },
  {
    "name": "agntdata_facebook_Get_Facebook_Post_ID",
    "description": "Get Facebook Post ID",
    "method": "GET",
    "path": "/get_facebook_post_id",
    "parameters": {
      "type": "object",
      "properties": {
        "link": {
          "type": "string",
          "description": "link"
        }
      },
      "required": [
        "link"
      ]
    }
  },
  {
    "name": "agntdata_facebook_Get_Facebook_Page_ID",
    "description": "Get Facebook Page ID",
    "method": "GET",
    "path": "/get_facebook_page_id",
    "parameters": {
      "type": "object",
      "properties": {
        "link": {
          "type": "string",
          "description": "link"
        }
      },
      "required": [
        "link"
      ]
    }
  }
]
```

## Example

```bash
curl -X GET "https://api.agntdata.dev/v1/data/facebook/get_facebook_video_post_details?param=value" \
  -H "Authorization: Bearer $AGNTDATA_API_KEY"
```

## Links

- [Documentation](https://agnt.mintlify.app)
- [API Reference](https://agnt.mintlify.app/apis/social/facebook)
- [Dashboard](https://app.agntdata.dev/dashboard)
