# 系统搭建命令映射

## 1. 使用目的

这份文档把“系统级搭建步骤”直接映射到可执行命令或接口，避免总控 Skill 只停留在路由建议，导致 AI 还要自己继续摸索具体参数。

## 2. 执行前检查

### 2.1 先完成认证

系统搭建、项目梳理、查询和修改都不能只靠维表页面 URL。URL 只能解析 `teamId/projectId/sheetId/viewId`，不能获取 token。

推荐优先使用：

```bash
dimens-cli auth api-key-login \
  --base-url https://dimens.bintelai.com/api \
  --api-key ak_xxx \
  --api-secret sk_xxx
```

登录成功后，本地 profile 会保存 token，后续 `project/sheet/row/doc/report/canvas/permission/workflow` 命令才有认证上下文。

如果还不清楚认证边界，先进入 `dimens-manager/references/key-auth/overview.md`，再看：

- `dimens-manager/references/key-auth/references/login-flow.md`
- `dimens-manager/references/key-auth/references/examples.md`

### 2.2 再确认上下文

```bash
dimens-cli auth use-team TEAM_ID
dimens-cli project list --team-id TEAM_ID
```

如果用户直接给的是维表链接，例如：

```text
https://dimens.bintelai.com/#/TTFFEN/PXWXBJQ/
```

默认直接解析为：

- `TEAM_ID = TTFFEN`
- `PROJECT_ID = PXWXBJQ`

后续命令直接代入即可，不要再把链接当普通描述文本丢掉。

## 3. 系统搭建步骤 → 命令

