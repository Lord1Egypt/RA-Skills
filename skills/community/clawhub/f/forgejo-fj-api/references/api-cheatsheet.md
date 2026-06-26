# Forgejo API Cheatsheet

This reference assumes `FORGEJO_URL` and `FORGEJO_TOKEN` are already set.

If required bins, env vars, or `fj` setup are missing, return to `SKILL.md`
prerequisites, readiness checks, or troubleshooting before proceeding.

Use these endpoints when `fj` does not support the requested operation.

The examples in this skill use these JSON request headers:

```bash
-H "Authorization: token $FORGEJO_TOKEN"
-H "Content-Type: application/json"
-H "Accept: application/json"
```

Forgejo also accepts bearer-style authorization headers. The examples in this
skill use the `Authorization: token ...` form for consistency.

## Wiki writes

Create a page:

```http
POST /repos/{owner}/{repo}/wiki/new
```

Request body:

```json
{
  "title": "Page Title",
  "content_base64": "<base64>",
  "message": "Create wiki page"
}
```

Update a page:

```http
PATCH /repos/{owner}/{repo}/wiki/page/{pageName}
```

Request body:

```json
{
  "title": "Page Title",
  "content_base64": "<base64>",
  "message": "Update wiki page"
}
```

If `title` is omitted or empty on update, the current page name is kept.

Delete a page:

```http
DELETE /repos/{owner}/{repo}/wiki/page/{pageName}
```

List or read pages:

```http
GET /repos/{owner}/{repo}/wiki/pages
GET /repos/{owner}/{repo}/wiki/page/{pageName}
GET /repos/{owner}/{repo}/wiki/revisions/{pageName}
```

Encode wiki content to base64 before sending it:

```bash
printf '%s' "# My Page
Page content here" | base64
```

The wiki create and edit request body uses the `CreateWikiPageOptions` schema in
Swagger. Confirm field names against the target instance's `/api/swagger` if you
need to script it precisely for a specific Forgejo version.

## Repository labels

List labels:

```http
GET /repos/{owner}/{repo}/labels
```

Create a label:

```http
POST /repos/{owner}/{repo}/labels
```

```json
{
  "name": "bug",
  "color": "#d73a4a",
  "description": "Bug report",
  "exclusive": false,
  "is_archived": false
}
```

Update a label:

```http
PATCH /repos/{owner}/{repo}/labels/{id}
```

Delete a label:

```http
DELETE /repos/{owner}/{repo}/labels/{id}
```

## Milestones

List milestones:

```http
GET /repos/{owner}/{repo}/milestones
GET /repos/{owner}/{repo}/milestones/{id}
```

Create a milestone:

```http
POST /repos/{owner}/{repo}/milestones
```

```json
{
  "title": "v2.0",
  "description": "Release milestone",
  "due_on": "2026-06-01T00:00:00Z",
  "state": "open"
}
```

Update a milestone:

```http
PATCH /repos/{owner}/{repo}/milestones/{id}
```

Delete a milestone:

```http
DELETE /repos/{owner}/{repo}/milestones/{id}
```

## Pull request reviews with inline comments

Create a review with summary and inline comments:

```http
POST /repos/{owner}/{repo}/pulls/{index}/reviews
```

```json
{
  "body": "Review summary",
  "event": "COMMENT",
  "comments": [
    {
      "path": "src/main.go",
      "new_position": 42,
      "body": "Potential nil pointer here"
    }
  ]
}
```

The Swagger schema also defines `old_position` for comments on removed lines and
an optional `commit_id` at the review level.

Supported review submission events are stable across checked Forgejo `v13.x`,
`v14.x`, and current source:
- `COMMENT`
- `APPROVED`
- `REQUEST_CHANGES`

Current server behavior is stricter than the enum list alone suggests:
- `COMMENT` requires a body or inline comments
- `REQUEST_CHANGES` requires a body
- `APPROVED` does not require a body
- omitted or unrecognized events fall back to a pending review flow
- `PENDING` can create a pending review but cannot be submitted as a final review
- `REQUEST_REVIEW` is not a supported create/submit review event; use the
  requested-reviewers endpoints instead

Only send `APPROVED` if the user explicitly asked for approval.

## Notifications

List all notifications:

```http
GET /notifications
GET /notifications/new
GET /notifications/threads/{id}
```

List repository notifications:

```http
GET /repos/{owner}/{repo}/notifications
```

Change notification status for the current user:

```http
PUT /notifications
PUT /repos/{owner}/{repo}/notifications
PATCH /notifications/threads/{id}
```

Current implementations also accept status controls such as `to-status` for read,
unread, or pinned transitions. Check the target instance Swagger before relying
on specific notification-status mutations.

Current server behavior also supports notification filters such as
`status-types`, `subject-type`, `all`, and `last_read_at` on the notification
endpoints.

## Pull request metadata

Use the pull request endpoint to discover the base branch, head branch, head SHA,
and merge state before reviewing or merging:

```http
GET /repos/{owner}/{repo}/pulls/{index}
```

Useful fields commonly include:
- `base.ref`
- `head.ref`
- `head.sha`
- `mergeable`
- `draft`
- `merged`

## Pagination pattern

For paginated endpoints, use `page` and `limit` parameters and keep paging until
the response or available pagination metadata shows there are no more results.

Example shell loop:

```bash
page=1
while true; do
  curl -sS -D headers.txt \
    -H "Authorization: token $FORGEJO_TOKEN" \
    -H "Accept: application/json" \
    "$FORGEJO_URL/api/v1/repos/$OWNER/$REPO/issues?page=$page&limit=50"
  page=$((page + 1))
  # Stop after the last page based on the response size or pagination metadata when available.
done
```
