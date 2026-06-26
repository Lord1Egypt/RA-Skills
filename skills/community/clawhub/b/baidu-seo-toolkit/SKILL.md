---
name: baidu-seo-toolkit
description: >
  SEO optimization toolkit for Chinese search engines: Baidu, Sogou, 
  360 Search. Includes keyword research, competitor analysis, and 
  Baidu-specific ranking factor optimization.
  Triggers: "百度SEO", "baidu seo", "中文搜索优化", "SEO工具".
version: 1.0.0
tags:
  - latest
  - seo
  - chinese-platform
  - marketing
---

# Baidu SEO Toolkit

SEO optimization toolkit for Chinese search engines. Optimizes for Baidu, Sogou, and 360 Search with platform-specific ranking factors.

## Baidu vs Google Key Differences

| Factor | Baidu | Google |
|--------|-------|--------|
| Domain Age | Very important | Less important |
| ICP Filing | Required for local ranking | N/A |
| Baidu Spider | `Baiduspider` | `Googlebot` |
| Mobile-first | Critical | Critical |
| Content Freshness | Very important | Important |
| Backlinks | Quality > Quantity | Quality > Quantity |

## Usage

### Keyword Research

```python
def baidu_keyword_research(keyword):
    """Research keywords for Baidu SEO"""
    suggestions = []
    
    # Baidu Index (index.baidu.com equivalent)
    suggestions.append(get_baidu_index(keyword))
    
    # Baidu auto-suggest
    suggestions.append(get_baidu_suggest(keyword))
    
    # Competitor keywords
    competitors = get_top_ranking_pages(keyword, "baidu")
    for page in competitors[:5]:
        suggestions.extend(extract_keywords_from_page(page))
    
    return deduplicate(suggestions)
```

### Baidu-Specific Optimization

```python
def optimize_for_baidu(page_content):
    """Apply Baidu-specific optimizations"""
    checks = []
    
    # 1. ICP filing notice (required for .cn domains)
    if has_cn_domain():
        checks.append("⚠️ Add ICP备案号 in footer")
    
    # 2. Baidu Zhidao backlinks (Baidu's Q&A platform)
    checks.append("💡 Create Baidu Zhidao answers with link")
    
    # 3. Baidu Submit sitemap
    checks.append("✅ Submit to Baidu Webmaster Tools")
    
    # 4. Mobile optimization (critical for Baidu)
    if not is_mobile_friendly():
        checks.append("❌ Mobile optimization required for Baidu")
    
    # 5. Chinese lang tag
    if not has_zh_cn_tag():
        checks.append("❌ Add <html lang='zh-cmn-Hans'>")
    
    return checks
```

### Competitor Analysis

```python
def analyze_baidu_competitors(target_keyword):
    """Analyze why competitors rank on Baidu"""
    results = []
    pages = get_top_10_baidu_results(target_keyword)
    
    for page in pages:
        analysis = {
            "url": page.url,
            "title_length": len(page.title),  # Baidu: 28-30 chars optimal
            "meta_description": len(page.meta),  # Baidu: ~80 chars
            "has_https": page.url.startswith("https"),
            "has_schema": page.has_structured_data,
            "domain_age": get_domain_age(page.domain),
            "backlinks": estimate_backlinks(page.url),
            "content_length": estimate_word_count(page),
        }
        results.append(analysis)
    
    return results
```

## Baidu Webmaster Tools

Submit sitemap: `https://ziyuan.baidu.com/linksubmit`

## Tags

`baidu` `seo` `chinese-seo` `search-engine` `keyword-research` `优化`
