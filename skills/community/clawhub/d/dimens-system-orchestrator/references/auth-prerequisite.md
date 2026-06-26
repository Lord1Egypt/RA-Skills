# dimens-system-orchestrator 认证前置机制

## 1. 结论

`dimens-system-orchestrator` 里的项目梳理、新建项目、修改项目内数据、查询和分类路由，只要进入真实执行命令阶段，都必须先完成认证。

认证只能通过 API Key / API Secret 换取 token，推荐统一使用：

```bash
dimens-cli auth api-key-login \
  --base-url https://dimens.bintelai.com/api \
  --api-key ak_xxx \
  --api-secret sk_xxx
```

页面 URL 只能用来解析 `teamId / projectId / sheetId / viewId`，不能用来换 token，也不能替代 `dimens-cli auth api-key-login`。

## 2. 为什么 URL 不能替代登录

用户常给这类链接：

```text
https://dimens.bintelai.com/#/TEAM_ID/PROJECT_ID/SHEET_ID?view=VIEW_ID
```

这个链接只能提供资源上下文：

| 链接片段 | 作用 |
| --- | --- |
| `TEAM_ID` | 团队上下文 |
| `PROJECT_ID` | 项目上下文 |
| `SHEET_ID` | 菜单资源、表格、画布或文档页面入口 |
| `VIEW_ID` | 表格视图上下文 |

它不能提供：

- `token`
- `refreshToken`
- 用户身份
- API Key / Secret
- 资源权限

因此，任何需要调用 `project/sheet/row/doc/report/canvas/role/permission/workflow` 的真实命令，都必须先有登录态。

## 3. 标准认证链路

### 3.1 API Key 登录

默认命令：

```bash
dimens-cli auth api-key-login \
  --base-url https://dimens.bintelai.com/api \
  --api-key ak_xxx \
  --api-secret sk_xxx
```

如果用户已经配置默认 `baseUrl`，也可以：

```bash
dimens-cli auth api-key-login \
  --api-key ak_xxx \
  --api-secret sk_xxx
```

成功后 CLI 会把返回的 `token` 写入本地 profile，后续命令默认复用。

### 3.2 确认团队上下文

登录成功后，如果用户提供了 `teamId`，建议显式切换：

```bash
dimens-cli auth use-team TEAM_ID
```

然后确认项目列表或目标项目：

```bash
dimens-cli project list --team-id TEAM_ID
```

如果用户提供的是项目链接，先从链接解析 `TEAM_ID / PROJECT_ID`，再使用命令确认：

```bash
dimens-cli project info \
  --team-id TEAM_ID \
  --project-id PROJECT_ID
```

## 4. 场景前置要求

| 场景 | 是否必须认证 | 原因 |
| --- | --- | --- |
| 场景 0：项目梳理 | 是 | 需要读取项目、菜单、表、文档、报表、权限等资源 |
| 场景 1：新建项目 | 是 | 需要创建项目、目录、表格、文档、报表、画布、角色和权限 |
| 场景 2：修改项目内数据 | 是 | 需要读取当前数据、版本、字段 ID，再提交更新 |
| 场景 3：查询 | 是 | 需要访问 `/app/*` 资源接口 |
| 场景 4：分类路由 | 仅方案可不认证；执行必须认证 | 纯方案可先分类，真实命令必须先登录 |

一句话规则：

```text
只做方案可以先不登录；只要要读、建、改、删、查项目资源，就必须先 auth api-key-login。
```

## 5. 总控执行顺序

系统总控处理执行类任务时，默认顺序改为：

```text
1. 判断任务场景
2. 判断是否只是方案，还是要真实执行
3. 如果要真实执行，先执行 auth api-key-login
4. 解析 URL 或用户输入中的 teamId/projectId/sheetId/viewId
5. auth use-team TEAM_ID
6. project info / project list 确认上下文
7. 进入 project/table/doc/report/canvas/permission/workflow 等章节
8. 执行后回查
```

## 6. 用户只给 URL 时的处理方式

用户只给 URL 时，总控不能把 URL 当认证凭据。

推荐回复口径：

```text
这个 URL 可以解析出 teamId/projectId/sheetId/viewId，但不能换 token。
如果要我执行查询、创建或修改，需要先用 API Key / API Secret 登录：

dimens-cli auth api-key-login \
  --base-url https://dimens.bintelai.com/api \
  --api-key ak_xxx \
  --api-secret sk_xxx

登录成功后，我再用 URL 里的 teamId/projectId 进入目标资源。
```

## 7. 登录成功不等于有业务权限

`api-key-login` 成功只代表认证成功。它不代表：

- 用户一定属于目标团队
- 用户一定能进入目标项目
- 用户一定能看目标表、文档、报表或画布
- 用户一定能修改目标数据
- 用户一定能创建角色、权限或工作流

API Key 登录返回的是绑定用户的 token，后续权限仍然继承该用户本身的团队、项目、表、列、行、资源权限。

如果登录成功但命令访问失败，应继续检查：

1. 当前 token 绑定用户是否在目标团队。
2. 用户是否能进入目标项目。
3. 用户是否有表格、文档、报表、画布资源权限。
4. 是否被行级策略、列级权限或资源权限收窄。
5. 是否存在协同权限快照未刷新的情况。

## 8. 不同场景的认证提示模板

### 8.1 新建项目

```text
新建项目需要先完成 CLI 登录。
请使用 API Key / API Secret 换 token：

dimens-cli auth api-key-login \
  --base-url https://dimens.bintelai.com/api \
  --api-key ak_xxx \
  --api-secret sk_xxx

登录后再创建项目、目录、表格、文档、报表、画布和权限。
```

### 8.2 修改项目内数据

```text
修改项目内数据必须先登录并读取当前数据。
URL 只能解析目标资源，不能提供 token。
先执行 auth api-key-login，然后我会按“读取当前数据 -> 修改目标字段 -> 提交更新 -> 回查”的链路执行。
```

### 8.3 查询项目

```text
查询项目资源需要 token。
如果你只提供 URL，我可以解析 teamId/projectId/sheetId/viewId，但不能直接查询数据。
请先使用 auth api-key-login 完成登录。
```

### 8.4 项目梳理

```text
项目梳理需要读取菜单树、表结构、文档、报表、画布和权限。
这些都依赖登录态，先用 API Key / Secret 登录，再按 URL 或 projectId 进入项目梳理。
```

## 9. 高风险错误

| 错误 | 后果 | 修正 |
| --- | --- | --- |
| 把 URL 当 token | 命令无法认证，或误以为能直接访问资源 | URL 只解析上下文，token 必须通过 `auth api-key-login` 获取 |
| 只解析 `teamId/projectId` 就执行命令 | 缺少登录态，接口会失败 | 先登录，再确认上下文 |
| 登录成功后直接声明可操作全部资源 | 权限判断错误 | 继续验证用户对目标团队、项目和资源的权限 |
| 让用户从浏览器复制 token | 不稳定且有安全风险 | 使用 API Key / Secret 通过 CLI 换 token |
| 把 API Key 当独立权限体系 | 越权理解 | Key 只换绑定用户 token，权限继承绑定用户 |

## 10. 下一跳文档

- `dimens-manager/references/key-auth/overview.md`
- `dimens-manager/references/key-auth/references/login-flow.md`
- `dimens-manager/references/team/overview.md`
- `references/command-mapping.md`
