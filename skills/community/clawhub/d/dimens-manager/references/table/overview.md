---
name: dimens-manager-table
slug: dimens-manager-table
description: 用于维表智联工作表、字段、视图、行数据、relation 和查询链路设计与排查。
version: 1.0.0
author: 方块智联工作室
tags: [table, sheet, row, column, view, dimens-cli]
---

# dimens-manager 多维表格章节

适用产品：

- 产品名称：`维表智联`
- 开发方：`方块智联工作室`
- 官网：[https://dimens.bintelai.com/](https://dimens.bintelai.com/)

## 执行前必读

- ✅ 执行任何 `project / sheet / column / row / ai` 命令前，先完成认证；认证方式优先参考 `dimens-manager/references/key-auth/overview.md`
- ✅ 表格能力默认要先确认 `projectId`，大多数写操作还需要 `teamId`
- ✅ 如果用户还处在“创建项目 / 初始化项目”阶段，先路由到 `dimens-manager/references/project/overview.md`，不要在 `dimens-manager/references/table/overview.md` 里直接吞掉上游步骤
- ✅ 字段、视图、行数据都属于工作表上下文，不能脱离 `sheetId` 单独判断
- ✅ 默认要优先帮助用户把“项目 -> 表 -> 字段 -> 关联 -> 示例数据 -> 查询案例”搭起来
- ✅ 字段设计必须细到可落地，不能只写“有客户名称、状态、时间”这种抽象描述
- ✅ relation 字段创建必须补齐目标表，推荐显式传 `--target-sheet-id`，并尽量补 `--display-column-id`
- ✅ `select` / `multiSelect` 字段在技能创建时必须同时给出完整候选项，不能只定义字段名和类型
- ✅ `select` / `multiSelect` / 下拉选择类配置在技能输出时必须同时给出候选项颜色策略：默认颜色还是自定义颜色，不能只给 `label`
- ✅ 用户上传 Excel 并要求创建选择器字段时，必须先从 Excel 表头和样本值提取候选项，用 `column create --options` 创建完整下拉；行数据写入必须映射到这些候选项，不能把不存在的下拉值直接写入
- ✅ 选项颜色字符串要与前端真实实现对齐：内置颜色使用 `bg-xxx-100 text-xxx-700`，自定义颜色使用 `custom:{\"bg\":\"#xxxxxx\",\"text\":\"#xxxxxx\"}`
- ✅ 当前 `dimens-cli` 对字段选项颜色的内置白名单已与前端真实字段配置对齐为 12 色；如果超出这 12 种内置色，优先改用 `custom:{...}`，不要直接写扩展类名
- ✅ `select` / `multiSelect`、`person`、`department` 都属于特殊字段，不能只按普通文本字段理解
- ✅ 如果项目已经有自己的部门、内置角色和用户体系，且需求本质是“人员下拉 / 负责人选择 / 成员选择”，优先配置 `person` 字段，不要误建成普通下拉字段
- ✅ 如果需求本质是部门选择、部门归属、部门筛选，优先配置 `department` 字段，不要误建成普通下拉字段
- ✅ 新表落地后必须确认至少存在一个公开默认视图；如果技能链路没有自动补齐，就要显式执行 `view create`
- ✅ `row/page` 默认要按“基于字段的搜索、筛选、排序”来解释，不只是分页
- ✅ 系统视图相关问题要区分团队级默认字段和项目级实际分配字段
- ✅ 处理字段和行写入问题时，不能只看字段结构，还要同步看权限与系统字段边界
- ✅ 表格接口能读取不代表一定可写，行级、列级、协同权限可能继续收敛
- ✅ 如果后续要做报表，这一步就要提前考虑字段能否直接进入 `report preview / query-widget / dataMapping`，不要等到报表阶段再返工

## 高风险跑偏点

下面这些是 AI 在表格建模阶段最容易做错、但会直接影响后续报表成功率的地方：

1. 只设计字段名，不设计字段类型
2. 把本该用于统计的字段建成文本字段
3. 把人员、部门字段误建成普通 `select`
4. 认为 `select` 只要有字段名就行，忘记补候选项
5. 给了候选项，但没给颜色，导致前端标签风格不统一
6. 把前端支持的 `custom:` 自定义颜色写丢，导致技能输出只能覆盖一半能力
7. 建表时没考虑哪些字段后面要做报表维度、数值轴、筛选项
8. 只关心表能录数据，不关心字段是否可用于 `preview` 和报表映射

对应提醒：

- 报表维度字段通常需要稳定标签和可读值
- 报表数值字段必须是数字或可稳定转数字
- 如果字段后续要进入报表，尽量在建表阶段就明确“谁做维度、谁做指标”
- 不要等到 `dimens-manager/references/report/overview.md` 阶段才发现字段类型不适合出图

## 命令维护表

| 命令 | 作用 | 必填参数 | 常用可选 | 细节说明 |
| --- | --- | --- | --- | --- |
| `dimens-cli sheet list` | 查询项目下工作表列表 | `projectId` | `teamId` | 表入口通常先从项目进入，排查问题时建议显式补 `teamId` |
| `dimens-cli sheet info` | 获取工作表详情 | `teamId`, `projectId`, `sheetId` | - | 表更新前默认先读当前表数据，确认结构和归属 |
| `dimens-cli sheet create` | 创建表或目录节点 | `projectId`, `name` | `teamId`, `folder-id`, `type` | 新表落地后还要继续检查默认公开视图是否存在；要放入目录时必须显式传 `--folder-id` |
| `dimens-cli sheet update` | 更新表基础信息或移动菜单归属 | `projectId`, `sheetId` | `teamId`, `name`, `folder-id`, `app-url` | 默认先 `sheet info` 拿当前数据，再改字段后更新；已有资源移入目录用 `--folder-id` |
| `dimens-cli column list` | 查询字段列表 | `teamId`, `projectId`, `sheetId` | - | 用于先确认字段结构、字段类型和现有字段 ID |
| `dimens-cli column create` | 创建字段 | `teamId`, `projectId`, `sheetId`, `type`, `label` 或兼容参数 `title` | `property`, `uiType`, `config`, `required`, `unique`, `key`, `options` | `select/multiSelect` 必须补完整 `options`，颜色协议要和前端一致 |
| `dimens-cli column update` | 更新字段定义 | `teamId`, `projectId`, `sheetId`, `fieldId` | `label`, `title`, `type`, `config`, `required`, `unique`, `app-url` | 默认先拿当前表结构，从 `structure.columns` 找到目标字段后再合并更新 |
| `dimens-cli view list` | 查询视图列表 | `teamId`, `projectId`, `sheetId` | - | 建表后先确认默认公开视图是否已经落地 |
| `dimens-cli view create` | 创建公开默认视图或业务视图 | `teamId`, `projectId`, `sheetId`, `name`, `type` | `isPublic`, `config` | 技能建表链路默认要求至少补一个公开 grid 视图 |
| `dimens-cli row page` | 分页查询行数据，也是后续数据分析的核心取数入口 | `teamId`, `projectId`, `sheetId` | `viewId`, `page`, `size`, `keyword`, `search-field-ids`, `filters`, `filter-match-type`, `sort-rule` | 使用前必须先 `column list` 获取真实字段 ID，再按字段设计搜索、筛选、排序；行读取链路会同时受字段筛选、视图配置和权限影响 |
| `dimens-cli row create` | 新增单行数据 | `sheetId`, `values` | - | 写入前必须先通过 `column list` 确认真实 `fieldId`，CLI 会把 `--values` 映射成服务端 `data` |
| `dimens-cli row batch-create` | 批量新增行数据 | `sheetId`, `file` 或 `values` | `batch-size` | 推荐大批量初始化、迁移和补数据使用；CLI 默认按 200 行稳定分片，后端单批硬限制 1000 行且单批事务原子 |
| `dimens-cli row update` | 更新整行数据 | `teamId`, `projectId`, `sheetId`, `rowId` | `data`, `version`, `app-url` | 默认先读当前行数据，再修改目标字段，再 update；不要只凭局部字段直接覆盖 |
| `dimens-cli row set-cell` | 更新单个单元格 | `sheetId`, `rowId`, `fieldId`, `value` | `version`, `columnId` | 服务端真实契约以 `fieldId` 为准，写入时仍要注意版本和权限边界 |

### 强调细节

- 表、字段、行的更新类命令默认都按“拿数据 -> 改数据 -> 更新数据”执行，不能把局部 patch 当成稳定更新方式。
- `sheet update` 前默认先 `sheet info`；`column update` 前默认先取当前 `structure.columns`；`row update` 前默认先读取当前行数据。
- 涉及搜索、筛选、排序、统计分析、报表预检时，不能直接盲猜字段名调用 `row page`；必须先 `column list` 拿到字段 ID、字段类型、选项值，再组装 `search-field-ids`、`filters`、`sort-rule`。
- 初始化、迁移、补数据这类多行写入优先用 `row batch-create --file`，不要让技能循环调用 `row create` 逐条写入；CLI 默认按 200 行稳定分片，后端只保证每个分片事务原子。
- 如果字段后续要进入报表，建模阶段就要把字段类型、选项、数值字段和维度字段设计清楚，不要拖到报表阶段返工。
- 新建表后默认检查公开默认视图，不要只建表不补视图。
- 行写入和字段更新除了结构正确，还要同步考虑权限、协同链路和版本字段。

## 核心约束

### 1. 资源层级

- 表属于项目
- 字段、视图、行属于表
- 任何字段或行问题都应该先落到具体 `sheetId`

### 1.1 默认公开视图约束

- 技能侧建表完成后，默认要检查是否已经存在公开视图
- 如果没有，就补一个 `name=默认视图`、`type=grid`、`isPublic=true` 的公开默认视图
- 推荐 `config` 至少包含：`filters=[]`、`filterMatchType='and'`、`sortRule=null`、`groupBy=[]`、`hiddenColumnIds=[]`、`rowHeight='medium'`
- 没有默认公开视图时，前端常见表现是“表能打开但筛选能力不完整”或“没有可继承的视图配置”

### 2. 系统视图字段边界

- `flow_info.usageType` 表示团队级默认能力类型
- `mul_project_workflow_binding.systemView` 表示项目级实际系统视图分配
- 当前规则是“项目绑定优先，全局默认回退”

### 3. 字段与值结构边界

- 字段类型不同，值结构和允许写入方式不同
- 字段能力不能只看名字，必须结合类型、`uiType`、`property`
- 字段设计默认至少要明确：字段名、类型、是否必填、是否唯一、默认值、是否参与筛选、是否参与排序、是否用于主展示
- 如果字段类型是 `select` 或 `multiSelect`，还必须同步明确候选项列表；没有选项值就不是完整字段设计
- 如果字段类型是 `select` 或 `multiSelect`，每个候选项默认至少明确：`id`、`label`、`color`
- 如果数据来源是 Excel，创建 `select` / `multiSelect` 字段前必须先扫描该列实际值，把去重后的合法值转成候选项；后续 `row batch-create` 写入时只能写已有候选项对应的 `label` 或 `id`，发现新值要先补字段选项再导入
- 下拉候选项颜色必须区分两类：
  1. 内置默认颜色：使用前端内置的 Tailwind 类名组合
  2. 自定义颜色：使用 `custom:{\"bg\":\"#xxxxxx\",\"text\":\"#xxxxxx\"}` 字符串
- 当前前端真实颜色来源在多维表格字段配置与字典管理页，技能输出时不要自造颜色协议
- 如果字段语义是“选人”，且项目本身已有用户体系、部门体系、内置角色，则这不是普通 `select`，应优先落到 `person`
- 如果字段语义是“选部门 / 归属部门 / 所属组织”，则这不是普通 `select`，应优先落到 `department`
- 关联字段默认要明确：目标表、展示字段、是否多选、是否双向、编辑视图字段
- 涉及工作流、AI 分析、审批、自动化入口时，还要同时检查系统视图字段映射

### 3.1 报表联动边界

如果用户后续还要做报表，这里要提前提醒：

- 哪些字段会作为图表维度字段
- 哪些字段会作为数值字段
- 哪些字段会进入筛选和排序
- 哪些字段只是详情说明，不适合直接出图

默认建议：

| 报表用途 | 推荐字段类型 | 说明 |
| --- | --- | --- |
| 类目维度 | `text` / `select` / `date` / `department` / `person` | 用于横轴、分类、分组 |
| 数值指标 | `number` | 用于求和、排序、统计 |
| 详情说明 | `text` | 不要默认当 `valueKey` |
| 组织筛选 | `department` | 不要退化成普通 `select` |
| 人员筛选 | `person` | 不要退化成普通 `select` |

### 4. 权限边界

- 表级可见不代表列级可写
- 列级可写不代表行级可写
- 表格在协同链路里还会受到 Yjs 写入净化与广播过滤影响

### 5. 上下文边界

- CLI 场景通常同时依赖 `teamId`、`projectId`、`sheetId`
- 如果只给出其中一个，很多结论都不稳定

## 必查文档

| Skill / references | 作用 | 什么时候必须看 |
| --- | --- | --- |
| `dimens-manager/references/key-auth/overview.md` | 认证、token 复用与第三方接入边界 | 执行任何表格命令前必须先确认 |
| `dimens-manager/references/team/overview.md` | 团队与项目上下文来源 | 进入表域前必须先看 |
| `dimens-manager/references/project/overview.md` | 项目创建、默认公开视图补偿、建表前置链路 | 用户还没完成项目初始化时必须先看 |
| `dimens-manager/references/permission/overview.md` | 表级、列级、行级与协同权限边界 | 处理写入权限时建议看 |
| `dimens-manager/references/workflow/overview.md` | 系统视图字段与工作流入口的映射关系 | 处理 AI 分析、审批、自动化入口时建议看 |
| `dimens-manager/references/report/overview.md` | 报表组件、字段映射、固定预检链 | 字段后续要进入看板、图表、统计分析时必须看 |
| `references/field-design-patterns.md` | 字段设计模板、relation 结构 | 设计字段时必须看 |
| `references/field-option-colors.md` | 单选/多选/下拉选择器颜色体系、默认颜色、自定义颜色协议 | 处理选项字段时必须看 |
| `references/row-filters.md` | `row/page` 搜索、筛选、排序与 `viewId` 继承 | 设计查询案例时必须看 |
| `references/field-rules.md` | 字段规则和系统视图字段边界 | 处理系统字段时必须看 |
| `references/build-flow.md` | 表域能力落地流程 | 从零搭表时建议看 |
| `references/examples.md` | 表 / 字段 / 行接口案例 | 需要直接举例时看 |

## 使用场景示例

### 场景 0：用户要“做一个客户管理系统”

默认优先输出：

1. 项目名称
2. 核心表：客户、联系人、跟进记录、商机
3. 每张表的字段设计
4. 表之间的 relation 关系
5. 示例行数据
6. `row/page` 查询案例

补充：

- 如果项目还没创建或默认公开视图还没补齐，这一步应先回到 `dimens-manager/references/project/overview.md`
- 如果后续还要做报表，字段设计阶段就要明确哪些字段要做维度、哪些字段要做数值

只有用户继续要求时，再扩展权限、工作流、报表。

如果用户已经明确后面要做报表，不要把“报表”理解成后置可忽略项，至少在建表阶段补一句：

1. 哪些字段会做图表维度
2. 哪些字段会做统计指标
3. 哪些字段要支持后续 `report preview` 和 `dataMapping`

### 场景 1：查询某项目下的表列表

```bash
dimens-cli sheet list --project-id PROJ1
```

建议：

- 排查问题时尽量显式补 `--team-id`
- 避免被本地默认上下文误导

### 场景 1.1：为新表补公开默认视图

```bash
dimens-cli view create \
  --team-id TTFFEN \
  --project-id PUQUNFE \
  --sheet-id sh_customer \
  --name 默认视图 \
  --type grid \
  --is-public true \
  --config '{"filters":[],"filterMatchType":"and","sortRule":null,"groupBy":[],"hiddenColumnIds":[],"rowHeight":"medium"}'
```

注意：

- 这是技能建表链路里的默认补偿步骤，不要跳过
- 如果后端已经自动生成了默认视图，应先用 `view list` 检查，避免重复创建
- 当前 CLI 只承诺 `view list/create` 基础能力，不要把 `update/delete/config/filters` 当成已稳定封装

### 场景 2：更新单元格

```bash
dimens-cli row set-cell \
  --sheet-id SHEET1 \
  --row-id ROW1 \
  --field-id fld_status \
  --value 已完成
```

注意：

- 写入前要先确认字段类型和值结构
- `fieldId` 需要先通过 `dimens-cli column list` 获取，不能直接拿中文字段名当写入键
- 如果是系统字段、只读字段或命中行级策略，后端仍可能拒绝

### 场景 2.0：批量初始化行数据

推荐把示例数据、迁移数据或补录数据写入 JSON 文件，再批量导入：

```json
[
  { "fld_customerName": "华东智造", "fld_customerLevel": "A" },
  { "fld_customerName": "华南制造", "fld_customerLevel": "B" }
]
```

```bash
dimens-cli row batch-create \
  --sheet-id SHEET1 \
  --file ./data/customers.json
```

如果数据量超过 200 行，CLI 默认按 200 行稳定切分请求：

```bash
dimens-cli row batch-create \
  --sheet-id SHEET1 \
  --file ./data/customers.json \
  --batch-size 200
```

注意：

- 后端单次 `batch-create` 最高限制 1000 行。
- 真实导入不要使用 1000 行分片，已确认 1000 行存在静默丢数据风险；技能生成命令默认使用 200 行。
- CLI 多批导入时，每批在后端事务内原子提交；整个文件不是一个全局事务。
- 仍然必须使用真实 `fieldId` 写入，不要用中文字段名。
- `select` / `multiSelect` 字段写入前必须先回查字段 `options`，把 Excel 单元格值映射到已有候选项；字段没有下拉时先补 `--options`，不能先导入行数据。
- 写入会继续受表级、列级、行级权限影响，只读字段会被后端过滤或拒绝。

### 场景 2.1：设计带颜色的单选/多选字段

推荐候选项结构：

```json
[
  { "id": "opt_pending", "label": "待提交", "color": "bg-slate-100 text-slate-700" },
  { "id": "opt_submitting", "label": "提交中", "color": "bg-blue-100 text-blue-700" },
  { "id": "opt_submitted", "label": "已提交", "color": "bg-emerald-100 text-emerald-700" },
  { "id": "opt_rejected", "label": "已驳回", "color": "bg-rose-100 text-rose-700" }
]
```

补充要求：

- 默认颜色优先使用前端内置颜色池，不要先上自定义色
- 如果业务已有明确品牌色或风险色，再使用 `custom:{...}` 形式
- 同一个字段下，`id` 必须稳定唯一；不要只靠中文 `label` 充当主键
- 技能输出若出现“多选题 / 判断题 / 状态 / 标签 / 等级”这类选项字段，必须带颜色，不要只返回纯文本数组

### 场景 3：解释为什么工作流在 AI 分析入口显示不对

标准排查顺序：

1. 看团队级 `usageType`
2. 看项目级 `systemView`
3. 明确当前规则是项目绑定优先、全局默认回退
4. 再看页面入口到底读的是哪个树接口或绑定接口

## 常见错误与排查

| 错误现象 | 根本原因 | 解决方案 |
| --- | --- | --- |
| 表搭出来了，但字段不好用 | 字段只按名字设计，没有提前考虑筛选、排序、主展示和关联 | 回到字段模板，补齐字段能力设计 |
| 人员下拉被建成普通下拉字段 | 没识别项目已有用户体系、内置角色、部门体系，误把“选人”当成静态枚举 | 优先改用 `person` 字段，先判断是不是用户选择场景 |
| 部门字段被建成普通下拉字段 | 没识别“部门归属 / 部门筛选”属于组织结构字段 | 优先改用 `department` 字段，不要用静态 `select` 代替 |
| 后面做报表时发现字段出不了图 | 建表阶段没区分维度字段、指标字段和说明字段 | 回到字段设计模板，先把用于报表的字段类型设计正确 |
| 行能查出来，但筛选条件不好表达 | 没按 `keyword / searchFieldIds / filters / filterMatchType / sortRule` 结构设计 | 按 `row/page` 真实请求结构重写查询案例 |
| 表能查到，但字段写入失败 | 字段类型不匹配、列级只读或系统字段受控 | 先查字段结构，再查列权限与系统字段规则 |
| 行分页读取正常，协同更新异常 | 普通接口权限和 Yjs 协同过滤不是同一条缓存链 | 检查协同权限快照、系统字段净化和广播过滤 |
| AI 分析入口工作流分类不对 | 把团队级默认字段当成项目级实际分配字段 | 区分 `usageType` 与 `systemView` |
| 同一字段在不同项目表现不同 | 项目级绑定、权限或系统视图规则不同 | 结合 `projectId` 重新判断，不要跨项目直接套用 |
| 单元格改不了但页面没明显报错 | 后端行级或列级鉴权拒绝 | 检查表级、列级、行级三层权限链路 |

## 参考文档

- `references/build-flow.md`
- `references/field-design-patterns.md`
- `references/row-filters.md`
- `references/field-rules.md`
- `references/examples.md`
