# 提交信息示例集合

## 按类型分类

### feat - 新功能

```
feat: add dark mode support
feat(ui): implement responsive layout
feat(api): add GraphQL endpoint
feat(auth): support multi-factor authentication
feat(search): add full-text search capability
```

### fix - Bug 修复

```
fix: resolve crash on startup
fix(parser): handle empty input correctly
fix(api): fix timeout issue in user service
fix(ui): correct button alignment on mobile
fix(database): prevent race condition in updates
```

### docs - 文档

```
docs: update README with installation steps
docs(api): add endpoint documentation
docs(readme): fix typos in examples
docs(contributing): add code style guidelines
docs(changelog): update release notes for v2.0
```

### style - 代码格式

```
style: format code with prettier
style(lint): fix eslint warnings
style(format): apply consistent indentation
style: remove trailing whitespace
style(import): organize import statements
```

### refactor - 重构

```
refactor: simplify error handling logic
refactor(core): extract common utilities
refactor(service): reduce method complexity
refactor: replace callbacks with promises
refactor(module): improve code organization
```

### perf - 性能优化

```
perf: reduce bundle size by 30%
perf(query): optimize database query
perf(cache): implement redis caching
perf(render): use virtual scrolling for lists
perf: lazy load images on scroll
```

### test - 测试

```
test: add unit tests for auth module
test(api): increase coverage to 80%
test(e2e): add login flow tests
test: fix flaky test in user service
test(integration): add api integration tests
```

### chore - 杂项

```
chore: update dependencies to latest
chore(build): configure webpack for production
chore(ci): add github actions workflow
chore: clean up unused imports
chore(release): bump version to 1.2.0
```

### ci - CI 配置

```
ci: add automated testing pipeline
ci(github): configure actions for PR checks
ci: enable code coverage reporting
ci(deploy): add staging deployment
ci: parallelize test execution
```

### build - 构建系统

```
build: upgrade to node 18
build(webpack): optimize build configuration
build: add source map generation
build(docker): create production image
build: configure typescript strict mode
```

### revert - 回滚

```
revert: revert "feat: add new dashboard"

This reverts commit abc123def due to performance issues.
```

---

## 按场景分类

### 日常开发

```
feat: add user profile page
fix: correct calculation error
refactor: clean up legacy code
docs: update api documentation
```

### 紧急修复

```
fix(critical): resolve production outage
fix(security): patch authentication bypass
fix(data): prevent data loss on error
```

### 版本发布

```
chore(release): v2.0.0
chore: update changelog for release
docs: add migration guide for v2.0
```

### 团队协作

```
feat: implement feature X for team Y

Co-authored-by: Alice <alice@example.com>
Co-authored-by: Bob <bob@example.com>

Closes #123
```

---

## 完整示例

### 示例 1：小型修复

```
fix: correct typo in error message
```

### 示例 2：功能开发

```
feat(notification): add push notification support

- Integrate Firebase Cloud Messaging
- Add notification preferences UI
- Implement notification history

Closes #456
```

### 示例 3：大型重构

```
refactor(auth): migrate to OAuth2

BREAKING CHANGE: OAuth2 replaces basic auth

The authentication system has been completely
rewritten to use OAuth2 protocol.

Changes:
- Remove basic auth endpoints
- Add OAuth2 authorization flow
- Update all API clients

Migration:
1. Update client credentials
2. Implement OAuth2 flow
3. Remove basic auth code

Closes #789
```

### 示例 4：性能优化

```
perf: optimize image loading

- Implement lazy loading
- Add image compression
- Use webp format with fallback

Results:
- Initial load time: -40%
- Bandwidth usage: -60%

Fixes #234
```

---

## 常见错误

### ❌ 错误示例

```
# 太模糊
fix: fix stuff

# 太长
feat: add a new feature that allows users to customize their profile page with different themes and layouts

# 时态错误
fix: fixed the bug in the parser

# 缺少上下文
update: changed some things

# 标点错误
feat: add new feature.
```

### ✅ 正确示例

```
# 清晰简洁
fix: resolve parser crash on empty input

# 包含范围
feat(profile): add theme customization

# 正确时态
fix: correct calculation error

# 详细说明
refactor(core): simplify validation logic

- Extract rules to separate module
- Remove duplicate code
- Add unit tests
```

---

## 团队规范模板

```markdown
## 我们的提交规范

1. **必须使用 Conventional Commits**
   - 类型：feat/fix/docs/style/refactor/perf/test/chore
   - 范围：模块名（小写）
   - 主题：50 字符以内

2. **正文要求**
   - 说明为什么修改
   - 每行 72 字符以内
   - 可包含变更列表

3. **Issue 关联**
   - 有需求号必须关联
   - 使用 Closes/Fixes/Refs

4. **破坏性变更**
   - 必须标注 BREAKING CHANGE
   - 提供迁移指南

5. **审查要点**
   - 原子提交
   - 清晰描述
   - 关联 Issue
```
