# Podcast Discovery & Generation Skill

Automated podcast topic discovery, research, script generation, fact-checking, and audio production using AI. Clean, configurable, open-source pipeline built for OpenClaw.

## Features

- 🔍 **Multi-Source Discovery**: Fetch topics from RSS feeds, Hacker News, Nature, and more
- 🧠 **Smart Ranking**: Prioritize topics by your interests using keyword matching
- 📚 **Deep Research**: Structure for web research with source verification
- ✍️ **Script Generation**: LLM-powered script writing with citation enforcement
- ✅ **Fact Verification**: Cross-reference claims against research sources
- 🎙️ **Audio Production**: ElevenLabs TTS with citation stripping
- ☁️ **Flexible Storage**: S3 or local file storage
- 📦 **Delivery-ready**: Designed to plug into your own delivery channel (WhatsApp/SMS/email) via a worker

## Quick Start

### 1. Install

```bash
# Install via ClawHub (recommended)
clawhub install podcast

# Or manual install
cd ~/.openclaw/skills/
git clone <repo-url> podcast
cd podcast
```

### 2. Configure

```bash
cp config.example.yaml config.yaml
# Edit config.yaml with your settings
```

**Required config:**
- `sources`: List of RSS feeds and built-in sources
- `interests`: Your topic preferences (keywords)
- `voice.voice_id`: Your ElevenLabs voice ID
- `storage.type`: `s3` or `local`

**For S3 storage:**
- `storage.bucket`: S3 bucket name
- `storage.region`: AWS region
- Ensure AWS credentials are configured (`aws configure`)

### 3. Discover Topics

```bash
python3 scripts/discover.py --config config.yaml --limit 10 --output discovery.json
```

This scans all configured sources and outputs a ranked list of topics.

### 4. Run Full Pipeline (Manual Mode)

```bash
python3 scripts/pipeline.py --config config.yaml --mode manual
```

Or specify a topic directly:

```bash
python3 scripts/pipeline.py --config config.yaml --topic "AI Reasoning Models" --mode manual
```

**Manual mode** pauses after each stage so you can review/edit before proceeding.

**Auto mode** runs all stages without pausing:

```bash
python3 scripts/pipeline.py --config config.yaml --mode auto
```

## Pipeline Stages

1. **Discovery** (`discover.py`): Fetch and rank topics from sources
2. **Research** (`research.py`): Web search framework (requires OpenClaw worker)
3. **Script** (`generate-script.py`): Generate podcast script with citations
4. **Verify** (`verify.py`): Cross-check facts against research
5. **Audio** (`generate-audio.py`): Strip citations and prepare for TTS
6. **Upload** (`upload.py`): Upload to S3 or local storage

Each script can run standalone or as part of the pipeline.

## Configuration

### Sources

Add any RSS feed:

```yaml
sources:
  - type: rss
    url: https://example.com/feed.rss
    name: Example Feed
    category: Tech
```

Built-in sources:
- `hackernews`: Hacker News API (filter by points/comments)
- `nature`: Nature journal (sections: news, research, biotech, medicine)

### Voice

Use your own ElevenLabs voice ID or voice name:

```yaml
voice:
  # Use YOUR voice_id (recommended)
  voice_id: "<your-voice-id>"
  # Or use a voice name from your ElevenLabs library:
  # voice_name: "Jessica"
  model: eleven_turbo_v2_5
```

Get voice IDs: `elevenlabs_search_voices`

### Storage

**S3:**
```yaml
storage:
  type: s3
  bucket: my-bucket
  region: us-east-1
  prefix: podcast/
```

**Local:**
```yaml
storage:
  type: local
  path: ./output
```

### Script Settings

```yaml
script:
  word_count: 2500-3500  # Target length
  style: conversational   # conversational | formal | casual
  fact_check: true        # Verify claims
```

## Usage Examples

### Discover topics only
```bash
python3 scripts/discover.py --config config.yaml --limit 5
```

### Research a specific topic
```bash
python3 scripts/research.py "AI Reasoning Models" --output research.json
```

### Generate script from research
```bash
python3 scripts/generate-script.py \
  --research research.json \
  --output script.txt \
  --config config.yaml
```

### Verify script facts
```bash
python3 scripts/verify.py \
  --script script.txt \
  --research research.json \
  --output verification.json
```

