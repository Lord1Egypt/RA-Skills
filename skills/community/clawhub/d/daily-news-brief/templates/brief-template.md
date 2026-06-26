# 📰 每日新闻简报 | {{date}} | {{dayOfWeek}}

## 🌍 国际时事
{{#each international}}
{{@index1}}. **{{title}}** [{{source}}]({{url}})
{{/each}}
{{^international}}
暂无重要国际新闻
{{/international}}

## 💰 经济形势
{{#each economic}}
{{@index1}}. **{{title}}** [{{source}}]({{url}})
{{/each}}
{{^economic}}
暂无重要经济新闻
{{/economic}}

## 🔬 科技发展
{{#each technology}}
{{@index1}}. **{{title}}** [{{source}}]({{url}})
{{/each}}
{{^technology}}
暂无重要科技新闻
{{/technology}}

## 👀 今日关注
{{#each highlights}}
• {{this}}
{{/each}}

## 📚 历史回顾
{{#each historicalContext}}
{{this}}
{{/each}}

---

*简报生成时间：{{generationTime}}*
*数据来源：{{sources}}*
*注：以上新闻基于公开信息整理，具体细节请以官方发布为准*

## 🔍 新闻分析

### 国际局势分析
{{internationalAnalysis}}

### 经济趋势解读
{{economicAnalysis}}

### 科技发展展望
{{technologyAnalysis}}

## 📊 数据统计
- 今日新闻总数：{{totalNewsCount}}
- 国际新闻：{{internationalCount}}条
- 经济新闻：{{economicCount}}条
- 科技新闻：{{technologyCount}}条
- 平均优先级：{{averagePriority}}

## 🎯 重点关注领域
{{#each focusAreas}}
- **{{category}}**: {{keywords}}
{{/each}}

## 📈 趋势预测
{{trendPrediction}}

## 🤖 AI分析摘要
{{aiSummary}}

---
**订阅设置** | **反馈建议** | **历史简报** | **关于我们**

*每日8点准时送达，助您把握全球动态*