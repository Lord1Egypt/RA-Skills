---
name: byted-las-document-parse
description: "CRITICAL: EXCELLENT at parsing BOTH PDF documents and IMAGES (including LONG SCREENSHOTS, scanned documents, and standard images). Extract structured Markdown content (text, tables, images). MUST use this skill WHENEVER a user wants to parse, read, OCR, or extract content from ANY PDF file, image file, or long screenshot. Also trigger this automatically when users share a local file path, URL, or TOS path pointing to a PDF or image, even if they don't explicitly say 'parse'."
metadata:
  { "openclaw": { "requires": { "env": ["LAS_API_KEY", "TOS_ACCESS_KEY", "TOS_SECRET_KEY", "TOS_BUCKET"] }, "primaryEnv": "LAS_API_KEY" } }
---

# LAS-AI Document Parsing

**Powerful Parser for PDF & Images:** Extract structured text, tables, and data from **PDF documents** and **IMAGES (especially extremely long screenshots and scanned files)**, converting them seamlessly to structured Markdown format. Powered by Bytedance LAS-AI.

## 设计模式

本 skill 主要采用：
- **Pipeline**：多步骤工作流（确认模式 → 提交 → 轮询 → 结果）
- **Tool Wrapper**：封装 LAS API，提供按需知识
- **Inversion**：在关键决策点（解析模式）先收集用户偏好

## Gotchas