| 系统搭建步骤 | 优先命令 | 说明 |
| --- | --- | --- |
| 确认团队与项目上下文 | `dimens-cli project list --team-id TEAM_ID` | 系统建设前先确认项目归属 |
| 创建项目 | `dimens-cli project create --team-id TEAM_ID --name 项目名 [--description 描述] [--project-type spreadsheet]` | 从 `dimens-manager/references/project/overview.md` 主链进入，所有表都挂在项目下 |
| 查看项目详情 | `dimens-cli project info --team-id TEAM_ID --project-id PROJECT_ID` | 校验上下文是否正确 |
| 上传 SVG 封面/图标 | `dimens-cli upload file --path ./project-cover.svg --team-id TEAM_ID --scene project-cover` | SVG 默认 `250x150px`、淡色背景、轻量动态效果；文件名必须保留 `.svg`，CLI 会按 `image/svg+xml` 上传，上传后再把 URL 写回项目或文档；如果希望同时进入素材管理，再补 `--source material` |
| 创建目录 | `dimens-cli sheet create --team-id TEAM_ID --project-id PROJECT_ID --name 目录名 --type folder` | 只创建目录节点，不会自动移动其他菜单 |
| 创建工作表 | `dimens-cli sheet create --team-id TEAM_ID --project-id PROJECT_ID --name 表名 [--folder-id FOLDER_SHEET_ID]` | 新系统一般先建核心表；要进入目录必须显式带 `--folder-id` |
| 移动已有菜单资源到目录 | `dimens-cli sheet update SHEET_OR_REPORT_ID --team-id TEAM_ID --project-id PROJECT_ID --folder-id FOLDER_SHEET_ID` | 已创建的表格/报表等资源不会因目录创建自动归位，必须单独移动 |
| 创建在线文档 | `dimens-cli doc create --team-id TEAM_ID --project-id PROJECT_ID --title 文档名 [--content <html>] [--format richtext]` | 在线文档走 TipTap 富文本链路 |
| 获取在线文档详情 | `dimens-cli doc info --team-id TEAM_ID --project-id PROJECT_ID --document-id DOCUMENT_ID` | 回查文档是否创建成功，或读取当前文档详情 |
| 更新在线文档 | `dimens-cli doc update --team-id TEAM_ID --project-id PROJECT_ID --document-id DOCUMENT_ID --content '<p>新内容</p>' --version 1 [--create-version true] [--change-summary 说明]` | TipTap 在线文档修改走这里，必须显式带版本号 |
| 删除在线文档 | `dimens-cli doc delete --team-id TEAM_ID --project-id PROJECT_ID --document-id DOCUMENT_ID` | 清理误建或废弃文档资源 |
| 查看文档版本列表 | `dimens-cli doc versions --team-id TEAM_ID --project-id PROJECT_ID --document-id DOCUMENT_ID [--page 1] [--size 20]` | 回查历史版本元数据列表 |
| 查看指定文档版本 | `dimens-cli doc version --team-id TEAM_ID --project-id PROJECT_ID --document-id DOCUMENT_ID --version 3` | 读取指定历史版本内容 |
| 恢复文档到指定版本 | `dimens-cli doc restore --team-id TEAM_ID --project-id PROJECT_ID --document-id DOCUMENT_ID --version 3` | 用于错误覆盖后的版本回滚，并生成新的当前版本 |
| 创建报表 | `dimens-cli report create --project-id PROJECT_ID --name 报表名 [--description 描述]` | 报表属于项目菜单资源；底层创建 `type=report` 的 sheet，返回 `reportId=sheetId`，适合经营看板和统计分析 |
| 查看表详情 | `dimens-cli sheet info --team-id TEAM_ID --project-id PROJECT_ID --sheet-id SHEET_ID` | 校验表结构 |
| 查看报表列表 | `dimens-cli report list --project-id PROJECT_ID` | 校验报表主资源是否已落地 |
| 查询报表数据 | `dimens-cli report query --project-id PROJECT_ID --report-id REPORT_ID [--params <json>]` | 用于验证报表查询链路 |
| 查看视图列表 | `dimens-cli view list --team-id TEAM_ID --project-id PROJECT_ID --sheet-id SHEET_ID` | 建表后先确认默认视图是否已存在 |
| 创建公开默认视图 | `dimens-cli view create --team-id TEAM_ID --project-id PROJECT_ID --sheet-id SHEET_ID --name 默认视图 --type grid --is-public true --config '{"filters":[],"filterMatchType":"and","sortRule":null,"groupBy":[],"hiddenColumnIds":[],"rowHeight":"medium"}'` | 技能建表链路默认要求至少补一个公开默认视图 |
| 查看字段列表 | `dimens-cli column list --team-id TEAM_ID --project-id PROJECT_ID --sheet-id SHEET_ID` | 写入行数据前必须先取字段 |
| 创建字段 | `dimens-cli column create --team-id TEAM_ID --project-id PROJECT_ID --sheet-id SHEET_ID --label 字段名 --type text` | 推荐统一使用 `--label`；`select/multiSelect` 必须同步传 `--options`；如果语义是选人或选部门，优先改配 `person` / `department`，不要误落成普通下拉 |
| 创建行 | `dimens-cli row create --sheet-id SHEET_ID --values '{\"fld_xxx\":\"值\"}'` | CLI 会映射到服务端 `data` |
| 批量创建行 | `dimens-cli row batch-create --sheet-id SHEET_ID --file ./rows.json [--batch-size 200]` | 系统初始化、迁移、批量补数据优先用这个命令；后端单批最高 1000 行，但真实导入默认按 200 行稳定分片 |
| 更新行 | `dimens-cli row update --sheet-id SHEET_ID --row-id ROW_ID --version 1 --values '{\"fld_xxx\":\"新值\"}'` | 更新前要拿到版本号 |
| 更新单元格 | `dimens-cli row set-cell --sheet-id SHEET_ID --row-id ROW_ID --field-id FIELD_ID --value 新值 --version 1` | 推荐用 `fieldId`，不要用中文字段名 |
| 查询行数据 | `dimens-cli row page --team-id TEAM_ID --project-id PROJECT_ID --sheet-id SHEET_ID --page 1 --size 20` | 验证表是否可用 |

## 3.1 系统搭建进入角色 / 项目权限落地

当用户在系统搭建阶段直接提出下面这些需求时：

- 需要设计角色
- 需要做项目权限或表权限
- 需要区分谁看自己、谁看部门、谁看全部
- 需要公开访问或外部协同
- 需要限制协同编辑或资源可见范围

总控 Skill 不应只停留在“可选扩展”，而应直接把路由切到 `dimens-manager/references/permission/overview.md`，并给出下面这条命令主链：

