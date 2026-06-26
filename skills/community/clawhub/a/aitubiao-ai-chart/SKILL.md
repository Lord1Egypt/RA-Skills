---
name: 爱图表-智能图表
description: AI智能图表生成。用户上传数据或粘贴表格，自动生成可视化图表（柱状图、折线图、饼图、词云图、桑基图、地图等40+种）。触发词：创建图表、做图表、可视化数据、用表格生成图表、柱状图、折线图、饼图、词云图、create chart、make a chart、visualize data。
license: MIT
license: MIT
compatibility: Requires network access to api.aitubiao.com, Bash shell, curl, and jq
metadata:
  author: aitubiao
  version: "1.2.3"
allowed-tools: Bash Read Write
---

# AI 智能图表生成

根据用户提供的数据，生成图表配置并创建可视化项目。

## 强制规则

**以下规则必须严格执行，不得跳过、变通或使用替代方案：**

1. **认证优先**：在执行任何操作之前，必须先检查凭证状态。认证未通过时，禁止执行任何后续步骤。
2. **按顺序执行**：工作流程的 5 个步骤必须按顺序执行，禁止跳步。
3. **费用确认前禁止调用生成接口**：必须成功查询配额、计算费用、并获得用户明确确认后，才能调用创建接口。
4. **仅通过 API 创建图表**：禁止使用本地工具（Chart.js、ECharts、matplotlib、D3.js、Plotly 等）生成图表。无论 API 因何种原因失败，都**绝对禁止使用本地工具**，没有任何例外。API 失败时正确做法是停止并告知用户，不是寻找替代方案。
5. **401/403 立即停止**：任何步骤中收到 HTTP 401/403（CLI exit 1），立即停止并引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) 检查或重新创建 API Key。401/403 不是超时，禁止重试。
6. **超时/500 不自动重试创建接口**：创建接口不可重试（可能重复扣费）。告知用户失败原因，由用户决定是否重新发起。
7. **多图一次调用**：用户要求 N 张图且 1 ≤ N ≤ 10 时，只调用一次 `create-chart`，请求体设置 `"maxCharts": N`；禁止按每张图循环调用 CLI。
8. **Windows 禁止脚本整理数据**：CSV/TXT 用 Read 读取，请求体用 Write 写 UTF-8 JSON 文件；禁止用 Python、PowerShell、heredoc、echo 或 shell 重定向整理数据或生成 JSON。

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
  - API_KEY 格式无效 → 告知用户"当前 API Key 已失效，请前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) 重新创建一个 API Key"
  - BASE_URL 与当前技能包环境不一致 → 说明凭证中残留了旧环境地址；向用户索要当前仍有效的 API Key，并执行下方"配置凭证"流程重写凭证（通常不需要重新创建 API Key）

### 配置凭证

1. 向用户索要 API Key（格式：`sk_v1_...`）。如果没有，引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) 创建一个新的 API Key，然后将创建好的 Key 粘贴回来。
2. 保存凭证：
```bash
bash scripts/aitubiao-cli.sh auth <用户提供的key>
```
3. 验证：再次运行 `bash scripts/aitubiao-cli.sh check-auth` 确认配置成功。

凭证保存在 `~/.aitubiao/credentials`，跨会话持久生效。

## Windows 编码注意事项（仅 Windows 用户需要关注）

在 Windows 上，**禁止用 PowerShell / Python / heredoc / echo / Set-Content / shell 重定向来生成含中文等非 ASCII 字符的 JSON 请求体**。这些方式容易经过 Windows 系统代码页（常为 GBK/CP936）或 MSYS argv 转换，导致传到后端的中文乱码。

正确做法：先用 Write 工具把完整 UTF-8 JSON 写到临时文件，然后用 `--body-file` 让 CLI 从文件读取，绕过 argv/控制台编码转换。

Windows 调用：

```bat
scripts\aitubiao-cli.cmd --body-file C:\Users\%USERNAME%\AppData\Local\Temp\aitubiao-payload.json create-chart
```

Git Bash 调用：

```bash
bash scripts/aitubiao-cli.sh --body-file /tmp/aitubiao-payload.json create-chart
```

`--body-file` 可用于所有读取 stdin JSON 的命令：`create-chart` / `create-ppt` / `create-sankey` / `create-3d` / `download-project`。CLI 会自动剥离 UTF-8 BOM 和 CRLF。

CSV/TXT 文件也只用 Read 工具读取。不要写 Python/PowerShell 脚本做本地解析、转码或聚合；如果 Read 出来的文本已经明显乱码，要求用户提供 UTF-8 文件或直接粘贴数据。

