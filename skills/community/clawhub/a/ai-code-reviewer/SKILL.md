# AI Code Reviewer

AI 驱动的代码审查工具。自动分析代码质量、发现潜在 bug、生成 PR 描述、建议测试用例。支持多种编程语言。

## 触发词

- 代码审查
- code review
- 代码分析
- PR 描述
- 代码质量检查
- 自动 review

## 核心功能

### 1. 代码质量分析

- **代码风格检查**: 命名规范、缩进、注释完整性
- **潜在 bug 检测**: 空指针、资源泄漏、边界条件
- **性能优化建议**: 时间复杂度、内存使用、数据库查询
- **安全漏洞扫描**: SQL 注入、XSS、敏感信息泄漏

### 2. 智能 PR 描述生成

```
输入：Git diff 或代码变更
↓
AI 分析:
- 变更摘要
- 影响范围
- 测试建议
- 注意事项
↓
输出：完整的 PR 描述 (Markdown)
```

### 3. 测试用例生成

- 根据代码逻辑生成单元测试
- 覆盖边界条件和异常场景
- 支持主流测试框架 (Jest, Pytest, JUnit 等)

### 4. 多语言支持

| 语言 | 支持程度 | 框架 |
|------|---------|------|
| JavaScript/TypeScript | ✅ 完整 | ESLint, Jest |
| Python | ✅ 完整 | Pylint, Pytest |
| Java | ✅ 完整 | Checkstyle, JUnit |
| Go | ✅ 完整 | gofmt, go test |
| Rust | ✅ 完整 | clippy, cargo test |
| PHP | ✅ 完整 | PHPCS, PHPUnit |

## 配置说明

### 环境变量

```bash
# OpenRouter API (已有)
OPENROUTER_API_KEY=sk-or-v1-xxxxx

# GitHub Token (可选，用于自动 PR)
GITHUB_TOKEN=ghp_xxxxx

# 代码审查规则 (可选)
CODE_REVIEW_STRICTNESS=medium  # low/medium/high
ENABLE_SECURITY_CHECK=true
ENABLE_PERFORMANCE_CHECK=true
```

### 本地配置

在 `TOOLS.md` 中添加:

```markdown
### AI Code Reviewer 配置

- 默认审查严格度：medium
- 自动修复建议：是
- 生成测试用例：是
- 支持语言：JS/TS, Python, Java, Go, Rust, PHP
```

## 使用示例

### 基础用法

```
审查这段代码
```

### 指定语言

```
用 Python 审查这段代码
```

### 生成 PR 描述

```
为这个变更生成 PR 描述
```

### 生成测试

```
为这个函数生成单元测试
```

### 完整审查

```
完整审查：检查代码质量 + 生成 PR 描述 + 生成测试
```

## 输出格式

### 代码审查报告

```
🔍 AI 代码审查报告

📁 文件：src/utils/validator.js
📊 评分：85/100 (良好)

✅ 优点:
• 函数命名清晰
• 注释完整
• 错误处理得当

⚠️ 需要改进 (3 个):
1. [性能] 第 23 行：循环内重复计算，建议提取到循环外
   建议：const limit = items.length; for (let i = 0; i < limit; i++)

2. [安全] 第 45 行：用户输入未验证，存在注入风险
   建议：添加 sanitizeInput() 验证

3. [风格] 第 67 行：函数过长 (80 行)，建议拆分
   建议：拆分为 validateUser() 和 validatePermissions()

🧪 测试建议:
• 添加边界条件测试 (空数组、null、undefined)
• 添加异常输入测试
• 覆盖率目标：80%

📝 自动修复：需要我帮你修复这些问题吗？[是/否/查看建议]
```

### PR 描述

```markdown
## 🎯 变更摘要

实现了用户权限验证功能，包括角色检查和权限过滤。

## 📝 详细说明

- 新增 `validatePermissions()` 函数
- 优化了循环性能 (减少重复计算)
- 添加了输入验证防止注入攻击

## 🧪 测试

- [x] 单元测试已添加
- [x] 边界条件测试通过
- [ ] 集成测试待完成

## ⚠️ 注意事项

- 需要更新数据库迁移脚本
- 向后兼容，无需手动迁移

## 📋 检查清单

- [x] 代码审查通过
- [x] 测试覆盖率 > 80%
- [x] 文档已更新
```

### 测试用例

```javascript
// 生成的测试用例
describe('validatePermissions', () => {
  test('应该允许管理员访问所有资源', () => {
    const user = { role: 'admin' };
    expect(validatePermissions(user, 'any')).toBe(true);
  });

  test('应该拒绝未授权用户访问', () => {
    const user = { role: 'guest' };
    expect(validatePermissions(user, 'admin-only')).toBe(false);
  });

  test('应该处理空用户对象', () => {
    expect(() => validatePermissions(null, 'resource'))
      .toThrow('Invalid user object');
  });

  test('应该处理边界条件：空权限列表', () => {
    const user = { role: 'user', permissions: [] };
    expect(validatePermissions(user, 'resource')).toBe(false);
  });
});
```

## 错误处理

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| 语言不支持 | 非支持语言 | 提示支持的语言列表 |
| 代码过短 | 无法分析 | 建议提供完整函数/类 |
| API 限流 | 请求过多 | 自动重试 + 排队 |
| 语法错误 | 代码不完整 | 提示具体错误位置 |

## 定价策略

| 版本 | 价格 | 功能 |
|------|------|------|
| 免费版 | $0 | 每日 5 次审查，基础检查 |
| 专业版 | $24.99/月 | 无限审查，PR 生成，测试生成 |
| 团队版 | $79.99/月 | 团队协作，CI/CD 集成，自定义规则 |

## 开发优先级

- [x] 技能框架和文档
- [ ] 代码解析引擎
- [ ] AI 审查规则库
- [ ] PR 描述生成器
- [ ] 测试用例生成器
- [ ] GitHub 集成 (自动 PR)
- [ ] CI/CD 集成
- [ ] 自定义规则支持

## 依赖技能

- coding-agent (代码分析)
- github (PR 操作)

## 更新日志

### v0.1.0 (2026-03-14)
- 初始框架创建
- 完成 SKILL.md 和 README.md
- 设计审查规则和输出格式
