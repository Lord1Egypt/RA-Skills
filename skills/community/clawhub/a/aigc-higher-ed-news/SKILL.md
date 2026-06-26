---
name: aigc-higher-ed-news
description: |
  高校AIGC资讯聚合。覆盖：AIGC行业资讯、AI微专业动态、高校招标需求（语音室/同声传译/云桌面）、高校AI政策。
  每日自动执行，输出结构化简报。
metadata:
  openclaw:
    emoji: "🎓"
---

# 高校AIGC资讯聚合

## 触发条件
- 定时任务触发（每日08:00）
- 用户说"高校资讯"、"AIGC日报"、"高校招标"等

## 执行流程

## 执行流程

### Step 1: 搜索

**如果 web_search 工具可用**，使用 web_search 按以下分类搜索，country=CN，language=zh，freshness=day。

**如果 web_search 不可用**，使用 web_fetch 直接抓取百度搜索结果页：
```
web_fetch("https://www.baidu.com/s?wd=关键词&rn=10")
```
从返回的 HTML 中提取搜索结果标题和链接。

同时可直接抓取以下源站获取最新文章：
- https://www.jiqizhixin.com/ （机器之心）
- https://www.zhidx.com/ （智东西）
- https://www.leiphone.com/category/ai （雷锋网AI频道）
- https://www.infoq.cn/topic/AI （InfoQ AI频道）
- http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/ （教育部工作动态）

**分类1: AIGC行业资讯**
- 百度搜索: `web_fetch("https://www.baidu.com/s?wd=AIGC+最新动态+2026&rn=10")`
- 百度搜索: `web_fetch("https://www.baidu.com/s?wd=大模型+教育应用+最新&rn=10")`
- 直接抓取: 智东西、雷锋网AI频道

**分类2: AI微专业**
- 百度搜索: `web_fetch("https://www.baidu.com/s?wd=AI微专业+高校+招生+2026&rn=10")`
- 百度搜索: `web_fetch("https://www.baidu.com/s?wd=人工智能+微专业+高校+新增&rn=10")`

**分类3: 招标需求（语音室/同声传译/云桌面）**
- 百度搜索: `web_fetch("https://www.baidu.com/s?wd=语音实验室+招标+高校+2026&rn=10")`
- 百度搜索: `web_fetch("https://www.baidu.com/s?wd=同声传译实验室+采购+招标&rn=10")`
- 百度搜索: `web_fetch("https://www.baidu.com/s?wd=云桌面+高校+招标+2026&rn=10")`

**分类4: 高校AI政策**
- 百度搜索: `web_fetch("https://www.baidu.com/s?wd=教育部+人工智能+政策+2026&rn=10")`
- 直接抓取: 教育部官网 http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/

### Step 2: 筛选

对搜索结果进行筛选：
- 仅保留过去24小时内的内容
- 去重：同一事件只保留最权威来源
- 剔除广告、软文、无关内容
- 每个分类保留3-5条最有价值的

### Step 3: 补充详情（可选）

对特别重要的条目（如重大招标、政策发布），使用 web_fetch 获取详情摘要。

### Step 4: 输出格式

```markdown
🎓 高校AIGC日报 | {{日期}} | 第{{期数}}期

📋 今日摘要
（1-2句话概括今日重点）

🤖 AIGC行业资讯
- {{标题}} — {{一句话摘要}} [链接]
  （按重要性排序，3-5条）

🎓 AI微专业动态
- {{标题}} — {{一句话摘要}} [链接]
  （2-3条）

🏢 高校招标需求
- {{标题}} — {{一句话摘要}} [链接]
  （语音室/同声传译/云桌面相关，3-5条）

📜 高校AI政策
- {{标题}} — {{一句话摘要}} [链接]
  （2-3条）

📊 趋势观察
（简要总结今日发现的趋势或值得关注的信号）
```

### Step 5: 存档

- 保存到本地: `skills/aigc-higher-ed-news/digests/YYYY-MM-DD.md`
- 如有IMA权限，同步到指定知识库

## 信源参考

| 分类 | 信源 |
|------|------|
| AIGC资讯 | 机器之心、量子位、新智元、智东西、36氪AI频道 |
| AI微专业 | 教育部官网、各省教育厅、高校官网教务处 |
| 招标需求 | 中国政府采购网、千里马招标、中国招标投标公共服务平台 |
| 高校AI政策 | 教育部官网、科技部、各省教育厅、高校官网 |

## 注意事项
- 搜索使用中文关键词，region=CN
- freshness=day 确保只获取24小时内内容
- 如某分类无结果，标注"今日暂无相关更新"
- 不要编造链接，只使用搜索返回的真实URL
