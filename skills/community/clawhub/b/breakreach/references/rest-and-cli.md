# Breakreach without MCP: CLI, REST, SDKs

Everything the MCP tools do is also a REST endpoint under `https://api.breakreach.com/v1`, with an API key (Breakreach, Settings → API & MCP, `br_...`). The rules of SKILL.md are the same: account ids from the accounts call, `scheduledAt` in the workspace timezone, media as public URLs.

## CLI

`npx breakreach` (Node 18+), or `npm install -g breakreach`.

```bash
npx breakreach login                    # asks for the key; or: echo "$KEY" | npx breakreach login
npx breakreach whoami                   # workspaces and their timezone
npx breakreach accounts --json
npx breakreach post "Text" --to instagram,linkedin --media ./photo.jpg --next-slot --json
npx breakreach post "Text" --to x --now
npx breakreach post "Text" --to x:northbeam --at 2026-10-20T09:00
npx breakreach post "Text" --to linkedin --draft
npx breakreach post - --to x --now < post.txt
npx breakreach posts --status failed --json
npx breakreach next-slot
npx breakreach upload ./clip.mp4        # prints the hosted URL
npx breakreach delete <postId>
```

- `--to`: an account id, a network when the workspace has one account there, or `network:name`. Comma-separated or repeated.
- When: exactly one of `--now`, `--at <time>`, `--next-slot`, or `--draft` (which can go with `--at`).
- `--media` takes files (uploaded first) and URLs. Pinterest: `--board <id>`, `--pin-link <url>`. Reddit: `--subreddit`, `--flair`. TikTok: `--tiktok-privacy PUBLIC_TO_EVERYONE`.
- `--workspace <slug>` on any command, `--json` for machine output. Exit code 1 = the API refused (the message says why), 2 = a usage error.
- Each `post` sends an Idempotency-Key and retries safely; to make re-running a whole script safe, pass `--idempotency-key <something stable>`.

## REST with curl

```bash
H=(-H "Authorization: Bearer $BREAKREACH_API_KEY" -H "Content-Type: application/json")

curl -s https://api.breakreach.com/v1/accounts "${H[@]}"

curl -s https://api.breakreach.com/v1/posts "${H[@]}" \
  -H "Idempotency-Key: $(uuidgen)" \
  -d '{"content": "Text", "accountIds": ["<id>", "<id>"], "media": ["https://…/photo.jpg"], "useNextSlot": true}'

curl -s https://api.breakreach.com/v1/media/upload -H "Authorization: Bearer $BREAKREACH_API_KEY" -F file=@photo.jpg
```

Retry a POST that got no answer with the same `Idempotency-Key` and the same body: within 24 hours it returns the first response (header `Idempotent-Replayed: true`). 409 = still running, retry shortly; 422 = the key was used for a different body.

| Endpoint | MCP tool |
| --- | --- |
| `GET /v1/workspaces`, `POST /v1/workspaces` | `list_workspaces`, `create_workspace` |
| `GET /v1/accounts` | `list_accounts` |
| `POST /v1/connect-links` | `create_connect_link` |
| `POST /v1/posts`, `GET /v1/posts?status=` | `create_post`, `list_posts` |
| `PATCH /v1/posts/{id}`, `DELETE /v1/posts/{id}` | `update_post`, `delete_post` |
| `POST /v1/media` (`{url}`), `POST /v1/media/upload` (multipart `file`) | `upload_media` (URL only) |
| `GET /v1/next-slot`, `GET /v1/pinterest-boards` | `get_next_slot`, `list_pinterest_boards` |
| `GET /v1/posts/{id}/metrics`, `GET /v1/performance`, `GET /v1/post-insights` | `get_post_metrics`, `get_content_performance`, `get_post_insights` |
| `GET /v1/accounts/stats`, `GET /v1/accounts/trends`, `GET /v1/analytics` | `get_account_stats`, `get_account_trends`, `get_analytics` |
| `GET /v1/comments`, `GET /v1/posts/{id}/comments`, `POST /v1/comments/reply` | `list_recent_comments`, `get_post_comments`, `reply_to_comment` |
| `GET /v1/inbox`, `GET` / `POST /v1/inbox/{conversationId}/messages` | `list_conversations`, `get_conversation_messages`, `send_message` |
| `/v1/comment-dm-rules` (GET, POST, PATCH, DELETE) | `*_comment_dm_rule(s)` |

Full spec: https://api.breakreach.com/v1/openapi.json

## SDKs

```ts
import { Breakreach } from "breakreach"; // npm install breakreach
const br = new Breakreach(); // BREAKREACH_API_KEY
const { accounts } = await br.listAccounts();
await br.createPost({ content: "Text", accountIds: [accounts[0].id], useNextSlot: true });
```

```python
from breakreach import Breakreach  # pip install breakreach
br = Breakreach()
accounts = br.list_accounts()["accounts"]
br.create_post(content="Text", account_ids=[accounts[0]["id"]], use_next_slot=True)
```

Both send the Idempotency-Key and retry for you; `BreakreachError` carries `status` and the API's `message`.