macOS / Linux 上仍可使用 heredoc，但包含中文的请求体也优先使用 `--body-file`。

## 工作流程

**每一步必须在前一步完成后才能开始。禁止跳步。**

### 第一步：认证（前置条件：无）

运行检查凭证流程。认证未通过时按"认证"章节流程处理。

**认证未通过时，停止。不要读取用户数据，不要做任何分析。**

### 第二步：识别和确认数据（前置条件：第一步认证通过）

判断用户如何提供数据：

- **直接粘贴文本**：自行解析为结构化数据。
- **本地文件**（CSV/TXT）：用 Read 工具读取，然后整理为结构化数据；不要用 Python/PowerShell 脚本读取、转码、聚合。
- **Excel 文件**（.xlsx/.xls）：使用 xlsx skill 或 Read 工具读取，禁止手动编写 Python 脚本解析 XML。

把用户已确认要画图的数据整理成结构化 `sources` 数组：每张表给一个 `index`（0-based）、可选 `title`、`header`（列名数组）、`rows`（二维数组，单元格只能是字符串或数字）。后端不再做任何文本解析。

向用户展示整理后的数据预览，并询问：
- 数据是否正确？
- 有没有特别的要求？

同时确定图表数量：

- 用户明确要求 N 张图：`maxCharts = N`，N 必须在 1-10 之间。
- 用户未指定数量：使用默认 `maxCharts = 5`。
- 用户要求超过 10 张图：按每批最多 10 张拆分；每批都是一次独立创建，费用确认时说明总批次数和总预扣费用。

### 第三步：检查配额并确认费用（前置条件：第二步数据已确认）

在创建图表前，**必须**检查用户的 AI贝余额和项目配额，并向用户确认费用后才能继续。

#### 3.1 查询配额

```bash
bash scripts/aitubiao-cli.sh quota --skill chart
```

CLI 返回配额 JSON（含 `shellBalance`、`projectsUsed`/`projectsLimit`/`projectsRemaining`、`feature` 等字段）。

#### 3.2 计算总费用

**图表项目按"个"计费**：单图单价 = `.feature.cost` 个 AI贝。创建接口会先按 `maxCharts × .feature.cost` 预扣，若实际生成数量少于 `maxCharts`，服务端会按实际生成数自动部分退款。

预估最高费用 = `maxCharts × .feature.cost`。`maxCharts` 使用第二步确定的图表数量；未指定数量时默认 5。

#### 3.3 向用户确认费用

**必须在调用生成接口前向用户展示费用确认信息，并等待用户确认后才能继续**：

```
本次操作最多预扣 {maxCharts × cost} 个 AI贝（{cost} AI贝/个 × {maxCharts} 个）
当前余额: {shellBalance} 个 AI贝
预扣后余额: {shellBalance - maxCharts × cost} 个 AI贝（实际生成较少时会自动部分退款）
项目数: 已用 {projectsUsed}/{projectsLimit}

是否继续？
```

- 如果 `shellBalance < maxCharts × cost`：告知用户当前 AI贝余额不足，需前往 aitubiao 网站购买会员或充值后再继续，**不要继续**
- 如果 `projectsRemaining <= 0`：告知用户当前项目数已满，需前往 aitubiao 网站升级会员，或在网站中删除旧项目后再继续，**不要继续**

### 第四步：创建图表项目（前置条件：第三步用户已确认费用）

**只有用户明确确认费用后才能执行此步骤。**

先用 Write 工具把请求体保存为 UTF-8 JSON 文件。

请求体文件内容：

```json
{
  "sources": [
    {
      "index": 0,
      "title": "<可选：源表标题>",
      "header": ["<列名1>", "<列名2>"],
      "rows": [
        ["<标签>", 100],
        ["<标签>", 150]
      ]
    }
  ],
  "maxCharts": 3,
  "projectName": "<项目名称>",
  "requirement": "生成3张图，覆盖用户要求的多个分析角度"
}
```

macOS / Linux 调用：

```bash
bash scripts/aitubiao-cli.sh --body-file <请求体文件路径> create-chart
```

Windows 调用：

```bat
scripts\aitubiao-cli.cmd --body-file <请求体文件路径> create-chart
```

**请求体字段说明**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| sources | array | 是 | 结构化数据源数组，最多 10 个。每项含 `index` / `title?` / `header` / `rows`，详见下方嵌套字段说明 |
| markdownTable | string | 否 | **已废弃**，仅用于旧客户端兼容。`sources` 与 `markdownTable` 至少提供其一 |
| maxCharts | number | 否 | 预期最多生成图表数，范围 1–10；用户要求 N 张图时填 N，未指定时默认 5；按 `maxCharts × .feature.cost` 预扣 AI贝，实际生成较少时部分退款 |
| projectName | string | 否 | 项目名称，默认"AI图表" |
| requirement | string | 否 | 用户需求（配色、图表类型偏好、关注点等） |

