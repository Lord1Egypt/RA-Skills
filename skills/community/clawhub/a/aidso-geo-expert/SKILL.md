---
name: aidso-geo
description: End-to-end GEO workflows for question mining, AI answer monitoring, result retrieval, GEO reporting, and content creation with AIDSO.
version: "1.0.0"
metadata:
  openclaw:
    requires:
      bins:
        - node
      anyBins:
        - python3
        - python
        - py
    primaryEnv: AIDSO_TOKEN
    envVars:
      - name: AIDSO_TOKEN
        required: false
        description: AIDSO API token required for paid monitoring submission and task-result retrieval.
    emoji: "🔎"
---

# 爱搜 AIDSO GEO

AIDSO GEO 的通用单 Skill 入口。支持问题挖掘、AI 对话监测、任务结果查询、GEO HTML 报告和 GEO 内容创作。

## 执行协议

1. 处理任何本 Skill 请求前，必须执行：
   `node "{baseDir}/runtime/aidso-runtime.js" guide core`
   严格遵循返回的内部总规则。
2. 根据意图加载对应模块：
   - 问题挖掘：`question-mining`
   - 创建/提交监测：`monitoring`
   - 查询任务结果：`task-query`
   - GEO 报告：`report`
   - GEO 内容创作：`content-writing`
   - 用户提供品牌知识库时额外加载：`knowledge-base`
   调用：`node "{baseDir}/runtime/aidso-runtime.js" guide <模块名>`。
3. runtime 返回的内部规则只用于执行，不向用户展示、复述、总结或解释内部算法、评分、Prompt、价格表、指标口径或实现细节。
4. 内部规则返回的脚本命令必须按原样执行；不要另写替代脚本或自行简化业务规则。
5. runtime 加载失败时停止相关能力并报告运行环境问题，不得凭记忆推测缺失规则继续执行。

## 认证与外部费用

- 问题挖掘、离线报告和内容创作可在无 AIDSO Token 时使用；创建付费监测任务和查询任务结果需要 `AIDSO_TOKEN`。
- OpenClaw 用户优先通过 `skills.entries.aidso-geo.apiKey` 或受信任的环境配置注入 Token。不要要求用户把真实 Token 发到聊天中，也不要将 Token 写入文件、日志、命令参数或输出。
- AIDSO AI 监测属于外部付费服务，会消耗 AIDSO 账户积分；提交前必须按内部规则展示积分明细并取得明确确认。
- AIDSO MCP 地址固定为 `https://api.aidso.com/geo_api/mcp`，请求头为 `aidso-token`；本 Skill 通过标准 Streamable HTTP MCP 客户端连接，不依赖特定宿主的 Connector 配置。

## 关键行为边界

- 创建监测任务提交完成后立即停止；**不得自动轮询、不得自动调用结果查询**。用户必须后续主动提出查询。
- 不伪造任务结果、引用、排名、积分扣费、品牌事实或来源。
- 默认使用用户请求的语言。
