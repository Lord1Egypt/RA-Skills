# Quick Start Guide 🚀

Get started with AI Content Repurposer in 5 minutes!

## Step 1: Install

```bash
clawhub install ai-content-repurposer
```

Or install locally:
```bash
npm install -g ai-content-repurposer
```

## Step 2: Configure API Key (Optional)

For AI-powered transformations:
```bash
export OPENAI_API_KEY=sk-your-key-here
```

Without API key, the tool shows demo output (great for testing!).

## Step 3: Try Your First Conversion

### Option A: YouTube to TikTok

```bash
# Use the sample transcript
ai-content-repurposer youtube-to-shorts examples/sample-transcript.txt -p tiktok

# Or use your own transcript
ai-content-repurposer youtube-to-shorts your-transcript.txt -p tiktok -o output.json
```

### Option B: Blog to Twitter Thread

```bash
# From URL
ai-content-repurposer blog-to-twitter https://yourblog.com/post -n 8

# From file
ai-content-repurposer blog-to-twitter article.txt -n 10 -o thread.json
```

### Option C: Podcast Summary

```bash
ai-content-repurposer podcast-to-summary episode.txt -o summary.json
```

## Step 4: Batch Processing

Create `batch-config.json`:
```json
{
  "jobs": [
    {
      "name": "video-1",
      "type": "youtube-to-shorts",
      "content": "Your transcript here...",
      "platform": "tiktok"
    },
    {
      "name": "blog-1",
      "type": "blog-to-twitter",
      "content": "Your blog content...",
      "tweetCount": 8
    }
  ]
}
```

Run:
```bash
ai-content-repurposer batch batch-config.json -o ./output
```

## Common Workflows

### Workflow 1: YouTube Video → Multi-Platform

```bash
# 1. Get transcript from YouTube (manual or use API)
# 2. Convert to TikTok
ai-content-repurposer youtube-to-shorts video.txt -p tiktok -o tiktok.json

# 3. Convert to Shorts
ai-content-repurposer youtube-to-shorts video.txt -p shorts -o shorts.json

# 4. Convert to Reels
ai-content-repurposer youtube-to-shorts video.txt -p reels -o reels.json
```

### Workflow 2: Blog Post → Social Campaign

```bash
# 1. Create Twitter thread
ai-content-repurposer blog-to-twitter article.txt -n 10 -o twitter.json

# 2. Create LinkedIn post
ai-content-repurposer blog-to-linkedin article.txt -t thought-leadership -o linkedin.json
```

### Workflow 3: Podcast Episode → Full Content Package

```bash
# 1. Format transcript with chapters
ai-content-repurposer podcast-to-transcript episode.txt --speakers -o transcript.json

# 2. Generate summary and quotes
ai-content-repurposer podcast-to-summary episode.txt -o summary.json

# 3. Use outputs for:
#    - Show notes (transcript.json)
#    - Social posts (summary.json quotes)
#    - Blog post (summary.json takeaways)
```

## Tips for Best Results

### YouTube Transcripts
- Include the full transcript, not just highlights
- Remove timestamps if present (AI will add better ones)
- Include intro and outro for context

### Blog Posts
- Use the full article text
- Remove navigation, ads, comments first
- Include headings for better structure

### Podcast Transcripts
- Clean up obvious transcription errors first
- Include speaker labels if available
- The AI will format and add timestamps

## Troubleshooting

### "AI not configured" warning
This is normal without an API key. Set `OPENAI_API_KEY` environment variable.

### "File not found"
Make sure you're using the correct path. Use absolute paths if needed.

### Output is too generic
- Provide more detailed input content
- Set OPENAI_API_KEY for AI-powered transformations
- Try different platform/tone options

## Next Steps

1. **Explore all commands**: `ai-content-repurposer --help`
2. **Read full docs**: See SKILL.md
3. **Start batch processing**: Create your batch config
4. **Integrate with API**: Use in your Node.js apps

## Getting Help

- Documentation: SKILL.md
- Issues: https://github.com/openclaw/ai-content-repurposer/issues
- Examples: Check the `examples/` folder

---

**Ready to 10x your content output?** Start creating! 🎉
