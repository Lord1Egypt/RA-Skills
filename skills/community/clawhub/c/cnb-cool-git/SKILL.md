---
AIGC:
    ContentProducer: Minimax Agent AI
    ContentPropagator: Minimax Agent AI
    Label: AIGC
    ProduceID: 5282d543add8072b9878699edc211fb0
    PropagateID: 5282d543add8072b9878699edc211fb0
    ReservedCode1: 3046022100f08c7a6975ef7a4387563429a8120e4ab79cb5ad7d41c4267cc637681acc899f022100ca2aaa4853dc830a1607b57a86755f6eb81398beb2b2f17d2bbdd0e692875d55
    ReservedCode2: 3045022057c25d43ffd6f94e2c7c68fba886004d0c3e8828a823f9eff52bd9ce9b34dc56022100ebeaaf1311141b4d00bf392ec576d5c080e1ab1ae439a9301279ba094f7df3f0
description: CNB 云原生构建平台的 Git 操作技能。使用 git 和 CNB Open API 进行代码克隆、提交、推送、分支管理、Merge Request 管理、流水线触发、流水线结果读取等操作。首次使用需收集用户的 Git 用户名和邮箱信息。
name: cnb-cool-git
---

# CNB Git Skill

在 CNB（cnb.cool）平台上进行 Git 操作和 API 调用。

## 认证配置

**Token（敏感）— 通过 Gateway secrets 注入**（不暴露在日志和配置展示中）：

| 变量名 | 说明 |
|--------|------|
| `CNB_COOL_GIT_TOKEN` | Git 访问令牌，用于 clone/push |
| `CNB_COOL_API_TOKEN` | API 令牌，用于调用 CNB Open API |

> ⚠️ **Token 类型注意**：必须使用**经典令牌（Classic Token）**或 REST API 令牌，MCP 读写权限 Token 对 REST API 无效（所有 `/-/` 路径返回 404）。

注入方式：在 OpenClaw `openclaw.json` 的 `env.vars` 中配置，密钥部分会被脱敏显示。

**用户名/邮箱（非敏感）— 写入 `.env` 文件**（放在 `/workspace/.env`）：

```
CNB_COOL_GIT_USER_NAME=你的Git用户名
CNB_COOL_GIT_USER_EMAIL=你的Git邮箱
```

同时设置 Git 全局配置：

```bash
git config --global user.name "${CNB_COOL_GIT_USER_NAME}"
git config --global user.email "${CNB_COOL_GIT_USER_EMAIL}"
```

**克隆仓库**：

```bash
git clone https://cnb:${CNB_COOL_GIT_TOKEN}@cnb.cool/your-group/your-repo.git
```

## API 基础调用

API 服务地址：`https://api.cnb.cool`

> ⚠️ **Token 类型注意**：CNB 的 MCP Token（MCP 读写权限）**不支持 REST API**，所有接口均返回 404。必须使用**经典令牌（Classic Token）**或具有 REST API 权限的 Personal Access Token。

```bash
# 所有 API 调用都需携带以下两个 Header
curl -H "Authorization: ${CNB_COOL_API_TOKEN}" \
     -H "Accept: application/vnd.cnb.api+json" \
     "https://api.cnb.cool/..."
```

## Merge Request（MR）操作

**创建 MR**：

```bash
curl -X "POST" \
  -H "Authorization: ${CNB_COOL_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.cnb.api+json" \
  -d '{
    "title": "feat: 功能描述",
    "head": "feature/branch-name",
    "base": "main",
    "body": "变更内容..."
  }' \
  "https://api.cnb.cool/{owner}/{repo}/-/pulls"
```

> 字段说明：`head` = 源分支，`base` = 目标分支（⚠️ 不是 `source_branch/target_branch`）

**列出 MR**：

```bash
# 查看所有 MR
curl "https://api.cnb.cool/{owner}/{repo}/-/pulls" \
  -H "Authorization: ${CNB_COOL_API_TOKEN}" \
  -H "Accept: application/vnd.cnb.api+json"

# 查看指定 MR
curl "https://api.cnb.cool/{owner}/{repo}/-/pulls/{number}" \
  -H "Authorization: ${CNB_COOL_API_TOKEN}" \
  -H "Accept: application/vnd.cnb.api+json"
```

**添加评论**：

```bash
curl -X "POST" \
  -H "Authorization: ${CNB_COOL_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.cnb.api+json" \
  -d '{"body": "评论内容"}' \
  "https://api.cnb.cool/{owner}/{repo}/-/pulls/{number}/comments"
```

