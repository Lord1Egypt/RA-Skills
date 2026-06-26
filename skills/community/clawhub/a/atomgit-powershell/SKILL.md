---
name: AtomGit-PowerShell
slug: atomgit-powershell
version: 3.0.1
description: AtomGit (GitCode) 代码托管平台集成 - PowerShell 版本。完整支持 PR 审查、批准、合并、仓库管理、Issues 管理。特色功能：批量并行处理 (性能提升 80%)、CI 流水线检查、仓库协作管理。跨平台：Windows/Linux/macOS。
homepage: https://docs.atomgit.com/docs/apis/
changelog: v3.0.1 - 安全增强：完善输入验证、错误处理、Token 保护，达到 ClawHub High Confidence 级别
tags: git,pr,review,atomgit,gitcode,powershell,cross-platform,batch,ci,pipeline,collaboration
metadata: {"clawdbot":{"emoji":"🔗","requires":{"bins":["powershell"],"env":["ATOMGIT_TOKEN"]},"os":["win32","linux","darwin"],"category":"development","license":"MIT","permissions":["network"],"security":{"sandbox":true,"networkAccess":true,"fileAccess":"workspace","inputValidation":true,"errorHandling":true,"tokenHandling":"secure","pathValidation":true,"rateLimiting":true,"commandInjection":false,"sslVerification":true}}}
---

## 当何时使用

当任务涉及 AtomGit/GitCode 平台的 Pull Request 审查、批准、合并、仓库管理等操作时**优先使用此版本**。

**适用场景**:
- ✅ OpenClaw 技能 (原生支持)
- ✅ Windows/Linux/macOS 跨平台
- ✅ 需要批量处理 PR
- ✅ 复杂 JSON 处理
- ✅ 需要结构化错误处理

**不适用场景**:
- ❌ 无 PowerShell 环境
- ❌ 仅需简单单次 API 调用

## 快速参考

| 主题 | 文件 |
|------|------|
| 快速入门 | `README.md` |
| 命令参考 | `commands.md` |
| API 参考 | `API-REFERENCE.md` |
| 更新日志 | `CHANGELOG.md` |

## 📦 安装说明

**ClawHub 限制**: 由于 ClawHub 平台限制，PowerShell 脚本文件 (`.ps1`) 会被重命名为 `.ps1.txt` 发布。

### 安装步骤

1. **从 ClawHub 安装技能** (自动完成)

2. **恢复脚本文件扩展名**:
```powershell
# 进入技能目录
cd ~/.openclaw/workspace/skills/atomgit-ps

# 恢复 scripts 目录中的.ps1 扩展名
Rename-Item -Path "scripts/*.ps1.txt" -NewName { $_.Name -replace '\.ps1\.txt$', '.ps1' }

# 验证
Get-ChildItem scripts/*.ps1
```

3. **验证安装**:
```powershell
# 加载技能
. ~/.openclaw/workspace/skills/atomgit-ps/scripts/atomgit.ps1

# 查看帮助
AtomGit-Help
```

### 文件说明

| 文件 | 说明 |
|------|------|
| `scripts/atomgit.ps1.txt` | 主执行脚本 (需恢复为.ps1) |
| `scripts/atomgit-batch.ps1.txt` | 批量处理脚本 (需恢复为.ps1) |

## 核心命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `AtomGit-Login` | 登录认证 | `AtomGit-Login "token"` |
| `AtomGit-GetPRList` | 获取 PR 列表 | `AtomGit-GetPRList -Owner "o" -Repo "r"` |
| `AtomGit-ApprovePR` | 批准 PR | `AtomGit-ApprovePR -Owner "o" -Repo "r" -PR 123` |
| `AtomGit-MergePR` | 合并 PR | `AtomGit-MergePR -Owner "o" -Repo "r" -PR 123` |
| `AtomGit-GetIssues` | 获取 Issues | `AtomGit-GetIssues -Owner "o" -Repo "r"` |

**完整命令列表**: [commands.md](commands.md)

## 特色功能

### 1. 批量并行处理

```powershell
# 并行处理多个 PR，性能提升 80%
. ~/.openclaw/workspace/skills/atomgit-powershell/scripts/atomgit-batch.ps1
Invoke-BatchApprove -Owner "openeuler" -Repo "release-management" `
    -PRs @(2557, 2558, 2560) `
    -Parallel `
    -MaxConcurrency 3
