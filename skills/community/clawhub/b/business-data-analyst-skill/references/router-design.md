# 路由设计说明

## 目的

该文档用于约定未来 `src/router.js` 的职责边界，确保业务分析类请求在进入模型前能够被稳定分流。

目标不是做复杂的自然语言理解系统，而是先提供一层可维护、可解释、可扩展的轻量路由。

## 适用场景

未来 `src/router.js` 适合处理以下两类判断：

- 是否应命中 `business-data-analyst-skill`
- 命中后应进入哪类分析子场景

建议优先覆盖的子场景：

- 增长分析
- 漏斗分析
- 留存分析
- 收入或利润分析
- 运营效率分析
- 经营复盘或异常诊断

## 推荐输入

建议路由函数至少接收以下字段：

```js
{
  message: string,
  locale?: string,
  metadata?: {
    source?: string,
    channel?: string,
    userRole?: string
  }
}
```

其中 `message` 是主判断依据，`metadata` 只用于辅助，不应反向覆盖文本语义。

## 推荐输出

建议 `src/router.js` 输出统一结构，避免上层调用方自行猜测：

```js
{
  matched: boolean,
  intent: string | null,
  confidence: number,
  reason: string,
  promptHint?: string
}
```

字段建议：

- `matched`: 是否命中当前 skill
- `intent`: 命中的分析意图，例如 `growth_analysis`
- `confidence`: `0` 到 `1` 的置信度
- `reason`: 简短解释命中原因，便于调试
- `promptHint`: 可选，提供给上层的提示词片段或模式建议

## 推荐路由策略

建议按以下顺序判断：

1. 先识别是否为业务分析问题
2. 再识别具体分析子类型
3. 最后补充输出结构化解释

### 第一步：识别业务分析问题

优先识别以下信号：

- 指标词：GMV、转化率、留存、ROI、LTV、客单价、复购、人效、毛利
- 诊断词：为什么下降、定位原因、拆解、归因、复盘、分析波动
- 决策词：给建议、下一步动作、实验方案、优化优先级

反向排除以下场景：

- 纯闲聊
- 纯代码报错排查
- 通用写作润色
- 与经营分析无关的知识问答

### 第二步：识别子场景

建议用关键词和问题结构组合判断，而不是只靠单一词命中。

示例映射：

- `增长`、`新增`、`活跃`、`GMV`、`增长放缓` -> `growth_analysis`
- `漏斗`、`转化`、`注册`、`下单`、`激活` -> `funnel_analysis`
- `留存`、`复购`、`续费`、`流失`、`cohort` -> `retention_analysis`
- `收入`、`利润`、`毛利`、`价格`、`折扣` -> `revenue_analysis`
- `人效`、`库存`、`交付`、`客服效率`、`门店效率` -> `efficiency_analysis`
- `复盘`、`异常`、`波动`、`经营诊断` -> `business_diagnosis`

### 第三步：输出解释

`reason` 字段不要只写“keyword matched”，应尽量保留可读性，例如：

```txt
命中留存分析：请求同时包含“续费率下降”和“定位原因”，符合经营诊断场景。
```

## 实现建议

推荐先从纯规则实现开始，不要一开始引入复杂分类器。

建议拆成三个函数：

```js
function detectBusinessAnalysis(message) {}
function detectIntent(message) {}
function route(message, metadata) {}
```

如果后续规则变多，可以把关键词字典单独拆到配置文件。

## 最小可用版本

`src/router.js` 的第一版至少应满足：

- 能判断是否命中当前 skill
- 能识别 3 到 6 个核心分析意图
- 能返回统一结构
- 能给出简单可读的命中原因

## 与文档内容的关系

路由只负责分流，不负责生成最终分析结论。

真正的分析过程仍应遵守以下文档：

- [../SKILL.md](../SKILL.md)
- [examples.md](examples.md)
- [metric-playbook.md](metric-playbook.md)
