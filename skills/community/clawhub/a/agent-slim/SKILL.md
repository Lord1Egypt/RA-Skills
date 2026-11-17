---
name: agent-slim
slug: agent-slim
displayName: Agent 整体瘦身师
version: 0.3.0
status: release-candidate
platforms: [macos, windows, linux]
author: lis
license: MIT
description: Agent 瘦身：压缩规则/记忆/技能/工具，量化省 token，可回滚不改体验。
---

# Agent Slim

Agent 用久了，规则、记忆、技能、工具清单、参考文档和旧会话会越积越多。它们大多仍有用，但每轮都在占 Token。本技能先量出**每轮到底被哪些内容吃掉**，再用可回滚的小动作把常驻开销降下来：体验不变，账能对上。

不绑定具体 Agent：已知布局自动识别，未知布局写一份 `layout.json` 描述即可，不用改代码。三个入口：整体瘦身、跨 Agent 的通用手法、发布前的注入闸门。

## 何时使用

- 每轮对话变慢或变贵，怀疑常驻上下文太重
- 规则、记忆、技能描述越攒越多，不知道哪块最费
- 想瘦身但怕触发词失效、技能调不出来
- 新 Skill 发布或既有 Skill 改动前，需要最后瘦身闸门
- 只想要磁盘瘦身（那属 Cold 层，单独算，不算 Token）

不适用：单个 Skill 的章节外移（`skill-architect`）、某功能该不该存在（`ponytail`）、记忆阈值与交接（`memory-orchestrator`）、改密钥或 provider。

## 三层账本

| 层 | 什么时候进上下文 | 收益口径 |
| --- | --- | --- |
| Hot | 每轮或每次调用都在 | 缩小才可能减少每轮 Token |
| Warm | 触发、路由或任务条件成立才加载 | 只有确实不再加载的那部分才算 |
| Cold | 从不进上下文，只占磁盘 | 只记磁盘，Token 收益恒为 0 |

## 六类源 × 五类手法

| 源 | 典型形态 | 首选手法 |
| --- | --- | --- |
| 规则 | 常驻指令文件、多份重复约束 | 压缩 → 去重 |
| 记忆 | 记忆摘要、画像、每轮注入块 | 结论常驻，过程外移留指针 |
| 技能 | 清单描述 + 正文 + 参考 + 子项 | 压描述（留全触发词）→ 外移正文 → 去重名 |
| 工具 | MCP server 的 tool schema | 裁剪暴露面，只留真用过的 |
| 文档 | 固定注入的模板与参考 | 外移，补读取条件 |
| 冷数据 | 会话、备份、日志、缓存 | 归档（只算磁盘） |

五类手法：**压缩、外移留指针、去重、裁剪暴露面、归档**。前四类才可能省 Token，第五类只省磁盘。逐类识别信号与红线见 `references/generic-playbook.md`。

## 流程

1. **基线**：先量每轮常驻，逐块记字符数，形成 before 表。没有基线就没有"省了多少"。
2. **盘点**：分 Hot/Warm/Cold，每项标证据（measured / estimated / unknown）。
3. **分级**：R1 压缩与外移、R2 隔离与归档、R3 删除与密钥默认禁止。
4. **逐项执行**：一次只改一块，改完立刻记账，并留下回滚位置。
5. **回归**：触发词逐条核对、引用完整、抽样任务仍可用。
6. **对照**：复跑同一口径出 before/after 表。对不上就不算完成。

## 整体瘦身入口

```sh
python3 scripts/agent_slim.py host  --home <agent-home> [--layout layout.json] --output host.json
python3 scripts/agent_slim.py audit --home <agent-home> [--layout layout.json] --json --output audit.json
python3 scripts/agent_slim.py plan  --audit audit.json --output plan.json
python3 scripts/agent_slim.py apply --plan plan.json              # dry-run
python3 scripts/agent_slim.py apply --plan plan.json --apply      # 显式事务
python3 scripts/agent_slim.py verify --plan plan.json --test-prompts prompts.json
python3 scripts/agent_slim.py restore --manifest <transaction>/manifest.json --apply
```

`host` 输出 `supported / unknown / unsupported` 三态，没有证据的能力不得当作可用。只执行三种移动：隔离冗余备份、归档已确认关闭的旧会话、隔离已确认低频的 Skill 文件。目标冲突即停止，不覆盖。缺少 `test-prompts` 时，触发/路由回归只能是 `PARTIAL`。

内置分支认不出的 Agent，用 `layout.json` 声明常驻文件与各层根目录即可（字段见 `schemas/layout.schema.json`，用法见 `docs/usage.md` 第 3 节）。路径必须是审计根内的相对路径；绝对路径与 `..` 一律拒绝。

## 发布闸门（新 Skill 或任何改动，必过）

任一项 FAIL 就停在发布前，不把 `UNMEASURED` 或 `UNKNOWN` 写成 PASS。

```sh
python3 scripts/injection_state.py --check       # 先看 DRIFT / BODY_CHANGED
python3 scripts/injection_state.py --record      # 确认变更符合预期后重记基线
python3 scripts/injection_state.py --check       # 必须 overall: OK
python3 scripts/measure_prompt.py --gate 57344   # 文本七块必须 PASS
python3 scripts/self_test.py                     # 必须 ALL PASS
```

硬指标：`description` 单条 ≤45 字且保留触发词；`SKILL.md` 目标 ≤8 KB，超出外移到 `references/`，只搬不删；文本块闸门 57,344 B 必须 PASS；`check_integration`、`check_release`、包内测试全通过，发布包不含 `.bak.*`、个人路径和公司数据。

## 固定注入测量（内置，针对 Codex）

七块：记忆摘要、基础系统提示、技能目录、权限块、全局 AGENTS、MCP schema、环境上下文。`measure_prompt.py` 只读调用 `codex debug prompt-input` 并解析文本块；不读聊天正文，不写 Codex Home。无 `codex` 命令时如实报 `UNMEASURED`，不得猜数。

其他 Agent 用 `references/measurement.md` 的手工与账单口径：逐块字符数基线、同类任务 input token 对比、日/月换算公式。

- `injection_state.py --record` 不是伪造 PASS，只是确认这批变更后更新下一次比对基准。
- 技能正文、脚本、references 改动通常记 `BODY_CHANGED`，不影响技能目录注入；`description`、技能数量、记忆/AGENTS/rules 改动才会引起 `DRIFT`。
- MCP `tools/list` 原始总量不是每请求注入；App 首请求实际注入缺实测时必须写 `UNMEASURED`。

## 体验不变的底线

- 触发词一个都不能少：描述可压，触发词不可压
- 引用可解析、frontmatter 可闭合
- 每项改动有回滚位置与哈希
- 门槛不过就回滚，不美化数字

## 边界

只做跨维度盘点、排序、调度、验收和回滚；不重写被瘦身 Agent 的内容，不替其他技能做判断。注入测量只读源文件和 `tools/list` schema，不读会话、备份、日志或数据库正文。禁止删除原件、数据库 VACUUM、改密钥或 provider、上传公司数据。实际改动必须有事务清单、哈希和回滚证据。

## 按需路由

先看 `references/routing-index.md`：通用手法读 `generic-playbook.md`；怎么量、怎么让用户看见读 `measurement.md`；真实案例读 `case-workbuddy.md`；命令与布局文件读 `docs/usage.md`；注入口径读 `docs/injection-measurement.md`、`references/budgets.md`、`references/mcp-measure.md`；与 `ponytail`、`skill-architect`、`memory-orchestrator` 的边界见 `references/integration-routing.md`。
