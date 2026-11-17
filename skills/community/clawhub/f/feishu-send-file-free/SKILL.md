---
slug: "feishu-send-file-free"
name: "feishu-send-file-free"
version: "1.0.0"
displayName: "飞书发文件(免费)"
summary: "飞书发送普通文件附件的基础版,支持file_key两步上传链路。。飞书机器人发送普通文件附件的基础技能。覆盖 HTML、ZIP、PDF、代码文件等普通文件的两步上传链路, 提供脚本化与手动两"
summary_zh: "飞书发送普通文件附件的基础版,支持file_key两步上传链路。。飞书机器人发送普通文件附件的基础技能。覆盖 HTML、ZIP、PDF、代码文件等普通文件的两步上传链路, 提供脚本化与手动两"
license: "MIT"
description: "|-. 适用于需要feishu send file相关能力的开发场景,包含结构化的工作流程和可复用的模板,帮助用户快速完成任务并保持代码质量.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性.该技能适用于相关开发场景,包含结构化的工作流程和配置指引.经过深度差异化处置,针对用户反馈和使用痛点进行了改进,提升了实用性和可操作性."
  飞书机器人发送普通文件附件的基础技能。覆盖 HTML、ZIP、PDF、代码文件等普通文件的两步上传链路,
  提供脚本化与手动两种调用方式。适用于个人开发者与轻量级文件投递场景.
  本免费版仅支持普通文件链路,图片稳定发送与国际版 Lark 适配等高级能力请升级付费版.
tags:
  - 研发工具
  - feishu
  - send
  - file
  - automation
  - 工具
  - 效率
  - 通信
  - html
  - file_key
tools:
  - read
  - exec
  - glob
  - grep
homepage: ""
category: "Automation"
pricing_tier: free
---
# feishu-send-file-free

飞书机器人发送普通文件附件需要两步:先上传文件到 `im/v1/files` 获取 `file_key`,再用 `file_key` 发送 `msg_type=file` 消息。直接把本地路径塞给消息发送器只会显示路径文本.
本免费版封装普通文件两步上传链路的基础调用方式.
## 输入格式

| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | 飞书发文件(免费)处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

## 依赖说明

### 运行环境
- **Agent平台**: 支持SKILL.md的任意AI Agent（Claude Code / Cursor / Codex / Gemini CLI等）
- **操作系统**: Windows / macOS / Linux

### 依赖项
| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:-----|:-----|:-----|:-----|
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置
需要配置对应API Key，详见上文环境配置章节

### 可用性分类
- **分类**: MD+EXEC（）

**API Key配置方式**:
```bash
export API_KEY=${API_KEY:?请设置环境变量}
```
配置后需重启会话或开启新终端生效。API Key应妥善保管,避免泄露到版本控制系统.
## 核心能力

- 普通文件两步发送:上传到 `im/v1/files` 获取 `file_key`,再用 `msg_type=file` 推送到指定 `open_id`
- 文件类型统一处理:普通文件一律使用 `file_type=stream`,兼容 HTML、ZIP、PDF、代码文件、CSV 等
- 脚本化调用:通过 `send_file.py` 一键完成上传与发送两步
- 手动两步调用:支持 curl 手动执行,便于排查问题
#
## 快速开始

1. 确认运行环境满足依赖说明中的要求
2. 在AI Agent对话中调用本技能,提供必要的输入参数
3. 检查输出结果,根据需要进行后续处理

> 详细的输入输出格式请参考下方章节说明。

## 使用流程

1. **环境确认**: 确认Agent平台已加载本skill，检查依赖说明中的环境要求
2. **指令输入**: 向Agent描述需要执行的任务，引用`feishu-send-file-free`的相关能力
3. **执行处理**: Agent按照核心能力章节的指令执行任务
4. **结果验证**: 检查输出结果是否符合预期，参考错误处理章节处理异常

#
## 调用方式

### 方式一:脚本化调用(推荐)

```bash
python3 （请参考skill目录中的脚本文件） <file_path> <open_id> <app_id> <app_secret> [file_name]
```

参数说明:

- `file_path`:要发送的文件本地路径(HTML/PDF/ZIP/代码文件等)
- `open_id`:接收者 open_id,格式 `ou_identifier`
- `app_id`:飞书应用 ID,从 `skill-platform.json` 的 `channels.feishu.appId` 读取
- `app_secret`:飞书应用密钥,从 `skill-platform.json` 的 `channels.feishu.appSecret` 读取
- `file_name`:可选,自定义文件名,不填则用原文件名

快速读取应用配置:

```bash
grep -A 2 '"feishu"' /root/.skill-platform/skill-platform.json | grep -E '(appId|appSecret)'
```

完整示例:

```bash
python3 /root/.skill-platform/workspace/skills/feishu-send-file/（请参考skill目录中的脚本文件） \
  /root/myfiles/report.html \
  ou_abc123def456 \
  cli_a1b2c3d4e5f6g7h8 \
  secretAbCdEfGhIjKlMnOp \
  weekly-report.html
```

### 方式二:手动两步

Step 1 - 获取 token 并上传文件:

```bash
TOKEN=$(# 安全数据传输示例/internal" \
  -H "Content-Type: application/json" \
  -d '{"app_id":"<APP_ID>","app_secret":"<APP_SECRET>"}' \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])")
# ...
FILE_KEY=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/files" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file_type=stream" \
  -F "file_name=<文件名>" \
  -F "file=@<文件路径>" \
load(sys.stdin)['data']['file_key'])")
```

Step 2 - 发送文件消息:

```bash
curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=open_id" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"receive_id\":\"<OPEN_ID>\",\"msg_type\":\"file\",\"content\":\"{\\\"file_key\\\":\\\"$FILE_KEY\\\"}\"}"
```

