# dimens-manager 多维表格章节 建模落地链路

## 1. 文档目标

这份文档专门补“怎么一步步把系统搭出来”。

前面的 references 已经分别说明了：

- 接口总览：`examples.md`
- 字段设计：`field-design-patterns.md`
- 行筛选与排序：`row-filters.md`
- 系统视图规则：`field-rules.md`

但用户还需要一条更直接的落地链路：

1. 先有项目
2. 再有表 / 文档
3. 再补公开默认视图
4. 再设计字段
5. 再写示例数据
6. 最后用查询案例验证这套结构是否真的能用

---

## 2. 默认落地顺序

当用户说“帮我搭一个系统”时，围绕表格能力，默认建议按这个顺序落地：

1. 确认项目
2. 创建表 / 文档
3. 补公开默认视图
4. 设计字段
5. 组织 relation
6. 写示例行数据
7. 用 `row/page` 验证搜索、筛选、排序

这条顺序的重点是：

- 先把容器和结构搭出来
- 再把筛选、排序依赖的默认公开视图补齐
- 再验证它是不是可搜索、可筛选、可排序

如果这个系统后续还要进入报表，建表阶段还要同步考虑：

- 哪些字段会作为图表维度字段
- 哪些字段会作为图表指标字段
- 哪些字段只是说明字段，不应该直接做 `valueKey`
- 哪些字段要避免退化成普通下拉，应该直接走人员字段或部门字段

否则表虽然能建出来，后面进入 `report preview / query-widget / dataMapping` 时仍然会失败。

---

## 3. 第一步：从项目进入

表格能力默认先从项目进入，而不是脱离项目单独开始。

建议先确认：

| 需要确认的项 | 说明 |
| --- | --- |
| `teamId` | 团队上下文 |
| `projectId` | 业务系统容器 |
| 项目名称 | 用户最终看到的系统名称 |
| 项目菜单是否已有入口 | 决定后续表 / 文档入口如何组织 |

如果项目还没建，可以先用项目命令作为第一步：

```bash
dimens-cli project create --team-id TTFFEN --name 客户管理系统
```

注意：

- 这是上游步骤，但现在应优先通过 `dimens-manager/references/project/overview.md` 主链理解和执行，而不是继续归到 `dimens-manager/references/team/overview.md`。
- 如果项目不明确，后续所有表结构讨论都会飘。

---

## 4. 第二步：创建表 / 文档

### 4.1 先决定是表还是文档

一般建议：

| 资源类型 | 适合场景 |
| --- | --- |
| 表 | 结构化业务对象，例如客户、联系人、工单、商机 |
| 文档 | 说明页、制度页、知识沉淀、操作说明 |

对多数业务系统，默认主线仍然是先建表。

### 4.2 创建表的基本路径

接口路径：

| 方法 | 路径 |
| --- | --- |
| `POST` | `/app/mul/project/:projectId/sheet/create` |

CLI 命令：

```bash
dimens-cli sheet create --project-id PUQUNFE --name 客户表
```

创建表前建议先明确：

| 项 | 说明 |
| --- | --- |
| 表名 | 用户能直接理解的业务名 |
| 表的业务对象 | 客户、联系人、工单、商机等 |
| 是否需要多个核心表 | 一般是 |
| 是否需要辅助文档 | 视业务复杂度决定 |

### 4.3 创建表后立即检查默认公开视图

用户这轮反馈已经证明，只建表和字段还不够，技能链路如果没有公开默认视图，前端常见表现就是“无法筛选”。

所以建表后默认追加下面两步：

1. 先执行 `view list` 检查是否已经存在公开视图
2. 如果没有，就显式创建一个公开的 `grid` 默认视图

推荐检查命令：

```bash
dimens-cli view list \
  --team-id TTFFEN \
  --project-id PUQUNFE \
  --sheet-id sh_customer
```

推荐补建命令：

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

默认公开视图建议采用下面这组最小配置：

