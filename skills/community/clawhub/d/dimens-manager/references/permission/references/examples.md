# dimens-manager 权限管理章节 接口案例

本文档把权限 Skill 要引用的真实接口和真实权限链路拆开说明，重点覆盖：

1. 项目准入与项目内资源授权的区别
2. 角色接口
3. 项目权限接口
4. 行级策略接口
5. 单行 ACL 接口
6. Yjs 协同连接与权限快照入口
7. 当前 CLI 未直接封装，但 Skill 必须解释的平台真实接口

更细的规则说明请分别查看：

- `matrix.md`
- `scenario-routing.md`
- `capability-status.md`

---

## 1. 项目准入不是最终授权

Skill 在解释权限时，第一句话必须先区分这两个层次：

1. 能不能进入项目
2. 能不能操作项目内资源

对于 `role` / `permission` 使用，还要再补一句：

3. CLI 命令执行成功，不等于前端权限快照与后端最终授权已经完全一致

### 1.1 项目准入链路

项目准入依赖项目访问校验链路。

准入判断要点：

| 判断项 | 说明 |
| --- | --- |
| 项目是否存在 | 项目不存在直接拒绝 |
| 项目是否过期 | 过期则拒绝 |
| 项目是否禁用 | 禁用则拒绝 |
| 是否是项目成员 | 是则直接通过 |
| 是否是公开项目 | 不是成员但 `visibility = public_read` 时，可按公开访问者进入 |

准入成功后注入上下文：

| 字段 | 说明 |
| --- | --- |
| `ctx.project` | 当前项目 |
| `ctx.projectAccess.isProjectMember` | 是否项目成员 |
| `ctx.projectAccess.isPublicVisitor` | 是否公开访问者 |
| `ctx.projectAccess.visibility` | 项目可见性 |

结论：

- 通过准入只代表能进入项目上下文
- 不代表自动有表、字段、行、协同权限

---

## 2. 角色接口

### 2.1 路径前缀

| 项 | 内容 |
| --- | --- |
| 前缀 | `/app/mul/project/:projectId/role` |
| 入口角色 | 项目角色入口 |

### 2.2 查询角色列表

| 项 | 内容 |
| --- | --- |
| 方法 | `GET` |
| 路径 | `/app/mul/project/:projectId/role/list` |
| 当前 CLI | `dimens-cli role list` |

### 2.3 新增角色

| 项 | 内容 |
| --- | --- |
| 方法 | `POST` |
| 路径 | `/app/mul/project/:projectId/role/add` |
| 当前 CLI | `dimens-cli role create` |

请求体关键字段：

```json
{
  "name": "班主任",
  "description": "班级管理角色",
  "canManageSheets": false,
  "canEditSchema": false,
  "canEditData": true
}
```

### 2.4 分配 / 移除用户角色

分配：

| 方法 | 路径 | 当前 CLI |
| --- | --- | --- |
| `POST` | `/app/mul/project/:projectId/role/assignUser` | `dimens-cli role assign-user` |

移除：

| 方法 | 路径 | 当前 CLI |
| --- | --- | --- |
| `POST` | `/app/mul/project/:projectId/role/removeUser` | `dimens-cli role revoke-user` |

请求体关键字段：

```json
{
  "roleId": "role_teacher",
  "userId": 1001,
  "sheetId": "sh_class"
}
```

说明：

- `sheetId` 不传时是项目级角色
- `sheetId` 传入时是表级角色

---

## 3. 项目权限接口

### 3.1 路径前缀

| 项 | 内容 |
| --- | --- |
| 前缀 | `/app/mul/project/:projectId/permission` |
| 入口角色 | 项目权限管理入口 |

### 3.2 查询我的权限快照

| 项 | 内容 |
| --- | --- |
| 方法 | `GET` |
| 路径 | `/app/mul/project/:projectId/permission/myPermissions` |
| 鉴权 | `Authorization: Bearer {token}` |

