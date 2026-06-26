---
name: 爱图表-AIPPT
description: 输入一个主题或一段文字，自动生成一份完整可编辑的PPT演示文稿。适合做汇报、讲课、方案展示。支持中文/英文，可以自由选择页数和风格。触发词：创建PPT、做PPT、生成演示文稿、制作幻灯片、create PPT、make slides、generate presentation。
license: MIT
compatibility: Requires network access to api.aitubiao.com, Bash shell, curl, and jq
metadata:
  author: aitubiao
  version: "1.2.3"
allowed-tools: Bash Read
---

# AI PPT/演示文稿生成

根据用户提供的主题、内容或文件，自动生成PPT演示文稿项目。

## 强制规则

**以下规则必须严格执行，不得跳过、变通或使用替代方案：**

1. **认证优先**：在执行任何操作之前，必须先检查凭证状态。认证未通过时，禁止执行任何后续步骤。
2. **按顺序执行**：工作流程的 5 个步骤必须按顺序执行，禁止跳步。
3. **费用确认前禁止调用生成接口**：必须成功查询配额、计算费用、并获得用户明确确认后，才能调用创建接口。
4. **仅通过 API 创建PPT**：禁止使用本地工具（reveal.js、impress.js、Google Slides API、python-pptx、LibreOffice 等）生成PPT。无论 API 因何种原因失败，都**绝对禁止使用本地工具**，没有任何例外。API 失败时正确做法是停止并告知用户，不是寻找替代方案。
5. **401/403 立即停止**：任何步骤中收到 HTTP 401/403（CLI exit 1），立即停止并引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) 检查或重新创建 API Key。401/403 不是超时，禁止重试。
6. **超时/500 不自动重试创建接口**：创建接口不可重试（可能重复扣费）。告知用户失败原因，由用户决定是否重新发起。

**⚠️ 以下想法是错误的，如果你发现自己在这样想，请立即停止：**
- ❌ "API 不可用，我可以用本地工具生成PPT作为替代" → 违反规则 4
- ❌ "至少让用户看到一些演示文稿效果" → 本技能唯一输出方式是 aitubiao API
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

## 支持的输入方式

| 输入方式 | 处理方法 |
|---------|---------|
| **主题文本** | 用户直接输入主题（如"人工智能发展趋势"），直接作为 `prompt` |
| **粘贴内容** | 用户粘贴完整文本，作为 `prompt` |
| **本地文件**（TXT/MD/CSV） | 用 Read 工具读取文件内容，作为 `prompt` |
| **Excel 文件**（.xlsx/.xls） | 使用 xlsx skill 或 Read 工具读取，禁止手动编写 Python 脚本解析 |

## 工作流程

**每一步必须在前一步完成后才能开始。禁止跳步。**

### 第一步：认证（前置条件：无）

运行检查凭证流程。认证未通过时按"认证"章节流程处理。

**认证未通过时，停止。不要读取用户数据，不要做任何分析。**

### 第二步：识别和确认内容（前置条件：第一步认证通过）

获取用户内容后，向用户确认以下信息：

- 内容/主题是否正确？
- 需要生成多少页？（默认 6 页，上限由会员等级决定，可通过配额接口获取 `pptGeneratePageLimit`）
- 主题风格偏好？（浅色 `light` / 深色 `dark`，默认浅色）
- 主题色偏好？（可选：蓝色`#004eff`、橙色`#f16f0b`、红色`#ee4646`、天蓝`#2197fc`、紫色`#8a61ec`、绿色`#35b13f`、动态配色`dynamic`）
- 有没有特殊要求？（如"简洁风格"、"多用图表"等，作为 `requirements`）

### 第三步：检查配额并确认费用（前置条件：第二步内容已确认）

在创建PPT前，**必须**检查用户的 AI贝余额和项目配额，并向用户确认费用后才能继续。

#### 3.1 查询配额

```bash
bash scripts/aitubiao-cli.sh quota --skill ppt
```

#### 3.2 计算总费用

**PPT 项目按"页"计费**：每生成一页扣 `.feature.cost` 个 AI贝。

总费用 = `.feature.cost` × `pageCount`

（`pageCount` 上限由顶层字段 `pptGeneratePageLimit` 决定，超过会被拒绝。）

