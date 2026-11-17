# 路由设计与实现

## 职责

`src/router.js` 是一个可解释的关键词路由层，判断请求是否属于商业分析，并在命中后分到一个分析子场景。它只返回意图、置信度、原因和提示语，不读取业务数据、不执行分析，也不调用搜索工具。

## 输入与输出

公开入口 `routeSkillIntent(input)` 接受字符串，或至少包含 `message` 字符串的对象。对象中的其他字段（例如 `locale`、`metadata`）目前不会参与判断。

命中时返回：

```js
{
  matched: true,
  intent: "retention_analysis",
  confidence: 0.72,
  reason: "命中留存分析，检测到相关问题模式和关键词。",
  promptHint: "优先做 cohort、续费和流失阶段拆解。"
}
```

未命中时 `intent` 和 `promptHint` 为 `null`。`detectBusinessAnalysis(message)` 用于单独检查是否属于业务分析；`detectIntent(message)` 用于单独识别子场景。

## 当前意图与优先级

路由目前覆盖：

- `growth_analysis`：增长分析
- `funnel_analysis`：漏斗分析
- `retention_analysis`：留存分析
- `revenue_analysis`：收入利润分析
- `efficiency_analysis`：运营效率分析
- `business_diagnosis`：经营诊断
- `market_research`：市场调研

意图分数为命中的非重叠关键词数。同一较长关键词中包含的短关键词不会重复计分。分数相同时按规则中显式声明的 `priority` 选择，不依赖数组排列；置信度仍是规则匹配分数的启发式映射，不代表校准后的概率。

业务场景门控要求至少命中一个业务信号，且综合分数达到 0.2。纯技术或通用写作请求应排除。未识别到具体子场景但已通过业务门控时，默认进入 `business_diagnosis`。

## 维护约定

- 新增关键词或意图时，在 `test/router.test.js` 增加真实输入与预期路由的测试。
- 为会同时命中多个意图的输入明确优先级，并用测试锁定结果。
- 路由规则保持轻量和可解释；路由只负责分流，最终分析仍遵守 [SKILL.md](../SKILL.md)。
- 市场调研所需的数据和网页搜索能力由宿主提供；路由提示语不会执行这些操作。
