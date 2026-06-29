---
name: flux
description: Manage Flux kanban boards, cards, columns, and labels through the Flux REST API. Create and move cards, assign members, toggle labels, search, and build board automations.
version: 1.0.0
homepage: https://flux.umin.ai
metadata:
  openclaw:
    emoji: 🗂️
    primaryEnv: FLUX_API_KEY
    envVars:
      - name: FLUX_API_KEY
        required: true
        description: Flux API key. Starts with `flux_`. Create one in Flux under Settings → API Keys.
      - name: FLUX_BASE_URL
        required: false
        description: Base URL of your Flux instance. Defaults to https://flux.umin.ai.
---

# Flux

Flux is a kanban board management platform. Use this skill to build automations, manage
cards, and organize work through the Flux REST API.

## Setup

- **`FLUX_API_KEY`** (required) — an API key beginning with `flux_`. Every request is
  authenticated with it.
- **`FLUX_BASE_URL`** (optional) — the origin of the Flux instance, e.g.
  `https://flux.umin.ai`. Defaults to `https://flux.umin.ai`.

## Authentication

Send the key as a Bearer token on every request:

```
Authorization: Bearer flux_YOUR_KEY
```

API keys carry granular scopes, so a request may succeed for reads but be rejected for
writes if the key lacks the scope. A `401` means the key is missing or invalid; a `403`
means the key is valid but not permitted for that action.

## Core concepts

- **Active workspace** — most board/card endpoints operate on the *active workspace* tied
  to the key. List workspaces with `GET /api/workspaces`, change it with
  `POST /api/workspaces/switch`.
- **Two ID formats** — boards accept either a UUID or a short URL id (`shortId`, e.g.
  `av-tX6qQ`). Cards have an internal UUID *and* a human id (`humanId`, e.g. `TB-1`) used in
  URLs. Use the UUID for write operations unless an endpoint says otherwise.
- **Cache key gotcha** — a board is keyed by its `shortId`, not by `card.boardId` (which is
  a UUID). Don't assume the two are interchangeable when matching a card to its board.
- **Soft deletes** — every `DELETE` is reversible. Deleted records are hidden, not
  destroyed, and can be restored via `POST /api/undo`.
- **Idempotency** — include `X-Idempotency-Key: <uuid>` on every write (POST/PATCH/PUT/
  DELETE). On retry, Flux returns the original result instead of duplicating the action.
- **Dates** — all timestamps are ISO 8601.

## Endpoints

### Workspaces

| Method | Path | Body / Query | Notes |
|---|---|---|---|
| GET | `/api/workspaces` | — | List your workspaces → `{ workspaces: [{ id, name, slug }] }` |
| POST | `/api/workspaces` | `{ name }` | Create a workspace |
| POST | `/api/workspaces/switch` | `{ workspaceId }` | Set the active workspace |

### Boards

| Method | Path | Body / Query | Notes |
|---|---|---|---|
| GET | `/api/boards` | — | Boards in the active workspace → `{ boards: [{ id, shortId, title, columns }] }` |
| GET | `/api/boards/all` | — | Boards across all workspaces |
| POST | `/api/boards` | `{ title, workspaceId? }` | Create a board |
| GET | `/api/boards/{boardId}` | accepts shortId or UUID | Full board → `{ board, cards: { [cardId]: card }, boardLabels, members }` |
| PATCH | `/api/boards/{boardId}` | `{ title?, settings?, doneColumnId? }` | Update a board |
| DELETE | `/api/boards/{boardId}` | — | Soft-delete a board |

### Columns

| Method | Path | Body / Query | Notes |
|---|---|---|---|
| POST | `/api/columns` | `{ boardId, title }` | Create a column |
| PATCH | `/api/columns` | `{ columnId, title?, isDone? }` | Update a column |
| DELETE | `/api/columns?columnId={id}` | — | Delete a column |
| PUT | `/api/columns/reorder` | `{ boardId, columnIds: [ordered UUIDs] }` | Reorder columns |

### Cards

