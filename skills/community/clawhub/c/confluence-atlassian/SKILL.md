---
name: confluence-atlassian
description: |
  Full-featured Confluence Cloud REST API v2 skill. Manage pages, spaces, blogposts, attachments, comments, labels, and more via direct Atlassian API calls.
  Use when managing Confluence content, creating/updating pages, working with spaces, or interacting with Confluence via API.
  Requires Atlassian email and API token for authentication.
metadata:
  author: jeffersonling1217-png
  version: "1.0.0"
  clawdbot:
    emoji: 📄
    homepage: https://clawhub.ai/jeffersonling1217-png/confluence-atlassian
    requires:
      env:
        - CONFLUENCE_EMAIL
        - CONFLUENCE_API_TOKEN
        - CONFLUENCE_DOMAIN
---

# Confluence REST API v2 Skill

Interact with Atlassian Confluence Cloud using the REST API v2. This skill enables reading, creating, updating, and deleting Confluence content including pages, blog posts, attachments, comments, spaces, labels, and more.

## Authentication

### Basic Auth (Email + API Token)

**Required Environment Variables:**
```bash
CONFLUENCE_EMAIL=your_email@example.com
CONFLUENCE_API_TOKEN=your_api_token
CONFLUENCE_DOMAIN=your_domain  # e.g. "yourcompany" for yourcompany.atlassian.net
```

### Base URL
```
https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2
```

### Generate API Token
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Click "Create API token"
3. Label it (e.g., "nanobot")
4. Copy the token

### curl Authentication
```bash
--user "$CONFLUENCE_EMAIL:$CONFLUENCE_API_TOKEN"
```

**curl Authentication Header:**
```bash
-H "Authorization: Basic $(echo -n '$CONFLUENCE_EMAIL:$CONFLUENCE_API_TOKEN' | base64)"
```

### Generate Base64 Auth String
```bash
# Linux/Mac
echo -n "$CONFLUENCE_EMAIL:$CONFLUENCE_API_TOKEN" | base64

# Windows PowerShell
[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("$CONFLUENCE_EMAIL:$CONFLUENCE_API_TOKEN"))
```

## Rate Limiting

- If you encounter HTTP 429 (Too Many Requests), wait 5-10 seconds and retry automatically
- Maximum 3 retries with exponential backoff

## Common Headers
```bash
-H "Accept: application/json"
-H "Content-Type: application/json"
-H "Authorization: Basic <base64_encoded_auth>"
```

---

## API Endpoints Reference

Total: **100+ API Endpoints** across 29 API Groups

---

### 1. Admin Key (3 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin-key` | Get Admin Key status |
| POST | `/admin-key` | Enable Admin Key |
| DELETE | `/admin-key` | Disable Admin Key |

**Get Admin Key:**
```bash
curl -X GET "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/admin-key" \
  -H "Authorization: Basic <base64_auth>"
```

**Enable Admin Key (10 min default):**
```bash
curl -X POST "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/admin-key" \
  -H "Authorization: Basic <base64_auth>" \
  -H "Content-Type: application/json" \
  -d '{"durationInMinutes": 10}'
```

---

### 2. Attachment (8 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/attachments` | Get all attachments |
| GET | `/attachments/{id}` | Get attachment by ID |
| DELETE | `/attachments/{id}` | Delete attachment |
| GET | `/attachments/{id}/labels` | Get labels for attachment |
| GET | `/attachments/{id}/operations` | Get permitted operations |
| GET | `/attachments/{id}/versions` | Get attachment versions |
| GET | `/attachments/{id}/versions/{version-number}` | Get version details |
| GET | `/attachments/{id}/footer-comments` | Get attachment comments |

**Get All Attachments:**
```bash
curl -X GET "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/attachments?limit=25" \
  -H "Authorization: Basic <base64_auth>"
```

**Get Attachment by ID:**
```bash
curl -X GET "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/attachments/att123456" \
  -H "Authorization: Basic <base64_auth>"
```

**Delete Attachment (move to trash):**
```bash
curl -X DELETE "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/attachments/att123456" \
  -H "Authorization: Basic <base64_auth>"
```

**Purge (permanently delete) trashed attachment:**
```bash
curl -X DELETE "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/attachments/att123456?purge=true" \
  -H "Authorization: Basic <base64_auth>"
```

---