| 系统搭建权限步骤 | 优先命令 | 下一跳 reference |
| --- | --- | --- |
| 创建角色 | `dimens-cli role create --app-url https://dimens.bintelai.com/#/TEAM_ID/PROJECT_ID/ --name 角色名 --description 说明 --can-manage-sheets false --can-edit-schema false --can-edit-data true` | `dimens-manager/references/permission/references/command-mapping.md` |
| 给用户绑定项目角色 | `dimens-cli role assign-user --app-url https://dimens.bintelai.com/#/TEAM_ID/PROJECT_ID/ --role-id ROLE_ID --user-id USER_ID` | `dimens-manager/references/permission/references/command-mapping.md` |
| 给用户绑定表级角色 | `dimens-cli role assign-user --app-url https://dimens.bintelai.com/#/TEAM_ID/PROJECT_ID/ --role-id ROLE_ID --user-id USER_ID --sheet-id SHEET_ID` | `dimens-manager/references/permission/references/command-mapping.md` |
| 创建项目 / 表权限 | `dimens-cli permission create --app-url https://dimens.bintelai.com/#/TEAM_ID/PROJECT_ID/ --role-id ROLE_ID --sheet-id SHEET_ID --data-access private_rw --can-read true --can-write true` | `dimens-manager/references/permission/references/command-mapping.md` |
| 设置资源权限 | `dimens-cli permission set-resource --app-url https://dimens.bintelai.com/#/TEAM_ID/PROJECT_ID/ --role-id ROLE_ID --resource-id RESOURCE_ID --resource-type document --visible true --editable false` | `dimens-manager/references/permission/references/command-mapping.md` |
| 增加行级策略 | `dimens-cli row-policy create --app-url https://dimens.bintelai.com/#/TEAM_ID/PROJECT_ID/ --sheet-id SHEET_ID --role-id ROLE_ID --name 策略名 --effect allow --actions view --conditions '[{\"columnId\":\"createdBy\",\"operator\":\"equals\",\"value\":\"{{currentUser}}\"}]' --priority 10 --match-type and --active true` | `dimens-manager/references/permission/references/command-mapping.md` |

补充说明：

- 系统搭建落权限时，默认主链是 `role create -> permission create -> role assign-user -> row-policy create`
- `permission set-resource` 用于文档、报表、页面等资源，不替代表/列/行权限
- 更完整的参数案例继续看 `dimens-manager/references/key-auth/references/examples.md`
- 更严格的判断边界继续看 `dimens-manager/references/permission/references/matrix.md`

## 4. CRM 最小可执行链路

### 4.1 创建项目

```bash
dimens-cli upload file \
  --path ./project-cover.svg \
  --team-id TEAM_ID \
  --scene project-cover \
  --source material

dimens-cli project create \
  --team-id TEAM_ID \
  --name 客户管理系统 \
  --description 客户全生命周期管理 \
  --project-type spreadsheet

dimens-cli project info --team-id TEAM_ID --project-id PROJECT_ID
```

`project-cover.svg` 生成要求：`width="250" height="150" viewBox="0 0 250 150"`，淡色背景，使用轻量 `animate` / `animateTransform` 做动态效果，视觉元素与项目主题一致。

如果项目创建后才拿到封面 URL，必须按 `project info -> project update` 写回 URL；不要把“上传成功”当成“项目封面已生效”。

### 4.2 创建客户表

```bash
dimens-cli sheet create --team-id TEAM_ID --project-id PROJECT_ID --name 客户中心 --type folder

dimens-cli sheet create --team-id TEAM_ID --project-id PROJECT_ID --name 客户表 --folder-id FOLDER_CUSTOMER_ID

dimens-cli sheet tree --team-id TEAM_ID --project-id PROJECT_ID
```

`sheet tree` 必须能看到 `客户表` 位于 `客户中心` 目录下，否则还要执行：

```bash
dimens-cli sheet update SHEET_ID \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --folder-id FOLDER_CUSTOMER_ID
```

### 4.3 创建字段

```bash
dimens-cli column create \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --sheet-id SHEET_ID \
  --label 客户名称 \
  --type text
```

```bash
dimens-cli column create \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --sheet-id SHEET_ID \
  --label 客户等级 \
  --type select
```

补充：

- `select`、`multiSelect` 等字段在技能链路里必须直接补齐选项值，不要只创空字段
- 系统初始化不要只考虑表格，默认还要同时判断是否需要在线文档和报表
- 在线文档走文档主链 `doc create / doc info / doc update / doc delete`，报表走 `report create`；这两类资源都不要误建成普通表
- 创建目录后必须用 `sheet tree` 验证归位；没有看到子资源在目录下，就不能说菜单整理完成
- 上传 SVG 后必须确认 URL 已写回项目封面/图标或文档内容；只上传不写回不算完成
- 如果用户提到历史版本、回滚恢复、旧内容比对，在线文档继续走版本主链 `doc versions / doc version / doc restore`
- 如果项目本身已经有用户体系、部门体系、内置角色，而字段需求本质是“负责人 / 成员 / 处理人 / 审批人”这类人员选择，则优先使用 `person`
- 如果字段需求本质是“所属部门 / 负责部门 / 发起部门 / 归属组织”这类组织选择，则优先使用 `department`
- 人员字段、部门字段和普通下拉字段都属于特殊情况，不能只看“UI 像下拉”就统一建成 `select`
- 推荐写法示例：