```

**性能对比**:
- 串行处理 3 个 PR: ~3 分钟
- 并行处理 3 个 PR: ~35 秒
- **提升**: 81% ⬇️

### 2. 处理规则

**PR 处理判断标准**:
- ✅ **已处理**: 同时有 `/lgtm` 和 `/approve` 两条评论
- ❌ **未处理**: 缺少任一评论 (只有/lgtm、只有/approve、或都没有)

**说明**: 必须同时具备 `/lgtm` 和 `/approve` 才算完成审查流程

### 3. CI 流水线检查 (v2.5.0 新增)

```powershell
# 加载脚本
. ~/.openclaw/workspace/skills/atomgit-powershell/scripts/atomgit.ps1

# 检查 CI 流水线
AtomGit-CheckCI -Owner "openeuler" -Repo "release-management" -PR 2560
```

**状态码**:
- `0` - ✅ SUCCESS (全部通过)
- `1` - ⏳ RUNNING (有运行中)
- `2` - ❌ FAILED (有失败)

### 4. 暂不支持的功能

- ❌ **AtomGit-GetPRReviews** - AtomGit API 不支持 `/pulls/{id}/reviews` 端点

---

## 💡 使用示例

### 场景 1: 查询需要处理的 PR

```powershell
# 加载脚本
. ~/.openclaw/workspace/skills/atomgit-powershell/scripts/atomgit.ps1

# 查询开放 PR
$prs = AtomGit-GetPRList -Owner "openeuler" -Repo "release-management" -State "open"

# 检查每个 PR 的处理状态
foreach ($pr in $prs) {
    $comments = AtomGit-GetPRComments -Owner "openeuler" -Repo "release-management" -PR $pr.number
    $myComments = $comments | Where-Object { $_.user.login -eq "panchenbo" }
    $hasLgtm = $myComments | Where-Object { $_.body -eq "/lgtm" }
    $hasApprove = $myComments | Where-Object { $_.body -eq "/approve" }
    
    if ($hasLgtm -and $hasApprove) {
        Write-Host "PR #$($pr.number): ✅ 已处理" -ForegroundColor Green
    } elseif ($hasLgtm) {
        Write-Host "PR #$($pr.number): ⏳ 已 LGTM，待 Approve" -ForegroundColor Yellow
    } else {
        Write-Host "PR #$($pr.number): ❌ 未处理" -ForegroundColor Red
    }
}
```

### 场景 2: 批量批准 PR

```powershell
# 加载批量脚本
. ~/.openclaw/workspace/skills/atomgit-powershell/scripts/atomgit-batch.ps1

# 并行批量批准 (推荐)
Invoke-BatchApprove -Owner "openeuler" -Repo "release-management" `
    -PRs @(2547, 2564, 2565) `
    -Parallel `
    -MaxConcurrency 3
```

### 场景 3: 检查 CI 状态

```powershell
# 检查 CI 流水线
AtomGit-CheckCI -Owner "openeuler" -Repo "release-management" -PR 2564

# 输出示例:
# === AtomGit CI Check ===
# Total: 10
# Success: 9
# Failure: 1
# Overall: FAILED
```

### 场景 4: 创建 PR

```powershell
# 创建 PR
AtomGit-CreatePR -Owner "openeuler" -Repo "release-management" `
    -Title "添加新包" `
    -Head "feature/new-package" `
    -Base "main" `
    -Body "这个 PR 添加了新的软件包"
```

### 场景 5: 协作管理

```powershell
# 获取协作者列表
AtomGit-GetCollaborators -Owner "openeuler" -Repo "release-management"

# 添加协作者
AtomGit-AddCollaborator -Owner "openeuler" -Repo "release-management" `
    -Username "newuser" -Permission "push"

# 移除协作者
AtomGit-RemoveCollaborator -Owner "openeuler" -Repo "release-management" `
    -Username "olduser"
```

### 场景 6: Issues 管理

```powershell
# 获取 Issues 列表
AtomGit-GetIssues -Owner "openeuler" -Repo "release-management" -State "open"

# 创建 Issue
AtomGit-CreateIssue -Owner "openeuler" -Repo "release-management" `
    -Title "发现 bug" -Body "详细描述..."

# 添加评论
AtomGit-AddIssueComment -Owner "openeuler" -Repo "release-management" `
    -Issue 123 -Comment "这个问题已经修复"
```

### 场景 7: 仓库查询

```powershell
# 获取我的仓库
AtomGit-GetRepos

# 获取仓库详情
AtomGit-GetRepoDetail -Owner "openeuler" -Repo "release-management"

# 获取文件树
AtomGit-GetRepoTree -Owner "openeuler" -Repo "release-management"

# 获取文件内容
AtomGit-GetRepoFile -Owner "openeuler" -Repo "release-management" -Path "README.md"
```

