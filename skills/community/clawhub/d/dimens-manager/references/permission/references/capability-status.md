# dimens-manager 权限管理章节 能力状态说明

## 1. 文档目标

这份文档专门回答：

`dimens-manager/references/permission/overview.md` 里哪些能力已经有 CLI，哪些仍然只是 server 真实接口，哪些属于部分对齐。

如果不把这层写清楚，Skill 很容易把“后端有接口”误说成“CLI 已可直接操作”。

---

## 2. 三种状态口径

| 状态 | 含义 | 输出要求 |
| --- | --- | --- |
| `已封装` | 当前已有 CLI 命令 | 可以直接给命令案例 |
| `server-only` | 当前只有后端接口或服务入口 | 只能给接口案例，不能伪装成 CLI 能力 |
| `部分对齐` | CLI 有相关上下游能力，但不能等同于完整权限管理能力 | 必须提示边界 |

---

## 3. 当前权限能力状态

### 3.1 已封装

当前 `dimens-manager/references/permission/overview.md` 已经有可直接执行的 CLI 主链：

| 能力 | 当前状态 | 说明 |
| --- | --- | --- |
| 自定义角色管理 | `已封装` | 已支持 `role list/info/create/update/delete` |
| 用户角色分配 | `已封装` | 已支持 `role assign-user` / `role revoke-user` |
| 项目 / 表级权限管理 | `已封装` | 已支持 `permission list/create/update/delete` |
| 资源权限设置 | `已封装` | 已支持 `permission set-resource` |
| 行级策略管理 | `已封装` | 已支持 `row-policy list/create/update/delete/enable/disable` |
| 单行 ACL 主链 | `已封装` | 已支持 `row-acl list`、`grant-user/grant-role/grant-dept`、`revoke-role` |

补充说明：

- `已封装` 只代表命令入口已存在，不代表“复杂项目权限解释”已经可以脱离前后端真实实现独立完成
- 对 `role` / `permission` 来说，复杂场景仍必须结合前端 `permissionStore`、后端 `/permission/myPermissions` 与 `getEffectiveSheetPermission()` 一起判断

### 3.2 server-only

下面这些能力当前仍然不能伪装成 CLI 主能力：

| 能力 | 当前状态 | 说明 |
| --- | --- | --- |
| 项目准入诊断 | `server-only` | Skill 可以解释准入链路，但当前没有独立 `project_authority_check` CLI |
| 协同权限快照与广播过滤 | `server-only` | 主要是后端服务与 WebSocket 链路能力 |
| 公开角色专项诊断 | `server-only` | 需要结合服务端权限快照、公开角色和协同链路一起看 |
| 前端权限快照消费层 | `server-only` | 当前没有独立 CLI 去还原前端 `permissionStore` 的全部消费逻辑 |

### 3.3 部分对齐

下面这些能力容易被误判成“权限 CLI 已完全支持”：

| 现象 | 为什么只是部分对齐 |
| --- | --- |
| `project list/info`、`sheet info` 能查出结果 | 只能说明上下文和资源读取入口存在，不等于权限管理能力已 CLI 化 |
| `row page/info` 能读出数据 | 只能说明某次读取命中了当前权限，不等于已经有完整权限诊断命令 |
| 行 ACL 已支持 `grant-user/grant-role/grant-dept` | 说明主链已可执行，但并不等于所有撤销、批量授权、转移所有权都已 CLI 化 |

---

## 4. Skill 输出要求

当用户问“这个权限能力 CLI 有没有”时，建议固定按下面顺序回答：

1. 先说明当前属于 `已封装 / server-only / 部分对齐` 哪一类。
2. 如果已有 CLI，就优先给命令案例。
3. 如果没有 CLI，就给真实接口案例，不要伪装成命令能力。
4. 如果只是部分对齐，要明确这是“上下游能力存在”，不是“完整权限管理已全部命令化”。

对 `role / permission` 特别要补一句：

- 当前 CLI 已适合“执行权限变更”
- 但复杂项目权限是否真的正确，仍要回到前端快照和后端最终授权事实源验证

---

## 5. 与其他 references 的关系

建议按下面顺序组合使用：

1. 先看 `command-mapping.md`，确认是否已有现成 CLI。
2. 再看本文件，确认这项能力到底是 `已封装 / server-only / 部分对齐` 哪一类。
3. 如果需要真实接口和字段结构，再看 `examples.md`。
4. 如果是具体业务场景，再看 `scenario-routing.md`。