| Method | Path | Body / Query | Notes |
|---|---|---|---|
| POST | `/api/cards` | `{ boardId, columnId, title, description? }` | Create a card |
| PATCH | `/api/cards` | `{ cardId, title?, description?, columnId?, assignees?, dueDate?, coverUrl?, archivedAt? }` | Update a card. `assignees` is an array of user IDs and replaces the whole set. |
| DELETE | `/api/cards?cardId={id}` | — | Soft-delete a card |
| GET | `/api/cards/{cardId}` | — | Full detail: checklist, comments, attachments, labels, assignees |
| PUT | `/api/cards/reorder` | `{ boardId, moves: [{ cardId, columnId, position }] }` | Move/reorder cards |

### Card sub-resources

**Checklist**
| Method | Path | Body / Query |
|---|---|---|
| POST | `/api/cards/{cardId}/checklist` | `{ text }` |
| PATCH | `/api/cards/{cardId}/checklist` | `{ itemId, text?, done?, position? }` |
| DELETE | `/api/cards/{cardId}/checklist?itemId={id}` | — |

**Comments**
| Method | Path | Body / Query |
|---|---|---|
| POST | `/api/cards/{cardId}/comments` | `{ content, parentId? }` |
| PATCH | `/api/cards/{cardId}/comments` | `{ commentId, content }` |
| DELETE | `/api/cards/{cardId}/comments?commentId={id}` | — |

**Labels on a card** (toggle a board-level label onto the card)
| Method | Path | Body / Query |
|---|---|---|
| POST | `/api/cards/{cardId}/labels` | `{ labelId }` |
| DELETE | `/api/cards/{cardId}/labels?labelId={id}` | — |

**Attachments**
| Method | Path | Body / Query | Notes |
|---|---|---|---|
| POST | `/api/cards/{cardId}/attachments/upload-url` | `{ fileName, mimeType }` | Returns a presigned S3 upload URL |
| POST | `/api/cards/{cardId}/attachments` | `{ fileName, fileUrl, s3Key?, mimeType? }` | Register the attachment after uploading |
| DELETE | `/api/cards/{cardId}/attachments?attachmentId={id}` | — | Delete an attachment |

### Labels (board-level definitions)

| Method | Path | Body / Query |
|---|---|---|
| POST | `/api/boards/{boardId}/labels` | `{ text, color }` |
| PATCH | `/api/boards/{boardId}/labels` | `{ labelId, text?, color? }` |
| DELETE | `/api/boards/{boardId}/labels?labelId={id}` | — |

### Search & undo

| Method | Path | Body / Query | Notes |
|---|---|---|---|
| GET | `/api/search?q={query}&workspaceId={id?}&type={card\|board?}` | — | Full-text search |
| POST | `/api/undo` | `{ boardId }` | Undo the last action on a board |

## Common workflows

### Create a card on a board
1. `GET /api/boards` — find the board by title, note its `shortId`.
2. `GET /api/boards/{shortId}` — read `board.columns` to pick the target `columnId`.
3. `POST /api/cards` with `{ boardId, columnId, title }`.

### Move a card to another column
1. `GET /api/boards/{shortId}` — find the source/target `columnId`s and the card.
2. `PUT /api/cards/reorder` with `{ boardId, moves: [{ cardId, columnId, position: 0 }] }`
   (`position: 0` drops it at the top of the target column).

### Assign members to a card
1. `GET /api/boards/{shortId}` — the response `members` array lists user IDs.
2. `PATCH /api/cards` with `{ cardId, assignees: [userId1, userId2] }`.
   Assignees are replaced wholesale — send the full desired list, not a delta.
   Note: the **write** field is `assignees`; board reads expose the same data as
   `assigneeIds`. Sending `assigneeIds` to PATCH is silently ignored and returns
   `422 "No updates provided"`.

### Add a label to a card
1. `GET /api/boards/{shortId}` — the response `boardLabels` array lists label IDs.
   (Create the label first with `POST /api/boards/{boardId}/labels` if it doesn't exist.)
2. `POST /api/cards/{cardId}/labels` with `{ labelId }`.

## Notes & gotchas

- Always send `X-Idempotency-Key: <uuid>` on writes to make retries safe.
- All deletes are soft and reversible via `POST /api/undo`.
- Board IDs accept both UUID and `shortId`; card IDs have a UUID and a `humanId` (`TB-1`).
- Resolve a board's columns and labels *before* creating or moving cards — you need their
  IDs from `GET /api/boards/{shortId}`.
- A `403` on a write usually means the API key lacks the required scope, not that the
  resource is missing.