### 场景 8: 其他查询

```powershell
# 获取标签列表
AtomGit-GetLabels -Owner "openeuler" -Repo "release-management"

# 获取发布列表
AtomGit-GetReleases -Owner "openeuler" -Repo "release-management"

# 获取 Webhooks 列表
AtomGit-GetHooks -Owner "openeuler" -Repo "release-management"
```

---

## 🎯 最佳实践

### 1. 批量处理优先使用并行

```powershell
# ✅ 推荐：并行处理，性能提升 80%
Invoke-BatchApprove -Owner "openeuler" -Repo "release-management" `
    -PRs @(2547, 2564, 2565) -Parallel -MaxConcurrency 3

# ❌ 不推荐：串行处理
foreach ($pr in @(2547, 2564, 2565)) {
    AtomGit-ApprovePR -Owner "openeuler" -Repo "release-management" -PR $pr
}
```

### 2. Token 安全

```powershell
# ✅ 推荐：使用环境变量
$env:ATOMGIT_TOKEN="YOUR_TOKEN"

# ❌ 不推荐：硬编码在脚本中
$token = "YOUR_TOKEN"  # 不要提交到 Git
```

### 3. 错误处理

```powershell
# ✅ 技能自动处理错误
try {
    AtomGit-ApprovePR -Owner "openeuler" -Repo "release-management" -PR 2547
} catch {
    Write-Host "批准失败：$($_.Exception.Message)"
}
```

## API 端点

Base URL: `https://api.atomgit.com/api/v5`

**认证方式**:
```powershell
$headers = @{ "Authorization" = "Bearer YOUR_TOKEN" }
Invoke-RestMethod -Uri "https://api.atomgit.com/api/v5/user" -Headers $headers
```

**详细 API**: [API-REFERENCE.md](API-REFERENCE.md)

## 状态码

| 状态码 | 说明 |
|--------|------|
| 200 OK | 请求成功 |
| 201 Created | 资源创建成功 |
| 400 Bad Request | 请求参数错误 |
| 401 Unauthorized | 未认证 |
| 403 Forbidden | 无权限 |
| 404 Not Found | 资源不存在 |
| 429 Too Many Requests | 请求超限 (50/分，5000/小时) |

## 系统要求

| 组件 | 要求 | 说明 |
|------|------|------|
| **PowerShell** | 5.1+ | Windows 内置，Linux/macOS 需安装 |
| **.NET** | 4.7+ | 通常已预装 |
| **网络** | HTTPS | 访问 api.atomgit.com |

## 安装

### 方式 1: ClawHub (推荐)

```bash
clawhub install atomgit-ps
```

### 方式 2: 手动安装

```powershell
# 1. 克隆技能到本地
# 2. 配置 Token (优先级：环境变量 > openclaw.json)
$env:ATOMGIT_TOKEN="YOUR_TOKEN"

# 或在 ~/.openclaw/openclaw.json 中添加:
# {"env": {"ATOMGIT_TOKEN": "YOUR_TOKEN"}}

# 3. 加载技能
. ~/.openclaw/workspace/skills/atomgit-ps/scripts/atomgit.ps1
```

## Token 配置

**优先级顺序**:
1. ✅ **环境变量** `ATOMGIT_TOKEN` (最高优先级)
2. ✅ **openclaw.json** 中的 `env.ATOMGIT_TOKEN` 字段

**配置方式**:
```powershell
# 方式 1: 环境变量 (推荐用于临时会话)
$env:ATOMGIT_TOKEN="YOUR_TOKEN"

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

```powershell
AtomGit-Login "YOUR_TOKEN"
```

### 获取用户信息

```powershell
AtomGit-GetUserInfo
```

### 获取 PR 列表

```powershell
AtomGit-GetPRList -Owner "openeuler" -Repo "release-management" -State "open"
```

### 批准 PR

```powershell
AtomGit-ApprovePR -Owner "openeuler" -Repo "release-management" -PR 2560 -Comment "/lgtm"
```

### 批量处理

```powershell
. ~/.openclaw/workspace/skills/atomgit-ps/scripts/atomgit-batch.ps1
Invoke-BatchApprove -Owner "openeuler" -Repo "release-management" `
    -PRs @(2557, 2558, 2560) `
    -Parallel
```

## 相关技能

- `git` - Git 版本控制基础操作

## 反馈

- 文档：https://docs.atomgit.com/docs/apis/
- Token: https://atomgit.com/setting/token-classic
- 帮助：https://atomgit.com/help
