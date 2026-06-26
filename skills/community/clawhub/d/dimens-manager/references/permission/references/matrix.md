# dimens-manager 权限管理章节 权限矩阵说明

本文档把权限 Skill 里最容易混淆的“层级判断、接口入口、关键入参、关键出参”统一收口，避免解释权限时只停留在抽象概念。

## 1. 五层判断矩阵

处理权限问题时，至少按下面五层判断：

| 层级 | 典型问题 | 真实入口 | 关键入参 | 关键出参 / 结论 |
| --- | --- | --- | --- | --- |
| 准入层 | 能不能进入项目 | `ProjectAuthorityMiddleware` | `projectId`、当前用户身份、项目 `visibility` | `ctx.projectAccess.isProjectMember`、`ctx.projectAccess.isPublicVisitor` |
| 表级层 | 能不能看表、改表 | `/app/mul/project/:projectId/permission/myPermissions`、`/permission/list` | `projectId`、可选 `sheetId` | `effectiveCanRead`、`effectiveCanWrite`、`effectiveDataAccess` |
| 列级层 | 能不能看/改字段 | 权限快照 + 字段权限配置 | `sheetId`、字段集合、角色集合 | 可见字段集合、只读字段集合 |
| 行级层 | 能不能看/改某一行 | `/row_policy/check`、`/row_policy/filter` | `sheetId`、`rowData` / `rows`、`action`、`context` | 当前行可见/可编辑/可删除的最终判定 |
| 协同层 | 能不能连协同、能不能广播给别人 | `/mul/yjs/*`、`YjsPermissionFilter`、`RowChangeBroadcastGuard` | `token`、`projectId`、`sheetId`、接收者权限快照 | `canView`、`canEdit`、是否广播、接收者专属增量包 |

## 2. 接口矩阵

### 2.1 项目准入与综合权限

| 接口 / 入口 | 方法 | 场景 | 核心入参 | 返回重点 |
| --- | --- | --- | --- | --- |
| `/app/mul/project/:projectId/permission/myPermissions` | `GET` | 看当前用户在项目内的综合权限快照 | `projectId` | `roles`、`isGuest`、`publicRoleId`、`effectiveCanRead`、`effectiveCanWrite`、`capabilities` |
| `/app/mul/project/:projectId/permission/list?sheetId=:sheetId` | `GET` | 看项目级或指定表的权限配置列表 | `projectId`、可选 `sheetId` | 权限记录列表、角色与资源范围 |
| `project_authority.ts` | 中间件 | 先判断能否进入项目上下文 | `projectId`、当前用户 | 项目上下文、公开访问者状态 |

### 2.2 行级策略

| 接口 | 方法 | 场景 | 核心入参 | 返回重点 |
| --- | --- | --- | --- | --- |
| `/app/mul/project/:projectId/row_policy/list?sheetId=:sheetId` | `GET` | 查看某张表的行策略 | `projectId`、`sheetId` | 策略列表、条件、动作、effect |
| `/app/mul/project/:projectId/row_policy/check` | `POST` | 判断单行是否允许某动作 | `sheetId`、`rowData`、`action`、可选 `context` | 当前行对当前动作是否放行 |
| `/app/mul/project/:projectId/row_policy/filter` | `POST` | 批量过滤行可见性或可编辑性 | `sheetId`、`rows`、`action`、可选 `context` | 过滤后的可见/可操作行 |
| `/app/mul/project/:projectId/row_policy/addWithCheck` | `POST` | 新增并检测策略冲突 | 策略 body | `conflicts`、`hasErrors` |
| `/app/mul/project/:projectId/row_policy/updateWithCheck` | `POST` | 更新并检测策略冲突 | 策略 body | `conflicts`、`hasErrors` |

### 2.3 协同权限

| 接口 / 入口 | 方法 | 场景 | 核心入参 | 返回重点 |
| --- | --- | --- | --- | --- |
| `/mul/yjs/*` | WebSocket | 协同连接建立 | `token`、`projectId`、`sheetId` / `id`、`type` | 是否允许连接；失败时 `NO_VIEW_PERMISSION` 等控制消息 |
| `permissionGuardService.canViewSheet` | 服务调用 | 协同连接前判断可见性 | 当前用户、`projectId`、`sheetId` | `canView` |
| `permissionGuardService.canEditSheet` | 服务调用 | 协同写入前判断可编辑性 | 当前用户、`projectId`、`sheetId` | `canEdit` |
| `sanitizeCollaborativeUpdate` | 服务调用 | 先净化系统字段再鉴权 | 原始 Yjs update、当前用户 | `sanitizedUpdate`、净化后 `changedRows` |
| `rowChangeBroadcastGuard` | 服务调用 | 广播前判断接收者是否该收到 | 接收者权限快照、变更前后行 | 是否广播 |

## 3. 推荐排查顺序

1. 先确认项目准入。
2. 再确认前端 `permissionStore` 当前展示和 `myPermissions` 的综合权限快照是否一致。
3. 再确认是表级问题、列级问题还是行级问题。
4. 涉及某一行时，继续落到 `row_policy/check` 或 `row_policy/filter`。
5. 涉及协同时，再看 WebSocket 准入、权限快照缓存、系统字段净化和广播过滤。

补充：

- `role` / `permission` 改动后，如果只验证 CLI 返回，不验证 `myPermissions` 和前端快照，很容易误判“权限已生效”
- 复杂项目权限问题必须同时看前端消费层和后端合并层

## 4. 常见误判对照

| 误判 | 为什么错 | 正确口径 |
| --- | --- | --- |
| 能进入项目就等于能看表 | 准入层只负责进入上下文 | 还要继续看项目权限快照和表级权限 |
| 行分页读取正常就等于协同没问题 | HTTP 读取链路和协同投影链路不同 | 继续检查 Yjs 权限快照和广播过滤 |
| 前端按钮可点就等于后端可写 | 前端只是预判 | 最终以后端权限服务为准 |
| 公开访问者等于匿名游客 | 公开访问者有独立记录和公开角色映射 | 需要结合 `publicRoleId` 一起判断 |
| 系统字段报错一定是列权限问题 | 协同链路还涉及系统字段净化顺序 | 先看净化是否发生，再看列级与行级鉴权 |

## 5. 绝对不要跳过的点

- 不要因为前端按钮可点就默认后端可写。
- 不要因为行分页读取正常就默认协同没问题。
- 不要把协同缓存和普通接口缓存视为同一个东西。
- 不要把项目准入和资源授权混成一个结论。
- 不要用“这人是公开访问者”替代真正的角色、权限、策略分析。