### 3. Blog Post (15 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/blogposts` | Get all blog posts |
| POST | `/blogposts` | Create blog post |
| GET | `/blogposts/{id}` | Get blog post by ID |
| PUT | `/blogposts/{id}` | Update blog post |
| DELETE | `/blogposts/{id}` | Delete blog post |
| GET | `/blogposts/{id}/attachments` | Get attachments |
| GET | `/blogposts/{id}/custom-content` | Get custom content |
| GET | `/blogposts/{id}/labels` | Get labels |
| GET | `/blogposts/{id}/likes/count` | Get like count |
| GET | `/blogposts/{id}/likes/users` | Get users who liked |
| GET | `/blogposts/{id}/operations` | Get operations |
| GET | `/blogposts/{id}/versions` | Get versions |
| GET | `/blogposts/{id}/versions/{version-number}` | Get version details |
| GET | `/blogposts/{id}/footer-comments` | Get footer comments |
| GET | `/blogposts/{id}/inline-comments` | Get inline comments |

**Get All Blog Posts:**
```bash
curl -X GET "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/blogposts?limit=25&space-id=123" \
  -H "Authorization: Basic <base64_auth>"
```

**Create Blog Post:**
```bash
curl -X POST "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/blogposts" \
  -H "Authorization: Basic <base64_auth>" \
  -H "Content-Type: application/json" \
  -d '{
    "spaceId": "SPACE_KEY",
    "title": "My Blog Post",
    "body": {
      "representation": "storage",
      "value": "<p>Blog post content here</p>"
    }
  }'
```

**Get Blog Post with Body:**
```bash
curl -X GET "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/blogposts/123?body-format=storage" \
  -H "Authorization: Basic <base64_auth>"
```

---

### 4. Comment (12 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/footer-comments` | Get all footer comments |
| POST | `/footer-comments` | Create footer comment |
| GET | `/footer-comments/{comment-id}` | Get footer comment |
| PUT | `/footer-comments/{comment-id}` | Update footer comment |
| DELETE | `/footer-comments/{comment-id}` | Delete footer comment |
| GET | `/footer-comments/{id}/children` | Get child comments |
| GET | `/inline-comments` | Get all inline comments |
| POST | `/inline-comments` | Create inline comment |
| GET | `/inline-comments/{comment-id}` | Get inline comment |
| PUT | `/inline-comments/{comment-id}` | Update inline comment |
| DELETE | `/inline-comments/{comment-id}` | Delete inline comment |
| GET | `/inline-comments/{id}/children` | Get child inline comments |

**Create Footer Comment on Page:**
```bash
curl -X POST "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/footer-comments" \
  -H "Authorization: Basic <base64_auth>" \
  -H "Content-Type: application/json" \
  -d '{
    "pageId": "123456",
    "body": {
      "representation": "storage",
      "value": "<p>Comment content</p>"
    }
  }'
```

**Create Inline Comment:**
```bash
curl -X POST "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/inline-comments" \
  -H "Authorization: Basic <base64_auth>" \
  -H "Content-Type: application/json" \
  -d '{
    "pageId": "123456",
    "body": {
      "representation": "storage",
      "value": "<p>Inline comment</p>"
    },
    "inlineCommentProperties": {
      "textSelection": "selected text",
      "textSelectionMatchCount": 1,
      "textSelectionMatchIndex": 0
    }
  }'
```

**Resolve Inline Comment:**
```bash
curl -X PUT "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/inline-comments/123" \
  -H "Authorization: Basic <base64_auth>" \
  -H "Content-Type: application/json" \
  -d '{
    "version": {"number": 2},
    "resolved": true
  }'
```

---

### 5. Content Properties (40 endpoints)

For: Attachments, Blog Posts, Pages, Custom Content, Whiteboards, Databases, Folders, Comments, Smart Links

| Method | Endpoint Pattern | Description |
|--------|-----------------|-------------|
| GET | `/{type}/{id}/properties` | Get all properties |
| POST | `/{type}/{id}/properties` | Create property |
| GET | `/{type}/{id}/properties/{property-id}` | Get property |
| PUT | `/{type}/{id}/properties/{property-id}` | Update property |
| DELETE | `/{type}/{id}/properties/{property-id}` | Delete property |

**Get Page Properties:**
```bash
curl -X GET "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/pages/123456/properties" \
  -H "Authorization: Basic <base64_auth>"
```

**Create Page Property:**
```bash
curl -X POST "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/pages/123456/properties" \
  -H "Authorization: Basic <base64_auth>" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "custom-key",
    "value": {"nested": "value"}
  }'
```

**Update Page Property:**
```bash
curl -X PUT "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/pages/123456/properties/789" \
  -H "Authorization: Basic <base64_auth>" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "custom-key",
    "value": {"updated": "value"},
    "version": {"number": 2}
  }'
```

---

### 6. Label (14 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/labels` | Get all labels |
| GET | `/labels/{id}/attachments` | Get attachments with label |
| GET | `/labels/{id}/blogposts` | Get blog posts with label |
| GET | `/labels/{id}/pages` | Get pages with label |
| GET | `/attachments/{id}/labels` | Get attachment labels |
| GET | `/blogposts/{id}/labels` | Get blog post labels |
| GET | `/custom-content/{id}/labels` | Get custom content labels |
| GET | `/pages/{id}/labels` | Get page labels |
| GET | `/spaces/{id}/labels` | Get space labels |
| GET | `/spaces/{id}/content/labels` | Get space content labels |

