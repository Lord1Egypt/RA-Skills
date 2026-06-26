---
name: dimens-manager-project
slug: dimens-manager-project
description: 用于维表智联项目创建、项目初始化、菜单、文档和系统落地入口设计。
version: 1.0.0
author: 方块智联工作室
tags: [project, bootstrap, setup, initialization, dimens-cli]
---

# dimens-manager 项目初始化章节

适用产品：

- 产品名称：`维表智联`
- 开发方：`方块智联工作室`
- 官网：[https://dimens.bintelai.com/](https://dimens.bintelai.com/)

## 执行前必读

- ✅ 执行任何项目命令前，先完成认证；认证方式优先参考 `dimens-manager/references/key-auth/overview.md`
- ✅ 项目一定挂在团队下面，创建项目前必须先确认 `teamId`
- ✅ 当用户给的是 `https://dimens.bintelai.com/#/TEAM_ID/PROJECT_ID/` 这类链接时，优先直接解析成当前项目上下文
- ✅ 这个技能只负责“项目创建 / 项目初始化 / 项目落地入口”，不替代表结构、字段设计、权限设计
- ✅ 当用户要求“创建项目”时，默认先按维表特性完成建模方案设计，再进入创建命令
- ✅ 默认项目初始化主链是：`project create -> sheet/doc/report create -> view list/create -> column create -> role create -> permission create -> role assign-user`
- ✅ 项目创建后不要只补资源本身，还要补项目菜单结构；菜单默认至少包含：目录、表格、报表、文档
- ✅ 目录功能不能漏；如果项目有多个业务域、多个资源区块或需要更清晰的导航入口，优先先建目录，再把表格/文档/报表挂到对应目录下
- ✅ 如果用户只是查团队、成员、租户隔离，优先回到 `dimens-manager/references/team/overview.md`
- ✅ 如果用户已经明确要建表和字段，项目创建完成后应继续路由到 `dimens-manager/references/table/overview.md`
- ✅ 项目初始化时不要只想到多维表格和报表，文档也是项目内的核心资源；在线文档走 TipTap 富文本链路，文档主链默认是 `doc create -> doc info -> doc update -> doc delete`
- ✅ 在线文档默认不是纯文本备注，而是 TipTap 富文本内容；用户创建文档时，默认要具备标题层级、彩色状态标签、淡色提示块/摘要卡片、正文样式和附件区，避免只有黑白文字的单调文档
- ✅ 富文本编辑器已支持 Mermaid 数据；业务流程图、审批流、状态流转、系统对接链路可以直接写入文档，不必截图上传
- ✅ 当前服务端文档内容允许保留 `class`、`style`、`data-video`、`data-attachment`、`data-file-name`、`data-file-size` 等属性，适合承接富文本样式和附件节点
- ✅ 文件/图片上传在产品侧已存在 `/app/base/comm/upload` 上传接口，`dimens-cli` 也已支持 `upload file / upload mode`；如果目标是把文件继续写入在线文档，优先走 `doc attach-file / doc append-image`
- ✅ 如果目标是“上传完成后还能在素材管理里看到”，必须显式传 `--source material`；素材链路会额外写入 `name/size/mimeType` 并落库到素材管理
- ✅ 项目封面、图标、文档图片、文档附件等资源类更新，统一先 `upload file` 拿 `url`，再把 `url` 写回当前业务数据后更新
- ✅ SVG 封面/图标上传时必须保留 `.svg` 扩展名；当前 CLI 会按 `image/svg+xml` 上传，避免被后端当成普通二进制文件处理
- ✅ 项目封面 SVG 默认规格是 `250x150px`，建议写入 `width="250" height="150" viewBox="0 0 250 150"`；背景使用淡色系，动画使用轻量 SVG 动态效果，不要做高饱和、强闪烁或过重动画
- ✅ 所有更新类操作默认都按“先拿数据 -> 改数据 -> 更新数据”执行，不能把局部字段 patch 当成通用更新模型
- ✅ 用户创建项目时，如果还没有现成封面，技能可以先调用 SVG 工具生成一个“符合项目主题、具备动态动画效果”的 SVG 封面，再走上传拿 URL，最后进入项目创建
- ✅ 目录创建成功不代表其他菜单会自动进入目录；表格/目录资源创建时必须带 `--folder-id`，已有资源归位必须再执行 `sheet update --folder-id`
- ✅ 项目资源默认按“三驾马车”理解：表格、文档、报表；不要只初始化其中一个就停下
- ✅ 三驾马车的推荐初始化顺序是：先定项目，再补核心表格，再补在线文档，再补经营报表，最后回到视图、字段、权限和报表预检
- ✅ 如果项目初始化包含报表，不要只执行 `report create`；默认还应继续进入 `report create -> report preview -> report widget-add -> report query-widget -> report query` 这条固定预检链
- ✅ 用户创建项目需求的默认标准路径是：`创建项目 -> 创建多表格 -> 创建多字段 -> 设计 1 对多 / 多对一关联数据 -> 补案例数据 -> (看需求)补项目文档 -> (看需求)补项目报表 -> (看需求)补角色 -> (看需求)补权限`
- ✅ 其中多表、多字段、关联、案例数据属于基础建模路径，默认不应跳过；文档、报表、角色、权限属于按需补齐的后置模块

高风险跑偏点：

- 不要把项目初始化理解成“只建一个项目壳子”
- 不要在维表建模还没明确前，直接开始执行创建命令
- 不要跳过多表、多字段、关联和案例数据这条基础路径
- 不要只建表格，不补文档和报表入口
- 不要漏掉项目菜单和目录；只创建资源、不做目录归位，后续导航和展示会很乱
- 不要把在线文档误解成只创建一次、不需要维护的资源
- 不要把 TipTap 文档写成没有层级、没有状态、没有颜色语义的一整块纯文本；默认至少补 2-3 处有意义的颜色表达
- 不要把上传能力和文档写回能力混为一谈；当前应明确区分 `upload file / upload mode` 与 `doc attach-file / doc append-image`
- 不要把任何 update 命令理解成只传改动字段就够了；默认先读取当前数据，再合并目标变更
- 不要在创建项目时忽略封面表达；如果项目是对外展示型、模板型、知识库型、品牌型项目，优先补 SVG 动态封面再创建
- 不要以为项目里有报表资源就代表看板已可用
- 不要在项目初始化阶段只补 `report create` 就结束
- 不要在没有表结构或字段映射的情况下直接创建组件

## 命令维护表

| 命令 | 作用 | 必填参数 | 常用可选 | 细节说明 |
| --- | --- | --- | --- | --- |
| `dimens-cli project create` | 创建项目主资源，作为系统初始化入口 | `teamId`, `name` | `description`, `projectType`, `remark`, `app-url` | 只创建项目壳子，不代表初始化闭环，后面通常还要继续建目录、表格、文档、报表 |
| `dimens-cli project list` | 查询团队下项目列表 | `teamId` | `page`, `size`, `keyword`, `app-url` | 用于先确认项目上下文，再决定后续进入哪个项目做资源初始化或更新 |
| `dimens-cli project info` | 获取项目详情 | `teamId`, `id` | `app-url` | 项目更新前默认先拿当前项目数据，避免把局部 patch 误当成完整更新数据 |
| `dimens-cli auth use-project` | 切换本地默认项目上下文 | `projectId` | - | 只影响默认上下文，不会替代真实的项目详情读取和更新流程 |
| `dimens-cli upload file` | 上传封面、图标、文档图片、附件等资源，先拿 URL | `file` | `team-id`, `project-id`, `scene`, `source`, `classify-id`, `app-url` | 所有资源类更新先走上传，再把返回 `url` 写回业务数据，最后执行 update；要进入素材管理必须显式传 `--source material` |
| `dimens-cli sheet create` | 创建项目目录节点或表格节点 | `projectId`, `name` | `type=folder`, `folder-id`, `teamId`, `app-url` | 项目创建后优先补菜单骨架；创建子资源时要显式传 `--folder-id` |
| `dimens-cli sheet update` | 更新资源名称或把已有菜单资源移动到目录 | `teamId`, `projectId`, `sheetId` | `name`, `folder-id`, `app-url` | 已创建资源不会因为目录创建自动归位，移动时必须显式执行 `sheet update --folder-id` |
| `dimens-cli doc create` | 创建在线文档资源 | `teamId`, `projectId`, `title` | `content`, `format`, `parent-id`, `app-url` | 文档是项目核心资源；可在 `content` 中写入 Mermaid 流程图 |
| `dimens-cli doc info` | 获取文档详情和当前内容 | `teamId`, `projectId`, `documentId` | `app-url` | 文档修改前默认先读当前内容和 `version`，后续再改内容并 update |
| `dimens-cli doc update` | 更新 TipTap 在线文档内容 | `teamId`, `projectId`, `documentId`, `content`, `version` | `create-version`, `change-summary`, `app-url` | 必须遵循“先 `doc info` -> 改内容 -> `doc update`”；流程类内容优先补 Mermaid 图表块 |
| `dimens-cli doc attach-file` | 上传附件后把附件节点写入文档 | `teamId`, `projectId`, `documentId`, `file` | `scene`, `app-url` | 内部应先走上传拿 `url`，再把附件节点并入当前文档内容，最后做文档更新 |
| `dimens-cli doc append-image` | 上传图片后把图片节点写入文档 | `teamId`, `projectId`, `documentId`, `file` | `scene`, `app-url` | 内部应先走上传拿 `url`，再把图片节点并入当前文档内容，最后做文档更新 |
| `dimens-cli doc delete` | 删除文档资源 | `teamId`, `projectId`, `documentId` | `app-url` | 删除前建议先确认当前文档归属和用途，避免误删项目说明页 |
| `dimens-cli doc versions` | 查询文档历史版本列表 | `teamId`, `projectId`, `documentId` | `page`, `size`, `app-url` | 适合版本回查、误改排查和恢复前确认 |
| `dimens-cli doc version` | 读取指定文档历史版本 | `teamId`, `projectId`, `documentId`, `version` | `app-url` | 用于确认历史内容，再决定是否恢复 |
| `dimens-cli doc restore` | 恢复文档到指定版本 | `teamId`, `projectId`, `documentId`, `version` | `app-url` | 恢复前最好先查看目标版本内容，避免错误回滚 |
| `dimens-cli report create` | 创建报表主资源 | `projectId`, `name` | `description`, `type`, `app-url` | 只创建报表主资源，后面通常还要继续做 preview、widget-add、query-widget、query |
| `dimens-cli report preview` | 预览报表数据源结果 | `projectId`, `data-source` | `data-mapping`, `params`, `app-url` | 创建或修改组件前默认先执行，用来判断数据源和映射是否可用 |
| `dimens-cli report widget-add` | 给报表新增图表组件 | `projectId`, `reportId`, `type`, `data-source` | `title`, `data-mapping`, `chart-config`, `layout`, `app-url` | 不要跳过预检链，先 preview 再 add 才稳妥 |
| `dimens-cli report query-widget` | 单独试跑一个报表组件 | `projectId`, `reportId`, `widgetId` | `params`, `data-source`, `data-mapping`, `app-url` | 用于验证组件配置是否真实可跑，不要只看创建成功 |

### 强调细节

- 所有更新类操作默认都按“拿数据 -> 改数据 -> 更新数据”执行，项目、文档、报表都不应直接把局部 patch 当通用更新模型。
- 所有资源类更新默认都按“先上传拿 URL -> 把 URL 写回当前业务数据 -> 再 update”执行，项目封面、图标、文档图片、文档附件都走这条链。
- 纯上传拿 URL 和“上传后进入素材管理”不是一回事；后者必须显式带 `--source material`，必要时再补 `--classify-id`。
- 文档相关更新必须先拿 `doc info`，因为内容更新依赖当前文档内容和 `version`，不能跳过版本控制。
- 如果是项目封面、项目图标这类资源字段更新，默认先 `project info` 拿当前数据，再合并上传后的 `url`，最后 `project update`。
- 报表或报表组件更新默认先读当前报表数据，不直接盲改；组件场景还要先确认 `reportId`、当前组件配置和数据映射。

## 核心约束

### 1. 项目是系统落地的最小业务容器

- 团队是最高隔离边界
- 项目是系统建设的第一层业务容器
- 表、字段、视图、角色权限都挂在项目之下继续展开

### 2. 项目创建完成不代表系统可用

项目创建成功后，默认还要继续补：

1. 至少一张核心表
2. 至少一份在线文档
3. 至少一份核心报表
4. 至少一个公开默认视图
5. 至少一组核心字段
6. 若用户要求多人协作，则继续补角色和项目权限

如果项目里包含报表，还应继续补：

7. 至少一次 `report preview`
8. 至少一个 `widget-add`
9. 至少一次 `report query` 或 `report query-widget`

否则项目里的报表大概率只是空壳资源。

推荐理解方式：

- 表格负责承接结构化业务对象
- 文档负责承接 TipTap 在线说明、制度、知识沉淀
- 报表负责承接管理层统计、仪表盘和经营看板
- 目录负责承接项目菜单分层、导航分组和资源归位

目录 + 表格 + 文档 + 报表默认一起构成项目初始化的主导航骨架，不要漏掉其中任何一类再声称项目初始化已闭环。

补充说明：

- 菜单层默认至少考虑 4 类节点：`folder`、`sheet`、`document`、`report`
- 目录节点不是装饰功能，而是项目菜单的真实分层能力；涉及多业务模块时应优先创建
- 创建完资源后，建议立刻用 `sheet tree` 回查项目菜单树，确认目录和资源归位是否正确
- 文档资源不是一次性资源，默认还要支持 `doc info / doc update / doc delete`
- 如果用户要求版本追踪或历史回滚，还要继续支持 `doc versions / doc version / doc restore`
- 如果用户要的是操作手册、制度页、知识沉淀页，通常意味着后续会持续修订，不要只创建不维护
- 如果项目需要更完整的视觉入口，创建项目前可先补一张封面图；优先使用 SVG 工具生成与项目主题一致、`250x150px`、淡色背景、带轻量动态效果的 SVG 封面
- 推荐封面处理链路是：
  1. 用 SVG 工具生成封面
  2. 上传 SVG，拿到 URL
  3. 再进入项目创建主链
- TipTap 文档内容建议至少按“标题 / 段落 / 彩色摘要卡片 / 状态标签 / 提示块 / 清单 / 附件”组织，不要退化成一整段 HTML 或黑白纯文本
- 彩色表达必须服务于信息语义：蓝色用于说明或进行中，绿色用于完成或正常，橙色用于待确认或警告，红色用于风险或异常，紫色用于分类或强调
- 如果文档内容涉及流程、审批、状态流转、系统对接或数据流，默认补一个 Mermaid 图表块，例如 `flowchart TD`、`sequenceDiagram` 或 `stateDiagram-v2`
- 如果文档里包含图片、附件、视频，先区分两层：
  1. 上传能力层：`upload file / upload mode`
  2. 文档写回层：`doc attach-file / doc append-image / doc update`
- 如果只是拿上传结果，走 `upload file`
- 如果目标是把素材直接并入 TipTap 文档，优先走 `doc attach-file` 或 `doc append-image`

### 2.1 用户创建项目时的标准引导路径

当用户说“帮我创建一个项目”时，默认不要把关注点只放在 `project create` 上，而要先把维表建模路径设计清楚。

推荐按下面顺序理解和推进：

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

说明：

- 第 3 步是项目导航骨架步骤，涉及多资源项目时默认不应跳过
- 第 4 到第 7 步是项目落地的基础建模路径，默认不应跳过
- 第 2 步属于展示型项目、模板型项目、知识库项目的常见增强步骤
- 第 8 到第 11 步是按需补齐的后置模块，不是每个项目都必须同权重建设
- 如果项目后续还要持续维护，表格、文档、报表都应视为可继续增改的长期资源

### 3. 项目创建参数要与真实 CLI 对齐

- 推荐使用 `--description` 传项目说明
- 推荐使用 `--project-type` 传项目类型，当前常见值是 `spreadsheet` / `document`
- `--remark` 仅作为兼容备注字段，不替代 `description`

### 4. 项目初始化后续路由

| 下一步目标 | 优先 Skill |
| --- | --- |
| 继续建表、字段、relation、默认视图 | `dimens-manager/references/table/overview.md` |
| 继续做角色、项目权限、行级策略 | `dimens-manager/references/permission/overview.md` |
| 继续补经营看板、统计图表、仪表盘 | `dimens-manager/references/report/overview.md` |
| 回头确认 teamId、成员、上下文来源 | `dimens-manager/references/team/overview.md` |
| 做系统级整体拆解 | `dimens-system-orchestrator` |

### 4.1 报表初始化默认顺序

如果项目初始化阶段就要把报表一起补齐，建议按下面顺序执行：

1. `dimens-cli report create`
2. `dimens-cli report preview`
3. `dimens-cli report widget-add`
4. `dimens-cli report query-widget`
5. `dimens-cli report query`
6. 如需公开，再执行 `dimens-cli report publish`

不要把报表初始化理解成“只创建一个空报表资源”，而要把上面这条顺序当成固定预检链。

### 4.2 三驾马车初始化顺序

如果用户要求“帮我把项目整体搭起来”，默认建议按下面顺序推进：

1. `dimens-cli project create`
2. 看需求补 SVG 动态封面并上传
3. 先规划项目菜单目录
4. 先创建目录节点，再创建表格 / 文档 / 报表资源
5. `dimens-cli sheet create`
6. `dimens-cli doc create`
7. `dimens-cli report create`
8. `dimens-cli sheet tree`
9. `dimens-cli view list`
10. 如缺少默认公开视图，再执行 `dimens-cli view create`
11. `dimens-cli column create`
12. 如果报表要真正可用，再继续执行 `report preview -> report widget-add -> report query-widget -> report query`
13. 如果涉及协作，再继续执行角色和权限主链

注意：

- 三驾马车不是要求每个项目都做得一样重，而是要求初始化时不要漏掉资源类型
- 如果项目要对外展示、进入市场、作为模板使用或强调品牌表达，SVG 动态封面应视为项目入口的一部分
- 如果项目包含多个业务域，目录应先于资源创建被规划好，不要等资源堆出来以后再补菜单层
- 当前菜单层真实能力应通过 `sheet tree` 回查，不要只靠资源列表假设目录已落好
- 文档资源默认走 TipTap 富文本链路，不要误用表格链路代替在线文档；文档维护默认继续走 `doc info / doc update / doc delete`
- 如果用户提到历史版本、误恢复、版本回退，默认继续进入 `doc versions / doc version / doc restore`
- 报表资源默认要走固定预检链，不要只留下空壳
- 如果用户还没提供多表、多字段、关联和案例数据，就不要过早声称项目初始化已闭环

## 必查文档

| Skill / references | 作用 | 什么时候必须看 |
| --- | --- | --- |
| `dimens-manager/references/key-auth/overview.md` | 认证、token 获取与上下文切换 | 执行任何项目命令前必须先确认 |
| `dimens-manager/references/team/overview.md` | 团队、成员、上下文来源 | 缺少 teamId 或上下文不稳时必须看 |
| `dimens-manager/references/table/overview.md` | 项目创建后的建表主链 | 项目创建完成后建议立刻看 |
| `dimens-manager/references/permission/overview.md` | 角色和项目权限主链 | 需要多人协作时建议看 |
| `references/doc-richtext-guidelines.md` | TipTap 文档颜色、状态、附件与图片写法约束 | 处理在线文档时必须看 |
| `references/examples.md` | 项目命令与初始化案例 | 直接执行时建议先看 |
| `references/bootstrap-flow.md` | 从项目到建表/权限的端到端初始化顺序 | 用户要求一步到位时必须看 |

## 使用场景示例

### 场景 1：创建 CRM 项目

```bash
dimens-cli project create \
  --team-id TTFFEN \
  --name 客户管理系统 \
  --description 客户全生命周期管理 \
  --project-type spreadsheet
```

创建完成后建议立刻继续：

1. 看需求补 SVG 动态封面并上传
2. `dimens-cli sheet create --type folder`
3. `dimens-cli sheet create --folder-id FOLDER_SHEET_ID`
4. `dimens-cli doc create --parent-id FOLDER_SHEET_ID`
5. `dimens-cli report create`
6. `dimens-cli sheet tree`
7. `dimens-cli view list`
8. 若没有默认公开视图，再执行 `dimens-cli view create`
9. `dimens-cli column create`
10. 如果还要管理层看板，再继续 `dimens-cli report preview -> report widget-add -> report query-widget -> report query`

### 场景 2：用户只给了维表链接

如果用户给的是：

```text
https://dimens.bintelai.com/#/TTFFEN/PXWXBJQ/
```

默认解释为：

- `teamId = TTFFEN`
- `projectId = PXWXBJQ`

这时不需要重复追问项目来源，而是直接进入项目初始化后的下一步操作。

### 场景 3：创建文档型项目

```bash
dimens-cli project create \
  --team-id TTFFEN \
  --name 知识库项目 \
  --description 内部知识沉淀空间 \
  --project-type document
```

创建项目后建议立刻继续：

```bash
dimens-cli doc create \
  --team-id TTFFEN \
  --project-id PROJECT_ID \
  --title 产品说明文档 \
  --content '<p>欢迎使用在线文档</p>' \
  --format richtext
```

如果要做文档闭环维护，继续：

```bash
dimens-cli doc info \
  --team-id TTFFEN \
  --project-id PROJECT_ID \
  --document-id DOC_ID

dimens-cli doc update \
  --team-id TTFFEN \
  --project-id PROJECT_ID \
  --document-id DOC_ID \
  --content '<p>更新后的在线文档</p>' \
  --version 1 \
  --create-version true \
  --change-summary 补充项目说明

dimens-cli doc delete \
  --team-id TTFFEN \
  --project-id PROJECT_ID \
  --document-id DOC_ID
```

如果文档需要带颜色块、状态标签、图片或附件，先看 `references/doc-richtext-guidelines.md`，再组织 `--content`。

## 常见错误与排查

| 错误现象 | 根本原因 | 解决方案 |
| --- | --- | --- |
| 项目创建成功，但后续建表报缺少上下文 | 没切换默认项目，也没显式传 `projectId` | 继续执行 `auth use-project` 或显式传 `--project-id` |
| 技能里写了 `description`，CLI 落不进去 | 用了旧命令口径或 CLI 未同步 | 当前应使用 `--description`，并确认 CLI 已升级 |
| 项目建好了，但前端表无法筛选 | 只建了项目和表，没补默认公开视图 | 继续执行 `view list` / `view create` |
| 项目里想创建在线文档却失败 | 只按表格链路初始化，没走文档主链 | 使用 `dimens-cli doc create` 创建 TipTap 在线文档 |
| 文档创建完后不知道怎么继续维护 | 误以为在线文档只有创建命令 | 继续使用 `dimens-cli doc info / doc update / doc delete` 做回查、修订和清理 |
| 项目里需要经营看板却没有报表入口 | 只初始化了表格或文档，没把报表作为核心资源补齐 | 使用 `dimens-cli report create` 先补报表主资源 |
| 项目里已经有报表资源，但图表还是空的 | 只创建了报表，没有继续预览数据源和创建组件 | 按 `report create -> report preview -> report widget-add -> report query-widget -> report query` 的固定预检链继续补齐 |
| 项目初始化做完了，但其实只有单一资源 | 没按“三驾马车”理解项目资源 | 回到表格、文档、报表三类资源，确认哪些还没补齐 |
| 项目能打开，但多人协作没权限 | 只创建了项目，没有继续配置角色和项目权限 | 继续路由到 `dimens-manager/references/permission/overview.md` |

## 参考文档

- `references/examples.md`
- `references/bootstrap-flow.md`
