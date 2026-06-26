---
name: dimens-manager-permission
slug: dimens-manager-permission
description: 用于维表智联角色、项目权限、行级策略、单行 ACL、公开访问和协同权限排查。
version: 1.0.0
author: 方块智联工作室
tags: [permission, access-control, acl, row-policy, dimens-cli]
---

# dimens-manager 权限管理章节

适用产品：

- 产品名称：`维表智联`
- 开发方：`方块智联工作室`
- 官网：[https://dimens.bintelai.com/](https://dimens.bintelai.com/)

## 执行前必读

- ✅ 当前技能目录统一承载“角色 + 项目权限 + 行级权限”能力，不再拆散到多个技能目录
- ✅ 执行任何权限命令前，先完成认证；认证方式优先参考 `dimens-manager/references/key-auth/overview.md`
- ✅ 如果用户给的是 `https://dimens.bintelai.com/#/TEAM/PROJECT/` 这种地址，CLI 可通过 `--app-url` 自动解析 `teamId / projectId / baseUrl`
- ✅ `role` 和 `permission` 的操作口径必须以前端 `permissionStore` 展示的权限快照和后端 `/permission/myPermissions`、`getEffectiveSheetPermission()` 的最终结果一起对齐，不能只看 CLI 命令是否执行成功
- ✅ 先区分“能进入项目”和“能操作项目内资源”不是一回事
- ✅ 最终权限真值以后端为准，前端只负责预判和保守渲染
- ✅ 设计权限时，默认顺序应是：角色 -> 项目/表级权限 -> 行级策略 -> 单行 ACL 例外
- ✅ 行分页读取正常不代表 `yjs-socket` 一定正常；协同问题仍要回到权限快照和广播过滤去判断
- ✅ 角色创建和权限写入后，不代表前端立即等价生效；真实系统里还要联动缓存失效、`notifyPermissionChanged` 和前端权限快照刷新

## 命令维护表

| 命令 | 作用 | 必填参数 | 常用可选 | 细节说明 |
| --- | --- | --- | --- | --- |
| `dimens-cli role create` | 创建项目下自定义角色 | `projectId`, `name` | `description`, `canManageSheets`, `canEditSchema`, `canEditData`, `app-url` | 角色只是权限底盘入口，创建后不代表用户已经有权限 |
| `dimens-cli role update` | 更新角色基础配置 | `projectId`, `roleId` | `name`, `description`, `canManageSheets`, `canEditSchema`, `canEditData`, `app-url` | 默认先读取当前角色数据，再改字段后 update，避免覆盖已有角色能力 |
| `dimens-cli role assign-user` | 给用户绑定角色 | `projectId`, `roleId`, `userId` | `sheetId`, `app-url` | 可做项目级或表级绑定，绑定后还要看缓存刷新和权限快照是否收敛 |
| `dimens-cli permission list` | 查询角色当前权限配置 | `projectId` | `sheetId`, `app-url` | 用于确认角色在项目级或表级的真实权限记录 |
| `dimens-cli permission create` | 创建项目级或表级权限 | `projectId`, `roleId` | `sheetId`, `dataAccess`, `canRead`, `canWrite`, `columnVisibility`, `columnReadonly` | 创建后还要回看前端权限快照和后端有效权限结果 |
| `dimens-cli permission update` | 更新项目级或表级权限 | `projectId`, `id` 或 `roleId` | `sheetId`, `dataAccess`, `canRead`, `canWrite`, `columnVisibility`, `columnReadonly`, `app-url` | 默认先拿当前权限记录，再改字段后 update，不直接盲写局部 patch |
| `dimens-cli permission set-resource` | 设置文档、报表、页面等非表资源权限 | `projectId`, `roleId`, `resourceId`, `resourceType`, `visible`, `editable` | `app-url` | 用于非表资源授权，提交前要先确认资源归属和角色边界 |
| `dimens-cli row-policy create` | 创建行级策略 | `projectId`, `sheetId`, `name`, `effect`, `actions`, `conditions` | `roleId`, `priority`, `matchType`, `active`, `app-url` | 规则型行权限，条件表达式需要和真实字段 ID 对齐 |
| `dimens-cli row-policy update` | 更新行级策略 | `projectId`, `id`, `sheetId` | `name`, `effect`, `actions`, `conditions`, `priority`, `matchType`, `active`, `app-url` | 默认先读当前策略，再改目标字段后更新，避免把原有条件或动作覆盖丢失 |
| `dimens-cli row-policy enable` | 启用行级策略 | `projectId`, `id`, `sheetId` | `app-url` | 策略切换后还要联动确认缓存和权限快照刷新 |
| `dimens-cli row-policy disable` | 禁用行级策略 | `projectId`, `id`, `sheetId` | `app-url` | 禁用后可能影响分页读取和协同结果，要做回归确认 |
| `dimens-cli row-acl grant-user/grant-role/grant-dept` | 授予单行 ACL 例外权限 | `sheetId`, `rowId`, `permission`, `target` | `expiresAt`, `canTransfer` | 用于单行例外授权，不替代通用角色权限设计 |
| `dimens-cli row-acl revoke-role` | 撤销单行 ACL | `sheetId`, `rowId`, `roleId` | - | 当前已封装角色撤销主链，撤销后要看真实生效结果 |
| `yjs_permission_snapshot` | 排查协同越权广播 | `projectId`, `sheetId`, `userId` | `rowFilters`, `columnFilters` | 这是诊断能力，不是标准业务写接口 |

### 强调细节

- 角色、权限、行级策略的更新命令统一遵循“拿数据 -> 改数据 -> 更新数据”，不要把局部 patch 当成通用模式。
- `role create` 不会自动给用户赋权；权限设计的默认顺序仍然是 `role -> permission -> row-policy -> row-acl`。
- `permission update` 和 `row-policy update` 前默认先读取当前记录，避免把原有字段、动作、条件、列权限覆盖丢失。
- CLI 命令执行成功，不等于前端权限快照、后端有效权限、协同权限快照都已收敛；更新后要结合 `myPermissions`、`permissionStore`、协同快照一起判断。
- 涉及文档、报表、页面的资源权限时，先确认资源归属和项目上下文，再写资源权限。

## 核心约束

### 1. 技能职责边界

- 本技能目录同时负责：自定义角色、项目/表级权限、行级策略、单行 ACL
- `role` 负责“谁是谁”
- `permission` 负责“某角色在项目/表/资源层能做什么”
- `row-policy` 负责“满足什么条件的行可以看/改”
- `row-acl` 负责“某一行对某个用户/角色/部门的例外授权”

### 1.1 `role / permission` 的真实前提

- `role create` 只是在项目下创建角色记录，不会自动把角色分配给任何用户
- `role assign-user` 不只是“绑角色”，服务端还会自动确保该用户成为项目成员，并刷新该用户的权限缓存
- `permission create` 的真实作用是为某个 `roleId + sheetId` 写入或更新权限记录；若同角色同表已有旧记录，服务端会按最新记录收敛，而不是简单无限追加
- 前端真实展示依赖 `permissionStore.loadPermissions()` 调 `/app/mul/project/:projectId/permission/myPermissions`
- 后端最终表级结果依赖 `MulPermissionService.getEffectiveSheetPermission()`，它会把角色底盘、显式权限、公开角色回退一起合并

### 1.2 内置角色与公开角色不要误判

- 服务端项目下默认存在 4 个内置角色：管理员、编辑者、查看者、公开角色
- `公开角色` 不是匿名游客，也不是“默认开放”
- 新表创建后，服务端会执行 `ensureDefaultPermissionsForSheet()` 自动补默认权限：
  - 管理员默认 `full_access`
  - 编辑者默认 `team_rw`
  - 查看者默认 `no_access`
  - 公开角色默认 `no_access`
- 所以如果用户要让公开访问者真正看到表，不能只说“项目是 public_read”，还必须继续检查 `publicRoleId` 和该表的显式权限记录

### 2. 五层权限结构

当前至少要按下面五层理解：

1. 准入层
2. 角色与表级层
3. 列级与资源级层
4. 行级裁决层
5. 协同投影层

### 3. 准入不等于授权

- 通过项目准入，只代表能进入项目上下文
- 不代表天然能看任何表、字段、行或协同数据
- 前端能打开某个页面，也不等于后端最终允许读写该资源

### 4. 公开访问者边界

- 公开访问者不是无状态游客
- 公开访问有独立访问记录和公开角色映射
- 公开项目可进入，也不代表默认拥有完整资源权限

### 5. 协同边界

- 行分页读取链路和 `yjs-socket` 必须共用同一套权限事实源
- 但协同权限快照缓存不能和普通接口缓存混用
- 广播前必须先判断接收者对前后行变化是否可见
- `role assign-user`、`permission add/update/delete`、`row-policy` 变更后，后端会触发 `notifyPermissionChanged`；解释“为什么协同权限跟着变”时必须把这一层说明清楚

### 6. 系统字段边界

- 系统字段是“可读受控、写入托管”
- 协同写入到达后，必须先净化系统字段，再做行级和列级校验

## 必查文档

| Skill / references | 作用 | 什么时候必须看 |
| --- | --- | --- |
| `dimens-manager/references/key-auth/overview.md` | 认证、token 获取与失效处理 | 执行任何权限命令前必须先确认 |
| `dimens-manager/references/team/overview.md` | 团队 / 项目准入与角色边界 | 处理能进不能看时必须先看 |
| `dimens-manager/references/table/overview.md` | 表、字段、行数据为什么被继续收窄 | 处理表格权限时建议看 |
| 前端 `web/src/store/permissionStore.ts` | 前端权限快照的真实消费方式 | 解释“前端为什么这样显示”时必须看 |
| 后端 `server/src/modules/mul/service/permission.ts` | `getEffectiveSheetPermission()`、默认权限补齐、缓存失效 | 解释 `permission` 真值时必须看 |
| 后端 `server/src/modules/mul/service/role.ts` | 内置角色、公开角色回退、用户角色绑定 | 解释 `role` 真值时必须看 |
| `references/matrix.md` | 五层权限结构与判断矩阵 | 处理权限问题时必须看 |
| `references/command-mapping.md` | 角色、权限、行策略、单行 ACL 的命令速查 | 直接执行技能时建议先看 |
| `references/scenario-routing.md` | 场景排查路径 | 设计排查步骤时必须看 |
| `references/capability-status.md` | 当前权限相关能力范围 | 判断是否已 CLI 封装时建议看 |
| `references/examples.md` | 权限场景案例 | 需要直接举例时看 |

## 使用场景示例

### 场景 0：为项目落一套自定义角色权限

推荐执行顺序：

1. 先查当前项目真实权限快照，确认不是上下文或公开角色问题
2. 再创建角色
3. 再给角色配置项目级 / 表级权限
4. 再把角色分配给用户
5. 再刷新前端权限快照或重新拉一次 `myPermissions`
6. 如需“只能看自己 / 只能改自己”，再补 `row-policy`
7. 如需对单条记录特例放权，再补 `row-acl`

执行前建议先核对这三个事实源：

1. 前端：`permissionStore` 当前显示的 `effectiveCanRead / effectiveCanWrite / publicRoleId`
2. 后端：`/app/mul/project/:projectId/permission/myPermissions`
3. 后端：目标表的 `permission/list` 与 `getEffectiveSheetPermission()` 对应的表级结果

参考命令：

```bash
dimens-cli role create \
  --app-url https://dimens.bintelai.com/#/TTFFEN/PXWXBJQ/ \
  --name 班主任 \
  --description 班级管理角色 \
  --can-manage-sheets false \
  --can-edit-schema false \
  --can-edit-data true

dimens-cli permission create \
  --app-url https://dimens.bintelai.com/#/TTFFEN/PXWXBJQ/ \
  --role-id role_xxx \
  --sheet-id sh_class \
  --data-access private_rw \
  --can-read true \
  --can-write true \
  --column-visibility '{"fld_name":true,"fld_student_count":true}'

dimens-cli role assign-user \
  --app-url https://dimens.bintelai.com/#/TTFFEN/PXWXBJQ/ \
  --role-id role_xxx \
  --user-id 1001
```

### 场景 1：为什么能进项目却看不到表

标准解释：

1. 项目准入只决定能否进入上下文
2. 表格是否可见还要看表级权限
3. 字段、资源、行数据可能继续被收窄
4. 如果是公开项目，还要继续核对 `publicRoleId` 和公开角色是否真的拿到了该表显式权限

### 场景 2：为什么行分页读取正常但协同仍然越权

标准排查顺序：

1. 检查是否复用了同一套权限事实源
2. 检查协同权限快照缓存是否单独隔离
3. 检查系统字段是否先净化再鉴权
4. 检查广播前后可见性判断是否生效

### 场景 3：公开角色配置成“只能看自己”，为什么协同还是能看到别人

重点判断：

- 问题不一定在策略数据本身
- 先看协同权限快照是否拿对
- 再看广播过滤是否按接收者逐个裁决

### 场景 4：怎么做“只能看自己创建的数据”

推荐命令：

```bash
dimens-cli row-policy create \
  --app-url https://dimens.bintelai.com/#/TTFFEN/PXWXBJQ/ \
  --sheet-id sh_class \
  --role-id role_teacher \
  --name 仅查看自己 \
  --effect allow \
  --actions view \
  --conditions '[{"columnId":"createdBy","operator":"equals","value":"{{currentUser}}"}]' \
  --priority 10 \
  --match-type and \
  --active true
```

## 常见错误与排查

| 错误现象 | 根本原因 | 解决方案 |
| --- | --- | --- |
| 只看 CLI 创建成功，就认定权限已生效 | CLI 只说明命令调用成功，不代表前端权限快照、后端有效权限、协同快照都已收敛 | 继续核对 `myPermissions`、`permissionStore` 和目标表权限列表 |
| 角色建好了就以为用户已经有权限 | `role create` 只创建角色，不会自动绑定用户 | 必须继续执行 `role assign-user` |
| 角色建好了，但用户仍然没权限 | 只创建了角色，没有分配角色或没配权限记录 | 继续执行 `role assign-user` + `permission create/update` |
| 给用户绑定角色后，用户突然能进入项目 | 服务端 `assignUser` 会自动补项目成员关系 | 这是当前真实实现，不是异常 |
| 表级有权限，但某些行还是看不到 | 命中了 `row-policy` 或行级 ACL | 继续检查 `row-policy` 和 `row-acl` |
| 能进项目但不能看表 | 准入通过，不代表表级授权通过 | 继续检查表级权限和角色集合 |
| 新建表后公开访问者仍然看不到 | `ensureDefaultPermissionsForSheet()` 会让公开角色默认 `no_access` | 继续给公开角色配置该表显式权限，不要只依赖项目 `public_read` |
| 前端显示和 CLI 刚改完的权限不一致 | 前端展示依赖 `permissionStore`，后端还涉及缓存失效和权限变更通知 | 刷新 `myPermissions`、重新进入页面，并检查 `notifyPermissionChanged` 链路 |
| 行分页读取正常，协同看到别人行 | 协同缓存串用、广播过滤失效或权限快照错误 | 检查 Yjs 权限快照和 Redis 隔离 |
| 协同更新时报系统字段禁止修改 | 客户端带了系统字段，后端未先净化 | 检查系统字段净化链路 |
| 前端显示可编辑，提交后被拒绝 | 前端只是预判，后端是真值 | 以后端权限服务结论为准 |
| 公开项目访问行为异常 | 把公开访问者当成普通成员或匿名游客 | 重新检查公开角色映射与项目准入 |

## 参考文档

- `references/command-mapping.md`
- `references/matrix.md`
- `references/scenario-routing.md`
- `references/capability-status.md`
- `references/examples.md`
