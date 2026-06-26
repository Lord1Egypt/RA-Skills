---
name: free-novel-search
description: Search and discover free novel resources online. Use when users need to find: (1) Free novel reading websites, (2) Public domain literary works, (3) Open source book repositories, or (4) Legal free小说资源. This skill provides curated lists, search tools, and quality assessments for legitimate free novel platforms.
---

# Free Novel Search

## Overview

This skill helps discover and access free, legally available novel resources. It includes curated platform lists, search utilities, and guidance on identifying legitimate free novel sources.

**Scope:** Public domain works, open-licensed novels, and legitimate free-to-read platforms.

**Out of Scope:** Piracy sites, unauthorized copies, or copyrighted works offered without permission.

## Quick Start

For most requests, use the resources directly:

1. **Common platforms**: See [Free Novel Platforms](references/novel_platforms.md)
2. **Search utilities**: Run `scripts/search_novels.py --help`
3. **Chinese novels**: See [Chinese Novel Resources](references/chinese_novels.md)

## Search Scripts

### search_novels.py

Search free novel databases and aggregators.

```bash
# Basic search
python scripts/search_novels.py --query "fantasy novel"

# Search specific category
python scripts/search_novels.py --query "science fiction" --category scifi

# Search Project Gutenberg (public domain)
python scripts/search_novels.py --query "Jane Austen" --source gutenberg

# Export results to file
python scripts/search_novels.py --query "mystery" --output results.json
```

**Options:**
- `--query`: Search term
- `--source`: gutenberg, openlibrary, all (default: all)
- `--category`: fiction, scifi, fantasy, mystery, romance, nonfic
- `--limit`: Maximum results (default: 20)
- `--output`: Output file path (JSON)

## Common Free Novel Platforms

### International (English)

| Platform | Type | Content | URL |
|----------|------|---------|-----|
| Project Gutenberg | Public Domain | Classic literature | gutenberg.org |
| Open Library | Open Access | Modern + classics | openlibrary.org |
| ManyBooks | Public Domain | 50,000+ free eBooks | manybooks.net |
| Feedbooks | Mixed | Fiction & non-fiction | feedbooks.com |
| Wikisource | User-contributed | Public domain works | en.wikisource.org |
| LoCosmos | Open License | Science fiction | lcosmos.com |
| Royal Road | Original Fiction | Web novels | royalroad.com |
| Wattpad | User-generated | Modern fiction | wattpad.com |

### Chinese (中文小说)

| Platform | Type | Content | URL |
|----------|------|---------|-----|
| 书旗网 | Free Reading | Popular web novels | shuqi.com |
| 顶点中文 | Free Reading | Web novels | dingdian.cn |
| 笔趣阁 | Free Reading | Classic + Web novels | biquge.com.cn |
| 17K小说网 | Freemium | Various genres | 17k.com |
| 纵横中文网 | Free Reading | Web fiction | zongheng.com |

### Japanese (日本語)

| Platform | Type | Content | URL |
|----------|------|---------|-----|
| 青空文庫 | Public Domain | Classic Aozorabunko | aozora.gr.jp |
| 小説家になろう | Self-published | Web novels | syosetu.com |
| カクヨム | Free Reading | Various genres | kakuyomu.jp |
| ハーメルン | Fan fiction | Fan works | hameln.jp |

### Korean (한국어)

| Platform | Type | Content | URL |
|----------|------|---------|-----|
| 문피아 | Free Reading | Web novels | munpia.com |
|  카카오페이지 | Freemium | Various genres | page.kakao.com |
| 리디북스 | Freemium | Light novels | ridibooks.com |

## License Types

Understanding license types helps identify truly free resources:

- **Public Domain**: No copyright, free for all use (e.g., works from 1920s or earlier in most countries)
- **CC0 (Public Domain Dedication)**: Authors explicitly waive all rights
- **CC-BY / CC-BY-SA**: Attribution required, but free to read and share
- **CC-BY-NC**: Attribution required, non-commercial use only
- **Open Access**: Publisher-granted free access (may have terms)

## Finding Legal Free Novels

### Step 1: Identify Copyright Status

For modern works (post-1928), assume copyrighted unless verified otherwise.

**Safe to search:**
- Project Gutenberg (all public domain)
- Author's personal website offering free chapters
- Publisher's official free promotions

### Step 2: Check Platform Legitimacy

**Red flags for illegal sites:**
- No clearly stated content licensing
- Offers paywalled bestsellers for free
- Frequent DMCA takedown notices
- No author/publisher attribution

**Green flags for legitimate sites:**
- Clear DMCA/privacy policies
- Partnership with publishers
- Author accounts and verification
- Open about revenue model (ads, optional membership)

### Step 3: Alternative Free Sources

- **Library digital services**: OverDrive/Libby, Hoopla
- **Publisher free chapters**: Official promotional excerpts
- **Author blogs**: Personal websites with serialized fiction

## Resources

### references/
- [novel_platforms.md](references/novel_platforms.md) - Detailed platform database
- [chinese_novels.md](references/chinese_novels.md) - Chinese novel resources
- [japanese_novels.md](references/japanese_novels.md) - Japanese novel resources
- [license_guide.md](references/license_guide.md) - Copyright and licensing reference

### scripts/
- [search_novels.py](scripts/search_novels.py) - Multi-platform search tool
- [check_license.py](scripts/check_license.py) - Verify site licensing status

---

**Note:** This skill promotes legal access to literature. Always verify that platforms and works are properly licensed before recommending them.