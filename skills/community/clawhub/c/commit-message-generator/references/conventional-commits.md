# Conventional Commits 规范

## 概述

Conventional Commits 是一种为提交信息添加简单规则的规范，便于生成变更日志、自动化版本发布等。

## 提交信息结构

```
<type>(<scope>): <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

### 必需部分

- **type**（必需）：提交类型
- **subject**（必需）：简短描述

### 可选部分

- **scope**（可选）：影响范围
- **body**（可选）：详细描述
- **footer**（可选）：页脚信息

---

## 提交类型（type）

| 类型 | 说明 | 版本影响 |
|------|------|----------|
| `feat` | 新功能 | 次版本号（minor） |
| `fix` | 修复 Bug | 修订号（patch） |
| `docs` | 文档更新 | 无 |
| `style` | 代码格式（不影响功能） | 无 |
| `refactor` | 重构（既不是新功能也不是 Bug 修复） | 无 |
| `perf` | 性能优化 | 修订号（patch） |
| `test` | 测试相关 | 无 |
| `chore` | 构建过程或辅助工具变动 | 无 |
| `ci` | CI 配置 | 无 |
| `build` | 构建系统 | 无 |
| `revert` | 回滚 | 依回滚内容而定 |

---

## 影响范围（scope）

scope 用于标识提交影响的范围，通常是模块名、组件名或文件名。

### 常见 scope 示例

```
feat(auth): 新增用户登录功能
fix(api): 修复接口超时问题
docs(readme): 更新安装说明
refactor(core): 重构核心算法
test(ui): 添加界面测试用例
chore(build): 更新构建配置
```

### scope 命名建议

- 使用小写字母
- 使用连字符分隔单词（如 `user-management`）
- 保持简洁，2-3 个音节为宜
- 团队内部统一 scope 列表

---

## 主题行（subject）

### 规则

1. **时态**：使用一般现在时（"add" 而非 "added"）
2. **语气**：使用祈使句（"change" 而非 "changes"）
3. **大小写**：首字母小写
4. **标点**：末尾不加句号
5. **长度**：不超过 50 字符

### 正确示例

```
feat: add user authentication
fix: resolve memory leak in parser
docs: update installation guide
```

### 错误示例

```
feat: added new feature          # 时态错误
fix: fixed the bug               # 时态错误
docs: updating readme            # 时态错误
feat: Add New Feature            # 大小写错误
fix: fix the issue.              # 多余标点
feat: this is a very long subject line that exceeds 50 characters  # 过长
```

---

## 正文（body）

### 规则

1. **内容**：说明为什么修改，而非修改了什么
2. **格式**：每行不超过 72 字符
3. **可选**：可以包含多个变更点

### 示例

```
feat(auth): add OAuth2 support

- Integrate OAuth2 provider for third-party login
- Add token refresh mechanism
- Update user session management

This change enables users to log in using Google,
GitHub, or Microsoft accounts.
```

---

## 页脚（footer）

### Issue 关联

```
Closes #123
Fixes #456
Refs #789
```

### 破坏性变更

```
BREAKING CHANGE: authentication API now requires token

The previous session-based authentication has been
replaced with token-based authentication.

Migration guide:
1. Update client to include token in requests
2. Handle 401 responses for token refresh
```

### 联合作者

```
Co-authored-by: Name <name@example.com>
```

---

## 完整示例

### 示例 1：新功能

```
feat(user): add password reset functionality

- Add password reset request endpoint
- Send reset email with token
- Implement token validation

Closes #234
```

### 示例 2：Bug 修复

```
fix(api): resolve null pointer in user service

- Add null check before accessing user profile
- Return 404 for non-existent users

Fixes #567
```

### 示例 3：破坏性变更

```
refactor(auth): migrate to JWT tokens

BREAKING CHANGE: session-based auth replaced with JWT

The authentication API now returns JWT tokens instead
of session IDs. Clients must update to handle tokens.

Migration:
1. Update auth request to accept JWT
2. Store token in localStorage
3. Include token in Authorization header

Closes #890
```

### 示例 4：重构

```
refactor(core): simplify validation logic

- Extract validation rules to separate module
- Remove duplicate validation code
- Add unit tests for edge cases

Impact: No functional changes, improved maintainability
```

---

## 工具集成

### Git Hook 示例

```bash
#!/bin/bash
# .git/hooks/commit-msg

commit_msg=$(cat "$1")
if ! grep -qE "^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(\([a-z-]+\))?: .{1,50}$" <<< "$commit_msg"; then
    echo "ERROR: Commit message does not follow Conventional Commits"
    exit 1
fi
```

### 自动生成变更日志

```bash
# 使用 conventional-changelog
npx conventional-changelog -p angular -i CHANGELOG.md -s
```

### 自动版本发布

```bash
# 使用 semantic-release
npx semantic-release
```

---

## 最佳实践

1. **原子提交**：一次提交只做一件事
2. **及时提交**：完成小功能就提交，不要堆积
3. **清晰描述**：让他人（和未来的你）能看懂
4. **关联 Issue**：便于追溯和项目管理
5. **审查历史**：定期查看 git log，保持规范

---

## 参考资料

- [Conventional Commits 官网](https://www.conventionalcommits.org/)
- [Angular Commit Message Guidelines](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)
- [semantic-release](https://semantic-release.gitbook.io/)
- [conventional-changelog](https://github.com/conventional-changelog/conventional-changelog)