**`sources[].*` 嵌套字段**：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| index | number | 是 | 源表 0-based 下标，多源场景用于绑定每张图与源表 |
| title | string | 否 | 源表标题，作为 plan / per-chart prompt 的语义锚点 |
| header | string[] | 是 | 列名数组，非空 |
| rows | (string\|number)[][] | 是 | 数据行二维数组；单元格只能是字符串或有限数字。**数值列必须是 `number`（不要传 `"100"` 字符串），以免影响图表数值轴判断** |

**检查 CLI 退出码**：
- **Exit 0**：成功。解析 stdout JSON 获取项目主体（`project`）、初始 charts（此时 `screenshotSuccess` 为 `false`、无 `screenshotUrl`）、以及 **`snapshotJob.id`**（截图作业 ID）。
- **Exit 1**：认证失败。引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub)。
- **Exit 2**：业务错误（如 AI贝不足、项目数已满）。向用户展示错误详情。
- **Exit 3**：网络/超时错误。告知用户稍后重试。

> **默认不要主动获取截图**——直接进入第五步交付项目即可。仅当用户明确要求"我要截图 / 给我图片 / 把图发我"等时，才执行下方"可选：获取图表截图"。

响应字段说明详见下方"响应字段参考"。

### 第五步：返回结果（前置条件：第四步创建成功）

向用户提供：
- 项目 URL（从 `project.projectUrl` 获取）
- 项目 ID（从 `project.id` 获取）
- 摘要：图表数量、类型、标题
- 截图链接（如果 `charts[].screenshotSuccess` 为 true）
- 资源消耗：本次消耗 AI贝数、剩余 AI贝、已用项目数/上限

## 可选：获取图表截图（仅当用户主动要求时）

仅当用户在项目创建成功后明确要求时（含「截图 / 图片 / 配图 / 把图发我 / screenshots / images」等触发词，或追问「图呢 / 我看不到图」），才执行此节。

如果第四步响应里没有 `snapshotJob.id`，**不要进入此节**。

### 步骤

1. 从第四步响应取 `snapshotJob.id`
2. 立即查询一次（截图常常已经完成）：
   ```bash
   bash scripts/aitubiao-cli.sh query-snapshot-job <snapshotJob.id>
   ```
3. 解析返回 JSON 的 `status`：
   - **`success`**：用 `results[]` 替换第四步响应中的 `charts[]`，把 `results[].screenshotUrl` 提供给用户
   - **`failed`**：把 `errorMessage` 告知用户，项目本体仍可在 `projectUrl` 访问
   - **`processing`**：告知用户「截图还在生成，约 10 秒后再试」，**等用户再次明确要求时再查询**
4. 上限 5 分钟（约 30 次查询）。仍 `processing` 时告知用户「截图生成较慢，可稍后访问 `projectUrl` 查看，项目本体已经创建成功」

### 强约束

- **每次 `query-snapshot-job` 都是独立的 Bash 调用**，禁止在同一次 Bash 调用里 `sleep` 循环
- 作业仅短期保留；若返回 404（CLI exit 3），告知用户截图作业已过期，无需自动重试

### 返回 JSON 结构

```json
{
  "id": "...",
  "status": "processing | success | failed",
  "totalCharts": 9,
  "results": [
    {
      "index": 1,
      "type": "basic-bar",
      "title": "Revenue Trend",
      "description": "...",
      "screenshotSuccess": true,
      "screenshotUrl": "https://oss.xxx/ai-snapshot/..."
    }
  ],
  "errorMessage": "...",
  "completedAt": "2026-05-14T08:31:14.000Z"
}
```

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
| 1 | 认证失败（HTTP 401/403 或凭证无效） | 立即停止，引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) |
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
    "projectUrl": "https://app.aitubiao.com/workspace/cuid_string?utm_source=skill_skill-clawhub&channel=skill-clawhub"
  },
  "charts": [
    {
      "index": 1,
      "type": "basic-bar",
      "title": "Revenue Trend",
      "description": "Monthly revenue analysis.",
      "screenshotSuccess": false
    }
  ],
  "snapshotJob": {
    "id": "snapshot_job_id",
    "status": "processing",
    "totalCharts": 1
  },
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

