---
name: content-creation-helper
description: Generate finance/trading content for Chinese social platforms — Xiaohongshu (小红书), Zhihu (知乎), and WeChat Official Accounts (公众号). Includes platform-adapted styling, SEO optimization, and audience-aware tone adjustment.
emoji: ✍️
metadata:
  openclaw:
    requires:
      bins: []
    envVars: []
---

# Content Creation Helper — 内容创作助手

Generate platform-optimized finance and trading content for Chinese social media.

**Use this skill when:**
- User asks "帮写一篇小红书笔记" about trading/futures
- User wants to publish a market analysis on Zhihu or 公众号
- User needs content ideas or copy for social media
- User asks for SEO/标题优化
- User wants multi-platform content adaptation

## Platform-Specific Guides

### 1. 小红书 (Xiaohongshu / RED)

**Style:**
- Casual, personal, relatable
- Heavy use of emojis and line breaks
- 800-1500 characters max keep it concise
- Must have: eye-catching cover description, structured sections, call-to-action

**Title patterns:**
```
🔥 [数字]个信号告诉你XX要来了！
📈 期货人必看：我真的被XX搞怕了...
💰 今天操作记录：XX成交，赚了XX
⚠️ 新手做期货千万别犯这[数字]个错误
💡 XX行情深度复盘，错过后悔一年
```

**Structure template:**
```
【封面标题】（大字吸引眼球）

📌 今日重点
[核心观点 1-2句]

📊 行情速览
[关键数据 + 个人解读]

💡 我的思考
[交易逻辑/心态分享]

⚠️ 风险提示
[必要的风险声明]

#期货 #交易 #投资 #理财 #搞钱
```

**Example:**
```
🔥 纯碱今天又跌了，我为什么反而加仓了？

📌 今日重点
纯碱今天跌了3%，但我觉得可能是个机会。
（不是推荐！！理性看！）

📊 行情速览
· 纯碱主力合约 1550，跌幅3.2%
· 库存连续3周累积创新高
· 技术面已经超卖了 ❗️

💡 我的思考
利空出尽 + 技术超卖 + 成本支撑
这三个信号同时出现的时候，
往往就是情绪的极致反转点。
当然，右侧确认之前，绝不重仓。

⚠️ 风险提示
纯碱基本面确实弱势，库存高位
这只是个人复盘记录，不构成投资建议
保护好自己的本金最重要！

#期货 #纯碱 #交易 #投资 #复盘
```

---

### 2. 知乎 (Zhihu)

**Style:**
- Professional, structured, in-depth
- 2000-5000 characters, with clear sections
- Data-driven arguments, citations preferred
- Start with a strong hook, end with actionable summary

**Title patterns:**
```
如何评价202X年X月X日期货市场行情？
期货交易中，XX指标到底有没有用？
期货新手如何建立自己的交易系统？
如何看待近期XX品种的暴涨/暴跌？
期货日内交易真的能稳定盈利吗？
```

**Structure template:**
```
**问题：[用户原始问题或自拟话题]**

**回答：**

## 一、核心观点
[明确的立场和论点]

## 二、数据支撑
[引用行情数据、历史数据对比]
- 数据1：XX品种从XX涨到XX
- 数据2：持仓量变化XX
- 数据3：跨品种对比

## 三、逻辑分析
[分点论述，逻辑链条清晰]
1. 基本面因素
2. 技术面因素
3. 资金面因素

## 四、结论与建议
[不构成投资建议，但给出参考思路]
- 短期判断
- 中长期判断
- 风险警示

---

⚠️ **风险提示：** 以上内容仅为个人分析，不构成投资建议。期货交易风险较高，请合理控制仓位，设置止损。
```

**Example:**
```
**问题：如何评价今日纯碱期货大跌3%？**

**回答：**

## 一、核心观点
今日纯碱大跌是基本面累库 + 资金出逃双杀的结果，短期尚未见底。

## 二、数据支撑
截至今日收盘：
- SA2609 报收 1550，跌幅3.2%
- 交割库库存周环比+8.5万吨，连续3周累库
- 主力合约持仓减少1.8万手，资金明显流出

## 三、逻辑分析
1. 供应端：前期检修装置陆续复产，周度产量恢复至70万吨以上
2. 需求端：玻璃厂补库意愿不强，刚需采购为主
3. 资金面：多头主动减仓，空头增仓打压

## 四、结论
短期1500是关键支撑，若跌破可能加速下行。不建议盲目抄底，等待库存拐点信号。

⚠️ **风险提示：** ...
```

---

### 3. 微信公众号 (WeChat Official Account)

