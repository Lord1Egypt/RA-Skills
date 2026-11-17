---
name: blog-toolkit
version: 1.0.0
description: |
  管理 Blog System API v1.0.0 的文章/标签/用户/评论/留言/说说/文件上传/健康检查。
  无认证公开 API，27 个子命令（26 API + 1 capability-list），输出 JSON 与 Markdown 表格。
  纯 CLI 管理 skill，不含 Grape Agent 加载集成与自动回复 Issue 能力。
triggers:
  - 博客工具
  - blog toolkit
  - 博客管理
  - blog-toolkit
tags:
  - blog
  - rest-api
  - content-management
  - blog-system
  - cli
tools:
  - curl
---

# blog-toolkit

## 安全硬约束（必须遵守）

1. **敏感信息隔离**：API Key / Token / 密码等敏感信息只从环境变量或项目知识（.project-info/member/）读取，严禁写入文件/日志/评论/脚本常量。
2. **API 调用超时**：所有 API 调用设 30s 超时（timeout=30），超时判定失败，不 hang。
3. **403/429 处理**：API 返回 403（无权限）/ 429（限流）时停止重试并报告，不绕行。
4. **长命令静默**：文件上传/批量上传/大响应处理会静默，提前告知用户等待。

## Overview / 概述

管理 Blog System API v1.0.0（文章/标签/用户/评论/留言/说说/文件上传/健康检查）。
基于 OpenAPI 文档自动解析生成，覆盖 26 个 API 端点 + 1 个 capability-list，共 27 个子命令。

纯 CLI 管理 skill——无 Grape Agent 加载集成（frontmatter 无 `agent` 字段，无 `handle-event` 事件入口）、
无自动回复 Issue 能力（无 `--issue-number` 参数，无 `auto_reply` 配置）。可与管理相同 API 的其他 skill 共存。

- **目标系统 API 地址**：{base_url}（运行时动态获取，不硬编码——见下方解析优先级）
- **API 路径前缀**：/api（健康检查为 /health）
- **认证方式**：无认证（none，公开 API）
- **凭据变量前缀**：BLOG_TOOLKIT（无认证模式仅需 BASE_URL）
- **地址环境变量**：BLOG_TOOLKIT_BASE_URL（覆盖默认地址）

> 标签管理 API 路径为 `/api/lables`（原文拼写），子命令使用正确拼写 `labels`
>（list-labels / create-label），脚本内部请求仍走 `/api/lables`。

### base_url 解析优先级

1. 项目知识（.project-info/member/ 下文件，向上递归查找，支持 JSON/YAML/Markdown，只读 base_url/api_url/host）
2. 环境变量 `BLOG_TOOLKIT_BASE_URL`
3. 交互输入（缺失时提示用户输入，以 http:// 或 https:// 开头）

> ⚠️ API 地址不硬编码在 SKILL.md / 脚本常量里——由脚本运行时动态获取。

## Prerequisites / 前置条件

- Python 3.8+
- requests 库（`pip install -r requirements.txt`）
- 博客 API 地址（三选一，优先级从高到低）：
  1. 项目知识：在 .project-info/member/ 下配置文件中添加 `BLOG_TOOLKIT_BASE_URL` / `base_url` / `api_url` / `host`
  2. 环境变量：`export BLOG_TOOLKIT_BASE_URL="http://host:port"`
  3. 运行时交互输入（缺失环境变量时脚本自动提示）

```bash
export BLOG_TOOLKIT_BASE_URL="http://host:port"
```

如需切换 API 地址（如测试→生产），覆盖该环境变量即可。

## Workflow / 工作流

1. 从项目知识/环境变量 `BLOG_TOOLKIT_BASE_URL` 读取 API 地址（缺失时交互提示输入）
2. 按子命令调用对应的 REST API 端点（无认证直接请求）
3. 输出 JSON（默认）或 Markdown 表格（`--format md`）
4. 退出码：0=成功；2=参数错误；3=缺少配置（地址）；4=API 调用失败

## Core Commands / 核心命令

### 文章管理（7）

