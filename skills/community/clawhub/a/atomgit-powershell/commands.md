# AtomGit-PowerShell 命令参考

> **版本**: v3.0.0  
> **最后更新**: 2026-03-26

---

## 🚀 快速启动

```powershell
# 加载脚本
. ~/.openclaw/workspace/skills/atomgit-powershell/scripts/atomgit.ps1

# 登录
AtomGit-Login "YOUR_TOKEN"

# 查看帮助
AtomGit-Help
```

---

## 📋 命令总览

| 类别 | 命令数 | 说明 |
|------|--------|------|
| **认证** | 1 | 登录认证 |
| **Users** | 6 | 用户相关查询 |
| **Repositories** | 5 | 仓库管理 |
| **Pull Requests** | 8 | PR 管理 |
| **Issues** | 6 | Issue 管理 |
| **工具** | 1 | 帮助信息 |
| **总计** | **26** | |

---

## 🔐 认证命令

### AtomGit-Login

**登录到 AtomGit**

```powershell
AtomGit-Login "YOUR_TOKEN"
```

---

## 👤 Users 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `AtomGit-GetUserInfo` | 获取当前用户信息 | `AtomGit-GetUserInfo` |
| `AtomGit-GetUserProfile` | 获取指定用户信息 | `AtomGit-GetUserProfile -Username "user"` |
| `AtomGit-GetUserRepos` | 获取用户仓库 | `AtomGit-GetUserRepos -Username "user"` |
| `AtomGit-GetStarredRepos` | 获取 Star 的仓库 | `AtomGit-GetStarredRepos` |
| `AtomGit-GetWatchedRepos` | 获取 Watch 的仓库 | `AtomGit-GetWatchedRepos` |
| `AtomGit-GetUserEvents` | 获取用户动态 | `AtomGit-GetUserEvents -Username "user"` |

---

## 📁 Repositories 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `AtomGit-GetRepos` | 获取我的仓库 | `AtomGit-GetRepos` |
| `AtomGit-GetRepoDetail` | 获取仓库详情 | `AtomGit-GetRepoDetail -Owner "o" -Repo "r"` |
| `AtomGit-GetRepoTree` | 获取文件树 | `AtomGit-GetRepoTree -Owner "o" -Repo "r"` |
| `AtomGit-GetRepoFile` | 获取文件内容 | `AtomGit-GetRepoFile -Owner "o" -Repo "r" -Path "README.md"` |
| `AtomGit-SearchRepos` | 搜索仓库 | `AtomGit-SearchRepos -Query "keyword"` |

---

## 🔀 Pull Requests 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `AtomGit-GetPRList` | 获取 PR 列表 | `AtomGit-GetPRList -Owner "o" -Repo "r"` |
| `AtomGit-GetPRDetail` | 获取 PR 详情 | `AtomGit-GetPRDetail -Owner "o" -Repo "r" -PR 123` |
| `AtomGit-GetPRFiles` | 获取变更文件 | `AtomGit-GetPRFiles -Owner "o" -Repo "r" -PR 123` |
| `AtomGit-GetPRCommits` | 获取提交记录 | `AtomGit-GetPRCommits -Owner "o" -Repo "r" -PR 123` |
| `AtomGit-ApprovePR` | 批准 PR | `AtomGit-ApprovePR -Owner "o" -Repo "r" -PR 123` |
| `AtomGit-MergePR` | 合并 PR | `AtomGit-MergePR -Owner "o" -Repo "r" -PR 123` |
| `AtomGit-CheckPR` | 触发 PR 检查 | `AtomGit-CheckPR -Owner "o" -Repo "r" -PR 123` |
| `AtomGit-CreatePR` | 创建 PR | `AtomGit-CreatePR -Owner "o" -Repo "r" -Title "标题" -Head "branch" -Base "main"` |

---

## 📝 Issues 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `AtomGit-GetIssues` | 获取 Issue 列表 | `AtomGit-GetIssues -Owner "o" -Repo "r"` |
| `AtomGit-GetIssueDetail` | 获取 Issue 详情 | `AtomGit-GetIssueDetail -Owner "o" -Repo "r" -Issue 123` |
| `AtomGit-CreateIssue` | 创建 Issue | `AtomGit-CreateIssue -Owner "o" -Repo "r" -Title "标题"` |
| `AtomGit-UpdateIssue` | 更新 Issue | `AtomGit-UpdateIssue -Owner "o" -Repo "r" -Issue 123 -State "closed"` |
| `AtomGit-GetIssueComments` | 获取评论 | `AtomGit-GetIssueComments -Owner "o" -Repo "r" -Issue 123` |
| `AtomGit-AddIssueComment` | 添加评论 | `AtomGit-AddIssueComment -Owner "o" -Repo "r" -Issue 123 -Comment "评论"` |

---

## 🔧 工具命令

### AtomGit-Help

**查看帮助信息**

```powershell
AtomGit-Help
```

---

## ⚡ 批量处理

### 并行处理 PR

```powershell
# 加载批量脚本
. ~/.openclaw/workspace/skills/atomgit-ps/scripts/atomgit-batch.ps1

# 并行处理多个 PR
Invoke-BatchApprove -Owner "openeuler" -Repo "release-management" `
    -PRs @(2557, 2558, 2560) `
    -Parallel `
    -MaxConcurrency 3
```

**性能提升**: 80% (从 3 分钟降至 35 秒)

---

## ⚠️ 暂不支持的功能

- **AtomGit-GetPRReviews** - AtomGit API 不支持 `/pulls/{id}/reviews` 端点 (返回 404)

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| [README.md](README.md) | 快速入门 |
| [API-REFERENCE.md](API-REFERENCE.md) | API 参考 |
| [CHANGELOG.md](CHANGELOG.md) | 更新日志 |

---

*最后更新：2026-03-24*
