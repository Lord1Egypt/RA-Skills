---
name: cn-hot-trends
description: >
  聚合中国主流平台热点榜单，获取实时热搜、热议、科技、财经、影视、音乐等多维度热点内容。
  当用户询问"今天热搜是什么"、"微博热搜"、"知乎热榜"、"B站热门"、"抖音热点"、
  "今日热点"、"热点新闻"、"热门话题"、"各平台热榜"、"热点聚合"等时使用此 skill。
  支持按平台查询（微博/百度/知乎/抖音/B站/36Kr/虎嗅等）或按分类查询（热搜/科技/财经/影视/音乐）。
---

# 中国热点榜单聚合

从国内主流平台抓取实时热点，汇总成简报。

## 核心平台（优先抓取）

### 🔥 热搜榜
| 平台 | URL | 抓取方式 |
|------|-----|---------|
| 微博热搜 | `https://weibo.com/ajax/side/hotSearch` | JSON API |
| 百度热搜 | `https://top.baidu.com/board?tab=realtime` | 抓取 `.c-single-text-ellipsis` |
| 抖音热点 | `https://www.douyin.com/hot` | 抓取热榜列表 |
| 知乎热榜 | `https://www.zhihu.com/billboard` | 抓取 `.HotItem-content` |
| 贴吧热议 | `http://c.tieba.baidu.com/hottopic/browse/topicList?res_type=1` | JSON API |

### 📱 社区热议
| 平台 | URL |
|------|-----|
| 虎扑热帖 | `https://bbs.hupu.com/topic-daily-hot` |
| 豆瓣热门讨论 | `https://www.douban.com/group/explore` |
| 掘金热榜 | `https://juejin.cn/hot/articles` |
| 观察者热评 | `https://user.guancha.cn/main/index?click=24-hot-list` |

### 💼 科技财经
| 平台 | URL |
|------|-----|
| 36Kr热榜 | `https://36kr.com/hot-list/catalog` |
| 虎嗅热文 | `https://www.huxiu.com/article/` |
| 钛媒体热文 | `https://www.tmtpost.com/hot` |
| 雪球财经 | `https://xueqiu.com/` |

### 🎬 影视娱乐
| 平台 | URL |
|------|-----|
| B站热门视频 | `https://www.bilibili.com/v/popular/rank/all` |
| 电影票房榜 | `https://piaofang.maoyan.com/dashboard` |
| 豆瓣电影榜 | `https://movie.douban.com/chart` |
| 爱奇艺风云榜 | `https://www.iqiyi.com/trending/` |

### 🎵 音乐榜
| 平台 | URL |
|------|-----|
| QQ音乐流行榜 | `https://y.qq.com/n/yqq/toplist/4.html` |
| 网易云飙升榜 | `https://music.163.com/#/discover/toplist` |

## 抓取工作流

### 通用热搜简报（默认）

1. 并发抓取微博热搜 + 百度热搜 + 知乎热榜
2. 每个平台取 Top 10
3. 去重合并，按热度排序
4. 输出格式化简报

```powershell
# 微博热搜（JSON API，无需登录）
$wb = Invoke-WebRequest -Uri "https://weibo.com/ajax/side/hotSearch" -UseBasicParsing
$data = ($wb.Content | ConvertFrom-Json).data.realtime
$data | Select-Object -First 10 | ForEach-Object { "🔥 $($_.word) [$($_.num)]" }
```

```powershell
# 百度实时热搜
$bd = Invoke-WebRequest -Uri "https://top.baidu.com/board?tab=realtime" -UseBasicParsing
# 解析 data-click 属性中的 title 字段
```

```powershell
# 知乎热榜（需 User-Agent）
$headers = @{ "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" }
$zh = Invoke-WebRequest -Uri "https://www.zhihu.com/billboard" -Headers $headers -UseBasicParsing
```

### 按分类查询

- **热搜类**：微博 + 百度 + 360 + 搜狗
- **科技类**：36Kr + 虎嗅 + 钛媒体 + 掘金 + CSDN
- **财经类**：雪球 + 36Kr财经 + 凤凰科技
- **影视类**：猫眼票房 + 豆瓣电影 + B站热门
- **音乐类**：QQ音乐 + 网易云 + 酷狗TOP500

## 输出格式

```
🔥 热点简报 · [日期 时间]

━━━ 微博热搜 TOP5 ━━━
1. [话题] 🔥[热度]
2. [话题]
...

━━━ 百度热搜 TOP5 ━━━
1. [关键词]
...

━━━ 知乎热榜 TOP5 ━━━
1. [问题标题]
...

📊 今日热点关键词：[词云摘要]
```

## 注意事项

- 部分平台（抖音、微博）需要 Cookie 才能获取完整数据；无 Cookie 时降级抓取公开页面
- 知乎需要设置 User-Agent，否则返回 403
- 百度热搜可直接访问 `https://top.baidu.com/board?tab=realtime`，HTML 中含结构化数据
- 若某平台抓取失败，跳过并继续其他平台，不中断整体流程
- 建议每次聚合 3-5 个平台，避免响应过慢
