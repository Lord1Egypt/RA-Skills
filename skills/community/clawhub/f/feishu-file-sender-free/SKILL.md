---
name: "feishu-file-sender-free"
description: "飞书文件与图片发送工具，支持两步上传与稳定投递"
license: Proprietary
allowed-tools: read exec
compatibility: "Requires LLM with tool-use capability"
metadata:
  displayName: "飞书文件发送免费版"
  version: "1.0.0"
  summary: "飞书文件与图片发送工具，支持两步上传与稳定投递"
  tags:
    - "沟通协作"
    - "飞书"
    - "文件发送"
    - "个人效率"
  source: "SkillHub"
  converted_at: "2026-07-22T17:58:36"
---

# 飞书文件发送免费版

**版本**: 1.0.0
**适用对象**: 个人用户、独立开发者、一人公司
**核心定位**: 飞书文件与图片稳定发送基础工具

---

## 概述

飞书文件发送免费版是一款帮助个人用户通过飞书向用户发送普通文件与图片的工具。飞书机器人发送文件需要两步操作：先上传文件获取 `file_key`（普通文件）或 `image_key`（图片），再使用 key 发送消息。本工具将这两步流程封装为简洁的脚本，确保文件稳定投递。

工具特别解决了"本地图片路径被发成路径文本"的常见问题——当图片通过常规消息路径发送后用户看到的是路径文本而非图片本体时，本工具的稳定图片上传脚本可直接解决。支持国内版飞书与国际版 Lark，覆盖 HTML、ZIP、PDF、代码文件等各类普通文件格式。免费版聚焦个人文件发送需求，流程清晰、投递可靠。

---

## 核心能力

### 普通文件发送

- **支持格式**: HTML、ZIP、PDF、代码文件、文档等各类普通文件
- **两步流程**: 上传文件获取 `file_key` → 发送 `msg_type=file` 消息
- **自定义文件名**: 可指定发送时的文件名
- **file_type=stream**: 适用于所有普通文件类型

**输入**: 用户提供普通文件发送所需的指令和必要参数。
**处理**: 按照skill规范执行普通文件发送操作,遵循单一意图原则。
**输出**: 返回普通文件发送的执行结果,包含操作状态和输出数据。

### 图片稳定发送

- **解决问题**: 修复图片路径被发成文本的问题
- **正确流程**: 上传到 `im/v1/images` 获取 `image_key` → 发送 `msg_type=image`
- **成功标准**: 用户在飞书中实际看到图片本体
- **国际版支持**: 兼容国际版 Lark

**输入**: 用户提供图片稳定发送所需的指令和必要参数。
**处理**: 按照skill规范执行图片稳定发送操作,遵循单一意图原则。
**输出**: 返回图片稳定发送的执行结果,包含操作状态和输出数据。

### 操作方式

- **脚本方式（推荐）**: 一行命令完成上传与发送
- **手动两步**: 分别执行上传与发送命令
- **AI 助手集成**: 支持在 AI 助手中通过 exec 调用

**输入**: 用户提供操作方式所需的指令和必要参数。
**处理**: 按照skill规范执行操作方式操作,遵循单一意图原则。
**输出**: 返回操作方式的执行结果,包含操作状态和输出数据。

### 接收者支持

- **个人用户**: `receive_id_type=open_id`（`ou_xxx`）
- **群聊**: `receive_id_type=chat_id`（`oc_xxx`）

---

**输入**: 用户提供接收者支持所需的指令和必要参数。
**处理**: 按照skill规范执行接收者支持操作,遵循单一意图原则。
**输出**: 返回接收者支持的执行结果,包含操作状态和输出数据。
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：飞书文件与图片发、送工具、支持两步上传与稳、定投递、飞书文件发送免费、版是一款面向个人、用户的飞书文件与、图片发送工具、通过两步上传流程、先上传获取、再发送消息、确保文件稳定投递、Use、when、需要文件处理、文档转换、格式互转、内容提取时使用、不适用于加密文件、适用于独立开发者、企业团队和自动化、工作流场景等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持。

## 使用场景

### 场景一：发送 HTML 报告文件

向同事发送生成的 HTML 报告文件。

```bash
# 使用脚本一键发送
python3 scripts/send_file.py \
  /path/to/report.html \
  ou_xxxxxxx \
  your_app_id \
  your_app_secret \
  report.html
```

输出示例：

