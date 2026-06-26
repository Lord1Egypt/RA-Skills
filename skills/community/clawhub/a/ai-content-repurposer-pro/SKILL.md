# AI Content Repurposer Skill

Transform long-form content into multiple formats instantly. Repurpose YouTube videos, blog posts, and podcasts into platform-optimized content.

## Description

**AI Content Repurposer** is a powerful content transformation tool that helps creators, marketers, and businesses maximize their content ROI by automatically converting long-form content into multiple platform-specific formats.

### Key Features

- 🎬 **YouTube → TikTok/Shorts/Reels**: Transform video transcripts into engaging short-form scripts with hooks, visual cues, and CTAs
- 📝 **Blog → Twitter Threads**: Convert articles into viral Twitter threads with proper formatting and engagement hooks
- 💼 **Blog → LinkedIn Posts**: Create professional LinkedIn posts with thought-leadership tone and engagement questions
- 🎙️ **Podcast → Transcripts**: Format raw transcripts with chapters, timestamps, and speaker labels
- 📊 **Podcast → Summaries**: Generate episode summaries, key takeaways, and shareable quote cards
- 🔄 **Batch Processing**: Process multiple content pieces at once with configurable output formats

## Installation

```bash
# Install via ClawHub (recommended)
clawhub install ai-content-repurposer

# Or install manually
npm install -g ai-content-repurposer
```

## Usage

### Basic Commands

```bash
# Convert YouTube video to TikTok script
ai-content-repurposer youtube-to-shorts transcript.txt -p tiktok -o output.json

# Convert blog post to Twitter thread
ai-content-repurposer blog-to-twitter https://example.com/blog-post -n 10 -o thread.json

# Convert blog to LinkedIn post
ai-content-repurposer blog-to-linkedin article.txt -t thought-leadership

# Format podcast transcript
ai-content-repurposer podcast-to-transcript episode.txt --speakers -o formatted.json

# Generate podcast summary and quotes
ai-content-repurposer podcast-to-summary episode.txt -o summary.json

# Batch process multiple content pieces
ai-content-repurposer batch config.json -o ./output

# Interactive mode
ai-content-repurposer interactive
```

### Command Options

#### `youtube-to-shorts`

```
Usage: ai-content-repurposer youtube-to-shorts [options] <transcript>

Arguments:
  transcript                 Path to transcript file or text

Options:
  -p, --platform <platform>  Target platform: tiktok, shorts, reels (default: "tiktok")
  -o, --output <file>        Output file path
  -h, --help                 Display help
```

#### `blog-to-twitter`

```
Usage: ai-content-repurposer blog-to-twitter [options] <url-or-file>

Arguments:
  url-or-file               Blog URL or file path

Options:
  -n, --tweets <number>     Number of tweets (default: "7")
  -o, --output <file>       Output file path
  -h, --help                Display help
```

#### `blog-to-linkedin`

```
Usage: ai-content-repurposer blog-to-linkedin [options] <url-or-file>

Arguments:
  url-or-file               Blog URL or file path

Options:
  -t, --tone <tone>         Tone: thought-leadership, educational, story (default: "thought-leadership")
  -o, --output <file>       Output file path
  -h, --help                Display help
```

#### `podcast-to-transcript`

```
Usage: ai-content-repurposer podcast-to-transcript [options] <transcript>

Arguments:
  transcript                Path to transcript file

Options:
  --no-timestamps           Disable timestamps
  --speakers                Add speaker labels
  -o, --output <file>       Output file path
  -h, --help                Display help
```

#### `podcast-to-summary`

```
Usage: ai-content-repurposer podcast-to-summary [options] <transcript>

Arguments:
  transcript                Path to transcript file

Options:
  -o, --output <file>       Output file path
  -h, --help                Display help
```

#### `batch`

```
Usage: ai-content-repurposer [options] <config>

Arguments:
  config                    Path to batch config JSON file

Options:
  -o, --output-dir <dir>    Output directory (default: "./output")
  -h, --help                Display help
```

## Configuration

### Environment Variables

```bash
# OpenAI API Key (required for AI-powered transformations)
export OPENAI_API_KEY=your_api_key_here

# Optional: Custom model
export AI_MODEL=gpt-4-turbo
```

### Batch Config Example

Create a `batch-config.json`:

