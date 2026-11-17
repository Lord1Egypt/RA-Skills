---
name: benxiang-memory
description: Shadow Memory —— 把聊天历史持续提交为世界状态，新会话秒恢复。MCP Server（stdio，零依赖）：项目状态持久化在 .origin 包里，AI 不再「记住」什么，开工前 origin_state 取投影，收工时 origin_commit 提交语义事务。事务过确定性门禁才落盘，状态不会因模型记错而腐坏；每个字段都能回答「凭什么是这个值」。当新会话丢失上下文、多 agent 协作状态漂移、项目进度需要持久化与追责时使用。
version: 1.1.1
slug: benxiang-memory
license: Apache-2.0
displayName: Shadow Memory 项目状态持久化
summary: 把聊天历史持续提交为世界状态，新会话秒恢复。MCP Server，事务过确定性门禁才落盘。
metadata:
  openclaw:
    runtime: node >= 18
    tags: [memory, mcp, state, persistence, agent]
---

# 本象记忆 · Shadow Memory（MCP Server）

> 聊天记录是一次性的操作窗口，项目状态持久存在于本象包里。
> AI 不再「记住」什么——开工前申请一份投影，收工时提交一个语义事务。

## 为什么

上下文爆炸的真正问题不是窗口太小，是**聊天记录被当成了项目状态**。
聊得越久越接近内存爆满，压缩摘要不断失真，新开一个会话前功尽弃。

这里把两者拆开：能被丢掉而不心疼的东西（对话）和不能丢的东西（世界状态）分开存放。
状态的每一次改动都要过确定性门禁，所以它不会因为模型记错而慢慢腐坏；
每一个字段都能回答「凭什么是这个值」，所以对不上账时查得出是谁在哪一步弄错的。

## 安装

```bash
# 本象协议仓库
git clone https://github.com/dongsheng123132/2origin.git
cd 2origin

# 验证
npm run test:e2e        # 25 项断言（真起子进程走 stdio JSON-RPC）
```

## 用

```bash
# 建包（空的——每条决策都必须经由事务写入，才都自带来历）
node adapters/memory/init.mjs ./my-project.origin my-project "我的项目"

# 接进 Claude Code
claude mcp add benxiang -- node /绝对路径/adapters/memory/mcp-server.mjs /绝对路径/my-project.origin

# 或设环境变量
ORIGIN_PKG=<包路径> node adapters/memory/mcp-server.mjs
```

## 五个工具

| 工具 | 什么时候用 |
|---|---|
| `origin_state` | 新会话开始、或不确定当前进展时。返回持久状态的投影，不是聊天记录 |
| `origin_commit` | 每做完一件有结论的事就提交一次。不通过则零字节写入并给出可据以重写的理由 |
| `origin_why` | 要汇报一个数字、或对某个当前值有疑问时。给出完整改动链与责任者 |
| `origin_history` | 「最近都改了什么」「谁动过这块」 |
| `origin_diagnose` | 约束、悬空引用、双份账本、模型记错前值的比例 |

## 五类对象

`decision:` 决策 · `task:` 待办 · `risk:` 风险 · `fact:` 已核实事实 · `module:` 工作区

刻意不收聊天记录本身、临时想法、没有结论的讨论——那些属于操作窗口，用完即弃。

## 六条机器可判定的约束

- 决策状态只能取合法值
- 待办状态只能取合法值
- 风险状态只能取合法值
- **每个决策必须写明理由**——没有理由的决策，三个月后没人说得清当初为什么这么定
- 每个待办必须有负责人
- 每条事实必须附证据引用（事实与推断分离）

## 新建对象要显式声明

```json
{ "creates": [{ "id": "decision:mvp", "type": "decision" }],
  "state_changes": [{ "object": "decision:mvp", "field": "status", "to": "decided" }] }
```

不声明就写一个不存在的对象会被当场拒绝——ID 打错一个字母若能静默造出
一个新对象，那个幽灵对象将永远不被任何约束管到。

## 验证

```bash
npm run test:e2e     # 真起子进程走 stdio JSON-RPC 打一整轮，25 项断言
```

`e2e.mjs` 把每一次请求与响应原样打印，任何人可以自己跑一遍对照——
包括「违规提交被拒绝且零字节写入」和「两个 agent 先后改同一个字段后 why 查得出两次改动」。

## 相关

- 本象协议（benxiang-protocol）：AI 时代的持久对象表示层。
- OriginWriter（origin-writer）：同一套机制的写作领域应用——长篇小说的世界状态持久化。

---
