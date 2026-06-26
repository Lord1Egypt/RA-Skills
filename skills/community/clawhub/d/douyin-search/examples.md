# Douyin Scraper — Examples

## Example 1: Basic natural language search

**User:** 搜索一下海鲜视频

**Agent:**
1. Extracts keyword: `海鲜视频`
2. Runs: `python3 scripts/douyin_search.py "海鲜视频" --count 10 --json`
3. Presents formatted results

**Output:**
```
🔍 搜索 "海鲜视频" — 共 10 个结果

1. **小明的海鲜日记** — 今天赶海抓到超大海蟹！
   ❤️ 12.3万  💬 856  ▶️ 89.2万
   🔗 https://www.douyin.com/video/7xxx
```

## Example 2: Search with login required

**User:** 帮我找抖音上的编程教程

**Agent:**
1. Runs search script
2. Gets `login_required` status
3. Falls back to suggestion API
4. Presents related keywords + login prompt

**Output:**
```
还没登录抖音，无法直接搜视频。找到以下相关搜索词：
- 编程教程
- Python编程教程
- 编程入门教程
- 零基础学编程

登录后即可搜索完整结果。需要我帮你登录吗？
```

## Example 3: English keyword search

**User:** douyin search for funny cats

**Agent:**
1. Extracts keyword: `funny cats`
2. URL-encodes and searches
3. Returns results (Douyin may return Chinese results for English keywords)

## Example 4: Ambiguous keyword

**User:** 抖音搜苹果

**Agent:**
1. Keyword "苹果" is ambiguous (fruit vs Apple Inc)
2. Uses suggestion API to clarify: "苹果手机", "苹果测评", "苹果吃法"
3. Asks user which they mean, or searches "苹果" directly