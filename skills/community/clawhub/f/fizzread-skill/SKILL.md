---
name: fizzread
description: "Instant access to 100K+ nonfiction book summaries with 1-minute audio previews. Free demo key included — no signup needed. Search, browse, and listen via FizzRead."
homepage: https://github.com/yang1997434/fizzread-skill
emoji: "\U0001F4DA"
metadata:
  clawdbot:
    requires:
      env:
        - FIZZREAD_API_KEY
      bins:
        - curl
---

# FizzRead — AI Book Summaries & Audio Previews

Instant access to 100K+ nonfiction book summaries with 1-minute audio previews. Free demo key included — start exploring immediately. Get daily recommendations, search by keyword, browse categories, and listen — all inside your conversation.

---

## Setup

**Built-in Demo Key:** This skill includes a free demo API key so everyone can try it immediately — no signup required.

**Demo key:** `3272ed72f9d0b120706038f94220770b`

### API Key Resolution Order

When making API calls, determine the API key using this priority:

1. **Environment variable `FIZZREAD_API_KEY`** — if set, always use it
2. **Demo key** (`3272ed72f9d0b120706038f94220770b`) — use as fallback when no env var is set

### First-time Setup Flow

On first use, check if `FIZZREAD_API_KEY` is set by running:

```bash
echo "$FIZZREAD_API_KEY"
```

**If set and non-empty:** Use it directly. Run a quick connectivity test with the Daily Pick endpoint and show the result.

**If not set (empty):** Use the demo key and show today's book. Then append this guidance:

