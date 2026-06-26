---
name: ai-info-digest
description: |
  微信公众号文章摘要整理工具。获取用户关注的微信公众号在指定时间范围内发布的文章，逐篇阅读全文，然后按主题聚合整理成一篇简明的摘要文章，标注来源便于评估各公众号的价值。
  当用户提到以下场景时触发：整理公众号文章、公众号周报/日报、微信文章摘要、帮我看看公众号最近发了什么、总结一下这几天的公众号内容、公众号阅读整理、subscription digest、WeChat article summary。
  即使用户没有明确说"公众号"，只要提到"整理最近的文章"、"帮我看看订阅号"、"这周的阅读摘要"等类似表达也应触发。
---

# 微信公众号文章摘要整理

## 概述

收集指定时间范围内用户关注的微信公众号文章，逐篇阅读后按主题聚合整理成简明摘要。每条摘要标注来源公众号，便于用户评估各号的价值（是否值得继续关注）。

## 前置条件

- **Claude in Chrome** MCP 工具（用于浏览器阅读知乎/官网文章全文）
- **WebSearch** 工具（用于搜索兜底）
- 公众号列表配置文件：`~/.claude/skills/wechat-digest/wechat-accounts.json`

配置文件结构：
```json
{
  "accounts": [
    {
      "name": "量子位",
      "zhihu": "https://zhuanlan.zhihu.com/qbitai",
      "website": "qbitai.com",
      "priority": "high"
    }
  ]
}
```
- `zhihu`：知乎专栏或个人主页链接（**首选获取渠道**，绝大多数公众号在此同步发布）
- `website`：公众号独立网站（次选）
- `priority`：high 的公众号文章摘要更详细

## 各公众号知乎链接速查

| 公众号 | 知乎链接 | 类型 |
|--------|----------|------|
| 新智元 | zhihu.com/org/xin-zhi-yuan-88-3/posts | 机构主页（文章列表） |
| 创业邦 | zhuanlan.zhihu.com/chuangyebang | 机构专栏 |
| 运筹OR帷幄 | zhuanlan.zhihu.com/operations-research | 机构专栏 |
| 刘聪NLP | zhihu.com/people/LiuCongNLP | 个人主页 |
| 量子位 | zhuanlan.zhihu.com/qbitai | 机构专栏 |
| 机器之心 | zhuanlan.zhihu.com/jiqizhixin | 机构专栏 |
| 集智俱乐部 | zhuanlan.zhihu.com/swarma | 机构专栏 |
| 数字生命卡兹克 | zhihu.com/people/Khazix | 个人主页 |
| PaperWeekly | zhuanlan.zhihu.com/paperweekly | 机构专栏 |
| AI科技评论 | zhuanlan.zhihu.com/leiphone | 机构专栏 |
| AI前线 | zhuanlan.zhihu.com/infoq | 机构专栏 |
| AINLP | （无知乎，用WebSearch兜底） | — |

## 工作流程

### 第一步：确认输入

1. **时间范围**：用户提供日期范围（如 "最近一天"、"4月1日到4月3日"），根据当前日期计算具体起止日期。
2. **公众号列表**：从 `~/.claude/skills/wechat-digest/wechat-accounts.json` 读取。

### 第二步：获取文章列表

对每个公众号，按以下优先级获取时间范围内的文章：

---

**方案 A（首选）：知乎专栏 / 个人主页**

知乎是绝大多数公众号的内容镜像站，无访问限制，文章时间戳精确。

**机构专栏**（`zhuanlan.zhihu.com/xxx`）：
1. 导航到专栏文章列表：`https://zhuanlan.zhihu.com/xxx?order_by=hot`（或直接访问专栏主页）
2. 用 `get_page_text` 提取文章列表，找到时间范围内的文章标题 + 链接
3. 逐篇导航并 `get_page_text` 读取全文