返回字段重点：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data.roles.globalRoles` | `array` | 全局角色 |
| `data.roles.sheetRoles` | `array` | 表级角色 |
| `data.isGuest` | `boolean` | 是否公开访问者 |
| `data.visibility` | `string` | 项目可见性 |
| `data.publicRoleId` | `string \| null` | 公开角色 |
| `data.effectiveDataAccess` | `string` | 生效数据访问范围 |
| `data.effectiveCanRead` | `boolean` | 是否可读 |
| `data.effectiveCanWrite` | `boolean` | 是否可写 |
| `data.capabilities` | `object` | 管理表、编辑结构、编辑数据能力 |
| `data.access` | `object` | 设置、成员、角色、审计、回收站入口权限 |
| `data.currentRole` | `object \| null` | 当前主要角色 |

解释 `role` / `permission` 是否真正生效时，优先看这个接口，而不是先看命令执行是否报错。

### 3.3 查询某张表的权限配置列表

| 项 | 内容 |
| --- | --- |
| 方法 | `GET` |
| 路径 | `/app/mul/project/:projectId/permission/list?sheetId=:sheetId` |
| 当前 CLI | `dimens-cli permission list --project-id PROJ1 --sheet-id sh_xxx` |

### 3.4 新增权限配置

| 项 | 内容 |
| --- | --- |
| 方法 | `POST` |
| 路径 | `/app/mul/project/:projectId/permission/add` |
| 当前 CLI | `dimens-cli permission create` |

请求体说明：

- body 是 `MulPermissionEntity` 的部分字段
- 若带 `sheetId`，服务端会校验该表属于当前项目

### 3.5 更新 / 删除权限配置

更新：

| 方法 | 路径 | 当前 CLI |
| --- | --- | --- |
| `POST` | `/app/mul/project/:projectId/permission/update` | `dimens-cli permission update` |

删除：

| 方法 | 路径 | 当前 CLI |
| --- | --- | --- |
| `POST` | `/app/mul/project/:projectId/permission/delete` | `dimens-cli permission delete` |

删除请求体重点：

```json
{
  "ids": [1, 2, 3],
  "sheetId": "sh_xxx"
}
```

说明：

- 删除和更新后会触发 `yjsSyncService.notifyPermissionChanged`
- 所以 Skill 在解释“为什么协同权限会跟着变化”时，要把权限变更事件也提到

### 3.6 设置资源权限

| 方法 | 路径 | 当前 CLI |
| --- | --- | --- |
| `POST` | `/app/mul/project/:projectId/permission/updateResourcePermission` | `dimens-cli permission set-resource` |

请求体示例：

```json
{
  "roleId": "role_teacher",
  "resourceId": "doc_xxx",
  "resourceType": "document",
  "permission": {
    "visible": true,
    "editable": false
  }
}
```

---

## 4. 行级策略接口

### 4.1 路径前缀

| 项 | 内容 |
| --- | --- |
| 前缀 | `/app/mul/project/:projectId/row_policy` |
| 入口角色 | 行级策略入口 |

### 4.2 查询策略列表

| 项 | 内容 |
| --- | --- |
| 方法 | `GET` |
| 路径 | `/app/mul/project/:projectId/row_policy/list?sheetId=:sheetId` |
| 当前 CLI | `dimens-cli row-policy list` |

### 4.3 新增策略

| 项 | 内容 |
| --- | --- |
| 方法 | `POST` |
| 路径 | `/app/mul/project/:projectId/row_policy/add` |
| 当前 CLI | `dimens-cli row-policy create` |

说明：

- body 是 `MulRowPolicyEntity` 的部分字段
- 如果带 `sheetId`，服务端会校验这张表属于当前项目

### 4.4 带冲突检测的新增 / 更新

新增并检测冲突：

| 方法 | 路径 |
| --- | --- |
| `POST` | `/app/mul/project/:projectId/row_policy/addWithCheck` |

更新并检测冲突：

| 方法 | 路径 |
| --- | --- |
| `POST` | `/app/mul/project/:projectId/row_policy/updateWithCheck` |

### 4.5 行级判定与过滤接口

检查单行访问：

| 方法 | 路径 |
| --- | --- |
| `POST` | `/app/mul/project/:projectId/row_policy/check` |

批量过滤行：

| 方法 | 路径 |
| --- | --- |
| `POST` | `/app/mul/project/:projectId/row_policy/filter` |

### 4.6 启用 / 禁用策略

| 方法 | 路径 | 当前 CLI |
| --- | --- | --- |
| `POST` | `/app/mul/project/:projectId/row_policy/toggle` | `dimens-cli row-policy enable/disable` |

---

## 5. 单行 ACL 接口

### 5.1 路径前缀

| 项 | 内容 |
| --- | --- |
| 前缀 | `/app/mul/rowAcl` |
| 入口角色 | 行级 ACL 例外授权入口 |

### 5.2 授权接口

通用授权：

| 方法 | 路径 | 当前 CLI |
| --- | --- | --- |
| `POST` | `/app/mul/rowAcl/grant` | `dimens-cli row-acl grant-user/grant-role/grant-dept` |

请求体关键字段：

```json
{
  "sheetId": "sh_class",
  "rowId": "row_xxx",
  "target": {
    "roleId": "role_teacher"
  },
  "permission": "edit",
  "canTransfer": false
}
```

### 5.3 查询 ACL 列表

| 方法 | 路径 | 当前 CLI |
| --- | --- | --- |
| `GET` | `/app/mul/rowAcl/list?sheetId=:sheetId&rowId=:rowId` | `dimens-cli row-acl list` |

### 5.4 撤销角色 ACL

| 方法 | 路径 | 当前 CLI |
| --- | --- | --- |
| `POST` | `/app/mul/rowAcl/revokeRoleAccess` | `dimens-cli row-acl revoke-role` |

说明：

- 当前 CLI 先打通了角色撤销主链
- 其他批量授权、转移所有权、更多 revoke 变体，Skill 仍需按能力状态文档说明边界

---

## 6. 协同权限与 Yjs 入口

### 6.1 WebSocket 连接入口

| 项 | 内容 |
| --- | --- |
| 协议入口 | `/mul/yjs/*` |
| 入口角色 | 协同连接入口 |

### 6.2 协同连接阶段的权限判断

连接时会做这些事：

1. `jwt.verify(token, secret)` 解析用户身份
2. 解析 `sheetId` 和 `projectId`
3. 调 `yjsPermissionFilter.getUserPermission`
4. 调 `permissionGuardService.canViewSheet`
5. 调 `permissionGuardService.canEditSheet`
6. 若 `canView` 不通过，直接拒绝连接

这意味着：

- 协同连接本身就是一层独立权限门槛
- 行分页接口能读，不代表 WebSocket 一定能连上
