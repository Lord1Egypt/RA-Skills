---
name: Instagram Publisher
description: >
  Publish Instagram images, Reels, and carousels, check Instagram publishing
  status, fetch recent Instagram direct messages, and send Instagram direct
  messages through a preconfigured MyBrandMetrics API connection. Supports
  local files, remote media URLs, captions, carousel items, Reel feed sharing,
  thumbnail offset, publish status checks, and messaging workflows after
  Instagram Insights is connected in MyBrandMetrics.
compatibility:
  tools:
    - bash
    - python
  dependencies:
    - requests
---

# Instagram Publisher

Publish Instagram images, Reels, and carousels, check publish status, and work
with Instagram direct messages through bundled MyBrandMetrics scripts.

Use this skill when the user wants to publish to Instagram, post to IG, upload a
Reel, create a carousel, publish a hosted media URL, publish a local media file,
check an Instagram publish job, fetch recent Instagram DMs, or send an
Instagram direct message.

Website: [https://www.clawbus.com/](https://www.clawbus.com/)  
MyBrandMetrics API: [https://mybrandmetrics.com/](https://mybrandmetrics.com/)

## Why This Instagram Publisher

| This skill | Building your own Instagram publishing and messaging integration |
| --- | --- |
| Sign in to MyBrandMetrics with Google and connect Instagram Insights. | Set up and maintain your own Meta developer integration. |
| Use a MyBrandMetrics API key, connection ID, and account ID for publishing. | Manage app credentials, account selection, publishing tokens, and token handling yourself. |
| Publish images and Reels from local files or remote URLs with one script. | Implement media upload, hosted media handling, and publish requests for each media type. |
| Build mixed carousels by passing local files or URLs as `--items`. | Upload every carousel child, collect child IDs, wait for processing, and publish the final carousel yourself. |
| Set captions, Reel feed sharing, thumbnail offset, wait behavior, and status checks from CLI flags. | Build separate request handling for metadata, media-type differences, retries, and publish-status polling. |
| Fetch recent Instagram DMs and send replies with bundled messaging scripts. | Implement Instagram messaging endpoints and handle Meta messaging-window errors yourself. |

Use this when you want Instagram publishing and messaging workflows without
building a full Instagram backend yourself.

## Core Capabilities

| Capability | Details |
| --- | --- |
| Image publishing | Publish a single Instagram image from a remote URL or local file. |
| Reels publishing | Publish an Instagram Reel from a remote video URL or local video file. |
| Carousel publishing | Publish multi-item carousels from images and videos, including mixed local files and remote URLs. |
| Post metadata | Set captions, Reel feed sharing, thumbnail offset, and wait behavior. |
| Publish status checks | Check an existing Instagram publish job with a returned publish ID. |
| Direct message fetch | Fetch recent Instagram direct messages with a configurable `--limit`. |
| Direct message send | Send a message to a `conversation_id` returned by the message fetch script. |
| Natural-language workflows | Use chat instructions after the skill is installed and credentials are configured. |

## Setup Flow

1. Open [https://mybrandmetrics.com/](https://mybrandmetrics.com/) and sign in
   with Google.
2. In MyBrandMetrics, open **Data sources**.
3. Connect **Instagram Insights** as a data source.
4. Wait until the MyBrandMetrics connection is ready.
5. Get the MyBrandMetrics API key, Instagram connection ID, and Instagram
   account ID from MyBrandMetrics.
6. Install the `instagram-publish` skill.
7. Provide credentials through command-line arguments, environment variables,
   or a workspace `config.json`.
8. Start an image, Reel, carousel, publish-status, or direct-message workflow
   with natural-language instructions or direct scripts.

Messaging scripts only require the API key and connection ID. Publishing scripts
also require the account ID.

## Credential Options

The scripts load credentials in this order:

1. Command-line arguments such as `--api-key`, `--connection-id`, and
   `--account-id`.
2. Environment variables:
   `INSTAGRAM_API_KEY`, `INSTAGRAM_AUTHORIZATION_TOKEN`,
   `INSTAGRAM_CONNECTION_ID`, `INSTAGRAM_ACCOUNT_ID`, and optionally
   `INSTAGRAM_PUBLISH_CONFIG`.
3. A workspace `config.json` file with an `instagram` object.

Example `config.json`:

```json
{
  "instagram": {
    "authorization_token": "YOUR_API_KEY",
    "connection_id": "YOUR_CONNECTION_ID",
    "account_id": "YOUR_ACCOUNT_ID"
  }
}
```

Do not commit real API keys, connection IDs, or account IDs.

## Workflow

Use natural-language prompts in chat after the skill is installed. Include:

- the task: publish, check status, fetch messages, or send a message;
- the media URL, local file path, or carousel item list;
- the post type when it is not obvious: `IMAGE`, `REELS`, or `CAROUSEL`;
- the caption;
- whether a Reel should be shared to feed;
- the publish ID for status checks;
- the message `conversation_id` and message text for DM replies.

Before publishing, confirm the Instagram account, media source, post type, and
caption. For carousels, review every item before posting. For direct messages,
confirm the target `conversation_id` and exact message text.

Instagram direct messaging is subject to Meta platform policy and
messaging-window limits. If the API returns a policy error, show the real
response instead of retrying indefinitely.

## Use The Scripts Directly

Use `scripts/publish_instagram.py` for publishing and status checks.

Single image from URL:

```bash
python3 scripts/publish_instagram.py \
  --type IMAGE \
  --url "https://example.com/image.jpg" \
  --caption "Hello World!"
```

Reel from local file:

```bash
python3 scripts/publish_instagram.py \
  --type REELS \
  --path "/path/to/video.mp4" \
  --caption "Check this out!" \
  --thumb-offset 1000
```

Mixed carousel:

```bash
python3 scripts/publish_instagram.py \
  --type CAROUSEL \
  --items "/path/to/img1.jpg" "https://example.com/video2.mp4" \
  --caption "My Carousel"
```

Check publish status:

```bash
python3 scripts/publish_instagram.py \
  --check-id "PUBLISH_ID"
```

Fetch recent direct messages:

```bash
python3 scripts/receive_messages.py \
  --limit 25
```

Send a direct message:

```bash
python3 scripts/send_message.py \
  --conversation-id "CONVERSATION_ID" \
  --message "Thanks for reaching out!"
```

## Parameters

| Parameter | Script | Required | Purpose |
| --- | --- | --- | --- |
| `--api-key` | all scripts | No, if configured elsewhere | MyBrandMetrics API key. |
| `--connection-id` | all scripts | No, if configured elsewhere | Instagram connection ID from MyBrandMetrics. |
| `--account-id` | publish script | No, if configured elsewhere | MyBrandMetrics Instagram account ID for publishing. |
| `--config` | all scripts | No | Path to a custom `config.json`. |
| `--type` | publish script | No | `IMAGE`, `REELS`, or `CAROUSEL`; default is `IMAGE`. |
| `--caption` | publish script | No | Instagram caption text. |
| `--url` | publish script | For URL-based single media | Remote media URL for a single image or Reel. |
| `--path` | publish script | For local single media | Local media path for a single image or Reel. |
| `--items` | publish script | For carousel | Space-separated carousel item URLs or paths. |
| `--thumb-offset` | publish script | No | Reel or video carousel thumbnail offset in milliseconds. |
| `--no-feed` | publish script | No | Disable sharing Reels to feed. |
| `--no-wait` | publish script | No | Do not wait for publishing or media processing completion. |
| `--check-id` | publish script | For status checks | Check status of an existing publish ID. |
| `--limit` | receive messages script | No | Number of recent messages to fetch; default is `25`. |
| `--conversation-id` | send message script | Yes | Conversation ID returned by `receive_messages.py`. |
| `--message` | send message script | Yes | Direct message text to send. |

## Reference Files

| File | Purpose |
| --- | --- |
| `references/configuration.md` | Supported credential sources, config shape, and secret-handling rules. |
| `references/publishing-examples.md` | Concrete commands for publishing, status checks, and direct messages. |

The scripts print the real JSON response from the MyBrandMetrics API. Treat that
response as the source of truth; do not fabricate publish IDs, media container
IDs, message IDs, or success states.