## 适用场景

### 场景一:开发者本地文件投递

输入:本地 HTML 报告 `/root/myfiles/report.html`、接收者 `ou_identifier`、飞书应用凭证
输出:用户在飞书会话中收到 `report.html` 文件附件,可点击预览或下载

### 场景二:轻量级 PDF 分发

输入:周报 PDF `/root/reports/weekly.pdf`、接收者 `ou_identifier`、应用凭证
输出:用户收到 PDF 附件消息,可下载查看

## 案例展示

### 案例一:HTML 报告投递失败排查

某用户反馈飞书机器人发送的 HTML 报告,接收方只看到 `📎 /root/myfiles/report.html` 文本,无法点击预览.
排查步骤:
1. 检查发送链路,确认使用的是 `message` 工具的 `filePath` 参数直传本地路径
2. 确认这是降级回显,不是真正发送成功
3. 改用脚本化调用:

```bash
python3 /root/.skill-platform/workspace/skills/feishu-send-file/（请参考skill目录中的脚本文件） \
  ou_abc123def456 \
  cli_a1b2c3d4e5f6g7h8 \
  secretAbCdEfGhIjKlMnOp \
  report.html
```

4. 接收方在飞书中收到可预览的 HTML 文件附件,问题解决.
## 异常处理

### 1. tenant_access_token 获取失败

现象:`curl` 返回 `app_access_token` 为空或 HTTP 401
原因:`app_id` 或 `app_secret` 错误、应用已被停用
处理:核对 `skill-platform.json` 中 `channels.feishu.appId` 与 `appSecret`,确认应用在飞书开放平台处于启用状态

### 2. 文件上传返回 230002

现象:上传到 `im/v1/files` 返回 code `230002`
原因:文件大小超过 30MB 限制,或 `file_type` 取值非法
处理:确认文件不超过 30MB;普通文件一律用 `file_type=stream`,不要用 `pdf`、`opus` 等枚举值

### 3. 发送消息返回 230001

现象:调用 `im/v1/messages` 返回 code `230001`
原因:`receive_id` 格式错误或机器人未与接收者建立会话
处理:`open_id` 应为 `ou_` 开头的纯 ID(不含 `user:` 前缀);首次发送需接收者先向机器人发过任意消息建立会话

### 4. 文件名含中文导致上传失败

现象:`file_name` 含中文或特殊字符时上传返回 400
原因:curl `-F` 参数编码问题
处理:使用脚本化调用,Python 脚本内部已处理编码;手动调用时确保 `file_name` 与本地文件名一致且为 UTF-8

### 5. file_key 过期导致发送失败

现象:Step 1 拿到 `file_key` 后延迟较久,Step 2 发送返回 `file_key` 无效
原因:`file_key` 有效期有限,通常需在获取后立即使用
处理:两步操作应连续执行,不要间隔超过数分钟;脚本化调用已自动连续执行

## FAQ

### Q1:为什么文件发送返回成功,但用户看不到文件?

`messageId` 返回成功只代表消息已投递到飞书服务器,不代表用户看到文件本体。如果用户看到的是 `📎 /root/...` 路径文本,说明本地路径被降级回显,需要改用本技能的两步上传链路.
### Q2:普通文件和图片可以走同一条链路吗?

不可以。普通文件走 `im/v1/files` 获取 `file_key` 发 `msg_type=file`,图片需走 `im/v1/images` 获取 `image_key` 发 `msg_type=image`。本免费版仅支持普通文件链路,图片链路请升级付费版.
### Q3:如何获取接收者的 open_id?

从 inbound_meta 的 `chat_id` 字段获取,格式为 `user:ou_identifier`,取 `ou_identifier` 部分.
### Q4:file_type 必须用 stream 吗?

是的。普通文件一律使用 `file_type=stream`,这是飞书 API 对通用文件的统一类型。`pdf`、`opus`、`mp4` 等枚举值仅用于特定媒体类型,普通文件使用会导致上传失败.
## 错误处理

| 错误场景 | 原因 | 处理方式 |
|---:|---:|---:|
| LLM响应超时或无响应 | 网络延迟或模型负载过高 | 检查网络连接和配置后重试；确认Agent平台LLM服务正常 |
| 输入内容格式不正确 | 用户输入不符合skill预期格式 | 检查输入是否符合skill使用说明中的格式要求，参考示例章节 |
| 执行结果与预期不符 | 指令描述不够明确或上下文不足 | 提供更详细的指令描述，补充必要的上下文信息 |
| 命令执行失败 | 运行环境不满足要求或权限不足 | 确认运行环境符合依赖说明中的要求；检查命令权限设置 |

## 已知限制

- 普通文件单文件大小上限 30MB,超过需拆分或使用飞书云文档
- `file_key` 有有效期,获取后需立即使用,不适合异步流水线长时间间隔
- 机器人主动推送需用户先建立会话,冷启动场景需引导用户触发
- 本免费版不支持图片稳定发送链路,不支持国际版 Lark 域名适配,不支持群聊 `chat_id` 发送

## 升级提示

本免费版仅覆盖普通文件两步上传基础链路。如需以下能力,请升级到付费版 `feishu-send-file`:

- 图片稳定发送(`send_image.py`,解决本地图片路径被发成文本的故障)
- 国际版 Lark 域名适配(`open.larksuite.com`)
- 群聊 `chat_id` 批量推送
- 完整的 8 类领域异常处理与 6 类 FAQ 排查指引

## 输出格式

```json
{
  "success": true,
  "data": {
    "result": "飞书发文件(免费)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "feishu-send-file"
    }
  },
  "execution_log": [
    "解析输入参数",
    "执行核心处理",
    "格式化输出结果"
  ],
  "error": null
}
```
