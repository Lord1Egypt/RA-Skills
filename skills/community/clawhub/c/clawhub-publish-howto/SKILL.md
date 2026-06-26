---
name: clawhub-publish-howto
description: 发布技能到 ClawHub 的完整流程与故障排查。当需要发布、更新、调试 OpenClaw skill 到 ClawHub 时使用。包含账号准备、认证配置、发布命令、常见错误排查。
version: 1.0.0
tags: [clawhub, publish, skill, github, troubleshooting, rate-limit]
license: MIT
---

# ClawHub 发布技能

## 发布前检查清单

| 检查项 | 命令 |
|--------|------|
| 登录状态 | `clawhub whoami` |
| GitHub Token 限额 | `curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit` |
| 账号年龄 | GitHub 账号需满 **14 天**才能发布 |

## 认证方式（推荐）

### 方法一：Token 登录（服务器/无头环境推荐）

```bash
# 1. 获取 clawhub token
clawhub login

# 2. 使用 token 登录（无浏览器）
clawhub login --token <clh_token>

# 3. 验证
clawhub whoami
```

### 方法二：环境变量配置 GitHub Token（解决限流）

clawhub 后台使用共享的 GitHub App 配额（180次/小时），容易触发限流。
配置自己的 GitHub Token 可以突破共享限额：

```bash
# 临时使用（单次）
GITHUB_TOKEN="ghp_your_token_here" clawhub publish <path> --version 1.0.0 --tags "..."

# 永久配置（加到 ~/.bashrc 或环境变量）
echo 'export GITHUB_TOKEN="ghp_your_token_here"' >> ~/.bashrc
source ~/.bashrc
```

**验证 Token 有效：**
```bash
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/rate_limit
# 限额应为 5000（不是 60）
```

## 发布命令

```bash
# 标准发布
clawhub publish /path/to/skill --version 1.0.0 --tags "tag1,tag2,tag3"

# 带名称
clawhub publish /path/to/skill --name "Skill Name" --version 1.0.0 --tags "..."

# 带变更日志
clawhub publish /path/to/skill --version 1.0.0 --changelog "Initial release"
```

## 常见错误排查

### 1. `GitHub API rate limit exceeded`

**原因：** clawhub 共享的 GitHub App 配额耗尽

**解决：** 使用自己的 `GITHUB_TOKEN`
```bash
GITHUB_TOKEN="ghp_your_token" clawhub publish ...
```

### 2. `GitHub account must be at least 14 days old`

**原因：** GitHub 账号年龄不足 14 天

**解决：** 等待账号满 14 天（无法绕过）
```bash
# 查看账号创建日期
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user | jq '.created_at'
```

### 3. `Error: Not logged in`

**原因：** 未登录或登录已过期

**解决：**
```bash
clawhub login --token <clh_token>
clawhub whoami
```

### 4. `rate limit exceeded` 但 `remaining: 179/180`

**原因：** 账号年龄不足时，clawhub 错误地显示为限流（而非账号年龄错误）

**特征：** 每次都是 `179/180`，reset 40-55 秒，间隔短且稳定

**解决：** 用 `GITHUB_TOKEN` 看真实错误：
```bash
GITHUB_TOKEN="ghp_your_token" clawhub publish ...
# 会显示真正的错误：账号年龄不足
```

### 5. `Skill.md required`

**原因：** SKILL.md 文件不存在

**解决：** 确保 skill 目录中有 `SKILL.md` 或 `skills.md`

### 6. `--version must be valid semver`

**原因：** 版本号格式错误

**解决：** 使用标准 semver：`1.0.0`、`0.1.0`、`2.3.4-beta`

## SKILL.md 必填字段

```yaml
---
name: skill-slug          # 唯一标识（英文、连字符）
description: 描述         # 一句话说明
version: 1.0.0          # 语义化版本
tags: [tag1, tag2]       # 标签
license: MIT             # 许可证
---
```

## 发布后验证

```bash
# CLI 验证
clawhub inspect <slug>

# 网页验证
# https://clawhub.ai/skills/<slug>
```

## 关键经验总结

1. **用自己的 GITHUB_TOKEN** — 避免 clawhub 共享限流
2. **账号需满 14 天** — 这是 GitHub 策略，无法绕过
3. **错误信息可能不准确** — `rate limit exceeded` 也可能是账号年龄问题
4. **用 GITHUB_TOKEN 前缀看真实错误** — 绕过 clawhub 的错误映射
5. **发布前先 inspect** — 确认 skill 名称未被占用
