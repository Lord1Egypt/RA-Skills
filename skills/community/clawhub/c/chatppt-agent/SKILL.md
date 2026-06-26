---
name: chatppt-cli
description: 使用 ChatPPT CLI 命令行工具通过 AI 自动生成 PPT 演示文稿。适用场景：用户需要根据主题文字或现有文件（Word/PDF/Markdown）生成 PPT 时触发本 skill。支持登录认证、PPT 生成、文件导入生成、结果查询等完整流程。
---

# ChatPPT CLI Skill

## 环境准备

### CLI 安装
运行npm命令进行安装，安装前先检查是否已存在chatppt命令。

```bash
npm install -g @yooai/cli
```

安装后可运行chatppt命令进行调用，比如：
```bash
chatppt --help
```

### 全局 Flag

| Flag | 说明 |
|------|------|
| `--config string` | 配置文件路径（默认 `$HOME/.chatppt/config.yaml`） |
| `-d, --debug` | 启用调试模式 |
| `-f, --format string` | 输出格式：`json`（默认）/ `table` / `pretty` |
| `-h, --help` | 帮助 |
| `-v, --version` | 版本 |

---

## 标准工作流

```
1. 检查登录状态（auth status
2. 未登录 → 执行登录（auth login）
3. 生成 PPT（ppt generate 或 ppt import_file）
4. 自动轮询等待结果（直到 `2` 或 `3`）
5. 询问用户要直接下载pptx文件还是跳转到线上编辑器
```

### Agent 执行强约束（必须遵守）

1. **严格流程顺序**：始终按“检查登录 -> 登录（如需要） -> 生成 PPT -> 轮询结果”执行，不得跳步。
2. **路径二选一**：在生成前必须询问用户选择：
   - 普通生成路径
   - 绘图生成路径
3. **自动提取参数**：先从用户输入中自动提取可识别参数值；仅对缺失且必要的信息追问用户。
4. **用户不想配置参数**：若用户明确表示不关心参数或不想填写，全部使用默认值发起请求。
5. **轮询展示图片**：轮询期间如果返回 `images.urls`，可直接把图片链接展示给用户。
6. **成功即停止**：当任务状态为 `2`或`3` 后，仅返回成功结果与关键信息，不执行任何后续操作（后续接口未就绪）。
7. **Web Search 收费确认**：`--web-search` 涉及额外收费，启用前必须先告知用户并获得明确确认；未确认则按关闭处理（传 `--web-search=false`）。
8. **如果已经进入到了自动轮询流程中，要一直等待轮询成功或失败，不能在轮询过程中又进行生成。如果是Agent手动轮询，也需要轮询到成功或失败，不能中途停止对话等待用户继续输入。**
9. **如果轮询接口返回了失败，不要再次生成，要询问用户是否要再次生成。**
10. **如果用户权益用完了，提示用户去clawppt官网 <https://chat-ppt.com/openclaw> 进行充值点数。**

### 参数提取与追问规则（Agent）

1. **先提取后追问**：先从用户自然语言中提取参数（主题、路径选择、样式参数等），再补问缺失信息。
2. **最小追问原则**：仅追问生成任务必需信息（如 `主题` 或导入时的 `文件路径`）。
3. **路径参数边界**：
   - 普通生成路径只处理：`font-name`、`theme-color`、`ai-picture`、`image-style`、`template-id`、`custom-template-id`、`custom-page-count`
   - 绘图生成路径只处理：`banana-style-id`、`banana-doc-type`、`banana-reference-image`
4. **默认值策略**：若用户明确“不想设置参数/你看着办/默认就行”，则所有未指定参数使用默认值，不再反复追问。
5. **收费项单独确认**：`web-search` 为额外收费项，不能并入“默认就行”；必须单独征得用户同意后才启用。

### 确认普通生成与绘图生成路径后的参数提取与追问规则（Agent）
1. **模板风格确认**：在普通生成和绘图生成中，都需要询问用户是否需要预览模板风格并指定模板生成。
   - 普通生成路径参数：`template-id`
   - 绘图生成路径参数：`banana-style-id`
2. **普通生成路径中的图片风格确认**：在普通生成中询问用户是否需要指定AI图片风格，如果指定了，则参数--ai-picture必须等于true。参考--image-style参数获取方式。
3. **绘图生成排版风格确认**：在绘图模式中还需要确认用户是否需要指定排版样式，如果需要，参考--banana-doc-type参数获取方式。

---

## 命令速查

| 目标 | 命令 |
|------|------|
| 查看登录状态 | `auth status` |
| 登录 | `auth login` |
| 登出 | `auth logout` |
| 刷新令牌 | `auth refresh` |
| 生成 PPT（主题文字） | `ppt generate "主题"` |
| 生成绘图PPT（主题文字） | `ppt generate_banana "主题"` |
| 生成 PPT（文件导入） | `ppt import_file "/path/to/file"` |
| 生成绘图PPT（文件导入） | `ppt import_file_banana "/path/to/file"` |
| 查询 PPT 结果 | `ppt result <ppt_id>` |
| 查看配置 | `config show` |
| 重载配置 | `config reload` |
| 查看版本 | `version` |

