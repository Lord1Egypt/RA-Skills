---
name: anime-character-loader
type: python-package
description: |
  Load anime character info from multiple sources and generate validated SOUL.generated.md files.
  Features: multi-source query, forced disambiguation, cross-source consistency scoring, 
  idempotent merge, semantic validation.
version: 2.4.2
author: Anchormind

commands:
  - name: load
    description: Load character with multi-source validation
    usage: load_character.py <character_name> [options]
    examples:
      - "load_character.py 'Kasumigaoka Utaha'"
      - "load_character.py '霞之丘诗羽' --anime 'Saekano'"
      - "load_character.py 'Sakurajima Mai' -o ./characters"

options:
  --anime, -a: Anime/manga name hint for disambiguation (REQUIRED for ambiguous names)
  --output, -o: Output directory (default: current)
  --info, -i: Show character info only
  --force, -f: Force generation even with low confidence
  --select, -s: Select specific match by index (when multiple found)

output:
  filename: SOUL.generated.md
  loading_options:
    - "[1] REPLACE - cp SOUL.generated.md SOUL.md"
    - "[2] MERGE - Idempotent merge into existing SOUL.md (no duplicates)"
    - "[3] KEEP - Manual review"

validation:
  score_threshold: 80
  required_sections:
    - Identity
    - Personality
    - Boundaries
  semantic_checks:
    - contains_name: Character name present
    - contains_source: Source work referenced
    - has_structure: All required sections present
    - content_length: Minimum 500 characters
    - no_placeholders: No TODO/FIXME/placeholder text
    - meaningful_background: Background has substance
    - specific_personality: Personality not generic
    - speaking_style_details: Speaking Style has bullets
    - name_consistency: Name variations consistent

data_sources:
  - name: AniList
    endpoint: https://graphql.anilist.co
    weight: 0.5
    auth: none
  - name: Jikan (MyAnimeList)
    endpoint: https://api.jikan.moe/v4
    weight: 0.3
    auth: none

exit_codes:
  0: Success
  10: Network error (API timeout, no internet)
  20: Data error (no matches, ambiguous name, low confidence)
  30: Validation error (quality checks failed)
  40: File error (write failure, permission denied)

features:
  - Multi-source parallel query with cross-source validation
  - Automatic failover and retry (3 attempts)
  - 24-hour response cache (SQLite)
  - Forced disambiguation (requires --anime for ambiguous names)
  - Cross-source consistency scoring (AniList + Jikan comparison)
  - Force manual selection when top matches are close (<0.15 gap)
  - Semantic validation with 9 checks
  - Idempotent merge (character+work deduplication)
  - Atomic write with rollback (no partial files)

confidence_levels:
  high: ">= 0.8"
  medium: "0.5-0.8"
  low: "< 0.5 (reject or --force)"

forced_disambiguation: |
  When multiple matches found OR single match with low confidence,
  --anime hint is REQUIRED. Prevents selecting wrong character.
  
  When top 2 matches have similar scores (gap < 0.15), 
  --select is REQUIRED. Prevents auto-selecting ambiguous match.

merge_behavior:
  idempotent: true
  duplicate_detection: "character_name + source_work"
  update_on_change: true
  atomic_write: true
---

# Anime Character Loader v2.3

## Structured Architecture (Skill + CLI)

This repository is organized as a skill + CLI hybrid:

- `load_character.py`: legacy-compatible CLI command (wrapper)
- `src/anime_character_loader/cli.py`: structured CLI entrypoint
- `src/anime_character_loader/legacy.py`: preserved legacy behavior implementation
- `src/anime_character_loader/{sources,disambiguation,generator,validator,storage}`: module boundaries for maintainability
- `tests/`: minimal regression coverage for compatibility-critical paths

## Overview

多源动漫角色数据加载器，生成经过验证的 SOUL.generated.md 人格文件。

**v2.3 关键改进**:
1. **幂等合并**: 同一角色多次合并不会重复
2. **跨源一致性评分**: AniList + Jikan 交叉验证
3. **强制选择**: 分数接近时强制用户选择
4. **标准化退出码**: 脚本可识别错误类型

## Key Improvements (v2.3)

### 1. 退出码系统
```bash
0   # 成功
10  # 网络错误
20  # 数据错误（无匹配、消歧失败）
30  # 验证失败
40  # 文件错误
```

### 2. 跨源一致性评分
```
Confidence = (AniList * 0.5 + Jikan * 0.3) + (Consistency * 0.2)

如果 top1 和 top2 差距 < 0.15:
    → 强制要求 --select 手动选择
```

### 3. 幂等合并
```bash
# 第一次合并
python load_character.py "Megumi" --anime "Saekano"
# 选择 MERGE → 添加角色

# 第二次合并（相同角色）
python load_character.py "Megumi" --anime "Saekano"  
# 选择 MERGE → 检测到重复，跳过

# 第三次合并（内容更新）
# 如果生成内容有变化 → 更新而非追加
```

### 4. 强制消歧增强
```bash
# ❌ 会失败 - Sakura 有多个角色
python load_character.py "Sakura"

# ❌ 即使指定作品，如果多个源返回相似结果
python load_character.py "Sakura" --anime "Fate"
# 可能仍要求 --select 如果 AniList 和 Jikan 结果不一致

# ✅ 必须手动选择
python load_character.py "Sakura" --anime "Fate" --select 1
```

