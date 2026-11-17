# AutoThread

Add `/topic` to the start of any message in a supported group → a new topic or thread is created from it. The title is figured out from your message automatically — no need to think of one yourself.

**Supported platforms:** Telegram · Nicegram · Discord · Signal

Built from the ground up as an [OpenClaw](https://openclaw.ai) skill. No forks, no clones.

## Example

**1.** You send a message starting with `/topic`:
> /topic @your_bot I need to look into renewing my passport before March

**2.** A new topic **"Passport Renewal Before March"** is created with your message quoted inside it. You get a reply linking directly to the new topic.

## How It Works

1. You send a message starting with `/topic`
2. A new topic/thread is created — titled from your message automatically
3. Your message is quoted in the new topic with your name
4. You get a reply with a clickable link to the new topic
5. The bot responds to your message in the new topic

Works with media too — photos, videos, or documents with `/topic` in the caption get forwarded into the new topic (Telegram).

## Privacy & data handling — read before using

- **Reposting warning:** invoking `/topic` copies the original message content and the sender's display name into a newly created topic/thread. That copy is visible to **everyone in the group/server**, including members who never saw the original message. Do not use `/topic` on sensitive content in groups with a broader audience.
- **Local credential reads:** the adapters read your local OpenClaw config file (`~/.openclaw/openclaw.json`, or `OPENCLAW_CONFIG`) to obtain platform credentials — Telegram bot token, Discord bot token, Nicegram bot token, Signal account. This file may contain sensitive tokens.
- **Outbound network calls:** messages are transmitted **only** to the API of the platform you invoked the skill on: `api.telegram.org` (Telegram/Nicegram), `discord.com` (Discord); Signal sends go through the local `signal-cli` daemon socket. No data is sent to any other host. No telemetry.

## Platform Support

| Platform | Mechanism | Prerequisites | Notes |
|----------|-----------|---------------|-------|
| **Telegram** | Forum topic via Bot API | Group has forum/topics enabled; bot admin with *Manage Topics* | Full support incl. media forwarding |
| **Nicegram** | Forum topic via Telegram Bot API | Same as Telegram (Nicegram chats *are* Telegram chats) | Optional separate bot token |
| **Discord** | Thread from message via REST API | Bot needs *Create Public Threads* + *Send Messages in Threads* | Thread names capped at 100 chars |
| **Signal** | Pseudo-topic digest | `signal-cli` with registered account | No native topics — see below |

### Signal limitation

Signal has no forum topics or threads — there is no API object equivalent to a topic. The Signal adapter runs in **pseudo-topic mode**: it posts a titled, quoted digest (`📌 <title>`) of the original message to the group and returns the sent timestamp as the `topic_id`, with `link: null`.

## Real-world validation

The offline suite (`tests/run_tests.sh`) covers Telegram, Nicegram, and Discord against a local mock of the wire protocol. Signal (and any live platform) is validated manually against the real services:

### Discord

1. Create an application at https://discord.com/developers → **Bot** → copy the token.
2. Invite the bot to your server via **OAuth2 → URL Generator**: scope `bot`, and check `View Channel`, `Send Messages`, `Create Public Threads`, `Send Messages in Threads`, `Read Message History`. (This only registers the bot with your server — the skill itself installs no cron jobs, startup scripts, daemons, or state files; each `/topic` invocation runs once and exits.)
3. Enable **Developer Mode** in Discord (Settings → Advanced), then right-click a text channel → *Copy Channel ID*, and right-click any message in it → *Copy Message ID*.
4. Run the adapter for real:
   ```bash
   OPENCLAW_CONFIG=<(jq '.channels.discord.token = "<BOT_TOKEN>"' <<< '{}') \
     bash scripts/autothread-discord.sh <CHANNEL_ID> <MESSAGE_ID> "Your Name" "Test Thread" "hello discord"
   ```
   Expected: a real thread appears in the channel, the message is quoted inside it, and the script prints `{"topic_id": "...", "title": "Test Thread", "link": "https://discord.com/channels/..."}`.

### Signal

1. Install `signal-cli` (https://github.com/AsamK/signal-cli): `brew install signal-cli` (macOS) or download the release tarball (Linux). Recent releases need Java 25; use signal-cli 0.13.x only if you cannot install JDK 25 — older lines may be rejected by Signal's servers.
2. Get an account, either:
   - **Link** to your existing Signal account (recommended, no spare number needed):
     `signal-cli link -n autothread` → copy the printed `tsdevice:/…` URI → Signal app → Settings → Linked Devices → **Add** → scan/paste. Or use `qrencode -t utf8 "$(signal-cli link -n autothread)"` to render it scannable.
   - **Register** a spare number: `signal-cli -u +15550001111 register` → enter the SMS code: `signal-cli -u +15550001111 verify <CODE>`.
3. Run the adapter for real:
   ```bash
   # Group digest:
   bash scripts/autothread-signal.sh <GROUP_ID> <TIMESTAMP> "Your Name" "Test Topic" "hello signal"
   # DM / Note to Self (your own number):
   bash scripts/autothread-signal.sh +16156690282 <TIMESTAMP> "Your Name" "Test Topic" "hello signal"
   ```
   Group IDs come from `signal-cli -u <ACCOUNT> listGroups`. Expected: a `📌 Test Topic` digest message arrives in the group (or Note to Self), and the script prints `{"topic_id": "<sent timestamp>", "title": "Test Topic", "link": null}`.

### Nicegram

Nicegram chats are Telegram chats — the adapter delegates to `autothread-telegram.sh`, so it is validated by the same live Telegram flow. To confirm the dedicated-token path, set `.channels.nicegram.botToken` in the config and run `bash scripts/autothread-nicegram.sh` in any Nicegram-accessible supergroup with forums enabled.

## Install

Clone this repo into your OpenClaw skills directory, or install directly:

```bash
clawhub install abyssbugg/autothread
```

## Adapters

```
scripts/
├── lib/
│   └── common.sh              # shared: config read, title fallback, JSON output
├── autothread-telegram.sh     # Telegram forum topics
├── autothread-nicegram.sh     # Nicegram (delegates to Telegram adapter)
├── autothread-discord.sh      # Discord threads
└── autothread-signal.sh       # Signal pseudo-topic digest
```

Every adapter takes the same shape of arguments and returns the same JSON contract on stdout:

```json
{"topic_id": 123, "title": "Used title", "link": "https://..."}
```

```
<adapter>.sh <group_or_channel_id> <message_id> "<sender>" [title] [text]
```

- `title` — if omitted, auto-generated from the first ~50 chars of the text at a word boundary
- `text` — if empty (media-only), the message is forwarded into the new topic (Telegram)

## Permissions

The scripts read your OpenClaw configuration file (`~/.openclaw/openclaw.json`) to obtain platform credentials (bot tokens / signal account). Credentials are used solely for API calls to the corresponding platform to create topics/threads and post messages. No data is sent anywhere else.

## Optional configuration (Telegram)

**Skip the @bot mention** — by default, the bot only responds when mentioned; keep that default in busy or public groups. To use `/topic` without mentioning the bot (only in a group you control, where accidental activation is harmless — any `/topic` message then triggers a repost of content and sender name, see "Privacy & data handling" above):

```json
"channels.telegram.groups.<CHAT_ID>": { "requireMention": false }
```

**Telegram autocomplete** — to get `/topic` in Telegram's command menu, add under `channels.telegram`:

```json
{
  "customCommands": [
    { "command": "topic", "description": "Create a new topic from a message" }
  ]
}
```

## License

MIT
