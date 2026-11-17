# Orders API contract

`GET /orders/{id}` returns:

| Field | Type | Meaning |
|---|---|---|
| `id` | string | Order identifier |
| `total_cents` | integer | Order total in cents |

`POST /orders/{id}/sync` may answer 429 with the JSON body `{"retry_after": N}`,
where N is the number of seconds the client must wait before retrying.
