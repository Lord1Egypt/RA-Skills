# cross-border-ecommerce — 跨境电商选品工具

## 痛点
- 手动调研竞品数据费时费力，格式不统一
- 亚马逊/eBay平台费用计算复杂，容易算错利润
- AI Listing生成需要借助ChatGPT，提示词调优耗时
- 关键词研究工具价格昂贵（Ahrefs月费$99+）

## 场景
- 输入"wireless earbuds"，秒级获取搜索量、竞争度、趋势
- 计算产品成本$10、运费$3、售价$35的亚马逊FBA利润率
- 基于产品名+竞品数据，AI一键生成优化标题+5点描述
- 批量分析多个关键词，快速筛选高价值利基市场

## 定价
- **免费**：关键词分析（10次/天）+ 利润计算器
- **Pro 29元**：无限关键词分析 + 竞品抓取 + AI Listing生成
- **Team 99元**：批量分析（100关键词）+ API调用 + 数据导出

## 指令格式

### 关键词分析
```
cross-border keyword <关键词>              # 分析单个关键词
cross-border keyword <关键词> --json      # JSON格式输出
```

### 批量关键词分析
```
cross-border keywords <关键词1,关键词2,...>  # 批量分析
```

### 利润计算
```
cross-border profit --cost 10 --shipping 3 --price 35 --platform amazon
cross-border profit --cost 50 --shipping 8 --price 199 --platform ebay --fba
cross-border suggest-price --cost 25 --margin 30 --platform amazon
```

### AI Listing生成
```
cross-border listing "<产品名称>"           # 生成AI Listing
cross-border listing "<产品名称>" --market US --platform amazon
```

## 示例输出

### 关键词分析
```
$ cross-border keyword "yoga mat"

📊 瑜伽垫 关键词分析
━━━━━━━━━━━━━━━━━━━━
🔍 搜索量: 67,000/月
📈 竞争度: 68% (中等)
📊 趋势: 稳定
💰 参考竞价: $1.50
🔗 相关词: exercise mat, pilates mat, non slip yoga mat
```

### 利润计算
```
$ cross-border profit --cost 15 --shipping 4 --price 49.99 --platform amazon --fba

💰 亚马逊 FBA 利润分析
━━━━━━━━━━━━━━━━━━━━
📦 产品成本: $15.00
🚢 运费: $4.00
🏭 平台费: $7.50
💳 推荐费 (15%): $7.50
📊 总成本: $34.00
💵 售价: $49.99
━━━━━━━━━━━━━━━━━━━━
✅ 利润: $15.99
📈 利润率: 32.0% (优秀)
```

## 技术栈
- Python 3.9+ / Flask 3.0
- OpenAI API（可选，用于AI Listing生成）
- 关键词数据库（内置热门品类模拟数据）

## 适用平台
- Amazon（全站点）
- eBay
- Shopify（DTC选品参考）