### Generate audio (requires ElevenLabs)
```bash
python3 scripts/generate-audio.py \
  --script script.txt \
  --output episode.mp3 \
  --config config.yaml
```

### Upload to storage
```bash
python3 scripts/upload.py \
  --file episode.mp3 \
  --config config.yaml \
  --title "Episode Title"
```

## Architecture

### Source System
Pluggable architecture for topic sources. Easy to add new sources:

1. Create class inheriting from `TopicSource`
2. Implement `fetch()` method
3. Register in `sources/__init__.py`

See `sources/rss.py` and `sources/hacker_news.py` for examples.

### Citation Enforcement
Scripts must include `[Source: URL]` citations. The verify script:
- Extracts all citations from script
- Checks against research sources
- Flags unverified claims
- Blocks audio generation if verification fails

### TTS Preparation
Audio generation strips all citation markers:
- `[Source: URL]` citations
- Structural markers (`[VERIFIED]`, `[SECTION N]`)
- Markdown formatting
- Results in clean narration text

## Integration with OpenClaw

This skill is designed to work with OpenClaw workers:

**Research stage**: Requires `web_search()` tool access
**Script generation**: Requires LLM access (Claude Sonnet recommended)
**Audio generation**: Requires `elevenlabs_text_to_speech` tool

Workers should:
1. Source environment setup if needed (e.g., `~/.openclaw/env-init.sh` if available)
2. Have necessary tool access (web_search, elevenlabs, etc.)
3. Pass results back to main agent for delivery

## Cron Integration

Run discovery daily:

```bash
# cron payload
cd ~/.openclaw/skills/podcast && \
python3 scripts/discover.py --config config.yaml --limit 10 \
--output data/discovery-$(date +%Y-%m-%d).json
```

Or full pipeline (auto mode):

```bash
python3 scripts/pipeline.py --config config.yaml --mode auto
```

## Dependencies

**Core (included):**
- Python 3.7+
- Standard library only (no pip packages required for discovery)

**Optional (for full pipeline):**
- `aws` CLI (for S3 upload)
- OpenClaw with ElevenLabs integration
- ElevenLabs API key

**Not required:**
- No pyyaml (uses simple regex parser)
- No feedparser (uses regex for RSS)
- No requests (uses urllib)

Zero external dependencies by design.

## File Structure

```
podcast/
├── SKILL.md              # Skill metadata and triggers
├── README.md             # This file
├── config.example.yaml   # Configuration template
├── scripts/
│   ├── discover.py       # Topic discovery
│   ├── research.py       # Research framework
│   ├── generate-script.py # Script generation
│   ├── verify.py         # Fact verification
│   ├── generate-audio.py # TTS preparation
│   ├── upload.py         # Storage upload
│   └── pipeline.py       # Full orchestrator
├── sources/
│   ├── base.py           # Base source class
│   ├── rss.py            # Generic RSS source
│   ├── hacker_news.py    # HN API source
│   └── nature.py         # Nature journal source
├── templates/
│   ├── script-prompt.md  # Script generation template
│   └── discovery-prompt.md # Topic ranking template
├── data/
│   └── history.json      # Topic history (auto-created)
└── output/               # Generated files (auto-created)
```

## Troubleshooting

**No topics discovered?**
- Check RSS feed URLs are valid
- Verify interests keywords match source content
- Try lowering `min_points` for Hacker News

**Verification fails?**
- Check research.json has populated `sources[]` array
- Ensure script has `[Source: URL]` after each claim
- URLs in citations must match research sources

**S3 upload fails?**
- Verify AWS credentials: `aws s3 ls s3://your-bucket`
- Check bucket exists and is in correct region
- Ensure bucket policy allows public read on `podcast/*`

**Audio generation fails?**
- Verify ElevenLabs API key is configured
- Check voice ID is valid: `elevenlabs_search_voices`
- Ensure sufficient ElevenLabs credits

## Contributing

This is an open-source skill for OpenClaw. Contributions welcome:

- Add new source types (Reddit, Twitter, etc.)
- Improve ranking algorithm
- Add delivery methods (email, Telegram, etc.)
- Enhance verification logic

## License

MIT

## Credits

Built for OpenClaw by the community. Battle-tested pipeline patterns with zero vendor lock-in.
