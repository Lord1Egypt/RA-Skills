---
name: blog-manager
version: 1.0.0
description: >-
  Manage Blog System API v1.0.0 via 27 CLI subcommands covering articles,
  tags, users, comments, messages, moods, uploads, and health checks.
triggers:
  - blog manager
  - manage blog
  - blog system api
  - blog articles
  - blog comments
tags:
  - blog
  - cli
  - api
  - rest
tools:
  - curl
---

# blog-manager

封装 Blog System API v1.0.0，提供 8 模块管理能力，共 27 个子命令（26 操作 + 1 capability-list）。子命令采用 flat kebab-case 命名（动词-名词式）。

## Overview / 概述

blog-manager 封装 Blog System API v1.0.0 的全部 26 个 API 端点，提供 27 个 CLI 子命令（含 capability-list）。

- 目标系统 API 地址：通过环境变量 `BLOG_MANAGER_BASE_URL` 配置（不硬编码）
- 认证方式：无认证（API 开放访问）
- 凭据变量前缀：`BLOG_MANAGER`（仅 `BLOG_MANAGER_BASE_URL`）
- 路径前缀：`/api`（健康检查端点 `/health` 在根路径）

## Prerequisites / 前置条件

- Python 3.8+
- requests 库（`pip install -r requirements.txt`）
- API 地址环境变量：`BLOG_MANAGER_BASE_URL`（须以 `http://` 或 `https://` 开头）

> 未设置时启动即抛 `BlogConfigError`（退出码 2）；地址不硬编码于源码中。

## Workflow / 工作流

1. 从环境变量 `BLOG_MANAGER_BASE_URL` 读取 API 地址（缺失抛 `BlogConfigError`，退出码 2）
2. 按子命令调用对应的 REST API 端点（HTTP 客户端层 `BlogClient`）
3. 输出 JSON + Markdown 双格式结果（`formatter.format_output`）

## Core Commands / 核心命令

### 文章管理（7）

| 子命令 | HTTP 方法 | 端点 | 说明 |
|--------|----------|------|------|
| `list-articles` | GET | /api/articles | 分页列出文章 |
| `create-article` | POST | /api/articles | 创建文章 |
| `get-article` | GET | /api/articles/{id} | 获取文章详情及评论 |
| `update-article` | PUT | /api/articles/{id} | 更新文章 |
| `delete-article` | DELETE | /api/articles/{id} | 删除文章（支持软删除） |
| `restore-article` | POST | /api/articles/{id}/restore | 恢复软删除的文章 |
| `top-articles` | GET | /api/articles/heat/top | 获取热门文章 |

### 标签管理（2）

| 子命令 | HTTP 方法 | 端点 | 说明 |
|--------|----------|------|------|
| `list-labels` | GET | /api/lables | 列出所有标签 |
| `create-label` | POST | /api/lables | 创建标签 |

### 用户管理（2）

| 子命令 | HTTP 方法 | 端点 | 说明 |
|--------|----------|------|------|
| `list-users` | GET | /api/users | 列出所有用户 |
| `create-user` | POST | /api/users | 创建用户 |

### 评论管理（3）

| 子命令 | HTTP 方法 | 端点 | 说明 |
|--------|----------|------|------|
| `create-comment` | POST | /api/comments | 创建评论 |
| `list-comments` | GET | /api/comments/{aid} | 列出文章评论 |
| `delete-comment` | DELETE | /api/comments/{comment_id} | 删除评论 |

### 留言管理（4）

| 子命令 | HTTP 方法 | 端点 | 说明 |
|--------|----------|------|------|
| `list-messages` | GET | /api/messages | 列出留言及回复 |
| `create-message` | POST | /api/messages | 创建留言 |
| `reply-message` | POST | /api/messages/reply | 回复留言 |
| `delete-message` | DELETE | /api/messages/{message_id} | 删除留言 |

### 说说管理（3）

| 子命令 | HTTP 方法 | 端点 | 说明 |
|--------|----------|------|------|
| `list-moods` | GET | /api/moods | 列出说说 |
| `create-mood` | POST | /api/moods | 创建说说 |
| `delete-mood` | DELETE | /api/moods/{mood_id} | 删除说说 |

### 文件上传（4）

| 子命令 | HTTP 方法 | 端点 | 说明 |
|--------|----------|------|------|
| `upload-file` | POST | /api/upload | 上传单个文件（multipart `file`） |
| `upload-files` | POST | /api/upload/multiple | 批量上传文件（multipart `files`） |
| `list-uploads` | GET | /api/uploads/list | 列出已上传文件 |
| `delete-upload` | DELETE | /api/uploads/{filename} | 删除已上传文件（filename URL 编码） |

### 健康检查（1）

| 子命令 | HTTP 方法 | 端点 | 说明 |
|--------|----------|------|------|
| `health-check` | GET | /health | 健康检查 |

### 元信息（1）

| 子命令 | 说明 |
|--------|------|
| `capability-list` | 列出全部 27 个子命令 |

### 使用示例