| 配置项 | 建议值 |
| --- | --- |
| `name` | `默认视图` |
| `type` | `grid` |
| `isPublic` | `true` |
| `filters` | `[]` |
| `filterMatchType` | `and` |
| `sortRule` | `null` |
| `groupBy` | `[]` |
| `hiddenColumnIds` | `[]` |
| `rowHeight` | `medium` |

注意：

- 不要假设后端或前端一定会自动补齐，技能链路必须显式检查
- 如果 `view list` 已经返回公开默认视图，就不要重复创建
- 当前 CLI 只稳定支持 `view list/create`，这里不要展开成更复杂的视图编排

---

## 5. 第四步：设计并创建字段

如果后续要做报表，这一步不能只看“能不能录入”，还要同步看“能不能统计、能不能出图”。

建议先把字段分成三类：

| 字段角色 | 推荐类型 | 主要用途 |
| --- | --- | --- |
| 维度字段 | `text` / `select` / `date` / `person` / `department` | 分类、横轴、筛选、分组 |
| 指标字段 | `number` | 求和、计数、排序、统计值 |
| 说明字段 | `text` | 详情补充、备注说明，不直接做数值映射 |

这三类字段一开始就分清楚，后面进入 `dimens-manager/references/report/overview.md` 才更容易一次生成成功。

### 5.1 创字段前先确认什么

不要一上来只问“这个字段叫什么”，至少要先确认：

| 需要确认的项 | 说明 |
| --- | --- |
| 字段名 | 业务上怎么称呼 |
| 类型 | `text` / `select` / `date` / `number` / `relation` 等 |
| 是否主展示 | 决定列表标题和 relation 展示 |
| 是否必填 | 决定录入约束 |
| 是否唯一 | 编号、手机号等常见需要 |
| 是否参与搜索 | 用于 `keyword + searchFieldIds` |
| 是否参与筛选 | 用于 `filters` |
| 是否参与排序 | 用于 `sortRule` |

如果是 relation 字段，还要继续确认：

- 目标表
- 展示字段
- 是否多选
- 是否双向
- `editViewFields`

如果是 `select` 或 `multiSelect` 字段，还要继续确认：

- 候选项列表
- 每个候选项的显示文案
- 是否需要颜色
- 如果来源是 Excel，先扫描该列去重值生成候选项，再创建字段；不要只按表头创建一个空 `select`
- 行数据导入前要把 Excel 单元格值映射到字段已有 `options` 的 `label` 或 `id`；遇到不存在的值，先补选项再写入

不要只创建空的 `select` 字段，否则前端新增数据时会直接报错或不可用。

如果字段语义本身就是“人员”或“部门”，不要退化成普通下拉：

- 项目已有自己的用户体系、部门体系、内置角色体系时，优先直接配置人员字段
- 部门选择也优先直接配置部门字段
- 这两类字段和普通下拉一样都属于特殊情况，不能简单按 `select` 处理

这样后续做权限、筛选、报表统计时，字段语义才不会丢失。

更详细的字段模板，请直接查看 `field-design-patterns.md`。

### 5.2 创建字段的基本路径

接口路径：

| 方法 | 路径 |
| --- | --- |
| `POST` | `/app/mul/:teamId/:projectId/sheet/:sheetId/column/create` |

CLI 命令：

```bash
dimens-cli column create \
  --team-id TTFFEN \
  --project-id PUQUNFE \
  --sheet-id sh_customer \
  --label 客户名称 \
  --type text
```

实践建议：

- 先建主展示字段
- 再建状态字段、时间字段、人员字段
- 最后建 relation 字段
- 当前 CLI 已兼容旧参数 `--title`，但推荐统一改用 `--label`，与服务端字段名保持一致
- `select` / `multiSelect` 创建时必须同步补 `--options`，推荐直接传 JSON 数组对象，便于补齐颜色等配置
- relation 字段当前复杂配置仍建议按 API 的 `relationConfig` 结构校验，不能只看 CLI 成功提示

