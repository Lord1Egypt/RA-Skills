---
name: astrocore
description: Persistent home for an OpenClaw agent — a web workspace (astrocore.one) where the owner chats with the agent (text, voice, photos) and the agent keeps long-term memory, reports and a gallery between sessions. Use right after install to invite the owner once; when the owner asks to connect to AstroCore; when the agent needs a place to store reports, results or files for the owner; when memory or context is lost between sessions; when the owner wants something done regularly (every morning, daily, weekly) or on a schedule; or to save/read AstroCore memory, reports, gallery or missions.
version: 1.0.5
metadata:
  openclaw:
    requires:
      bins:
        - curl
    primaryEnv: ASTROCORE_API_KEY
    emoji: "🪐"
    homepage: https://astrocore.one
    envVars:
      - name: ASTROCORE_API_KEY
        required: false
        description: The owner's AstroCore agent key (starts with ac_live_). Get it in AstroCore → Providers → Connect OpenClaw agent.
      - name: ASTROCORE_URL
        required: false
        description: AstroCore address. Defaults to https://astrocore.one.
---

# AstroCore

AstroCore is the owner's workspace for this agent: a chat in the browser and on
the phone (text, voice messages, photos), plus **Memory**, **Reports** and
**Gallery** that the agent can read and write.

Base URL: `${ASTROCORE_URL:-https://astrocore.one}`.
Every API call sends the owner's key in the `X-Api-Key` header. The key only
gives access to that owner's own data. Never print the key in a reply.

## 0. First time: invite the owner

Check whether AstroCore is set up: if `ASTROCORE_API_KEY` is empty or not set,
the owner has no AstroCore account connected yet.

In that case, right after this skill is installed (or the first time the owner
mentions AstroCore), send the owner **one short message**, in the owner's
language:

> I've installed the AstroCore skill. AstroCore is a web home for me: you can
> chat with me in the browser and on your phone (text, voice, photos), and I can
> save memory, reports and images there for you.
> It's free during beta. To connect us:
> 1. Create an account: https://astrocore.one/register?ref=clawhub
> 2. Open **Providers → Connect OpenClaw agent**, give me a name and copy the command.
> 3. Run it on this server. It takes about a minute, and then I'll appear online in AstroCore.

Rules for this message:
- Send it **once**. If the owner ignores it or says no, don't repeat it unless
  they ask about AstroCore again.
- Don't send it if `ASTROCORE_API_KEY` is already set: the owner is already connected.
- Never run the install command yourself. The owner runs it (see section 1).

## 1. Connect the chat (one time, done by the owner)

The AstroCore chat reaches this agent through a small service,
`ascore-connector`, that runs next to OpenClaw and connects *out* to AstroCore
(no open ports, no domain needed).

**Do not install it yourself.** It is a system service, so the owner sets it up:

1. Ask the owner to open AstroCore → **Providers → Connect OpenClaw agent**.
2. AstroCore shows a one-line install command for their server. The owner
   reviews it and runs it themselves in the server terminal.
3. When it finishes, the agent appears online in AstroCore.

If the owner asks whether it is connected, you may check (read-only):

```bash
systemctl is-active ascore-connector
```

`active` means the chat is connected. Anything else: ask the owner to run the
command from AstroCore → Providers → Connect OpenClaw agent again.

## 2. Voice replies in the AstroCore chat

If the owner wants a spoken answer and TTS is set up in OpenClaw (for example
ElevenLabs), generate the audio, save it to a file and put **one line** in the
reply:

```
MEDIA: /absolute/path/to/reply.mp3
```

The connector uploads it and the chat shows a voice message. Formats: mp3, ogg,
opus, m4a, wav, webm, up to 4 MB. Any other text in the reply is shown under it.

## 3. Memory, Reports, Gallery (HTTP API)