- 必须配置 `LAS_API_KEY` 环境变量，[获取方式](https://www.volcengine.com/docs/6492/2191994?lang=zh)
- 本地上传文件需要配置 `TOS_ACCESS_KEY` 和 `TOS_SECRET_KEY`，[获取方式](https://www.volcengine.com/docs/6291/65568?lang=zh)
- env.sh 自动加载（无需手动 source）：自动发现 skill 目录 / 当前目录的 env.sh，仅补充缺失变量；`--env-file` 显式指定则**强制覆盖**已有值
- 如果用户报告认证失败（401），优先建议加上 `--env-file` 参数以确保使用最新凭证
- 长图（宽高比 < 0.334）处理耗时更长，会自动分页
- API 并发限制为 1 QPM，过快调用可能触发限流
- **断点恢复**：如果会话中断，用户稍后回来提供 `task_id`，直接使用 `check-and-notify --task-id {task_id} --output /tmp/las_parse_{task_id} --poll` 即可恢复所有本地图片下载和 ZIP 打包流程。

## 工作流

复制此清单并跟踪进度：

```text
解析进度：
- [ ] 步骤 0：确认解析模式
- [ ] 步骤 1：确认虚拟环境就绪
- [ ] 步骤 2：提交任务
- [ ] 步骤 3：立即回复用户
- [ ] 步骤 4：后台异步轮询
```

### 第 0 步：确认解析模式（必须先执行）

在提交任务前，**必须先让用户确认解析模式**。向用户展示以下信息并询问：

```
请选择 PDF 解析模式：

| 模式 | 说明 | 价格 |
|------|------|------|
| normal | 默认模式，不进行深度思考，速度更快，适用于绝大多数文档 | 0.02 元/页 |
| detail | 深度分析模式，精度更高但处理时间更长 | 0.04 元/页 |

推荐：如果文档结构简单、以文字为主，选择 normal；如果文档包含复杂表格、图表或需要高精度识别，选择 detail。
```

**行为约束**：
- 如果用户明确指定了模式，直接使用用户指定的模式
- 如果用户未明确指定，默认使用 `normal` 模式
- 确认模式后，继续执行第 1 步

### 第 1 步：确认虚拟环境就绪（仅首次）

首次执行命令前，将环境初始化与 submit chain 在一起，一次工具调用完成：

```bash
cd {skill_directory} && (test -d .venv || (python3 -m venv .venv && .venv/bin/pip install -r requirements.txt)) && .venv/bin/python3 scripts/skill.py [--env-file /path/to/env.sh] submit --url "{文件路径或URL}" --parse-mode {normal|detail}
```

如果上述命令执行成功（未报错），说明虚拟环境已就绪。**后续命令无需再重复环境检查**，直接使用 `.venv/bin/python3` 即可。

### 第 2 步：提交任务

首次用上方 chain 命令完成环境检查 + submit。

- 输入类型自动识别（本地PDF / 本地图片 / HTTP URL / TOS路径）
- **stdout 输出一行 JSON**：`{"task_id": "xxx", "eta": "40秒~2分钟", "input_type": "local_image", "pages": 4}`
  - 若返回了 `tos_bucket` / `tos_prefix`，须在第 4 步透传给 check-and-notify
- 建议输出目录: `/tmp/las_parse_{task_id}/`

### 第 3 步：立即回复用户（submit 成功后必须先执行此步）

submit 命令返回后，**必须先回复用户再做任何其他操作**（包括启动轮询）。用户在等待反馈——如果跳过此步直接进入轮询，用户会长时间看不到任何响应。

解析 stdout JSON，**立刻**回复：
```
✅ PDF 解析任务已提交
📋 任务ID: {task_id}
⏳ 预计 {eta} 完成，完成后会自动通知您，您可以继续其他操作。
```

回复后，在**同一个响应**中继续第 4 步。

### 第 4 步：后台异步轮询

在回复用户的**同一个响应**中，根据当前运行环境，选择以下**第一个匹配**的方案执行：

> **环境检测方法**：
> - 支持后台子代理（可 spawn subagent） → **方案 A（后台子代理轮询）**
> - 不支持后台子代理 → **方案 B（降级：当前对话轮询）**

#### 方案 A：后台子代理轮询（首选）

使用后台子代理执行轮询。子代理在独立上下文中运行，不阻塞主对话，完成后结果自动返回主会话。

**调用后台子代理**，使用如下参数：

- **description**: `PDF解析结果轮询 ({task_id})`
- **prompt**:

```
你是一个后台轮询 Agent，任务是检查 PDF 解析任务状态并返回结果。

执行以下命令（一次调用即可，脚本内部会自动进行智能动态退避轮询，无需你手动循环）:
cd {skill_directory} && .venv/bin/python3 scripts/skill.py check-and-notify --task-id {task_id} --poll [--tos-bucket {tos_bucket}]

命令会阻塞直到任务完成/失败/超时，然后输出一行 JSON 到 stdout。

根据退出码向用户报告:
- exit 0 (成功): 读取 stdout JSON，按"结果回复模板"格式向用户报告
- exit 1 (失败): 读取 stdout JSON 中的 error_msg，报告错误
- exit 3 (超时): 报告任务耗时较长，提供 task_id 供手动查询

结果回复模板（exit 0 成功时）：

  ✅ PDF 解析完成
  📄 页数: {page_count} | 表格: {table_count} | 图片: {image_count}（已下载 {image_downloaded} 张）
  📝 内容预览: {preview}
  📂 本地路径: {output_dir}/
     ├── result.md（图片已替换为本地路径）
     ├── result.full.json（完整 API 响应）
     └── images/（{image_downloaded} 张图片）
  ☁️ 打包下载: {download_link_markdown}

  - 仅当 `has_download_url` 为 true 时显示下载行
  - 若 `has_download_url` 为 false，展示 `download_url_missing_reasons` 中的原因代替下载行
  - 直接原样输出 JSON 中 `download_link_markdown` 字段的值，不要自行拼接或截断
```

**行为约束**（主 Agent 侧）：
- 调用后台子代理后，**不要等待**子代理完成，继续响应用户
- 子代理完成后结果会自动回传，不要主动轮询子代理状态
- 如果后台子代理不可用或调用失败，**降级到方案 B**

#### 方案 B：当前对话轮询（后台子代理不可用时）

直接在当前对话中执行带 `--poll` 的命令，脚本内部会自动进行智能动态退避轮询：

```bash
cd {skill_directory} && .venv/bin/python3 scripts/skill.py check-and-notify --task-id {task_id} --poll [--tos-bucket {tos_bucket}]
```

命令会阻塞直到出结果（成功/失败/超时），**一次调用即可，不要手动循环**。

| Exit Code | 含义 | 处理 |
|-----------|------|------|
| 0 | 成功 | 读取 stdout JSON，按下方"结果回复模板"格式报告结果 |
| 1 | 失败 | 读取 stdout JSON 中的 `error_msg`，报告错误 |
| 3 | 超时 | 报告任务耗时较长，提供 task_id 供手动查询 |

## 结果回复模板（exit 0 成功时）

```
✅ PDF 解析完成
📄 页数: {page_count} | 表格: {table_count} | 图片: {image_count}（已下载 {image_downloaded} 张）
📝 内容预览: {preview}
📂 本地路径: {output_dir}/
   ├── result.md（图片已替换为本地路径）
   ├── result.full.json（完整 API 响应）
   └── images/（{image_downloaded} 张图片）
☁️ 打包下载: {download_link_markdown}
```

- 仅当 `has_download_url` 为 true 时显示下载行
- 若 `has_download_url` 为 false，展示 `download_url_missing_reasons` 中的原因代替下载行
- 直接原样输出 JSON 中 `download_link_markdown` 字段的值，不要自行拼接或截断

### 下载链接展示（重要）

返回 JSON 中包含 `download_link_markdown` 字段，值是已拼好的完整 Markdown 链接（如 `[点击下载ZIP（24小时有效）](https://...)`）。

**直接原样输出 `download_link_markdown` 的值**，不要自行拼接或改写。预签名 URL 包含签名参数（`?X-Tos-Algorithm=...&X-Tos-Signature=...`），任何截断都会导致 403 下载失败。

作为兜底，下载链接也写入了 `{output_dir}/download_url.txt`。如果输出时链接被截断，引导用户从该文件获取完整链接：
```
cat {output_dir}/download_url.txt
```

不要使用 `tos_internal_path` 字段——它是 `tos://` 内部路径，无法作为 HTTP 链接。

## 输出目录结构

```
/tmp/las_parse_{task_id}/
├── result.md              # Markdown 正文（图片 URL 已替换为本地相对路径）
├── result.full.json       # 完整 API 响应（含 detail / text_blocks / 位置信息）
├── images/                # 下载到本地的所有图片
├── images.json            # 图片清单（含原始 URL、本地路径、下载状态）
└── download_url.txt       # 完整下载链接（兜底，防止 LLM 输出截断）
```

配置了 `--tos-bucket` 时，结果会打包为 zip 上传到 TOS 并生成预签名下载 URL（默认 24 小时有效）。

## 更多参考
- [命令参数详解](references/commands.md)
- [使用示例 & 代码集成](references/usage-examples.md)
- [配置说明 & 依赖安装](references/configuration.md)
- [API 参数说明](references/api.md)
- [常见问题 FAQ](references/faq.md)
