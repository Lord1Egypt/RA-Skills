---
name: attio-crm
description: "Manage Attio CRM records, lists, notes, tasks, and meetings through the superagnt unified API."
version: 2.0.14
author: superagnt
license: MIT-0
platforms: [macos, linux, windows]
required_environment_variables:
  - SUPERAGNT_API_KEY
metadata:
  hermes:
    tags: [attio, integration, api, ai-agent]
  openclaw:
    requires:
      env:
        - SUPERAGNT_API_KEY
      bins:
        - curl
    primaryEnv: SUPERAGNT_API_KEY
    emoji: "🗂️"
    homepage: https://superagnt.com/r/ch-attio-crm-docs
---

# Attio Integration

The Attio integration connects your Attio workspace to superagnt, letting AI agents and workflows manage records, lists, attributes, notes, tasks, threads, comments, meetings, and call recordings programmatically. Supports the full Attio v2 REST API surface — including custom objects and attributes, list entries, SCIM, and webhooks — proxied through your superagnt API key.

## Alternative install: the MCP server

If this client speaks MCP, you can connect the workspace server instead of
using this skill's curl calls — after the user connects their
Attio account in the superagnt app, the same endpoints below are exposed
as native MCP tools:

```
https://mcp.superagnt.com/mcp
```

The URL publishes full OAuth discovery — an MCP-capable client needs the URL
and nothing else (approve once in the browser). Per-client setup lines:
https://www.superagnt.com/install

Everything below works on curl-only environments with just the API key.

## Capabilities and safety

This skill documents the Attio API surface the user's connected
account can reach — which can include destructive operations (updates,
deletes) and, where the vendor supports them, actions performed as the user
(sending messages, modifying records, changing settings). Two hard rules:

- **Confirm before destructive or outbound actions.** Never delete, overwrite,
  or send on the user's behalf without their explicit confirmation in the
  conversation.
- **Stay inside the user's request.** Use only the endpoints the task needs;
  this skill grants no access beyond the Attio connection the user
  set up themselves.

## Prerequisites

