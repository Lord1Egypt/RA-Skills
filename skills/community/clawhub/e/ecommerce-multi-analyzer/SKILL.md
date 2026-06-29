---
name: ecommerce-multi-analyzer
description: 电商多平台商品数据分析助手。输入任意主流电商平台商品链接（淘宝/天猫/京东/拼多多/抖音电商/1688），自动抓取商品详情、搜索跨平台同款商品、对比价格/评分/评价，生成交互式可视化HTML分析报告。触发词：电商分析, 商品分析, 比价, 多平台对比, 帮我看看这个商品, 分析这个链接, 这个值不值, ecommerce analyzer, 商品对比报告, 价格分析, 同款比价。
version: "1.0.0"
agent_created: true
allowed-tools:
  - Read
  - Write
  - Bash
  - WebFetch
  - WebSearch
  - Edit
metadata:
  openclaw:
    requires:
      bins:
        - python.exe
    emoji: "🛒"
    homepage: https://github.com/bettermen/ecommerce-analyzer
---

# 电商多平台商品数据分析助手

输入一个商品链接，自动生成多平台对比分析报告。

## 核心功能

1. **链接智能解析** - 自动识别京东/淘宝/拼多多/抖音/1688链接
2. **商品详情提取** - 价格、标题、规格、评分、评价数、店铺信息
3. **跨平台搜索** - 自动搜索同款商品在各平台的售卖情况
4. **多维度对比** - 价格/评分/评价数/店铺信誉多维度对比
5. **可视化报告** - 生成交互式HTML报告，含图表和购买建议

## 工作流程

### 第一步：解析商品链接

从用户输入中提取商品链接，识别平台类型：
- `jd.com` / `item.jd.com` → 京东
- `taobao.com` / `tmall.com` → 淘宝/天猫
- `pinduoduo.com` / `yangkeduo.com` → 拼多多
- `douyin.com` / `haohuo.jinritemai.com` → 抖音电商
- `1688.com` → 阿里巴巴1688

### 第二步：抓取源商品详情

使用 WebFetch 工具抓取商品页面，提取以下信息：
- 商品标题、主图描述
- 当前价格（含促销价）
- 评分（如页面显示）
- 评价总数
- 店铺名称
- 规格/SKU信息
- 销量数据（如可获取）

若 WebFetch 因反爬无法获取，使用 WebSearch 搜索该商品标题获取信息。

### 第三步：跨平台搜索同款

使用 WebSearch 在以下平台搜索同款商品：
- 搜索策略：`"{商品核心关键词}" site:{平台域名}` 或 `"{商品型号/名称}" {平台名} 价格`
- 覆盖平台：淘宝、京东、拼多多、抖音电商、1688、苏宁易购
- 每个平台提取前3个最相关的商品价格和评分

### 第四步：数据分析

整理数据，计算以下指标：
- 最低价平台 & 价格
- 最高价平台 & 价格
- 平均价 & 价差百分比
- 评分最高平台
- 性价比评分（综合价格/评分/销量）

### 第五步：生成HTML可视化报告

使用 `scripts/generate_report.py` 脚本生成交互式HTML报告：
- 将数据保存为 JSON 文件（`/tmp/ecommerce_data.json`）
- 运行脚本生成报告 HTML
- 数据格式见下方

## 数据格式

分析完成后，将数据整理为以下JSON格式保存到 `/tmp/ecommerce_data.json`：

```json
{
  "source_product": {
    "platform": "京东",
    "title": "商品标题",
    "price": 299.00,
    "original_price": 399.00,
    "rating": 4.8,
    "review_count": 10000,
    "shop_name": "官方旗舰店",
    "image_desc": "商品简要描述",
    "url": "原始链接"
  },
  "cross_platform": [
    {
      "platform": "淘宝",
      "title": "同款商品标题",
      "price": 289.00,
      "original_price": 359.00,
      "rating": 4.7,
      "review_count": 5000,
      "shop_name": "XX数码专营店",
      "url": "商品链接",
      "note": "备注信息"
    }
  ],
  "analysis": {
    "lowest_price": {"platform": "淘宝", "price": 289.00},
    "highest_price": {"platform": "抖音电商", "price": 329.00},
    "average_price": 305.33,
    "price_spread_pct": 13.8,
    "best_rated": {"platform": "京东", "rating": 4.8},
    "best_value": {"platform": "淘宝", "reason": "价格最低且评分4.7，性价比最优"}
  },
  "advice": {
    "buy_recommendation": "推荐在淘宝购买",
    "reason": "价格最低289元，比京东便宜10元，评分4.7分口碑良好",
    "watch_out": ["注意核对店铺是否官方授权", "查看最新评价确保品质稳定"],
    "price_trend_note": "建议关注大促节点（618/双11）可能有更大优惠"
  }
}
```

## 报告生成命令

```bash
python.exe {baseDir}/scripts/generate_report.py /tmp/ecommerce_data.json /tmp/ecommerce_report.html
```

## 使用示例

用户输入：
```
分析这个商品：https://item.jd.com/100012345678.html
```

或：
```
帮我看看这个值不值 https://detail.tmall.com/item.htm?id=123456789
```

## 注意事项

1. **反爬处理**：电商平台反爬严格，WebFetch 可能无法直接获取页面。此时使用 WebSearch 代替，搜索"商品标题 + 平台名"获取结构化信息。
2. **数据精确性**：标注数据来源和获取时间，如价格可能有波动。
3. **链接格式**：支持移动端短链接（如 `tb.cn`、`dwz.cn`），需要先展开或从链接中提取关键词。
4. **多平台覆盖**：至少覆盖 3 个以上平台才有对比意义，如果只在一个平台找到，建议用户手动补充。
5. **报告美观**：HTML报告需要美观专业，包含图表、配色方案和购买建议卡片。