```bash
export BLOG_MANAGER_BASE_URL="http://your-blog-host:18080"

python3 scripts/blog_manager.py capability-list
python3 scripts/blog_manager.py health-check
python3 scripts/blog_manager.py list-articles --page 1 --size 10
python3 scripts/blog_manager.py create-article --title "标题" --content "正文"
python3 scripts/blog_manager.py delete-article --id 1 --soft false
python3 scripts/blog_manager.py upload-file --file /path/to/image.png
python3 scripts/blog_manager.py upload-files --files a.png b.png

```

## Parameter Confirmation / 参数确认

| 子命令 | 参数 | 必填 | 说明 |
|--------|------|------|------|
| `list-articles` | --page | 否 | 页码，默认 1 |
| `list-articles` | --size | 否 | 每页条数，默认 10 |
| `list-articles` | --lid | 否 | 标签 ID（0=全部），默认 0 |
| `list-articles` | --keyword | 否 | 搜索关键词 |
| `create-article` | --title | 是 | 文章标题 |
| `create-article` | --content | 是 | 文章内容 |
| `create-article` | --uid | 否 | 用户 ID，默认 1 |
| `create-article` | --lid | 否 | 标签 ID，默认 1 |
| `create-article` | --img | 否 | 封面图路径 |
| `create-article` | --heat | 否 | 热度值，默认 0 |
| `get-article` | --id | 是 | 文章 ID |
| `update-article` | --id | 是 | 文章 ID |
| `update-article` | --title | 否 | 新标题 |
| `update-article` | --content | 否 | 新内容 |
| `update-article` | --lid | 否 | 标签 ID |
| `update-article` | --img | 否 | 封面图路径 |
| `update-article` | --heat | 否 | 热度值 |
| `delete-article` | --id | 是 | 文章 ID |
| `delete-article` | --soft | 否 | 软删除 true/false，默认 true |
| `restore-article` | --id | 是 | 文章 ID |
| `top-articles` | --limit | 否 | 返回条数，默认 5 |
| `create-label` | --lname | 是 | 标签名称 |
| `create-user` | --uname | 是 | 用户名 |
| `create-user` | --phone | 否 | 手机号 |
| `create-user` | --pwd | 否 | 密码 |
| `create-user` | --email | 否 | 邮箱 |
| `create-user` | --img | 否 | 头像路径，默认 img/moren.jpg |
| `create-comment` | --uid | 是 | 用户 ID |
| `create-comment` | --aid | 是 | 文章 ID |
| `create-comment` | --content | 是 | 评论内容 |
| `list-comments` | --aid | 是 | 文章 ID |
| `delete-comment` | --id | 是 | 评论 ID |
| `create-message` | --uid | 是 | 用户 ID |
| `create-message` | --content | 是 | 留言内容 |
| `reply-message` | --uid | 是 | 用户 ID |
| `reply-message` | --mid | 是 | 留言 ID |
| `reply-message` | --content | 是 | 回复内容 |
| `delete-message` | --id | 是 | 留言 ID |
| `create-mood` | --content | 是 | 说说内容 |
| `create-mood` | --title | 否 | 标题 |
| `create-mood` | --src | 否 | 媒体路径 |
| `delete-mood` | --id | 是 | 说说 ID |
| `upload-file` | --file | 是 | 文件路径 |
| `upload-files` | --files | 是 | 文件路径列表（空格分隔） |
| `delete-upload` | --filename | 是 | 文件名 |

## Reference Documents / 参考文档

- [API 端点文档](references/api-reference.md)
- [测试用例定义](templates/test-vars.json)

## 特殊语义

- **文章软删除/恢复**：`delete-article` 默认软删除（`--soft true`），传 `--soft false` 执行硬删除；`restore-article` 恢复软删除的文章。`soft` 参数以小写字符串 `true`/`false` 传递给后端。
- **批量上传**：`upload-files` 使用 multipart `files` 字段名上传多个文件（实测 API 要求字段名为 `files`，非 `files[]`）。
- **留言回复**：`reply-message` 调用 `/api/messages/reply` 端点。
- **文件名删除**：`delete-upload` 对 `--filename` 做 URL 编码，支持中文及特殊字符。
  - `--filename` 需传服务端存储的哈希文件名，**不是**本地原始文件名。
  - 来源：`list-uploads` 返回的 `filename` 字段，或上传返回的 `data.url` 末段路径。
  - `upload-file` 返回的 `data.filename` 是原始文件名，DELETE 端点不识别。
  - 正确流程：先 `list-uploads` 取 `filename`，或从 `data.url` 末段提取哈希名。

## 排除的端点

端点 #26（`GET /` 博客首页）和 #27（`GET /article/{id}` 文章详情页）为 Web 页面，非 API，不生成子命令。

## 退出码

| 退出码 | 含义 |
|--------|------|
| 0 | 成功 |
| 1 | API 错误 / 文件错误 / 其它异常 |
| 2 | 配置错误（`BLOG_MANAGER_BASE_URL` 未设置或格式非法） |
