# Doubao Podcast TTS Skill

[Agent Skills](https://agentskills.io) compatible skill for integrating ByteDance Doubao Podcast TTS API.

豆包（ByteDance）播客 TTS API 集成指南 — 兼容 Claude Code / Cursor / Codex 等支持 Agent Skills 规范的工具。

基于 7 篇微信长文 POC + 线上生产环境实战，涵盖 **11 条踩坑记录**。

## Quick Install

**Claude Code:**
```bash
# Clone to global skills directory
git clone https://github.com/mileszhang001-boom/doubao-podcast-skill.git ~/.claude/skills/doubao-podcast
```

**Other Agent Skills compatible tools:**
```bash
# Copy SKILL.md to your tool's skills directory
cp SKILL.md <your-skills-dir>/doubao-podcast/SKILL.md
```

## What's Inside

### 11 Production Pitfalls (踩坑记录)

| # | Pitfall | Impact |
|---|---------|--------|
| 1 | `input_url` vs `input_text` parameter placement | Silent failure, empty result |
| 2 | Waiting for SessionFinished after PodcastEnd | 5min podcast takes 15min |
| 3 | Insufficient timeout for long articles | Generation killed prematurely |
| 4 | Missing `ping_timeout=120` | WebSocket disconnects during generation |
| 5 | Discarding audio chunks on disconnect | Losing already-generated content |
| 6 | `audio_url` expires in 24 hours | CDN returns 403 after expiry |
| 7 | Python stdout buffering with nohup | No real-time logs |
| **8** | **Browser WebSocket can't set custom headers** | **Must use server-side proxy** |
| **9** | **`duration_sec` often returns 0** | **Need to estimate from audio size** |
| **10** | **RoundStart round 1 text is empty** | **Head music, real content from round 2** |
| **11** | **WeChat articles blocked on server IPs** | **Title extraction needs fallback** |

Pitfalls 8-11 (bold) are from production deployment, not found in initial POC.

### Code Examples

- **Python**: `scripts/generate_podcast.py` — Battle-tested batch generator (CLI + library)
- **Node.js**: Inline in SKILL.md — Production-verified binary frame codec + SSE proxy

### Architecture Patterns

- **Browser integration**: HTTP POST → Server SSE → Doubao WSS (bypasses header limitation)
- **Content caching**: URL deduplication + local mp3 storage (avoid 24h CDN expiry)
- **Title extraction**: Web scrape → Doubao round text fallback → default

### Performance Baseline

| Metric | Value |
|--------|-------|
| Generation speed | 2.7x realtime (1min podcast ≈ 22s) |
| First token | avg 6s |
| Audio format | MP3, 96kbps, 24kHz mono |
| Tested | 7 articles POC + multiple production runs |

## Use Cases

- Calling Doubao Podcast API to generate audio from articles
- Integrating podcast generation into browser-based apps
- Designing content storage and deduplication architecture
- Troubleshooting generation timeout, stuck, or empty audio issues
- Building podcast playback pipelines (streaming vs non-streaming)

## Requirements

**For podcast generation:**
- Doubao API credentials (4 headers: App-Id, Access-Key, Resource-Id, App-Key)
- Obtain from [Volcengine Console](https://console.volcengine.com/) → Speech Technology

**For Python script:**
- Python 3.8+
- `pip install websockets`

**For Node.js integration:**
- Node.js 18+
- `npm install ws`

## License

MIT