**提交评审**：

```bash
# APPROVE - 批准
curl -X "POST" \
  -H "Authorization: ${CNB_COOL_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.cnb.api+json" \
  -d '{"event": "APPROVE", "body": "LGTM"}' \
  "https://api.cnb.cool/{owner}/{repo}/-/pulls/{number}/reviews"

# REQUEST_CHANGES - 需要改进
curl -X "POST" \
  -H "Authorization: ${CNB_COOL_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.cnb.api+json" \
  -d '{"event": "REQUEST_CHANGES", "body": "请修复..."}' \
  "https://api.cnb.cool/{owner}/{repo}/-/pulls/{number}/reviews"
```

**合并 MR**：

```bash
curl -X "PUT" \
  -H "Authorization: ${CNB_COOL_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.cnb.api+json" \
  -d '{
    "merge_method": "merge"
  }' \
  "https://api.cnb.cool/{owner}/{repo}/-/pulls/{number}/merge"
```

**管理标签和评审人**：

```bash
# 添加标签
curl -X "POST" \
  -H "Authorization: ${CNB_COOL_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.cnb.api+json" \
  -d '{"labels": ["bug", "high-priority"]}' \
  "https://api.cnb.cool/{owner}/{repo}/-/pulls/{number}/labels"

# 添加评审人
curl -X "POST" \
  -H "Authorization: ${CNB_COOL_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.cnb.api+json" \
  -d '{"reviewers": ["username1", "username2"]}' \
  "https://api.cnb.cool/{owner}/{repo}/-/pulls/{number}/reviewers"
```

## Pipeline 构建结果

**获取构建历史**：

```bash
curl "https://api.cnb.cool/{owner}/{repo}/-/builds?page=1&page_size=20" \
  -H "Authorization: ${CNB_COOL_API_TOKEN}" \
  -H "Accept: application/vnd.cnb.api+json"
```

**获取构建详情和日志**：

```bash
# 构建详情
curl "https://api.cnb.cool/{owner}/{repo}/-/builds/{build_id}" \
  -H "Authorization: ${CNB_COOL_API_TOKEN}" \
  -H "Accept: application/vnd.cnb.api+json"

# 构建日志
curl "https://api.cnb.cool/{owner}/{repo}/-/builds/{build_id}/logs" \
  -H "Authorization: ${CNB_COOL_API_TOKEN}" \
  -H "Accept: application/vnd.cnb.api+json"
```

## Pipeline 触发

**手动触发 Pipeline**：

```bash
# 通过 API 触发流水线
curl -X "POST" \
  -H "Authorization: ${CNB_COOL_API_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "Accept: application/vnd.cnb.api+json" \
  -d '{
    "branch": "main",
    "event": "api_trigger",
    "env": {
      "KEY": "value"
    }
  }' \
  "https://api.cnb.cool/{owner}/{repo}/-/trigger"
```

**获取触发器列表**：

```bash
curl "https://api.cnb.cool/{owner}/{repo}/-/triggers" \
  -H "Authorization: ${CNB_COOL_API_TOKEN}" \
  -H "Accept: application/vnd.cnb.api+json"
```

**重新触发构建**：

```bash
curl -X "POST" \
  -H "Authorization: ${CNB_COOL_API_TOKEN}" \
  -H "Accept: application/vnd.cnb.api+json" \
  "https://api.cnb.cool/{owner}/{repo}/-/builds/{build_id}/retry"
```

## 关键环境变量

| 变量名 | 说明 |
|--------|------|
| CNB_REPO_SLUG | 仓库路径（group/repo） |
| CNB_BRANCH | 分支名 |
| CNB_COMMIT | 提交 SHA |
| CNB_BUILD_ID | 构建流水号 |
| CNB_BUILD_STATUS | 构建状态（success/error/cancel） |
| CNB_PIPELINE_STATUS | Pipeline 状态 |
| CNB_BUILD_WEB_URL | 构建日志地址 |
| CNB_PULL_REQUEST | 是否为 PR 触发 |
| CNB_TOKEN | 流水线临时令牌（系统注入） |

## 最佳实践

- 不要在代码中硬编码访问令牌
- 使用环境变量或密钥仓库存储敏感信息
- 定期轮换令牌
- 不可信事件（PR评论、Issue评论）的流水线权限受限，敏感操作应在可信事件中执行
