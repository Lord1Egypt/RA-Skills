# Media Type Fetch Strategies

## YouTube
- **Fetch:** `web_fetch` on the YouTube URL — gets title, description, auto-generated caption snippet if available
- **Limitation:** Full transcript requires yt-dlp or YouTube Data API (not available by default)
- **Workaround:** Note the video and ask user to paste transcript if deep analysis needed
- **What to extract:** Title, channel name, description, video length, comment on content type (tutorial, motivational, essay, etc.)

## Articles / Blog posts
- **Fetch:** `web_fetch` — works well for most articles
- **Limitation:** Paywalled content (NYT, WSJ, etc.) — only gets headline + lede
- **What to extract:** Full text → summarize key ideas + structure

## Tweets / X posts
- **Fetch:** FxTwitter API — `https://api.fxtwitter.com/{username}/status/{tweet_id}`
  - Extract username and tweet_id from URL: `https://x.com/username/status/123456`
  - Returns JSON with full tweet text, author, engagement
- **Thread:** Fetch each tweet in thread individually if linked

## PDFs
- **Fetch:** `pdf` tool
- **What to extract:** Title, author, key argument, structure

## Images
- **Fetch:** `image` tool with prompt: "Describe this image. What is it, what's the message or style, and what makes it notable?"
- **Use cases:** Design inspiration, memes, infographics, screenshots

## Podcast / Audio URLs
- **Limitation:** No audio transcription available
- **What to do:** Fetch the show notes page if it's a podcast page URL; note title + description
- **Flag to user:** "I can save the metadata but can't transcribe the audio — paste the transcript if you have it"

## Substack / Newsletter
- **Fetch:** `web_fetch` — usually works
- **Treat as:** Article

## Reddit threads
- **Fetch:** `web_fetch` — add `.json` to URL for raw data if needed
- **What to extract:** OP post + top comments (summarize the thread arc)

## GitHub repos
- **Fetch:** `web_fetch` on README
- **What to extract:** What it does, tech stack, why it's notable

## Unknown / generic URL
- **Fetch:** `web_fetch`, best effort
- **If it fails:** Ask user to paste the content directly