---

## chatppt auth — 认证管理

所有 PPT 生成命令都需要先登录。

```bash
# 查看当前登录状态
chatppt auth status

# 登录（默认自动打开浏览器）
chatppt auth login

# 登录但不自动打开浏览器
chatppt auth login --no-browser

# 刷新令牌（令牌即将过期时使用）
chatppt auth refresh

# 登出
chatppt auth logout
```

**典型返回（status）**
```json
{
  "success": true,
  "code": 200,
  "data": {
    "is_logged_in": true,
    "user": { "id": "string", "nickname": "string", "mobile": "string" }
  }
}
```

---

## chatppt ppt generate — 根据主题生成 PPT

**普通生成**
```bash
chatppt ppt generate "主题描述" [options]
```

**绘图生成**
```bash
chatppt ppt generate_banana "主题描述" [options]
```

### 必填

| 参数 | 说明 |
|------|------|
| `主题描述` | PPT 主题，1–200 字符 |

### 可选参数（公共）

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--complex` | int | 0 | 内容复杂度 1=简单，2=中等，3=复杂 |
| `--language` | string | — | 语言：`zh-CN` / `en-US` / `zh-TW` |
| `--web-search` | bool | false | 联网补充内容（额外收费，启用前需用户明确确认） |
| `--poll` | bool | true | 是否自动轮询等待结果 |
| `--interval` | int | 5 | 轮询间隔（秒） |
| `--max-retries` | int | 60 | 最大轮询次数（约 5 分钟） |

### 普通生成路径参数（与 Banana 路径平级）

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `--font-name` | string | — | 字体名，如 `微软雅黑` |
| `--theme-color` | string | — | 主题色：`蓝色` `红色` `绿色` `橙色` `紫色` `黄色` `粉色` |
| `--ai-picture` | bool | true | 是否启用 AI 配图 |
| `--image-style` | string | — | 配图风格描述，如 `商务风` |
| `--template-id` | string | — | 预制矢量模板 ID |
| `--custom-template-id` | string | — | 自定义模板 ID |
| `--custom-page-count` | int | 0 | 页数，0 = 自动 |

> 约束说明：
> - 在生成之前询问用户是否需要浏览并指定模板，需要的话调用chatppt ppt template获取--template-id参数数据，调用之后的数据，一定要将每一项的至少一张图片展示给用户挑选。

#### --image-style 参数获取方式

```bash
chatppt ppt picture_style
```

#### --template-id 参数获取方式
获取PPT模板风格列表，支持分页查询

支持查看模板的详细信息，包括：
  - 模板ID、标题、风格描述
  - 预览图片（封面、章节页、内容页、目录页）
  - 配色方案

示例:
  chatppt ppt template                    # 获取第1页，每页10个
  chatppt ppt template --page 2           # 获取第2页
  chatppt ppt template --limit 20         # 每页显示20个
  chatppt ppt template --page 2 --limit 5 # 获取第2页，每页5个

```bash
chatppt ppt template
```

### 绘图生成路径参数（与普通路径平级）

| 参数 | 类型 | 说明 |
|------|------|------|
| `--banana-style-id` | string | 绘图风格ID |
| `--banana-doc-type` | string | 绘图排版样式 |
| `--banana-reference-image` | string | 参考图片 URL 或路径 |

> 约束说明：
> - 绘图生成路径参数允许全部为空。
> - 普通路径与绘图生成路径是两条平级路线，不存在“更高级”关系。
> - Agent 必须先确认用户走哪条路径，再组装对应参数。
> - 生成任务默认开启轮询（`--poll=true`），接口内自动调用轮询接口持续查询直到 `SUCCESS` 或 `FAILED`。
> - 在生成之前询问用户是否需要浏览并指定风格，需要的话调用chatppt ppt banana-template获取--banana-style-id参数数据。

#### --banana-style-id 页面绘图风格参数获取方式

获取绘图生成PPT模板风格列表，支持分页查询

支持查看模板的详细信息，包括：
  - 模板ID、标题、风格描述
  - 预览图片（封面、章节页、内容页、目录页）
  - 配色方案

示例:
  chatppt ppt banana-template                    # 获取第1页，每页10个
  chatppt ppt banana-template --page 2           # 获取第2页
  chatppt ppt banana-template --limit 20         # 每页显示20个
  chatppt ppt banana-template --page 2 --limit 5 # 获取第2页，每页5个

```bash
chatppt ppt banana-template
```

#### --banana-doc-type 页面排版样式参数获取方式

```bash
chatppt ppt template_banana_style
```

### 示例

```bash
# 基础生成
chatppt ppt generate "人工智能发展趋势" --language zh

