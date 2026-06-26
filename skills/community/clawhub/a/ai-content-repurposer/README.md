# AI Content Repurposer 🎬

**Transform long-form content into multiple formats instantly.**

Turn 1 piece of content into 10+ platform-optimized assets. Save hours of manual work. Maximize your content ROI.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Node](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen)

## 🚀 What It Does

AI Content Repurposer automatically transforms your long-form content into platform-specific formats:

```
YouTube Video  ──→ TikTok, Shorts, Reels scripts
Blog Post      ──→ Twitter threads, LinkedIn posts
Podcast        ──→ Transcripts, summaries, quote cards
```

## ⚡ Quick Start

### Install

```bash
# Via ClawHub
clawhub install ai-content-repurposer

# Or via npm
npm install -g ai-content-repurposer
```

### Setup

```bash
# Set your OpenAI API key
export OPENAI_API_KEY=sk-...
```

### Use

```bash
# Convert YouTube transcript to TikTok
ai-content-repurposer youtube-to-shorts transcript.txt -p tiktok

# Convert blog to Twitter thread
ai-content-repurposer blog-to-twitter https://yourblog.com/post -n 8

# Generate podcast summary
ai-content-repurposer podcast-to-summary episode.txt -o summary.json
```

## 📋 Features

### 🎬 YouTube → Short-Form Video Scripts

Transform video transcripts into engaging scripts for:
- **TikTok** (up to 3 minutes)
- **YouTube Shorts** (up to 60 seconds)
- **Instagram Reels** (up to 90 seconds)

**Includes:**
- Hook (first 3 seconds)
- Body points
- Visual cues
- Call-to-action
- Hashtags

### 📝 Blog → Social Media Posts

**Twitter Threads:**
- Auto-split into 280-character tweets
- Numbered thread format (1/X, 2/X...)
- Engagement hooks
- Strategic hashtags

**LinkedIn Posts:**
- Professional tone options
- "See more" hook optimization
- White space formatting
- Engagement questions
- Industry hashtags

### 🎙️ Podcast → Text Content

**Formatted Transcripts:**
- Chapter markers
- Timestamps (optional)
- Speaker labels (optional)
- Cleaned filler words
- Proper punctuation

**Summaries & Quotes:**
- Episode summary (3 sentences)
- Key takeaways (bullet points)
- Shareable quotes (timestamped)
- Social post suggestions

### 🔄 Batch Processing

Process multiple content pieces at once:

```json
{
  "jobs": [
    {
      "name": "video-1",
      "type": "youtube-to-shorts",
      "content": "...",
      "platform": "tiktok"
    },
    {
      "name": "blog-1",
      "type": "blog-to-twitter",
      "content": "...",
      "tweetCount": 8
    }
  ]
}
```

## 📖 Documentation

Full documentation: [SKILL.md](./SKILL.md)

### All Commands

```bash
# YouTube conversions
ai-content-repurposer youtube-to-shorts <transcript> -p [tiktok|shorts|reels]

# Blog conversions
ai-content-repurposer blog-to-twitter <url-or-file> -n <tweet-count>
ai-content-repurposer blog-to-linkedin <url-or-file> -t <tone>

# Podcast conversions
ai-content-repurposer podcast-to-transcript <file> [--speakers] [--no-timestamps]
ai-content-repurposer podcast-to-summary <file>

# Batch processing
ai-content-repurposer batch <config.json> -o <output-dir>

# Interactive mode
ai-content-repurposer interactive
```

## 💡 Examples

### Example 1: TikTok from YouTube

```bash
# Save YouTube transcript to file
echo "Your transcript here..." > video.txt

# Convert to TikTok script
ai-content-repurposer youtube-to-shorts video.txt -p tiktok -o tiktok.json
```

**Output:**
```json
{
  "title": "3 Productivity Hacks",
  "hook": "Stop working harder. Start working smarter.",
  "body": ["Point 1", "Point 2", "Point 3"],
  "cta": "Follow for more!",
  "hashtags": ["#productivity", "#tips"],
  "visualCues": ["[Show clock]", "[Text overlay]"]
}
```

### Example 2: Twitter Thread from Blog

```bash
ai-content-repurposer blog-to-twitter \
  https://example.com/my-blog-post \
  -n 10 \
  -o thread.json
```

### Example 3: Podcast Summary

```bash
ai-content-repurposer podcast-to-summary \
  episode-transcript.txt \
  -o episode-summary.json
```

## 🛠️ API Usage

Use in your Node.js applications:

```javascript
const ContentConverter = require('ai-content-repurposer');

const converter = new ContentConverter({
  apiKey: process.env.OPENAI_API_KEY
});

// Convert content
const result = await converter.blogToTwitterThread(blogContent, 8);
console.log(result.tweets);
```

## 🎯 Use Cases

### Content Creators
- Scale content output without more work
- Maintain presence on all platforms
- Focus on creation, not repurposing

### Marketing Teams
- Turn one campaign into 20+ assets
- Consistent messaging across channels
- Faster time-to-market

### Podcasters
- Auto-generate show notes
- Create social media content
- Extract quotable moments

### Agencies
- Serve more clients with same resources
- Standardize content workflows
- White-label ready (coming soon)

## 💰 Pricing

**$79/month** - Unlimited transformations

Includes:
- ✅ All conversion types
- ✅ Batch processing
- ✅ API access
- ✅ Priority support
- ✅ Regular updates

## 🔧 Requirements

- Node.js >= 18.0.0
- OpenAI API key (for AI features)
- Internet connection

## 📦 Installation Options

### Option 1: ClawHub (Recommended)

```bash
clawhub install ai-content-repurposer
```

### Option 2: npm

```bash
npm install -g ai-content-repurposer
```

### Option 3: From Source

```bash
git clone https://github.com/openclaw/ai-content-repurposer
cd ai-content-repurposer
npm install
npm link
```

## 🔮 Roadmap

**Q2 2026:**
- [ ] YouTube Transcript API integration
- [ ] Custom template builder
- [ ] Multi-language support (ES, FR, DE, JA)

**Q3 2026:**
- [ ] Direct social media posting
- [ ] Analytics dashboard
- [ ] A/B testing for hooks

**Q4 2026:**
- [ ] Team collaboration
- [ ] White-label options
- [ ] Enterprise API

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repo
2. Create feature branch
3. Make changes
4. Submit PR

## 📞 Support

- **Docs**: https://clawhub.ai/skills/ai-content-repurposer
- **Issues**: https://github.com/openclaw/ai-content-repurposer/issues
- **Email**: support@openclaw.ai

## 📄 License

MIT License - See [LICENSE](./LICENSE) file

---

**Built with ❤️ by OpenClaw** | Part of ClawHub Skills

## 📊 ROI Calculator

**Time Saved per Content Piece:**
- Manual repurposing: 2-3 hours
- With AI Content Repurposer: 5 minutes
- **Time saved: 95%**

**Monthly Value (at $50/hr):**
- 10 content pieces/month = 20-30 hours saved = **$1,000-1,500**
- 20 content pieces/month = 40-60 hours saved = **$2,000-3,000**
- 50 content pieces/month = 100-150 hours saved = **$5,000-7,500**

**Cost: $79/month**
**Net savings: $921-7,421/month** 🚀

---

**Ready to 10x your content output?**

```bash
clawhub install ai-content-repurposer
```