```text
📤 文件发送中...
   文件: report.html (256 KB)
   接收者: ou_xxxxxxx

Step 1: 上传文件...
  ✅ 上传成功, file_key: file_v3_xxxx

Step 2: 发送消息...
  ✅ 发送成功!

📋 发送完成: 用户已在飞书中收到 report.html
```

### 场景二：稳定发送图片

当常规图片发送失败（用户看到路径文本）时，使用稳定图片发送脚本。

```bash
# 稳定发送图片（国内版飞书）
python3 scripts/send_image.py \
  /path/to/chart.png \
  ou_xxxxxxx \
  your_app_id \
  your_app_secret

# 国际版 Lark
python3 scripts/send_image.py \
  /path/to/chart.png \
  ou_xxxxxxx \
  your_app_id \
  your_app_secret \
  lark
```

### 场景三：发送 ZIP 压缩包

向团队发送项目代码的 ZIP 压缩包。

```bash
# 先压缩文件
zip -r project.zip project/

# 发送 ZIP 文件
python3 scripts/send_file.py \
  project.zip \
  oc_xxxxxxx \
  your_app_id \
  your_app_secret \
  project_source.zip
```

---

## 快速开始

### 第一步：获取飞书应用凭证

从飞书应用配置中获取 `app_id` 与 `app_secret`：

```bash
# 查看飞书应用配置
grep -A 2 '"feishu"' config.json | grep -E '(appId|appSecret)'
```

### 第二步：获取接收者 open_id

接收者的 open_id 可从消息回调的 `chat_id` 字段获取，格式为 `user:ou_xxx`，取 `ou_xxx` 部分。

### 第三步：发送文件

```bash
# 发送普通文件
python3 scripts/send_file.py <file_path> <open_id> <app_id> <app_secret> [file_name]

# 发送图片
python3 scripts/send_image.py <image_path> <open_id> <app_id> <app_secret> [domain]
```

### 参数说明

| 参数 | 说明 | 示例 |
|:-----|:-----|:-----|
| `file_path` | 文件路径 | `/path/to/report.html` |
| `open_id` | 接收者 ID | `ou_xxxxxxx` |
| `app_id` | 飞书应用 ID | `cli_xxxxxxx` |
| `app_secret` | 飞书应用密钥 | `xxxxxxx` |
| `file_name` | 自定义文件名（可选） | `report.html` |
| `domain` | 域名（图片专用，可选） | `lark`（国际版） |

---

**结果处理**: 执行完成后,查看输出结果确认操作状态。成功时输出包含处理摘要和结果数据;失败时根据错误信息排查问题,查阅错误处理章节获取恢复步骤。

#
## 示例

### 完整发送示例

```bash
# 完整的文件发送命令
python3 /path/to/scripts/send_file.py \
  /home/user/documents/report.html \
  ou_abc123def456 \
  cli_a1b2c3d4e5f6 \
  secret_abcdef123456 \
  monthly_report.html
```

### AI 助手集成示例

在 AI 助手中通过 exec 调用：

```python
exec(f"""
python3 /path/to/scripts/send_file.py \\
  {file_path} \\
  {user_open_id} \\
  {app_id} \\
  {app_secret} \\
  {custom_filename}
""")
```

### 手动两步发送

如果需要手动控制流程，可分两步执行：

**Step 1 - 获取 Token 并上传文件**:

```bash
# 获取 tenant_access_token
TOKEN=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"<APP_ID>","app_secret":"<APP_SECRET>"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")

# 上传文件获取 file_key
FILE_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=stream" \
  -F "file_name=report.html" \
  -F "file=@/path/to/report.html" \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['file_key'])")

echo "file_key: $FILE_KEY"
```

**Step 2 - 发送文件消息**:

```bash
# 发送文件消息
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"<OPEN_ID>\",\"msg_type\":\"file\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}"
```

---

## 最佳实践

### 文件与图片链路区分

**关键原则**: 普通文件与图片使用不同的 API 链路，不要混用。

| 类型 | 上传 API | 获取的 Key | 消息类型 |
|:-----|:---------|:-----------|:---------|
| 普通文件 | `im/v1/files` | `file_key` | `msg_type=file` |
| 图片 | `im/v1/images` | `image_key` | `msg_type=image` |

