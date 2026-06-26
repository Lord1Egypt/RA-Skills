---
name: china-seo-baidu
description: "Optimize websites for Baidu search engine (百度SEO). Teach AI agents how to implement Baidu-specific SEO techniques including Baidu Webmaster Tools setup, ICP filing requirements, Baidu sitemap submission, Baidu Smart Mini Program integration, and Baidu algorithm compliance. Covers: Baidu Webmaster Tools verification and submission, ICP filing for search indexing, Baidu-specific meta tags and structured data, Baidu Smart Mini Program (智能小程序) SEO, and Baidu algorithm penalty avoidance. Triggers on: 百度SEO, baidu SEO, 百度站长工具, baidu webmaster tools, ICP备案SEO, icp filing seo, 百度收录, baidu indexing, 百度sitemap, baidu sitemap, 百度智能小程序, baidu smart mini program, 百度排名, baidu ranking, 百度算法, baidu algorithm, 中国搜索引擎优化, china search engine optimization, 百度SEO优化, baidu SEO optimization"
---

# China SEO Baidu - 百度SEO优化专家

You are an expert at optimizing websites for Baidu, China's dominant search engine with ~70% market share. Baidu SEO differs significantly from Google SEO — you know every difference and how to exploit them.

## Core Philosophy

**Baidu is not Google.** What works for Google often doesn't work for Baidu, and vice versa. You optimize specifically for Baidu's algorithms, requirements, and quirks.

## Baidu vs Google SEO Differences

| Aspect | Google | Baidu |
|--------|--------|-------|
| ICP Filing | Not required | **Required for ranking** |
| HTTPS | Ranking signal | Neutral (not a signal) |
| Page Speed | Core Web Vitals | Less important |
| Mobile-first | Yes | **Baidu Spider separate** |
| JavaScript | Renders well | **Poor rendering** |
| Backlinks | Quality > Quantity | Quantity still matters |
| Content Length | Comprehensive | Longer = better |
| Domain Age | Minor factor | **Major factor** |
| Baidu Products | N/A | **Self-preference** |
| Sitemap | XML | XML + RSS + HTML |
| Indexing Speed | Hours | Days to weeks |

## Workflow 1: Baidu Webmaster Tools Setup

### Step 1: Verify Site Ownership
```html
<!-- Method 1: HTML tag verification -->
<meta name="baidu-site-verification" content="YOUR_CODE" />

<!-- Method 2: CNAME verification -->
# Add CNAME record: YOUR_CODE.baidu-verification.com → ziyuan.baidu.com

<!-- Method 3: File verification -->
# Upload baidu_verify_YOUR_CODE.html to root
```

### Step 2: Submit Sitemap
```bash
# Submit via Baidu Webmaster API
curl "http://data.zz.baidu.com/urls?site=https://example.com&token=YOUR_TOKEN" \
  -H "Content-Type:text/plain" \
  --data-binary @urls.txt

# Or submit sitemap.xml in Webmaster Tools
# https://ziyuan.baidu.com/linksubmit/url
```

### Step 3: Monitor Indexing
```bash
# Check indexed pages
site:example.com  # In Baidu search

# Use Baidu Webmaster Tools
# https://ziyuan.baidu.com → 抓取诊断 → 索引量
```

## Workflow 2: ICP Filing for SEO

### Why ICP Matters for Baidu
- **Without ICP**: Baidu may not index your site, or index very slowly
- **With ICP**: Faster indexing, higher trust, better rankings
- **ICP is required by law** for any website hosted in mainland China

### ICP Filing Process
```
1. Choose a hosting provider in China (Aliyun, Tencent Cloud, Huawei Cloud)
2. Submit ICP filing through provider's portal
3. Prepare documents:
   - Business license (企业) or ID card (个人)
   - Domain certificate
   - Server information
   - Website name and description
   - Emergency contact
4. Wait 10-20 business days for approval
5. Display ICP number in website footer
```

### ICP Display (Required)
```html
<!-- Footer of every page -->
<footer>
  <a href="https://beian.miit.gov.cn/">京ICP备XXXXXXXX号-1</a>
  <!-- If using CDN/Cloud, also need 公安备案 -->
  <a href="http://www.beian.gov.cn/">京公网安备XXXXXXXXXXXXX号</a>
</footer>
```

## Workflow 3: Baidu-Specific Meta Tags