**Get Page Labels:**
```bash
curl -X GET "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/pages/123456/labels" \
  -H "Authorization: Basic <base64_auth>"
```

---

### 7. Page (14 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/pages` | Get all pages |
| POST | `/pages` | Create page |
| GET | `/pages/{id}` | Get page by ID |
| PUT | `/pages/{id}` | Update page |
| DELETE | `/pages/{id}` | Delete page |
| PUT | `/pages/{id}/title` | Update page title |
| GET | `/pages/{id}/attachments` | Get attachments |
| GET | `/pages/{id}/custom-content` | Get custom content |
| GET | `/pages/{id}/labels` | Get labels |
| GET | `/pages/{id}/operations` | Get operations |
| GET | `/pages/{id}/versions` | Get versions |
| GET | `/pages/{id}/versions/{version-number}` | Get version details |
| GET | `/pages/{id}/footer-comments` | Get footer comments |
| GET | `/pages/{id}/inline-comments` | Get inline comments |

**Get All Pages in Space:**
```bash
curl -X GET "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/pages?space-id=123&limit=50" \
  -H "Authorization: Basic <base64_auth>"
```

**Get Page with Body:**
```bash
curl -X GET "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/pages/123456?body-format=storage" \
  -H "Authorization: Basic <base64_auth>"
```

**Create Page:**
```bash
curl -X POST "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/pages" \
  -H "Authorization: Basic <base64_auth>" \
  -H "Content-Type: application/json" \
  -d '{
    "spaceId": "SPACE_KEY",
    "title": "My New Page",
    "parentId": "123456",
    "body": {
      "representation": "storage",
      "value": "<p>Page content in storage format</p>"
    }
  }'
```

**Update Page:**
```bash
curl -X PUT "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/pages/123456" \
  -H "Authorization: Basic <base64_auth>" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "123456",
    "status": "current",
    "title": "Updated Page Title",
    "body": {
      "representation": "storage",
      "value": "<p>Updated content</p>"
    },
    "version": {
      "number": 5,
      "message": "Updated page content"
    }
  }'
```

**Delete Page (move to trash):**
```bash
curl -X DELETE "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/pages/123456" \
  -H "Authorization: Basic <base64_auth>"
```

---

### 8. Space (22 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/spaces` | Get all spaces |
| POST | `/spaces` | Create space |
| GET | `/spaces/{id}` | Get space by ID |
| PUT | `/spaces/{id}` | Update space |
| DELETE | `/spaces/{id}` | Delete space |
| GET | `/spaces/{id}/pages` | Get space pages |
| GET | `/spaces/{id}/pages/search` | Search pages in space |
| GET | `/spaces/{id}/blogposts` | Get space blog posts |
| GET | `/spaces/{id}/content` | Get space content |
| GET | `/spaces/{id}/content/types` | Get content types |
| GET | `/spaces/{id}/labels` | Get space labels |
| GET | `/spaces/{id}/content/labels` | Get space content labels |
| GET | `/spaces/{id}/operations` | Get space operations |
| GET | `/spaces/{id}/permissions` | Get space permissions |
| GET | `/spaces/{id}/properties` | Get space properties |
| POST | `/spaces/{id}/properties` | Create space property |
| GET | `/spaces/{id}/properties/{property-id}` | Get space property |
| PUT | `/spaces/{id}/properties/{property-id}` | Update space property |
| DELETE | `/spaces/{id}/properties/{property-id}` | Delete space property |
| GET | `/spaces/{id}/icons` | Get space icons |
| POST | `/spaces/{id}/icons` | Set space icon |
| GET | `/spaces/{id}/lookups` | Lookup space by key |

**Get All Spaces:**
```bash
curl -X GET "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/spaces?limit=50" \
  -H "Authorization: Basic <base64_auth>"
```

**Get Space by Key:**
```bash
curl -X GET "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/spaces?keys=SPACE_KEY" \
  -H "Authorization: Basic <base64_auth>"
```

**Create Space:**
```bash
curl -X POST "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/spaces" \
  -H "Authorization: Basic <base64_auth>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My New Space",
    "key": "MYSpace",
    "description": {
      "plain": {
        "value": "Space description"
      }
    }
  }'
```

---

### 9. User (9 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/me` | Get current user |
| GET | `/users/{id}` | Get user by ID |
| GET | `/users/bulk` | Get multiple users |
| POST | `/users/bulk` | Bulk get users by emails |
| GET | `/user/access/check-access-by-email` | Check user access by email |
| POST | `/user/access/check-access-by-email` | Check user access |
| GET | `/user/access/invite-by-email` | Get user invite by email |
| POST | `/user/access/invite-by-email` | Invite user by email |
| POST | `/user/access/batch-invite-by-email` | Batch invite users |