**机构主页**（`zhihu.com/org/xxx/posts`）：
1. 直接导航到 `/posts` 页面（如新智元：`https://www.zhihu.com/org/xin-zhi-yuan-88-3/posts`）
2. 文章按时间倒序排列，`get_page_text` 读取列表
3. 逐篇导航并读取全文

**个人主页**（`zhihu.com/people/xxx`）：
1. 导航到 `https://www.zhihu.com/people/xxx/posts`（文章列表）
2. 提取时间范围内的文章
3. 逐篇读取全文

**知乎日期识别技巧**：
- 知乎文章时间显示为"X 天前"、"X 小时前"或具体日期
- 根据当前日期反推，确认是否在目标时间范围内
- 如果列表按时间倒序排列，看到超出范围的文章即可停止

---

**方案 B（次选）：公众号官方网站**

适用于有独立网站且内容同步的公众号（量子位→qbitai.com，机器之心→jiqizhixin.com 等）：
1. 导航到官网首页
2. 提取最新文章列表（通常按时间倒序）
3. 筛选时间范围内的文章并逐篇读取

---

**方案 C（兜底）：WebSearch**

适用于知乎和官网都无法获取的情况（如 AINLP）：
- 搜索 `"{公众号名称}" site:mp.weixin.qq.com {YYYY}年{M}月`
- 或搜索 `"{公众号名称}" 最新 {YYYY}年{M}月{D}日`
- 注意：搜索结果日期可能不精准，需人工核实

---

**执行策略**：
- 优先用知乎批量处理所有有链接的公众号
- 可以在同一个标签页依次访问，无需开多个标签
- 有独立网站的公众号失败后才用官网
- 某公众号所有方案都失败时，记录到"未能获取"列表，不阻塞其他公众号的处理

### 第三步：阅读文章全文

对每篇文章：
1. `mcp__Claude_in_Chrome__navigate` 打开链接
2. `mcp__Claude_in_Chrome__get_page_text` 提取全文
3. 记录：公众号名称、标题、发布日期、核心要点

**注意**：`mp.weixin.qq.com` 链接通常被浏览器安全策略拦截，优先使用知乎或官网的同步文章链接。

### 第四步：整理摘要

```markdown
# 公众号摘要：{日期范围}

> {N} 个公众号 · {M} 篇文章

## 要点速览
- 要点1 `[来源号]`
- 要点2 `[来源号]`

## 按主题整理

### 主题一

- **文章标题** `[公众号名]` — 1-2句核心内容，关键数据/结论。
- **文章标题** `[公众号名]` — ...

### 主题二
...

## 各公众号本期表现

| 公众号 | 文章数 | 信息密度 | 独家/原创 | 建议 |
|--------|--------|----------|-----------|------|
| xx     | 3      | ★★★★   | 有        | 保留 |
| yy     | 5      | ★★☆☆   | 无，多转载 | 可考虑取关 |

## 未能获取的公众号
- AINLP：知乎暂无专栏，WebSearch未找到近期文章

## 原文链接
1. [文章标题](链接) — 公众号名
```

**整理原则**：
- 按主题聚合，不按公众号分组；同话题多来源观点并列
- 每篇摘要控制在 1-2 句，提炼信息增量，不复述
- 用 `[公众号名]` 标注来源
- 评估表帮用户判断哪些号值得保留：信息密度标准是独家内容、数据质量、观点深度，而非发文量

### 第五步：输出

1. 保存到 `~/Documents/ai-info-digest/{YYYY-MM-DD}_digest.md`
2. 对话中展示完整摘要
3. 告知文件保存路径

## 异常处理

| 情况 | 处理方式 |
|------|----------|
| 知乎专栏显示"X天前"日期模糊 | 根据当前日期推算，宁可多取不漏 |
| 知乎需要登录才能看文章 | 切换方案B（官网）或方案C（WebSearch） |
| 官网文章列表加载依赖JS | 用 `read_page` 替代 `get_page_text`，查找文章链接 |
| 某公众号近期无更新 | 在评估表中标注"本期无发布" |
| 验证码 / 反爬触发 | 立即停下通知用户，等待人工干预 |
