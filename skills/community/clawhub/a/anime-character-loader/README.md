# Anime Character Loader

> **输入角色名，生成可用 SOUL.generated.md，避免同名误判。**

Built by [Anchormind AI](https://anchormind-ai.com) — screen-free AI learning companions that actually see your books.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**核心价值**: 解决 AniList/Jikan 同名角色混淆问题，通过强制消歧 + 语义验证，确保输出可直接用于 OpenClaw 角色扮演。

**适合谁用**:
- OpenClaw/AI Agent 用户想快速加载动漫角色
- 角色扮演社区需要标准化 SOUL.md
- 开发者想批量生成角色配置文件

**3分钟上手**: 安装 → 运行命令 → 获得角色文件。

---

## Features

- 🔍 **Multi-source query**: Parallel search across AniList GraphQL + Jikan (MyAnimeList) APIs
- 🎯 **Forced disambiguation**: Requires `--anime` hint for ambiguous names (prevents wrong character selection)
- ✅ **Semantic validation**: 9-check validation system (structure + content quality)
- 🔄 **Idempotent merge**: Chapter-level merge with deduplication (same character won't be added twice)
- 💾 **Smart caching**: 24-hour SQLite cache with automatic retry logic
- 🎭 **Wikiquote Fetcher**: 3-phase台词抓取 (API → Browser → Local)，带置信度评分与Speaker识别
- Actual output example:
<img src="https://github.com/user-attachments/assets/41d52fb6-e82e-4e95-86a5-3a167042d53c" width="600" alt="对话演示">


## Installation

### As OpenClaw Skill (Recommended)

```bash
# Install via ClawHub
clawhub install anime-character-loader

# Or install from local clone
clawhub install ./anime-character-loader
```

Then use in OpenClaw:
```
@your_bot load_character "Kasumigaoka Utaha"
```

### As Standalone CLI

```bash
# Clone the repository
git clone https://github.com/colinchen4/anime-character-loader.git
cd anime-character-loader

# Install dependencies
pip install requests

# Run directly
python3 load_character.py "Kasumigaoka Utaha"
```

## Project Structure (Skill + CLI)

This repository is now organized as a **skill + CLI hybrid project**:

```text
anime-character-loader/
├─ load_character.py                    # legacy-compatible CLI wrapper
├─ src/anime_character_loader/          # structured package entrypoint + modules
│  ├─ cli.py
│  ├─ legacy.py                         # preserved behavior implementation snapshot
│  ├─ errors.py / models.py
│  ├─ sources/ disambiguation/ generator/ validator/ storage/
├─ tests/                               # minimal regression tests
└─ SKILL.md                             # skill metadata and usage
```

## Quick Start

### Quick Start (Legacy Command Compatible)

Old command remains supported:

```bash
python3 load_character.py "Kasumigaoka Utaha"
```

### Basic Usage

```bash
# Generate SOUL.md for a single character
python load_character.py "Kasumigaoka Utaha"

# Chinese names supported
python load_character.py "霞之丘诗羽"

# Preview without generating
python load_character.py "加藤惠" --info
```

### Disambiguation Required

Common names like "Sakura" or "Rin" appear in multiple anime. The system **requires** an anime hint:

```bash
# ❌ Will fail - ambiguous name
python load_character.py "Sakura"

# ✅ Works - disambiguated
python load_character.py "Sakura" --anime "Fate"
python load_character.py "Sakura" --anime "Naruto"

# ✅ Or use --select to choose manually
python load_character.py "Sakura" --select 2
```

### Multi-character Merge (Idempotent)

Generate multiple characters into a single SOUL.md:

```bash
# Generate first character
python load_character.py "Katou Megumi" --anime "Saekano"
# Choose [2] MERGE

# Generate second character - will not duplicate if already exists
python load_character.py "Kasumigaoka Utaha" --anime "Saekano"
# Choose [2] MERGE - checks for duplicates before merging
```

**MERGE mode features**:
- Detects duplicates by character name + source work
- Updates existing character if content changed
- Atomic write (no partial/corrupted files)

### Loading Options

After generation, choose how to load the character:

| Mode | Description |
|------|-------------|
| **REPLACE** | Replace existing SOUL.md |
| **MERGE** | Merge into existing SOUL.md (idempotent) |
| **KEEP** | Keep as SOUL.generated.md for manual review |

## How It Works

```
Query → Disambiguation → Generation → Validation → Output
   ↓         ↓              ↓            ↓          ↓
AniList   Cross-source   SOUL.md     9 checks   SOUL.generated.md
+ Jikan   consistency    creation    scoring    + loading options
```

### Cross-Source Consistency Scoring

When both AniList and Jikan return results:
- Name similarity is calculated
- Work title similarity is calculated
- Combined confidence = weighted average + consistency bonus

When top 2 matches have similar scores (gap < 0.15), manual selection is forced.

### Validation Checks

| Check | Type | Description |
|-------|------|-------------|
| contains_name | Basic | Character name present in output |
| contains_source | Basic | Source anime referenced |
| has_structure | Basic | Required sections (Identity/Personality/Boundaries) |
| content_length | Basic | Minimum 500 characters |
| no_placeholders | Basic | No TODO/FIXME/generic text |
| meaningful_background | Semantic | Background section has substance |
| specific_personality | Semantic | Personality traits are specific, not generic |
| speaking_style_details | Semantic | Speaking Style has concrete details |
| name_consistency | Semantic | Name variations are consistent |

**Pass threshold**: No errors + score ≥ 80/100

## Exit Codes

Scripts can check exit codes for specific error types:

| Code | Meaning | Example |
|------|---------|---------|
| 0 | Success | Character generated successfully |
| 10 | Network error | API timeout, no internet |
| 20 | Data error | No matches found, ambiguous name, low confidence |
| 30 | Validation error | Generated content failed quality checks |
| 40 | File error | Write failure, permission denied |

```bash
python load_character.py "Sakura"
if [ $? -eq 20 ]; then
    echo "Need to specify --anime for disambiguation"
fi
```

## Output Format

### Single Character
```markdown
# Character Name

**Source:** Anime Title

## Identity
You are Character Name from Anime Title...

## Personality
- Trait 1
- Trait 2

## Speaking Style
- Style cue 1
- Style cue 2

## Boundaries
- Stay in character as...

---
*Generated by anime-character-loader*
```

### Multi-character (after MERGE)
```markdown
# Multi-Character SOUL

## Character A
[Identity, Personality, Speaking Style, Boundaries]
*Hash: abc123*

## Character B
[Identity, Personality, Speaking Style, Boundaries]
*Hash: def456*

## Character Selection Guide
- Choose Character A when...
- Choose Character B when...
```

## Configuration

### Confidence Thresholds

Edit `load_character.py`:

```python
CONFIDENCE_THRESHOLD_HIGH = 0.8    # High confidence threshold
CONFIDENCE_THRESHOLD_MEDIUM = 0.6  # Medium confidence threshold  
CONFIDENCE_THRESHOLD_LOW = 0.5     # Minimum acceptable
FORCE_SELECTION_THRESHOLD = 0.15   # Gap below this forces manual selection
```

### Cache Settings

```python
CACHE_DURATION = timedelta(hours=24)  # Cache expiration
MAX_RETRIES = 3                       # API retry attempts
```

## API Sources & Wikiquote

| Source | Weight | Endpoint | Auth |
|--------|--------|----------|------|
| AniList | 50% | https://graphql.anilist.co | None |
| Jikan | 30% | https://api.jikan.moe/v4 | None |
| Wikiquote | Fallback | MediaWiki API (zh.moegirl.org.cn) | None |

### Wikiquote / Fandom Hybrid Integration
Three-phase quote fetching with confidence scoring:
- **Phase 1 (API)**: MediaWiki API (`action=parse`) for structured data
- **Phase 2 (Browser)**: Camofox fallback for Cloudflare bypass
- **Phase 3 (Local)**: `data/quotes_database.json` as seed corpus

**Features**:
- Speaker extraction: `Character: quote`, `(Character) quote`, `[Character] quote`
- Confidence scoring (0-1): section match + speaker match + text quality
- Deduplication: MD5-based `quote_id`

### Smart Excerpt Generator (辅助/兜底)
当 Wiki 没有专门的 Quotes 区块时，提取角色描述作为补充素材：
- **Source**: Fandom (英文) + 萌娘百科 (中文)
- **Content**: Biography, Personality, Background 等章节摘录
- **⚠️ Important**: 这是"角色描述摘录"，**不是原始台词**
- **Usage**: 作为 `wikiquote` 的兜底/补充，提供角色背景上下文

**Example**:
```python
from anime_character_loader.extractors.smart_excerpt_generator import generate_smart_excerpts

result = generate_smart_excerpts('泽村·斯潘塞·英梨梨', '路人女主')
# result['excerpts'][0]['text'] = "因为小学时被霸凌过，在外都会戴上大小姐的假面具..."
# result['excerpts'][0]['note'] = "⚠️ 来自Wiki角色描述，不是原始台词"
```
- Source tracing: `source_type` (api/browser/local/cache) + `source_url`

**Note**: "MediaWiki API抓取 + Playwright精准提取 + 本地语料兜底, 不保证所有页面结构一致".

**Example**:
```python
from anime_character_loader.extractors.fandom_hybrid import fetch_quotes_fandom

result = fetch_quotes_fandom('Eriri Spencer Sawamura', 'Saekano')
# result['source_type'] = 'local'  # when API/Browser fail
# result['quotes'][0] = {
#   'text': 'Baka! Chigau!',
#   'speaker': 'unknown',
#   'confidence': 0.8,
#   'quote_id': 'abc123',
#   'section': ''
# }
```

## Verified Scenarios

| Scenario | Status | Notes |
|----------|--------|-------|
| Japanese names (加藤恵) | ✅ Pass | AniList preferred |
| English names (Megumi Katou) | ✅ Pass | Jikan fallback |
| Mixed names (霞ヶ丘詩羽) | ✅ Pass | Unicode handling |
| Multi-character merge | ✅ Pass | Idempotent (3x merge = no duplicates) |
| Force disambiguation | ✅ Pass | "Sakura" + --anime "Fate" correctly identified |
| Cross-source validation | ✅ Pass | AniList + Jikan consistency check |

## Known Limitations

| Limitation | Workaround |
|------------|------------|
| Requires network | Cannot work offline |
| New anime delay | Latest characters may not be in databases |
| Niche characters | Use `--anime` to improve match rate |
| No Chinese API | Query uses Japanese/English names |

## Requirements

- Python 3.10+
- requests library
- Internet connection

## About

This tool is part of the [Anchormind](https://anchormind-ai.com) ecosystem.  
We build **AI-native learning hardware** — from character-driven study companions to interactive knowledge tools.

For product updates and enterprise solutions: [anchormind-ai.com](https://anchormind-ai.com)

## License

MIT License

## Changelog

### v2.3 (2026-03-02)
- **Idempotent merge**: Same character won't be added twice
- **Cross-source scoring**: AniList + Jikan consistency validation
- **Exit codes**: Standardized error codes for script integration
- **Force selection**: Manual selection required when top matches are close

### v2.1
- Forced disambiguation mode
- Semantic validation (9 checks)

### v2.0
- Multi-source query
- Atomic write with rollback

---
