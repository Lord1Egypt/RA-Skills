# 竞品监控周报 | {{dateRange}}

> 自动生成时间: {{generatedAt}}

## 📊 本周概览

| 竞品 | 动态数 | 重要程度 | 关键事件 |
|------|--------|----------|----------|
{{#each competitors}}
| {{name}} | {{dynamicCount}} | {{importanceIcon}} {{importance}} | {{keyEvent}} |
{{/each}}

---

## 🔍 详细动态

{{#each competitors}}
### {{name}}

{{#each dynamics}}

**[{{category}}] {{title}}**
- 时间：{{date}}
- 来源：{{source}}
- 平台：{{platform}}
{{#if highlights}}
- 亮点：{{highlights}}
{{/if}}
{{#if impact}}
- 影响：{{impact}}
{{/if}}

{{/each}}

{{/each}}

---

## 📈 趋势分析

{{trendAnalysis}}

## 💡 建议行动

{{#each suggestions}}
{{@index}}. {{this}}
{{/each}}

---

## 📎 相关资源

{{#each resources}}
- [{{title}}]({{url}})
{{/each}}

---

*由 OpenClaw 智能竞品监控系统自动生成*
*如有问题，请联系管理员*