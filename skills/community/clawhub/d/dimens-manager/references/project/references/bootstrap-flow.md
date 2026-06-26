# 项目初始化端到端链路

## 1. 目标

把下面这条链路收成用户可直接执行的初始化顺序：

1. 创建项目
2. 看需求补 SVG 动态封面
3. 创建项目菜单目录
4. 创建多表格
5. 创建多字段
6. 设计 `1 对多 / 多对一` 关联数据
7. 补案例数据
8. 看需求补项目文档
9. 看需求补项目报表
10. 看需求补角色
11. 看需求补权限

## 2. 推荐顺序

在执行命令前，默认先按维表特性把下面几件事设计清楚：

- 需要几张核心表
- 每张表的核心字段是什么
- 哪些表之间存在 `1 对多 / 多对一` 关系
- 准备写入哪些案例数据
- 是否需要文档、报表、角色、权限这些后置模块
- 是否需要先生成一个符合项目主题、具备动态动画效果的 SVG 封面
- 是否需要先规划项目菜单目录，以及目录下要挂哪些表格/文档/报表资源

### 2.1 创建项目

```bash
dimens-cli project create \
  --team-id TEAM_ID \
  --name 客户管理系统 \
  --description 客户全生命周期管理 \
  --project-type spreadsheet
```

补充建议：

- 如果项目强调品牌感、对外展示、模板销售、知识库入口或市场封面，建议在执行 `project create` 之前先补一张 SVG 封面
- 这张封面建议由 SVG 工具生成，要求：
  - 符合项目主题
  - 固定 `250x150px`，建议写入 `width="250" height="150" viewBox="0 0 250 150"`
  - 使用淡色背景，例如浅蓝、浅紫、浅绿、浅橙或浅灰渐变
  - 有轻量动态动画效果，例如慢速漂浮、淡入淡出、轻微位移或渐变流动
  - 避免快速闪烁、高饱和强对比和复杂大面积动画
  - 可直接作为项目封面图使用
- 封面处理链路建议固定为：
  1. SVG 工具生成封面
  2. `dimens-cli upload file --file ./project-cover.svg`
  3. 拿到上传返回的 URL
  4. 再进入项目创建流程

### 2.1.1 创建项目菜单目录

项目创建完成后，不要只开始堆资源，建议先把项目菜单目录规划出来。

默认至少考虑下面 4 类菜单节点：

1. 目录 `folder`
2. 表格 `sheet`
3. 文档 `document`
4. 报表 `report`

推荐做法：

- 先按业务域规划目录，例如：
  - 客户中心
  - 经营分析
  - 项目文档
- 再把表格、文档、报表分别挂到对应目录下
- 创建完成后，用下面命令回查菜单树：

```bash
dimens-cli sheet tree --project-id PROJECT_ID
```

说明：

- 目录功能不是可有可无的 UI 装饰，而是项目菜单分层能力的一部分
- 如果项目里会同时出现多张表、多份文档、多份报表，建议优先先建目录
- 当前 CLI 已有 `sheet tree`，可用于回查项目菜单树是否完整

### 2.2 创建多张核心表

```bash
dimens-cli sheet create --team-id TEAM_ID --project-id PROJECT_ID --name 客户表
dimens-cli sheet create --team-id TEAM_ID --project-id PROJECT_ID --name 联系人表
```

### 2.3 创建多字段

```bash
dimens-cli column create --team-id TEAM_ID --project-id PROJECT_ID --sheet-id CUSTOMER_SHEET_ID --label 客户名称 --type text
dimens-cli column create --team-id TEAM_ID --project-id PROJECT_ID --sheet-id CUSTOMER_SHEET_ID --label 客户等级 --type select --options '[{"id":"customer-level-a","label":"A级","color":"bg-blue-100 text-blue-700"},{"id":"customer-level-b","label":"B级","color":"bg-slate-100 text-slate-700"},{"id":"customer-level-c","label":"C级","color":"bg-amber-100 text-amber-700"}]'
```

说明：

- 普通下拉字段推荐直接传 JSON 数组选项，显式补齐 `id / label / color`
- 同一个字段下每个选项 `id` 必须唯一，不能重复
- 人员字段、部门字段属于特殊情况，不要退化成普通下拉
- 当项目本身已有用户体系、部门体系和内置角色体系时，人员下拉优先直接配置为人员字段，部门下拉优先直接配置为部门字段

### 2.4 创建 `1 对多 / 多对一` 关联字段

```bash
dimens-cli column create \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --sheet-id CONTACT_SHEET_ID \
  --label 所属客户 \
  --type relation \
  --target-sheet-id CUSTOMER_SHEET_ID \
  --display-column-id CUSTOMER_NAME_FIELD_ID
```

说明：

- 联系人表到客户表通常是“多对一”
- 从客户视角回看联系人通常是“一对多”
- 这类关系字段应建立在多表和主显示字段都已明确的前提下

### 2.5 补案例数据