| billingModel | 计算方式 | 示例 |
|-------------|---------|------|
| `per-page` | 总费用 = cost × pageCount | 生成6页PPT: 10 × 6 = 60 AI贝 |

#### 3.3 向用户确认费用

**必须在调用生成接口前向用户展示费用确认信息，并等待用户确认后才能继续**：

```
本次操作将消耗 {totalCost} 个 AI贝（PPT/图文生成，按页计费：{cost} AI贝/页 × {pageCount} 页）
当前余额: {shellBalance} 个 AI贝
操作后余额: {shellBalance - totalCost} 个 AI贝
项目数: 已用 {projectsUsed}/{projectsLimit}

是否继续？
```

- 如果 `shellBalance < totalCost`：告知用户当前 AI贝余额不足，需前往 aitubiao 网站购买会员或充值后再继续，**不要继续**
- 如果 `projectsRemaining <= 0`：告知用户当前项目数已满，需前往 aitubiao 网站升级会员，或在网站中删除旧项目后再继续，**不要继续**
- 如果 `pageCount > pptGeneratePageLimit`：告知用户请求的页数超过当前会员等级限制（最多 `pptGeneratePageLimit` 页），请减少页数或升级会员，**不要继续**

### 第四步：创建PPT项目（前置条件：第三步用户已确认费用）

**只有用户明确确认费用后才能执行此步骤。**

API 会在项目创建后立即返回项目地址（不等待所有页面生成完成）。用户可以通过项目地址实时查看生成进度。

```bash
bash scripts/aitubiao-cli.sh create-ppt <<'EOF'
{
  "prompt": "<用户的主题或内容>",
  "pageCount": 6,
  "theme": "light",
  "projectName": "<项目名称>"
}
EOF
```

**请求体字段说明**：

| 字段 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|-------|------|
| prompt | string | 是 | - | 用户输入的主题或内容文本 |
| pageCount | number | 否 | 6 | 页数（最小 1，上限由 `pptGeneratePageLimit` 决定） |
| theme | string | 否 | "light" | "light"（浅色）或 "dark"（深色） |
| color | string | 否 | - | 主题色：`#004eff`/`#f16f0b`/`#ee4646`/`#2197fc`/`#8a61ec`/`#35b13f`/`dynamic` |
| projectName | string | 否 | - | 项目名称 |
| requirements | string | 否 | - | 附加要求（风格偏好、内容侧重等） |
| title | string | 否 | - | 大纲标题 |

**检查 CLI 退出码**：
- **Exit 0**：成功。解析 stdout JSON 获取项目信息。
- **Exit 1**：认证失败。引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub)。
- **Exit 2**：业务错误。向用户展示错误详情。
- **Exit 3**：网络/超时错误。告知用户稍后重试。

响应字段说明详见下方"响应字段参考"。

### 第五步：返回结果（前置条件：第四步创建成功）

**立即向用户展示项目 URL**（从 `project.projectUrl` 获取）。PPT 页面仍在后台生成中，用户可以在浏览器中打开此链接实时查看生成进度和最终效果。格式示例：
```
您的 PPT 项目已创建成功！页面正在后台生成中（通常需要 5-10 分钟）。
请点击下方链接实时查看生成进度和编辑 PPT：
https://app.aitubiao.com/workspace/xxxxxxxxx?utm_source=skill_skill-clawhub&channel=skill-clawhub
```

同时提供以下补充信息：
- 项目 ID（从 `project.id` 获取）
- 总页数
- 资源消耗：本次消耗 AI贝数、剩余 AI贝、已用项目数/上限

## 下载已创建项目（可选后续操作）

如果用户在 PPT 项目创建后要求“帮我下载或者导出这个项目”，先提醒用户 PPT 页面仍可能在后台生成。**优先让用户通过 `projectUrl` 确认内容已生成完成，再执行下载。**

下载命令：

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
| 2 | 业务错误（code 90001=AI贝不足，40007=项目数已满，40015=创建失败，15009=同一项目已有 API Key 导出任务进行中） | 向用户展示详情；遇到 15009 时，提示用户等待上一个导出完成后再重试 |
| 3 | 网络/超时错误 | 告知用户稍后重试 |

## 响应字段参考