```html
<head>
  <!-- Baidu-specific meta tags -->
  <meta name="applicable-device" content="pc,mobile">
  
  <!-- Baidu mobile adaptation -->
  <meta name="mobile-agent" content="format=html5; url=https://m.example.com/page">
  
  <!-- Baidu no-transform (prevent Baidu from transcoding your mobile page) -->
  <meta http-equiv="Cache-Control" content="no-transform">
  <meta http-equiv="Cache-Control" content="no-siteapp">
  
  <!-- Baidu search result display -->
  <title>关键词 - 品牌名</title>  <!-- Baidu weights title heavily -->
  <meta name="description" content="...">  <!-- Baidu uses this for snippet -->
  <meta name="keywords" content="...">  <!-- Baidu still uses this! Unlike Google -->
  
  <!-- Open Graph for Baidu (different from Facebook OG) -->
  <meta property="baidu:page:type" content="article">
</head>
```

### Baidu Structured Data
```html
<!-- Baidu uses different structured data format than Google -->
<script type="application/ld+json">
{
  "@context": "https://ziyuan.baidu.com/contexts/cambrian.jsonld",
  "@id": "https://example.com/article/123",
  "appid": "YOUR_BAIDU_APPID",
  "title": "文章标题",
  "images": ["https://example.com/img1.jpg"],
  "description": "文章描述",
  "pubDate": "2026-05-26T08:00:00+08:00",
  "upDate": "2026-05-26T10:00:00+08:00"
}
</script>
```

## Workflow 4: Baidu Smart Mini Program SEO

### Why Smart Mini Program
- Baidu gives ranking boost to sites with Smart Mini Programs
- Appears in Baidu search results with special UI
- Access to Baidu's 600M+ monthly active users

### Setup
```bash
# Install Baidu Smart Mini Program CLI
npm install -g @baidu/smartapp-cli

# Create project
smartapp create my-app

# Preview
smartapp preview --project ./my-app

# Upload
smartapp upload --project ./my-app --desc "版本描述"
```

### Web-SmartApp Adaptation
```html
<!-- Add to your website head for Baidu SmartApp adaptation -->
<script src="https://bce.bdstatic.com/smartapp/xxx/swan-2.0.js"></script>
<script>
swan.webView.getEnv(function(res) {
  if (res.smartprogram) {
    // Running inside Baidu SmartApp
    swan.setNavigationBarTitle({ title: '页面标题' });
  }
});
</script>
```

## Workflow 5: Baidu Algorithm Penalty Avoidance

### Common Penalties
| Penalty Type | Cause | Recovery Time |
|-------------|-------|---------------|
| 降权 (Ranking drop) | Over-optimization, keyword stuffing | 1-3 months |
| K站 (De-indexing) | Spam, cloaking, malicious content | 3-6 months |
| 沙盒期 (Sandbox) | New domain, lack of trust | 1-3 months |
| 收录下降 | Low quality content, duplicate content | 1-2 months |

### Penalty Check
```bash
# Check if site is penalized
# 1. Search site:example.com — if pages disappear, likely penalized
# 2. Check Baidu Webmaster Tools → 安全检测
# 3. Check Baidu Webmaster Tools → 抓取异常

# Common causes:
# - Hidden text/links
# - Doorway pages
# - Link buying/selling
# - Content scraping
# - Keyword stuffing in title/description
# - Multiple domains pointing to same content
```

### Recovery Steps
```
1. Identify the penalty type via Webmaster Tools
2. Fix the violating content/techniques
3. Submit reconsideration via Webmaster Tools
4. Wait patiently (Baidu is slower than Google to respond)
5. Continue producing quality content during wait
```

## Safety Rules

1. **ICP first** — never try to rank on Baidu without ICP filing
2. **No black-hat** — Baidu penalties are harsher and longer than Google
3. **JavaScript caution** — Baidu Spider doesn't render JS well; use SSR or pre-render
4. **Content quality** — Baidu manually reviews top-ranking sites
5. **Baidu ecosystem** — leverage Baidu products (知道, 百科, 贴吧) for backlinks
6. **Mobile mandatory** — Baidu has separate mobile index; mobile optimization is critical
7. **Domain age matters** — new domains enter sandbox; consider buying aged domains

## Quick Reference

| Task | Tool/URL | Action |
|------|----------|--------|
| Webmaster Tools | ziyuan.baidu.com | Verify site, submit sitemap |
| ICP Filing | beian.miit.gov.cn | File through hosting provider |
| Index Check | site:domain.com | Check indexed pages |
| Speed Test | ce.baidu.com | Baidu speed test tool |
| Smart Mini Program | smartprogram.baidu.com | Create mini program |
| Penalty Check | ziyuan.baidu.com → 安全检测 | Check for penalties |
| Link Submit | data.zz.baidu.com/urls | Push URLs for indexing |
