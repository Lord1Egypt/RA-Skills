# Buy Me a Pie API Surface

Status: inferred from the live frontend assets fetched from `https://app.buymeapie.com` on March 14, 2026. This is not an official public API contract. Expect drift.

## Auth

- API host: `https://api.buymeapie.com`
- Auth model: HTTP Basic Auth with `base64("<login>:<pin>")`
- Web app stores the same credential pair in the `bmap_auth` cookie.

## Safe v1 endpoints

### Account

- `GET /bauth`
  - Validate credentials.
  - Frontend sends only the `Authorization` header.
- `POST /v4.0/users`
  - Create account.
  - Payload: `{"pin","login","email","subscription_status"}`
- `PUT /v4.0/users`
  - Update account.
  - Payload: `{"pin","email","login"}`
- `POST /password_resets`
  - Trigger PIN recovery.
  - Payload: `{"email"}`

### Lists

- `GET /restrictions`
  - Returns runtime limits such as list count and sharing count.
- `GET /lists`
  - Returns all lists.
- `POST /lists`
  - Create list.
  - Payload used by frontend: `{"id","name","items_purchased","items_not_purchased"}`
  - The `id` field is optional for a clean client. The web app sends a temporary ID.
- `PUT /lists/{list_id}`
  - Update list metadata.
  - Payload used by frontend: `{"name","emails"}`
  - Sharing is implemented by replacing the `emails` array on this endpoint.
- `DELETE /lists/{list_id}`
  - Delete list.

### Items

- `GET /lists/{list_id}/items`
  - Full item list.
- `GET /lists/{list_id}/changed_items/{unix_timestamp}`
  - Delta sync path.
  - Useful later for caching. Skip for v1 skill logic.
- `POST /lists/{list_id}/items`
  - Add item.
  - Payload used by frontend: `{"title","amount","is_purchased"}`
- `PUT /lists/{list_id}/items/{item_id}`
  - Partial item update.
  - Payload can contain any subset of `title`, `amount`, `is_purchased`.
- `DELETE /lists/{list_id}/items/{item_id}`
  - Delete item.

### Unique items

- `GET /unique_items`
  - Returns the autocomplete dictionary.
- `PUT /unique_items/{encoded_title}`
  - Payload: `{"group_id","permanent","use_count"}`
- `DELETE /unique_items/{encoded_title}`
- `DELETE /unique_items/permanent/{encoded_title}`

## Endpoints to avoid in v1

- `PUT /sync/v2.0.2`
  - Offline-store reconciliation path from the legacy web app.
  - Useful only if you intentionally implement offline sync semantics.
- `POST /v4.0/oauth2/code`
  - OAuth authorization flow.
  - Keep this in browser fallback unless a user explicitly asks for OAuth automation.

## Observed response fields

### List

Common fields observed in frontend code:

- `id`
- `name`
- `emails`
- `items_not_purchased`
- `items_purchased`
- `created_at`
- `type`
- `source_url`

### Item

Common fields observed in frontend code:

- `id`
- `title`
- `amount`
- `is_purchased`
- `created_at`
- `updated_at`
- `deleted`
- `group_id`

### Unique item

Common fields observed in frontend code:

- `title`
- `group_id`
- `use_count`
- `permanent`
- `updated_at`

## Error model inferred from frontend

- `401`
  - Invalid auth. Frontend logs out.
- `422`
  - Invalid session or invalid request state. Frontend also logs out.
- `423`
  - Temporary lock. Frontend retries the same request after a short delay.
- `404`
  - Frontend treats this as stale cache in some paths and forces cache clear.

## Practical guidance

- Prefer list and item IDs over names.
- Re-read current list state before any sharing update because `PUT /lists/{id}` overwrites the `emails` field.
- Treat recipe lists (`type == "recipe"`) as a different variant. Their `source_url` is informational and should not be mutated unless documented.
