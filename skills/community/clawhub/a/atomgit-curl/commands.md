# AtomGit-Curl 命令参考

> **版本**: v2.2.0  
> **最后更新**: 2026-03-25

---

## 🚀 快速启动

```bash
# 1. 设置执行权限
chmod +x ~/.openclaw/workspace/skills/atomgit-curl/scripts/atomgit.sh

# 2. 登录
./scripts/atomgit.sh login YOUR_TOKEN

# 3. 查看帮助
./scripts/atomgit.sh help
```

---

## 📋 命令总览

| 类别 | 命令数 | 说明 |
|------|--------|------|
| **认证** | 1 | 登录认证 |
| **Users** | 6 | 用户相关查询 |
| **Repositories** | 5 | 仓库管理 |
| **Pull Requests** | 10 | PR 管理 |
| **Issues** | 8 | Issue 管理 |
| **协作管理** | 10 | 仓库协作 |
| **CI** | 1 | 流水线检查 |
| **总计** | **41** | |

---

## 🔐 认证命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `login` | 登录/设置 Token | `./atomgit.sh login TOKEN` |

---

## 👤 Users 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `user-info` | 获取当前用户信息 | `./atomgit.sh user-info` |
| `user-profile` | 获取指定用户信息 | `./atomgit.sh user-profile username` |
| `user-repos` | 获取用户仓库 | `./atomgit.sh user-repos [username]` |
| `starred-repos` | 获取 Star 的仓库 | `./atomgit.sh starred-repos` |
| `watched-repos` | 获取 Watch 的仓库 | `./atomgit.sh watched-repos` |
| `user-events` | 获取用户动态 | `./atomgit.sh user-events [username]` |

---

## 📁 Repositories 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `get-repos` | 获取我的仓库 | `./atomgit.sh get-repos` |
| `repo-detail` | 获取仓库详情 | `./atomgit.sh repo-detail owner repo` |
| `repo-tree` | 获取文件树 | `./atomgit.sh repo-tree owner repo [ref]` |
| `repo-file` | 获取文件内容 | `./atomgit.sh repo-file owner repo path` |
| `search-repos` | 搜索仓库 | `./atomgit.sh search-repos query` |

---

## 🔀 Pull Requests 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `pr-list` | 获取 PR 列表 | `./atomgit.sh pr-list owner repo [state]` |
| `pr-detail` | 获取 PR 详情 | `./atomgit.sh pr-detail owner repo pr` |
| `pr-files` | 获取变更文件 | `./atomgit.sh pr-files owner repo pr` |
| `pr-commits` | 获取提交记录 | `./atomgit.sh pr-commits owner repo pr` |
| `approve-pr` | 批准 PR | `./atomgit.sh approve-pr owner repo pr [comment]` |
| `batch-approve` | 批量批准 PR | `./atomgit.sh batch-approve owner repo pr1 pr2 pr3` |
| `merge-pr` | 合并 PR | `./atomgit.sh merge-pr owner repo pr [message]` |
| `check-pr` | 触发 PR 检查 | `./atomgit.sh check-pr owner repo pr` |
| `check-ci` | 检查 CI 流水线 | `./atomgit.sh check-ci owner repo pr` |

---

## 📝 Issues 命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `issues-list` | 获取 Issues 列表 | `./atomgit.sh issues-list owner repo [state]` |
| `issue-detail` | 获取 Issue 详情 | `./atomgit.sh issue-detail owner repo issue` |
| `create-issue` | 创建 Issue | `./atomgit.sh create-issue owner repo title [body]` |
| `update-issue` | 更新 Issue | `./atomgit.sh update-issue owner repo issue [state]` |
| `issue-comments` | 获取 Issue 评论 | `./atomgit.sh issue-comments owner repo issue` |
| `add-issue-comment` | 添加 Issue 评论 | `./atomgit.sh add-issue-comment owner repo issue comment` |

---

## 🔧 工具命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `help` | 查看帮助信息 | `./atomgit.sh help` |

---

## ⚠️ 暂不支持的功能

- **pr-reviews** - AtomGit API 不支持 `/pulls/{id}/reviews` 端点 (返回 404)

---

## ⚡ 批量处理示例

### 批量批准 PR

```bash
./atomgit.sh batch-approve openeuler release-management 2557 2558 2560
```

### 批量操作脚本

```bash
#!/bin/bash
OWNER="openeuler"
REPO="release-management"
PRS=(2557 2558 2560)

for pr in "${PRS[@]}"; do
    ./atomgit.sh approve-pr $OWNER $REPO $pr
done
```

---

## 🔍 CI 检查

### 检查流水线状态

```bash
./atomgit.sh check-ci openeuler release-management 2560
```

**输出示例**:
```
=== AtomGit CI Check ===

Checking PR #2560...
Found CI bot comments

=== CI Check Results ===
Total: 5
Success: 5
Failure: 0
Running: 0

Details:
----------------------------------------
[OK] openEuler-24.03-LTS-SP3-Next-x86_64: success
[OK] openEuler-24.03-LTS-SP3-Next-aarch64: success
----------------------------------------

Overall: SUCCESS
All 5 checks passed!
```

**状态码**:
- `0` - ✅ SUCCESS (全部通过)
- `1` - ⏳ RUNNING (有运行中)
- `2` - ❌ FAILED (有失败)

---

## 🔗 外部资源

- **官方 API 文档**: https://docs.atomgit.com/docs/apis/
- **Token 管理**: https://atomgit.com/setting/token-classic
- **帮助中心**: https://atomgit.com/help

---

*最后更新：2026-03-25*
