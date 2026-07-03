---
name: 爱图表-AI图表3D插图
description:  AI图表3D插图生成。上传数据，一键将柱状图、折线图、饼图等转换为3D风格插画，支持13种材质风格（水晶、黄金、玻璃等）。触发词：3D图表、3D插图、图表转3D、立体图表、3D柱状图、3D折线图、3D饼图、3D illustration、3d chart、stylize chart。
license: MIT
compatibility: Requires network access to api.aitubiao.com, Bash shell, curl, and jq
metadata:
  author: aitubiao
  version: "1.2.3"
allowed-tools: Bash Read
---

# AI 图表3D插图生成

根据用户提供的数据和指定的图表类型，生成3D风格化数据可视化插画。

## 强制规则

**以下规则必须严格执行，不得跳过、变通或使用替代方案：**

1. **认证优先**：在执行任何操作之前，必须先检查凭证状态。认证未通过时，禁止执行任何后续步骤。
2. **按顺序执行**：工作流程的 5 个步骤必须按顺序执行，禁止跳步。
3. **费用确认前禁止调用生成接口**：必须成功查询配额、计算费用、并获得用户明确确认后，才能调用创建接口。
4. **仅通过 API 生成3D插图**：禁止使用本地工具（Blender、Three.js、matplotlib 等）生成3D可视化。无论 API 因何种原因失败，都**绝对禁止使用本地工具**，没有任何例外。API 失败时正确做法是停止并告知用户，不是寻找替代方案。
5. **401/403 立即停止**：任何步骤中收到 HTTP 401/403（CLI exit 1），立即停止并引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) 检查或重新创建 API Key。401/403 不是超时，禁止重试。
6. **超时/500 不自动重试创建接口**：创建接口不可重试（可能重复扣费）。告知用户失败原因，由用户决定是否重新发起。

**⚠️ 以下想法是错误的，如果你发现自己在这样想，请立即停止：**
- ❌ "API 不可用，我可以用本地工具生成3D可视化作为替代" → 违反规则 4
- ❌ "至少让用户看到一些3D效果" → 本技能唯一输出方式是 aitubiao API
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

## 支持的图表类型

仅以下 11 种图表类型支持转换为3D插图：

| chartType | 中文名称 | 数据结构 | 数据行数 | 数据要求 | 推荐场景 |
|-----------|---------|---------|---------|---------|---------|
| `basic-line` | 基础折线图 | 1列时间 + 1-8列数值 | 2-120行 | 数值或比率 | 时间序列/趋势数据 |
| `cascaded-area` | 层叠面积图 | 1列时间 + 1-8列数值 | 2-120行 | 数值或比率 | 多系列趋势对比 |
| `stacked-area` | 堆叠面积图 | 1列时间 + 1-12列数值 | 2-120行 | 数值或比率 | 累计趋势可视化 |
| `basic-pie` | 饼图 | 1列分类 + 1列数值 | 2-12行 | 比率(总和≈100%) | 占比/分布数据 |
| `basic-column` | 基础柱状图 | 1列分类 + 1列数值 | 2-120行 | 数值或比率 | 分类对比 |
| `check-in-bubble` | 打卡气泡图 | 1列维度 + 2-48列数值 | 2-48行 | 数值或比率 | 频次/热度数据 |
| `funnel` | 漏斗图 | 1列阶段名 + 1列数值 | 2-12行 | 数值或比率 | 转化率/流程数据 |
| `donut-progress` | 圆环进度图 | 1列名称 + 1列数值 | 仅1行 | 比率(0-100) | 占比/完成度 |
| `bar-progress` | 条形进度图 | 1列名称 + 1列数值 | 仅1行 | 比率(0-100) | 单指标进度 |
| `word-cloud` | 词云图 | 1列关键词 + 1列数值 | 12-120行 | 纯数值 | 关键词频率 |
| `liquid` | 水波图 | 1列名称 + 1列数值 | 1-48行 | 比率(0-100) | 单指标比率 |

### 数据格式注意事项

- **比率值使用百分制**：如完成度75%必须传 `75`，禁止传 `0.75`
- **饼图特殊要求**：所有数值之和必须在99.5%-100%之间
- **时间序列图表**（basic-line、cascaded-area、stacked-area）：第一列必须是时间
- **圆环进度图和条形进度图**：仅支持1行数据

## 工作流程

**每一步必须在前一步完成后才能开始。禁止跳步。**

### 第一步：认证（前置条件：无）

运行检查凭证流程。认证未通过时按"认证"章节流程处理。

**认证未通过时，停止。不要读取用户数据，不要做任何分析。**

### 第二步：识别数据并选择图表类型（前置条件：第一步认证通过）

#### 2.1 获取数据

判断用户如何提供数据：

- **直接粘贴文本**：解析为二维数组格式 `(string|number)[][]`，第一行为表头。
- **本地文件**（CSV/TXT）：用 Read 工具读取，然后解析为二维数组。
- **Excel 文件**（.xlsx/.xls）：使用 xlsx skill 或 Read 工具读取，禁止手动编写 Python 脚本解析 XML。

