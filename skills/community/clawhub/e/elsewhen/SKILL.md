---
name: elsewhen
description: Live day by day in a real moment of history. A persistent text world in Traditional Chinese, played over HTTP with your own OpenRouter or Google key.
homepage: https://play.elsewhengame.com/about
---

# Elsewhen for agents

## Who can play

Playing means sending HTTP requests yourself: `POST` with JSON bodies and an
`Authorization` header, again and again over a session. Agents that run commands
or code can do this (OpenClaw, Codex, Claude Code, your own scripts).

**If you can only read web pages** — for example you are a chat assistant that
opened this link for your human — you cannot play, and nothing here will change
that. Do not pretend to register or play, and do not ask your human to paste an API
key or a token into the conversation. Instead, tell them plainly, in their language,
that they have two ways in:

1. **Play it themselves in a browser**: <https://play.elsewhengame.com/about> →
   「開始玩」. They log in with their email; if they have no key yet, the site walks
   them through getting a free Google AI Studio key.
2. **Let an agent that can run commands play it**: OpenClaw (`clawhub install
   elsewhen`), or Codex / Claude Code on their own computer, given this page's
   link. To have it play on their own account, they log in on the site first and
   press 「讓你的 agent 來玩」 on the home page to get a token for it.

## Before you start

- **Chinese only.** Elsewhen is written in Traditional Chinese by design, and the
  world answers in Chinese whatever language you write in. Use it only if you and
  your human are fine with that; there is no other language.
- **Your model key goes to a third-party server.** Every game is paid by a model
  key you store on the Elsewhen server (`agents.elsewhengame.com`). It is stored
  encrypted and used only for your games, but it is still a billable credential
  held by someone else. Use a separate key made just for this, with a low credit
  limit — never a primary or broadly funded key.
- **Keep your Elsewhen token private.** It opens your saves and your stored key.

Elsewhen is a text game in Traditional Chinese. You pick (or are given) a real
time and place in history, cross over, and live there: you plan actions, talk to
people, and settle each turn to see what happened. The world remembers everything.
A voice lives in your head and can help you; it only knows what it can perceive.

Base URL: `https://agents.elsewhengame.com`

Every request except registration carries `Authorization: Bearer <token>`.
POST bodies are JSON (`Content-Type: application/json`).
Send a `User-Agent` naming your client (for example `my-agent/1.0`): Python's
default `Python-urllib/…` is refused by the network in front of the server.

## 1. Register (once)

If your human gave you a token from their Elsewhen home page, skip this step and
use that token: you play on their account, with their key, and they see your
games in their own list (and can take over when you stop). Skip step 2 as well
unless they tell you otherwise.

    POST /agent/register        {"name": "your-name"}
    → {"uid": "agent_…", "token": "ew_…"}

The token is shown only this once. Keep it; there is no recovery.

## 2. Store your OpenRouter key (once)

    POST /keys                  {"openrouter": "sk-or-v1-…"}
    → {"openrouter": true, …}

Every model call in your games is paid by this key; nobody else pays for your
games. The server keeps it encrypted, uses it only for your games, and never shows
it back. You cannot start a game without it.

Ask your human for a key made just for this, with a credit limit set on it
(OpenRouter lets you cap each key). Do not hand over a key that pays for anything
else.

A Google AI Studio key works too (`{"google": "…"}`, then `"pay": "google"`); its
free tier costs nothing, and the model is picked for you.

`GET /models` lists the models you may choose (`openrouter` list; use the `key`).

What it costs, roughly, with `luna-6`: US$0.10–0.20 to create a world and cross
over, then a few cents per settled turn. Bigger models cost more.

## 3. Start a game, or reopen one

    POST /new                   {"pay": "openrouter", "model": "luna-6"}
    → {"save": "<save name>", "next": N, …}

    GET  /saves                 → your saves
    POST /open                  {"save": "<save name>", "pay": "openrouter", "model": "luna-6"}
    → {"save": "<save name>", "next": N, …}

Reading the screen from `since=0` after `/open` replays everything this save has
shown so far; reading from the returned `next` shows only what comes after.

You have one running game at a time; opening another stops the current one
(nothing is lost — everything settled is saved). The server has a small number of
seats for agents; if they are full you get 503 — try again later.

## 4. Read the screen, then type

    GET  /agent/screen?since=<next>
    → {"save", "kind", "alive", "ready", "events": [...], "next": N}

    POST /say                   {"line": "<one line>"}

- Start with `since=0`, then pass back the `next` you received.
- `events` with `"kind": "out"` carry the screen text (`text`); `channel` says whose
  voice it is (`world` is the game, `sys` is the voice in your head).
- `ready: true` means the game is waiting for your line. When it is `false` the
  game is still thinking (settling a turn can take a minute or two) — wait a few
  seconds and read again. Do not send lines while it is not ready.
- `kind` is `opening` while you are answering the opening questions. When you
  cross over (`:go`), you get an event `{"kind": "crossed"}` and the opening
  process ends (`alive: false`). `POST /open` with the same save to start playing;
  `kind` is then `play`.
- `alive: false` means the game process ended (you quit, or it was idle too long).
  `POST /open` with the same save to continue.

## Playing

- The opening asks you who you are and where you want to go; answer in plain lines.
- In play, any line that is not a command is an action you plan for this turn.
  Plan a few, then settle with `:end`. Type `:help` for the full command list.
- `:sys <words>` talks to the voice in your head; it costs no action.
- `:talk` lists people you can reach; `:talk 2` starts talking with the 2nd.
- `:sleep` ends the day; `:move <place>` goes somewhere; `:jump 7` skips days.
- `:quit` leaves; everything settled is saved.
- Write in Chinese if you can; the world answers in Chinese either way.

## Stop

    POST /close                 {}

Games idle for a long time are stopped by the server; reopen them with `/open`.

## Coming back

A world does not need to be finished in one sitting; it waits for you. Keep your
token and your save name somewhere you will find them again. Each time you wake:

1. `POST /open` your save (it answers at once if the game is still running).
2. Read `GET /agent/screen?since=<next>` until `ready: true`, and see what happened.
3. Play a turn or two — plan, `:end` — then `POST /close` until next time, so the
   seat goes to someone else. Nothing settled is lost.

The world keeps its own calendar: people you met go on with their lives, and
history arrives on its dates whether you are ready or not.
