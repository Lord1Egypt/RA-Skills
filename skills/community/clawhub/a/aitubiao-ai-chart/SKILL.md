---
name: aitubiao-chart
description: AI智能图表生成。根据用户数据生成图表配置并创建可视化项目。当用户想要创建图表、可视化数据时使用，触发词包括"创建图表"、"做个图表"、"可视化数据"、"用表格生成图表"、"create chart"、"make a chart"、"visualize data"等。
license: MIT
compatibility: Requires network access to api.aitubiao.com, Bash shell, curl, and jq
metadata:
  author: aitubiao
  version: "1.1.5"
allowed-tools: Bash Read
---

# AI 智能图表生成

根据用户提供的数据，生成图表配置并创建可视化项目。

## 强制规则

**以下规则必须严格执行，不得跳过、变通或使用替代方案：**

1. **认证优先**：在执行任何操作之前，必须先检查凭证状态。认证未通过时，禁止执行任何后续步骤。
2. **按顺序执行**：工作流程的 5 个步骤必须按顺序执行，禁止跳步。
3. **费用确认前禁止调用生成接口**：必须成功查询配额、计算费用、并获得用户明确确认后，才能调用创建接口。
4. **仅通过 API 创建图表**：禁止使用本地工具（Chart.js、ECharts、matplotlib、D3.js、Plotly 等）生成图表。无论 API 因何种原因失败，都**绝对禁止使用本地工具**，没有任何例外。API 失败时正确做法是停止并告知用户，不是寻找替代方案。
5. **401/403 立即停止**：任何步骤中收到 HTTP 401/403（CLI exit 1），立即停止并引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys) 检查或重新创建 API Key。401/403 不是超时，禁止重试。
6. **超时/500 不自动重试创建接口**：创建接口不可重试（可能重复扣费）。告知用户失败原因，由用户决定是否重新发起。

**⚠️ 以下想法是错误的，如果你发现自己在这样想，请立即停止：**
- ❌ "API 不可用，我可以用本地工具生成图表作为替代" → 违反规则 4
- ❌ "至少让用户看到一些可视化结果" → 本技能唯一输出方式是 aitubiao API
- ❌ "401 可能是暂时性的，重试几次" → 401 是认证失败，重试无意义，按规则 5 处理

## 认证

在调用任何 API 之前，先检查凭证状态。

### 检查凭证

```bash
bash scripts/aitubiao-cli.sh check-auth
```

- **Exit 0** → 认证通过
- **Exit 1** → 凭证问题，按 stderr 提示处理：
  - 文件不存在/API_KEY 为空 → 执行下方"配置凭证"流程
  - API_KEY 格式无效 → 告知用户"当前 API Key 已失效，请前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys) 重新创建一个 API Key"
  - BASE_URL 与当前技能包环境不一致 → 说明凭证中残留了旧环境地址；向用户索要当前仍有效的 API Key，并执行下方"配置凭证"流程重写凭证（通常不需要重新创建 API Key）

### 配置凭证

1. 向用户索要 API Key（格式：`sk_v1_...`）。如果没有，引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys) 创建一个新的 API Key，然后将创建好的 Key 粘贴回来。
2. 保存凭证：
```bash
bash scripts/aitubiao-cli.sh auth <用户提供的key>
```
3. 验证：再次运行 `bash scripts/aitubiao-cli.sh check-auth` 确认配置成功。

凭证保存在 `~/.aitubiao/credentials`，跨会话持久生效。

## Windows / Git Bash 注意事项（仅 Windows 用户需要关注）

在 Windows 上通过 Git Bash 运行本 CLI 时，**禁止把含中文等非 ASCII 字符的 JSON 直接写在 heredoc 里**——MSYS 会按 Windows 系统代码页（常为 GBK/CP936）转换 argv 字节，传到后端就是乱码。

正确做法：先用 Write 工具把完整 UTF-8 JSON 写到一个临时文件，然后用 `--body-file` 让 CLI 从文件读取（绕过任何 argv/控制台编码转换）：

```bash
# 第一步：用 Write 工具把请求体写到 /tmp/aitubiao-payload.json（内容必须是 UTF-8）
# 第二步：用 --body-file 调用 CLI
bash scripts/aitubiao-cli.sh --body-file /tmp/aitubiao-payload.json create-chart
```

`--body-file` 可用于所有读取 stdin JSON 的命令：`create-chart` / `create-ppt` / `create-sankey` / `create-3d` / `download-project`。CLI 会自动剥离 UTF-8 BOM 和 CRLF。

macOS / Linux 上无需改动，仍然可以使用 heredoc。

