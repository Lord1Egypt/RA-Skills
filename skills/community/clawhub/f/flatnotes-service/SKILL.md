---
name: flatnotes-service
description: Flatnotes 笔记服务操作技能。用于创建、搜索、获取、更新、删除 Markdown 笔记，支持全文搜索和附件管理。**必需环境变量**：FLATNOTES_BASE_URL（服务地址）、FLATNOTES_USERNAME（用户名）、FLATNOTES_PASSWORD（密码，敏感）。使用时必须先获取用户明确同意。
homepage: https://cnb.cool/iceicc-ai-made/skills
---

# Flatnotes 笔记服务

用于与 Flatnotes 笔记服务交互，支持创建、搜索、管理 Markdown 笔记。

## 使用场景

1. **保存长文本报告** - 将股票行情分析、调研报告等长内容保存为笔记
2. **格式化输出** - 利用 Markdown 支持生成带格式的文档
3. **内容检索** - 搜索已有笔记，获取历史记录
4. **知识沉淀** - 将对话中的重要信息保存到笔记系统

## 环境变量配置

```bash
export FLATNOTES_BASE_URL="https://your-flatnotes-host"  # 服务地址
export FLATNOTES_USERNAME="your-username"
export FLATNOTES_PASSWORD="your-password"
```

> 所有配置项均通过环境变量注入，脚本不包含任何硬编码地址或凭证。

添加到 `~/.bashrc` 后执行 `source ~/.bashrc` 生效。

> 服务当前启用密码认证 (`authType: password`)，脚本会自动使用账号密码获取访问令牌。

### 自动检测机制

**重要**：执行技能前，先检查环境变量是否已配置：
- 如果三个环境变量均已设置 → **先向用户确认**是否需要调用（如"是否保存到笔记？"），获得同意后再执行
- 如果环境变量未配置 → 提示用户配置后再执行

> ⚠️ **注意**：使用存储的凭证前必须获得用户明确同意，禁止在用户未确认的情况下自动操作。

示例检查命令：
```bash
if [ -n "$FLATNOTES_BASE_URL" ] && [ -n "$FLATNOTES_USERNAME" ] && [ -n "$FLATNOTES_PASSWORD" ]; then
    echo "环境变量已配置，可直接调用"
else
    echo "环境变量未配置，需要设置"
fi
```

## 核心功能

### 获取令牌
脚本会自动处理认证，如需手动获取令牌：
```bash
python3 scripts/get_token.py [--username USER] [--password PASS] [--base-url URL]
```

### 创建笔记

**使用脚本（推荐）**:
```bash
python3 scripts/create_note.py "笔记标题" "笔记内容"
```

**直接 API 调用**:
```bash
curl -X POST $FLATNOTES_BASE_URL/api/notes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title": "标题", "content": "# Markdown 内容"}'
```

### 搜索笔记

**使用脚本（推荐）**:
```bash
python3 scripts/search_notes.py "关键词" --limit 10
```

**可用参数**:
- `--sort`: `score` (默认) | `title` | `lastModified`
- `--order`: `desc` (默认) | `asc`
- `--limit`: 结果数量限制

### 获取笔记

**使用脚本**:
```bash
python3 scripts/get_note.py "笔记标题"
```

### 更新笔记

```bash
curl -X PATCH $FLATNOTES_BASE_URL/api/notes/原标题 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"newTitle": "新标题", "newContent": "新内容"}'
```

### 删除笔记

```bash
curl -X DELETE $FLATNOTES_BASE_URL/api/notes/标题 \
  -H "Authorization: Bearer <token>"
```

## 典型工作流

### 保存股票分析报告

1. 生成报告内容（Markdown 格式）
2. 创建笔记保存:
   ```bash
   python3 scripts/create_note.py "2026-03-12 恒生科技分析" "# 恒生科技指数分析\n\n## 行情概述\n..."
   ```
3. 向用户返回笔记链接/标题

### 检索历史报告

```bash
python3 scripts/search_notes.py "恒生科技" --sort lastModified --limit 5
```

## 数据格式

### 笔记对象
```json
{
  "title": "string",
  "content": "string (Markdown)",
  "lastModified": 1234567890
}
```

### 搜索结果
```json
[
  {
    "title": "string",
    "lastModified": 1234567890,
    "score": 0.95,
    "contentHighlights": "匹配内容高亮..."
  }
]
```

## 完整 API 参考

详见 [references/api_docs.md](references/api_docs.md)

### 认证 API

获取访问令牌：
```bash
POST /api/token
Content-Type: application/json

{
  "username": "用户名",
  "password": "密码"
}
```

返回：
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

> 注意：旧版使用 `/api/login`，新版改为 `/api/token`

## 笔记URL格式

访问笔记的完整URL格式为：

```
https://your-flatnotes-host/note/{笔记标题}
```

**示例**:
- 笔记标题: `太子工作日志 - 2026年3月12日`
- 访问URL: `https://your-flatnotes-host/note/太子工作日志%20-%202026年3月12日`

> 注意：标题中的空格需编码为 `%20`，特殊字符需进行URL编码。

## 注意事项

1. **标题唯一性**: 笔记标题是唯一的，重复创建会返回 409 错误
2. **Markdown 支持**: 内容支持标准 Markdown 语法
3. **全文搜索**: 支持笔记内容和标题的模糊搜索
4. **URL 编码**: 标题含特殊字符时需要 URL 编码
5. **认证方式**: 服务使用 Bearer Token 认证，脚本会自动从环境变量获取凭证并请求令牌