**数据格式要求**：
API 接受 `data` 字段为 JSON 二维数组，第一行为表头，后续为数据行。数值类型的单元格应为 `number`，文本类型应为 `string`。

示例：
```json
[
  ["月份", "销售额", "利润"],
  ["1月", 1000, 200],
  ["2月", 1500, 350],
  ["3月", 2000, 500]
]
```

#### 2.2 确认图表类型

向用户展示解析后的数据（表格形式），并确认：
- 数据是否正确？
- 选择哪种图表类型？（展示上方支持的11种类型供选择）

如果用户不确定图表类型，根据数据特点推荐：
- **时间序列数据** → `basic-line`（折线图）或 `cascaded-area`（面积图）
- **分类占比数据** → `basic-pie`（饼图）或 `donut-progress`（圆环图）
- **分类对比数据** → `basic-column`（柱状图）
- **层级/流程数据** → `funnel`（漏斗图）
- **单个进度指标** → `bar-progress`（条形进度）或 `liquid`（水波图）

#### 2.3 选择3D风格（可选）

询问用户是否有特殊的3D风格要求。内置风格名称（直接传名称，系统自动解析为详细提示词，不区分大小写）：

`water` | `dollar` | `gold` | `chip` | `fuzzy` | `plants` | `steel` | `glass` | `watermelon` | `bread` | `crystal` | `container` | `wood`

用户也可以输入自定义风格描述（如"赛博朋克"、"黏土风"），系统直接使用。

| style 值 | 效果描述 |
|----------|---------|
| `water` | 纯净水/液体质感 |
| `dollar` | 美元钞票材质 |
| `gold` | 真实黄金材质 |
| `chip` | 电脑芯片/电路板风格 |
| `fuzzy` | 毛茸茸/长毛毯质感 |
| `plants` | 灌木丛/绿植风格 |
| `steel` | 不锈钢金属质感 |
| `glass` | 多彩玻璃质感 |
| `watermelon` | 西瓜切片材质 |
| `bread` | 面包切片材质 |
| `crystal` | 水晶质感 |
| `container` | 集装箱风格 |
| `wood` | 橡木木纹质感 |

### 第三步：检查配额并确认费用（前置条件：第二步数据和图表类型已确认）

在生成3D插图前，**必须**检查用户的 AI贝余额，并向用户确认费用后才能继续。

#### 3.1 查询配额

```bash
bash scripts/aitubiao-cli.sh quota --skill 3d
```

#### 3.2 计算总费用

**3D 插图按"次"计费**：每次调用固定扣 `.feature.cost` 个 AI贝，**与生成的图片张数无关**。

总费用 = `.feature.cost`

#### 3.3 向用户确认费用

**必须在调用生成接口前向用户展示费用确认信息，并等待用户确认后才能继续**：

```
本次操作将消耗 {cost} 个 AI贝（图表3D插图，按次计费）
当前余额: {shellBalance} 个 AI贝
操作后余额: {shellBalance - cost} 个 AI贝

是否继续？
```

- 如果 `shellBalance < cost`：告知用户当前 AI贝余额不足，需前往 aitubiao 网站购买会员或充值后再继续，**不要继续**

### 第四步：生成3D插图（前置条件：第三步用户已确认费用）

**只有用户明确确认费用后才能执行此步骤。**

**注意**：图表渲染 + 3D转换可能需要 60-120 秒。

```bash
bash scripts/aitubiao-cli.sh create-3d <<'EOF'
{
  "data": [["月份","销售额"],["1月",1000],["2月",1500],["3月",2000]],
  "chartType": "<图表类型>",
  "style": "<可选：3D风格描述>",
  "chartTitle": "<可选：图表标题>"
}
EOF
```

**请求体字段说明**：

| 字段 | 类型 | 必填 | 最大长度 | 说明 |
|------|------|------|---------|------|
| data | (string\|number)[][] | 是 | - | 二维数组，第一行表头，数值用 number，文本用 string |
| chartType | string | 是 | - | 图表类型（见上方 11 种支持类型） |
| style | string | 否 | 500 | 内置风格名或自定义描述 |
| chartTitle | string | 否 | 100 | 图表标题 |

**检查 CLI 退出码**：
- **Exit 0**：成功。**但必须检查 stdout JSON 中的 `success` 字段**（见下方 4.1）。
- **Exit 1**：认证失败。引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub)。
- **Exit 2**：业务错误。向用户展示错误详情。
- **Exit 3**：网络/超时错误。告知用户稍后重试。

#### 4.1 图表类型不兼容处理

**即使 CLI exit 0，也必须检查返回 JSON 中的 `success` 字段。** 当 `success === false` 且 `errorCode === "chart_type_incompatible"` 时：
1. 向用户展示 `error` 中的不兼容原因
2. 展示 `compatibleChartTypes` 中可用的图表类型供选择
3. 用户选择新类型后，重新执行第四步