如果目标里明确包含报表，字段设计时默认再补下面 4 个判断：

1. 维度字段是否有稳定可读值，而不是空值、长文本或混乱枚举
2. 指标字段是否真的是 `number`，不要把金额、数量存成文本
3. 人员字段、部门字段是否保留真实业务语义，而不是降级成普通下拉
4. 系统字段是否只作为补充说明，而不是直接当主维度或主指标

---

## 6. 第五步：组织 relation

如果系统不只是单表，默认要尽早把 relation 设计出来。

例如 CRM：

| 表 | relation 设计 |
| --- | --- |
| 联系人表 | 所属客户 -> 客户表 |
| 商机表 | 所属客户 -> 客户表 |
| 跟进记录表 | 所属客户 -> 客户表；所属联系人 -> 联系人表 |

relation 的目标不是“看起来有关系”，而是为了后续能做：

- 关联选择
- 关联追踪
- 关联筛选
- 多表查询解释

---

## 7. 第六步：写示例行数据

### 7.1 示例数据不要只写一条

为了验证表结构是否真能用，建议每张表至少写 3-5 条案例数据，并覆盖：

| 覆盖项 | 说明 |
| --- | --- |
| 主状态 | 例如潜客、跟进中、成交、流失 |
| 典型对象 | 例如重点客户、普通客户 |
| 时间差异 | 例如最近跟进、超期未跟进 |
| 负责人差异 | 例如不同销售负责人 |
| 关联关系 | 例如一个客户对应多个联系人 |

如果后续还要做报表，示例数据不要只追求“有值”，还要覆盖：

| 覆盖项 | 说明 |
| --- | --- |
| 维度分布 | 至少有 2-3 个分类值，方便验证分组统计 |
| 指标差异 | 至少有明显不同的数值，方便验证排序和聚合 |
| 时间跨度 | 至少覆盖多个日期，方便验证趋势图 |
| 人员 / 部门差异 | 方便验证人员维度或部门维度图表 |

### 7.2 创建行的基本路径

接口路径：

| 方法 | 路径 |
| --- | --- |
| `POST` | `/app/mul/sheet/:sheetId/row/create` |

CLI 命令：

```bash
dimens-cli row create \
  --sheet-id sh_customer \
  --values '{"fld_customerName":"华东智造","fld_customerLevel":"A","fld_customerStatus":"跟进中"}'
```

注意：

- 行创建前要先通过 `column list` 查询字段列表，拿到真实 `fieldId`
- `--values` 只是 CLI 参数名，CLI 内部会映射为服务端需要的 `data`
- 不要直接把中文字段名当请求体 key，服务端真实写入以 `fieldId` 为准

---

## 8. 第七步：用 `row/page` 验证结构是否可用

表搭出来之后，不能只看“有数据”，还要验证它能不能支撑真实查询。

至少建议做 4 类验证：

### 8.1 关键词搜索

验证主展示字段和编号字段是否真的能被搜到。

### 8.2 单字段筛选

验证状态、等级、负责人等字段是否真的适合筛选。

### 8.3 排序

验证时间、金额等字段是否真的适合排序。

### 8.4 relation 筛选

验证跨表关系能不能支撑“查某客户下全部联系人 / 商机 / 跟进记录”。

更详细的查询结构，请直接查看 `row-filters.md`。

如果系统下一步要进报表，这里不要停在 `row/page`。

建表链路完成后，默认继续交给 `dimens-manager/references/report/overview.md` 的固定预检链：

```bash
dimens-cli report create
dimens-cli report preview
dimens-cli report widget-add
dimens-cli report query-widget
dimens-cli report query
```

这条顺序的意义不是“多跑几个命令”，而是逐段确认：

- 表结构能不能被报表识别成合法数据源
- 维度字段 / 指标字段能不能形成稳定映射
- 组件加上去以后到底有没有数据
- 最终整份报表查询是不是通的

不要跳过这条固定预检链，直接从 `widget-add` 开始。

---

## 9. CRM 作为单一案例

