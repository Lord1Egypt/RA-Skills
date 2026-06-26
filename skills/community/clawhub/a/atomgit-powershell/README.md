# AtomGit-PowerShell 技能

> AtomGit (GitCode) 代码托管平台集成工具 - **PowerShell 版本**  
> **版本**: v3.0.0  
> **平台**: Windows ✅ | Linux ✅ | macOS ✅  
> **新增**: CI 流水线检查功能

---

## 🚀 快速开始

### 前置要求

- ✅ PowerShell 5.1+ (Windows 内置)
- ✅ .NET Framework 4.7+
- ✅ 网络连接 (访问 api.atomgit.com)

### 安装

```powershell
# 方式 1: ClawHub (推荐)
clawhub install atomgit-powershell

# 方式 2: 手动安装
# 1. 配置 Token (优先级：环境变量 > openclaw.json)
$env:ATOMGIT_TOKEN="YOUR_TOKEN"
# 或编辑 ~/.openclaw/openclaw.json 添加：{"env": {"ATOMGIT_TOKEN": "YOUR_TOKEN"}}

# 2. 加载技能
. ~/.openclaw/workspace/skills/atomgit-powershell/scripts/atomgit.ps1

# 3. 测试
AtomGit-Help
```

### Token 配置

**优先级**: 环境变量 > openclaw.json

```powershell
# 临时配置 (当前会话)
$env:ATOMGIT_TOKEN="YOUR_TOKEN"

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
| **Repositories** | 5 | 仓库管理 |
| **Pull Requests** | 8 | PR 管理 |
| **Issues** | 6 | Issue 管理 |
| **工具** | 1 | 帮助信息 |
| **总计** | **~26** | |

**完整命令列表**: [commands.md](commands.md)

---

## ⚡ 特色功能

### 1. 批量并行处理

```powershell
# 加载批量脚本
. ~/.openclaw/workspace/skills/atomgit-powershell/scripts/atomgit-batch.ps1

# 并行处理多个 PR，性能提升 80%
Invoke-BatchApprove -Owner "openeuler" -Repo "release-management" `
    -PRs @(2557, 2558, 2560) `
    -Parallel `
    -MaxConcurrency 3
```

**性能对比**:
- 串行处理 3 个 PR: ~3 分钟
- 并行处理 3 个 PR: ~35 秒
- **提升**: 81% ⬇️

---

### 2. 智能处理规则

| 情况 | 规则 | 提醒 |
|------|------|------|
| 已添加 `/lgtm` 评论 | ✅ 已处理 | ❌ 不提醒 |
| 已添加 `/approve` 评论 | ✅ 已处理 | ❌ 不提醒 |
| 已添加 `/close` 评论 | ✅ 已处理 | ❌ 不提醒 |
| 已添加任何文字评论 | ✅ 已处理 | ❌ 不提醒 |
| 无评论的 PR | ⏳ 待处理 | ✅ 提醒 |

---

### 3. CI 流水线检查 (v2.5.0 新增)

检查 PR 的 CI 流水线状态，读取 openeuler-ci-bot 的评论判断是否通过。

```powershell
# 加载主脚本（包含 CI 检查功能）
. ~/.openclaw/workspace/skills/atomgit-powershell/scripts/atomgit.ps1

# 检查单个 PR
AtomGit-CheckCI -Owner "openeuler" -Repo "release-management" -PR 2560
```

**输出示例**:
```
=== CI Check Results ===
Total Check Items: 5
Success: 5
Failure: 0
Running: 0

[OK] openEuler-24.03-LTS-SP3-Next-x86_64: success
[OK] openEuler-24.03-LTS-SP3-Next-aarch64: success

Overall: SUCCESS
All 5 checks passed!
```

**状态码**:
- `0` - ✅ SUCCESS (全部通过)
- `1` - ⏳ RUNNING (有运行中)
- `2` - ❌ FAILED (有失败)

---

## 💡 使用示例

### 登录

```powershell
AtomGit-Login "YOUR_TOKEN"
```

---

### 获取用户信息

```powershell
AtomGit-GetUserInfo
```

**输出**:
```
✅ 登录成功！欢迎，username
   邮箱：user@example.com
   主页：https://atomgit.com/username
```

---

### 获取 PR 列表

```powershell
AtomGit-GetPRList -Owner "openeuler" -Repo "release-management" -State "open"
```

---

### 批准 PR

```powershell
AtomGit-ApprovePR -Owner "openeuler" -Repo "release-management" -PR 2560 -Comment "/lgtm"
```

---

### 合并 PR

```powershell
AtomGit-MergePR -Owner "openeuler" -Repo "release-management" -PR 2560 -Message "合并完成"
```

---

### 批量处理

```powershell
# 加载批量脚本
. ~/.openclaw/workspace/skills/atomgit-powershell/scripts/atomgit-batch.ps1

# 并行批准多个 PR
Invoke-BatchApprove -Owner "openeuler" -Repo "release-management" `
    -PRs @(2557, 2558, 2560) `
    -Parallel
```

---

## 🔧 配置

### Token 配置

**方式 1: 环境变量**
```powershell
$env:ATOMGIT_TOKEN="YOUR_TOKEN"
```

**方式 2: 配置文件**
```powershell
# ~/.openclaw/config/atomgit.json
@{
    token = "YOUR_TOKEN"
    base_url = "https://api.atomgit.com/api/v5"
}
```

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| [commands.md](commands.md) | 完整命令参考 |
| [API-REFERENCE.md](API-REFERENCE.md) | API 快速参考 |
| [CHANGELOG.md](CHANGELOG.md) | 更新日志 |

---

## 🔗 外部资源

- **官方 API 文档**: https://docs.atomgit.com/docs/apis/
- **Token 管理**: https://atomgit.com/setting/token-classic
- **帮助中心**: https://atomgit.com/help

---

*最后更新：2026-03-25*  
*技能版本：v2.4.0*