不兼容响应示例：
```json
{
  "success": false,
  "chartType": "basic-line",
  "errorCode": "chart_type_incompatible",
  "error": "Chart type \"basic-line\" requires the first column to contain time values...",
  "compatibleChartTypes": ["basic-column", "basic-pie", "funnel"]
}
```

### 第五步：返回结果（前置条件：第四步生成成功）

向用户提供：
- 3D插图图片 URL（从 `imageUrl` 获取）
- 摘要：图表类型、处理时间
- 如有图片展示能力，直接展示3D插图图片

## 错误处理

| CLI Exit Code | 含义 | 处理方式 |
|--------------|------|---------|
| 0 + success=false | 图表类型不兼容 | 见第四步 4.1 处理流程 |
| 1 | 认证失败（HTTP 401/403 或凭证无效） | 立即停止，引导用户前往 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) |
| 2 | 业务错误（code 90001=AI贝不足，14301=存储容量不足） | 向用户展示详情 |
| 3 | 网络/超时错误 | 告知用户稍后重试 |

## 常见问题（FAQ）

### 💰 费用相关

**Q1：生成3D插图怎么收费？**

A：**按次计费**，每次调用固定消耗10 AI贝，**与生成的图片数量无关**。生成前会明确告知本次消耗金额，点击确认后才会扣费。



**Q2：首次使用有免费额度吗？**

A：有的。新用户赠送的免费 30 AI贝 可用于3D插图生成，用完后再按次计费。


### 📊 数据与图表类型

**Q3：支持哪些图表类型转3D？**

A：支持 11 种图表类型：

| 图表类型 | 适用场景 |
|----------|----------|
| 基础折线图 | 趋势变化 |
| 基础柱状图 | 分类对比 |
| 饼图 | 占比分布 |
| 层叠面积图 | 多系列趋势 |
| 堆叠面积图 | 累计趋势 |
| 漏斗图 | 转化流程 |
| 圆环进度图 | 完成度（1行数据） |
| 条形进度图 | 进度展示（1行数据） |
| 水波图 | 单指标比率 |
| 打卡气泡图 | 频次热度 |
| 词云图 | 关键词频率 |

如果数据不兼容所选图表类型，AI 会提示并推荐可用的图表类型供你更换。


**Q4：3D风格有哪些选择？**

A：支持 13 种内置风格：

| 风格 | 效果 | 风格 | 效果 |
|------|------|------|------|
| `water` | 液体质感 | `gold` | 黄金材质 |
| `steel` | 不锈钢质感 | `glass` | 玻璃质感 |
| `crystal` | 水晶质感 | `wood` | 木纹质感 |
| `plants` | 绿植风格 | `bread` | 面包材质 |
| `watermelon` | 西瓜材质 | `container` | 集装箱风格 |
| `chip` | 芯片风格 | `fuzzy` | 毛茸茸质感 |
| `dollar` | 钞票材质 |

也可以输入自定义风格描述，如"赛博朋克"、"黏土风"、"霓虹灯"等，系统会自动识别并应用。



**Q5：数据格式有什么特殊要求？**

A：是的，需要注意以下两点：

- **比率值用百分制**：如完成度75%必须传 `75`，不能传 `0.75`
- **饼图数值之和须在 99.5%-100% 之间**

如果数据格式不对，AI 会提示具体问题，你按提示调整后重新提交即可。



### ⚠️ 报错处理

**Q6：提示 401/403 错误怎么办？**

A：表示 **API Key 无效或已过期**。去 [API Key 管理页面](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) **删除旧 Key** → **创建新 Key** → 把新 Key 粘贴给我即可。

> ⚠️ 401 不是网络超时，**不要重试**，直接换新 Key。



**Q7：提示"AI贝 余额不足"怎么办？**

A：前往 [爱图表官网](https://app.aitubiao.com) 订阅会员或充值，完成后重新发起生成即可。


**Q8：生成需要多久？**

A：3D插图生成需要 **60-120 秒**，比其他图表生成时间更长，这是3D渲染的正常耗时。提交后请耐心等待，不要重复提交。


**Q9：生成失败或超时怎么办？**

A：如果收到超时或失败提示，告知 AI "刚才生成失败了，帮我重新发起"即可。如果反复失败，可能是数据格式或图表类型不兼容，AI 会给出具体建议。


### ✏️ 结果与后续操作

**Q10：生成的图片可以商用吗？**

A：图片的商用权取决于你的爱图表会员等级，请查阅爱图表官网的会员权益说明。如有特殊需求，可联系爱图表客服咨询。


## 📊 快速故障排查流程图
401/403 → 重新创建 API Key → 粘贴新 Key
余额不足 → 充值或订阅 → 重新发起
数据不兼容 → 查看 AI 推荐的图表类型 → 更换类型重新生成
生成超 120 秒 → 告知 AI "超时了，帮我重新发起"
其他报错 → 复制报错信息给 AI
