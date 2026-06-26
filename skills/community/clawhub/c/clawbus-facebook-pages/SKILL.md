---
name: Facebook Pages
description: >
  Publish and manage Facebook Page content through a preconfigured
  MyBrandMetrics API connection. Use this skill to connect Facebook Pages, list
  connected accounts and available Pages, create Page feed posts, publish
  Page photos or videos, read Page feeds, read and manage comments, and fetch
  Page or post insights. Supports bearer-token or API-key authentication,
  page/account/connection targeting, pagination, unpublished posts, comment
  moderation, and structured JSON API responses.
---

# Facebook Pages

Publish Facebook Page posts, photos, and videos; read Page feeds and comments;
moderate comments; and fetch Page or post insights through the MyBrandMetrics
Facebook Pages API.

Use this skill when the user wants to connect Facebook Pages, list available
Pages, post to a Facebook Page, publish a Page photo, upload a Page video, read
Page posts, reply to Page comments, hide or unhide comments, delete comments, or
check Page and post insights.

Website: [https://www.clawbus.com/](https://www.clawbus.com/)  
MyBrandMetrics API: [https://mybrandmetrics.com/](https://mybrandmetrics.com/)

## Why This Facebook Pages Skill

| This skill | Building your own Facebook Pages integration |
| --- | --- |
| Use one MyBrandMetrics connection for Facebook Pages. | Set up and maintain your own Meta app, auth flow, and Page token storage. |
| Target a Page by `page_id`, `account_id`, or `connection_id` when supported. | Build your own account and Page resolution layer before each request. |
| Publish feed posts, photos, and videos through one script. | Implement separate Page post, photo, and video endpoints yourself. |
| Read feeds, comments, Page insights, and post insights from the same tool. | Wire together multiple Graph API read paths, fields, pagination, and metrics. |
| Create, edit, hide, unhide, and delete comments with explicit commands. | Build your own comment moderation workflow and safety checks. |
| Return the real MyBrandMetrics JSON response. | Build response normalization, error handling, and retry decisions yourself. |

Use this when you want Facebook Page publishing, moderation, and insights
without building a full Facebook Pages backend yourself.

## Core Capabilities

| Capability | Details |
| --- | --- |
| Connect Pages | Start the Facebook Pages OAuth connection flow through MyBrandMetrics. |
| List connections | List connected Meta accounts for the `facebook_pages` source. |
| List Pages | List available Facebook Pages for the connected account. |
| Publish feed posts | Create Page feed posts with text, links, optional picture URLs, and optional unpublished mode. |
| Publish photos | Publish Page photo posts from public image URLs. |
| Publish videos | Publish Page video posts from public video URLs. |
| Read Page feed | Fetch Page feed posts with configurable fields, limit, and pagination cursors. |
| Read comments | Fetch comments for a post or object with fields, limit, and pagination cursors. |
| Manage comments | Create comments, edit comment text, hide or unhide comments, and delete comments. |
| Page insights | Fetch Page insight metrics with period and date range options. |
| Post insights | Fetch post insight metrics by `post_id` or `object_id`. |

## Setup Flow

1. Open [https://mybrandmetrics.com/](https://mybrandmetrics.com/) and sign in.
2. Connect Facebook Pages through MyBrandMetrics.
3. Get a MyBrandMetrics bearer token or API key.
4. Install the `clawbus-facebook-pages` skill.
5. Provide credentials through command-line arguments, environment variables, or
   a workspace `config.json`.
6. List connections and available Pages if you do not already know the target.
7. Run the publish, feed, comment, or insights workflow.

For photos and videos, the media URL must be publicly reachable.

## Credentials

Use a MyBrandMetrics bearer token or API key. You can provide it through command
line flags, environment variables, or a workspace config file. If the target
Page is already known, provide `page_id`; otherwise list available Pages first.

For the full credential shape, see `references/configuration.md`.

## Workflow

Use natural-language prompts after the skill is installed. Include:

- the task: connect, list Pages, publish, read feed, manage comments, or fetch
  insights;
- the target `page_id`, `account_id`, or `connection_id`;
- the post message, link, photo URL, or video URL for publishing;
- the `object_id`, `post_id`, or `comment_id` for comment and insights work;
- the fields, metrics, period, date range, limit, or pagination cursor when
  needed.

Before creating, updating, hiding, unhiding, deleting, or publishing anything,
confirm the target Page, content, IDs, and intended visibility. Read-only list,
feed, comments, and insights calls can run after the target is clear.

## Use The Script Directly

Use `scripts/facebook_pages.py`.

List available Pages:

```bash
python3 scripts/facebook_pages.py list-accounts
```

Publish a Page post:

```bash
python3 scripts/facebook_pages.py publish-post \
  --page-id "PAGE_ID" \
  --message "Hello from the Pages API!" \
  --link "https://www.mybrandmetrics.com"
```

Publish a Page photo:

```bash
python3 scripts/facebook_pages.py publish-photo \
  --page-id "PAGE_ID" \
  --url "https://example.com/image.jpg" \
  --caption "Photo from the Pages API"
```

Read comments:

```bash
python3 scripts/facebook_pages.py comments \
  --page-id "PAGE_ID" \
  --object-id "POST_ID" \
  --limit 25
```

Hide a comment:

```bash
python3 scripts/facebook_pages.py comment-update \
  --page-id "PAGE_ID" \
  --comment-id "COMMENT_ID" \
  --hide
```

Fetch Page insights:

```bash
python3 scripts/facebook_pages.py insights \
  --page-id "PAGE_ID" \
  --metrics "page_impressions,page_fans"
```

## Commands

| Command | Purpose |
| --- | --- |
| `connect` | Start the Facebook Pages OAuth connect flow. |
| `list-connections` | List connected Meta accounts. |
| `list-accounts` | List available Facebook Pages. |
| `publish-post` | Create a Page feed post. |
| `publish-photo` | Create a Page photo post from a public image URL. |
| `publish-video` | Create a Page video post from a public video URL. |
| `feed` | Read Page feed posts. |
| `comments` | Read comments for a post or object. |
| `comment-create` | Create a comment on a post or object. |
| `comment-update` | Edit, hide, or unhide a comment. |
| `comment-delete` | Delete a comment. |
| `insights` | Read Page insight metrics. |
| `post-insights` | Read post insight metrics. |

## Reference Files

| File | Purpose |
| --- | --- |
| `references/configuration.md` | Credential setup, auth modes, base URL, and config examples. |
| `references/examples.md` | Concrete invocation examples for each workflow. |
