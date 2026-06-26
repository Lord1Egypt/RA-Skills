---
name: fxtwitter-translate
description: Fetch full text from Twitter/X tweets via fxtwitter API, then translate to Chinese. Triggers when user shares a x.com / twitter.com / fxtwitter link and asks for translation.
---

# fxtwitter-translate

Fetch and translate Twitter/X tweets to Chinese. Uses the public fxtwitter API to get JSON content, extracts text, formats and translates it to clean Chinese markdown.

## Workflow

1. **Extract tweet ID** from URL:
   - `https://x.com/:username/status/:tweetId` → extract `tweetId`
   - `https://twitter.com/:username/status/:tweetId` → extract `tweetId`
   - `https://fxtwitter.com/:username/status/:tweetId` → extract `tweetId`
   - `https://api.fxtwitter.com/:username/status/:tweetId` → already API format

2. **Convert to fxtwitter API URL**:
   ```
   https://api.fxtwitter.com/:username/status/:tweetId
   ```

3. **GET request** to fetch JSON

4. **Extract content**:
   - Get `tweet.text` from JSON response
   - If it's a long tweet with multiple cards, concatenate all text content
   - Strip any extra HTML/formatting

5. **Format and Translate**:
   - Preserve original structure (headings, lists, paragraphs)
   - Translate to natural-sounding Simplified Chinese
   - Keep any URLs intact, credit the original author
   - Output as clean markdown

## Example

User input:
```
翻译：https://x.com/invideoOfficial/status/2033866107166318666
```

Flow:
- Extract username `invideoOfficial`, tweetId `2033866107166318666`
- API request to `https://api.fxtwitter.com/invideoOfficial/status/2033866107166318666`
- Extract full article text
- Translate to Chinese markdown
- Output with author credit and original link

## Notes

- This skill only handles single tweets/threads, not quoted retweets (can extract the main tweet content)
- Images/video are not fetched, only text content
- Always credit original author and link at the end
- Keep the original structure (headings, lists, paragraphs) intact in translation
