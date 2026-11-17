# 跨插件文件契约（CDH）

Personal Supervisor（`master-agent-assistance`）与 Governance
（`governance-multi-agent-harness`）之间 Capability Discovery and Handshake
的权威文件契约。插件**只实现**本契约，**不得**分叉或复述契约正文。

机器可读键与枚举保持英文。对人回复使用用户语言。

## 单写者所有权

「知道对方插件存在」≠ 共写同一可变目录。正确做法是：分层所有权 + 引用不复制 +
身份握手。

| 事实 | 唯一写者 | 对方 |
| --- | --- | --- |
| 工单 / `Docs/ACTIVE_PACKET.md` / 验收标准 | supervisor（CMS 面，intake 时写一次） | governance 只引用路径；delegate prompt 引用而不复述 |
| 适配器 / 权限上限 / 路由决策 | governance | supervisor 只读 run link |
| `.agent-state/<task-id>/` 下的 HANDOFF 与证据 | governance（子进程写） | supervisor review 只存 `{path, summary, sha256}` |
| 跨项目对齐 / 重定基线 / 决策 | supervisor | governance 无需知晓 |
| 生命周期状态（`routed` / `running` / …） | 各方自己的 **session log** | bridge 映射；**禁止共享 `status.json`** |
| 人工审批门 | **仅 supervisor** | bridge 程序化对 governance 调用 `approve()` |
| Owner accept / needs-fix | **supervisor review** | bridge 再调用 `governance.accept('accepted' \| 'needs-follow-up')` |

一次 dispatch ⇒ 一个工单 id ⇒ 一个 `.agent-state/<task-id>/` 证据命名空间。
生命周期绝不放进共享可变状态文件。

## 握手 front-matter（schema 1）

`.agent-state/<task-id>/` 下每个执行层 Markdown 文件以如下 YAML front-matter
开头：

```yaml
---
schema: 1
supervisor-task-id: <SupervisorTaskId>
owner: governance
upstream: Docs/ACTIVE_PACKET.md
---
```

| 字段 | 必填 | 规则 |
| --- | --- | --- |
| `schema` | 是 | 整数 `1`（本修订）。不匹配则大声失败。 |
| `supervisor-task-id` | 是 | 非空字符串；supervisor 拥有的任务 id。 |
| `owner` | 是 | 执行层文件固定为 `governance`。 |
| `upstream` | 否 | 指向 supervisor 拥有权威文件的项目相对路径（通常为 `Docs/ACTIVE_PACKET.md` 或工单）。禁止嵌入该文件正文。 |

会话戳记 `governance/supervisor-binding` 携带同一身份（`schema: 1`、`taskId`、
`supervisorTaskId`、`owner: governance`、可选 `upstream`），以便重启回放可在
未先读文件时完成 join。

## 跨层文件引用

一层引用另一层拥有的文件时，引用对象只能是：

```json
{ "path": "Docs/ACTIVE_PACKET.md", "summary": "…", "sha256": "<hex>" }
```

| 字段 | 必填 | 规则 |
| --- | --- | --- |
| `path` | 是 | 项目相对路径，或落在项目 cwd 内的绝对路径。 |
| `summary` | 是 | 短摘要；禁止塞入文件正文。 |
| `sha256` | 优先 | 文件字节的十六进制摘要。由写侧工具/宿主计算，禁止由模型自行声明。 |

不要把工单或 Active Packet 正文复制进 delegate prompt。引用 `upstream`
（或上述引用对象），让子进程打开权威文件。

## 证据命名空间

- 根目录：`.agent-state/<task-id>/`，其中 `<task-id>` 是 `routeFor` 返回的
  **governance** 任务 id。
- 允许内容：HANDOFF、证据摘要、测试日志、有界下一步包 — Markdown 时均带握手
  front-matter。
- 路径必须落在 session workspace 内（禁止 `..`、符号链接或 junction 逃逸）。
- supervisor review 只保留引用对象，不把正文吸入 durable supervisor-memory
  摘要。

## 插件义务

| 仓库 | 实现 | 不拥有 |
| --- | --- | --- |
| ClawSkills `cms-project-governance`（本 Skill） | 契约正文、所有权表、引用形状 | 运行时代码 |
| `governance-multi-agent-harness` | front-matter 助手、binding 戳记、handoff 哈希、路径约束 | 契约正文 |
| `master-agent-assistance` | intake 写 Active Packet / 工单；review 只存引用 | 契约正文；governance session 事件 |

实现选择与本文件冲突时，**以本文件为准**。
