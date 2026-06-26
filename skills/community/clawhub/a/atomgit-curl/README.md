# AtomGit-Curl 技能

> AtomGit (GitCode) 代码托管平台集成工具 - **Curl/Bash 版本**  
> **版本**: v2.6.0  
> **平台**: Windows ✅ (Git Bash) | Linux ✅ | macOS ✅  
> **命令数**: ~38 个

---

## 🚀 快速开始

### 前置要求

- ✅ **Windows**: Git Bash (安装 Git for Windows) 或 WSL
- ✅ **Linux**: curl 7.0+ + bash 4.0+ (通常已预装)
- ✅ **macOS**: curl 7.0+ + bash 4.0+ (通常已预装)

**Windows 用户**:
```bash
# 方式 1: 安装 Git for Windows (推荐)
# 下载地址：https://git-scm.com/download/win
# 安装后使用 Git Bash 运行

# 方式 2: 使用 WSL
# Windows Subsystem for Linux

# 方式 3: Windows 10+ 内置 curl
# 配合 Git Bash 使用 bash
```

### 安装

```bash
# 1. 设置执行权限
chmod +x ~/.openclaw/workspace/skills/atomgit-curl/scripts/atomgit.sh

# 2. 配置 Token (优先级：环境变量 > openclaw.json)
export ATOMGIT_TOKEN="YOUR_TOKEN"
# 或编辑 ~/.openclaw/openclaw.json 添加：{"env": {"ATOMGIT_TOKEN": "YOUR_TOKEN"}}

# 3. 测试
./scripts/atomgit.sh help
```

### Token 配置

**优先级**: 环境变量 > openclaw.json

```bash
# 临时配置 (当前会话)
export ATOMGIT_TOKEN="YOUR_TOKEN"

# 持久配置 (编辑 ~/.openclaw/openclaw.json)
{
  "env": {
    "ATOMGIT_TOKEN": "YOUR_TOKEN"
  }
}
```

---

## 📋 命令总览

| 类别 | 命令数 | 说明 |
|------|--------|------|
| **认证** | 1 | 登录认证 |
| **Users** | 6 | 用户相关查询 |
| **Repositories** | 4 | 仓库管理 (含 repo-tree, repo-file) |
| **Pull Requests** | 9 | PR 管理 (含 pr-files, pr-commits, check-pr) |
| **Issues** | 6 | Issue 管理 (含 issue-detail, update-issue, issue-comments) |
| **总计** | **~26** | |

---

## 🔐 认证命令

### login - 登录认证

```bash
./scripts/atomgit.sh login YOUR_TOKEN
```

**输出**:
```
🔐 当前 Token 状态
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ 登录成功！欢迎，username
   邮箱：user@example.com
   主页：https://atomgit.com/username
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 👤 Users 命令

### user-info - 获取用户信息

```bash
./scripts/atomgit.sh user-info
```

### user-profile - 获取指定用户信息

```bash
./scripts/atomgit.sh user-profile username
```

### user-repos - 获取用户仓库

```bash
./scripts/atomgit.sh user-repos [username]
```

### starred-repos - 获取 Star 的仓库

```bash
./scripts/atomgit.sh starred-repos
```

### watched-repos - 获取 Watch 的仓库

```bash
./scripts/atomgit.sh watched-repos
```

### user-events - 获取用户动态

```bash
./scripts/atomgit.sh user-events [username]
```

---

## 📁 Repositories 命令

### repo-detail - 获取仓库详情

```bash
./scripts/atomgit.sh repo-detail openeuler release-management
```

### search-repos - 搜索仓库

```bash
./scripts/atomgit.sh search-repos kde
```

---

## 🔀 Pull Requests 命令

### pr-list - 获取 PR 列表

```bash
./scripts/atomgit.sh pr-list openeuler release-management [open]
```

### pr-detail - 获取 PR 详情

```bash
./scripts/atomgit.sh pr-detail openeuler release-management 2560
```

### approve-pr - 批准 PR

```bash
./scripts/atomgit.sh approve-pr openeuler release-management 2560 "/approve"
```

### batch-approve - 批量批准 PR

```bash
./scripts/atomgit.sh batch-approve openeuler release-management 2557 2558 2560
```

**输出**:
```
🔄 批量批准 PR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   ✅ PR #2557 已批准
   ✅ PR #2558 已批准
   ✅ PR #2560 已批准
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### merge-pr - 合并 PR