## 工作流程

**每一步必须在前一步完成后才能开始。禁止跳步。**

### 第一步：认证（前置条件：无）

运行检查凭证流程。认证未通过时按"认证"章节流程处理。

**认证未通过时，停止。不要读取用户数据，不要做任何分析。**

### 第二步：识别和确认数据（前置条件：第一步认证通过）

判断用户如何提供数据：

- **直接粘贴文本**：自行解析为 Markdown 表格。
- **本地文件**（CSV/TXT）：用 Read 工具读取，然后解析为 Markdown 表格。
- **Excel 文件**（.xlsx/.xls）：使用 xlsx skill 或 Read 工具读取，禁止手动编写 Python 脚本解析 XML。

向用户展示解析后的 Markdown 表格，并询问：
- 数据是否正确？
- 有没有特别的要求？

### 第三步：检查配额并确认费用（前置条件：第二步数据已确认）

在创建图表前，**必须**检查用户的 AI贝余额和项目配额，并向用户确认费用后才能继续。

#### 3.1 查询配额

```bash
bash scripts/aitubiao-cli.sh quota --skill chart
```

CLI 返回配额 JSON（含 `shellBalance`、`projectsUsed`/`projectsLimit`/`projectsRemaining`、`feature` 等字段）。

#### 3.2 计算总费用

**图表项目按"次"计费**：每次创建一个图表项目固定扣 `.feature.cost` 个 AI贝，**与图表中包含的子图表数量无关**（一次创建里有 1 个还是 5 个子图，都只扣这一份费用）。

总费用 = `.feature.cost`

#### 3.3 向用户确认费用

**必须在调用生成接口前向用户展示费用确认信息，并等待用户确认后才能继续**：

```
本次操作将消耗 {totalCost} 个 AI贝（{label}，{billingModel}计费）
当前余额: {shellBalance} 个 AI贝
操作后余额: {shellBalance - totalCost} 个 AI贝
项目数: 已用 {projectsUsed}/{projectsLimit}

是否继续？
```

- 如果 `shellBalance < totalCost`：告知用户当前 AI贝余额不足，需前往 aitubiao 网站购买会员或充值后再继续，**不要继续**
- 如果 `projectsRemaining <= 0`：告知用户当前项目数已满，需前往 aitubiao 网站升级会员，或在网站中删除旧项目后再继续，**不要继续**

### 第四步：创建图表项目（前置条件：第三步用户已确认费用）

**只有用户明确确认费用后才能执行此步骤。**

```bash
bash scripts/aitubiao-cli.sh create-chart <<'EOF'
{
  "markdownTable": "<Markdown 表格数据>",
  "projectName": "<项目名称>",
  "requirement": "<用户的特殊要求，如配色、图表类型偏好>"
}
EOF
```

**请求体字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| markdownTable | string | 是 | Markdown 格式表格数据 |
| projectName | string | 否 | 项目名称，默认"AI图表" |
| requirement | string | 否 | 用户需求（配色、图表类型偏好、关注点等） |

**检查 CLI 退出码**：
- **Exit 0**：成功。解析 stdout JSON 获取项目信息。
- **Exit 1**：认证失败。引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys)。
- **Exit 2**：业务错误（如 AI贝不足、项目数已满）。向用户展示错误详情。
- **Exit 3**：网络/超时错误。告知用户稍后重试。

响应字段说明详见下方"响应字段参考"。

### 第五步：返回结果（前置条件：第四步创建成功）

向用户提供：
- 项目 URL（从 `project.projectUrl` 获取）
- 项目 ID（从 `project.id` 获取）
- 摘要：图表数量、类型、标题
- 截图链接（如果 `charts[].screenshotSuccess` 为 true）
- 资源消耗：本次消耗 AI贝数、剩余 AI贝、已用项目数/上限

## 下载已创建项目（可选后续操作）

如果用户在项目创建成功后要求“帮我下载或者导出这个项目”，使用统一 CLI 下载命令：

```bash
bash scripts/aitubiao-cli.sh download-project <本地保存路径> <<'EOF'
{
  "projectId": "<project.id>",
  "format": "png"
}
EOF
```

