# 数据源与搜索策略参考

每个模块的数据获取方式、搜索策略、信息饱和标准。

---

## 模块一：市场扫描 — 数据获取策略

### 1.1 Amazon Best Sellers 数据

**搜索**：
```
site:amazon.com "Best Sellers in [Category]"
```

**Fetch**：直接打开 BSR 页面，抓取 Top 100 信息。Amazon 的 BSR 页面分页显示（每页 50 个），尽量抓取至少 Top 50。

**提取字段**：标题、ASIN、售价、评分、评论数、BSR 排名。从 ASIN 可反查上架时间（通常在 Product Information 区块）。

### 1.2 价格带分析

**搜索**：
```
site:amazon.com "[keyword]" "$10" "$20"
"[keyword] price range distribution amazon"
```

**策略**：用不同价格区间关键词多次搜索，统计各区间 listing 数量。

### 1.3 季节性/趋势

**搜索**：
```
"[keyword] Google Trends"
"[keyword] seasonality amazon"
"[keyword] sales trend 2024 2025 2026"
```

**Fetch**：优先 Google Trends 的搜索量曲线（trends.google.com），获取过去 3-5 年的数据。

### 1.4 市场集中度

**搜索**：
```
"[keyword] market share amazon"
"top amazon sellers [category]"
"[keyword] brand concentration amazon"
```

**策略**：从 BSR Top 50 中手动统计品牌出现频率，判断是否有垄断品牌。

### 1.5 新品率

**策略**：从搜索结果中识别 listing 的上架时间。Amazon 页面通常在 Product Information 中标注 "Date First Available"。无法批量获取时，采样 Top 20 + 中部 10 + 尾部 10 估算。

---

## 模块二：竞品拆解 — 数据获取策略

### 2.1 竞品池构建

**搜索**：
```
site:amazon.com "[keyword]"
site:amazon.com "[keyword]" "[price range]"
```

**Fetch**：搜索结果前 2-3 页，提取所有自然排名 listing。过滤掉广告位和完全不相关的产品。

### 2.2 评论痛点提取

**Fetch 策略**：
1. 打开竞品 Amazon 页面 → 滚动到评论区块
2. 筛选 1-3 星评论（URL 添加 `&filterByStar=critical`）
3. 至少抓取 30-50 条 1-3 星评论
4. 对每条评论做归类统计

**搜索补充**：
```
"[product name] complaints reddit"
"[product name] problems review"
"[keyword] worst amazon"
```

### 2.3 评分-价格矩阵

**方法**：从竞品池中提取评分和价格，构建二维矩阵。在脑中或报告中定位四个象限：
- 高评分低价 → 强势竞品
- 高评分高价 → 高端定位
- 低评分低价 → 低端劣质品
- **低评分高价 → 差异化切入点**（用户花了钱但不满意）

### 2.4 供应链信号

**搜索**：
```
site:1688.com "[product keyword]"
"[product] supplier china"
"[product] manufacturer alibaba"
```

**判断维度**：是否有现货、MOQ、价格区间、起订量灵活性。

---

## 模块三：利润测算 — 数据获取策略

### 3.1 产品尺寸重量

**Fetch**：Amazon 产品页 → Product Information 区块 → Product Dimensions / Item Weight

如果页面未标注，通过类似竞品推断或搜索 `"[product] dimensions weight"`

### 3.2 当前 FBA 费率

**搜索**（每次必做）：
```
"Amazon FBA fulfillment fee 2026"
"Amazon referral fee [category] 2026"
"Amazon FBA storage fee 2026"
```

> FBA 费率每年调整 2-3 次，必须搜索最新数据。现有 SKILL.md references 中的费率仅作参考。

### 3.3 头程物流成本

**搜索**：
```
"China to US freight rate 2026"
"shipping cost China to USA per kg"
```

### 3.4 采购成本

**搜索**：
```
site:1688.com "[product] 批发"
site:alibaba.com "[product] wholesale"
```

取中位价格作为采购成本基准。

---

## 模块四：关键词与流量 — 数据获取策略

### 4.1 搜索量

**搜索**：
```
"[keyword] amazon monthly search volume"
"[keyword] search volume jungle scout"
"[keyword] amazon search frequency rank"
```

### 4.2 Google Trends

**URL 模式**：
```
https://trends.google.com/trends/explore?q=[keyword]&geo=US
```

直接 fetch 此 URL 获取趋势图数据。

### 4.3 长尾词

**搜索**：
```
"amazon autocomplete [keyword] suggestions"
"[keyword] related keywords amazon"
"people also search for [keyword] amazon"
```

### 4.4 PPC 竞价

**搜索**：
```
"[keyword] amazon ppc bid 2026"
"[keyword] cost per click amazon"
"[keyword] suggested bid amazon"
```

---

## 卖家社区与 VoC（Voice of Customer）

### Reddit
```
"site:reddit.com/r/FulfillmentByAmazon [keyword]"
"site:reddit.com/r/AmazonSeller [keyword]"
"site:reddit.com/r/AmazonFBA [keyword]"
```

### 中文社区
```
"site:mjzj.com [关键词]"
"[关键词] 亚马逊 卖家 论坛"
```

---

## 搜索纪律

### 强制要求

1. **每模块至少 5 次 web_search + 5 次 web_fetch** 才能声称"已充分收集"
2. **多源交叉验证**：同一数据点至少 2 个来源
3. **无法获取的数据不编造**：标注"需 [工具名] 获取，此处使用估算值"
4. **标注时间**：所有数据注明获取时间和来源

### 搜索优先级

1. 先用 web_search 发现数据源
2. 再用 web_fetch 深入提取具体页面内容
3. 如果 web_fetch 被亚马逊页面拒绝（反爬），改用搜索摘要 + 第三方工具数据补充
4. 竞品详情页是最优先的 fetch 目标（数据最直接）

### 信息饱和检查

完成一个模块后自查：
- [ ] 该模块需要的所有维度都有数据吗？
- [ ] 关键数据有 2+ 来源吗？
- [ ] 有标注"无法获取"的数据吗？如果有，影响结论吗？
- [ ] 最近 2 轮搜索有新信息吗？如果没有 → 可以进入下一模块
