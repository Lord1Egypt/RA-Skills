# dimens-manager 项目初始化章节 项目初始化案例

## 1. 创建项目

```bash
dimens-cli project create \
  --team-id TTFFEN \
  --name 客户管理系统 \
  --description 客户全生命周期管理 \
  --project-type spreadsheet
```

说明：

- `--description` 用于项目说明
- `--project-type` 当前常见值是 `spreadsheet` / `document`

## 1.1 创建项目前先补 SVG 动态封面

如果项目需要更强的品牌感、展示感或模板感，推荐先用 SVG 工具生成封面，再上传拿 URL，最后进入项目创建。

推荐封面要求：

- 封面应符合项目主题
- 使用 SVG
- 尺寸固定为 `250x150px`，建议写入 `width="250" height="150" viewBox="0 0 250 150"`
- 使用淡色背景，例如浅蓝、浅紫、浅绿、浅橙或浅灰渐变
- 具备轻量动态动画效果，例如慢速漂浮、淡入淡出、轻微位移或渐变流动
- 避免高饱和强对比、快速闪烁、大面积复杂动画
- 能直接作为项目封面使用

推荐链路：

```bash
dimens-cli upload file --file ./project-cover.svg --team-id TEAM_ID --scene project-cover
```

说明：

- `project-cover.svg` 由 SVG 工具提前生成，不要求手工绘制；必须符合 `250x150px`、淡色背景、轻量动态效果
- 上传成功后，拿到返回的 `url`
- 后续创建项目时，把这张 SVG 视为项目封面资源
- 如果当前项目创建命令还没有显式封面参数，技能层也应先保留这个封面 URL，供后续项目封面配置或项目展示页使用

## 2. 创建项目后立即校验

```bash
dimens-cli project list --team-id TTFFEN --output json
dimens-cli project info --team-id TTFFEN --id PROJECT_ID --output json
```

## 3. 创建项目菜单目录并回查

创建项目后，不要直接只建资源，先把菜单目录规划出来，尤其不要漏掉目录功能。

当前菜单层建议至少包含：

- 目录
- 表格
- 报表
- 文档

回查菜单树：

```bash
dimens-cli sheet tree --project-id PROJECT_ID
```

建议菜单结构示意：

1. 目录：客户中心
2. 目录：项目文档
3. 目录：经营分析
4. 表格：客户表、联系人表
5. 文档：项目说明文档
6. 报表：销售漏斗

说明：

- 目录节点要优先规划，不要等资源全建完再补
- 如果后续资源较多，目录能直接决定项目导航是否清晰
- `sheet tree` 是当前最直接的菜单树回查方式

### 3.1 项目初始化命令清单

下面这组命令可以直接作为“创建项目后的第一轮初始化清单”使用：

```bash
dimens-cli project create \
  --team-id TTFFEN \
  --name 客户管理系统 \
  --description 客户全生命周期管理 \
  --project-type spreadsheet

dimens-cli upload file --path ./project-cover.svg --team-id TTFFEN --scene project-cover --source material

dimens-cli sheet create \
  --project-id PROJECT_ID \
  --name 客户中心 \
  --type folder

dimens-cli sheet create \
  --project-id PROJECT_ID \
  --name 项目文档 \
  --type folder

dimens-cli sheet create \
  --project-id PROJECT_ID \
  --name 经营分析 \
  --type folder

dimens-cli sheet create \
  --project-id PROJECT_ID \
  --name 客户表 \
  --folder-id FOLDER_CUSTOMER_ID

dimens-cli sheet create \
  --project-id PROJECT_ID \
  --name 联系人表 \
  --folder-id FOLDER_CUSTOMER_ID

dimens-cli doc create \
  --team-id TTFFEN \
  --project-id PROJECT_ID \
  --title 项目说明文档 \
  --parent-id FOLDER_DOC_ID \
  --format richtext

dimens-cli report create \
  --project-id PROJECT_ID \
  --name 销售漏斗

dimens-cli sheet update REPORT_SHEET_ID \
  --team-id TTFFEN \
  --project-id PROJECT_ID \
  --folder-id FOLDER_REPORT_ID

dimens-cli sheet tree --project-id PROJECT_ID
```

说明：

- `project-cover.svg` 建议由 SVG 工具提前生成，要求符合项目主题、`250x150px`、淡色背景且具备轻量动态效果；上传文件名必须保留 `.svg`，CLI 会按 `image/svg+xml` 提交
- `FOLDER_CUSTOMER_ID`、`FOLDER_DOC_ID` 等目录 ID 可以在创建目录后，从返回结果里拿到
- 文档当前走 `doc create --parent-id` 挂到目录下；表格当前走 `sheet create --folder-id`
- 创建目录只会生成目录节点，不会自动把其他菜单移动进去；已存在的表格/报表/目录资源必须再执行 `sheet update --folder-id`
- 报表创建返回的 `reportId` 等于菜单资源 `sheetId`，如果需要移动到目录，使用这个 ID 执行 `sheet update REPORT_SHEET_ID --folder-id FOLDER_REPORT_ID`
- `sheet tree` 是这组命令的最后一步，不要省略

## 4. 切换默认项目

```bash
dimens-cli auth use-project PROJECT_ID
```

## 5. 项目内在线文档案例