**注意**：
- 同步返回时初始 `charts[].screenshotSuccess` 为 `false`、无 `screenshotUrl`；如需截图请走「可选：获取图表截图」节，用 `snapshotJob.id` 轮询。`quota` 可能为 `null`。
- `quota.shellCoinCost` 是**实际**扣费金额（已按真实生成的图表数结算），可能小于预扣的 `maxCharts × .feature.cost`。`quota.shellBalance` 已包含部分退款。

## Supported Chart Types (40 types)

基础: basic-bar, basic-column, basic-line, basic-pie, basic-radar, bar-progress, donut-progress
分组: grouped-bar, grouped-column
堆叠: stacked-bar, stacked-column, stacked-area, percent-bar, percent-column, percent-stacked-bar, percent-stacked-column
混合: mixed-line-grouped-column, mixed-line-stacked-column
特殊: funnel, cascaded-area, river-area, butterfly, dynamic-bar, dynamic-ranking, jade-jue
高级: sankey, chord, voronoi, descartes-heatmap, single-layer-treemap, word-cloud, rose-pie, symbol-bar, symbol-column, symbol-pie, difference-arrow-bar, difference-arrow-column, liquid, compose-waterfall, check-in-bubble

## 常见问题（FAQ）

### 💰 付费与免费

**Q1：这个技能收费吗？**

A：**技能本身完全免费**，任何人都可以安装使用。但生成图表时会调用爱图表的 AI 服务，该服务会按生成的图表个数消耗 **AI贝**（爱图表平台的虚拟点数）。

- 🎁 **首次使用**：新用户赠送 **30个图表** 免费额度（无需订阅）
- 💎 **后续使用**：生成多少张表扣多少 AI贝（如生成 5 张图 = 扣 5 AI贝）
- 🔔 **费用透明**：每次生成前会明确告知本次最高预扣金额，**点击确认后才会扣费**，实际生成少于预期时会自动退还多扣部分

---

**Q2：AI贝怎么获得？用完怎么办？**

A：AI贝通过订阅爱图表会员获得。

1. 登录 [爱图表官网](https://app.aitubiao.com)
2. 进入「会员中心」→「订阅套餐」
3. 选择适合你的套餐，支付后 AI贝自动到账

> 💡 建议先用免费体验效果，确认满足需求后再订阅。

---

### 🔑 使用前准备

**Q3：API Key 是什么？怎么获取？**

A：API Key 是你的"爱图表平台通行证"，用于验证你的身份和账户余额。

**获取步骤：**
1. 访问 [爱图表 API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) 
2. 注册/登录你的爱图表账号
3. 点击 **"创建新 Key"**，复制生成的 `sk_v1_...` 格式字符串
4. 回到对话中，把 Key 粘贴给我，系统会自动保存

> 🔒 **安全提示**：Key 只保存在你本地电脑的 `~/.aitubiao/credentials` 文件中，不会泄露给任何人。

---

**Q4：我需要在电脑上安装什么额外软件吗？**

A：需要确保你的电脑已安装以下工具（通常系统自带或开发环境已有）：

| 系统 | 需要安装 |
|------|----------|
| **macOS/Linux** | `curl`、`jq`（`jq` 可能需要手动安装：`brew install jq` 或 `apt install jq`） |
| **Windows** | Git Bash（推荐）、`curl`、`jq` |

如果不确定是否已安装，可以告诉 AI "帮我检查环境"，系统会自动检测并提示缺失项。

---

### 📊 数据准备与上传

**Q5：支持哪些数据格式？文件大小有限制吗？**

A：支持常见的数据格式：

| 数据来源 | 说明 |
|----------|------|
| **直接粘贴** | 在对话中直接粘贴表格数据，AI 会自动识别结构 |
| **Excel 文件（.xlsx / .xls）** | 上传 Excel 文件，AI 自动读取 |
| **CSV 文件** | 上传 `.csv` 文件，AI 自动读取 |
| **TXT 文件** | 上传包含结构化文本的 `.txt` 文件 |

> ⚠️ **文件大小限制**：单个文件不超过 **100K**。如果文件较大，建议拆分成多个小文件分批上传，或直接粘贴数据。
>
> 💡 推荐使用 **Excel 或 CSV**，数据结构更清晰，AI 识别更准确。

---

**Q6：AI 怎么处理我上传的数据？**

A：上传数据后，AI 会按以下流程处理：

1. **AI 解析数据**：将你上传的文件自动拆分解析成**一个或多个数据块**
2. **选择数据块**：你可以选择其中一个或多个数据块
3. **生成图表**：AI 根据选中的数据块自动生成对应的图表
4. **查看图表**：生成完成后，你会收到项目链接，点击即可查看

> 💡 如果对某张图表不满意，可以返回数据块列表，对同一个数据块**重新生成图表**，或对未生成过的数据块进行新的图表生成。

---

### ⚠️ 报错处理

**Q7：提示 401/403 错误怎么办？**

A：401 或 403 表示 **API Key 无效或已过期**。请按以下步骤处理：

1. 登录爱图表官网，进入 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) 
2. **删除旧 Key**，点击 **"创建新 Key"** 生成一个新的
3. 在对话中把新 Key 粘贴给我，我会帮你更新本地凭证