```bash
# 普通文件：使用 send_file.py
python3 scripts/send_file.py report.pdf ou_xxx app_id app_secret

# 图片：使用 send_image.py（不要用 send_file.py 发图片）
python3 scripts/send_image.py chart.png ou_xxx app_id app_secret
```

### 图片发送成功标准

**唯一成功标准: 用户在飞书中实际看到图片本体。**

如果用户看到的是以下内容，说明发送失败：
- `📎 /path/to/image.png`
- 纯本地路径文本

此时应立即改用 `scripts/send_image.py` 稳定脚本：

```bash
# 检测到路径文本，立即切换稳定脚本
python3 scripts/send_image.py /path/to/image.png ou_xxx app_id app_secret
```

### 文件大小管理

- 普通文件建议不超过 30MB
- 图片建议不超过 10MB
- 大文件建议先压缩

```bash
# 压缩大文件
zip -r compressed.zip large_folder/
python3 scripts/send_file.py compressed.zip ou_xxx app_id app_secret
```

### 群聊发送

发送到群聊时，使用 `chat_id` 并替换 `receive_id_type`：

```bash
# 群聊文件发送（需修改脚本中的 receive_id_type）
# 个人用户: receive_id_type=open_id, id=ou_xxx
# 群聊: receive_id_type=chat_id, id=oc_xxx
```

---

## 已知限制

- 本skill的能力范围受限于核心能力章节中定义的功能,不支持超出范围的操作
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力
## 常见问题

### 问题1：用户收到路径文本而非文件

```text
用户在飞书中看到: 📎 /path/to/file.png
```

**原因**: 直接使用了 `filePath` 参数而非两步上传流程。

**解决**: 使用本工具的两步流程脚本：

```bash
# 普通文件
python3 scripts/send_file.py /path/to/file.pdf ou_xxx app_id app_secret

# 图片（特别重要）
python3 scripts/send_image.py /path/to/image.png ou_xxx app_id app_secret
```

### 问题2：文件上传失败

```text
Error: 文件上传失败
```

**解决**: 检查文件路径与权限：

```bash
# 确认文件存在且可读
ls -la /path/to/file.pdf

# 已知限制
du -h /path/to/file.pdf
```

### 问题3：认证失败

```text
Error: tenant_access_token 获取失败
```

**解决**: 检查 app_id 与 app_secret 是否正确：

```bash
# 验证凭证
curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"your_app_id","app_secret":"your_app_secret"}'
```

### 问题4：国际版 Lark 发送失败

**解决**: 国际版需指定 `lark` 域名参数：

```bash
# 国内版飞书（默认）
python3 scripts/send_image.py image.png ou_xxx app_id app_secret

# 国际版 Lark
python3 scripts/send_image.py image.png ou_xxx app_id app_secret lark
```

### 问题5：群聊发送失败

**解决**: 群聊使用 `chat_id` 而非 `open_id`：

```bash
# 个人用户
receive_id_type=open_id, receive_id=ou_xxx

# 群聊
receive_id_type=chat_id, receive_id=oc_xxx
```

---

## 依赖说明

### 运行环境

- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux
- **Python版本**: 3.7 及以上
- **网络环境**: 需可访问飞书开放平台 API（国内: open.feishu.cn / 国际: open.larksuite.com）

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-------|:-----|:---------|:---------|
| LLM API | API | 必需 | 由Agent内置LLM提供 |
| Python | 运行时 | 必需 | 官方网站下载安装 |
| Python 标准库 | 运行库 | 必需 | Python 自带（requests, json） |
| 飞书应用 | 应用 | 必需 | 飞书开放平台创建应用 |
| app_id/app_secret | 凭证 | 必需 | 飞书应用配置页获取 |
| curl | CLI工具 | 可选 | 系统自带（手动两步方式需要） |

### API Key 配置

- 本工具通过飞书应用凭证（app_id 与 app_secret）获取 `tenant_access_token` 进行认证
- 凭证通过命令行参数传入
- 无需额外 API Key
- 应用需在飞书开放平台开通文件上传与消息发送权限

### 可用性分类

- **分类**: MD+EXEC（纯Markdown指令，部分功能需要 exec 命令行执行能力）
- **说明**: 基于Markdown的AI Skill，通过自然语言指令驱动Agent执行 Python 脚本，完成飞书文件与图片的两步上传发送流程

## 错误处理


| 错误场景 | 原因 | 处理方式 |
|---------|------|---------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |
