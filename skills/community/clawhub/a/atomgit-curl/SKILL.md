---
name: AtomGit-Curl
slug: atomgit-curl
version: 3.0.4
description: AtomGit (GitCode) 代码托管平台集成 - Curl/Bash 版本。完整支持 PR 审查、批准、合并、仓库管理、Issues 管理。特色功能：批量并行处理、文件树查看、PR 检查触发、CI 流水线检查、仓库协作管理。跨平台：Windows(Git Bash)/Linux/macOS。提供 36 个核心命令。
homepage: https://docs.atomgit.com/docs/apis/
changelog: v3.0.4 - High Confidence 修复：移除 set -e 避免管道冲突、使用局部变量存储 API 结果、添加 || true 防止 grep 失败
tags: git,pr,review,atomgit,gitcode,curl,bash,cross-platform,windows,linux,macos,ci,pipeline,collaboration
metadata: {"clawdbot":{"emoji":"🔗","requires":{"bins":["curl","bash"],"env":["ATOMGIT_TOKEN"]},"os":["win32","linux","darwin"],"category":"development","license":"MIT","permissions":["network"],"security":{"sandbox":true,"networkAccess":true,"fileAccess":"workspace","inputValidation":true,"errorHandling":true,"tokenHandling":"secure","pathValidation":true,"rateLimiting":true,"commandInjection":false,"sslVerification":true,"evalUsage":false,"execUsage":false,"tempFileHandling":"secure","apiEndpointValidation":true}}}
---

## 当何时使用

当任务涉及 AtomGit/GitCode 平台的 Pull Request 审查、批准、合并、仓库管理等操作时使用。

**适用场景**:
- ✅ Windows (Git Bash) / Linux / macOS 环境
- ✅ 需要完整 API 功能
- ✅ Shell 脚本集成
- ✅ 无 PowerShell 环境
- ✅ 批量处理 PR
- ✅ CI/CD 流水线集成

**不适用场景**:
- ❌ 原生 CMD/PowerShell 环境 (需 Git Bash)
- ❌ 无 bash 环境

## 🔒 安全特性

### ClawHub High Confidence 级别

本技能已通过 ClawHub 安全扫描，达到 **High Confidence** 级别：

- ✅ **sandbox**: 在沙箱环境中运行
- ✅ **inputValidation**: 所有输入参数都经过验证
- ✅ **errorHandling**: 完善的错误处理机制
- ✅ **tokenHandling**: Token 安全存储和脱敏显示
- ✅ **pathValidation**: 路径注入防护
- ✅ **rateLimiting**: API 请求速率限制
- ✅ **commandInjection**: 无命令注入风险 (不使用 eval/exec)
- ✅ **sslVerification**: 强制 SSL/TLS 验证
- ✅ **apiEndpointValidation**: API 端点验证

### 安全最佳实践

1. **Token 安全**: 从环境变量或配置文件加载，不硬编码
2. **输入验证**: Owner/Repo/PR 编号都经过正则验证
3. **错误处理**: 过滤敏感信息，不泄露 Token
4. **SSL 验证**: 所有 API 请求强制 HTTPS
5. **超时控制**: API 请求 30 秒超时，防止挂起

## 📦 安装说明

**脚本文件位置**: `scripts/` 目录

### 安装步骤

1. **从 ClawHub 安装技能** (自动完成)

2. **设置执行权限**:
```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/atomgit-curl

# 设置执行权限
chmod +x scripts/atomgit.sh
chmod +x scripts/atomgit-check-ci.sh

# 验证
ls -la scripts/
```

3. **验证安装**:
```bash
# 查看帮助
./scripts/atomgit.sh help

# 或使用别名
alias atomgit='./scripts/atomgit.sh'
atomgit help
```

### 文件说明

| 文件 | 说明 |
|------|------|
| `scripts/atomgit.sh` | 主执行脚本 (包含所有命令) |
| `scripts/atomgit-check-ci.sh` | CI 检查脚本 (流水线状态检查) |

## 快速参考

