---
name: feishu-send-files
description: 飞书文件批量发送技能，支持机器人触发和命令行调用，自动配置，零依赖
keywords:
  - feishu
  - lark
  - file-send
  - 飞书
  - 文件发送
  - 批量发送
license: MIT
metadata:
  {
    "openclaw":
      {
        "emoji": "📁",
        "requires": { "bins": ["node"] },
        "install":
          [
            {
              "id": "manual",
              "kind": "download",
              "label": "手动安装（复制技能文件夹）",
              "url": "https://clawhub.com",
            },
          ],
      },
  }
---

# feishu-send-files 技能说明

## 基础信息

- **技能名称**：feishu-send-files
- **触发指令**：发文件 / 帮我发 / 发送文件 / 自然语言
- **运行入口**：index.js
- **日志路径**：技能目录下 logs/
- **依赖**：无外部依赖（仅 Node.js 内置模块）

## ⚠️ 重要：两种触发模式的区别

### 模式 1：机器人触发（推荐）
**在群里@机器人 或 私聊@机器人**，直接说：
```
发文件 /path/to/file.pptx
发一下这个 PPT
```
✅ **自动识别发送目标**：
- 群里@机器人 → 发到当前群
- 私聊@机器人 → 发到私聊

### 模式 2：命令行调用（手动指定）
**在终端运行**：
```bash
cd /home/node/.openclaw/workspace/skills/feishu-send-files
node index.js --file "/path/to/file.pptx" --to "chat:群聊 ID"
```
⚠️ **必须手动指定发送目标**：
- `--to "chat:oc_xxx"` → 发到群聊
- `--to "open_id:ou_xxx"` → 发到个人
- **不传 `--to` 参数 → 默认发到个人**（容易发错！）

---

## 功能描述

飞书文件发送技能，支持三种模式：

### 1. 精确路径模式（机器人触发）
```
发文件 /home/node/test.pptx
```

### 2. 文件名搜索模式（机器人触发）
```
发文件 test.pdf
```
自动在 workspace 目录查找。

### 3. 模糊匹配 + 交互式选择（机器人触发）
```
把 workspace 里面那个 PPT 文件发给我
发一下 Excel 文件
```
机器人搜索→展示列表→让你选择→发送。

**核心特性**：
- ✅ 递归搜索 workspace 目录（3 层深度）
- ✅ 智能关键词提取（中文 + 英文）
- ✅ 自动文件类型识别（12 种常见格式）
- ✅ 交互式选择（数字/文件名）
- ✅ **批量发送（多文件选择）** - 回复 `1,2,3` 或 `all`
- ✅ 文件大小显示
- ✅ 完整日志记录
- ✅ 错误处理和状态反馈

## 触发规则

```json
{
  "triggers": [
    {"type": "exact_match", "value": "发文件"},
    {"type": "prefix_match", "value": "发文件 "},
    {"type": "mention", "value": "发文件"},
    {"type": "prefix_match", "value": "帮我发"},
    {"type": "prefix_match", "value": "发一下"},
    {"type": "prefix_match", "value": "把文件"},
    {"type": "prefix_match", "value": "发送文件"},
    {"type": "prefix_match", "value": "发这个文件"},
    {"type": "prefix_match", "value": "发那个文件"},
    {"type": "contains", "value": "发文件"},
    {"type": "contains", "value": "发送文件"}
  ]
}
```

## 快速使用指南

### ✅ 推荐：群里@机器人发送
```
@机器人 发文件 /path/to/file.pptx
@机器人 发一下这个 PPT
```
**优点**：自动识别群聊/私聊，不会发错！

### ⚠️ 命令行调用（需要手动指定目标）
```bash
# 发到群聊
node index.js --file "/path/to/file.pptx" --to "chat:oc_群聊 ID"

# 发到个人
node index.js --file "/path/to/file.pptx" --to "open_id:ou_用户 ID"

# 不传 --to 参数 → 默认发到个人（容易发错！）
```

## 命令行参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `--file` | 文件路径（可多次） | `--file "/path/a.pptx" --file "/path/b.pdf"` |
| `--files` | 多个文件（逗号分隔） | `--files "/path/a.pptx,/path/b.pdf"` |
| `--search` | 搜索关键词 | `--search "PPT"` |
| `--to` | **必须指定**发送目标 | `--to "chat:oc_xxx"` 或 `--to "open_id:ou_xxx"` |

## 使用示例

### 精确路径（机器人触发）
```
发文件 /home/node/test.pptx
@机器人 发文件 /path/to/data.xlsx
```

### 文件名搜索（机器人触发）
```
发文件 test.pdf
帮我发一下 report.docx
```

### 模糊匹配（机器人触发）
```
把 workspace 里面那个 PPT 文件发给我
发一下 Excel 文件
帮我发会议纪要
发送那个 PDF
```

**机器人响应**：
```
找到 3 个匹配文件，请选择：

1. test.pptx (2.3 MB)
2. 交易报告.pptx (1.8 MB)
3. 会议纪要.pptx (856 KB)

回复数字选择（如：1）或输入多个数字（如：1,2,3）或输入 "all" 发送全部
```

**批量发送示例**：
```
用户：发 PPT 文件
机器人：找到 3 个文件...请选择
用户：1,3
机器人：✅ 发送完成！成功 2/2 个文件
```

## 快速排错

| 问题 | 解决方法 |
|------|----------|
| **文件发错地方（发到个人而不是群里）** | 机器人触发时自动识别；命令行调用必须加 `--to "chat:群聊 ID"` |
| 文件名异常 | 使用最终版 index.js |
| 无日志 | 赋权 logs 目录：`chmod -R 777 logs` |
| 机器人无响应 | 重启 OpenClaw，检查文件路径 |
| 发送失败 | 检查飞书权限与 appId/appSecret 配置 |
| token 获取失败 | 检查 appId/appSecret 是否正确 |
| 文件上传失败 | 检查文件大小（≤30MB）和网络 |
| 未找到匹配文件 | 检查关键词是否准确，或用绝对路径 |
| 多个匹配文件 | 机器人会列出列表，回复数字或文件名选择 |

## 最佳实践

✅ **推荐**：在群里@机器人发送文件（自动识别群聊）
❌ **避免**：命令行调用时忘记加 `--to` 参数（会发到个人）

## 技术实现

- **Token 获取**：使用 tenant_access_token 内部门户 API
- **文件上传**：multipart/form-data 表单上传到飞书文件接口
- **消息发送**：使用 file_key 发送文件消息
- **日志记录**：同步追加写入，确保不丢失
- **路径提取**：智能识别绝对路径、相对路径、workspace 目录文件
- **模糊搜索**：递归搜索 + 关键词匹配 + 扩展名过滤
- **交互式选择**：展示文件列表，等待用户选择

## 权限要求

- im:message:send_as_bot
- im:message:send_to_chat
- im:message:send_to_open_id