| 子命令 | HTTP 方法 | 端点 | 说明 |
|--------|----------|------|------|
| list-articles | GET | /api/articles | 分页查询文章列表（关联用户名和标签名） |
| create-article | POST | /api/articles | 发布新文章 |
| get-article | GET | /api/articles/{article_id} | 查询单篇文章详情（含评论） |
| update-article | PUT | /api/articles/{article_id} | 更新文章 |
| delete-article | DELETE | /api/articles/{article_id} | 删除文章（默认软删除，soft=false 硬删除） |
| restore-article | POST | /api/articles/{article_id}/restore | 恢复软删除的文章 |
| top-articles | GET | /api/articles/heat/top | 获取热门文章 Top N |

### 标签管理（2）

| 子命令 | HTTP 方法 | 端点 | 说明 |
|--------|----------|------|------|
| list-labels | GET | /api/lables | 获取所有标签（路径拼写为 lables） |
| create-label | POST | /api/lables | 创建标签（路径拼写为 lables） |

### 用户管理（2）

| 子命令 | HTTP 方法 | 端点 | 说明 |
|--------|----------|------|------|
| list-users | GET | /api/users | 获取用户列表 |
| create-user | POST | /api/users | 创建用户 |

### 评论管理（3）

| 子命令 | HTTP 方法 | 端点 | 说明 |
|--------|----------|------|------|
| list-comments | GET | /api/comments/{aid} | 获取文章的评论列表 |
| create-comment | POST | /api/comments | 发表评论 |
| delete-comment | DELETE | /api/comments/{comment_id} | 删除评论（软删除） |

### 留言管理（4）

| 子命令 | HTTP 方法 | 端点 | 说明 |
|--------|----------|------|------|
| list-messages | GET | /api/messages | 获取留言列表（含回复） |
| create-message | POST | /api/messages | 发表留言 |
| reply-message | POST | /api/messages/reply | 回复留言 |
| delete-message | DELETE | /api/messages/{message_id} | 删除留言（软删除） |

### 说说管理（3）

| 子命令 | HTTP 方法 | 端点 | 说明 |
|--------|----------|------|------|
| list-moods | GET | /api/moods | 获取说说列表 |
| create-mood | POST | /api/moods | 发布说说 |
| delete-mood | DELETE | /api/moods/{mood_id} | 删除说说 |

### 文件上传（4）

| 子命令 | HTTP 方法 | 端点 | 说明 |
|--------|----------|------|------|
| upload-file | POST | /api/upload | 上传单个文件（multipart/form-data） |
| upload-files | POST | /api/upload/multiple | 批量上传文件（multipart/form-data） |
| list-uploads | GET | /api/uploads/list | 列出所有已上传文件 |
| delete-upload | DELETE | /api/uploads/{filename} | 删除已上传文件 |

### 健康检查（1）

| 子命令 | HTTP 方法 | 端点 | 说明 |
|--------|----------|------|------|
| health-check | GET | /health | 健康检查 |

### 能力清单（1）

| 子命令 | HTTP 方法 | 端点 | 说明 |
|--------|----------|------|------|
| capability-list | - | - | 列出本 skill 所有能力项 |

> 排除项：`GET /`（博客首页）与 `GET /article/{id}`（文章详情页）为 Web 页面端点，
> 非 API，不生成子命令。

使用示例：

```bash
# 进入 skill 目录后执行（所有命令在 skills/blog-toolkit/ 目录下运行）
cd skills/blog-toolkit/
export BLOG_TOOLKIT_BASE_URL="http://host:port"

# 文章管理
python3 scripts/blog-toolkit.py list-articles --page 1 --size 10
python3 scripts/blog-toolkit.py list-articles --lid 12 --keyword 美食 --format md
python3 scripts/blog-toolkit.py get-article --article-id 1 --format md
python3 scripts/blog-toolkit.py top-articles --limit 5

# 标签管理（子命令用正确拼写 labels，API 路径为 /api/lables）
python3 scripts/blog-toolkit.py list-labels
python3 scripts/blog-toolkit.py create-label --lname 新标签

# 用户管理
python3 scripts/blog-toolkit.py list-users
python3 scripts/blog-toolkit.py create-user --uname alice --email alice@x.com

# 评论管理
python3 scripts/blog-toolkit.py list-comments --aid 1
python3 scripts/blog-toolkit.py create-comment --uid 1 --aid 1 --content "好文章"

# 留言管理
python3 scripts/blog-toolkit.py list-messages
python3 scripts/blog-toolkit.py create-message --uid 1 --content "你好"
python3 scripts/blog-toolkit.py reply-message --uid 1 --mid 4 --content "回复"

# 说说管理
python3 scripts/blog-toolkit.py list-moods
python3 scripts/blog-toolkit.py create-mood --content "今天心情不错"

# 文件上传
python3 scripts/blog-toolkit.py upload-file --file /path/to/img.png
python3 scripts/blog-toolkit.py upload-files --files a.png b.png
python3 scripts/blog-toolkit.py list-uploads
python3 scripts/blog-toolkit.py delete-upload --filename abc.png

# 健康检查
python3 scripts/blog-toolkit.py health-check

# 能力清单
python3 scripts/blog-toolkit.py capability-list --format md
```