> ⚠️ 401/403 不是网络超时，**不要重试**，重试只会浪费时间，直接换新 Key 即可。

---

**Q8：提示"AI贝余额不足"怎么办？**

A：说明你的爱图表账户AI贝已用完，无法生成新的图表。

**解决方案：**
- 前往 [爱图表官网](https://app.aitubiao.com) 订阅会员或购买AI贝
- 充值和订阅完成后，重新发起生成即可

> 💡 你可以在生成前的费用确认界面看到当前余额，提前判断是否需要充值。

---

**Q9：提示"项目数已满"怎么办？**

A：爱图表免费版对"未删除的旧项目"有数量上限（通常为 10个左右），满了之后无法创建新项目。

**解决方案：**
1. 登录 [爱图表工作台](https://app.aitubiao.com/workspace)
2. 删除一些不再需要的旧项目
3. 回到对话中重新发起生成

---

**Q10：生成过程中卡住或报错"超时"怎么办？**

A：生成图表是后台任务，通常需要 1-3 分钟。

- ✅ **正常情况**：项目已创建成功，图表在后台生成，你可以点击返回的链接实时查看进度
- ❌ **报错超时（Exit 3）**：可能是网络波动，告知 AI "刚才超时了，帮我重新发起"即可

> ⚠️ **禁止重复提交**：如果已经收到"项目创建成功"的提示，说明任务已经在后台排队，不要再次提交，否则可能重复扣费。

---

### ✏️ 图表编辑、保存与下载

**Q11：生成后的图表在哪里查看？**

A：项目创建成功后，AI 会立即返回一个专属链接，格式类似：

> https://app.aitubiao.com/workspace/xxxxxxxxx

点击该链接即可在浏览器中实时查看生成进度和最终效果。

---

**Q12：生成的图表可以编辑吗？**

A：可以。爱图表提供了灵活的编辑方式：

- **快速调整**：将鼠标悬浮在图表上，底部会出现该图表的**文字解析**，方便你理解图表含义
- **切换皮肤**：点击图表下方的「切换皮肤」，系统提供多种专业级配色方案，每点一次都有"惊喜"
- **自定义编辑**：点击「自定义编辑」，系统会创建一个新项目，你可以在编辑器中体验更专业的图表配置，打造专属图表
- **批量操作**：勾选多个图表，可进行**批量保存、批量下载**或批量进入编辑器

---

**Q13：怎么下载图表文件？**

A：生成完成后，对 AI 说 **"帮我下载这个图表项目"**，AI 会通过爱图表 API 导出文件。

你也可以在爱图表工作台手动下载：
- 点击单个图表 → 选择「下载」
- 选择你想要的**格式**（png / jpg / pdf / ppt）和**尺寸**
- 点击「下载」即可

**各格式说明：**

| 格式 | 适用场景 | 是否需要付费 |
|------|----------|-------------|
| `png` / `jpg` / `pdf` | 预览、插入文档 | **免费导出** |
| `ppt`（PPTX 源文件） | 继续编辑 | 需付费会员权益 |

如果提示"当前会员不支持 PPT 导出"，可以选择 `pdf` 或 `png` 格式免费导出。

---

**Q14：可以保存图表到项目吗？**

A：可以。点击图表下方的「保存」，系统会**创建一个新的项目**，将当前图表保存到项目中。这样你可以把多次生成的图表汇总到同一个项目里统一管理。

---

## 📊 快速故障排查流程图

遇到问题时，可以按此流程自行判断：

遇到问题
│
├─ 401/403 错误 → 去爱图表官网重新创建 API Key → 粘贴新 Key
│
├─ "余额不足" → 去爱图表官网充值或订阅 → 重新发起
│
├─ "项目数已满" → 去爱图表工作台删除旧项目 → 重新发起
│
├─ 文件上传失败 → 检查文件是否超过 100K → 拆分或直接粘贴数据
│
├─ 生成超过 3 分钟没反应 → 点击返回的链接查看进度 → 正常排队中
│
└─ 其他报错 → 将报错信息完整复制给 AI → AI 会引导你处理