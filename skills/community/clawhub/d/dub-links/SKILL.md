---
name: dub-links
description: "Manage Dub short links, track conversions, and read link attribution analytics through the superagnt unified API."
version: 2.0.14
author: superagnt
license: MIT-0
platforms: [macos, linux, windows]
required_environment_variables:
  - SUPERAGNT_API_KEY
metadata:
  hermes:
    tags: [dub, integration, api, ai-agent]
  openclaw:
    requires:
      env:
        - SUPERAGNT_API_KEY
      bins:
        - curl
    primaryEnv: SUPERAGNT_API_KEY
    emoji: "🔗"
    homepage: https://superagnt.com/r/ch-dub-links-docs
---

# Dub Integration

The Dub integration connects your Dub workspace to superagnt so AI agents and workflows can manage short links, track lead and sale conversions, and pull real-time link attribution analytics. Supports link CRUD (including bulk and upsert), tags, folders, customers, custom domains, and the full conversion-tracking pipeline.

## Alternative install: the MCP server

If this client speaks MCP, you can connect the workspace server instead of
using this skill's curl calls — after the user connects their
Dub account in the superagnt app, the same endpoints below are exposed
as native MCP tools:

```
https://mcp.superagnt.com/mcp
```

The URL publishes full OAuth discovery — an MCP-capable client needs the URL
and nothing else (approve once in the browser). Per-client setup lines:
https://www.superagnt.com/install

Everything below works on curl-only environments with just the API key.

## Capabilities and safety

This skill documents the Dub API surface the user's connected
account can reach — which can include destructive operations (updates,
deletes) and, where the vendor supports them, actions performed as the user
(sending messages, modifying records, changing settings). Two hard rules:

- **Confirm before destructive or outbound actions.** Never delete, overwrite,
  or send on the user's behalf without their explicit confirmation in the
  conversation.
- **Stay inside the user's request.** Use only the endpoints the task needs;
  this skill grants no access beyond the Dub connection the user
  set up themselves.

## Prerequisites

