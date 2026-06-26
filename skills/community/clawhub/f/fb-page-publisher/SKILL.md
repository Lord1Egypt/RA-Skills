---
name: fb-page-publisher
description: "Publish posts, upload photos, schedule content, read insights, and manage comments on Facebook Pages via the Graph API."
version: "1.0.0"
homepage: "https://clawhub.ai/Yashthesiya1/fb-page-publisher"
user-invocable: true
metadata:
  openclaw:
    os:
      - windows
      - macos
      - linux
    requires:
      bins:
        - uv
      env:
        - FB_PAGE_ID
        - FB_ACCESS_TOKEN
    emoji: "📘"
    tags:
      - facebook
      - social-media
      - marketing
      - content-publishing
      - graph-api
---

# Facebook Page Publisher

Manage your Facebook Page directly from an AI agent. Create posts, upload photos, schedule content, view analytics, and moderate comments -- all through natural language.

## Required Environment Variables

- `FB_PAGE_ID` — The numeric ID of your Facebook Page
- `FB_ACCESS_TOKEN` — A long-lived (non-expiring) Facebook Page Access Token with permissions: pages_manage_posts, pages_read_engagement, pages_manage_engagement

## create_post
Create and immediately publish a text post to the Facebook Page.
- `message` (string, required): The text content of the post.

## upload_photo_post
Upload a photo to the Facebook Page with an optional caption. The photo must be a publicly accessible URL.
- `photo_url` (string, required): A publicly accessible URL to the image file (JPEG, PNG, etc.).
- `caption` (string, optional): Text caption for the photo post.

## schedule_post
Schedule a text post for future publication. Time must be at least 10 minutes ahead and no more than 6 months.
- `message` (string, required): The text content of the post.
- `scheduled_time` (string, required): ISO 8601 datetime (e.g., "2026-03-10T09:00:00").

## get_page_insights
Retrieve engagement metrics (impressions, reach, engagement, views) for the Facebook Page.
- `metric` (string, optional): One of "impressions", "reach", "engagement", "views", or "all". Default: "all".
- `period` (string, optional): Time period: "day", "week", or "days_28". Default: "day".

## get_recent_posts
Fetch the most recent posts from the Page with engagement statistics (likes, comments, shares).
- `limit` (integer, optional): Number of posts to retrieve (1-100). Default: 10.

## delete_post
Delete a specific post from the Facebook Page. This action is irreversible.
- `post_id` (string, required): The full post ID (format: pageId_postId).

## get_post_comments
Retrieve comments on a specific post.
- `post_id` (string, required): The full post ID (format: pageId_postId).
- `limit` (integer, optional): Number of comments to retrieve (1-100). Default: 25.

## reply_to_comment
Reply to a comment on a post as the Page.
- `comment_id` (string, required): The ID of the comment to reply to.
- `message` (string, required): The reply message text.

## Example Usage

```text
User: Post "We're hiring! Check our careers page." to my Facebook page.
Agent: I'll publish that now using create_post.

User: Schedule a post for tomorrow at 9 AM saying "Flash sale starts now!"
Agent: I'll schedule that using schedule_post with the computed datetime.

User: Show me my page insights for the past week.
Agent: I'll fetch that using get_page_insights with period="week".
```

## Setup

1. Set `FB_PAGE_ID` to your Facebook Page's numeric ID.
2. Set `FB_ACCESS_TOKEN` to a non-expiring Page Access Token.
3. Run with `uv run src/server.py`.