下面给一条更接近用户视角的最小落地链路：

### 9.1 创建项目

```bash
dimens-cli project create --team-id TTFFEN --name 客户管理系统
```

### 9.2 创建 4 张核心表

```bash
dimens-cli sheet create --project-id PUQUNFE --name 客户表
dimens-cli sheet create --project-id PUQUNFE --name 联系人表
dimens-cli sheet create --project-id PUQUNFE --name 跟进记录表
dimens-cli sheet create --project-id PUQUNFE --name 商机表
```

### 9.2.1 为每张核心表确认默认公开视图

```bash
dimens-cli view list --team-id TTFFEN --project-id PUQUNFE --sheet-id sh_customer
dimens-cli view create --team-id TTFFEN --project-id PUQUNFE --sheet-id sh_customer --name 默认视图 --type grid --is-public true --config '{"filters":[],"filterMatchType":"and","sortRule":null,"groupBy":[],"hiddenColumnIds":[],"rowHeight":"medium"}'
```

如果 `view list` 已经有公开默认视图，就跳过 `view create`。

### 9.3 设计关键字段

- 客户表：客户名称、客户编号、客户等级、客户状态、销售负责人、最近跟进时间
- 联系人表：联系人姓名、手机号、职位、所属客户
- 跟进记录表：跟进主题、跟进时间、所属客户、所属联系人、跟进结果
- 商机表：商机名称、所属客户、商机阶段、预计金额、预计成交日期

### 9.4 写案例数据

- 客户表至少覆盖 A/B/C 等级和不同客户状态
- 联系人表至少覆盖一个客户多个联系人
- 商机表至少覆盖不同阶段和不同金额
- 跟进记录表至少覆盖最近跟进和超期未跟进两类情况

### 9.5 做查询验证

- 搜“华东”能搜到客户名称
- 筛 A 级客户能命中客户等级字段
- 按最近跟进时间倒序能排序
- 按所属客户 relation 能查到该客户下全部联系人

### 9.6 如果后续要做 CRM 看板，再补报表预检

这一步至少要明确：

- `客户等级`、`客户状态`、`销售负责人` 更适合做维度字段
- `预计金额`、`成交金额`、`跟进次数` 更适合做指标字段
- `客户简介`、`备注` 更适合做说明字段，不直接做 `valueKey`

然后再进入 `dimens-manager/references/report/overview.md` 的固定预检链：

```bash
dimens-cli report create --project-id PUQUNFE --name CRM 经营看板
dimens-cli report preview --team-id TTFFEN --project-id PUQUNFE --sheet-id sh_customer
dimens-cli report widget-add --team-id TTFFEN --project-id PUQUNFE --sheet-id rpt_xxx --widget-config '{...}'
dimens-cli report query-widget --team-id TTFFEN --project-id PUQUNFE --sheet-id rpt_xxx --widget-id wgt_xxx
dimens-cli report query --team-id TTFFEN --project-id PUQUNFE --sheet-id rpt_xxx
```

如果在这一步才发现字段不能做统计，问题通常不在报表命令，而在前面的表结构设计。

---

## 10. 高风险跑偏点

1. 不要把“表能录入”误判成“后面一定能出报表”。
2. 不要把金额、数量、次数这类指标字段设计成文本。
3. 不要把人员字段、部门字段一律降级成普通下拉。
4. 不要把系统字段默认当成主维度或主指标。
5. 不要等到 `report widget-add` 失败了，才回头补字段语义。

---

## 11. 与其他 references 的关系

建议按下面顺序组合使用：

1. 先看本文件，明确搭系统时的默认落地顺序。
2. 再看 `field-design-patterns.md`，把字段设计细化。
3. 再看 `row-filters.md`，把查询验证写成真实结构。
4. 再看 `examples.md`，确认接口路径、CLI 命令和当前能力状态。
5. 如果系统还要进入图表、统计分析、经营看板，再继续看 `../../report/README.md` 和 `../../report/overview.md`。
