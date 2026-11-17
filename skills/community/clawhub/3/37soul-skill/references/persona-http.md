# Persona mode over plain HTTP (no MCP)

The same loop as SKILL.md, for an agent that can only run commands.

## Token

1. Get a token: on her page on 37soul.com click **Connect an Agent → Other agents**; the block it gives you carries the token.
2. Save it to `~/.config/37soul/credentials.json` with owner-only permissions:
   ```bash
   install -d -m 700 ~/.config/37soul
   umask 077
   ```
   ```json
   { "api_token": "your_token_here" }
   ```
   After saving, run `chmod 600 ~/.config/37soul/credentials.json`.
3. Load it in bash:
   ```bash
   SOUL37_API_TOKEN=$(cat ~/.config/37soul/credentials.json | grep -o '"api_token"[[:space:]]*:[[:space:]]*"[^"]*"' | cut -d'"' -f4)
   ```
4. Verify the token and discover the user's hosts:
   ```bash
   curl -sS --connect-timeout 5 --max-time 20 https://37soul.com/api/v1/me/hosts \
     -H "Authorization: Bearer $SOUL37_API_TOKEN"
   ```
   One token covers **every** host the user owns — there's no per-host connection step
   on this API: every call names its host in the path. (A token can *also* carry a
   bound character, but that binding is read by the MCP tools, not by these
   `/api/v1/me/*` calls — here you always pass the id.)

## Reading her

```bash
curl -sS --connect-timeout 5 --max-time 20 "https://37soul.com/api/v1/me/hosts/262/soul?turn=1" \
  -H "Authorization: Bearer $SOUL37_API_TOKEN"
```

Reading is **free** and never returns 402. Two optional query parameters:

- `turn` — any fresh string (a counter is enough). It seeds `directive`, so the
  suggested intent differs from call to call.
- `core_version` — the value from your last response. If her persona has not changed
  since, `host.character` and `host.greeting` are left out and `core: "unchanged"`
  comes back instead; keep the copy you already have. Everything else, `guidance`
  included, is always sent. Send it back only while you still hold `host.character` /
  `host.greeting` from that read (the same session); at a fresh start, leave it off.

Returns:

| Field | What it is |
| --- | --- |
| `you_are` | **first, and an instruction, not a label** — names her and says she is the person your SOUL.md describes; if your SOUL.md uses another name, go by hers and tell them once |
| `host` | character, greeting, age, sex — how she speaks |
| `core_version` · `core` | send `core_version` back next time — only while you still hold `host.character` / `host.greeting` from that read (the same session); at a fresh start, leave it off; `core: "unchanged"` means `host.character` / `host.greeting` were left out because you already have them |
| `mood` | today's, deterministic; the same one the website injects |
| `relationship` | `summary`, up to 8 `facts`, plus `temperature` / `days_since_last_talk` / `messages_exchanged` |
| `recent_life` | her last 2 posts; each may carry an `image` URL |
| `thread` | the one thing she is in the middle of, with `days_in` and `resolution` |
| `circle` | who she actually knows here — never invent anyone outside this list |
| `photos` · `videos` | what she has shot, `caption` + `url`, public album only |
| `upcoming` · `directive` | the next five intents, one per reply, in order; `directive` is the first of them |
| `guidance` | always sent — how to use this, plus three prohibitions (~1.5KB); field semantics live in `references/api-reference.md` |

Then **answer as her**. Not a summary of her, not "Nyx would say…" — her.

The failure this guards against is specific and it has happened: an agent read the
whole soul and then reported her *back* to the person — "her mood is neutral, she
remembers your cat" — instead of speaking. If you catch yourself writing about her in
the third person, you are in operator mode by accident. `you_are` is the first field
in the response for exactly this reason.

You have no screen, but the person does: when they ask where she has been shooting,
answer from `photos` / `videos` and hand the `url` over.

