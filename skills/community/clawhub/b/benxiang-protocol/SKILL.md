---
name: benxiang-protocol
description: 本象协议（Benxiang）—— AI 时代的持久对象表示层。聊天记录是一次性的操作窗口，项目世界状态持久存在于 .origin 包里：对象 + 关系 + 状态 + 约束 + 来源。AI 不再「记住」什么——开工前申请一份投影，收工时提交一个语义事务。事务过确定性门禁才落盘，每个字段都能回答「凭什么是这个值」。当新会话丢失上下文、多 agent 协作状态漂移、需要对项目状态做持久化/追责/回放时使用。
version: 1.1.1
slug: benxiang-protocol
license: Apache-2.0
displayName: 本象协议 Benxiang 状态层
summary: AI 时代的持久对象表示层：语义事务 + 确定性门禁 + 证据链。状态可查、可验、可追溯。
metadata:
  openclaw:
    runtime: node >= 18
    tags: [protocol, state, provenance, transaction, agent, mcp]
---

# 本象协议 · Benxiang（Origin IR + 语义事务 + 证据链）

**聊天记录是一次性的操作窗口，项目世界状态持久存在于 .origin 包里。**

AI 不再「记住」什么——开工前申请一份投影，收工时提交一个语义事务。
事务过确定性门禁才落盘，所以状态不会因为模型记错而慢慢腐坏；
每一个字段都能回答「凭什么是这个值」，所以对不上账时查得出是谁在哪一步弄错的。

> 定位：本象协议是面向 AI 工作的中间表示（AI 时代的 LLVM IR）。
> AI 不直接重造世界，只提交对世界的语义修改。

## 安装

```bash
git clone https://github.com/dongsheng123132/2origin.git
cd 2origin
npm run verify    # 自测 96 项 + MCP 端到端 25 项 + 变异检查 19/19
```

零依赖：核心运行时（compiler/）不引任何第三方包，可直接独立核对。

## 用

```bash
# 1. 建包（空的——每条决策都必须经由事务写入，才都自带来历）
node adapters/memory/init.mjs my-project.origin my-project "我的项目"

# 2. 新会话第一件事：恢复项目世界状态
node compiler/cli.mjs status my-project.origin

# 3. 每做完一件有结论的事，提交一个语义事务
#    （决策 / 待办 / 风险 / 事实 / 工作区，见下方对象模型）
node compiler/cli.mjs commit my-project.origin tx.json --by agent-a

# 4. 对某个值有疑问，问它凭什么
node compiler/cli.mjs why my-project.origin decision:mvp.status

# 5. 包体检：约束有没有违反、有没有悬空引用、模型记错前值的比例
node compiler/cli.mjs diagnose my-project.origin && echo healthy
```

事务文件（tx.json）形状：

```json
{
  "transaction_id": "tx-20260807-001",
  "operation": "decide",
  "creates": [{ "id": "decision:mvp", "type": "decision" }],
  "state_changes": [
    { "object": "decision:mvp", "field": "status", "from": "proposed", "to": "decided", "op": "set" },
    { "object": "decision:mvp", "field": "value", "to": "先做 Shadow Memory", "op": "set" }
  ],
  "assertions": ["no-ghost-objects", "every-decision-has-rationale"]
}
```

## 五类对象

| 前缀 | 对象 | 收什么 |
|---|---|---|
| `decision:` | 决策 | 定了什么、为什么（必须写明理由） |
| `task:` | 待办 | 做什么、谁负责（必须有负责人） |
| `risk:` | 风险 | 风险、等级、缓解（状态必须合法） |
| `fact:` | 已核实事实 | 事实（必须附证据引用，事实与推断分离） |
| `module:` | 工作区 | 某个模块/领域的边界 |

## 六条机器可判定的约束

全部用通配对象（`decision:*`），新增对象自动被覆盖，不需要有人记得补规则：

- 决策状态只能取合法值
- 待办状态只能取合法值
- 风险状态只能取合法值
- **每个决策必须写明理由**——没有理由的决策，三个月后没人说得清为什么这么定
- 每个待办必须有负责人
- 每条事实必须附证据引用（事实与推断分离）

## 为什么状态不会腐坏

1. **原文与事实是本源**——摘要只是可重建投影，无权覆盖本源
2. **每次改动都过门禁**——结构/引用/快照隔离逐条复核，失败零字节写入
3. **推断与事实分开**——`status: inference` + 置信度 + 证据引用
4. **每个状态都有来源**——`valid_from` 事件 + `evidence` 引用，出错也能追溯回原文
5. **新建对象要显式声明**——ID 打错一个字母不会静默造出没人管的幽灵对象

## MCP 接入（推荐）

```bash
node adapters/memory/mcp-server.mjs my-project.origin
# 或
ORIGIN_PKG=my-project.origin node adapters/memory/mcp-server.mjs
```

五个工具：`origin_state`（新会话恢复投影）/ `origin_commit`（提交事务）/
`origin_why`（查值凭什么）/ `origin_history`（谁动过这块）/ `origin_diagnose`（包体检）。

## 验证

```bash
npm run verify
```

完整验证链：核心自测 + 五个方言自测（cad/law/office/xlsx/story）+
MCP 端到端（e2e）+ 一致性向量（conformance）+ 变异检查（mutation）。

`compiler/mutation-check.mjs` 会故意打坏协议承诺看自测抓不抓得到——改核心代码后必须重跑。

## 相关

- OriginWriter（origin-writer skill）：百万字小说写作引擎——把长篇写作变成事务性写作，
  本协议在 Story 方言上的应用。
- Shadow Memory（benxiang-memory skill）：MCP Server 版的项目状态持久化，开箱即用。
- 影核协议（Action Kernel）：统一动作层——AI 想做什么、由谁执行。
- 叠象（Redline）：状态、差异、证据与版本层——改了什么、对不对、能否证明。

---
