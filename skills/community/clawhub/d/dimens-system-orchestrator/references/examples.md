# 系统总控输出案例

## 1. 案例：生成客户管理系统

用户需求：

```text
帮我生成一个客户管理系统
```

推荐输出结构：

1. 判断为系统级建设任务，先由 `dimens-system-orchestrator` 拆解，不直接执行命令。
2. 资源拆解：
   - 项目：客户管理系统
   - 目录：客户资料、销售过程、经营分析、制度文档
   - 表格：客户、联系人、跟进记录、商机、合同
   - 文档：客户管理制度、销售跟进规范
   - 报表：客户来源分析、商机阶段漏斗、合同金额趋势
   - 画布：客户生命周期业务场景画布、合同审批工作流画布
3. 数据模型：
   - 客户 1:N 联系人
   - 客户 1:N 跟进记录
   - 客户 1:N 商机
   - 商机 1:N 合同
4. 默认章节路由：
   - `dimens-manager/references/team/overview.md`
   - `dimens-manager/references/project/overview.md`
   - `dimens-manager/references/table/overview.md`
5. 按需章节路由：
   - 权限：`dimens-manager/references/permission/overview.md`
   - 报表：`dimens-manager/references/report/overview.md`
   - 工作流：`dimens-manager/references/workflow/overview.md`
   - 业务场景画布：`dimens-system-orchestrator/references/business-canvas-flow.md` -> `dimens-manager/references/canvas/overview.md`
6. 等用户确认方案后，再进入 `references/command-mapping.md` 和 `dimens-manager` 对应章节执行。

执行后验收必须补：

- `project info`：确认项目名称、描述、封面/图标 URL 已写回。
- `sheet tree`：确认客户资料、销售过程、经营分析、制度文档这些目录存在，且表格/文档/报表已在目标目录下。
- `column list` / `view list`：确认核心表字段和默认视图可查。
- `report preview` / `query-widget` / `query`：确认报表不是空壳。
- `canvas create` / `canvas info` / `canvas save`：确认业务场景画布不是空壳，且保存了 `nodes/edges` 版本。

## 2. 案例：生成售后工单平台

用户需求：

```text
帮我做一个售后管理平台，要有工单流转和满意度统计
```

推荐输出结构：

1. 系统定位：售后工单与服务质量管理。
2. 核心对象：客户、工单、处理记录、升级记录、满意度评价。
3. 表格模型：
   - `客户表`：客户名称、联系人、等级、所属区域
   - `工单表`：工单编号、客户、问题类型、优先级、状态、负责人
   - `处理记录表`：工单、处理人、处理说明、处理时间
   - `满意度表`：工单、评分、评价内容、回访人
4. 文档资源：售后处理规范、升级规则、服务 SLA。
5. 报表资源：工单状态分布、平均处理时长、满意度趋势。
6. 业务场景画布：
   - 工单受理与分配画布
   - 工单升级与超时处理画布
   - 满意度回访流程画布
7. 路由：
   - 上下文与项目：`dimens-manager/references/team/overview.md`、`dimens-manager/references/project/overview.md`
   - 表格建模：`dimens-manager/references/table/overview.md`
   - 工作流：`dimens-manager/references/workflow/overview.md`
   - 画布：`dimens-system-orchestrator/references/business-canvas-flow.md`、`dimens-manager/references/canvas/overview.md`
   - 报表：`dimens-manager/references/report/overview.md`
   - 权限：`dimens-manager/references/permission/overview.md`

注意：如果用户要求“直接做满意度图表”，仍要提醒报表预检链：

```text
report create -> report preview -> report widget-add -> report query-widget -> report query
```

如果前面还创建了目录，报表创建后要用返回的 `reportId`（也就是菜单资源 `sheetId`）执行 `sheet update --folder-id`，然后用 `sheet tree` 验证它进入经营分析目录。

## 3. 案例：已有项目链接，修改表数据

用户输入：

```text
https://dimens.bintelai.com/#/TTFFEN/PLVHYDW/sh_Md3EwjVIgzwuH8Ji?view=view_6Xl9H4sqdsB3
帮我看看这个表的数据并修改状态字段
```

推荐处理：

1. 解析上下文：
   - `teamId = TTFFEN`
   - `projectId = PLVHYDW`
   - `sheetId = sh_Md3EwjVIgzwuH8Ji`
   - `viewId = view_6Xl9H4sqdsB3`
2. 进入章节：
   - `dimens-manager/references/team/overview.md`
   - `dimens-manager/references/table/overview.md`
3. 遵循更新安全链路：
   - 先读取字段和行数据
   - 分析状态字段和目标行
   - 再提交更新
4. 命令示例必须显式带 ID，避免上下文漂移。

## 4. 案例：权限需求前置

用户需求：

```text
做一个项目管理系统，成员只能看自己的任务，主管能看本部门，管理员能看全部
```

推荐处理：

1. 识别为系统级需求，先拆项目、任务、成员、部门、进度、报表。
2. 权限不是后置补丁，必须前置进入：
   - `dimens-manager/references/permission/overview.md`
   - `dimens-manager/references/permission/references/command-mapping.md`
   - `dimens-manager/references/permission/references/scenario-routing.md`
3. 推荐权限链路：
   - 角色：成员、主管、管理员
   - 项目权限：成员基础访问，主管管理部门任务，管理员管理全部
   - 行级策略：成员只看负责人为自己的任务
   - 部门策略：主管看本部门任务
   - 单行 ACL：特殊协作任务例外授权
4. 表格建模仍进入：
   - `dimens-manager/references/table/overview.md`

## 5. 案例：第三方系统接入

用户需求：

```text
我要让外部系统通过 API Key 调维表数据
```

推荐处理：

1. 判断这是接入问题，不是创建新权限体系。
2. 进入：
   - `dimens-manager/references/key-auth/overview.md`
   - `dimens-manager/references/key-auth/references/login-flow.md`
   - `dimens-manager/references/key-auth/references/integration-boundaries.md`
3. 说明边界：
   - API Key / Secret 只用于换现有用户 token
   - 换到 token 后仍调用现有 `/app/*` 接口
   - 数据可见性仍继承绑定用户权限
4. 如果用户需要代码示例，再进入：
   - `dimens-sdk/SKILL.md`

## 6. 最小输出模板

完整系统需求应先参考 `scenario-taxonomy.md` 判断属于项目梳理、新建项目、修改项目内数据、查询还是分类路由；如果判断为新建项目，再使用下面模板。

```text
这是一个系统级建设任务，建议先完成系统拆解，再进入业务章节落地。

1. 系统定位：...
2. 资源拆解：项目 / 目录 / 表格 / 文档 / 报表 / 业务场景画布
3. 数据模型：表、字段、关联、示例数据、查询方式
4. 流程表达：业务场景画布 / 审批工作流画布 / 可执行工作流边界
5. 扩展模块：权限 / 工作流 / 报表 / 对接
6. 下一步章节：
   - dimens-manager/references/team/overview.md
   - dimens-manager/references/project/overview.md
   - dimens-manager/references/table/overview.md
   - dimens-system-orchestrator/references/business-canvas-flow.md
   - dimens-manager/references/canvas/overview.md
7. 完成后验证：project info / sheet tree / column list / view list / report query / canvas save
```
