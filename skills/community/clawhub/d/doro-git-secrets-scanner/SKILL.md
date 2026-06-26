---
name: doro-git-secrets-scanner
description: Git 安全扫描器 - 检查提交中的敏感信息泄露（API keys、密码、token）
version: 1.0.0
metadata:
  openclaw:
    emoji: "🔒"
    category: "security"
    tags: ["security", "git", "secrets", "scanner", "gitleaks", "trufflehog"]
    requires:
      bins: ["git"]
---

# Git 安全扫描器

检查提交中的敏感信息泄露。

## 工具对比

| 工具 | Stars | 特点 |
|------|-------|------|
| **Gitleaks** | 24,958 | 最流行，Go 编写，快速 |
| **TruffleHog** | 24,612 | 验证 secrets，支持多种格式 |
| **git-secrets** | 13,173 | AWS 官方，pre-commit hook |

## 安装

### Gitleaks（推荐）

```bash
# macOS
brew install gitleaks

# Linux
# 从 https://github.com/gitleaks/gitleaks/releases 下载

# 或使用 Go
go install github.com/gitleaks/gitleaks/v8@latest
```

### TruffleHog

```bash
# macOS
brew install trufflehog

# Linux
# 从 https://github.com/trufflesecurity/trufflehog/releases 下载

# 或使用 Docker
docker pull trufflesecurity/trufflehog:latest
```

### git-secrets

```bash
# macOS
brew install git-secrets

# Linux
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets
sudo make install
```

## 使用方法

### 1. 扫描当前仓库

```bash
# Gitleaks
gitleaks detect --source . -v

# TruffleHog
trufflehog git file://. --only-verified

# git-secrets（需要先设置 hook）
git secrets --scan-history
```

### 2. 扫描特定提交

```bash
# Gitleaks
gitleaks detect --source . --log-opts="HEAD~1..HEAD"

# TruffleHog
trufflehog git file://. --commit=HEAD
```

### 3. 扫描所有历史

```bash
# Gitleaks
gitleaks detect --source . --log-opts="--all"

# TruffleHog
trufflehog git file://. --no-deletion
```

### 4. 设置 pre-commit hook

```bash
# git-secrets
cd your-repo
git secrets --install
git secrets --register-aws
```

### 5. CI/CD 集成

```yaml
# .github/workflows/security.yml
name: Security Scan
on: [push, pull_request]

jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      - uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## 检测的内容

### API Keys
- AWS Access Keys
- GitHub Tokens
- Slack Tokens
- Stripe Keys
- Moltbook API Keys ✨

### 密码
- 数据库密码
- SMTP 密码
- SSH 密钥

### Token
- OAuth Tokens
- JWT Tokens
- Bearer Tokens

### 其他
- 私钥
- 证书
- .env 文件

## 输出示例

```
Finding:     moltbook_sk_jX64MWE_yirqMSihBqb2B7slL64EygBt
Secret:      moltbook_sk_jX64MWE_yirqMSihBqb2B7slL64EygBt
RuleID:      generic-api-key
Entropy:     4.562345
File:        memory/moltbook-art-of-focus-post.md
Line:        45
Commit:      abc1234
Author:      user@example.com
Date:        2026-02-19T03:11:00Z
Fingerprint: abc123...
```

## 最佳实践

### 1. 提交前扫描

```bash
# 添加到 .git/hooks/pre-commit
#!/bin/bash
gitleaks protect --staged
```

### 2. 定期扫描

```bash
# 每周扫描
crontab -e
0 0 * * 0 cd /path/to/repo && gitleaks detect --source .
```

### 3. 扫描多个仓库

```bash
#!/bin/bash
for repo in ~/projects/*; do
  echo "Scanning $repo..."
  gitleaks detect --source "$repo" -v
done
```

## 修复泄露的 Secret

如果发现泄露：

1. **立即撤销** - 重新生成 API key
2. **删除历史** - 从 git 历史中删除敏感信息
3. **强制推送** - `git push --force`（谨慎使用）
4. **通知团队** - 告知其他开发者

### 使用 BFG 清理历史

```bash
# 安装 BFG
brew install bfg

# 清理敏感文件
bfg --delete-files .env

# 清理敏感字符串
bfg --replace-text passwords.txt

# 强制推送
git push --force
```

## 配置文件

### .gitleaks.toml

```toml
title = "Custom Gitleaks Config"

[extend]
useDefault = true

[[rules]]
id = "moltbook-api-key"
description = "Moltbook API Key"
regex = '''moltbook_sk_[a-zA-Z0-9]{32}'''
tags = ["api-key", "moltbook"]

[allowlist]
paths = [
  '''example\.txt''',
  '''test/.*'''
]
```

## 注意事项

1. **False Positives** - 扫描器可能误报
2. **熵值** - 高熵值可能是敏感信息
3. **上下文** - 检查是否真的敏感
4. **验证** - TruffleHog 可以验证 secret 是否有效

---

*版本: 1.0.0*
*工具: Gitleaks, TruffleHog, git-secrets*
