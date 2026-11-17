---
name: dailyhot
description: "热搜聚合,50+平台热搜列表+关键词搜索+热度趋势+排行榜订阅。触发:热点追踪/热搜查询/内容选题/趋势分析"
tools: [read]
dependencies: []
metadata:
  priority: P1
  category: data
  openclaw:
    emoji: "📊"
    os: ["win32", "linux", "darwin"]
    requires:
      bins: ["python"]
      env: ["DAILYHOT_BASE_URL"]
      config: ["mcp.servers.dailyhot-mcp"]
---

# DailyHot 热搜聚合

基于DailyHotApi(5.5k+星)的50+平台热搜聚合服务，支持微博/知乎/抖音/B站/百度/头条/豆瓣等平台热搜列表获取、多平台批量查询和关键词搜索。内置5分钟缓存机制，减少重复请求，提升响应速度。支持代理池自动切换，确保数据采集稳定性。

## 使用场景

1. 内容创作热点追踪（CP-04热点监控）
2. 营销活动热点结合选题
3. 社交媒体话题监测与预警
4. 行业动态分析与竞品追踪
5. 用户兴趣洞察与趋势预判
6. 多平台热搜横向对比分析
7. 定时巡检与告警（基于Cron定时获取热搜+关键词趋势分析+选题报告生成）

## 工作流

### 主流程: 单平台热搜获取

1. 调用get_supported_platforms获取可用平台列表
2. 用户指定目标平台(如weibo/zhihu/douyin)
3. 调用get_hot_list传入platform和limit获取热搜数据
4. 解析返回结果，提取title/hot/url字段
5. 输出结构化热搜列表

### 多平台批量查询

1. 确定需要对比的平台列表(如weibo,zhihu,douyin)
2. 调用get_multi_hot传入逗号分隔的platforms和limit
3. 解析各平台热搜数据，识别跨平台共同热点
4. 输出多平台热搜对比结果

### 关键词搜索

1. 用户输入搜索关键词
2. 调用search_hot_keyword传入keyword和platform
3. 在指定平台热搜中过滤匹配条目
4. 输出包含关键词的热搜条目及热度值

### 定时巡检模式（来源:合并dailyhot-monitor）

1. 调用get_multi_hot批量获取多平台热搜(weibo,zhihu,douyin,bilibili)
2. 调用search_hot_keyword按关键词过滤相关热点
3. AI筛选匹配账号定位的选题，生成3-5个标题建议
4. 输出选题报告，包含标题建议/切入角度/目标平台/预估流量

## 输入格式

### 单平台热搜
```json
{
  "platform": "weibo",
  "limit": 20
}
```

### 多平台批量
```json
{
  "platforms": "weibo,zhihu,douyin",
  "limit": 10
}
```

### 关键词搜索
```json
{
  "keyword": "AI",
  "platform": "weibo",
  "limit": 20
}
```

## 输出格式

```json
{
  "success": true,
  "data": {
    "platform": "weibo",
    "items": [
      {"title": "热搜标题", "hot": 1234567, "url": "https://...", "index": 1}
    ],
    "total": 20,
    "from_cache": false
  },
  "error": null,
  "code": null
}
```

## MCP工具清单

| 工具 | 参数 | 说明 |
|:-----|:-----|:-----|
| get_hot_list | platform, limit | 获取指定平台热搜榜 |
| get_multi_hot | platforms, limit | 批量获取多平台热搜 |
| get_supported_platforms | 无 | 获取支持的平台列表 |
| search_hot_keyword | keyword, platform, limit | 在热搜中搜索关键词 |

## 支持平台

| 平台ID | 名称 | 类型 |
|:-------|:-----|:-----|
| weibo | 微博热搜 | 社交 |
| zhihu | 知乎热榜 | 知识 |
| douyin | 抖音热搜 | 视频 |
| bilibili | B站热门 | 视频 |
| baidu | 百度热搜 | 搜索 |
| toutiao | 今日头条 | 新闻 |
| douban | 豆瓣热门 | 文化 |
| ithome | IT之家 | 科技 |
| 36kr | 36氪 | 科技 |
| tieba | 百度贴吧 | 社交 |

## 异常处理

| 错误代码 | 场景 | 处理方式 |
|:---------|:-----|:---------|
| HOTLIST_ERROR | 热搜列表获取失败 | 尝试返回缓存数据，无缓存则报错 |
| HOTLIST_CACHE_FALLBACK | API请求失败但缓存可用 | 返回缓存数据并标注cache_reason |
| MULTI_HOT_ERROR | 多平台批量查询失败 | 返回已成功平台数据，标注failed_platforms |
| PLATFORM_ERROR | 平台列表获取失败 | 返回错误信息 |
| SEARCH_ERROR | 关键词搜索失败 | 返回空结果+错误信息 |
| NETWORK_TIMEOUT | 网络超时(30s) | 自动重试1次，失败后返回缓存 |
| PROXY_UNAVAILABLE | 代理池不可用 | 降级为直连模式继续请求 |

## 三省六部归口

- **部门**: 礼部 (libu)
- **职责**: 热点内容追踪与分析
- **关联Agent**: libu

## 示例

### 示例1: 获取微博热搜Top10

输入:
```json
{"platform": "weibo", "limit": 10}
```

执行:
1. 调用get_hot_list(platform="weibo", limit=10)
2. 解析返回的10条热搜数据

输出:
```json
{
  "success": true,
  "data": {
    "platform": "weibo",
    "items": [
      {"title": "AI大模型新突破", "hot": 2345678, "url": "https://weibo.com/...", "index": 1},
      {"title": "科技股大涨", "hot": 1890123, "url": "https://weibo.com/...", "index": 2}
    ],
    "total": 10
  }
}
```

### 示例2: 多平台对比热搜

输入:
```json
{"platforms": "weibo,zhihu,douyin", "limit": 5}
```

执行:
1. 调用get_multi_hot(platforms="weibo,zhihu,douyin", limit=5)
2. 识别三平台共同热点

输出:
```json
{
  "success": true,
  "data": {
    "platforms": {
      "weibo": [{"title": "AI大模型", "hot": 2345678, "url": "..."}],
      "zhihu": [{"title": "AI新突破", "hot": 890123, "url": "..."}],
      "douyin": [{"title": "AI话题", "hot": 567890, "url": "..."}]
    },
    "total_platforms": 3,
    "failed_platforms": null
  }
}
```
