---
name: bili-anime
description: |
  自动抓取 Bilibili 最近一周最热门的当季新番，按类型分类，展示主要内容简介和更新时间。
  Use when user wants to know trending seasonal anime on Bilibili, current hot anime, weekly anime rankings,
  or asks what anime to watch. Trigger keywords: 追番、新番、新番推荐、B站新番、当季番、B站番剧、anime recommendations.
license: MIT
metadata: {"author": "user", "version": "1.1", "category": "entertainment", "tags": ["bilibili", "anime", "seasonal"]}
allowed-tools: WebSearch WebFetch
---

# Bilibili 当季新番热榜

## 执行步骤

1. 搜索本季度（根据当前月份判断季节：1-3月=冬季番、4-6月=春季番、7-9月=夏季番、10-12月=秋季番）Bilibili 热门新番
2. 重点查找最近一周播放量、追番人数、弹幕数靠前的番剧
3. 每部番剧补充：类型标签、剧情简介（2-3句）、更新状态
4. 按类型分组输出

## 搜索策略

先搜索以下内容获取数据：
- "bilibili 2026 {当前季节}新番 热门排行"
- "B站 {当前季节}番 追番人数 排行榜"
- 必要时访问 Bilibili 番剧页面或相关动漫资讯站获取准确数据

## 输出格式

输出为标准 Markdown 文档，结构如下：

```markdown
# 📅 {YYYY}年{季节}新番热榜

> 数据截至 {当前日期} | 来源：Bilibili 番剧热度榜

---

## 🔥 本周最热 TOP 3

### 1. 《番剧名》

- **类型**：热血 / 冒险 / 奇幻
- **简介**：xxx（2-3句话说清楚核心设定和看点）
- **更新**：每周X更新，已更第X集（共X集）
- **热度**：追番人数 约xxx万 / 本周弹幕最多

### 2. 《番剧名》
...

### 3. 《番剧名》
...

---

## 📂 按类型分类

### 热血·战斗
| 番剧 | 一句话定位 | 更新进度 |
|------|-----------|---------|
| 《番名》 | xxx | 已更第X集 |

### 恋爱·日常
...

### 奇幻·异世界
...

### 悬疑·推理
...

（根据实际有哪些类型灵活调整，没有的类型不强行列出）

---

## 💡 推荐入坑顺序

- **只追一部**：《xxx》—— 理由：xxx
- **追三部**：《xxx》→《xxx》→《xxx》
```

## 注意事项

- 只列当季新番（本季度首播），不列续集和老番
- 如果搜索结果中有续集（第二季、第三季），单独在末尾注明"续集·老粉专属"区
- 热度数据优先用 B站官方数据，其次用动漫资讯站数据
- 数据如有不确定，标注"约" 或 "参考值"，不要瞎编数字