## Usage Examples

### Basic Usage (Unique Names)
```bash
# 唯一名字可以直接生成
python load_character.py "Kasumigaoka Utaha"
python load_character.py "霞之丘诗羽"
```

### Disambiguation Required
```bash
# 同名角色必须指定作品
python load_character.py "Sakura" --anime "Fate"
python load_character.py "Rin" --anime "Fate"
python load_character.py "Miku" --anime "Quintessential"
```

### Manual Selection
```bash
# 列出所有匹配手动选择
python load_character.py "Sakura" --select 2
```

### Preview Mode
```bash
# 只查看信息不生成
python load_character.py "加藤惠" --info
```

## Workflow

```
1. 名称翻译 (中文→英文/日文)
        ↓
2. 多源并行查询 (AniList + Jikan)
        ↓
3. 跨源一致性评分
   - 计算名字相似度
   - 计算作品相似度
   - 综合置信度排序
        ↓
4. 强制消歧检查
   - 多匹配? → 需要 --anime
   - 分数接近? → 需要 --select
   - 低置信? → 需要 --anime
        ↓
5. 生成 SOUL.generated.md
        ↓
6. 语义验证 (9项检查)
        ↓
7. 提示加载选项 (REPLACE/MERGE/KEEP)
        ↓
8. 幂等合并（如选择 MERGE）
```

## Configuration

### 强制消歧开关
```python
# 在 load_character.py 顶部
FORCE_DISAMBIGUATION = True  # 设为 False 恢复宽松模式
```

### 强制选择阈值
```python
FORCE_SELECTION_THRESHOLD = 0.15  # 分数差距小于此值强制选择
```

### 置信度阈值
```python
CONFIDENCE_THRESHOLD_HIGH = 0.8    # 高置信度
CONFIDENCE_THRESHOLD_MEDIUM = 0.6  # 中等置信度
CONFIDENCE_THRESHOLD_LOW = 0.5     # 最低接受线
```

## Error Handling

| 场景 | 退出码 | 处理 |
|------|--------|------|
| API 失败 | 10 | 重试3次后退出 |
| 同名无提示 | 20 | 强制失败，提示用 `--anime` |
| 分数接近 | 20 | 强制失败，提示用 `--select` |
| 验证失败 | 30 | 回滚，可 `--force` 覆盖 |
| 文件写入失败 | 40 | 清理临时文件后退出 |

## Cache & Performance

- SQLite 缓存 (`~/.cache/anime-character-loader/`)
- 24小时过期
- 自动限流 (0.5s 间隔)
- 失败重试 (指数退避)

---

## 🔒 Privacy Notice

### Data Sent to External Services

When you query a character name, the following data may be sent to external APIs:

| Service | URL | Data Sent | Purpose |
|---------|-----|-----------|---------|
| AniList | `anilist.co` | Character name | Primary character lookup |
| Jikan | `jikan.moe` | Character name | MyAnimeList backup source |
| Fandom Wiki | `*.fandom.com` | Character name + Anime name | Quotes and descriptions |
| 萌娘百科 | `zh.moegirl.org.cn` | Character name | Chinese character database |
| yurippe API | `yurippe.vercel.app` | Character name | Anime quotes database |

### Privacy Protection

- No personal data is collected or transmitted
- Only character names and anime titles are sent to external services
- All external requests use HTTPS encryption
- Local caching minimizes repeated external calls

### Opt-Out Options

```bash
# Disable external quotes fetching (use local database only)
export DISABLE_EXTERNAL_QUOTES=1
python load_character.py "Character Name"
```

---

## ⚖️ Legal & Copyright Notice

### Quotes Database

The local quotes database (`data/quotes_database.json`) contains:
- **Fan-collected quotes** from anime/manga for educational/research purposes
- **Fair use doctrine**: Limited excerpts for character study and AI personality modeling
- All characters and works belong to their respective copyright holders

### Wiki Content

Descriptions and excerpts are sourced from:
- **Fandom Wiki** (CC-BY-SA license)
- **萌娘百科 Moegirlpedia** (CC BY-NC-SA 3.0)

### Usage Restrictions

- ✅ Personal use and research
- ✅ OpenClaw agent personality configuration
- ❌ Commercial redistribution of quotes database
- ❌ Creating competing content databases

### Copyright Holders

Characters referenced in this tool belong to their respective creators and publishers including but not limited to:
- Saekano: © Fumiaki Maruto, Kurehito Misaki, KADOKAWA
- Rascal Does Not Dream: © Hajime Kamoshida, Keiji Mizoguchi, KADOKAWA
- And other respective copyright holders

For DMCA or copyright concerns, please contact through GitHub Issues.

---

## 🛡️ File Safety Notice

⚠️ **Warning About File Operations**

- **REPLACE mode** will overwrite existing `SOUL.md` (automatic backup created at `SOUL.md.backup.YYYYMMDD_HHMMSS`)
- **MERGE mode** adds content without removing existing characters (idempotent - no duplicates)
- All write operations use atomic writes (temp file + rename)

**Recommendation**: Back up important `SOUL.md` files before using REPLACE mode.
