# 职责路由与调用契约

Agent Slim 是**总调度层**：它盘点、排序、执行、验证和回滚，但不判断内容该不该存在、不设计单个 Skill 的内部结构、不定义记忆阈值、不做发布。下列能力各有唯一归属，Agent Slim 只通过输入/输出契约调用它们，不复制其规则。

## 1. 归属表

| 问题 | 唯一归属 | Agent Slim 的角色 | 禁止事项 |
|---|---|---|---|
| 这段内容还有必要存在吗？ | `ponytail` | 把“存在性候选”连同证据交出去，接收 keep/merge/drop 结论 | 不得自行删减或改写正文 |
| 单个 Skill 太大，怎么拆、怎么路由、怎么校验？ | `skill-architect` | 交出 `route-large-skill-body`、`route-large-warm-file` 候选和目标路径 | 不得自己实现章节抽取、pack 生成或路由模板 |
| 现在该不该压缩、该不该交接、阈值是多少？ | `memory-orchestrator` | 只报告记忆摘要的体积与位置，交接由用户触发后走该技能 | 不得写入或复制轮数、Token 阈值，不得生成恢复包 |
| 这一轮到底花了多少 Token？ | 宿主或现有用量工具（如 `token-usage.sh`） | 只读调用，把事实用量放进排序；缺失时标 `unknown` | 不得把 `ceil(chars × 0.6)` 说成账单实测 |
| 怎么打包、过审、发到 GitHub/SkillHub/ClawHub？ | `skill-publisher` | 产出通过验收的候选包，交给发布流程 | 不得跳过 Ponytail/架构师审查，不得自带上传逻辑 |

## 2. 推荐调用顺序

```text
用户提出“整体瘦身”
  -> agent-slim audit              只读盘点，产出 Hot/Warm/Cold 与候选
  -> agent-slim plan               生成 dry-run 计划，候选按动作类型分流
       |-- 存在性疑问      -> ponytail           （结论：keep / merge / drop / rewrite）
       |-- 单 Skill 结构   -> skill-architect    （产出：外移后的文件与路由）
       |-- 记忆/交接       -> 用户显式触发 memory-orchestrator
       `-- 用量事实        -> 宿主用量工具
  -> agent-slim apply              默认 dry-run，显式 --apply 才移动
  -> agent-slim verify             目标状态、哈希、引用、frontmatter、触发回归
  -> agent-slim restore            任一门槛失败时的幂等回滚
  -> skill-publisher               仅在用户要求发布时进入
```

每一步都可单独停止；上游结论缺失时，相关候选只能停留在 `pending-confirmation`，不得被执行。

## 3. 交接数据

交给 `ponytail` 的最小输入：

```json
{
  "candidateId": "cand-012",
  "kind": "skill-body|reference|rule|backup|plugin",
  "evidencePath": "<home-relative path>",
  "bytes": 18234,
  "estimatedTokens": 10940,
  "recentUse": {"available": true, "lastUsedAt": "2026-08-01T00:00:00Z"},
  "question": "is this content still needed?"
}
```

交给 `skill-architect` 的最小输入：同一候选加上 `skillName`、`bodyChars`、`referenceEdges`、`keepEntrySections`。它返回 `packs/` 落点、`SKILL.md` 保留段和校验命令；Agent Slim 只负责把这些结果纳入计划与回归，不重写其内容。

交给 `memory-orchestrator` 的最小输入：`memorySummaryBytes`、`residentRuleBytes`、`sessionCount`、`userRequestedHandoff`。阈值判定、恢复包和“开新对话”提示词全部由该技能决定。

交给 `skill-publisher` 的最小输入：通过 `verify` 的发布候选包路径、版本号、变更摘要、隐私检查结果。发布状态以平台回查为准。

## 4. 能力缺失时的降级

| 缺失能力 | 降级行为 |
|---|---|
| 宿主导出实测 Token 用量 | 只做静态估算排序，标注 `estimated`，不写“已节省” |
| Skill 使用记录（`.usage.json` 等） | `recentUse.available=false`，低频判断降为 `pending-confirmation` |
| 插件管理接口 | 插件只做只读清单，`plugin_disable` 恒为 `unsupported` |
| 会话目录 | `session_archive` 标 `unknown`，不生成归档动作 |
| 路由测试命令 | 触发回归标 `PARTIAL`，不得写成 PASS |

降级结果必须出现在审计与验证输出里；不得用“应该没问题”替代证据。

## 5. 与发布流程的边界

Agent Slim 自身发布同样走 `skill-publisher`：先 Ponytail 判存在性，再由 `skill-architect` 外移低频大块，发布前必须过本技能的注入测量与瘦身闸门，最后打包与三平台检查。闸门只判定“能不能发”，上传、审核轮询和平台回查仍归 `skill-publisher`。发布前的隐私、版权、涉政、密钥、公司数据检查不可因“已预授权”而省略。

## 6. 不重复清单

- 不复制、不推断、不对外声明任何记忆轮数或 Token 阈值；阈值由 `memory-orchestrator` 独占决定。
- 不实现章节抽取、pack 生成、路由模板。
- 不实现平台上传、审核轮询、图标生成。
- 不实现 Token 计费或 provider 用量采集。
- 不实现删除、VACUUM、密钥轮换或系统级配置修改。
