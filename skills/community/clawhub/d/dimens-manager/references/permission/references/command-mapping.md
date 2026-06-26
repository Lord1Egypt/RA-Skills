# dimens-manager 权限管理章节 命令速查

## 1. 目标

这份文档把“角色 -> 项目/表级权限 -> 行级策略 -> 单行 ACL”直接映射为可执行 CLI 命令。

说明：

- 下面主示例统一优先使用 `--app-url`，CLI 会自动解析 `teamId / projectId / baseUrl`
- `role create`、`permission create`、`row-policy create` 这几条主链命令已在 CLI 命令测试中覆盖，优先按这里的参数名执行
- 但 `role` / `permission` 的正确使用不能只看命令层；复杂项目权限必须同时参考前端 `permissionStore`、后端 `/permission/myPermissions` 和服务端 `getEffectiveSheetPermission()` 的真实结果

适用场景：

- 用户要直接搭一套自定义角色权限
- AI 需要把权限设计立刻落成命令
- 不希望在权限 Skill 中继续手工摸索参数名

---

## 2. 角色层

执行 `role` 命令前，先记住三个真实规则：

1. `role create` 只是在项目下创建角色，不会自动给任何用户生效
2. `role assign-user` 会自动确保该用户成为项目成员，并刷新其权限缓存
3. 内置角色和公开角色的默认能力不是靠 CLI 命令定义的，而是由后端服务固定管理

### 2.1 创建角色

```bash
dimens-cli role create \
  --app-url https://dimens.bintelai.com/#/TTFFEN/PXWXBJQ/ \
  --name 班主任 \
  --description 班级管理角色 \
  --can-manage-sheets false \
  --can-edit-schema false \
  --can-edit-data true
```

### 2.2 给用户分配角色

```bash
dimens-cli role assign-user \
  --app-url https://dimens.bintelai.com/#/TTFFEN/PXWXBJQ/ \
  --role-id role_teacher \
  --user-id 1001
```

### 2.3 给某张表分配表级角色

```bash
dimens-cli role assign-user \
  --app-url https://dimens.bintelai.com/#/TTFFEN/PXWXBJQ/ \
  --role-id role_teacher \
  --user-id 1001 \
  --sheet-id sh_class
```

---

## 3. 项目 / 表级权限层

执行 `permission` 命令前，先记住四个真实规则：

1. `permission create` 是按 `roleId + sheetId + projectId` 收敛权限记录，不是无限叠加
2. 新表创建后，服务端会执行 `ensureDefaultPermissionsForSheet()` 自动补默认权限
3. 公开角色对新表默认是 `no_access`，不要因为项目是 `public_read` 就误以为公开访问者天然能看表
4. 前端真实展示依赖 `myPermissions` 快照，不是只看某一条 `permission create` 的请求体

### 3.1 创建权限记录

```bash
dimens-cli permission create \
  --app-url https://dimens.bintelai.com/#/TTFFEN/PXWXBJQ/ \
  --role-id role_teacher \
  --sheet-id sh_class \
  --data-access private_rw \
  --can-read true \
  --can-write true
```

建议在真正写入前，先做这两个校验：

1. `dimens-cli permission list --app-url ... --sheet-id SHEET_ID`
2. 前端或接口确认 `/app/mul/project/:projectId/permission/myPermissions` 当前返回

### 3.2 限制列可见范围

```bash
dimens-cli permission create \
  --app-url https://dimens.bintelai.com/#/TTFFEN/PXWXBJQ/ \
  --role-id role_teacher \
  --sheet-id sh_class \
  --data-access private_rw \
  --can-read true \
  --can-write true \
  --column-visibility '{"fld_name":true,"fld_class_no":true,"fld_remark":false}'
```

### 3.3 设置文档 / 报表 / 页面资源权限

```bash
dimens-cli permission set-resource \
  --app-url https://dimens.bintelai.com/#/TTFFEN/PXWXBJQ/ \
  --role-id role_teacher \
  --resource-id doc_xxx \
  --resource-type document \
  --visible true \
  --editable false
```

---

## 4. 行级策略层

### 4.1 只允许查看自己创建的行

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

### 4.2 禁用某条策略

```bash
dimens-cli row-policy disable \
  --app-url https://dimens.bintelai.com/#/TTFFEN/PXWXBJQ/ \
  --id policy_xxx \
  --sheet-id sh_class
```

---

## 5. 单行 ACL 层

### 5.1 给某个用户开放单行查看权限

```bash
dimens-cli row-acl grant-user \
  --sheet-id sh_class \
  --row-id row_xxx \
  --user-id 1001 \
  --permission view \
  --can-transfer false
```

### 5.2 给某个角色开放单行编辑权限

```bash
dimens-cli row-acl grant-role \
  --sheet-id sh_class \
  --row-id row_xxx \
  --role-id role_teacher \
  --permission edit
```

### 5.3 撤销某角色的单行权限

```bash
dimens-cli row-acl revoke-role \
  --sheet-id sh_class \
  --row-id row_xxx \
  --role-id role_teacher
```

---

## 6. 当前建议顺序

默认按下面顺序执行：

1. 先核对前端 `permissionStore` 与后端 `myPermissions`
2. `role create`
3. `permission create`
4. `role assign-user`
5. 再次核对 `myPermissions`
6. `row-policy create`
7. `row-acl grant-*`

如果只做前 2 和第 3 步，不做第 4 步，角色不会自动生效。

如果只看到“命令执行成功”，但前端表现仍不对，优先回到：

1. `references/matrix.md`
2. `references/examples.md`
3. `web/src/store/permissionStore.ts`
4. `server/src/modules/mul/service/permission.ts`