在字段和关联关系落好以后，默认继续准备并写入案例数据，用于验证：

- 表结构是否合理
- 关联关系是否能正确回查
- 后续文档描述和报表统计是否有可用样例

### 2.6 看需求创建第一份在线文档

如果项目需要文档说明页、知识沉淀页、协作文档，而不是先建表，可以直接创建在线文档：

```bash
dimens-cli doc create \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --title 产品说明文档 \
  --content '<p>欢迎使用在线文档</p>' \
  --format richtext
```

说明：

- 当前在线文档编辑器走 TipTap 富文本链路
- 这种场景不要误用 `sheet create` 代替文档创建
- 如果是文档型项目，建议先补 `doc create`，再决定是否继续建表
- 文档资源不是一次性资源，创建后默认还要继续支持查询、修改、删除

### 2.6.1 文档闭环维护

文档创建成功后，推荐继续掌握下面这条文档主链：

```bash
dimens-cli doc info \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --document-id DOC_ID

dimens-cli doc info \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --sheet-id sh_xxx

dimens-cli doc update \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --document-id DOC_ID \
  --content '<p>更新后的在线文档</p>' \
  --version 1 \
  --create-version true \
  --change-summary 补充说明

dimens-cli doc delete \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --document-id DOC_ID
```

说明：

- `doc info` 用于回查文档详情，确认文档是否创建成功、当前版本是多少
- 如果输入来自浏览器文档链接，URL 里通常拿到的是 `sheetId=sh_xxx` 这一层菜单资源 ID，不是 `documentId=doc_xxx`；这时先用 `doc info --sheet-id sh_xxx` 拿文档详情，再继续更新
- `doc update` 用于修订 TipTap 在线文档内容，必须显式带 `version`
- `doc delete` 用于清理误建或废弃的文档资源
- 如果项目是文档型项目，不要停在 `doc create`，而要把 `info/update` 一起视作默认维护链路

### 2.6.2 文档版本管理

如果在线文档承担制度页、说明页、知识沉淀页，建议继续掌握版本链：

```bash
dimens-cli doc versions \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --document-id DOC_ID \
  --page 1 \
  --size 20

dimens-cli doc version \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --document-id DOC_ID \
  --version 3

dimens-cli doc restore \
  --team-id TEAM_ID \
  --project-id PROJECT_ID \
  --document-id DOC_ID \
  --version 3
```

说明：

- `doc versions` 用于查看版本元数据列表
- `doc version` 用于查看指定历史版本正文
- `doc restore` 用于恢复到指定历史版本，并生成新的当前版本
- 不要在误修改后直接继续 `doc update` 覆盖当前内容；先看版本链，再决定是否恢复

### 2.7 检查并补默认公开视图

```bash
dimens-cli view list --team-id TEAM_ID --project-id PROJECT_ID --sheet-id SHEET_ID
```

如果缺失：

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

### 2.8 看需求创建报表

如果项目还需要经营看板、统计分析或仪表盘，建议继续走报表固定预检链：

1. `dimens-cli report create`
2. `dimens-cli report preview`
3. `dimens-cli report widget-add`
4. `dimens-cli report query-widget`
5. `dimens-cli report query`

### 2.8.1 菜单层回查

资源创建完成后，建议再回查一次项目菜单树：

```bash
dimens-cli sheet tree --project-id PROJECT_ID
```

重点确认：

- 是否已经存在目录节点
- 表格是否归到正确目录
- 文档是否归到正确目录
- 报表是否归到正确目录

### 2.9 创建角色并配置项目权限

权限主链推荐直接沿用 `dimens-manager/references/permission/references/command-mapping.md` 的 `--app-url` 写法，这样其他产品接技能时不需要先拆上下文。

```bash
dimens-cli role create \
  --app-url https://dimens.bintelai.com/#/TEAM_ID/PROJECT_ID/ \
  --name 销售 \
  --description CRM 销售角色 \
  --can-manage-sheets false \
  --can-edit-schema false \
  --can-edit-data true

dimens-cli permission create \
  --app-url https://dimens.bintelai.com/#/TEAM_ID/PROJECT_ID/ \
  --role-id ROLE_ID \
  --sheet-id SHEET_ID \
  --data-access private_rw \
  --can-read true \
  --can-write true
```

### 2.10 给用户分配角色

```bash
dimens-cli role assign-user \
  --app-url https://dimens.bintelai.com/#/TEAM_ID/PROJECT_ID/ \
  --role-id ROLE_ID \
  --user-id USER_ID
```

## 3. 什么时候继续跳转其他 Skill

| 下一步需求 | 跳转 Skill |
| --- | --- |
| 字段细节、relation 模式、筛选案例 | `dimens-manager/references/table/overview.md` |
| 角色、项目权限、行级策略 | `dimens-manager/references/permission/overview.md` |
| teamId、成员、上下文来源 | `dimens-manager/references/team/overview.md` |
| 系统级整体拆解 | `dimens-system-orchestrator` |
