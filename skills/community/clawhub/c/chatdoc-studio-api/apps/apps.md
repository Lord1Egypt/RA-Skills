# Apps API

The Apps API allows you to manage all types of applications (Chat, Agent, Extract, RAG) in your team.

## Base Path

```
/apps
```

## App Types

| Type | Name | Description |
|------|------|-------------|
| `1` | ChatApp | Document-based chat application |
| `2` | ExtractApp | Structured data extraction application |
| `5` | ContentRetrievalApp | RAG (Retrieval-Augmented Generation) application |
| `7` | AgentApp | Task-based document analysis application |

**Note**: PDF Parser (type 99) is not an app and is not managed by this API.

### 1. Get Apps

Retrieve a paginated list of all applications in your team.

**Endpoint:** `GET /apps/`

**Query Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `currentPage` | integer | No | Page number (default: 1, min: 1) |
| `pageSize` | integer | No | Items per page (default: 20, min: 1) |

**Response:**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `items` | array | No | Array of app objects |
| `page` | integer | No | Current page number |
| `size` | integer | No | Items per page |
| `total` | integer | No | Total number of apps |

**App Object:**

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | string | No | App ID |
| `name` | string | No | App name |
| `app_type` | integer | No | App type (1=Chat, 2=Extract, 5=RAG, 7=Agent) |
| `created_at` | integer | No | Creation timestamp (Unix timestamp) |
| `updated_at` | integer | No | Last update timestamp (Unix timestamp) |

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 200 | - | Success |

### 2. Delete App

Delete an application by app_id. This operation permanently removes the app and all its associated data.

**Endpoint:** `DELETE /apps/{app_id}`

**Path Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `app_id` | string | App ID |

**Response:** Empty data field on success

**Status Codes:**

| HTTP Code | Error Code | Description |
|-----------|------------|-------------|
| 200 | - | Success |
| 404 | `not_found` | App not found |

**Important Notes:**

1. **App ID**: Use the `id` field from the Get Apps response. This is the public app identifier.

2. **Deletion Behavior**:
   - For Chat/RAG apps: Deletes all app versions and associated conversations
   - For Extract apps: Soft deletes all app versions with the same app_id
   - For Agent apps: Deletes all app versions and associated task records

3. **Irreversible**: Deletion is permanent. Make sure you have backups if needed.

4. **App Types**: This API works for Chat (1), Extract (2), RAG (5), and Agent (7) apps. PDF Parser (99) is not supported.

## Important Notes

1. **Pagination**: Use `currentPage` and `pageSize` query parameters to navigate through large lists of apps.

2. **Timestamp Format**: All timestamps are Unix timestamps (seconds since epoch).

3. **App Identification**: The `id` field in the response - use this for all subsequent API calls.

4. **Type Filtering**: The `app_type` field helps you distinguish between different app types when processing the response.