**Get Current User:**
```bash
curl -X GET "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/users/me" \
  -H "Authorization: Basic <base64_auth>"
```

**Get User by ID:**
```bash
curl -X GET "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/users/123456" \
  -H "Authorization: Basic <base64_auth>"
```

**Bulk Get Users:**
```bash
curl -X GET "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/users/bulk?ids=123,456" \
  -H "Authorization: Basic <base64_auth>"
```

---

### 10. Version History (8 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/pages/{id}/versions` | Get page versions |
| GET | `/pages/{id}/versions/{version-number}` | Get specific version |
| GET | `/blogposts/{id}/versions` | Get blog post versions |
| GET | `/blogposts/{id}/versions/{version-number}` | Get specific version |
| GET | `/attachments/{id}/versions` | Get attachment versions |
| GET | `/attachments/{id}/versions/{version-number}` | Get specific version |
| POST | `/pages/{id}/versions/restore` | Restore page version |
| POST | `/blogposts/{id}/versions/restore` | Restore blog post version |

**Get Page Versions:**
```bash
curl -X GET "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/pages/123456/versions?limit=10" \
  -H "Authorization: Basic <base64_auth>"
```

**Restore Page Version:**
```bash
curl -X POST "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/pages/123456/versions/restore" \
  -H "Authorization: Basic <base64_auth>" \
  -H "Content-Type: application/json" \
  -d '{"newVersion": {"message": "Restoring previous version"}}'
```

---

### 11. Whiteboard (7 endpoints)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/whiteboards` | Get all whiteboards |
| POST | `/whiteboards` | Create whiteboard |
| GET | `/whiteboards/{id}` | Get whiteboard by ID |
| PUT | `/whiteboards/{id}` | Update whiteboard |
| DELETE | `/whiteboards/{id}` | Delete whiteboard |
| GET | `/whiteboards/{id}/connections` | Get whiteboard connections |
| GET | `/whiteboards/{id}/operations` | Get whiteboard operations |

**Create Whiteboard:**
```bash
curl -X POST "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/whiteboards" \
  -H "Authorization: Basic <base64_auth>" \
  -H "Content-Type: application/json" \
  -d '{
    "spaceId": "123456",
    "title": "My Whiteboard"
  }'
```

---

## Pagination

The V2 API uses cursor-based pagination. Responses include a `_links.next` URL when more results are available.

```bash
curl -X GET "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/pages?space-id=123456&limit=100" \
  -H "Authorization: Basic <base64_auth>"
```

**Response:**
```json
{
  "results": [...],
  "_links": {
    "next": "/wiki/api/v2/pages?cursor=abc123",
    "base": "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki"
  }
}
```

---

## Search

### Search Pages by Title
```bash
curl -X GET "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/pages?title=My%20Page&space-id=123456" \
  -H "Authorization: Basic <base64_auth>"
```

### Get Page with All Details
```bash
curl -X GET "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/pages/123456?include-labels=true&include-properties=true&include-versions=true&body-format=storage" \
  -H "Authorization: Basic <base64_auth>"
```

### Update Page Title
```bash
curl -X PUT "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/pages/123456/title" \
  -H "Authorization: Basic <base64_auth>" \
  -H "Content-Type: application/json" \
  -d '{"value": "New Page Title"}'
```

### Redact Page Content (remove sensitive content)
```bash
curl -X POST "https://$CONFLUENCE_DOMAIN.atlassian.net/wiki/api/v2/pages/123456/redact" \
  -H "Authorization: Basic <base64_auth>" \
  -H "Content-Type: application/json" \
  -d '{
    "version": {"number": 3},
    "body": {
      "representation": "storage",
      "value": "<p>Redacted content</p>"
    }
  }'
```

---

## Error Handling

| Status | Meaning |
|--------|---------|
| 400 | Bad request or malformed data |
| 401 | Invalid credentials or expired token |
| 403 | Permission denied |
| 404 | Resource not found |
| 409 | Conflict (e.g., duplicate title) |
| 429 | Rate limited - wait and retry |
| 500 | Internal server error |

---

## Notes

- **Confluence Storage Format**: Content uses XML-like storage format. Example: `<p>Paragraph</p>`, `<h1>Heading</h1>`, `<ul><li>Item</li></ul>`
- **Version Numbers**: When updating pages, you must increment the version number
- **DELETE Returns 204**: DELETE operations return 204 No Content
- **IDs are Strings**: All IDs are passed as strings
- **Cursor Pagination**: Use the cursor from `_links.next` for pagination