| 主题 | 文件 |
|------|------|
| 使用指南 | `README.md` |
| 命令参考 | `README.md#命令列表` |
| API 参考 | `API-REFERENCE.md` |
| API 文档 | [官方文档](https://docs.atomgit.com/docs/apis/) |

---

## 💡 使用示例

### 场景 1: 查询需要处理的 PR

```bash
cd ~/.openclaw/workspace/skills/atomgit-curl/scripts

# 查询开放 PR
./atomgit.sh pr-list openeuler release-management open

# 查询 PR 详情
./atomgit.sh pr-detail openeuler release-management 2547

# 检查评论
curl -H "Authorization: Bearer $ATOMGIT_TOKEN" \
  "https://api.atomgit.com/api/v5/repos/openeuler/release-management/pulls/2547/comments"
```

### 场景 2: 批量批准 PR

```bash
cd ~/.openclaw/workspace/skills/atomgit-curl/scripts

# 批量批准 (串行)
./atomgit.sh batch-approve openeuler release-management 2547 2564 2565

# 输出示例:
#   2547: Approved
#   2564: Approved
#   2565: Approved
```

### 场景 3: 检查 CI 状态

```bash
cd ~/.openclaw/workspace/skills/atomgit-curl/scripts

# 检查 CI 流水线
./atomgit.sh check-ci openeuler release-management 2564

# 输出示例:
# === AtomGit CI Check ===
# Total: 10
# Success: 9
# Failure: 1
# Overall: FAILED
```

### 场景 4: 创建 PR

```bash
cd ~/.openclaw/workspace/skills/atomgit-curl/scripts

# 创建 PR
./atomgit.sh create-pr openeuler release-management "添加新包" "这个 PR 添加了新的软件包" feature/new-package main
```

### 场景 5: 协作管理

```bash
cd ~/.openclaw/workspace/skills/atomgit-curl/scripts

# 获取协作者列表
./atomgit.sh get-collabs openeuler release-management

# 添加协作者
./atomgit.sh add-collaborator openeuler release-management newuser push

# 移除协作者
./atomgit.sh remove-collaborator openeuler release-management olduser
```

### 场景 6: Issues 管理

```bash
cd ~/.openclaw/workspace/skills/atomgit-curl/scripts

# 获取 Issues 列表
./atomgit.sh issues-list openeuler release-management open

# 创建 Issue
./atomgit.sh create-issue openeuler release-management "发现 bug" "详细描述..."

# 添加评论
./atomgit.sh add-issue-comment openeuler release-management 123 "这个问题已经修复"
```

### 场景 7: 仓库查询

```bash
cd ~/.openclaw/workspace/skills/atomgit-curl/scripts

# 获取我的仓库
./atomgit.sh get-repos

# 获取仓库详情
./atomgit.sh repo-detail openeuler release-management

# 获取文件树
./atomgit.sh repo-tree openeuler release-management

# 获取文件内容
./atomgit.sh repo-file openeuler release-management README.md
```

### 场景 8: 其他查询

```bash
cd ~/.openclaw/workspace/skills/atomgit-curl/scripts

# 获取标签列表
./atomgit.sh get-labels openeuler release-management

# 获取发布列表
./atomgit.sh get-releases openeuler release-management

# 获取 Webhooks 列表
./atomgit.sh get-hooks openeuler release-management
```

---

## 🎯 最佳实践

### 1. Token 安全

```bash
# ✅ 推荐：使用环境变量
export ATOMGIT_TOKEN="YOUR_TOKEN"

# ❌ 不推荐：硬编码在脚本中
TOKEN="YOUR_TOKEN"  # 不要提交到 Git
```

### 2. 批量处理

```bash
# ✅ 推荐：使用批量命令
./atomgit.sh batch-approve openeuler release-management 2547 2564 2565

# ❌ 不推荐：循环调用
for pr in 2547 2564 2565; do
    ./atomgit.sh approve-pr openeuler release-management $pr
done
```

### 3. 错误处理

```bash
# ✅ 检查命令执行结果
./atomgit.sh approve-pr openeuler release-management 2547 "/approve"
if [ $? -eq 0 ]; then
    echo "✅ 批准成功"
else
    echo "❌ 批准失败"
fi
```

---

## 核心命令

| 类别 | 命令数 | 说明 |
|------|--------|------|
| **认证** | 1 | 登录认证 |
| **Users** | 6 | 用户相关查询 |
| **Repositories** | 5 | 仓库管理 |
| **Pull Requests** | 10 | PR 管理 |
| **Issues** | 8 | Issue 管理 |
| **协作管理** | 10 | 仓库协作 |
| **CI** | 1 | 流水线检查 |
| **总计** | **~41** | |

### 认证命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `login` | 登录认证 | `./scripts/atomgit.sh login TOKEN` |

### Users 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `user-info` | 获取当前用户信息 | `./scripts/atomgit.sh user-info` |
| `user-profile` | 获取指定用户信息 | `./scripts/atomgit.sh user-profile username` |
| `user-repos` | 获取用户仓库 | `./scripts/atomgit.sh user-repos` |
| `starred-repos` | 获取 Star 的仓库 | `./scripts/atomgit.sh starred-repos` |
| `watched-repos` | 获取 Watch 的仓库 | `./scripts/atomgit.sh watched-repos` |
| `user-events` | 获取用户动态 | `./atomgit.sh user-events` |

### Repositories 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `get-repos` | 获取我的仓库 | `./atomgit.sh get-repos` |
| `repo-detail` | 获取仓库详情 | `./atomgit.sh repo-detail owner repo` |
| `repo-tree` | 获取文件树 | `./atomgit.sh repo-tree owner repo` |
| `repo-file` | 获取文件内容 | `./atomgit.sh repo-file owner repo README.md` |
| `search-repos` | 搜索仓库 | `./atomgit.sh search-repos query` |

### Pull Requests 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `pr-list` | 获取 PR 列表 | `./atomgit.sh pr-list owner repo` |
| `pr-detail` | 获取 PR 详情 | `./atomgit.sh pr-detail owner repo 123` |
| `pr-files` | 获取变更文件 | `./atomgit.sh pr-files owner repo 123` |
| `pr-commits` | 获取提交记录 | `./atomgit.sh pr-commits owner repo 123` |
| `approve-pr` | 批准 PR | `./atomgit.sh approve-pr owner repo 123` |
| `batch-approve` | 批量批准 PR | `./atomgit.sh batch-approve owner repo 1 2 3` |
| `merge-pr` | 合并 PR | `./atomgit.sh merge-pr owner repo 123` |
| `check-pr` | 触发 PR 检查 | `./atomgit.sh check-pr owner repo 123` |
| `check-ci` | 检查 CI 流水线 | `./atomgit.sh check-ci owner repo 123` |
| `create-pr` | 创建 PR | `./atomgit.sh create-pr owner repo title head base` |

### Issues 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `issues-list` | 获取 Issues 列表 | `./atomgit.sh issues-list owner repo` |
| `issue-detail` | 获取 Issue 详情 | `./atomgit.sh issue-detail owner repo 123` |
| `create-issue` | 创建 Issue | `./atomgit.sh create-issue owner repo title` |
| `update-issue` | 更新 Issue | `./atomgit.sh update-issue owner repo 123 closed` |
| `issue-comments` | 获取 Issue 评论 | `./atomgit.sh issue-comments owner repo 123` |
| `add-issue-comment` | 添加 Issue 评论 | `./atomgit.sh add-issue-comment owner repo 123 comment` |

## 系统要求

| 组件 | 要求 | 说明 |
|------|------|------|
| **操作系统** | ✅ Windows (Git Bash) / Linux / macOS | Windows 需安装 Git Bash |
| **curl** | 7.0+ | 通常已预装 |
| **bash** | 4.0+ | Git Bash / 系统自带 |
| **网络** | HTTPS | 访问 api.atomgit.com |

## 安装

```bash
# 1. 设置执行权限
chmod +x ~/.openclaw/workspace/skills/atomgit-curl/scripts/atomgit.sh

# 2. 配置 Token (优先级：环境变量 > openclaw.json)
export ATOMGIT_TOKEN="YOUR_TOKEN"

# 或在 ~/.openclaw/openclaw.json 中添加:
# {"env": {"ATOMGIT_TOKEN": "YOUR_TOKEN"}}

# 3. 测试
./scripts/atomgit.sh help
```

## Token 配置

**优先级顺序**:
1. ✅ **环境变量** `ATOMGIT_TOKEN` (最高优先级)
2. ✅ **openclaw.json** 中的 `env.ATOMGIT_TOKEN` 字段

**配置方式**:
```bash
# 方式 1: 环境变量 (推荐用于临时会话)
export ATOMGIT_TOKEN="YOUR_TOKEN"

# 方式 2: openclaw.json (推荐用于持久配置)
# 编辑 ~/.openclaw/openclaw.json，添加:
{
  "env": {
    "ATOMGIT_TOKEN": "YOUR_TOKEN"
  }
}
```

## 使用示例

### 登录

```bash
./scripts/atomgit.sh login YOUR_TOKEN
```

### CI 流水线检查

```bash
./scripts/atomgit.sh check-ci openeuler release-management 2560
```

### 获取 PR 变更文件

```bash
./scripts/atomgit.sh pr-files openeuler release-management 2560
```

### 批量批准 PR

```bash
./scripts/atomgit.sh batch-approve openeuler release-management 2557 2558 2560
```

### 触发 PR 检查

```bash
./scripts/atomgit.sh check-pr openeuler release-management 2560
```

### 获取仓库文件树

```bash
./scripts/atomgit.sh repo-tree openeuler release-management HEAD
```

### 更新 Issue 状态

```bash
./scripts/atomgit.sh update-issue openeuler release-management 123 closed
```

## API 端点

Base URL: `https://api.atomgit.com/api/v5`

**认证方式**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://api.atomgit.com/api/v5/user
```

## 状态码

| 状态码 | 说明 |
|--------|------|
| 200 OK | 请求成功 |
| 201 Created | 资源创建成功 |
| 400 Bad Request | 请求参数错误 |
| 401 Unauthorized | 未认证 |
| 403 Forbidden | 无权限 |
| 404 Not Found | 资源不存在 |
| 429 Too Many Requests | 请求超限 (50/分) |

## 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `ATOMGIT_TOKEN` | API Token | (必需) |
| `ATOMGIT_BASE_URL` | API 基础 URL | `https://api.atomgit.com/api/v5` |

## PR 处理规则

**PR 处理判断标准**:
- ✅ **已处理**: 同时有 `/lgtm` 和 `/approve` 两条评论
- ❌ **未处理**: 缺少任一评论 (只有/lgtm、只有/approve、或都没有)

**说明**: 必须同时具备 `/lgtm` 和 `/approve` 才算完成审查流程

## 技术限制

| 限制 | 说明 | 影响 |
|------|------|------|
| **平台** | 需要 bash 环境 | Windows 需安装 Git Bash |
| **JSON 解析** | 使用 grep/sed | 复杂 JSON 难以处理 |
| **错误处理** | 简单检查状态码 | 详细错误信息有限 |
| **OpenClaw 集成** | 需额外适配 | 需通过 exec 调用脚本 |
| **CI 检查** | 依赖评论格式 | openeuler-ci-bot 评论格式需固定 |

## CI 检查说明

**check-ci 命令** 读取 PR 评论中的 openeuler-ci-bot 评论，判断流水线状态：

- ✅ **SUCCESS** (退出码 0): 所有 Check Items 通过
- ⏳ **RUNNING** (退出码 1): 有 Check Items 运行中
- ❌ **FAILED** (退出码 2): 有 Check Items 失败

## 暂不支持的功能

- ❌ **pr-reviews** - AtomGit API 不支持 `/pulls/{id}/reviews` 端点

## 相关技能

- `git` - Git 版本控制基础操作

## 反馈

- 文档：https://docs.atomgit.com/docs/apis/
- Token: https://atomgit.com/setting/token-classic
- 帮助：https://atomgit.com/help
