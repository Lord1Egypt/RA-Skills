---
name: podcast
version: 1.0.1
description: |
  Discover, research, script, fact-check, and generate podcast episodes automatically.
  Multi-source topic discovery, LLM script generation, citation enforcement, ElevenLabs TTS.
  Zero vendor lock-in - works with any RSS feed, S3 or local storage.
---

# Podcast Discovery & Generation

Automated end-to-end podcast production pipeline. Discovers trending topics from configurable sources, researches them deeply, generates fact-checked scripts with citations, and produces audio via ElevenLabs TTS.

## Triggers

Use this skill when user asks to:
- "Generate a podcast"
- "Make a podcast episode"
- "Discover podcast topics"
- "Create an audio episode about X"
- "Find topics for podcast"
- "Research and script a podcast"
- "Produce a podcast episode"

## Quick Start

### 1. Configure
```bash
cd ~/.openclaw/skills/podcast
cp config.example.yaml config.yaml
# Edit config.yaml: add sources, interests, voice, storage
```

### 2. Discover Topics
```bash
python3 scripts/discover.py --config config.yaml --limit 10
```

### 3. Run Pipeline
```bash
python3 scripts/pipeline.py --config config.yaml --topic "Your Topic" --mode manual
```

## Configuration

**Minimal config.yaml:**
```yaml
sources:
  - type: rss
    url: https://aeon.co/feed.rss
    name: Aeon
  - type: hackernews
    min_points: 200

interests:
  - AI/Tech
  - Science

voice:
  voice_id: "<your-voice-id>"

storage:
  type: local
  path: ./output
```

**Storage options:**
- `type: s3` — Upload to S3 (requires bucket, region)
- `type: local` — Save to local directory

## Pipeline Stages

1. **Discovery** — Fetch and rank topics from sources
2. **Research** — Web search framework (OpenClaw worker populates)
3. **Script** — Generate script with LLM, enforce `[Source: URL]` citations
4. **Verify** — Cross-check claims against research sources
5. **Audio** — Strip citations, call ElevenLabs TTS
6. **Upload** — Save to S3 or local storage

Each stage can run standalone or as full pipeline.

## Usage Examples

**Discover only:**
```bash
python3 scripts/discover.py --config config.yaml --limit 5 --output topics.json
```

**Full pipeline (auto mode):**
```bash
python3 scripts/pipeline.py --config config.yaml --mode auto
```

**Specific topic:**
```bash
python3 scripts/pipeline.py --config config.yaml --topic "AI Reasoning" --mode manual
```

**Resume from stage:**
```bash
python3 scripts/pipeline.py --config config.yaml --resume-from audio
```

## Source Types

**Built-in:**
- `rss` — Generic RSS/Atom feed (any URL)
- `hackernews` — HN API with point/comment filters
- `nature` — Nature journal (sections: news, research, biotech, medicine)

**Add custom RSS:**
```yaml
sources:
  - type: rss
    url: https://yourfeed.com/rss
    name: Your Source
    category: Your Category
```

## Output Files

```
output/
├── discovery-YYYY-MM-DD.json      # Ranked topics
├── research-YYYY-MM-DD-slug.json  # Research data
├── script-YYYY-MM-DD-slug.txt     # Script with citations
├── verification-YYYY-MM-DD.json   # Fact-check report
├── tts-ready-YYYY-MM-DD-slug.txt  # Clean text for TTS
├── episode-YYYY-MM-DD-slug.mp3    # Final audio
└── pipeline-state-YYYY-MM-DD.json # Pipeline state
```

## Integration with OpenClaw

**For discovery:** Run directly (no tools needed)

**For full pipeline:** Spawn OpenClaw worker with:
- `web_search()` — Research stage
- LLM access — Script generation (Claude Sonnet recommended)
- `elevenlabs_text_to_speech` — Audio generation

**Worker pattern:**
```bash
cd ~/.openclaw/skills/podcast
# Source environment if available
[ -f ~/.openclaw/env-init.sh ] && source ~/.openclaw/env-init.sh
python3 scripts/pipeline.py --config config.yaml --mode auto
```

## Citation Enforcement

Every factual claim in scripts MUST have `[Source: URL]` citation:

✅ **Correct:**
```
The market grew to $10.2 billion in 2025 [Source: https://example.com/report].
```

❌ **Incorrect:**
```
The market grew significantly.
```

The verify script cross-references citations against research sources and blocks audio generation if unverified claims are found.

## Cron Integration

**Daily discovery (8 AM):**
```yaml
schedule: "0 8 * * *"
payload: |
  cd ~/.openclaw/skills/podcast
  python3 scripts/discover.py --config config.yaml --limit 10 \
    --output data/discovery-$(date +%Y-%m-%d).json
```

**Weekly full pipeline:**
```yaml
schedule: "0 9 * * 1"
payload: |
  cd ~/.openclaw/skills/podcast
  [ -f ~/.openclaw/env-init.sh ] && source ~/.openclaw/env-init.sh
  python3 scripts/pipeline.py --config config.yaml --mode auto
```

## Key Features

✅ **Zero vendor lock-in** — Use any RSS feed, any storage
✅ **No external dependencies** — Pure Python stdlib (except ElevenLabs for TTS)
✅ **Citation enforcement** — Every claim must have source
✅ **Fact verification** — Cross-check against research
✅ **Pluggable sources** — Easy to add new topic sources
✅ **Resume support** — Restart from any stage
✅ **Manual or auto** — Review each stage or run end-to-end

## Troubleshooting

**No topics found:**
- Check RSS URLs are valid
- Verify interests match source content
- Lower `min_points` for Hacker News

**Verification fails:**
- Ensure research.json has sources
- Check script has `[Source: URL]` after claims
- URLs must match research sources

**S3 upload fails:**
- Verify AWS credentials
- Check bucket exists and region matches
- Ensure bucket policy allows public read

## Files

- `SKILL.md` — This file
- `README.md` — Detailed documentation
- `config.example.yaml` — Configuration template
- `scripts/` — Pipeline scripts
- `sources/` — Source implementations
- `templates/` — Prompt templates

## License

MIT — Open source, community-maintained OpenClaw skill
