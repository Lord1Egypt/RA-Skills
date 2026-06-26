# Ikara API patterns

## Base pattern
`{BaseUrl}/tenants/{tenantId}/...`

## Common auth pattern
- `Authorization: Bearer <access_token>`
- function/app key usually passed as `?code=<key>`

## Practical rules
- Confirm the active endpoint family before chaining calls (`/CRUD/...` versus non-CRUD refactor paths).
- Do one sanity call first to confirm the right path and auth shape.
- Reuse the same bearer token and app code for the whole chain.
- Prefer list endpoints when you can derive titles, ids, and created dates from one response.

## Common bulk workflows
- fetch all integrations once, then match by title/id locally
- create/update titles in a continuous loop after one approval
- create service compliances first, then one root group, then all criteria under that group
- for manual assessments, use the exact endpoint/method/content type the API expects

## Manual assessment note
Some manual assessment endpoints require:
- specific route shape
- PUT instead of POST
- multipart/form-data instead of JSON or urlencoded form data

Do not assume the write contract. Probe one working example first when the route is unfamiliar.