1. An API key — get one from the [superagnt app](https://superagnt.com/r/ch-dub-links-key) and export it as
   `SUPERAGNT_API_KEY`.
2. A connected Dub account — connect it on the
   [Connections page](https://app.superagnt.com/dashboard/connections). Calls fail with a clear error
   until the vendor is connected; that error is the signal to send the user to
   the connections page, not a bug.

Note: `/v1/connections/*` calls run on the USER'S Dub credentials —
vendor-side rate limits and billing are theirs, not platform credits.

## Authentication

```
Authorization: Bearer $SUPERAGNT_API_KEY
```

If the variable is not set, ask the user for their key or point them at
https://superagnt.com/r/ch-dub-links-key.

## Verify the install (do this first)

```bash
curl -s https://api.superagnt.com/v1/credits \
  -H &#x27;Authorization: Bearer $SUPERAGNT_API_KEY&#x27;
```

A JSON result proves the key end to end. 401 = bad key; an error naming the
connection means the Dub account is not connected yet.

## Base URL

```
https://api.superagnt.com/v1/connections/dub
```

## Available Endpoints

| Method | Path | Summary |
|--------|------|---------|
| `GET` | `/links` | Retrieve a list of links |
| `POST` | `/links` | Create a link |
| `PUT` | `/links` | Upsert a link |
| `GET` | `/links/info` | Retrieve a link |
| `GET` | `/links/count` | Retrieve links count |
| `PATCH` | `/links/{linkId}` | Update a link |
| `DELETE` | `/links/{linkId}` | Delete a link |
| `POST` | `/links/bulk` | Bulk create links |
| `PATCH` | `/links/bulk` | Bulk update links |
| `DELETE` | `/links/bulk` | Bulk delete links |
| `GET` | `/analytics` | Retrieve analytics |
| `GET` | `/events` | Retrieve a list of events |
| `GET` | `/tags` | Retrieve a list of tags |
| `POST` | `/tags` | Create a tag |
| `PATCH` | `/tags/{id}` | Update a tag |
| `GET` | `/folders` | Retrieve a list of folders |
| `POST` | `/folders` | Create a folder |
| `PATCH` | `/folders/{id}` | Update a folder |
| `DELETE` | `/folders/{id}` | Delete a folder |
| `GET` | `/customers` | Retrieve a list of customers |
| `GET` | `/customers/{id}` | Retrieve a customer |
| `PATCH` | `/customers/{id}` | Update a customer |
| `DELETE` | `/customers/{id}` | Delete a customer |
| `POST` | `/domains` | Create a domain |
| `PATCH` | `/domains/{slug}` | Update a domain |
| `DELETE` | `/domains/{slug}` | Delete a domain |
| `POST` | `/track/lead` | Track a lead |
| `POST` | `/track/sale` | Track a sale |
| `GET` | `/partners` | List partners |
| `POST` | `/partners` | Create or update a partner |
| `GET` | `/partners/links` | Retrieve a partner&#x27;s links |
| `POST` | `/partners/links` | Create a partner link |
| `PUT` | `/partners/links/upsert` | Upsert a partner link |
| `POST` | `/partners/ban` | Ban a partner |
| `POST` | `/partners/deactivate` | Deactivate a partner |
| `GET` | `/bounties/{bountyId}/submissions` | List bounty submissions |
| `POST` | `/bounties/{bountyId}/submissions/{submissionId}/approve` | Approve a bounty submission |
| `POST` | `/bounties/{bountyId}/submissions/{submissionId}/reject` | Reject a bounty submission |
| `GET` | `/commissions` | List commissions |
| `PATCH` | `/commissions/{id}` | Update a commission |
| `GET` | `/payouts` | List payouts |

## Tool Schemas

The following JSON defines every operation with its parameters. Each tool maps
to an API endpoint under the base URL.

```json
[
  {
    "name": "superagnt_connection_dub_getLinks",
    "description": "Retrieve a list of links",
    "method": "GET",
    "path": "/links",
    "parameters": {
      "type": "object",
      "properties": {
        "domain": {
          "type": "string",
          "description": "The domain to filter the links by (e.g. `ac.me`). If not provided, all links for the workspace will be returned."
        },
        "tagIds": {
          "type": "string",
          "description": "The tag IDs to filter the links by."
        },
        "tagNames": {
          "type": "string",
          "description": "The unique name of the tags assigned to the short link (case insensitive)."
        },
        "folderId": {
          "type": "string",
          "description": "The folder ID to filter the links by."
        },
        "search": {
          "type": "string",
          "description": "Free-text search applied to the short link slug and destination URL."
        },
        "userId": {
          "type": "string",
          "description": "The user ID to filter the links by."
        },
        "tenantId": {
          "type": "string",
          "description": "The tenant ID (from your system) to filter the links by."
        },
        "showArchived": {
          "type": "boolean",
          "description": "Whether to include archived links in the response."
        },
        "sortBy": {
          "type": "string",
          "description": "The field to sort the links by."
        },
        "sortOrder": {
          "type": "string",
          "description": "The sort order."
        },
        "endingBefore": {
          "type": "string",
          "description": "Cursor pagination — only return results before this cursor. Mutually exclusive with `startingAfter`."
        },
        "startingAfter": {
          "type": "string",
          "description": "Cursor pagination — only return results after this cursor. Mutually exclusive with `endingBefore`."
        },
        "page": {
          "type": "number",
          "description": "Page number for pagination (deprecated — prefer cursor pagination)."
        },
        "pageSize": {
          "type": "number",
          "description": "Number of items per page (max 100)."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_dub_createLink",
    "description": "Create a link",
    "method": "POST",
    "path": "/links",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_dub_upsertLink",
    "description": "Upsert a link",
    "method": "PUT",
    "path": "/links",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_dub_getLinkInfo",
    "description": "Retrieve a link",
    "method": "GET",
    "path": "/links/info",
    "parameters": {
      "type": "object",
      "properties": {
        "domain": {
          "type": "string",
          "description": "The domain of the link to retrieve. E.g. for `d.to/github`, the domain is `d.to`."
        },
        "key": {
          "type": "string",
          "description": "The key of the link to retrieve. E.g. for `d.to/github`, the key is `github`."
        },
        "linkId": {
          "type": "string",
          "description": "The unique ID of the short link."
        },
        "externalId": {
          "type": "string",
          "description": "The external ID of the link in your database."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_dub_getLinksCount",
    "description": "Retrieve links count",
    "method": "GET",
    "path": "/links/count",
    "parameters": {
      "type": "object",
      "properties": {
        "domain": {
          "type": "string",
          "description": "Filter links by domain."
        },
        "tagIds": {
          "type": "string",
          "description": "The tag IDs to filter the links by."
        },
        "folderId": {
          "type": "string",
          "description": "The folder ID to filter the links by."
        },
        "search": {
          "type": "string",
          "description": "Free-text search applied to the short link slug and destination URL."
        },
        "userId": {
          "type": "string",
          "description": "Filter links by the creator's user ID."
        },
        "tenantId": {
          "type": "string",
          "description": "Filter links by tenant ID."
        },
        "showArchived": {
          "type": "boolean",
          "description": "Whether to include archived links."
        },
        "groupBy": {
          "type": "string",
          "description": "Group the count by a dimension."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_dub_updateLink",
    "description": "Update a link",
    "method": "PATCH",
    "path": "/links/{linkId}",
    "parameters": {
      "type": "object",
      "properties": {
        "linkId": {
          "type": "string",
          "description": "The id of the link to update. You may use either `linkId` (obtained via `/links/info`) or `externalId` prefixed with `ext_`."
        }
      },
      "required": [
        "linkId"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_deleteLink",
    "description": "Delete a link",
    "method": "DELETE",
    "path": "/links/{linkId}",
    "parameters": {
      "type": "object",
      "properties": {
        "linkId": {
          "type": "string",
          "description": "The id of the link to delete. You may use either `linkId` or `externalId` prefixed with `ext_`."
        }
      },
      "required": [
        "linkId"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_bulkCreateLinks",
    "description": "Bulk create links",
    "method": "POST",
    "path": "/links/bulk",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_dub_bulkUpdateLinks",
    "description": "Bulk update links",
    "method": "PATCH",
    "path": "/links/bulk",
    "parameters": {
      "type": "object",
      "properties": {
        "linkIds": {
          "type": "array",
          "description": "The IDs of the links to update. Takes precedence over `externalIds`."
        },
        "externalIds": {
          "type": "array",
          "description": "The external IDs of the links to update (as stored in your database)."
        },
        "data": {
          "type": "string",
          "description": "Partial link properties to apply to every targeted link. `domain`, `key`, `prefix`, and `keyLength` are ignored."
        }
      },
      "required": [
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_bulkDeleteLinks",
    "description": "Bulk delete links",
    "method": "DELETE",
    "path": "/links/bulk",
    "parameters": {
      "type": "object",
      "properties": {
        "linkIds": {
          "type": "array",
          "description": "Comma-separated list of link IDs to delete (max 100). Non-existing IDs are ignored."
        }
      },
      "required": [
        "linkIds"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_retrieveAnalytics",
    "description": "Retrieve analytics",
    "method": "GET",
    "path": "/analytics",
    "parameters": {
      "type": "object",
      "properties": {
        "event": {
          "type": "string",
          "description": "The type of event to retrieve analytics for."
        },
        "groupBy": {
          "type": "string",
          "description": "The dimension to group the analytics data points by."
        },
        "domain": {
          "type": "string",
          "description": "The domain to filter analytics for. Supports advanced filtering: comma-separated values or `-` exclusion prefix."
        },
        "key": {
          "type": "string",
          "description": "The slug of the short link to retrieve analytics for. Must be used with `domain`."
        },
        "linkId": {
          "type": "string",
          "description": "The unique ID of the link to retrieve analytics for."
        },
        "externalId": {
          "type": "string",
          "description": "The external ID (your DB ID) of the link, prefixed with `ext_`."
        },
        "tenantId": {
          "type": "string",
          "description": "The tenant ID to filter analytics by."
        },
        "tagId": {
          "type": "string",
          "description": "The tag ID to filter analytics by."
        },
        "folderId": {
          "type": "string",
          "description": "The folder ID to filter analytics by."
        },
        "groupId": {
          "type": "string",
          "description": "The partner-group ID to filter analytics by."
        },
        "partnerId": {
          "type": "string",
          "description": "The partner ID to filter analytics by."
        },
        "customerId": {
          "type": "string",
          "description": "The customer ID to filter analytics by."
        },
        "interval": {
          "type": "string",
          "description": "The interval to retrieve analytics for. Defaults to `24h`."
        },
        "start": {
          "type": "string",
          "description": "The start date and time. If set, takes precedence over `interval`."
        },
        "end": {
          "type": "string",
          "description": "The end date and time. If set with `start`, takes precedence over `interval`."
        },
        "timezone": {
          "type": "string",
          "description": "IANA time zone code (e.g. `America/New_York`) used to align timeseries granularity."
        },
        "country": {
          "type": "string",
          "description": "Filter by 2-letter ISO 3166-1 country code."
        },
        "city": {
          "type": "string",
          "description": "Filter by city."
        },
        "region": {
          "type": "string",
          "description": "Filter by ISO 3166-2 region code."
        },
        "continent": {
          "type": "string",
          "description": "Filter by continent (`AF`, `AN`, `AS`, `EU`, `NA`, `OC`, `SA`)."
        },
        "device": {
          "type": "string",
          "description": "Filter by device (e.g. `Desktop`, `Mobile`, `Tablet`)."
        },
        "browser": {
          "type": "string",
          "description": "Filter by browser (e.g. `Chrome`, `Firefox`)."
        },
        "os": {
          "type": "string",
          "description": "Filter by OS (e.g. `Mac`, `Windows`, `Linux`)."
        },
        "trigger": {
          "type": "string",
          "description": "Filter by trigger type (`qr`, `link`, `pageview`)."
        },
        "referer": {
          "type": "string",
          "description": "Filter by referer hostname (e.g. `google.com`)."
        },
        "refererUrl": {
          "type": "string",
          "description": "Filter by full referer URL."
        },
        "url": {
          "type": "string",
          "description": "Filter by destination URL."
        },
        "utm_source": {
          "type": "string",
          "description": "Filter by UTM source."
        },
        "utm_medium": {
          "type": "string",
          "description": "Filter by UTM medium."
        },
        "utm_campaign": {
          "type": "string",
          "description": "Filter by UTM campaign."
        },
        "utm_term": {
          "type": "string",
          "description": "Filter by UTM term."
        },
        "utm_content": {
          "type": "string",
          "description": "Filter by UTM content."
        },
        "root": {
          "type": "boolean",
          "description": "If `true`, filter for root domains; if `false`, links only; if undefined, return both."
        },
        "saleType": {
          "type": "string",
          "description": "Filter sales by type. Only applies to sale events."
        },
        "query": {
          "type": "string",
          "description": "Search events by a custom metadata value. Only available for lead and sale events. Examples: `metadata['key']:'value'`."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_dub_listEvents",
    "description": "Retrieve a list of events",
    "method": "GET",
    "path": "/events",
    "parameters": {
      "type": "object",
      "properties": {
        "event": {
          "type": "string",
          "description": "The type of event to retrieve."
        },
        "domain": {
          "type": "string",
          "description": "Filter by domain."
        },
        "key": {
          "type": "string",
          "description": "The slug of the short link. Must be used with `domain`."
        },
        "linkId": {
          "type": "string",
          "description": "Filter by link ID."
        },
        "externalId": {
          "type": "string",
          "description": "Filter by external ID (prefixed with `ext_`)."
        },
        "tenantId": {
          "type": "string",
          "description": "Filter by tenant ID."
        },
        "tagId": {
          "type": "string",
          "description": "Filter by tag ID."
        },
        "folderId": {
          "type": "string",
          "description": "Filter by folder ID."
        },
        "partnerId": {
          "type": "string",
          "description": "Filter by partner ID."
        },
        "customerId": {
          "type": "string",
          "description": "Filter by customer ID."
        },
        "interval": {
          "type": "string",
          "description": "The interval to retrieve events for."
        },
        "start": {
          "type": "string",
          "description": "The start date and time."
        },
        "end": {
          "type": "string",
          "description": "The end date and time."
        },
        "timezone": {
          "type": "string",
          "description": "IANA time zone code."
        },
        "country": {
          "type": "string",
          "description": "Filter by 2-letter ISO 3166-1 country code."
        },
        "city": {
          "type": "string",
          "description": "Filter by city."
        },
        "region": {
          "type": "string",
          "description": "Filter by region."
        },
        "continent": {
          "type": "string",
          "description": "Filter by continent."
        },
        "device": {
          "type": "string",
          "description": "Filter by device."
        },
        "browser": {
          "type": "string",
          "description": "Filter by browser."
        },
        "os": {
          "type": "string",
          "description": "Filter by OS."
        },
        "trigger": {
          "type": "string",
          "description": "Filter by trigger."
        },
        "referer": {
          "type": "string",
          "description": "Filter by referer hostname."
        },
        "refererUrl": {
          "type": "string",
          "description": "Filter by full referer URL."
        },
        "url": {
          "type": "string",
          "description": "Filter by destination URL."
        },
        "utm_source": {
          "type": "string",
          "description": "utm_source"
        },
        "utm_medium": {
          "type": "string",
          "description": "utm_medium"
        },
        "utm_campaign": {
          "type": "string",
          "description": "utm_campaign"
        },
        "utm_term": {
          "type": "string",
          "description": "utm_term"
        },
        "utm_content": {
          "type": "string",
          "description": "utm_content"
        },
        "saleType": {
          "type": "string",
          "description": "saleType"
        },
        "sortOrder": {
          "type": "string",
          "description": "The sort order."
        },
        "sortBy": {
          "type": "string",
          "description": "The field to sort the events by."
        },
        "page": {
          "type": "number",
          "description": "Page number for pagination."
        },
        "limit": {
          "type": "number",
          "description": "Number of items per page (max 100)."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_dub_getTags",
    "description": "Retrieve a list of tags",
    "method": "GET",
    "path": "/tags",
    "parameters": {
      "type": "object",
      "properties": {
        "sortBy": {
          "type": "string",
          "description": "The field to sort the tags by."
        },
        "sortOrder": {
          "type": "string",
          "description": "The order to sort the tags by."
        },
        "search": {
          "type": "string",
          "description": "The search term to filter the tags by."
        },
        "ids": {
          "type": "string",
          "description": "IDs of tags to filter by."
        },
        "page": {
          "type": "number",
          "description": "The page number for pagination."
        },
        "pageSize": {
          "type": "number",
          "description": "The number of items per page."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_dub_createTag",
    "description": "Create a tag",
    "method": "POST",
    "path": "/tags",
    "parameters": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "The name of the tag to create."
        },
        "color": {
          "type": "string",
          "description": "The color of the tag. If not provided, a random color will be assigned."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_dub_updateTag",
    "description": "Update a tag",
    "method": "PATCH",
    "path": "/tags/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the tag to update."
        },
        "name": {
          "type": "string",
          "description": "The new name of the tag."
        },
        "color": {
          "type": "string",
          "description": "The new color of the tag."
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_listFolders",
    "description": "Retrieve a list of folders",
    "method": "GET",
    "path": "/folders",
    "parameters": {
      "type": "object",
      "properties": {
        "search": {
          "type": "string",
          "description": "Free-text search applied to folder names."
        },
        "page": {
          "type": "number",
          "description": "Page number for pagination."
        },
        "pageSize": {
          "type": "number",
          "description": "Number of items per page."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_dub_createFolder",
    "description": "Create a folder",
    "method": "POST",
    "path": "/folders",
    "parameters": {
      "type": "object",
      "properties": {
        "name": {
          "type": "string",
          "description": "The name of the folder."
        },
        "accessLevel": {
          "type": "string",
          "description": "Workspace access level for the folder. `null` makes the folder private to its creator."
        }
      },
      "required": [
        "name"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_updateFolder",
    "description": "Update a folder",
    "method": "PATCH",
    "path": "/folders/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the folder to update."
        },
        "name": {
          "type": "string",
          "description": "The new name of the folder."
        },
        "accessLevel": {
          "type": "string",
          "description": "Workspace access level for the folder."
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_deleteFolder",
    "description": "Delete a folder",
    "method": "DELETE",
    "path": "/folders/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The ID of the folder to delete."
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_listCustomers",
    "description": "Retrieve a list of customers",
    "method": "GET",
    "path": "/customers",
    "parameters": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "description": "Filter customers by email address."
        },
        "externalId": {
          "type": "string",
          "description": "Filter customers by external ID (your DB ID)."
        },
        "search": {
          "type": "string",
          "description": "Free-text search applied to customer email and name."
        },
        "country": {
          "type": "string",
          "description": "Filter customers by 2-letter ISO 3166-1 country code."
        },
        "includeExpandedFields": {
          "type": "boolean",
          "description": "Whether to expand related fields like the customer's link, partner, and discount."
        },
        "sortBy": {
          "type": "string",
          "description": "The field to sort the customers by."
        },
        "sortOrder": {
          "type": "string",
          "description": "The sort order."
        },
        "page": {
          "type": "number",
          "description": "Page number for pagination."
        },
        "pageSize": {
          "type": "number",
          "description": "Number of items per page."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_dub_getCustomer",
    "description": "Retrieve a customer",
    "method": "GET",
    "path": "/customers/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The customer ID. May be the Dub customer ID or the external ID prefixed with `ext_`."
        },
        "includeExpandedFields": {
          "type": "boolean",
          "description": "Whether to expand related fields."
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_updateCustomer",
    "description": "Update a customer",
    "method": "PATCH",
    "path": "/customers/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The customer ID."
        },
        "externalId": {
          "type": "string",
          "description": "The external ID of the customer in your system."
        },
        "name": {
          "type": "string",
          "description": "The customer's display name."
        },
        "email": {
          "type": "string",
          "description": "The customer's email address."
        },
        "avatar": {
          "type": "string",
          "description": "URL to the customer's avatar image."
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_deleteCustomer",
    "description": "Delete a customer",
    "method": "DELETE",
    "path": "/customers/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The customer ID."
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_createDomain",
    "description": "Create a domain",
    "method": "POST",
    "path": "/domains",
    "parameters": {
      "type": "object",
      "properties": {
        "slug": {
          "type": "string",
          "description": "The custom domain name (e.g. `acme.link`)."
        },
        "expiredUrl": {
          "type": "string",
          "description": "The URL to redirect to when a link on this domain has expired."
        },
        "notFoundUrl": {
          "type": "string",
          "description": "The URL to redirect to when a link on this domain is not found."
        },
        "placeholder": {
          "type": "string",
          "description": "Placeholder URL shown in the link builder."
        },
        "logo": {
          "type": "string",
          "description": "Logo URL displayed on the domain's landing page."
        }
      },
      "required": [
        "slug"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_updateDomain",
    "description": "Update a domain",
    "method": "PATCH",
    "path": "/domains/{slug}",
    "parameters": {
      "type": "object",
      "properties": {
        "slug": {
          "type": "string",
          "description": "The domain slug to update (e.g. `acme.link`)."
        },
        "expiredUrl": {
          "type": "string",
          "description": "expiredUrl"
        },
        "notFoundUrl": {
          "type": "string",
          "description": "notFoundUrl"
        },
        "placeholder": {
          "type": "string",
          "description": "placeholder"
        },
        "logo": {
          "type": "string",
          "description": "logo"
        }
      },
      "required": [
        "slug"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_deleteDomain",
    "description": "Delete a domain",
    "method": "DELETE",
    "path": "/domains/{slug}",
    "parameters": {
      "type": "object",
      "properties": {
        "slug": {
          "type": "string",
          "description": "The domain slug to delete."
        }
      },
      "required": [
        "slug"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_trackLead",
    "description": "Track a lead",
    "method": "POST",
    "path": "/track/lead",
    "parameters": {
      "type": "object",
      "properties": {
        "clickId": {
          "type": "string",
          "description": "The unique ID of the click that the lead conversion event is attributed to. Read this from the `dub_id` cookie. For deferred lead tracking, an empty string lets Dub look up the click ID from the existing customer."
        },
        "eventName": {
          "type": "string",
          "description": "The name of the lead event to track. Doubles as a unique identifier when associating subsequent sale events."
        },
        "customerExternalId": {
          "type": "string",
          "description": "The unique ID of the customer in your system. Used to attribute all future events to this customer."
        },
        "customerName": {
          "type": "string",
          "description": "The customer's display name. If not passed, a random name will be generated."
        },
        "customerEmail": {
          "type": "string",
          "description": "The customer's email address."
        },
        "customerAvatar": {
          "type": "string",
          "description": "URL to the customer's avatar."
        },
        "mode": {
          "type": "string",
          "description": "`async` does not block; `wait` blocks until the event is recorded; `deferred` defers creation to a subsequent request."
        },
        "eventQuantity": {
          "type": "number",
          "description": "Numerical value associated with the lead event. If defined as N, the lead event will be tracked N times."
        },
        "metadata": {
          "type": "object",
          "description": "Additional metadata to be stored with the lead event. Max 10,000 characters when stringified."
        }
      },
      "required": [
        "clickId",
        "eventName",
        "customerExternalId"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_trackSale",
    "description": "Track a sale",
    "method": "POST",
    "path": "/track/sale",
    "parameters": {
      "type": "object",
      "properties": {
        "customerExternalId": {
          "type": "string",
          "description": "The unique ID of the customer in your system."
        },
        "amount": {
          "type": "integer",
          "description": "The amount of the sale in cents (for two-decimal currencies). For zero-decimal currencies (e.g. JPY), pass the full integer value."
        },
        "currency": {
          "type": "string",
          "description": "ISO 4217 currency code. Sales are stored as USD using the latest exchange rate."
        },
        "eventName": {
          "type": "string",
          "description": "The name of the sale event (e.g. `Invoice paid` or `Subscription created`)."
        },
        "paymentProcessor": {
          "type": "string",
          "description": "The payment processor via which the sale was made."
        },
        "invoiceId": {
          "type": "string",
          "description": "Invoice ID, used as an idempotency key — only one sale event can be recorded per invoice ID."
        },
        "metadata": {
          "type": "object",
          "description": "Additional metadata to be stored with the sale event. Max 10,000 characters."
        },
        "leadEventName": {
          "type": "string",
          "description": "Name of the lead event that occurred before the sale (case-sensitive). Used to associate the sale with a particular lead."
        },
        "clickId": {
          "type": "string",
          "description": "[For direct sale tracking] The unique click ID. Read from the `dub_id` cookie."
        },
        "customerName": {
          "type": "string",
          "description": "[For direct sale tracking] The customer's display name."
        },
        "customerEmail": {
          "type": "string",
          "description": "[For direct sale tracking] The customer's email address."
        },
        "customerAvatar": {
          "type": "string",
          "description": "[For direct sale tracking] URL to the customer's avatar."
        }
      },
      "required": [
        "customerExternalId",
        "amount"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_listPartners",
    "description": "List partners",
    "method": "GET",
    "path": "/partners",
    "parameters": {
      "type": "object",
      "properties": {
        "groupId": {
          "type": "string",
          "description": "Filter partners by their `groupId`."
        },
        "status": {
          "type": "string",
          "description": "Filter partners by enrollment status."
        },
        "country": {
          "type": "string",
          "description": "Filter partners by ISO 3166-1 alpha-2 country code."
        },
        "sortBy": {
          "type": "string",
          "description": "Field to sort the partners by."
        },
        "sortOrder": {
          "type": "string",
          "description": "Sort order."
        },
        "email": {
          "type": "string",
          "description": "Filter by partner email (takes precedence over `search`)."
        },
        "tenantId": {
          "type": "string",
          "description": "Filter by the partner's `tenantId` in your system (takes precedence over `email` and `search`)."
        },
        "search": {
          "type": "string",
          "description": "Free-text search applied to partner ID, name, email, or link."
        },
        "page": {
          "type": "number",
          "description": "Page number for pagination."
        },
        "pageSize": {
          "type": "number",
          "description": "Number of items per page (max 100)."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_dub_createPartner",
    "description": "Create or update a partner",
    "method": "POST",
    "path": "/partners",
    "parameters": {
      "type": "object",
      "properties": {
        "email": {
          "type": "string",
          "description": "The partner's email address. They can claim their profile at `partners.dub.co` with this email."
        },
        "name": {
          "type": "string",
          "description": "The partner's full name. Defaults to their email if omitted."
        },
        "username": {
          "type": "string",
          "description": "The partner's unique username in your system. Used to build their default short link."
        },
        "image": {
          "type": "string",
          "description": "The partner's avatar image URL."
        },
        "tenantId": {
          "type": "string",
          "description": "The partner's unique ID in your system. Used to retrieve their links and stats later."
        },
        "groupId": {
          "type": "string",
          "description": "The group ID to add the partner to. Defaults to the program's default group."
        },
        "country": {
          "type": "string",
          "description": "The partner's country (ISO 3166-1 alpha-2)."
        },
        "description": {
          "type": "string",
          "description": "Brief description of the partner and their background."
        },
        "linkProps": {
          "type": "string",
          "description": "linkProps"
        }
      },
      "required": [
        "email"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_retrievePartnerLinks",
    "description": "Retrieve a partner's links",
    "method": "GET",
    "path": "/partners/links",
    "parameters": {
      "type": "object",
      "properties": {
        "partnerId": {
          "type": "string",
          "description": "The Dub partner ID. Takes precedence over `tenantId` if both are provided."
        },
        "tenantId": {
          "type": "string",
          "description": "The partner's ID in your system. At least one of `partnerId` or `tenantId` is required."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_dub_createPartnerLink",
    "description": "Create a partner link",
    "method": "POST",
    "path": "/partners/links",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_dub_upsertPartnerLink",
    "description": "Upsert a partner link",
    "method": "PUT",
    "path": "/partners/links/upsert",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_dub_banPartner",
    "description": "Ban a partner",
    "method": "POST",
    "path": "/partners/ban",
    "parameters": {
      "type": "object",
      "properties": {
        "partnerId": {
          "type": "string",
          "description": "The Dub partner ID. Takes precedence over `tenantId` if both are provided."
        },
        "tenantId": {
          "type": "string",
          "description": "The partner's ID in your system. At least one of `partnerId` or `tenantId` is required."
        },
        "reason": {
          "type": "string",
          "description": "The reason for the ban."
        }
      },
      "required": [
        "reason"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_deactivatePartner",
    "description": "Deactivate a partner",
    "method": "POST",
    "path": "/partners/deactivate",
    "parameters": {
      "type": "object",
      "properties": {
        "partnerId": {
          "type": "string",
          "description": "The Dub partner ID. Takes precedence over `tenantId` if both are provided."
        },
        "tenantId": {
          "type": "string",
          "description": "The partner's ID in your system. At least one of `partnerId` or `tenantId` is required."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_dub_listBountySubmissions",
    "description": "List bounty submissions",
    "method": "GET",
    "path": "/bounties/{bountyId}/submissions",
    "parameters": {
      "type": "object",
      "properties": {
        "bountyId": {
          "type": "string",
          "description": "The bounty ID on Dub (prefixed with `bnty_`). Found in the URL of the bounty page."
        },
        "status": {
          "type": "string",
          "description": "Filter submissions by status."
        },
        "groupId": {
          "type": "string",
          "description": "Filter submissions by partner group."
        },
        "partnerId": {
          "type": "string",
          "description": "Filter submissions by partner."
        },
        "sortBy": {
          "type": "string",
          "description": "Field to sort the submissions by."
        },
        "sortOrder": {
          "type": "string",
          "description": "Sort order."
        },
        "page": {
          "type": "number",
          "description": "Page number for pagination."
        },
        "pageSize": {
          "type": "number",
          "description": "Number of items per page (max 100)."
        }
      },
      "required": [
        "bountyId"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_approveBountySubmission",
    "description": "Approve a bounty submission",
    "method": "POST",
    "path": "/bounties/{bountyId}/submissions/{submissionId}/approve",
    "parameters": {
      "type": "object",
      "properties": {
        "bountyId": {
          "type": "string",
          "description": "The ID of the bounty."
        },
        "submissionId": {
          "type": "string",
          "description": "The ID of the bounty submission."
        },
        "rewardAmount": {
          "type": "number",
          "description": "Custom reward amount (in cents). Only applicable to performance-based bounties whose reward amount is not preset."
        }
      },
      "required": [
        "bountyId",
        "submissionId"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_rejectBountySubmission",
    "description": "Reject a bounty submission",
    "method": "POST",
    "path": "/bounties/{bountyId}/submissions/{submissionId}/reject",
    "parameters": {
      "type": "object",
      "properties": {
        "bountyId": {
          "type": "string",
          "description": "The ID of the bounty."
        },
        "submissionId": {
          "type": "string",
          "description": "The ID of the bounty submission."
        },
        "rejectionReason": {
          "type": "string",
          "description": "The reason for rejecting the submission."
        },
        "rejectionNote": {
          "type": "string",
          "description": "Optional free-form note explaining the rejection (visible to the partner)."
        }
      },
      "required": [
        "bountyId",
        "submissionId"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_listCommissions",
    "description": "List commissions",
    "method": "GET",
    "path": "/commissions",
    "parameters": {
      "type": "object",
      "properties": {
        "type": {
          "type": "string",
          "description": "Filter by commission type."
        },
        "customerId": {
          "type": "string",
          "description": "Filter by associated customer."
        },
        "payoutId": {
          "type": "string",
          "description": "Filter by associated payout."
        },
        "partnerId": {
          "type": "string",
          "description": "Filter by associated partner. Takes precedence over `tenantId`."
        },
        "tenantId": {
          "type": "string",
          "description": "Filter by the partner's `tenantId` in your system."
        },
        "groupId": {
          "type": "string",
          "description": "Filter by partner group."
        },
        "invoiceId": {
          "type": "string",
          "description": "Filter by associated invoice. Returns at most one commission per invoice."
        },
        "status": {
          "type": "string",
          "description": "Filter by commission status."
        },
        "sortBy": {
          "type": "string",
          "description": "Field to sort by."
        },
        "sortOrder": {
          "type": "string",
          "description": "Sort order."
        },
        "interval": {
          "type": "string",
          "description": "Convenience time range filter."
        },
        "start": {
          "type": "string",
          "description": "Start of the date range (ISO-8601). Use with `end` to override `interval`."
        },
        "end": {
          "type": "string",
          "description": "End of the date range (ISO-8601)."
        },
        "timezone": {
          "type": "string",
          "description": "IANA timezone (e.g. `America/New_York`) used to interpret `start`/`end` and `interval`."
        },
        "endingBefore": {
          "type": "string",
          "description": "Cursor pagination — only return results before this commission ID."
        },
        "startingAfter": {
          "type": "string",
          "description": "Cursor pagination — only return results after this commission ID."
        },
        "page": {
          "type": "number",
          "description": "Deprecated. Use `startingAfter` instead."
        },
        "pageSize": {
          "type": "number",
          "description": "Number of items per page (max 100)."
        }
      }
    }
  },
  {
    "name": "superagnt_connection_dub_updateCommission",
    "description": "Update a commission",
    "method": "PATCH",
    "path": "/commissions/{id}",
    "parameters": {
      "type": "object",
      "properties": {
        "id": {
          "type": "string",
          "description": "The commission's unique ID on Dub (e.g. `cm_1JVR7XRCSR0EDBAF39FZ4PMYE`)."
        },
        "saleAmount": {
          "type": "number",
          "description": "New absolute sale amount (in cents). Paid commissions cannot be updated."
        },
        "modifySaleAmount": {
          "type": "number",
          "description": "Delta to apply to the current sale amount (positive to increase, negative to decrease). Takes precedence over `saleAmount`."
        },
        "earnings": {
          "type": "number",
          "description": "New absolute earnings (for `custom` commissions)."
        },
        "currency": {
          "type": "string",
          "description": "ISO 4217 currency code for the sale amount."
        },
        "status": {
          "type": "string",
          "description": "New status. Takes precedence over `saleAmount`/`modifySaleAmount`. Marking as anything other than `pending` removes the commission from its payout and recalculates the payout amount."
        },
        "amount": {
          "type": "number",
          "description": "Deprecated — use `saleAmount`."
        },
        "modifyAmount": {
          "type": "number",
          "description": "Deprecated — use `modifySaleAmount`."
        }
      },
      "required": [
        "id"
      ]
    }
  },
  {
    "name": "superagnt_connection_dub_listPayouts",
    "description": "List payouts",
    "method": "GET",
    "path": "/payouts",
    "parameters": {
      "type": "object",
      "properties": {
        "status": {
          "type": "string",
          "description": "Filter payouts by status."
        },
        "partnerId": {
          "type": "string",
          "description": "Filter by associated partner. Takes precedence over `tenantId`."
        },
        "tenantId": {
          "type": "string",
          "description": "Filter by the partner's `tenantId` in your system."
        },
        "invoiceId": {
          "type": "string",
          "description": "Filter by invoice ID. Pending payouts do not have an invoice ID."
        },
        "sortBy": {
          "type": "string",
          "description": "Field to sort by."
        },
        "sortOrder": {
          "type": "string",
          "description": "Sort order."
        },
        "page": {
          "type": "number",
          "description": "Page number for pagination."
        },
        "pageSize": {
          "type": "number",
          "description": "Number of items per page (max 100)."
        }
      }
    }
  }
]
```

## Example

```bash
curl -X GET &#x27;https://api.superagnt.com/v1/connections/dub/links&#x27; \
  -H &#x27;Authorization: Bearer $SUPERAGNT_API_KEY&#x27;
```

## Use Cases

- Programmatically generate millions of branded short links from your CRM
- Track sign-ups and purchases as conversions on referral and marketing links
- Build dashboards showing link clicks, leads, and revenue by campaign
- Sync customers and conversion events into your data warehouse
- Automate UTM tagging and A/B test rotation for outbound campaigns
- Power affiliate and partner programs with attributed short links

## Links

- [Documentation](https://superagnt.com/r/ch-dub-links-docs)
- [superagnt app / API keys](https://superagnt.com/r/ch-dub-links-key)
- [Connections page](https://app.superagnt.com/dashboard/connections)
- [This listing](https://clawhub.ai/superagnt/skills/dub-links)