```bash
dimens-cli column create \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --sheet-id SHEET_ID \
  --label 客户等级 \
  --type select \
  --options '[{"label":"A 级客户","color":"bg-blue-100 text-blue-700"},{"label":"B 级客户","color":"bg-slate-100 text-slate-700"}]'
```

- relation 字段目前 CLI 只支持基础参数透传，复杂 `relationConfig.displayColumnId / bidirectional` 仍应优先参考 API 结构与 `dimens-manager/references/table/references/field-design-patterns.md`
- 如需确认字段结构，优先回看 `dimens-manager/references/table/references/field-design-patterns.md`
- `--options` 推荐传 JSON 数组对象，以便一次补齐颜色等展示配置；逗号分隔字符串仅兼容基础场景
- 如果遇到“人员下拉”或“部门下拉”这类说法，先判断业务语义，不要直接套用 `--options`

### 4.4 先补默认公开视图，再继续

```bash
dimens-cli view list \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --sheet-id SHEET_ID
```

如果还没有公开默认视图：

```bash
dimens-cli view create \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --sheet-id SHEET_ID \
  --name 默认视图 \
  --type grid \
  --is-public true \
  --config '{"filters":[],"filterMatchType":"and","sortRule":null,"groupBy":[],"hiddenColumnIds":[],"rowHeight":"medium"}'
```

### 4.5 先查字段，再写行

```bash
dimens-cli column list \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --sheet-id SHEET_ID
```

### 4.6 用 fieldId 写入行

```bash
dimens-cli row create \
  --sheet-id SHEET_ID \
  --values '{"fld_customerName":"华东智造","fld_customerLevel":"A"}'
```

批量初始化示例数据时，不要循环执行单行 `row create`，应写入 JSON 文件后走批量命令：

```bash
dimens-cli row batch-create \
  --sheet-id SHEET_ID \
  --file ./data/customers.json \
  --batch-size 200
```

说明：

- `customers.json` 顶层必须是数组，每一项可以是 `{ "fld_xxx": "值" }` 或 `{ "data": { "fld_xxx": "值" } }`。
- 后端单批最多 1000 行；CLI 会按 `--batch-size` 自动分片，默认使用 200 行。不要为了减少请求数改成 1000 行，真实导入中 1000 行分片存在静默丢数据风险。
- 多批导入时只保证每个后端分片事务原子，不保证整个文件全局事务。

## 5. 必须显式提醒的坑

| 坑点 | 正确做法 |
| --- | --- |
| 没登录就直接跑表格命令 | 先执行 `auth api-key-login` 或其他认证链路 |
| 创建字段还用 `--title` 当规范写法 | 现在兼容，但推荐统一改成 `--label` |
| 建表后没检查默认视图 | 先 `view list`，缺失时补一个公开的 `grid` 默认视图 |
| `select` / `multiSelect` 只建字段不配选项 | 创建字段时直接补 `--options`，不要留空配置；Excel 导入前必须先从表头/样本值提取候选项并创建选项 |
| 把人员字段误建成普通下拉 | 没识别项目已有用户、部门、角色体系，误把“选人”当静态枚举 | 优先改成 `person`，不要手工维护人员选项 |
| 把部门字段误建成普通下拉 | 没识别组织结构字段和静态枚举字段的区别 | 优先改成 `department`，不要手工维护部门选项 |
| relation 字段创建显示成功但没真正落库 | 当前复杂 relation 仍需按 API 的 `relationConfig` 校验，不要只看 CLI 成功提示 |
| 行写入直接用中文字段名 | 先查字段列表，拿 `fieldId` 再写 |
| 批量导入还循环调用 `row create` | 使用 `row batch-create --file`，让 CLI 默认按 200 行稳定分片，减少 HTTP 和数据库压力 |
| Excel 里的下拉值直接原样写入 | 先确认字段真实 `options`，写入值必须映射到已有选项的 `label` 或 `id`；缺失选项先更新字段选项，不能写表里不存在的下拉值 |
| `row set-cell` 继续用 `columnId` 理解服务端 | 服务端真实字段是 `fieldId`，`columnId` 只是兼容参数 |
| 忽略 `version` | 行更新和单元格更新都建议显式带 `version` |