```bash
dimens-cli doc create \
  --team-id TTFFEN \
  --project-id PROJECT_ID \
  --title 项目说明文档 \
  --content '<p>欢迎使用在线文档</p>' \
  --format richtext

dimens-cli doc info \
  --team-id TTFFEN \
  --project-id PROJECT_ID \
  --document-id DOC_ID

dimens-cli doc update \
  --team-id TTFFEN \
  --project-id PROJECT_ID \
  --document-id DOC_ID \
  --content '<p>更新后的项目说明</p>' \
  --version 1 \
  --create-version true \
  --change-summary 补充项目背景

dimens-cli doc versions \
  --team-id TTFFEN \
  --project-id PROJECT_ID \
  --document-id DOC_ID \
  --page 1 \
  --size 20

dimens-cli doc version \
  --team-id TTFFEN \
  --project-id PROJECT_ID \
  --document-id DOC_ID \
  --version 2

dimens-cli doc restore \
  --team-id TTFFEN \
  --project-id PROJECT_ID \
  --document-id DOC_ID \
  --version 2
```

说明：

- 文档维护主链是 `doc create / doc info / doc update / doc delete`
- 如果要回看历史版本或恢复旧内容，继续走 `doc versions / doc version / doc restore`
- 文档内容默认按 TipTap 富文本理解，不要退化成纯文本备注或黑白单调页面
- 用户创建文档时，默认至少补状态标签、淡色摘要卡片或提示块，让文档更生动但保持可读
- 如果文档涉及业务流程、审批流、状态流转或系统对接，优先用 Mermaid 图表块写入文档内容，不要截图上传
- 如果文档里要放状态标签、提示色块、图片或附件，先参考 `doc-richtext-guidelines.md`

## 5.1 带颜色状态的文档更新示例

```bash
dimens-cli doc update \
  --team-id TTFFEN \
  --project-id PROJECT_ID \
  --document-id DOC_ID \
  --version 1 \
  --create-version true \
  --change-summary 补充发布状态 \
  --content '<h1>项目发布说明</h1><div style="background:#eff6ff;color:#1d4ed8;border-left:4px solid #60a5fa;padding:12px 14px;border-radius:10px;margin:12px 0;"><strong>发布摘要：</strong>本次发布包含字段颜色规范、文档规范和附件能力。</div><p><span style="background:#dbeafe;color:#1d4ed8;padding:2px 8px;border-radius:999px;">发布中</span><span style="background:#ecfdf5;color:#047857;padding:2px 8px;border-radius:999px;margin-left:8px;">已校验</span></p>'
```

说明：

- 这是当前 CLI 已能直接承接的能力，因为 `doc update` 支持直接传富文本内容
- 样式要服务于状态语义，不要把整篇文档写满颜色
- 建议使用淡色背景卡片、状态标签和提示块点缀，不要只生成黑白正文

## 5.2 带 Mermaid 业务流程图的文档更新示例

```bash
dimens-cli doc update \
  --team-id TTFFEN \
  --project-id PROJECT_ID \
  --document-id DOC_ID \
  --version 1 \
  --create-version true \
  --change-summary 补充客户流程图 \
  --content '<h1>客户管理流程</h1><p>下面是从线索到合同的核心业务流程。</p><pre data-type="mermaid"><code>flowchart LR
  Lead[线索录入] --> Customer[客户建档]
  Customer --> Opportunity[商机推进]
  Opportunity --> Contract[合同签署]
  Opportunity --> Follow[继续跟进]
</code></pre>'
```

说明：

- Mermaid 图适合写业务流程图、审批流、状态流转、接口调用顺序
- 更新已有文档时仍必须先 `doc info` 拿当前内容和 `version`，再替换目标 Mermaid 图块

## 5.3 文件与图片上传链路

当前要明确区分：

- 产品接口层已经存在上传接口：`POST /app/base/comm/upload`
- `dimens-cli` 已有独立上传命令：`upload file`、`upload mode`
- 如果目标是把素材继续写回文档，优先走：`doc attach-file`、`doc append-image`

推荐链路 1：只上传文件

```bash
dimens-cli upload file --path ./release.pdf
dimens-cli upload mode
```

推荐链路 2：上传后直接追加文档附件

```bash
dimens-cli doc attach-file \
  --team-id TTFFEN \
  --project-id PROJECT_ID \
  --document-id DOC_ID \
  --file ./release.pdf \
  --title 发布清单.pdf
```

推荐链路 3：上传后直接追加文档图片

```bash
dimens-cli doc append-image \
  --team-id TTFFEN \
  --project-id PROJECT_ID \
  --document-id DOC_ID \
  --file ./cover.png \
  --alt 系统封面图
```

推荐链路 4：如果需要完全自定义 TipTap HTML 或 Mermaid 图表，再自行组合 `doc update --content ...`

## 6. 继续进入建表主链

```bash
dimens-cli sheet create --team-id TTFFEN --project-id PROJECT_ID --name 客户表
dimens-cli view list --team-id TTFFEN --project-id PROJECT_ID --sheet-id SHEET_ID
```

如果还没有默认公开视图：

```bash
dimens-cli view create \
  --team-id TTFFEN \
  --project-id PROJECT_ID \
  --sheet-id SHEET_ID \
  --name 默认视图 \
  --type grid \
  --is-public true \
  --config '{"filters":[],"filterMatchType":"and","sortRule":null,"groupBy":[],"hiddenColumnIds":[],"rowHeight":"medium"}'
```

## 7. 继续进入权限主链

```bash
dimens-cli role create \
  --app-url https://dimens.bintelai.com/#/TTFFEN/PROJECT_ID/ \
  --name 销售 \
  --description CRM 销售角色 \
  --can-manage-sheets false \
  --can-edit-schema false \
  --can-edit-data true
```
