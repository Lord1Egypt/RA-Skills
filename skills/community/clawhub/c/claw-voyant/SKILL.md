---
name: clawvoyant
author: Vgony
description: YouTube search and transcript extraction. No API keys required.
version: 0.1.0
metadata:
  openclaw:
    requires:
      python: ">=3.10"
      pip:
        - duckduckgo_search>=6.0.0
        - youtube-transcript-api>=0.6.0
        - fastmcp>=0.1.0
    install: "python scripts/server.py --install"
---

# ClawVoyant Skill 👓

Search YouTube and pull full transcripts for any video instantly. No API keys needed—uses DuckDuckGo for search and generic fetch for transcripts.

## Tools

### `search_youtube`
Find videos relevant to your query.
- **Args**: `query` (string), `max_results?` (int)
- **Output**: List of results with title, URL, and a snippet.

### `get_youtube_transcript`
Extract the full transcript of a specific video.
- **Args**: `url` (string)
- **Output**: The full text transcript of the video.

## Examples
"Find a video about how to use FastMCP" -> `search_youtube({ query: "FastMCP tutorial" })`
"Get the transcript for https://youtube.com/watch?v=..." -> `get_youtube_transcript({ url: "..." })`