| 字段 | 类型 | 说明 |
|------|------|------|
| success | boolean | 项目是否创建成功 |
| outlineId | string | 大纲会话 ID |
| project.id | string | 项目 ID |
| project.title | string | 项目标题 |
| project.status | string | 通常为 `generating`（页面在后台异步生成） |
| project.projectUrl | string? | 项目 URL，用户打开可查看生成进度和编辑 PPT |
| quota | object? | 配额快照（**可能为 null**） |
| quota.shellCoinCost | number | 本次消耗 AI贝 |
| quota.shellBalance | number | 剩余 AI贝 |
| totalPages | number | 总页数 |
| completedPages | number | 已完成页数（API 返回时为 0，页面后台异步生成） |
| processingTime | string | API 响应时间（不含页面生成时间） |

**异步生成行为**：API 立即返回，页面在后台生成（5-10 分钟）。`projectUrl` 必须醒目展示给用户。

## 常见问题（FAQ）

### 💰付费与免费

**Q1：这个技能收费吗？**

A：**技能本身完全免费**，但生成 PPT时会调用爱图表的API服务，按生成页数消耗 **AI贝**。

- 🎁 **首次使用**：新用户赠送 **3页** 免费额度（无需订阅）
- 💎 **后续使用**：生成多少页扣多少 AI贝
- 🔔 **费用透明**：生成前会明确告知扣费金额，**点击确认后才会扣费**

---

**Q2：AI贝怎么获得？**

A：通过订阅爱图表会员获得。登录 [爱图表官网](https://app.aitubiao.com) → 会员中心 → 选择套餐订阅即可。建议先用免费 3页体验效果，再决定是否订阅。

---

### 🔑 使用前准备

**Q3：API Key 是什么？怎么获取？**

A：API Key 是你的爱图表平台通行证。

**获取步骤：**
1. 访问 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub)
2. 注册/登录后，点击 **"创建新 Key"**，复制生成的 `sk_v1_...` 字符串
3. 回到对话中，把 Key 粘贴给我即可

> 🔒 Key 只保存在你本地电脑，不会泄露。

---

### 📄 生成规则

**Q4：PPT 最多可以生成多少页？**

A：一次PPT最多可以生成60页。 生成前 AI 会查询你的配额并告知上限。

---

**Q5：生成一份 PPT 需要多久？**

A：通常 **3-5 分钟**。项目创建后会立即返回链接，页面在后台生成，点击链接可实时查看进度。

> ⚠️ 收到"创建成功"后不要重复提交，否则可能重复扣费。

---

### ⚠️ 报错处理

**Q6：提示 401/403 错误怎么办？**

A：表示 **API Key 无效或已过期**。去 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) **删除旧 Key** → **创建新 Key** → 把新 Key 粘贴给我即可。

> ⚠️ 401 不是网络超时，**不要重试**，直接换新 Key。

---

**Q7：提示"AI贝余额不足"怎么办？**

A：前往 [爱图表官网](https://app.aitubiao.com) 订阅会员或充值，完成后重新发起生成即可。

---

**Q8：提示"项目数已满"怎么办？**

A：免费版项目上限约 10 个。登录 [爱图表工作台](https://app.aitubiao.com/workspace) 删除旧项目后，重新发起生成。

---

### ✏️ 结果与后续操作

**Q9：生成后的 PPT 在哪里查看和编辑？**

A：项目创建成功后 AI 会返回专属链接，点击即可查看。在爱图表工作台中可：
- 在线编辑文字、图片和排版
- 切换配色方案
- 调整页面顺序或增删页面
- 单独重新生成某一页

---

**Q10：怎么下载 PPT 文件？**

A：对 AI 说 **"帮我下载这个 PPT"**，或在工作台点击「下载」。

| 格式 | 适用场景 | 是否付费 |
|------|----------|----------|
| `png` / `pdf` | 预览、分享 | **免费** |
| `ppt`（PPTX） | 继续编辑 | 需付费会员 |

---

## 📊 快速排查流程图
401/403 → 重新创建 API Key → 粘贴新 Key
余额不足 → 充值或订阅 → 重新发起
项目数已满 → 删除旧项目 → 重新发起
生成超5分钟 → 点击链接查看进度（正常排队中）
其他报错 → 复制报错信息给 AI