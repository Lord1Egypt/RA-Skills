# Content Creator Skill

`Content Creator Skill` is a GitHub-ready OpenClaw skill scaffold for tracking YouTube creators from pasted links, normalizing follow targets, and preparing concise update cards for new uploads.

The published skill slug in this repo is `creator-feed-watch`. I kept the repo name broad and the skill name specific so the project can later grow beyond YouTube without confusing users about what the skill does today.

This repo is licensed under `MIT-0`, which matches ClawHub's publish-time license requirement.

## Install in OpenClaw

For local OpenClaw testing, install from the project path:

```bash
openclaw skill install --path ./content-creator-skill
```

OpenClaw's skill lifecycle and local install flow are documented here:
- https://openclawdoc.com/docs/skills/installation
- https://openclawdoc.com/docs/skills/creating-skills/

After you publish to GitHub or ClawHub, OpenClaw can install the skill from a repository or registry entry depending on the user's setup.

## Current MVP

- Normalize pasted YouTube inputs such as channel URLs, `@handles`, video URLs, and channel IDs
- Work out of the box without a YouTube API key by using public YouTube pages and feeds
- Resolve supported YouTube inputs into a stable channel target with the YouTube Data API
- Fetch the latest uploads from the channel's uploads playlist
- Persist a local JSON watchlist of followed creators
- Check the watchlist for newly published uploads
- Prepare and dispatch notification payloads when the runtime exposes a delivery adapter
- Prepare a channel-friendly update card from video metadata
- Provide a minimal, testable Node runtime entry point that matches the OpenClaw skill layout

## Not Implemented Yet

- Polling or webhook-based new video detection
- Transcript-aware summarization

## Suggested Roadmap

1. Add scheduled checks so OpenClaw can run this without a manual trigger.
2. Add a delivery adapter that posts updates into OpenClaw-connected channels.
3. Add transcript retrieval and better summaries when captions are available.
4. Add dedupe and retry behavior for production notification flows.

## Project Layout

```text
content-creator-skill/
  SKILL.md
  manifest.yaml
  config.example.yaml
  package.json
  src/
  test/
```

## Local Development

```bash
cd content-creator-skill
npm run check:release
npm test
```

## Configuration

This skill now has two modes:

- Zero-config mode: no API key required, using public YouTube pages and feeds
- Enhanced mode: optional `youtube_api_key` for stronger and more reliable resolution

Optional configuration:

```yaml
youtube_api_key: "YOUR_YOUTUBE_DATA_API_KEY"
summary_style: "brief"
watchlist_path: "./data/watchlist.json"
delivery_target: "telegram:my-channel"
```

If you do provide a key, it can be supplied through OpenClaw skill config or `YOUTUBE_API_KEY`.

## Watchlist Actions

- `add_follow`: resolve a YouTube input and persist it in the local watchlist
- `list_follows`: return all persisted follow targets
- `remove_follow`: remove a creator by channel ID, URL, handle, username, or original source input
- `check_watchlist_updates`: fetch the newest upload for each followed creator and return only the new ones
- `notify_watchlist_updates`: build notification messages for new uploads and deliver them through a runtime adapter when available

## Example Inputs

Add a creator:

```json
{
  "action": "add_follow",
  "source": "https://www.youtube.com/@OpenAI"
}
```

Check for new uploads without sending:

```json
{
  "action": "check_watchlist_updates"
}
```

Notify new uploads through the runtime adapter:

```json
{
  "action": "notify_watchlist_updates",
  "delivery_target": "telegram:my-channel"
}
```

## Delivery Behavior

`notify_watchlist_updates` tries the following runtime interfaces in order:

- `context.deliver(notification)`
- `context.notify(notification)`
- `context.sendMessage(text, notification)`
- `context.channel.send(text, notification)`
- `context.channels.send(target, notification)`

If none of those exist, the skill returns the prepared notifications without marking them as seen.

## Publish to ClawHub

When you are ready to publish:

```bash
npm run release:dry
openclaw clawhub login
openclaw skill publish .
```

ClawHub will validate the manifest and skill metadata, run tests, bundle the skill, and publish a new version. Publishing behavior and semver rules are documented here:
- https://openclawdoc.com/docs/skills/clawhub/
- https://openclawdoc.com/docs/skills/creating-skills/
