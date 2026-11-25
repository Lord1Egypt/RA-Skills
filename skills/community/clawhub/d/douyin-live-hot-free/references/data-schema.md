# Data Schema

`search-results.json` uses schema version `2.0`.

```json
{
  "schemaVersion": "2.0",
  "source": {
    "platform": "抖音精选",
    "pageType": "web-search-results",
    "url": "https://www.douyin.com/jingxuan/search/AI%E5%B7%A5%E5%85%B7?type=general",
    "method": "Easy WebBridge authorized browser page",
    "scope": "抖音精选网页关键词搜索当前快照"
  },
  "query": {
    "keyword": "AI工具",
    "type": "general"
  },
  "capturedAt": "ISO-8601 UTC timestamp",
  "capturedAtLocal": "Asia/Shanghai display timestamp",
  "browser": {
    "displayName": "selected browser display name",
    "browser": "browser family",
    "extensionVersion": "Easy WebBridge extension version"
  },
  "resultCount": 20,
  "items": [
    {
      "position": 1,
      "contentId": "visible work id",
      "contentType": "video | image",
      "duration": "08:55 | null",
      "visibleLikesText": "1.0万",
      "title": "visible title and hashtags",
      "author": "visible author",
      "publishedText": "5天前",
      "coverUrl": "visible cover URL | null",
      "url": "https://www.douyin.com/video/...",
      "visibleLikesValue": 10000
    }
  ],
  "notice": "scope disclaimer"
}
```

Keep unavailable values `null`. Never add fabricated metrics for downstream layouts.