```bash
./scripts/atomgit.sh merge-pr openeuler release-management 2560 "合并完成"
```

### create-pr - 创建 PR

```bash
./scripts/atomgit.sh create-pr openeuler release-management "标题" "feature-branch" "main" "描述"
```

---

## 📝 Issues 命令

### issues-list - 获取 Issues 列表

```bash
./scripts/atomgit.sh issues-list openeuler release-management [open]
```

### create-issue - 创建 Issue

```bash
./scripts/atomgit.sh create-issue openeuler release-management "发现 Bug" "详细描述..."
```

### add-issue-comment - 添加 Issue 评论

```bash
./scripts/atomgit.sh add-issue-comment openeuler release-management 123 "已修复"
```

---

## ⚡ 批量处理示例

### 批量批准 PR

```bash
# 批准多个 PR
./scripts/atomgit.sh batch-approve openeuler release-management 2557 2558 2560 2547 2505
```

### 批量操作脚本

```bash
#!/bin/bash
# 批量处理待审查 PR

OWNER="openeuler"
REPO="release-management"
PRS=(2557 2558 2560)

for pr in "${PRS[@]}"; do
    ./scripts/atomgit.sh approve-pr $OWNER $REPO $pr
done
```

---

## 🔧 配置

### Token 配置

**方式 1: 环境变量**
```bash
export ATOMGIT_TOKEN="YOUR_TOKEN"
```

**方式 2: 配置文件**
```bash
# ~/.atomgit/config
export ATOMGIT_TOKEN="YOUR_TOKEN"
export ATOMGIT_BASE_URL="https://api.atomgit.com/api/v5"
```

**方式 3: 每次指定**
```bash
./scripts/atomgit.sh login YOUR_TOKEN
```

---

## 💡 使用技巧

### 1. 使用环境变量

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export ATOMGIT_TOKEN="YOUR_TOKEN"
export PATH="$PATH:~/.openclaw/workspace/skills/atomgit-curl/scripts"

# 重新加载
source ~/.bashrc

# 直接使用命令
atomgit.sh user-info
```

### 2. 创建别名

```bash
# 添加到 ~/.bashrc
alias atomgit='~/.openclaw/workspace/skills/atomgit-curl/scripts/atomgit.sh'

# 使用
atomgit user-info
atomgit pr-list openeuler release-management
```

### 3. 批量处理脚本

```bash
#!/bin/bash
# daily-review.sh

OWNER="openeuler"
REPO="release-management"

# 获取待审查 PR
./scripts/atomgit.sh pr-list $OWNER $REPO open

# 批量批准
./scripts/atomgit.sh batch-approve $OWNER $REPO 2557 2558 2560
```

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| [SKILL.md](SKILL.md) | 技能描述 |
| [commands.md](commands.md) | 完整命令参考 |
| [API-REFERENCE.md](API-REFERENCE.md) | API 快速参考 |
| [COMPARISON.md](COMPARISON.md) | 技术对比分析 (可选) |

---

## 🔗 外部资源

- **官方 API 文档**: https://docs.atomgit.com/docs/apis/
- **Token 管理**: https://atomgit.com/setting/token-classic
- **帮助中心**: https://atomgit.com/help

---

## 📝 更新历史

### v2.6.0 (2026-03-25)

- ✅ 新增 11 个 API 功能
- ✅ 新增 API-REFERENCE.md 文档
- ✅ PR 审查列表、更新 PR、添加 Issue 指派人
- ✅ 创建仓库、添加协作者、获取协作者列表
- ✅ 获取 Issue 时间线、获取标签列表
- ✅ 获取 Webhook 列表、获取发布列表

### v2.2.0 (2026-03-25)

- ✅ 新增 CI 流水线检查功能 (check-ci 命令)
- ✅ 支持读取 openeuler-ci-bot 评论判断流水线状态
- ✅ HTML 表格解析优化

### v2.1.0 (2026-03-24)

- ✅ 新增 repo-tree, repo-file 命令
- ✅ 新增 pr-files, pr-commits, check-pr 命令
- ✅ 新增 issue-detail, update-issue, issue-comments 命令
- ✅ 批量处理支持 (串行)
- ✅ 完善错误处理和彩色输出

---

*最后更新：2026-03-25*  
*技能版本：v2.6.0*
