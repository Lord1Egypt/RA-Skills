---
name: "deepwiki-ask"
description: "通过 DeepWiki MCP 查询仓库信息。支持提问、获取结构、获取文档内容。Query a repository via DeepWiki MCP: ask questions, get structure, get documentation. 用户提供 owner/repo 时触发。"
---

# DeepWiki 仓库查询

通过 DeepWiki MCP 对指定仓库发起查询，支持三种操作模式：提问、获取仓库结构、获取文档内容。

## 触发场景

- 用户询问某仓库的作用、结构或功能
- 用户提供仓库名（owner/repo）并带有问题
- 用户需要了解仓库的整体结构
- 用户需要查看仓库的详细文档内容

## 参数

| 参数   | 必填 | 说明           |
|--------|------|----------------|
| repo   | 是   | 仓库名 owner/repo |
| question | 否 | 要问的问题（提问模式） |
| structure | 否 | 获取文档结构（结构模式） |
| contents | 否 | 获取文档内容（内容模式） |
| topic | 否 | 指定文档主题（与 contents 一起使用） |

## 执行流程

### 提问模式
1. 从用户消息提取 **repo**（owner/repo）和 **question**。
2. 执行（必须加 `--json`）：
   ```
   python <SKILL_ROOT>/deepwiki_ask.py -r <owner/repo> -q "<question>" --json
   ```
   Windows 下中文问题若编码异常，可把问题写入 UTF-8 文件后：`-q @<SKILL_ROOT>/temp_q.txt`

### 结构模式
1. 从用户消息提取 **repo**（owner/repo）。
2. 执行（必须加 `--json`）：
   ```
   python <SKILL_ROOT>/deepwiki_ask.py -r <owner/repo> --structure --json
   ```

### 内容模式
1. 从用户消息提取 **repo**（owner/repo）和可选的 **topic**。
2. 执行（必须加 `--json`）：
   ```
   python <SKILL_ROOT>/deepwiki_ask.py -r <owner/repo> --contents --json
   python <SKILL_ROOT>/deepwiki_ask.py -r <owner/repo> --contents --topic "<topic_name>" --json
   ```

3. 解析 stdout JSON：`status == "success"` 则根据操作模式展示相应结果；`status == "error"` 则提示 `message`。
4. 请求可能需 30–120 秒，需等待。

## 输出示例

### 提问模式
```json
{"status": "success", "repo": "owner/repo", "mode": "question", "question": "...", "result": "..."}
```

### 结构模式
```json
{"status": "success", "repo": "owner/repo", "mode": "structure", "result": "..."}
```

### 内容模式
```json
{"status": "success", "repo": "owner/repo", "mode": "contents", "result": "..."}
```

### 错误响应
```json
{"status": "error", "repo": "owner/repo", "message": "..."}
```

## 配置

`config.json`：`request_timeout_seconds`（10–600，默认 120）、`request_max_retries`（0–10，默认 3）。

## 错误处理

- 仓库格式错误：提示 owner/repo 格式
- 超时/网络错误：脚本重试后返回 `status: "error"`，需要提示用户检查网络

## 历史版本

**v1.1.0** (2026-03-14)
- 📋 支持获取文档结构（--structure）
- 📄 支持获取文档内容（--contents）
- 📄 支持指定文档主题（--topic）
- 🔄 重构为 MCP 客户端类，移除 requests 依赖，改用标准库 urllib

**v1.0.0** (2026-03-10)
- 🎉 初始版本发布
- 📖 支持 owner/repo + question 单次问答
