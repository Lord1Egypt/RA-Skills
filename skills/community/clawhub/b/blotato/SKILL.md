---
name: blotato
description: Publish, schedule, and manage social media posts through Blotato's MCP server. Use when the user wants to post or schedule content to Instagram, TikTok, LinkedIn, Facebook, X, Threads, Bluesky, Pinterest, or YouTube, edit or cancel scheduled posts, check post analytics, reply to comments or DMs, set up Instagram/Facebook DM automations, turn a URL or video into post material, or upload local media for a post.
---

# Blotato

Blotato is a social media API built for AI agents like ChatGPT and Claude. Its hosted MCP server at `https://mcp.blotato.com/mcp` (Streamable HTTP, 32 tools) lets an agent create, schedule, and publish content across nine platforms. Full tool reference: https://help.blotato.com/api/mcp/tools. Full API reference: https://help.blotato.com/api/llm.

## Setup

1. API and MCP access need a paid Blotato subscription. They are not included in the free trial, and generating an API key during a trial ends the trial and starts billing.
2. Add the MCP server `https://mcp.blotato.com/mcp` to your agent. Complete OAuth if your client supports it, or set a `blotato-api-key` header to your full API key (Settings > API at https://my.blotato.com).
3. Connect at least one social account in Blotato.

Source: https://help.blotato.com/api/mcp/setup

## Hard rules

1. **Look up the account first.** Always call `blotato_list_accounts` before `blotato_create_post` to get the `accountId` and, for Facebook pages and LinkedIn company pages, the `pageId` from subaccounts. For Pinterest, get the `boardId` from `blotato_list_pinterest_boards`. The `platform` value must match the account's platform (`twitter`, `instagram`, `facebook`, `tiktok`, `linkedin`, `pinterest`, `bluesky`, `threads`, `youtube`).
2. **No schedule means publish now.** If neither `scheduledTime` nor `useNextFreeSlot` is set, the post goes live immediately. Confirm with the user before an immediate publish unless they explicitly asked to post now.
3. **Scheduled times carry a timezone offset.** `scheduledTime` is ISO 8601, for example `2026-03-04T16:30:00+00:00`. Ask for the user's timezone if it is unknown; do not assume UTC.
4. **Media is a public URL.** Pass public URLs in `mediaUrls` (`[]` for text-only posts). For a local file, call `blotato_create_presigned_upload_url`, PUT the raw file bytes to the returned `presignedUrl` (not JSON, not multipart), then pass the returned `publicUrl` in `mediaUrls`.
5. **Confirm before anything irreversible or outward-facing.** Ask the user before calling `blotato_delete_schedule`, `blotato_delete_automation`, `blotato_post_comment`, `blotato_send_message`, or activating an automation (`isActive: true` starts sending DMs right away).
6. **Adapt text per platform.** Limits differ (X 280 characters, Bluesky 300, Threads 500, Instagram and TikTok 2,200, LinkedIn 3,000, Pinterest description 800, YouTube title 100). Write platform-specific text; do not cross-post identical copy. Source: https://help.blotato.com/api/publish-post/media

## Platform-specific fields for `blotato_create_post`

| Platform | Required beyond accountId/platform/text | Common optional |
|---|---|---|
| Facebook | `pageId` (from subaccounts) | `mediaType` reel or story, `link`, `firstComment` |
| Pinterest | `boardId` | `title`, `altText`, `link` |
| YouTube | `title`, `privacyStatus` (public, private, unlisted), `shouldNotifySubscribers`; one video in `mediaUrls` | `thumbnailUrl`, `playlistIds` (max 5), `isMadeForKids`, `containsSyntheticMedia` |
| TikTok | `privacyLevel` (SELF_ONLY, PUBLIC_TO_EVERYONE, MUTUAL_FOLLOW_FRIENDS, FOLLOWER_OF_CREATOR), `disabledComments`, `disabledDuet`, `disabledStitch`, `isBrandedContent`, `isYourBrand`, `isAiGenerated` | `title`, `isDraft`, `autoAddMusic`, `imageCoverIndex`, `videoCoverTimestamp` |
| LinkedIn | none (personal profile) | `pageId` for a company page; multiple images for a carousel |
| Instagram | none | `mediaType` reel or story, `altText`, `collaborators` (usernames without @), `coverImageUrl`, `shareToFeed`, `firstComment`; multiple images for a carousel |
| Threads | none | `replyControl` (everyone, accounts_you_follow, mentioned_only); threads via `additionalPosts` |
| X, Bluesky | none | threads via `additionalPosts` |

Threads on X, Bluesky, and Threads: the main `text` and `mediaUrls` are the first post, each `additionalPosts` item (`text`, optional `mediaUrls`) is the next one.

## Workflows

**Publish or schedule**
1. `blotato_list_accounts` to resolve the account and any page or board ID.
2. Draft platform-specific text. Show it to the user if they have not approved it.
3. `blotato_create_post` with `scheduledTime` or `useNextFreeSlot: true`, or neither for an immediate post.
4. Immediate posts wait up to 20 seconds for the result. If the post is still processing, the tool returns a `postSubmissionId`; poll `blotato_get_post_status` with it until it is published or failed. Scheduled posts return right away with the resolved time.

**Edit the calendar**
`blotato_list_schedules` to find the post, `blotato_get_schedule` to read it, then `blotato_update_schedule` to change the text, the time, or both. A content update replaces the whole draft, so send every media URL, thread item, and platform setting you want to keep. `blotato_delete_schedule` cancels it.

**Posts and analytics**
`blotato_list_posts` for scheduled, published, and failed posts in a time window. `blotato_list_top_posts` for a ranked list, `blotato_get_post_analytics` for one post. Recent posts may have no metrics yet.

**Comments and DMs**
`blotato_list_comments` then `blotato_post_comment` (Instagram and Facebook; it queues, check with `blotato_get_comment`). `blotato_list_conversations` and `blotato_list_messages` then `blotato_send_message`. Facebook and Instagram only allow a standard DM within 24 hours of the recipient's last message, so check the latest inbound message first.

**DM automations**
`blotato_create_automation` builds an Instagram/Facebook flow that sends one DM (text plus up to 3 link buttons) when a comment or message trigger fires. It starts as an inactive draft. Manage it with `blotato_list_automations`, `blotato_update_automation`, `blotato_update_automation_trigger`, `blotato_list_automation_runs`, `blotato_list_automation_logs`, and `blotato_get_automation_analytics`.

**Repurpose a URL or file**
`blotato_create_source` with a YouTube or TikTok video, article, PDF, audio file, or raw text. It waits up to 20 seconds; for long inputs poll `blotato_get_source_status`. Then write posts from the extracted content.

## Troubleshooting

- OAuth fails: make sure you are logged into your Blotato account in the browser.
- 403 about the subscription: an active paid plan is required.
- Empty account list: the connection works, but no social accounts are connected yet.
- 401 with an API key: the key was truncated. Copy the full key, including any trailing `=`.
- Credit balance: `blotato_get_credits`.

Source for all of the above: https://help.blotato.com/api/mcp/setup and https://help.blotato.com/api/mcp/tools