## Parameter Confirmation / 参数确认

| 子命令 | 参数 | 必填 | 说明 |
|--------|------|------|------|
| list-articles | --page | 否 | 页码，默认 1 |
| list-articles | --size | 否 | 每页数量，默认 10，最大 100 |
| list-articles | --lid | 否 | 标签筛选 ID，默认 0（不筛选） |
| list-articles | --keyword | 否 | 关键词搜索，默认空 |
| create-article | --title | 是 | 文章标题 |
| create-article | --content | 是 | 文章内容 |
| create-article | --uid | 否 | 作者用户 ID，默认 1 |
| create-article | --lid | 否 | 标签 ID，默认 1 |
| create-article | --img | 否 | 封面图片路径 |
| create-article | --heat | 否 | 热度，默认 0 |
| get-article | --article-id | 是 | 文章 ID |
| update-article | --article-id | 是 | 文章 ID |
| update-article | --title/--content/--lid/--img/--heat | 否 | 需更新的字段（至少一个） |
| delete-article | --article-id | 是 | 文章 ID |
| delete-article | --soft | 否 | 软删除，默认 true；传 false 硬删除 |
| restore-article | --article-id | 是 | 文章 ID |
| top-articles | --limit | 否 | 返回数量，默认 5，范围 1-20 |
| create-label | --lname | 是 | 标签名称 |
| create-user | --uname | 是 | 用户名 |
| create-user | --phone/--pwd/--email/--img | 否 | 手机/密码/邮箱/头像，有默认值 |
| list-comments | --aid | 是 | 文章 ID |
| create-comment | --uid | 是 | 用户 ID |
| create-comment | --aid | 是 | 文章 ID |
| create-comment | --content | 是 | 评论内容 |
| delete-comment | --comment-id | 是 | 评论 ID |
| create-message | --uid | 是 | 用户 ID |
| create-message | --content | 是 | 留言内容 |
| reply-message | --uid | 是 | 用户 ID |
| reply-message | --mid | 是 | 留言 ID |
| reply-message | --content | 是 | 回复内容 |
| delete-message | --message-id | 是 | 留言 ID |
| create-mood | --content | 是 | 内容 |
| create-mood | --title/--src | 否 | 标题/图片路径，默认空 |
| delete-mood | --mood-id | 是 | 说说 ID |
| upload-file | --file | 是 | 待上传文件路径 |
| upload-files | --files | 是 | 待上传文件路径列表（至少 1 个） |
| delete-upload | --filename | 是 | 存储文件名（hash，即 upload 返回 data.url 末段或 list-uploads 的 filename） |
| 所有子命令 | --format | 否 | 输出格式 json/md，默认 json |

## Reference Documents / 参考文档

- [API 端点文档](references/api-reference.md)
- [测试用例](templates/test-vars.json)

## 任务结束

完成所有操作后，在最终答复末尾输出 JSON 块，然后结束任务：

```json
{
  "actions": ["做了什么，如 list-articles / create-article / delete-article"],
  "conclusion": "处理结论（成功/失败/部分成功）",
  "artifacts": ["产生的产物：创建的文章 ID / 删除的资源 / 查询结果"],
  "next_step": "下一步建议",
  "issue_summary": "Issue 最新聚合结论（紧凑文本，用 | 分隔）"
}
```

注意：
- 只输出一个 JSON 块，放在答复末尾
- 若无法确定动作或结论，相应字段填空数组/空字符串，不要伪造
