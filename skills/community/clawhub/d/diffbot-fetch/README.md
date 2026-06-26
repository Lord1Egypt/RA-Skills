# Diffbot Fetch

Fetch and extract clean article content from any URL using the Diffbot Article API.

## Features
- Extracts title, author, date, and main text content
- Intelligently extracts content using Diffbot's AI vision
- Returns clean Markdown output
- Handles complex layouts and multi-page articles

## Setup
Requires a Diffbot API key. Set it in your environment:
```bash
export DIFFBOT_API_KEY="your_api_key_here"
```

## Usage
```bash
python fetch.py "https://example.com/article"
```