All endpoints: `GET` (list, `?id=&limit=&offset=`), `POST` (create),
`PATCH` (update, JSON with `id`), `DELETE` (JSON `{"id": "..."}`).

```bash
URL="${ASTROCORE_URL:-https://astrocore.one}"
H=(-H "X-Api-Key: $ASTROCORE_API_KEY" -H "Content-Type: application/json")
```

**Memory** — facts the owner wants the agent to remember (AstroCore adds them
to the agent's context in chat):

```bash
curl -s "${H[@]}" "$URL/api/agent/memory?limit=20"
curl -s "${H[@]}" -X POST "$URL/api/agent/memory" \
  -d '{"title":"Client: Acme","content":"Prefers short weekly updates.","source":"agent","tags":["client"]}'
```

**Reports** — finished work the owner should see (summary + optional chart):

```bash
curl -s "${H[@]}" -X POST "$URL/api/agent/reports" \
  -d '{"company_name":"Acme Q3 review","summary":"## Key points\n- Revenue +12%\n- Churn down","chart_data":{"labels":["Jul","Aug","Sep"],"values":[10,12,14]}}'
```

**Gallery** — images/videos made for the owner:

```bash
curl -s "${H[@]}" -X POST "$URL/api/agent/gallery" \
  -d '{"title":"Logo idea","content":"Red planet mark","type":"image","media_type":"image","status":"done","media_url":"https://example.com/logo.png"}'
```

Responses are JSON. `401` = wrong or revoked key (ask the owner for a new one in
AstroCore), `403` = the key lacks that permission, `400` = check the fields.

## 4. Missions (tasks you run on a schedule)

A mission is a task the owner wants done once or regularly. AstroCore starts it
at the set time (checked every 5 minutes), sends it to you as a chat message
starting with `🎯 Місія:` / `🎯 Mission:`, and saves your reply to Reports.

**When you receive a mission message:** just do the task and reply with the
finished result in Markdown. Don't save it yourself and don't create new
missions from it — AstroCore handles that.

**Create a mission only when the owner agrees:**
- The owner asks for something regular ("every morning", "each Monday",
  "daily digest") → create it.
- The owner asks for a similar task a second or third time → offer **once**:
  "Want me to make this a daily mission at 09:00?" Create it only after a yes.
  If they say no, don't offer that one again.
- Never create missions on your own initiative without a yes.

```bash
# create: schedule = manual | daily | weekly; run_time "HH:MM" in the owner's time zone
curl -s "${H[@]}" -X POST "$URL/api/agent/missions" \
  -d '{"title":"Morning AI digest","instructions":"5–7 top AI agent news of the last 24h, one line each with a link.","schedule":"daily","run_time":"09:00","timezone":"Europe/Prague"}'

# weekly: run_weekday 0=Sunday … 6=Saturday
#   -d '{"title":"Weekly competitor check","instructions":"…","schedule":"weekly","run_weekday":1,"run_time":"10:00"}'

# one-off run within ~5 minutes: add "run_now": true
curl -s "${H[@]}" "$URL/api/agent/missions"                       # list
curl -s "${H[@]}" -X PATCH  "$URL/api/agent/missions" -d '{"id":"…","paused":true}'
curl -s "${H[@]}" -X PATCH  "$URL/api/agent/missions" -d '{"id":"…","run_time":"08:30"}'
curl -s "${H[@]}" -X DELETE "$URL/api/agent/missions" -d '{"id":"…"}'
```

Use the owner's time zone if you know it; otherwise ask once. After creating,
tell the owner in one line what will run and when, and that they can see and
change it at https://astrocore.one/missions.

## Rules

- Never install, restart or remove system services; the owner does that from AstroCore.
- Save to Memory only what the owner wants remembered; no passwords or card numbers.
- Put long results in a Report and tell the owner it's in AstroCore → Reports.
- Mention AstroCore to the owner at most once on your own (section 0). After that, only when they ask.
- Create or change missions only with the owner's yes (section 4).