# 普通生成路径（带样式）
chatppt ppt generate "2024年度工作总结" \
  --language zh \
  --font-name "微软雅黑" \
  --theme-color blue \
  --custom-page-count 15 \
  --image-style "商务风"

# 绘图生成风格路径（参数可部分或全部为空）
chatppt ppt generate_banana "产品介绍" \
  --banana-style-id style_001 \
  --banana-doc-type business

# 异步模式（不等待结果，手动查询）
chatppt ppt generate "主题" --poll=false
```

### 成功返回

```json
{
  "success": true,
  "code": 200,
  "data": {
    "ppt_id": "ppt_1234567890",
    "request_id": "string",
    "title": "string",
    "task_status": "2",
    "images": {
      "urls": [{ "url": "https://example.com/ppt/slide1.jpg" }]
    }
  }
}
```

**task_status 说明**

| 值 | 含义 |
|----|------|
| `1` | 生成中 |
| `2` | 已完成 |
| `3` | 失败 |

---

## chatppt import file — 文件导入生成 PPT

上传本地文件后基于其内容生成 PPT，适合将现有 Word / PDF / Markdown 转为演示文稿。

**导入生成普通PPT**
```bash
chatppt ppt import_file --file-path "/绝对路径/文档.docx"
```

**导入生成绘图PPT**
```bash
chatppt ppt import_file_banana --file-path "/绝对路径/文档.docx"
```

### 必填

| 参数 | 说明 |
|------|------|
| `--file-path` | 本地文件绝对路径 |

### 支持格式

| 格式 | 扩展名 | 大小上限 |
|------|--------|---------|
| Word | `.doc` `.docx` | 100 MB |
| PDF | `.pdf` | 100 MB |
| Markdown | `.md` | 100 MB |
| 纯文本 | `.txt` | 100 MB |

> 文本文件须为 UTF-8 编码。

其余可选参数与 `ppt generate` 完全相同，包括普通路径参数与 Banana 路径参数。

### 示例

```bash
# Word 文档导入
chatppt ppt import_file \
  --file-path "/Users/me/docs/product.docx" \
  --theme-color 蓝色

# PDF 导入，绘图生成风格
chatppt ppt import_file_banana \
  --file "/Users/me/docs/annual.pdf" \
  --banana-style-id style_002 \
  --banana-doc-type business 
```

返回格式与 `ppt generate` 相同。

---

## chatppt ppt result — 查询 PPT 生成结果

在异步模式（`--poll=false`）下使用，主动查询任务状态。

```bash
chatppt ppt result <ppt_id> [-f pretty]
```

| 参数 | 说明 |
|------|------|
| `ppt_id` | `ppt generate` / `ppt import_file` 返回的 `ppt_id` |
| `-f` | 输出格式（继承全局 flag） |

---

## config — 配置管理

```bash
# 查看当前配置
chatppt config show

# 重新加载配置文件
chatppt config reload
```

**典型返回（show）**
```json
{
  "success": true,
  "code": 200,
  "data": {
    "app": { "name": "ChatPPT CLI", "version": "1.0.0" },
    "api": { "url": "http://localhost:9157", "timeout": 30000 },
    "auth": { "type": "Bearer", "access_key_id": "csVyGKphwM..." },
    "ppt": { "default_ai_picture": true }
  }
}
```

---

## 生成下载链接 chatppt downloadppt

```bash
chatppt ppt downloadppt [ppt-id]
```

---

## 生成线上编辑器链接 chatppt editor

```bash
chatppt ppt editor [ppt-id]
```

---

## 错误处理

### 常见错误码

| 错误码 | 原因 | 处理 |
|--------|------|------|
| 400 | 参数错误（topic 超长、路径无效等） | 修正参数后重试 |
| 401 | 未登录或令牌失效 | 执行 `auth login` |
| 403 | 文件上传权限不足 | 检查 BCE AK/SK 配置 |
| 413 | 文件超过 100 MB | 压缩或拆分文件 |
| 429 | 请求频率过高 | 等待 5 秒后重试，最多 3 次 |
| 500 | 服务端错误 | 等待 10 秒后重试，最多 3 次 |

### 通用错误格式

```json
{
  "success": false,
  "code": 400,
  "message": "错误描述",
  "error_type": "VALIDATION_ERROR",
  "error_details": { "field": "topic", "reason": "主题长度必须在 1-200 字符之间" },
  "suggestion": "请检查输入参数并重试"
}
```

---

## 注意事项

- **并发限制**：同一用户同时只能有一个 PPT 生成任务，需串行执行。
- **文件上传**：依赖百度 BOS 服务，需正确配置 BCE 参数（AK/SK、Bucket 权限）。
- **令牌自动刷新**：运行时令牌过期会自动刷新；刷新失败则需重新 `auth login`。
- **敏感信息**：勿在日志中记录 AK/SK 或密码；定期清理云端不再使用的 PPT 文件。
- **Agent 提问策略**：优先自动提取用户输入中的参数；仅在缺失关键信息时追问；若用户不想配置参数，按默认值执行。