1. An API key — get one from the [superagnt app](https://superagnt.com/r/ch-attio-crm-key) and export it as
   `SUPERAGNT_API_KEY`.
2. A connected Attio account — connect it on the
   [Connections page](https://app.superagnt.com/dashboard/connections). Calls fail with a clear error
   until the vendor is connected; that error is the signal to send the user to
   the connections page, not a bug.

Note: `/v1/connections/*` calls run on the USER'S Attio credentials —
vendor-side rate limits and billing are theirs, not platform credits.

## Authentication

```
Authorization: Bearer $SUPERAGNT_API_KEY
```

If the variable is not set, ask the user for their key or point them at
https://superagnt.com/r/ch-attio-crm-key.

## Verify the install (do this first)

```bash
curl -s https://api.superagnt.com/v1/credits \
  -H &#x27;Authorization: Bearer $SUPERAGNT_API_KEY&#x27;
```

A JSON result proves the key end to end. 401 = bad key; an error naming the
connection means the Attio account is not connected yet.

## Base URL

```
https://api.superagnt.com/v1/connections/attio
```

## Available Endpoints

| Method | Path | Summary |
|--------|------|---------|
| `GET` | `/v2/objects` | List objects |
| `POST` | `/v2/objects` | Create an object |
| `GET` | `/v2/objects/{object}` | Get an object |
| `PATCH` | `/v2/objects/{object}` | Update an object |
| `GET` | `/v2/objects/{object}/views` | List views for object |
| `GET` | `/v2/{target}/{identifier}/attributes` | List attributes |
| `POST` | `/v2/{target}/{identifier}/attributes` | Create an attribute |
| `GET` | `/v2/{target}/{identifier}/attributes/{attribute}` | Get an attribute |
| `PATCH` | `/v2/{target}/{identifier}/attributes/{attribute}` | Update an attribute |
| `GET` | `/v2/{target}/{identifier}/attributes/{attribute}/options` | List select options |
| `POST` | `/v2/{target}/{identifier}/attributes/{attribute}/options` | Create a select option |
| `PATCH` | `/v2/{target}/{identifier}/attributes/{attribute}/options/{option}` | Update a select option |
| `GET` | `/v2/{target}/{identifier}/attributes/{attribute}/statuses` | List statuses |
| `POST` | `/v2/{target}/{identifier}/attributes/{attribute}/statuses` | Create a status |
| `PATCH` | `/v2/{target}/{identifier}/attributes/{attribute}/statuses/{status}` | Update a status |
| `POST` | `/v2/objects/{object}/records/query` | List records |
| `POST` | `/v2/objects/{object}/records` | Create a record |
| `PUT` | `/v2/objects/{object}/records` | Assert a record |
| `GET` | `/v2/objects/{object}/records/{record_id}` | Get a record |
| `PUT` | `/v2/objects/{object}/records/{record_id}` | Update a record (overwrite multiselect values) |
| `PATCH` | `/v2/objects/{object}/records/{record_id}` | Update a record (append multiselect values) |
| `DELETE` | `/v2/objects/{object}/records/{record_id}` | Delete a record |
| `GET` | `/v2/objects/{object}/records/{record_id}/attributes/{attribute}/values` | List record attribute values |
| `GET` | `/v2/objects/{object}/records/{record_id}/entries` | List record entries |
| `POST` | `/v2/objects/records/search` | Search records |
| `GET` | `/v2/lists` | List all lists |
| `POST` | `/v2/lists` | Create a list |
| `GET` | `/v2/lists/{list}` | Get a list |
| `PATCH` | `/v2/lists/{list}` | Update a list |
| `GET` | `/v2/lists/{list}/views` | List views for list |
| `POST` | `/v2/lists/{list}/entries/query` | List entries |
| `POST` | `/v2/lists/{list}/entries` | Create an entry (add record to list) |
| `PUT` | `/v2/lists/{list}/entries` | Assert a list entry by parent |
| `GET` | `/v2/lists/{list}/entries/{entry_id}` | Get a list entry |
| `PUT` | `/v2/lists/{list}/entries/{entry_id}` | Update a list entry (overwrite multiselect values) |
| `PATCH` | `/v2/lists/{list}/entries/{entry_id}` | Update a list entry (append multiselect values) |
| `DELETE` | `/v2/lists/{list}/entries/{entry_id}` | Delete a list entry |
| `GET` | `/v2/lists/{list}/entries/{entry_id}/attributes/{attribute}/values` | List attribute values for a list entry |
| `GET` | `/v2/workspace_members` | List workspace members |
| `GET` | `/v2/workspace_members/{workspace_member_id}` | Get a workspace member |
| `GET` | `/v2/notes` | List notes |
| `POST` | `/v2/notes` | Create a note |
| `GET` | `/v2/notes/{note_id}` | Get a note |
| `DELETE` | `/v2/notes/{note_id}` | Delete a note |
| `GET` | `/v2/tasks` | List tasks |
| `POST` | `/v2/tasks` | Create a task |
| `GET` | `/v2/tasks/{task_id}` | Get a task |
| `PATCH` | `/v2/tasks/{task_id}` | Update a task |
| `DELETE` | `/v2/tasks/{task_id}` | Delete a task |
| `GET` | `/v2/threads` | List threads |
| `GET` | `/v2/threads/{thread_id}` | Get a thread |
| `POST` | `/v2/comments` | Create a comment |
| `GET` | `/v2/comments/{comment_id}` | Get a comment |
| `DELETE` | `/v2/comments/{comment_id}` | Delete a comment |
| `GET` | `/v2/meetings` | List meetings |
| `POST` | `/v2/meetings` | Find or create a meeting |
| `GET` | `/v2/meetings/{meeting_id}` | Get a meeting |
| `GET` | `/v2/meetings/{meeting_id}/call_recordings` | List call recordings |
| `POST` | `/v2/meetings/{meeting_id}/call_recordings` | Create call recording |
| `GET` | `/v2/meetings/{meeting_id}/call_recordings/{call_recording_id}` | Get call recording |
| `DELETE` | `/v2/meetings/{meeting_id}/call_recordings/{call_recording_id}` | Delete call recording |
| `GET` | `/v2/meetings/{meeting_id}/call_recordings/{call_recording_id}/transcript` | Get call transcript |
| `GET` | `/v2/files` | List files |
| `POST` | `/v2/files` | Create a folder |
| `POST` | `/v2/files/upload` | Upload a file |
| `GET` | `/v2/files/{file_id}` | Get a file |
| `DELETE` | `/v2/files/{file_id}` | Delete a file |
| `GET` | `/v2/files/{file_id}/download` | Download a file |
| `GET` | `/scim/v2/Schemas` | List SCIM schemas |
| `GET` | `/scim/v2/Users` | List SCIM users |
| `POST` | `/scim/v2/Users` | Create SCIM user |
| `GET` | `/scim/v2/Groups` | List SCIM groups |
| `POST` | `/scim/v2/Groups` | Create SCIM group |
| `GET` | `/scim/v2/Users/{user_id}` | Get SCIM user |
| `PUT` | `/scim/v2/Users/{user_id}` | Update SCIM user |
| `PATCH` | `/scim/v2/Users/{user_id}` | Patch SCIM user |
| `DELETE` | `/scim/v2/Users/{user_id}` | Delete SCIM user |
| `GET` | `/scim/v2/Groups/{workspace_team_id}` | Get SCIM group |
| `PUT` | `/scim/v2/Groups/{workspace_team_id}` | Update SCIM group |
| `PATCH` | `/scim/v2/Groups/{workspace_team_id}` | Patch SCIM group |
| `DELETE` | `/scim/v2/Groups/{workspace_team_id}` | Delete SCIM group |
| `GET` | `/v2/webhooks` | List webhooks |
| `POST` | `/v2/webhooks` | Create a webhook |
| `GET` | `/v2/webhooks/{webhook_id}` | Get a webhook |
| `PATCH` | `/v2/webhooks/{webhook_id}` | Update a webhook |
| `DELETE` | `/v2/webhooks/{webhook_id}` | Delete a webhook |
| `GET` | `/v2/self` | Identify |

## Tool Schemas

The following JSON defines every operation with its parameters. Each tool maps
to an API endpoint under the base URL.

```json
[
  {
    "name": "superagnt_connection_attio_get_v2_objects",
    "description": "List objects",
    "method": "GET",
    "path": "/v2/objects",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_attio_post_v2_objects",
    "description": "Create an object",
    "method": "POST",
    "path": "/v2/objects",
    "parameters": {
      "type": "object",
      "properties": {
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_objects__object_",
    "description": "Get an object",
    "method": "GET",
    "path": "/v2/objects/{object}",
    "parameters": {
      "type": "object",
      "properties": {
        "object": {
          "type": "string",
          "description": "object"
        }
      },
      "required": [
        "object"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_patch_v2_objects__object_",
    "description": "Update an object",
    "method": "PATCH",
    "path": "/v2/objects/{object}",
    "parameters": {
      "type": "object",
      "properties": {
        "object": {
          "type": "string",
          "description": "object"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "object",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_objects__object__views",
    "description": "List views for object",
    "method": "GET",
    "path": "/v2/objects/{object}/views",
    "parameters": {
      "type": "object",
      "properties": {
        "object": {
          "type": "string",
          "description": "object"
        },
        "show_archived": {
          "type": "boolean",
          "description": "show_archived"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "cursor": {
          "type": "string",
          "description": "cursor"
        }
      },
      "required": [
        "object"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_list_attributes",
    "description": "List attributes",
    "method": "GET",
    "path": "/v2/{target}/{identifier}/attributes",
    "parameters": {
      "type": "object",
      "properties": {
        "target": {
          "type": "string",
          "description": "target"
        },
        "identifier": {
          "type": "string",
          "description": "identifier"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "offset": {
          "type": "integer",
          "description": "offset"
        },
        "show_archived": {
          "type": "boolean",
          "description": "show_archived"
        }
      },
      "required": [
        "target",
        "identifier"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_create_attribute",
    "description": "Create an attribute",
    "method": "POST",
    "path": "/v2/{target}/{identifier}/attributes",
    "parameters": {
      "type": "object",
      "properties": {
        "target": {
          "type": "string",
          "description": "target"
        },
        "identifier": {
          "type": "string",
          "description": "identifier"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "target",
        "identifier",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_attribute",
    "description": "Get an attribute",
    "method": "GET",
    "path": "/v2/{target}/{identifier}/attributes/{attribute}",
    "parameters": {
      "type": "object",
      "properties": {
        "target": {
          "type": "string",
          "description": "target"
        },
        "identifier": {
          "type": "string",
          "description": "identifier"
        },
        "attribute": {
          "type": "string",
          "description": "attribute"
        }
      },
      "required": [
        "target",
        "identifier",
        "attribute"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_update_attribute",
    "description": "Update an attribute",
    "method": "PATCH",
    "path": "/v2/{target}/{identifier}/attributes/{attribute}",
    "parameters": {
      "type": "object",
      "properties": {
        "target": {
          "type": "string",
          "description": "target"
        },
        "identifier": {
          "type": "string",
          "description": "identifier"
        },
        "attribute": {
          "type": "string",
          "description": "attribute"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "target",
        "identifier",
        "attribute",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_list_attribute_options",
    "description": "List select options",
    "method": "GET",
    "path": "/v2/{target}/{identifier}/attributes/{attribute}/options",
    "parameters": {
      "type": "object",
      "properties": {
        "target": {
          "type": "string",
          "description": "target"
        },
        "identifier": {
          "type": "string",
          "description": "identifier"
        },
        "attribute": {
          "type": "string",
          "description": "attribute"
        },
        "show_archived": {
          "type": "boolean",
          "description": "show_archived"
        }
      },
      "required": [
        "target",
        "identifier",
        "attribute"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_create_attribute_option",
    "description": "Create a select option",
    "method": "POST",
    "path": "/v2/{target}/{identifier}/attributes/{attribute}/options",
    "parameters": {
      "type": "object",
      "properties": {
        "target": {
          "type": "string",
          "description": "target"
        },
        "identifier": {
          "type": "string",
          "description": "identifier"
        },
        "attribute": {
          "type": "string",
          "description": "attribute"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "target",
        "identifier",
        "attribute",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_update_attribute_option",
    "description": "Update a select option",
    "method": "PATCH",
    "path": "/v2/{target}/{identifier}/attributes/{attribute}/options/{option}",
    "parameters": {
      "type": "object",
      "properties": {
        "target": {
          "type": "string",
          "description": "target"
        },
        "identifier": {
          "type": "string",
          "description": "identifier"
        },
        "attribute": {
          "type": "string",
          "description": "attribute"
        },
        "option": {
          "type": "string",
          "description": "option"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "target",
        "identifier",
        "attribute",
        "option",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_list_attribute_statuses",
    "description": "List statuses",
    "method": "GET",
    "path": "/v2/{target}/{identifier}/attributes/{attribute}/statuses",
    "parameters": {
      "type": "object",
      "properties": {
        "target": {
          "type": "string",
          "description": "target"
        },
        "identifier": {
          "type": "string",
          "description": "identifier"
        },
        "attribute": {
          "type": "string",
          "description": "attribute"
        },
        "show_archived": {
          "type": "boolean",
          "description": "show_archived"
        }
      },
      "required": [
        "target",
        "identifier",
        "attribute"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_create_attribute_status",
    "description": "Create a status",
    "method": "POST",
    "path": "/v2/{target}/{identifier}/attributes/{attribute}/statuses",
    "parameters": {
      "type": "object",
      "properties": {
        "target": {
          "type": "string",
          "description": "target"
        },
        "identifier": {
          "type": "string",
          "description": "identifier"
        },
        "attribute": {
          "type": "string",
          "description": "attribute"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "target",
        "identifier",
        "attribute",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_update_attribute_status",
    "description": "Update a status",
    "method": "PATCH",
    "path": "/v2/{target}/{identifier}/attributes/{attribute}/statuses/{status}",
    "parameters": {
      "type": "object",
      "properties": {
        "target": {
          "type": "string",
          "description": "target"
        },
        "identifier": {
          "type": "string",
          "description": "identifier"
        },
        "attribute": {
          "type": "string",
          "description": "attribute"
        },
        "status": {
          "type": "string",
          "description": "status"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "target",
        "identifier",
        "attribute",
        "status",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_list_records",
    "description": "List records",
    "method": "POST",
    "path": "/v2/objects/{object}/records/query",
    "parameters": {
      "type": "object",
      "properties": {
        "object": {
          "type": "string",
          "description": "object"
        },
        "filter": {
          "type": "object",
          "description": "An object used to filter results to a subset of results. Cannot be used together with `filter_view_id`. See the [full guide to filtering and sorting here](/rest-api/guides/filtering-and-sorting)."
        },
        "filter_view_id": {
          "type": "string",
          "description": "UUID of a saved view on this object or list. When set, results are filtered using that view's filter configuration. Cannot be used together with `filter`. Note: sorts, limits, and offsets are applied independently and are not taken from the view. All attributes are returned regardless of which attributes are visible in the view."
        },
        "sorts": {
          "type": "array",
          "description": "An object used to sort results. See the [full guide to filtering and sorting here](/rest-api/guides/filtering-and-sorting)."
        },
        "limit": {
          "type": "number",
          "description": "The maximum number of results to return. Defaults to 500. See the [full guide to pagination here](/rest-api/guides/pagination)."
        },
        "offset": {
          "type": "number",
          "description": "The number of results to skip over before returning. Defaults to 0. See the [full guide to pagination here](/rest-api/guides/pagination)."
        }
      },
      "required": [
        "object"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_post_v2_objects__object__records",
    "description": "Create a record",
    "method": "POST",
    "path": "/v2/objects/{object}/records",
    "parameters": {
      "type": "object",
      "properties": {
        "object": {
          "type": "string",
          "description": "object"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "object",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_put_v2_objects__object__records",
    "description": "Assert a record",
    "method": "PUT",
    "path": "/v2/objects/{object}/records",
    "parameters": {
      "type": "object",
      "properties": {
        "object": {
          "type": "string",
          "description": "object"
        },
        "matching_attribute": {
          "type": "string",
          "description": "matching_attribute"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "object",
        "matching_attribute",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_record",
    "description": "Get a record",
    "method": "GET",
    "path": "/v2/objects/{object}/records/{record_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "object": {
          "type": "string",
          "description": "object"
        },
        "record_id": {
          "type": "string",
          "description": "record_id"
        }
      },
      "required": [
        "object",
        "record_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_overwrite_record",
    "description": "Update a record (overwrite multiselect values)",
    "method": "PUT",
    "path": "/v2/objects/{object}/records/{record_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "object": {
          "type": "string",
          "description": "object"
        },
        "record_id": {
          "type": "string",
          "description": "record_id"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "object",
        "record_id",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_update_record",
    "description": "Update a record (append multiselect values)",
    "method": "PATCH",
    "path": "/v2/objects/{object}/records/{record_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "object": {
          "type": "string",
          "description": "object"
        },
        "record_id": {
          "type": "string",
          "description": "record_id"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "object",
        "record_id",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_delete_record",
    "description": "Delete a record",
    "method": "DELETE",
    "path": "/v2/objects/{object}/records/{record_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "object": {
          "type": "string",
          "description": "object"
        },
        "record_id": {
          "type": "string",
          "description": "record_id"
        }
      },
      "required": [
        "object",
        "record_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_list_record_attribute_values",
    "description": "List record attribute values",
    "method": "GET",
    "path": "/v2/objects/{object}/records/{record_id}/attributes/{attribute}/values",
    "parameters": {
      "type": "object",
      "properties": {
        "object": {
          "type": "string",
          "description": "object"
        },
        "record_id": {
          "type": "string",
          "description": "record_id"
        },
        "attribute": {
          "type": "string",
          "description": "attribute"
        },
        "show_historic": {
          "type": "boolean",
          "description": "show_historic"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "offset": {
          "type": "integer",
          "description": "offset"
        }
      },
      "required": [
        "object",
        "record_id",
        "attribute"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_list_record_list_entries",
    "description": "List record entries",
    "method": "GET",
    "path": "/v2/objects/{object}/records/{record_id}/entries",
    "parameters": {
      "type": "object",
      "properties": {
        "object": {
          "type": "string",
          "description": "object"
        },
        "record_id": {
          "type": "string",
          "description": "record_id"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "offset": {
          "type": "integer",
          "description": "offset"
        }
      },
      "required": [
        "object",
        "record_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_post_v2_objects_records_search",
    "description": "Search records",
    "method": "POST",
    "path": "/v2/objects/records/search",
    "parameters": {
      "type": "object",
      "properties": {
        "query": {
          "type": "string",
          "description": "Query string to search for. An empty string returns a default set of results."
        },
        "limit": {
          "type": "number",
          "description": "The maximum number of results to return. Defaults to 25."
        },
        "objects": {
          "type": "array",
          "description": "Specifies which objects to filter results by. At least one object must be specified. Accepts object slugs or IDs."
        },
        "request_as": {
          "type": "string",
          "description": "Specifies the context in which to perform the search. Use 'workspace' to return all search results or specify a workspace member to limit results to what one specific person in your workspace can see."
        }
      },
      "required": [
        "query",
        "objects",
        "request_as"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_lists",
    "description": "List all lists",
    "method": "GET",
    "path": "/v2/lists",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_attio_post_v2_lists",
    "description": "Create a list",
    "method": "POST",
    "path": "/v2/lists",
    "parameters": {
      "type": "object",
      "properties": {
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_lists__list_",
    "description": "Get a list",
    "method": "GET",
    "path": "/v2/lists/{list}",
    "parameters": {
      "type": "object",
      "properties": {
        "list": {
          "type": "string",
          "description": "list"
        }
      },
      "required": [
        "list"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_patch_v2_lists__list_",
    "description": "Update a list",
    "method": "PATCH",
    "path": "/v2/lists/{list}",
    "parameters": {
      "type": "object",
      "properties": {
        "list": {
          "type": "string",
          "description": "list"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "list",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_lists__list__views",
    "description": "List views for list",
    "method": "GET",
    "path": "/v2/lists/{list}/views",
    "parameters": {
      "type": "object",
      "properties": {
        "list": {
          "type": "string",
          "description": "list"
        },
        "show_archived": {
          "type": "boolean",
          "description": "show_archived"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "cursor": {
          "type": "string",
          "description": "cursor"
        }
      },
      "required": [
        "list"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_list_list_entries",
    "description": "List entries",
    "method": "POST",
    "path": "/v2/lists/{list}/entries/query",
    "parameters": {
      "type": "object",
      "properties": {
        "list": {
          "type": "string",
          "description": "list"
        },
        "filter": {
          "type": "object",
          "description": "An object used to filter results to a subset of results. Cannot be used together with `filter_view_id`. See the [full guide to filtering and sorting here](/rest-api/guides/filtering-and-sorting)."
        },
        "filter_view_id": {
          "type": "string",
          "description": "UUID of a saved view on this object or list. When set, results are filtered using that view's filter configuration. Cannot be used together with `filter`. Note: sorts, limits, and offsets are applied independently and are not taken from the view. All attributes are returned regardless of which attributes are visible in the view."
        },
        "sorts": {
          "type": "array",
          "description": "An object used to sort results. See the [full guide to filtering and sorting here](/rest-api/guides/filtering-and-sorting)."
        },
        "limit": {
          "type": "number",
          "description": "The maximum number of results to return. Defaults to 500. See the [full guide to pagination here](/rest-api/guides/pagination)."
        },
        "offset": {
          "type": "number",
          "description": "The number of results to skip over before returning. Defaults to 0. See the [full guide to pagination here](/rest-api/guides/pagination)."
        }
      },
      "required": [
        "list"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_post_v2_lists__list__entries",
    "description": "Create an entry (add record to list)",
    "method": "POST",
    "path": "/v2/lists/{list}/entries",
    "parameters": {
      "type": "object",
      "properties": {
        "list": {
          "type": "string",
          "description": "list"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "list",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_put_v2_lists__list__entries",
    "description": "Assert a list entry by parent",
    "method": "PUT",
    "path": "/v2/lists/{list}/entries",
    "parameters": {
      "type": "object",
      "properties": {
        "list": {
          "type": "string",
          "description": "list"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "list",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_list_entry",
    "description": "Get a list entry",
    "method": "GET",
    "path": "/v2/lists/{list}/entries/{entry_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "list": {
          "type": "string",
          "description": "list"
        },
        "entry_id": {
          "type": "string",
          "description": "entry_id"
        }
      },
      "required": [
        "list",
        "entry_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_overwrite_list_entry",
    "description": "Update a list entry (overwrite multiselect values)",
    "method": "PUT",
    "path": "/v2/lists/{list}/entries/{entry_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "list": {
          "type": "string",
          "description": "list"
        },
        "entry_id": {
          "type": "string",
          "description": "entry_id"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "list",
        "entry_id",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_update_list_entry",
    "description": "Update a list entry (append multiselect values)",
    "method": "PATCH",
    "path": "/v2/lists/{list}/entries/{entry_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "list": {
          "type": "string",
          "description": "list"
        },
        "entry_id": {
          "type": "string",
          "description": "entry_id"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "list",
        "entry_id",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_delete_list_entry",
    "description": "Delete a list entry",
    "method": "DELETE",
    "path": "/v2/lists/{list}/entries/{entry_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "list": {
          "type": "string",
          "description": "list"
        },
        "entry_id": {
          "type": "string",
          "description": "entry_id"
        }
      },
      "required": [
        "list",
        "entry_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_list_list_entry_attribute_values",
    "description": "List attribute values for a list entry",
    "method": "GET",
    "path": "/v2/lists/{list}/entries/{entry_id}/attributes/{attribute}/values",
    "parameters": {
      "type": "object",
      "properties": {
        "list": {
          "type": "string",
          "description": "list"
        },
        "entry_id": {
          "type": "string",
          "description": "entry_id"
        },
        "attribute": {
          "type": "string",
          "description": "attribute"
        },
        "show_historic": {
          "type": "boolean",
          "description": "show_historic"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "offset": {
          "type": "integer",
          "description": "offset"
        }
      },
      "required": [
        "list",
        "entry_id",
        "attribute"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_workspace_members",
    "description": "List workspace members",
    "method": "GET",
    "path": "/v2/workspace_members",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_attio_get_workspace_member",
    "description": "Get a workspace member",
    "method": "GET",
    "path": "/v2/workspace_members/{workspace_member_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "workspace_member_id": {
          "type": "string",
          "description": "workspace_member_id"
        }
      },
      "required": [
        "workspace_member_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_notes",
    "description": "List notes",
    "method": "GET",
    "path": "/v2/notes",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "offset": {
          "type": "integer",
          "description": "offset"
        },
        "parent_object": {
          "type": "string",
          "description": "parent_object"
        },
        "parent_record_id": {
          "type": "string",
          "description": "parent_record_id"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_attio_post_v2_notes",
    "description": "Create a note",
    "method": "POST",
    "path": "/v2/notes",
    "parameters": {
      "type": "object",
      "properties": {
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_notes__note_id_",
    "description": "Get a note",
    "method": "GET",
    "path": "/v2/notes/{note_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "note_id": {
          "type": "string",
          "description": "note_id"
        }
      },
      "required": [
        "note_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_delete_v2_notes__note_id_",
    "description": "Delete a note",
    "method": "DELETE",
    "path": "/v2/notes/{note_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "note_id": {
          "type": "string",
          "description": "note_id"
        }
      },
      "required": [
        "note_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_tasks",
    "description": "List tasks",
    "method": "GET",
    "path": "/v2/tasks",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "offset": {
          "type": "integer",
          "description": "offset"
        },
        "sort": {
          "type": "string",
          "description": "sort"
        },
        "linked_object": {
          "type": "string",
          "description": "linked_object"
        },
        "linked_record_id": {
          "type": "string",
          "description": "linked_record_id"
        },
        "assignee": {
          "type": [
            "string",
            "null"
          ],
          "description": "assignee"
        },
        "is_completed": {
          "type": "boolean",
          "description": "is_completed"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_attio_post_v2_tasks",
    "description": "Create a task",
    "method": "POST",
    "path": "/v2/tasks",
    "parameters": {
      "type": "object",
      "properties": {
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_tasks__task_id_",
    "description": "Get a task",
    "method": "GET",
    "path": "/v2/tasks/{task_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "task_id": {
          "type": "string",
          "description": "task_id"
        }
      },
      "required": [
        "task_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_patch_v2_tasks__task_id_",
    "description": "Update a task",
    "method": "PATCH",
    "path": "/v2/tasks/{task_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "task_id": {
          "type": "string",
          "description": "task_id"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "task_id",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_delete_v2_tasks__task_id_",
    "description": "Delete a task",
    "method": "DELETE",
    "path": "/v2/tasks/{task_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "task_id": {
          "type": "string",
          "description": "task_id"
        }
      },
      "required": [
        "task_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_threads",
    "description": "List threads",
    "method": "GET",
    "path": "/v2/threads",
    "parameters": {
      "type": "object",
      "properties": {
        "record_id": {
          "type": "string",
          "description": "record_id"
        },
        "object": {
          "type": "string",
          "description": "object"
        },
        "entry_id": {
          "type": "string",
          "description": "entry_id"
        },
        "list": {
          "type": "string",
          "description": "list"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "offset": {
          "type": "integer",
          "description": "offset"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_threads__thread_id_",
    "description": "Get a thread",
    "method": "GET",
    "path": "/v2/threads/{thread_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "thread_id": {
          "type": "string",
          "description": "thread_id"
        }
      },
      "required": [
        "thread_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_post_v2_comments",
    "description": "Create a comment",
    "method": "POST",
    "path": "/v2/comments",
    "parameters": {
      "type": "object",
      "properties": {
        "data": {
          "type": "string",
          "description": "data"
        }
      },
      "required": [
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_comments__comment_id_",
    "description": "Get a comment",
    "method": "GET",
    "path": "/v2/comments/{comment_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "comment_id": {
          "type": "string",
          "description": "comment_id"
        }
      },
      "required": [
        "comment_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_delete_v2_comments__comment_id_",
    "description": "Delete a comment",
    "method": "DELETE",
    "path": "/v2/comments/{comment_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "comment_id": {
          "type": "string",
          "description": "comment_id"
        }
      },
      "required": [
        "comment_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_meetings",
    "description": "List meetings",
    "method": "GET",
    "path": "/v2/meetings",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "cursor": {
          "type": "string",
          "description": "cursor"
        },
        "linked_object": {
          "type": "string",
          "description": "linked_object"
        },
        "linked_record_id": {
          "type": "string",
          "description": "linked_record_id"
        },
        "participants": {
          "type": "string",
          "description": "participants"
        },
        "sort": {
          "type": "string",
          "description": "sort"
        },
        "ends_from": {
          "type": [
            "string",
            "null"
          ],
          "description": "ends_from"
        },
        "starts_before": {
          "type": [
            "string",
            "null"
          ],
          "description": "starts_before"
        },
        "timezone": {
          "type": "string",
          "description": "timezone"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_attio_post_v2_meetings",
    "description": "Find or create a meeting",
    "method": "POST",
    "path": "/v2/meetings",
    "parameters": {
      "type": "object",
      "properties": {
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_meetings__meeting_id_",
    "description": "Get a meeting",
    "method": "GET",
    "path": "/v2/meetings/{meeting_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "meeting_id": {
          "type": "string",
          "description": "meeting_id"
        }
      },
      "required": [
        "meeting_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_list_call_recordings",
    "description": "List call recordings",
    "method": "GET",
    "path": "/v2/meetings/{meeting_id}/call_recordings",
    "parameters": {
      "type": "object",
      "properties": {
        "meeting_id": {
          "type": "string",
          "description": "meeting_id"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "cursor": {
          "type": "string",
          "description": "cursor"
        }
      },
      "required": [
        "meeting_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_create_call_recording",
    "description": "Create call recording",
    "method": "POST",
    "path": "/v2/meetings/{meeting_id}/call_recordings",
    "parameters": {
      "type": "object",
      "properties": {
        "meeting_id": {
          "type": "string",
          "description": "meeting_id"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "meeting_id",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_call_recording",
    "description": "Get call recording",
    "method": "GET",
    "path": "/v2/meetings/{meeting_id}/call_recordings/{call_recording_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "meeting_id": {
          "type": "string",
          "description": "meeting_id"
        },
        "call_recording_id": {
          "type": "string",
          "description": "call_recording_id"
        }
      },
      "required": [
        "meeting_id",
        "call_recording_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_delete_call_recording",
    "description": "Delete call recording",
    "method": "DELETE",
    "path": "/v2/meetings/{meeting_id}/call_recordings/{call_recording_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "meeting_id": {
          "type": "string",
          "description": "meeting_id"
        },
        "call_recording_id": {
          "type": "string",
          "description": "call_recording_id"
        }
      },
      "required": [
        "meeting_id",
        "call_recording_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_call_recording_transcript",
    "description": "Get call transcript",
    "method": "GET",
    "path": "/v2/meetings/{meeting_id}/call_recordings/{call_recording_id}/transcript",
    "parameters": {
      "type": "object",
      "properties": {
        "meeting_id": {
          "type": "string",
          "description": "meeting_id"
        },
        "call_recording_id": {
          "type": "string",
          "description": "call_recording_id"
        },
        "cursor": {
          "type": "string",
          "description": "cursor"
        }
      },
      "required": [
        "meeting_id",
        "call_recording_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_files",
    "description": "List files",
    "method": "GET",
    "path": "/v2/files",
    "parameters": {
      "type": "object",
      "properties": {
        "object": {
          "type": "string",
          "description": "object"
        },
        "record_id": {
          "type": "string",
          "description": "record_id"
        },
        "storage_provider": {
          "type": "string",
          "description": "storage_provider"
        },
        "parent_folder_id": {
          "type": "string",
          "description": "parent_folder_id"
        },
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "cursor": {
          "type": "string",
          "description": "cursor"
        }
      },
      "required": [
        "object",
        "record_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_post_v2_files",
    "description": "Create a folder",
    "method": "POST",
    "path": "/v2/files",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_attio_post_v2_files_upload",
    "description": "Upload a file",
    "method": "POST",
    "path": "/v2/files/upload",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_files__file_id_",
    "description": "Get a file",
    "method": "GET",
    "path": "/v2/files/{file_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "file_id": {
          "type": "string",
          "description": "file_id"
        }
      },
      "required": [
        "file_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_delete_v2_files__file_id_",
    "description": "Delete a file",
    "method": "DELETE",
    "path": "/v2/files/{file_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "file_id": {
          "type": "string",
          "description": "file_id"
        }
      },
      "required": [
        "file_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_files__file_id__download",
    "description": "Download a file",
    "method": "GET",
    "path": "/v2/files/{file_id}/download",
    "parameters": {
      "type": "object",
      "properties": {
        "file_id": {
          "type": "string",
          "description": "file_id"
        }
      },
      "required": [
        "file_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_scim_v2_Schemas",
    "description": "List SCIM schemas",
    "method": "GET",
    "path": "/scim/v2/Schemas",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_attio_get_scim_v2_Users",
    "description": "List SCIM users",
    "method": "GET",
    "path": "/scim/v2/Users",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_attio_post_scim_v2_Users",
    "description": "Create SCIM user",
    "method": "POST",
    "path": "/scim/v2/Users",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_attio_get_scim_v2_Groups",
    "description": "List SCIM groups",
    "method": "GET",
    "path": "/scim/v2/Groups",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_attio_post_scim_v2_Groups",
    "description": "Create SCIM group",
    "method": "POST",
    "path": "/scim/v2/Groups",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_attio_get_scim_v2_Users__user_id_",
    "description": "Get SCIM user",
    "method": "GET",
    "path": "/scim/v2/Users/{user_id}",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_attio_put_scim_v2_Users__user_id_",
    "description": "Update SCIM user",
    "method": "PUT",
    "path": "/scim/v2/Users/{user_id}",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_attio_patch_scim_v2_Users__user_id_",
    "description": "Patch SCIM user",
    "method": "PATCH",
    "path": "/scim/v2/Users/{user_id}",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_attio_delete_scim_v2_Users__user_id_",
    "description": "Delete SCIM user",
    "method": "DELETE",
    "path": "/scim/v2/Users/{user_id}",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_attio_scim_get_group",
    "description": "Get SCIM group",
    "method": "GET",
    "path": "/scim/v2/Groups/{workspace_team_id}",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_attio_scim_replace_group",
    "description": "Update SCIM group",
    "method": "PUT",
    "path": "/scim/v2/Groups/{workspace_team_id}",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_attio_scim_patch_group",
    "description": "Patch SCIM group",
    "method": "PATCH",
    "path": "/scim/v2/Groups/{workspace_team_id}",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_attio_scim_delete_group",
    "description": "Delete SCIM group",
    "method": "DELETE",
    "path": "/scim/v2/Groups/{workspace_team_id}",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_webhooks",
    "description": "List webhooks",
    "method": "GET",
    "path": "/v2/webhooks",
    "parameters": {
      "type": "object",
      "properties": {
        "limit": {
          "type": "integer",
          "description": "limit"
        },
        "offset": {
          "type": "integer",
          "description": "offset"
        }
      }
    }
  },
  {
    "name": "superagnt_connection_attio_post_v2_webhooks",
    "description": "Create a webhook",
    "method": "POST",
    "path": "/v2/webhooks",
    "parameters": {
      "type": "object",
      "properties": {
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_webhooks__webhook_id_",
    "description": "Get a webhook",
    "method": "GET",
    "path": "/v2/webhooks/{webhook_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "webhook_id": {
          "type": "string",
          "description": "webhook_id"
        }
      },
      "required": [
        "webhook_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_patch_v2_webhooks__webhook_id_",
    "description": "Update a webhook",
    "method": "PATCH",
    "path": "/v2/webhooks/{webhook_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "webhook_id": {
          "type": "string",
          "description": "webhook_id"
        },
        "data": {
          "type": "object",
          "description": "data"
        }
      },
      "required": [
        "webhook_id",
        "data"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_delete_v2_webhooks__webhook_id_",
    "description": "Delete a webhook",
    "method": "DELETE",
    "path": "/v2/webhooks/{webhook_id}",
    "parameters": {
      "type": "object",
      "properties": {
        "webhook_id": {
          "type": "string",
          "description": "webhook_id"
        }
      },
      "required": [
        "webhook_id"
      ]
    }
  },
  {
    "name": "superagnt_connection_attio_get_v2_self",
    "description": "Identify",
    "method": "GET",
    "path": "/v2/self",
    "parameters": {
      "type": "object",
      "properties": {}
    }
  }
]
```

## Example

```bash
curl -X GET &#x27;https://api.superagnt.com/v1/connections/attio/v2/objects&#x27; \
  -H &#x27;Authorization: Bearer $SUPERAGNT_API_KEY&#x27;
```

## Use Cases

- Sync leads and accounts between your data warehouse and Attio records
- Build AI agents that enrich, deduplicate, and update CRM records automatically
- Trigger Attio list entries from product or billing events in your stack
- Generate meeting summaries from call transcripts and write them back as notes
- Automate handoff workflows that create tasks for the right Attio workspace member
- Power reporting dashboards over Attio records, list entries, and activity

## Links

- [Documentation](https://superagnt.com/r/ch-attio-crm-docs)
- [superagnt app / API keys](https://superagnt.com/r/ch-attio-crm-key)
- [Connections page](https://app.superagnt.com/dashboard/connections)
- [This listing](https://clawhub.ai/superagnt/skills/attio-crm)
