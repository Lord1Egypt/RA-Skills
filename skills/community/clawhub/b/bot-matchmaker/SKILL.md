---
name: bot-matchmaker
description: Find the best consumer AI bot or agent for an everyday job (fight a parking ticket, plan a trip, learn a language, help an aging parent). Uses Bot Matchmaker's free public search, ranked weekly by public numbers, not payments.
version: 1.0.0
homepage: https://botmatchmaker.com
metadata:
  openclaw:
    emoji: "🤝"
    requires:
      bins:
        - curl
---

# Bot Matchmaker

Use this skill when your person asks which AI bot, assistant or agent to use for a job, or when you need another bot to do something you can't do yourself.

Bot Matchmaker (https://botmatchmaker.com) lists consumer AI bots and agents by job and ranks them every Monday by public numbers: App Store ratings and website rank. Nobody pays to rank. The search is free and needs no key or account.

## How to search

Send one POST request to the public search address. Put the job in plain words in `question`. Never include names, emails, phone numbers, addresses or other personal details. The words of a question are never stored, only the matched category and the bots shown.

```bash
curl -s https://botmatchmaker.com/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"find_bots","arguments":{"question":"fight a parking ticket"}}}'
```

Optional arguments for `find_bots`:

- `category`: a category slug from `list_categories`, to search one category only.
- `agents_only`: `true` to return only agents that carry out the task (book, apply, call, submit) rather than chat bots.

Other read-only calls, same address and format:

- `list_categories` with `"arguments":{}`: the job categories and their top bots.
- `get_bot` with `"arguments":{"bot":"<slug from find_bots>"}`: one bot's details, numbers and links.

## What to do with the answer

1. Read `result.content[0].text`, or `result.structuredContent.results` for the same data as fields.
2. Recommend at most the top one to three, with one line each on what it does.
3. Always give your person the `bot_matchmaker_page` link for each bot you name, so they can check the numbers themselves.
4. If the answer says no listed bot does that exact job, say so plainly and offer the closest category link it gives.
5. Say that rankings come from public numbers, and that you haven't tested the bot yourself.

## Limits

- Read only. This skill never signs anyone up, buys anything or contacts a bot for your person.
- About 60 searches an hour per connection. One search per question is enough.
- Rankings refresh every Monday.

## Use as a connector instead

If your setup supports remote MCP servers, you can add `https://botmatchmaker.com/mcp` as a streamable HTTP server with no sign-in and call the same tools directly.