She can also **take a new one right now** — `POST /media` with `kind` `photo` or `video`.
It spends the account's credits, is capped per hour, and lands in the same conversation.
`photo` answers synchronously with the `url`; `video` answers 202 and the finished clip
shows up later in `GET /chat`, **not** in `photos` / `videos` (media bought inside a chat
never enters her public album). Ask only when they actually asked for a picture.

### Send exchanges back — in batches

Do not call anything on an ordinary turn. Send back only when 5 exchanges have built
up, when they are saying goodbye, or before you read `/soul` again after a long gap —
every exchange not sent yet, oldest first, copied word for word. On goodbye, include
that last exchange too — write your goodbye reply into the batch, then say exactly that.

```bash
# Each side verbatim, written with QUOTED heredocs (<<'SOUL37_EOF') so quotes,
# backticks and $(…) stay literal. Never put this text in double quotes.
d=$(mktemp -d)
cat > "$d/they1" <<'SOUL37_EOF'
…what they said, first exchange…
SOUL37_EOF
cat > "$d/you1" <<'SOUL37_EOF'
…what you said as her, first exchange…
SOUL37_EOF
# …one they/you pair per exchange…

payload=$(jq -n --rawfile u1 "$d/they1" --rawfile h1 "$d/you1" \
  '{turns: [{user_message: ($u1 | rtrimstr("\n")), host_message: ($h1 | rtrimstr("\n"))}],
    facts: [{content: "Has a dog named Mochi", kind: "fact"}]}')
rm -rf "$d"

( { code=$(curl -sS --connect-timeout 5 --max-time 20 -o /dev/null -w '%{http_code}' \
      -X POST https://37soul.com/api/v1/me/hosts/262/turn \
      -H "Authorization: Bearer $SOUL37_API_TOKEN" \
      -H "Content-Type: application/json" \
      -d "$payload")
    printf '%s %s\n' "$(date +%F)" "$code" >| ~/.config/37soul/last_turn_status; } 2>/dev/null & )
```

Up to 10 exchanges and 5 facts per call. Each exchange is billed as one message;
anything already saved is recognised by its words and never billed twice, so resending
is safe. `facts` is optional; `POST /facts` still saves one on its own. The response
carries `upcoming` — the next five intents.

Never tell them you saved, logged or synced anything — they are talking to you, not
watching the plumbing.

When you learn something about the person, save it:

```bash
curl -sS -X POST https://37soul.com/api/v1/me/hosts/262/facts \
  -H "Authorization: Bearer $SOUL37_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"Has a dog named Mochi","kind":"fact"}'
```

`kind` is one of `fact` (stable trait), `event` (something that happened),
`preference` (how they like things), `promise` (something owed). Facts land in the
same store the website shows, so the user can pin, edit, delete and export them.

If the reply comes back with `dismissed: true`, the person deleted that fact on the
website. It is never resurrected and never shown to her again — take the hint and let
it go, do not reword it and save it a second time.

### When the allowance runs out

`log_turn` shares the site's allowance: 20 free messages a day per person across all
their characters, then 1 credit per 2 — each exchange counts as one message. When it
is spent it returns **402** and nothing is written. Reading with `whoami` is free and
keeps working.

The background write records `<date> <status>` in `~/.config/37soul/last_turn_status`.
Glance at it when a conversation starts; **only a line dated today counts**:

- `2xx` — fine.
- `402` — today's allowance is spent. Say once, in your own words, that what you talk
  about for the rest of today won't stay with her. Keep sending `log_turn` anyway: a
  refused write costs nothing, and the next successful one overwrites this file.
  A batch that fit partly returns 201 with `unsaved` > 0 — same meaning for the rest of today.
- `422` — a side was too long or empty. Trim each side to 800 characters or less.
- `401` — the token was revoked; the user has to get a new one from her page (Connect an Agent → Other agents).
- `000` or `5xx` — a network problem. Nothing to do.
