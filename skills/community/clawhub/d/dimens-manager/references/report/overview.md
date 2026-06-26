---
name: dimens-manager-report
slug: dimens-manager-report
description: 用于维表智联报表、图表组件、参数联动和数据源查询链路说明。
version: 1.0.0
author: 方块智联工作室
tags: [report, dashboard, data-source, analytics, dimens-cli]
---

# dimens-manager 报表章节

适用产品：

- 产品名称：`维表智联`
- 开发方：`方块智联工作室`
- 官网：[https://dimens.bintelai.com/](https://dimens.bintelai.com/)

## 执行前必读

- ✅ 报表默认是项目级资源，先确认 `projectId`
- ✅ 报表问题不要只看页面表现，还要看数据源、参数、组件配置和权限链路
- ✅ 参数联动异常不一定是前端问题，也可能是查询链路或默认值问题
- ✅ 报表可访问不代表底层数据源一定可访问，项目权限和数据源约束可能继续收窄
- ✅ 涉及多维表格数据源时，还要联动检查表格权限和字段映射
- ✅ 当前报表前端图表主渲染基于 `recharts@3.6.0`，生成组件时必须按前端真实支持的 `type` 和字段映射输出
- ✅ 当报表组件来自多维表格时，不能只给 `sheetId`，必须同时补 `sheet.columns`、`fieldIds`、`recommendedMapping`、`previewMapping`、`dataMapping`
- ✅ 报表主资源和报表组件的更新都应默认按“先拿数据 -> 改数据 -> 更新数据”执行，不要直接把局部 patch 当成通用模式

## 高风险跑偏点

下面这些是 AI 在报表场景最容易做错的地方，主技能必须优先强调：

1. 不要把“创建报表”理解成只执行旧 `/app/report/add`
2. 不要跳过固定预检链，直接执行 `widget-add`
3. 不要把 `recommendedMapping` 当成最终图表映射
4. 不要把 `sheetId` 当成完整数据源配置
5. 不要默认任何字段都适合作为图表数值轴
6. 不要把系统字段默认拿来做主维度或主指标
7. 不要把 `query`、`query-widget`、`preview` 三者混成一件事
8. 不要跳过 `report info` 或现有组件读取，直接覆盖更新报表或组件

对应解释：

- 当前 `report create` 创建的是项目菜单中的 `type=report` 资源，底层走 `/app/mul/project/:projectId/sheet/create`
- 该接口返回 `sheetId`，CLI 会把 `sheetId` 归一化为后续可用的 `reportId`
- `report create` 只会创建报表主资源和空 dashboard，不会自动补组件
- `preview` 是看数据源是否能出数，`query-widget` 是看组件配置后能不能正确跑，`query` 是整报表结果校验
- `recommendedMapping` 更偏规范层，真正给前端渲染的是 `dataMapping`
- 对多维表格数据源，通常至少要有：`sheetId + columns + fieldIds + recommendedMapping + previewMapping + dataMapping`
- 数值轴字段必须是数字或可稳定转数字，文本字段不要硬塞成 `valueKey`

## 报表生成时禁止省略的关键层

只要是“直接生成图表组件”，下面这些层任意缺一，都应该视为高风险：

1. 项目上下文：`projectId`
2. 组件类型：`type`
3. 数据源定义：`dataSource`
4. 多维表格元信息：`sheet.columns`、`fieldIds`
5. 查询预检映射：`previewMapping`
6. 最终渲染映射：`dataMapping`
7. 执行前验证：`preview` 或 `query-widget`

## 命令维护表

| 命令 | 作用 | 必填参数 | 常用可选 | 细节说明 |
| --- | --- | --- | --- | --- |
| `dimens-cli report list` | 查询项目下报表列表 | `projectId` | `keyword`, `status`, `type`, `page`, `size`, `app-url` | 报表属于项目资源，排查问题先锁定 `projectId` |
| `dimens-cli report info` | 获取报表详情 | `projectId`, `reportId` | `app-url` | 报表更新前默认先读当前主资源和组件数组 |
| `dimens-cli report create` | 创建项目菜单报表主资源 | `projectId`, `name` | `description`, `app-url` | 底层创建 `type=report` 的 sheet；返回里的 `reportId` 等于 `sheetId`，后续 `widget-add/query` 直接使用它 |
| `dimens-cli report update` | 更新报表主资源信息 | `projectId`, `reportId` | `name`, `description`, `type`, `app-url` | 默认先 `report info` 拿当前数据，再改目标字段，再 update |
| `dimens-cli report copy` | 复制已有报表 | `projectId`, `reportId` | `name`, `app-url` | 适合快速生成副本，不替代跨项目迁移 |
| `dimens-cli report publish` | 发布或取消公开报表 | `projectId`, `reportId`, `is-public` | `app-url` | 发布前建议至少做一次 `query` 或 `query-widget` 验证 |
| `dimens-cli report delete` | 删除报表主资源 | `projectId`, `reportId` | `app-url` | 删除前先确认是不是仍有组件和外部入口依赖 |
| `dimens-cli report archive` | 归档报表 | `projectId`, `reportId` | `app-url` | 用于生命周期收口，不等价删除 |
| `dimens-cli report validate` | 校验报表配置 | `projectId`, `config` | `app-url` | 创建或更新前建议先校验配置结构 |
| `dimens-cli report sort` | 调整报表顺序 | `projectId`, `reportId`, `target-index` | `app-url` | 影响列表顺序，不改报表内容本身 |
| `dimens-cli report move` | 将报表迁移到其他项目 | `projectId`, `reportId`, `target-project-id` | `app-url` | 迁移后要重新校验查询结果和访问权限 |
| `dimens-cli report widget-add` | 给报表新增组件 | `projectId`, `reportId`, `type`, `data-source` | `title`, `description`, `layout`, `data-mapping`, `chart-config`, `order-num`, `app-url` | 正常链路是先 `preview`，再新增组件，最后 `query-widget` |
| `dimens-cli report widget-update` | 更新某个报表组件配置 | `projectId`, `widgetId` | `report-id`, `type`, `title`, `description`, `data-source`, `layout`, `data-mapping`, `chart-config`, `order-num`, `app-url` | 默认先 `report info` 读取当前组件，再合并变更后更新，不要直接盲写局部 patch |
| `dimens-cli report widget-delete` | 删除组件 | `projectId`, `widgetId` | `app-url` | 删除前应确认目标组件归属和顺序影响 |
| `dimens-cli report widget-batch` | 批量覆盖整份组件数组 | `projectId`, `reportId`, `widgets` | `app-url` | 属于高风险命令，提交前要先拿当前组件数组并确认覆盖范围 |
| `dimens-cli report widget-sort` | 调整组件顺序 | `projectId`, `reportId`, `widgetId`, `target-order` | `app-url` | 只调整顺序，不应误改组件主体配置 |
| `dimens-cli report query` | 执行整报表查询 | `projectId`, `reportId` | `params`, `widget-ids`, `app-url` | 用于整报表联调和发布前确认 |
| `dimens-cli report query-widget` | 执行单组件查询 | `projectId`, `reportId`, `widgetId` | `params`, `data-source`, `data-mapping`, `app-url` | 适合单组件试跑和映射排查 |
| `dimens-cli report preview` | 预览数据源结果 | `projectId`, `data-source` | `data-mapping`, `params`, `app-url` | 创建和修改组件前的固定预检步骤，不建议跳过 |

### 强调细节

- 报表主资源更新和组件更新都默认遵循“拿数据 -> 改数据 -> 更新数据”，不能把局部 patch 当通用更新模型。
- `report update` 前默认先 `report info`；`widget-update` 前默认先拿当前报表和当前组件数据，再合并目标字段。
- 报表链路不要只执行 `report create` 或 `widget-add`，固定预检链是 `report preview -> widget-add/widget-update -> query-widget -> query`。
- 如果组件来自多维表格数据源，不能只传 `sheetId`，还要把 `columns`、`fieldIds`、映射信息一起带齐。
- `widget-batch` 是整数组覆盖操作，风险高，默认先读取当前 `widgets` 并明确覆盖范围后再提交。

## 核心约束

### 1. 资源边界

- 报表归属于项目
- 图表组件、参数、版本都从属于报表
- 任何“报表查不到”问题都应该先落到具体 `projectId + reportId`

### 2. 数据源边界

- 报表可使用多维表格、SQL、外部 API、静态数据等数据源
- 不同数据源的限制不同，不能按同一条排查路径处理
- 涉及多维表格数据源时，要联动表格 Skill 判断权限与字段映射

### 3. 参数联动边界

- 参数默认值、依赖关系、选项数据源都会影响最终查询结果
- “图表空白”不一定是无数据，也可能是参数没传对或联动条件不满足

### 4. 权限边界

- 当前统一口径是项目级权限校验优先
- 用户必须具备项目访问权限才能操作报表
- 组件可显示不代表底层查询一定能返回完整数据

### 5. 当前报表能力现状

当前 `dimens-cli` 在报表这块已经不是“只支持一点点”，而是三条主链都已可执行：

1. 主资源链：
   `list -> info -> create -> update -> copy -> publish -> delete -> archive -> validate -> sort -> move`
2. 组件链：
   `widget-add -> widget-update -> widget-delete -> widget-batch -> widget-sort`
3. 查询链：
   `query -> query-widget -> preview`

但要注意：

- 当前命令层已经能做基础结构校验，不代表任何复杂报表都能一次自动生成成功
- 真正影响成功率的关键，仍然是 `dataSource + dataMapping + previewMapping + 组件 type` 是否和前端真实实现一致
- 更复杂的可视化诊断、批量运维、副作用联动，还不能等同于“报表运维平台已经完全 CLI 化”

## 标准执行顺序

### 1. 用户要“创建一个报表”

建议默认按下面顺序执行：

1. 先确认 `projectId`
2. 执行 `dimens-cli report create`，并记录返回的 `reportId`（即菜单资源 `sheetId`）
3. 如果要加组件，先回到 `references/recharts-widget-guide.md`
4. 先执行 `dimens-cli report preview`
5. 再执行 `dimens-cli report widget-add`
6. 如需验证单个组件，再执行 `dimens-cli report query-widget`
7. 全部组件补齐后，再执行 `dimens-cli report query`
8. 确认结果可用后，再决定是否 `report publish`

这条顺序就是报表生成时的固定预检链，不要跳过中间步骤。

### 2. 用户要“修一个有问题的报表”

建议默认按下面顺序执行：

1. `dimens-cli report info`
2. 如果是结构问题，先查组件配置
3. 先跑 `dimens-cli report preview`
4. 再跑 `dimens-cli report query-widget`
5. 如果只是基础信息问题，用 `dimens-cli report update`
6. 如果是组件问题，用 `widget-update` / `widget-batch` / `widget-sort`
7. 无论是报表还是组件更新，默认先读当前数据，再改目标字段，再提交更新

防跑偏提醒：

- 不要一看到“图表空白”就直接改组件
- 先分清是数据源空、参数不对，还是映射错误
- 没有 `preview` 结果时，不要急着判断前端渲染有问题

### 3. 用户要“把一个报表迁移到别的项目”

建议默认按下面顺序执行：

1. 先确认源 `projectId`
2. 先确认目标 `targetProjectId`
3. 如果只是保留一份副本，优先 `report copy`
4. 如果明确是迁移，执行 `report move`
5. 迁移后立刻执行 `report info` 或 `report query` 做校验

## 创建前预检规则

当 Skill 准备帮用户直接生成报表、图表组件或命令时，至少要先完成下面这些检查：

1. 是否已经锁定 `projectId`
2. 组件 `type` 是否属于前端真实支持列表
3. 如果数据源来自多维表格，是否已经明确 `sheetId`
4. `sheet.columns` 是否包含真实字段标签和类型
5. `fieldIds` 是否与选中字段一致
6. `recommendedMapping` 是否使用规范键名
7. `previewMapping` 是否存在
8. `dataMapping` 是否使用真实字段标签
9. 是否能先用 `report preview` 预览
10. 是否需要再用 `report query-widget` 做单组件试跑

只要上面任一项不完整，就不要直接输出“可一次成功创建”的结论。

特别提醒：

- 如果用户只给了“想做一个折线图”，不要自动假设维度列和值列
- 如果用户只给了示例数据，没有给真实字段结构，不要直接伪造 `sheet.columns`
- 如果用户要的是“复用现有报表”，优先 `report info` 和 `query-widget`，不要直接重建

## 生成报表时的固定输出要求

当用户要你“直接生成一个报表 / 看板 / 图表组件”时，Skill 不应该只给一句命令。默认至少要输出这四块：

1. 报表主资源信息：
   名称、描述、项目上下文
2. 组件设计：
   `type`、标题、布局、数据源、字段映射
3. 预检命令：
   `report preview` 或 `report query-widget`
4. 最终执行命令：
   `report create`、`widget-add`、必要时 `publish`

如果用户要求“直接给 JSON”，也要把 JSON 按下面顺序组织：

1. `dataSource`
2. `dataMapping`
3. `chartConfig`
4. 展示层字段如 `colSpan`、`height`、`showLegend`

## 常用命令模板

### 1. 先创建报表主资源

```bash
dimens-cli report create \
  --project-id PROJ1 \
  --name "销售分析看板" \
  --description "月度销售经营看板" \
  --type 1
```

### 2. 先预览数据再加组件

```bash
dimens-cli report preview \
  --project-id PROJ1 \
  --data-source '{"mode":"sheet","sheet":{"sheetId":"S1","columns":[{"fieldId":"fld_1","label":"名称","type":"text"},{"fieldId":"fld_2","label":"销售额","type":"number"}],"fieldIds":["fld_1","fld_2"],"recommendedMapping":{"nameKey":"name","valueKey":"value"},"previewMapping":{"nameKey":"name","valueKey":"value","aggregation":"sum","limit":10}}}' \
  --data-mapping '{"nameKey":"名称","valueKey":"销售额"}'
```

### 3. 创建组件

```bash
dimens-cli report widget-add \
  --project-id PROJ1 \
  --report-id REPORT_1 \
  --type line \
  --title "销售趋势" \
  --data-source '{"mode":"sheet","sheet":{"sheetId":"S1","columns":[{"fieldId":"fld_1","label":"名称","type":"text"},{"fieldId":"fld_2","label":"销售额","type":"number"}],"fieldIds":["fld_1","fld_2"],"recommendedMapping":{"nameKey":"name","valueKey":"value"},"previewMapping":{"nameKey":"name","valueKey":"value","aggregation":"sum","limit":10}}}' \
  --data-mapping '{"nameKey":"名称","valueKey":"销售额"}'
```

### 4. 单组件试跑

```bash
dimens-cli report query-widget \
  --project-id PROJ1 \
  --report-id REPORT_1 \
  --widget-id widget_1 \
  --params '{"month":"2026-04"}'
```

## 必查文档

| Skill / references | 作用 | 什么时候必须看 |
| --- | --- | --- |
| `dimens-manager/references/team/overview.md` | 项目级资源边界与上下文 | 处理报表时必须先看 |
| `dimens-manager/references/table/overview.md` | 多维表格数据源与字段映射 | 报表基于表格数据源时必须看 |
| `dimens-manager/references/permission/overview.md` | 项目权限、数据访问范围与可见性 | 解释访问问题时建议看 |
| `references/usage.md` | 报表使用分层说明 | 处理报表时必须看 |
| `references/capability-status.md` | 当前报表能力范围 | 判断是否已封装时建议看 |
| `references/examples.md` | 报表 / 图表 / 参数接口案例 | 需要直接举例时看 |
| `references/recharts-widget-guide.md` | Recharts 组件类型、字段映射与一次生成成功规范 | 生成或修改报表组件时必须看 |

## 使用场景示例

### 场景 0：AI 直接生成报表组件

固定顺序：

1. 先确认 `projectId + reportId`
2. 再确认图表类型是否属于前端真实支持列表
3. 如果数据来自多维表格，必须确认 `sheetId + 字段列表 + 字段类型 + 最终 dataMapping`
4. 最后再生成命令或 JSON

如果上面信息不完整，不要直接承诺“一次创建成功”

### 场景 0.1：AI 直接生成整份看板

默认动作：

1. 先创建报表主资源
2. 按组件逐个设计 `type + dataSource + dataMapping`
3. 每个组件先预览，再创建
4. 所有组件完成后再整报表查询
5. 确认无误后再发布

### 场景 1：解释为什么报表能打开但图表没数据

标准排查顺序：

1. 确认 `projectId` 与 `reportId`
2. 检查参数默认值和联动关系
3. 检查组件绑定的数据源
4. 检查数据源权限和返回结果

### 场景 2：查询报表详情

```json
{
  "projectId": "PROJ1",
  "reportId": "REPORT1"
}
```

### 场景 3：按参数执行图表查询

```json
{
  "projectId": "PROJ1",
  "reportId": "REPORT1",
  "params": {
    "dateRange": "this_month",
    "owner": "currentUser"
  }
}
```

## 常见错误与排查

| 错误现象 | 根本原因 | 解决方案 |
| --- | --- | --- |
| 报表能打开但图表空白 | 参数没传对、联动不满足或数据源无结果 | 先检查参数定义，再查数据源 |
| 同一报表不同人看到的数据不一样 | 项目权限或底层数据源权限不同 | 继续检查项目权限与数据源访问范围 |
| 图表组件不显示 | 组件可见性条件或布局配置异常 | 检查组件配置和显示条件 |
| 导出结果和页面结果不一致 | 导出链路与查询参数不一致 | 对比导出参数与页面查询参数 |
| 报表查多维表格数据失败 | 底层表格权限、字段映射或数据源配置有问题 | 联动检查 `dimens-manager/references/table/overview.md` 和权限链路 |
| AI 生成的图表创建失败或渲染空白 | 图表类型、`dataMapping`、`sheet.columns`、`previewMapping` 其中一层缺失 | 必须回到 `references/recharts-widget-guide.md` 按 checklist 重建 |
| AI 直接创建组件就失败 | 没先执行 `report preview` 或 `report query-widget` 做预检 | 先预览数据源，再创建组件 |
| 报表迁移后打不开 | 只做了资源移动，没有继续校验数据源和查询 | 迁移后立即执行 `report info`、`report preview` 或 `report query` |
| 以为 Skill 说得通就一定能创建成功 | 技能和命令之间少了预检步骤 | 把 `report create -> report preview -> report widget-add -> report query-widget -> report query` 当成固定预检链 |
| 把字段标签和字段 ID 混用 | 映射层和元信息层混在一起了 | `sheet.columns/fieldIds` 保留字段 ID，`dataMapping` 使用真实字段标签或前端消费键 |
| 把文本列当数值列 | 没先确认字段类型 | 数值轴只使用数字字段，必要时先在预览阶段验证 |

## 参考文档

- `references/usage.md`
- `references/capability-status.md`
- `references/examples.md`
- `references/recharts-widget-guide.md`
- 如需查看整个 Skill 体系的能力总览，请返回 `dimens-cli/skills/README.md`