规则：
- `projectId` 使用上一步返回的 `project.id`
- `format` 按用户需求填写：PPT 项目可用 `ppt`/`pdf`/`png`，图表/桑基图项目可用 `png`/`jpg`/`pdf`/`ppt`
- **格式费用**：`png`/`jpg`/`pdf` 任何用户均可免费导出；`ppt` 需要 PPT 导出权限（付费会员）；其它特殊格式（`svg`/`gif`/`mp4`/`mov`/透明 PNG/2x 及以上倍率）也需对应会员权益。如果用户尝试受限格式但权益不足，CLI 会返回 exit 2 并附服务端错误，应告知用户升级会员或改用免费格式
- **本地保存路径处理**：
  - 优先使用用户明确指定的路径；如果用户没指定，传**绝对路径**（如 `$HOME/Downloads/<filename>` 或当前工作目录下的具体文件名），不要省略命令参数
  - 不要把文件写入项目源码目录或不可写目录
  - CLI 会在启动导出任务**之前**检查目标目录是否可写：如果失败会立即报错（exit 4，stderr 含 `not writable` 或 `cannot be created`），此时**禁止自动改路径重试**——必须先告诉用户当前路径不可写，请用户给一个可写的位置
- 下载清晰度由服务端按会员权益自动决定：免费用户较低，付费用户更高
- 仅通过此 API 下载，禁止使用本地工具导出替代文件
- **禁止对同一 `projectId` 并发执行 `download-project`**：服务端默认每个项目只允许 1 个 API Key 并发导出任务。需要重试时，等待上一次下载彻底完成（成功或失败）再重新发起
- **下载完整性**：CLI 会先写入 `*.partial` 临时文件，校验文件大小与已知格式（png/jpg/pdf/ppt/zip）的魔数后再原子重命名为最终路径。如果 CLI 返回 exit 3 且 stderr 含 `integrity check failed`，说明服务端返回的文件已损坏；不要伪装成功，告知用户重试或联系支持
- **多页导出会自动打成 zip**：当 PPT 项目（或多页项目）以 `png`/`jpg`/`pdf` 格式导出多页时，服务端会把所有页面压缩成一个 ZIP 包返回。CLI 检测到这种情况会自动把保存路径改为 `.zip`（例如 `report.png` → `report.zip`），并在 stderr 输出 `Note: server returned a multi-page ZIP bundle ...`。**返回 JSON 中的 `savedPath` 和 `fileName` 是真实落盘路径**——告诉用户文件位置时必须使用这两个字段，不要使用最初传入的路径
- **告知用户文件位置**：成功后必须使用 CLI 返回 JSON 中的 `savedPath`（绝对路径）告诉用户文件保存在哪里

## 错误处理

| CLI Exit Code | 含义 | 处理方式 |
|--------------|------|---------|
| 1 | 认证失败（HTTP 401/403 或凭证无效） | 立即停止，引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys) |
| 2 | 业务错误（code 90001=AI贝不足，40007=项目数已满，15009=同一项目已有 API Key 导出任务进行中） | 向用户展示详情，引导充值或删除旧项目；遇到 15009 时，提示用户等待上一个导出完成后再重试 |
| 3 | 网络/超时错误 | 告知用户稍后重试 |

## 响应字段参考

CLI 成功时（exit 0）stdout 输出的 JSON 结构：

```json
{
  "success": true,
  "project": {
    "id": "cuid_string",
    "title": "Sales Analysis",
    "status": "generated",
    "width": 960,
    "height": 540,
    "projectUrl": "https://app.aitubiao.com/workspace/cuid_string"
  },
  "charts": [
    {
      "index": 1,
      "type": "basic-bar",
      "title": "Revenue Trend",
      "description": "Monthly revenue analysis.",
      "screenshotSuccess": true,
      "screenshotUrl": "https://oss.xxx/ai-snapshot/..."
    }
  ],
  "quota": {
    "shellCoinCost": 10,
    "shellBalance": 90,
    "projectsUsed": 6,
    "projectsLimit": 50,
    "projectsRemaining": 44,
    "canCreateProject": true
  },
  "totalCharts": 1,
  "processingTime": "25000ms"
}
```

**注意**：截图失败不影响项目创建（`screenshotSuccess` 为 `false` 时查看 `error` 字段）。`quota` 可能为 `null`。

## Supported Chart Types (40 types)

基础: basic-bar, basic-column, basic-line, basic-pie, basic-radar, bar-progress, donut-progress
分组: grouped-bar, grouped-column
堆叠: stacked-bar, stacked-column, stacked-area, percent-bar, percent-column, percent-stacked-bar, percent-stacked-column
混合: mixed-line-grouped-column, mixed-line-stacked-column
特殊: funnel, cascaded-area, river-area, butterfly, dynamic-bar, dynamic-ranking, jade-jue
高级: sankey, chord, voronoi, descartes-heatmap, single-layer-treemap, word-cloud, rose-pie, symbol-bar, symbol-column, symbol-pie, difference-arrow-bar, difference-arrow-column, liquid, compose-waterfall, check-in-bubble