**Style:**
- Semi-formal, professional but readable
- 1500-3000 characters ideal
- Strong headline, clear subheadings, good formatting
- Must include: introduction → analysis → conclusion

**Title patterns:**
```
【盘后总结】202X.XX.XX 期货市场复盘：XX领涨，XX承压
【深度】纯碱连续下跌，抄底还是观望？
【周报】期货市场一周回顾：五大看点
【技术派】用MACD金叉信号抓反弹的正确姿势
【新手课堂】期货交易入门：从零开始认识K线
```

**Structure template:**
```
📌 **今日看点**

[摘要：1-2句话概括核心内容]

---

## 一、市场概览

[今日行情简述，涨跌分布]

## 二、重点品种分析

### 1. [品种A]
[分析 + 数据 + 观点]

### 2. [品种B]
[分析 + 数据 + 观点]

### 3. [品种C]
[分析 + 数据 + 观点]

## 三、交易策略参考

[策略建议 + 风控提醒]

---

📝 **免责声明：** 以上分析仅供参考，不构成投资建议。期货交易风险较大，请根据自身情况谨慎决策。

*如果觉得内容有帮助，欢迎点赞/在看/转发👇*
```

**Example:**
```
📌 **今日看点**

黑色系全线反弹，焦炭领涨+2.5%，铁矿石跟随走强+1.6%；化工品普遍承压，纯碱延续跌势。

---

## 一、市场概览

今日跟踪的40个品种中，25个上涨，12个下跌，3个持平。整体偏强，但结构性分化明显。

## 二、重点品种分析

### 1. 焦炭 J2609 — 领涨黑色系
- 收盘价 2350，涨幅2.5%
- 焦化厂开启第二轮提涨，市场情绪好转
- 但需注意：钢厂利润仍在低位，上方空间或有限

### 2. 纯碱 SA2609 — 继续承压
- 收盘价 1550，跌幅3.2%
- 库存累积 + 产能恢复，短期难有像样反弹
- 技术面超卖，但基本面尚未改善

## 三、交易策略参考

黑色系短期偏强，但追多风险加大。建议等待回调后做多。化工品关注纯碱是否企稳，暂不建议抄底。

---

📝 **免责声明：** ...
```

---

## SEO / 关键词优化

### 标题关键词策略

| Platform | Keywords to Include | Example |
|:---------|:-------------------|:--------|
| 小红书 | 期货/XX品种名/交易/搞钱/干货/避坑 | "纯碱期货大跌后加仓、我的交易思路分享" |
| 知乎 | 如何看待/如何评价/期货/XX品种/交易系统 | "如何评价2026年5月20日期货市场行情？" |
| 公众号 | 复盘/周报/月度总结/深度/交易策略 | "5月20日期货盘后总结 | 焦炭领涨黑色系" |

### Hashtag Strategy

**小红书 hashtags (5-10 tags):**
- Mix high-traffic + niche tags
- Examples: `#期货 #交易 #投资 #理财 #纯碱 #技术分析 #搞钱 #复盘 #趋势交易`

**知乎的话题系统:**
- Select 2-3 broad topics (e.g., 期货, 交易) + 1-2 specific topics (e.g., 纯碱, 化工)

**公众号关键词:**
- Optimize for WeChat search: include "期货复盘", "期货日报", specific product names

## Scripts

### `scripts/content_generator.py`
Content generation utilities:
- `generate_xiaohongshu_post(data, product_name)` — Generate RED-styled note
- `generate_zhihu_answer(topic, data, style)` — Generate Zhihu answer
- `generate_wechat_article(data, section_focus)` — Generate 公众号 article
- `optimize_title(text, platform)` — SEO title optimization
- `generate_hashtags(text, platform)` — Auto-generate relevant hashtags
- `adapt_across_platforms(markdown_content)` — Adapt content for all 3 platforms

## Tone Reference

| Platform | Tone | Formality | Knowledge Level |
|:---------|:-----|:----------|:----------------|
| 小红书 | Friendly, casual, personal | ★★☆☆☆ | Beginner-friendly |
| 知乎 | Professional, analytical | ★★★★☆ | Intermediate+ |
| 公众号 | Semi-formal, authoritative | ★★★☆☆ | Mixed audience |

## Notes

- Always include 风险提示 Disclaimer at the end of any finance-related content
- For 小红书: short paragraphs, generous line breaks, emojis every 2-3 lines
- For 知乎: structured markdown (headings, lists, bold for emphasis)
- For 公众号: avoid too many emojis; use bold and section markers instead
- Never give specific trading advice disguised as educational content
- When in doubt, err on the side of caution with disclaimers
- Content should be informative, never promotional or deceptive