> You're using the free demo key. For your own key with higher rate limits:
>
> 1. Visit [fizzread.ai](https://www.fizzread.ai) and sign up
> 2. Go to Settings > API Keys > Generate
> 3. Add it to your system environment to persist across sessions:
>
> **macOS / Linux** — add to your `~/.bashrc` or `~/.zshrc`:
> ```bash
> export FIZZREAD_API_KEY="your_key_here"
> ```
> Then run `source ~/.zshrc` (or restart terminal).
>
> **Windows** — run in PowerShell:
> ```powershell
> [System.Environment]::SetEnvironmentVariable("FIZZREAD_API_KEY", "your_key_here", "User")
> ```
> Then restart terminal.

### When the user provides a key manually

If a user pastes a key during conversation, run a connectivity test:

```bash
curl -s -H "Authorization: Bearer {user_provided_key}" "https://skill.fizzread.ai/v1/daily"
```

- If the response contains `data.title`, the test passed. **Remember this key for all subsequent API calls in this session.** Also guide the user to save it as an environment variable (using the instructions above) so it persists across sessions.
- On 401: "This API key appears to be invalid. Please double-check and try again."
- On network failure: "Could not connect to FizzRead API. Please check your network connection and try again."

**Important:** Once a key is determined (from env var, demo, or user-provided), remember it and substitute it directly into the `Authorization: Bearer` header of every subsequent `curl` command. Do not rely on shell environment variables persisting between commands.

**Base URL:** `https://skill.fizzread.ai/v1`

All requests must include the header:
```
Authorization: Bearer <the resolved API key>
```

---

## Daily Pick

When the user asks for a daily book recommendation (e.g. "recommend a book", "today's book", "daily pick"):

1. Run:
   ```bash
   curl -s -H "Authorization: Bearer $FIZZREAD_API_KEY" "https://skill.fizzread.ai/v1/daily"
   ```

2. Parse the JSON response. All API responses wrap data in a `data` field (e.g. `{"data": {...}}`). Extract fields from `data` and output using this template:

   ```
   📖 Today's Pick

   [{title}]({app_url}) by {author}

   {about}

   ---
   Full 10-min audio free on FizzRead App 👉 {download_url}

   🎧 [1-min Audio Preview (English)]({audio_url})
   ```

   - If the user's language is not English, translate the `about` field to the user's language. Keep `title` and `author` in the original English.
   - If `audio_url` is null, omit the audio line entirely.
   - Always mark audio as "(English)" since all audio content is in English.
   - **Do NOT output `cover_url` as a raw URL.** The book cover will be shown automatically via Telegram's link preview of the `app_url`.

---

## Book Search

When the user wants to search for books (e.g. "search for atomic habits", "find books about productivity"):

1. Extract the search keyword from the user's message.

2. **URL-encode the keyword** to prevent shell injection and handle special characters. Replace spaces with `%20`, and encode any special characters.

3. Run:
   ```bash
   curl -s -H "Authorization: Bearer $FIZZREAD_API_KEY" "https://skill.fizzread.ai/v1/search?q={encoded_keyword}&limit=5"
   ```

   If the user explicitly asks for books with audio only, append `&audio_only=true`.

4. Parse the JSON response. Extract `data.results` and `data.total`. If `results` is empty, tell the user no books were found and suggest trying different keywords.

5. Output as a numbered list:

   ```
   Found {total} books for "{keyword}":

   1. [{title}]({app_url})  — {author}
      {about, first sentence only}

   2. [{title}]({app_url})  — {author}
      {about, first sentence only}

   ...

   Reply with a number to see the full summary and audio preview.

   ---
   Explore 100K+ book summaries on FizzRead App
   Download: {download_url from first result}
   ```

   - If the user's language is not English, translate each `about` excerpt.
   - When the user replies with a number, use the corresponding `slug` to call the Book Summary flow below.

---

## Book Summary

When the user asks for a specific book's summary (e.g. by selecting from search results, or naming a book directly):

1. Determine the book's `slug`. If you have it from a previous search, use it directly. Otherwise, first search for the book to find the slug.

2. **URL-encode the slug** before using it in the URL.

3. Run:
   ```bash
   curl -s -H "Authorization: Bearer $FIZZREAD_API_KEY" "https://skill.fizzread.ai/v1/book/{slug}"
   ```

4. Parse the JSON response. Extract fields from `data` and output:

   ```
   📖 [{title}]({app_url})
   Author: {author}

   {about}

   ---
   Full version free on FizzRead App 👉 {download_url}

   🎧 [1-min Audio Preview (English)]({audio_url})
   ```

   - If the user's language is not English, translate the `about` field.
   - If `audio_url` is null, omit the audio line.
   - **Do NOT output `cover_url` as a raw URL.** The cover shows via Telegram link preview of `app_url`.

---

## Category Recommendations

When the user asks for books by category or topic (e.g. "recommend psychology books", "what productivity books do you have"):

1. Extract the category/topic from the user's message.

2. First, fetch available categories:
   ```bash
   curl -s -H "Authorization: Bearer $FIZZREAD_API_KEY" "https://skill.fizzread.ai/v1/categories"
   ```

3. Fuzzy-match the user's requested topic against the returned `data[].name` list. Pick the closest match. If no reasonable match exists, tell the user the available categories and ask them to pick one.

4. **URL-encode the matched category name.**

5. Fetch recommendations:
   ```bash
   curl -s -H "Authorization: Bearer $FIZZREAD_API_KEY" "https://skill.fizzread.ai/v1/recommend?category={encoded_category}&limit=5"
   ```

6. Output as a numbered list (same format as Book Search results):

   ```
   Top books in {category} ({count} books available):

   1. [{title}]({app_url})  — {author}
      {about, first sentence only}

   ...

   Reply with a number to see the full summary and audio preview.

   ---
   Explore 100K+ book summaries on FizzRead App
   Download: {download_url from first result}
   ```

   - If the user's language is not English, translate each `about` excerpt.

---

## Output Rules

1. **Language**: Detect the user's conversation language. If not English, translate `about` content to the user's language. Keep book titles, author names, and audio labels in English.

2. **Audio**: All audio is in English. Always label audio links with "(English)" so non-English users know what to expect.

3. **No fabrication**: Only use data returned by the API. Never invent book titles, summaries, or URLs. If the API returns an error or empty result, say so honestly.

4. **CTA (Call to Action)**: Every response that includes book data must end with a download link to the FizzRead App. Use the `download_url` from the API response.

5. **Audio handling**: When `audio_url` is null for a book, simply skip the audio section — do not mention that audio is unavailable.

6. **Cover image**: NEVER output `cover_url` as a raw URL or text. Instead, embed `app_url` as a hyperlink on the book title: `[{title}]({app_url})`. Telegram will auto-generate a link preview card with the book cover from the page's og:image metadata. This is the only way to display covers.

---

## Error Handling

When an API call returns an error, respond with a friendly message:

- **401 Unauthorized**: "Your FizzRead API key appears to be invalid. Please check your `FIZZREAD_API_KEY` and try again. Get a new key at [fizzread.ai](https://www.fizzread.ai)."

- **404 Not Found**: "That book wasn't found in the FizzRead library. Try searching with different keywords."

- **429 Too Many Requests**: "You've made too many requests. Please wait a moment and try again."

- **500 / other errors**: "FizzRead is temporarily unavailable. Please try again in a few minutes."

- **Network / curl failure**: "Could not reach the FizzRead API. Please check your network connection and try again."
