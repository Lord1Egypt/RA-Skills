#!/usr/bin/env node
'use strict';
/**
 * BuyWise — 评价提炼
 * 用法: node scripts/review-scan.js <商品名> [--lang zh|en]
 */

const args = process.argv.slice(2);
const langIdx = args.indexOf('--lang');
const lang = langIdx !== -1 && args[langIdx + 1] === 'en' ? 'en' : 'zh';
const productArgs = args.filter((a, i) => a !== '--lang' && args[i - 1] !== '--lang');
const product = productArgs.join(' ').trim();

if (!product) {
  console.error(lang === 'zh' ? '用法: node scripts/review-scan.js <商品名>' : 'Usage: node scripts/review-scan.js <product>');
  process.exit(1);
}

if (lang === 'zh') {
  console.log(`请深度分析「${product}」的用户评价口碑。

搜索以下多个来源：
1. 搜索「${product} 评测 真实体验」
2. 搜索「${product} 差评 问题」「${product} 踩坑 注意」
3. 搜索「${product} 值得买 知乎」或「${product} 小红书 使用感受」
4. 搜索「${product} reddit review」或「${product} honest review」（国际口碑）
5. 若有重大质量投诉，搜索「${product} 质量问题 投诉」

分析维度：
- 综合评分感知（用户整体满意度）
- 高频好评关键词（反复出现的优点）
- 高频差评关键词（反复出现的问题）
- 严重问题（安全隐患、致命缺陷、虚假宣传）
- 适合场景 vs 不适合场景

输出格式：
⭐ 评价分析 · ${product}
━━━━━━━━━━━━━━━━━━━━━━━
综合口碑：[好评如潮 / 褒贬不一 / 差评较多]

✅ 核心优点
1. [优点一]
2. [优点二]
3. [优点三]

❌ 主要槽点
1. [问题一]
2. [问题二]
3. [问题三]

🚩 红旗警告（若有）
[严重质量问题 / 虚假宣传 / 安全投诉]

👤 适合人群
适合：[具体场景/人群]
不适合：[具体场景/人群]
━━━━━━━━━━━━━━━━━━━━━━━
💡 回复"比价"查看最低购买渠道`);
} else {
  console.log(`Please deeply analyze user reviews and reputation for "${product}".

Search multiple sources:
1. Search "${product} review honest experience"
2. Search "${product} problems complaints" "${product} issues to know"
3. Search "${product} reddit review" "${product} forum"
4. Search "${product} 1 star review" "${product} worst problems"
5. If quality issues suspected, search "${product} recall" "${product} safety issue"

Analysis dimensions:
- Overall sentiment (user satisfaction level)
- Frequently praised features
- Frequently complained issues
- Serious problems (safety hazards, fatal flaws, misleading claims)
- Best use cases vs. situations to avoid

Output format:
⭐ Review Analysis · ${product}
━━━━━━━━━━━━━━━━━━━━━━━
Overall reputation: [Highly rated / Mixed / Poorly rated]

✅ Core strengths
1. [Strength 1]
2. [Strength 2]
3. [Strength 3]

❌ Main complaints
1. [Issue 1]
2. [Issue 2]
3. [Issue 3]

🚩 Red flags (if any)
[Quality defects / misleading claims / safety complaints]

👤 Best for
Good fit: [specific use case / user type]
Not for: [specific use case / user type]
━━━━━━━━━━━━━━━━━━━━━━━
💡 Reply "compare" to find the best price`);
}
