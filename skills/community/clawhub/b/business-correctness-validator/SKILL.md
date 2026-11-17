---
name: business-correctness-validator
description: "业务正确性验证层,LLM输出后独立校验业务规则(28平台内容合规+电商价格风控+风控阈值),校验失败拒绝输出并告警。触发:LLM生成内容后/内容发布前/价格设定后/风控检查 不触发:纯文本生成无校验需求"
version: 1.0.0
user-invocable: true
tools:
  - read
  - exec
dependencies: []
# 注: sensitive-word-mcp是MCP(非Skill),已在metadata.requires.config中声明
# 不在dependencies中声明(dependencies仅用于Skill→Skill依赖)
metadata:
  layer: infrastructure
  priority: "P0"
  category: "validation"
  requires:
    bins:
      - python
    config:
      - mcp.servers.business-correctness-validator-mcp
      - mcp.servers.sensitive-word-mcp
    env:
      - BUSINESS_RULES_CONFIG
  openclaw:
    emoji: "✅"
    os: ["win32", "linux", "darwin"]
---

> **核心功能**: 本技能提供内容后/内容发布前/价格设定后/风控检查、无校验需求等能力。


# business-correctness-validator — 业务正确性验证层

LLM输出后独立校验业务规则,作为LLM与业务落地之间的"最后一道防线"。校验失败→拒绝输出+告警;校验通过→放行。

## 使用场景

1. LLM生成营销文案/商品描述后,发布前校验内容合规性
2. LLM生成定价建议后,校验价格是否在品类风控区间内
3. 定时Cron任务校验租户风控指标(退款率/投诉率/虚假发货率)是否超阈值
4. 违规历史追溯查询,分析租户风控趋势
5. 多租户场景下,各租户独立风控阈值校验

## 工作流

1. **接收校验请求**
   - 输入: content(内容)/price(价格)/metrics(风控指标), platform(平台), tenant_id(租户ID)
   - 验证: 参数非空+类型正确+平台有效
   - 异常: 参数无效→返回`{success:false, error:"...", code:"INVALID_INPUT"}`

2. **加载业务规则矩阵**
   - 配置路径: config/business_rules_matrix.yaml
   - 降级: 配置文件不存在→使用内置默认规则(来源:01/02手册)
   - 来源: 02手册§二28平台矩阵 + 01手册§十风控阈值

3. **执行校验(按类型)**
   - 内容校验: 长度+格式+品类禁令+绝对化用语(严格度分级)
   - 价格校验: 全局区间+品类区间+倾销/欺诈检测
   - 风控校验: 退款率+投诉率+虚假发货率+响应时长(多租户阈值)
   - 来源: 02手册§八8.2平台严格度 + 01手册§七7.3定价风控 + 01手册§十风控

4. **判定结果**
   - pass: 无违规→放行
   - warning: 中低风险违规→告警但放行
   - blocked: 高危/严重违规→拒绝输出+记录违规
   - 风险等级: SAFE/LOW/MEDIUM/HIGH/CRITICAL

5. **记录违规(校验失败时)**
   - 路径: data/business_violations/{tenant_id}_{date}.jsonl
   - 内容: 时间戳+租户ID+违规类型+详情
   - 用途: 违规历史追溯+风控趋势分析

6. **返回校验结果JSON**
   - 结构: {success, data:{result, risk_level, violations, ...}, error, code}

## 输入格式

### 内容校验
```json
{"content": "AI代写文案,专业润色", "platform": "xianyu", "tenant_id": "default"}
```

### 价格校验
```json
{"price": 99.9, "category": "virtual", "platform": "xianyu"}
```

### 风控校验
```json
{"metrics": "{\"refund_rate\":0.08,\"complaint_rate\":0.02}", "tenant_id": "default"}
```

## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "pass|warning|blocked",
    "risk_level": "SAFE|LOW|MEDIUM|HIGH|CRITICAL",
    "platform": "xianyu",
    "tenant_id": "default",
    "violation_count": 0,
    "violations": [],
    "validated_at": "2026-07-07T10:00:00",
    "rule_source": "02手册§二+§八8.1+§八8.2"
  },
  "error": null,
  "code": null
}
```

## 异常处理

| 异常 | 处理 | code |
|:-----|:-----|:-----|
| content为空 | 返回success:false | INVALID_INPUT |
| platform无效 | 返回success:false | INVALID_PLATFORM |
| price非数值 | 返回success:false | INVALID_PRICE |
| category为空 | 返回success:false | INVALID_CATEGORY |
| metrics JSON解析失败 | 返回success:false | INVALID_JSON |
| tenant_id为空 | 返回success:false | INVALID_TENANT |
| 规则矩阵加载失败 | 降级为内置默认规则 | 无(继续执行) |
| 违规日志写入失败 | 记录error日志,不阻断校验 | 无(继续执行) |
| MCP调用超时 | 熔断器触发,返回降级建议 | CIRCUIT_OPEN |

## 业务规则来源

| 规则类型 | 来源文档 | 具体章节 |
|:---------|:---------|:---------|
| 28平台内容矩阵 | 02手册 | §二28平台内容矩阵 |
| 平台严格度分级 | 02手册 | §八8.2(5星最严~2星最松) |
| 广告法违禁词 | 02手册 | §八8.1(绝对化用语) |
| 定价风控区间 | 01手册 | §七7.3(价格区间/异常波动) |
| 退款率阈值 | 01手册 | §十10.2(warn 5%/block 15%) |
| 投诉率阈值 | 01手册 | §十10.3(warn 3%/block 10%) |
| 虚假发货率阈值 | 01手册 | §十10.4(warn 2%/block 8%) |
| 响应时长阈值 | 01手册 | §十10.5(warn 1h/block 24h) |

## 示例

### 示例1: 闲鱼内容校验通过

输入: `{"content": "AI代写文案,专业润色服务", "platform": "xianyu", "tenant_id": "default"}`
输出:
```json
{
  "success": true,
  "data": {
    "result": "pass",
    "risk_level": "SAFE",
    "platform": "xianyu",
    "tenant_id": "default",
    "platform_strictness": 4,
    "content_length": 14,
    "violation_count": 0,
    "violations": [],
    "rule_source": "02手册§二+§八8.1+§八8.2"
  }
}
```

### 示例2: 小红书内容含绝对化用语被拦截

输入: `{"content": "这是全网最好的产品,100%有效", "platform": "xiaohongshu", "tenant_id": "default"}`
输出:
```json
{
  "success": true,
  "data": {
    "result": "blocked",
    "risk_level": "HIGH",
    "platform": "xiaohongshu",
    "platform_strictness": 5,
    "violation_count": 2,
    "violations": [
      {"type": "absolute_word_violation", "severity": "high", "message": "内容包含广告法违禁绝对化用语: 最好", "keyword": "最好"},
      {"type": "absolute_word_violation", "severity": "high", "message": "内容包含广告法违禁绝对化用语: 100%", "keyword": "100%"}
    ]
  }
}
```

### 示例3: 价格倾销检测

输入: `{"price": 0.05, "category": "service", "platform": "xianyu"}`
输出:
```json
{
  "success": true,
  "data": {
    "result": "blocked",
    "risk_level": "CRITICAL",
    "price": 0.05,
    "category": "service",
    "violation_count": 2,
    "violations": [
      {"type": "price_below_category_min", "severity": "medium", "message": "价格0.05低于service品类最低价1.0"},
      {"type": "suspicious_dumping_price", "severity": "critical", "message": "价格0.05低于service品类最低价50%,疑似倾销"}
    ]
  }
}
```

### 示例4: 风控阈值超标告警

输入: `{"metrics": "{\"refund_rate\":0.08,\"complaint_rate\":0.02,\"false_shipment_rate\":0.01}", "tenant_id": "default"}`
输出:
```json
{
  "success": true,
  "data": {
    "result": "blocked",
    "risk_level": "HIGH",
    "tenant_id": "default",
    "violation_count": 1,
    "violations": [
      {"type": "refund_rate_exceeded_warn", "severity": "high", "message": "退款率8.00%超过告警阈值5.00%"}
    ],
    "rule_source": "01手册§十风控阈值"
  }
}
```

## 历史记录

| 版本 | 操作 | 时间 | 原因 |
|------|------|------|------|
| 1.0.0 | created | 2026-07-07 | ARCH-1业务正确性验证层v8.0方案实施 |
