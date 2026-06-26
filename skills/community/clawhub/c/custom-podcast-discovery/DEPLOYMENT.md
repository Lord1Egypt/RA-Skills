# Deployment Guide

## For End Users

### 1. Install from ClawHub (Once Published)

```bash
clawhub install podcast
```

### 2. Configure

```bash
cd ~/.openclaw/skills/podcast
cp config.example.yaml config.yaml
# Edit config.yaml with your settings
```

**Required settings:**
- Add RSS feed URLs to `sources`
- Set your interests in `interests`
- Configure ElevenLabs `voice_id`
- Choose storage: `s3` or `local`

**For S3:**
```yaml
storage:
  type: s3
  bucket: your-bucket-name
  region: us-east-1
```

Ensure AWS credentials are configured:
```bash
aws configure
```

**For local:**
```yaml
storage:
  type: local
  path: ./output
```

### 3. Test Discovery

```bash
cd ~/.openclaw/skills/podcast
python3 scripts/discover.py --config config.yaml --limit 5
```

### 4. Run Full Pipeline

**Manual mode** (pause after each stage):
```bash
python3 scripts/pipeline.py --config config.yaml --mode manual
```

**Auto mode** (run all stages):
```bash
python3 scripts/pipeline.py --config config.yaml --mode auto
```

**Specific topic:**
```bash
python3 scripts/pipeline.py --config config.yaml --topic "AI Reasoning" --mode manual
```

### 5. Cron Integration

Add to OpenClaw cron for daily discovery:

```yaml
schedule: "0 8 * * *"
label: "podcast-discovery"
payload: |
  cd ~/.openclaw/skills/podcast
  python3 scripts/discover.py --config config.yaml --limit 10 \
    --output data/discovery-$(date +%Y-%m-%d).json
```

## For OpenClaw Workers

When user asks to "generate a podcast", spawn a worker:

```bash
cd ~/.openclaw/skills/podcast
[ -f ~/.openclaw/env-init.sh ] && source ~/.openclaw/env-init.sh
python3 scripts/pipeline.py --config config.yaml --mode auto
```

**Worker needs:**
- `web_search()` tool for research stage
- LLM access for script generation
- `elevenlabs_text_to_speech` tool for audio generation

## For ClawHub Publishing

### 1. Prepare Repository

The skill is already in the correct structure:

```
skills/podcast/
├── SKILL.md              # Required: skill metadata
├── README.md             # Required: user docs
├── skill.json            # Required: manifest
├── config.example.yaml   # Required: config template
├── scripts/              # Scripts
├── sources/              # Source modules
├── templates/            # Prompt templates
└── .gitignore           # Git ignore
```

### 2. Publish to ClawHub

```bash
cd <path-to-podcast-skill>
clawhub publish
```

This will:
- Validate skill.json
- Check required files exist
- Create tarball
- Upload to ClawHub

### 3. Test Installation

On a fresh system:

```bash
clawhub search podcast
clawhub install podcast
cd ~/.openclaw/skills/podcast
cp config.example.yaml config.yaml
# Edit config
python3 scripts/discover.py --config config.yaml --limit 5
```

## Troubleshooting

### Discovery fails

**"No sources configured"**
→ Check config.yaml has `sources:` section with items

**"Failed to fetch RSS"**
→ Check RSS URL is valid with `curl <url>`

**"No topics discovered"**
→ Lower `min_points` for HN or adjust interests keywords

### Pipeline fails

**Research stage: "Worker should populate"**
→ Research script is a framework; OpenClaw worker must call `web_search()`

**Script stage: "Prompt created"**
→ Script script is a framework; worker must call LLM

**Audio stage: "Pending TTS generation"**
→ Audio script prepares text; worker must call `elevenlabs_text_to_speech`

**Upload stage: S3 403 error**
→ Check AWS credentials: `aws s3 ls s3://your-bucket`

### Verification fails

**"Citations not in research"**
→ Ensure research.json has `sources[]` populated
→ URLs in script must match research source URLs

**"Claims without nearby citations"**
→ Add `[Source: URL]` after each factual claim in script

## Environment Requirements

**Minimal (discovery only):**
- Python 3.7+
- No external packages

**Full pipeline:**
- Python 3.7+
- OpenClaw with ElevenLabs integration
- AWS CLI (for S3 upload)
- ElevenLabs API key

**Optional:**
- `aws` configured for S3
- WhatsApp integration for delivery

## Storage Configuration

### S3 Setup

1. Create bucket:
```bash
aws s3 mb s3://my-podcast-bucket --region us-east-1
```

2. Set bucket policy for public read:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::my-podcast-bucket/podcast/*"
    }
  ]
}
```

3. Update config.yaml:
```yaml
storage:
  type: s3
  bucket: my-podcast-bucket
  region: us-east-1
  prefix: podcast/
```

### Local Storage Setup

1. Create output directory:
```bash
mkdir -p ~/podcast-output
```

2. Update config.yaml:
```yaml
storage:
  type: local
  path: ~/podcast-output
```

## Adding Custom Sources

### 1. Create source class

Create `sources/my_source.py`:

```python
from .base import TopicSource

class MySource(TopicSource):
    def __init__(self, config):
        super().__init__(config)
        # Your config
    
    def fetch(self):
        # Fetch topics
        return [
            {
                "title": "Topic Title",
                "url": "https://...",
                "category": "Category",
                "source": self.name
            }
        ]
```

### 2. Register in loader

Edit `sources/__init__.py`:

```python
from .my_source import MySource

sources = {
    "rss": RSSSource,
    "hackernews": HackerNewsSource,
    "nature": NatureSource,
    "mysource": MySource,  # Add here
}
```

### 3. Use in config

```yaml
sources:
  - type: mysource
    name: My Custom Source
    # Your config fields
```

## Support

- GitHub Issues: [repo URL]
- ClawHub: `clawhub info podcast`
- OpenClaw Discord: [invite link]

## Version History

**1.0.0** (2026-03-06)
- Initial release
- Multi-source discovery (RSS, HN, Nature)
- Full pipeline with citation enforcement
- S3 and local storage support
- Resume from any stage
- Manual and auto modes
