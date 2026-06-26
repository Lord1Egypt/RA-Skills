---
name: clawhub-search
description: |
  搜索 ClawHub Skills 技能市场。使用此技能查找和发现 OpenClaw 社区贡献的各种技能。
  激活条件：用户提到搜索技能、查找 skill、找某个功能的 skill、ClawHub、clawhub。
---

# ClawHub Skill 搜索工具

## 概述

此技能用于在 ClawHub 技能市场上搜索 OpenClaw Skills。通过调用 ClawHub API 获取技能列表，支持按关键词搜索和下载量排序。

## API 信息

- **API 地址**: `https://clawhub.ai/api/v1/skills`
- **认证方式**: Bearer Token
- **参数**:
  - `q`: 搜索关键词
  - `sort`: 排序方式 (downloads, stars, newest)
  - `limit`: 返回数量 (可选)

## 使用方法

## API Token

使用环境变量 `CLAWHUB_TOKEN` 存储 API Token。

获取方式：在 ClawHub 官网申请 API Token。

**重要：不要将 Token 明文写入代码或文档中！**

### 1. 获取 API Token

需要用户的 ClawHub API Token。可以在 ClawHub 官网申请。

### 2. 搜索 Skills

使用 curl 命令搜索：

```bash
# 基础搜索（按下载量排序）
curl -s "https://clawhub.ai/api/v1/skills?sort=downloads&q=关键词" \
  -H "Authorization: Bearer $CLAWHUB_TOKEN"

# 精确搜索
curl -s "https://clawhub.ai/api/v1/skills?q=agent+team" \
  -H "Authorization: Bearer $CLAWHUB_TOKEN"

# 搜索并格式化输出
curl -s "https://clawhub.ai/api/v1/skills?sort=downloads&q=关键词" \
  -H "Authorization: Bearer $CLAWHUB_TOKEN" | python3 -c "
import sys,json
d=json.load(sys.stdin)
for i in d.get('items',[])[:10]:
    print(f\"{i['slug']}: {i['summary'][:60]}... ({i['stats']['downloads']} downloads)\")
"
```

### 3. 安装 Skills

找到想用的 skill 后，使用以下命令安装：

```bash
# 通过 ClawHub 安装
npx clawhub@latest install <skill-slug>

# 或手动安装（下载并解压到 skills 目录）
```

## 常用搜索示例

| 搜索需求 | 命令 |
|----------|------|
| 代码开发相关 | `?q=code+developer&sort=downloads` |
| 多 Agent 相关 | `?q=agent&sort=downloads` |
| 记忆/内存相关 | `?q=memory&sort=downloads` |
| 自动化相关 | `?q=automation&sort=downloads` |
| 搜索/查找相关 | `?q=search&sort=downloads` |
| 团队协作相关 | `?q=team+delegation&sort=downloads` |

## 示例：搜索 "agent" 相关的 Skills

```bash
curl -s "https://clawhub.ai/api/v1/skills?sort=downloads&q=agent" \
  -H "Authorization: Bearer YOUR_TOKEN" | python3 -c "
import sys,json
d=json.load(sys.stdin)
items = d.get('items', [])
print(f'找到 {len(items)} 个结果:\n')
for i in items[:15]:
    stats = i.get('stats', {})
    print(f\"- {i['slug']}\")
    print(f\"  描述: {i.get('summary', '')[:80]}\")
    print(f\"  下载: {stats.get('downloads', 0)} | 星标: {stats.get('stars', 0)}\")
    print()
"
```

## 输出格式解析

API 返回的 JSON 包含以下字段：

| 字段 | 说明 |
|------|------|
| `slug` | Skill 的唯一标识符 |
| `displayName` | 显示名称 |
| `summary` | 简短描述 |
| `stats.downloads` | 下载次数 |
| `stats.stars` | 星标数量 |
| `createdAt` | 创建时间 (Unix时间戳) |
| `updatedAt` | 更新时间 (Unix时间戳) |

## 注意事项

1. **Token 管理**: API Token 需要妥善保管，不要泄露
2. **速率限制**: 注意 API 调用频率限制
3. **动态页面**: ClawHub 前端页面是动态加载的，无法通过普通网页抓取获取内容，必须使用 API
4. **搜索策略**: 如果搜索结果少于 5 个，尝试用更通用的关键词

## 常用技巧

1. **组合搜索**: 使用多个关键词组合，如 `agent+memory`、`code+automation`
2. **过滤筛选**: 可以先搜索再根据描述人工筛选
3. **关注下载量**: 高下载量通常意味着更稳定、更受欢迎的技能

## 相关链接

- ClawHub 官网: https://clawhub.ai/
- 技能市场: https://clawhub.ai/skills
- 发布技能: https://clawhub.ai/upload