```json
{
  "jobs": [
    {
      "name": "video-1-tiktok",
      "type": "youtube-to-shorts",
      "content": "Path to or text of transcript",
      "platform": "tiktok"
    },
    {
      "name": "blog-1-twitter",
      "type": "blog-to-twitter",
      "content": "Blog content text",
      "tweetCount": 8
    },
    {
      "name": "podcast-1-summary",
      "type": "podcast-to-summary",
      "content": "Path to transcript file"
    }
  ]
}
```

## Output Examples

### YouTube → TikTok Script

```json
{
  "title": "3 Secrets to Productivity",
  "hook": "Stop working harder. Start working smarter.",
  "body": [
    "Most people focus on time management. Wrong approach.",
    "Energy management is the real game-changer.",
    "Here's the framework that changed everything for me..."
  ],
  "cta": "Follow for more productivity hacks!",
  "hashtags": ["#productivity", "#lifehacks", "#success"],
  "visualCues": [
    "[Show clock spinning]",
    "[Cut to energy graph]",
    "[Text overlay: 'The Framework']"
  ]
}
```

### Blog → Twitter Thread

```json
{
  "threadTitle": "The Complete Guide to Content Repurposing",
  "tweets": [
    {
      "number": 1,
      "text": "🧵 Create once, publish everywhere. Here's how to turn 1 piece of content into 20+ assets (without burning out):"
    },
    {
      "number": 2,
      "text": "1/ Start with long-form content. A blog post, video, or podcast episode. This is your 'pillar' content."
    }
    // ... more tweets
  ],
  "hashtags": ["#contentmarketing", "#socialmedia"]
}
```

### Podcast Summary

```json
{
  "summary": "In this episode, we explore the future of AI and its impact on creative work with industry expert Jane Doe.",
  "takeaways": [
    "AI won't replace creators, but creators using AI will replace those who don't",
    "The best AI tools augment human creativity rather than automate it",
    "Building AI literacy is now as important as digital literacy"
  ],
  "quotes": [
    {
      "text": "AI is not the enemy of creativity. It's the amplifier.",
      "timestamp": "12:34",
      "speaker": "Jane Doe"
    }
  ],
  "socialPosts": [
    {
      "platform": "twitter",
      "content": "🎙️ New episode alert! We're diving deep into AI + creativity with @JaneDoe..."
    }
  ]
}
```

## API Integration

Use the converter directly in your Node.js applications:

```javascript
const ContentConverter = require('ai-content-repurposer');

const converter = new ContentConverter({
  apiKey: 'your-openai-api-key',
  model: 'gpt-4'
});

// YouTube to TikTok
const tiktokScript = await converter.youtubeToShortForm(transcript, 'tiktok');

// Blog to Twitter
const twitterThread = await converter.blogToTwitterThread(blogContent, 8);

// Podcast summary
const podcastSummary = await converter.podcastToSummary(transcript);
```

## Use Cases

### Content Creators
- Turn YouTube videos into TikTok, Reels, and Shorts scripts
- Create promotional social posts from podcast episodes
- Generate quote cards and highlight reels

### Marketing Teams
- Repurpose blog posts into social media campaigns
- Create LinkedIn thought-leadership content from whitepapers
- Generate Twitter threads from case studies

### Podcasters
- Auto-generate episode transcripts with chapters
- Create show notes and summaries
- Extract shareable quotes for social media

### Agencies
- Scale content production for multiple clients
- Maintain consistent brand voice across platforms
- Reduce content creation time by 80%

## Pricing

**$79/month** - Unlimited transformations

- ✅ All conversion types
- ✅ Batch processing
- ✅ API access
- ✅ Priority support
- ✅ Custom templates (coming soon)

## Requirements

- Node.js >= 18.0.0
- OpenAI API key (for AI-powered features)
- Internet connection

## Limitations

- YouTube transcript fetching requires manual input (API integration coming soon)
- AI transformations depend on OpenAI API availability
- Maximum input size: 10,000 characters per transformation

## Roadmap

- [ ] YouTube Transcript API integration
- [ ] Custom template support
- [ ] Multi-language support
- [ ] Direct social media posting
- [ ] Analytics and performance tracking
- [ ] Team collaboration features
- [ ] White-label options for agencies

## Support

- **Documentation**: https://clawhub.ai/skills/ai-content-repurposer
- **Issues**: https://github.com/openclaw/ai-content-repurposer/issues
- **Email**: support@openclaw.ai

## License

MIT License - See LICENSE file for details

---

**Created by OpenClaw** | Part of the ClawHub Skills Ecosystem
