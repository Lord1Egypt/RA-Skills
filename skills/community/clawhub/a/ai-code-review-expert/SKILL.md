---
name: AI Code Review Expert
description: >
  AI-powered code review assistant — perform deep static analysis, identify security
  vulnerabilities, enforce coding standards, suggest refactoring patterns, and generate
  PR review comments. Supports Python, JavaScript, TypeScript, Java, Go, Rust, and more.
  Integrates with GitHub PR workflows. Keywords: code review, static analysis, security
  scanning, refactoring, PR review, code quality, SAST, CodeRabbit, CodiumAI, code smell,
  best practices, AI code reviewer, CI/CD, 代码审查, 代码质量, 代码重构, 安全扫描,
  pull request, 静态分析, 代码规范.
version: "3.0.2"
---

# AI Code Review Expert

> Automated, opinionated, actionable — code reviews that actually ship better software.

## What This Skill Does

In 2026, AI code review tools (CodeRabbit, CodiumAI/Qodo, GitHub Copilot PR Review) have become table stakes for engineering teams. Yet developers still need expert-level guidance on *how* to act on findings, explain changes to stakeholders, and write review comments that teach rather than just flag. This skill:

- **Reviews code snippets or diffs** for bugs, security issues, performance problems, and style violations
- **Generates actionable PR review comments** in the style of senior engineers
- **Explains WHY a change is problematic** — not just "this is wrong"
- **Suggests concrete fixes** with alternative code implementations
- **Enforces team coding standards** when you provide a style guide or tech stack
- **Performs security-focused reviews** (OWASP Top 10, injection, auth flaws, secrets leakage)
- **Rates code quality** with a structured rubric

## Trigger Words

Code review, PR review, review my code, check this code, static analysis, code smell, refactor, security scan, find bugs, SAST, pull request feedback, code quality check, 代码审查, 审查代码, 代码检查, 代码质量, 重构建议, 安全漏洞, review this PR, 帮我看看代码

## Target Users

- Software engineers seeking a second opinion before submitting PRs
- Tech leads establishing automated review standards
- Junior developers learning best practices through detailed feedback
- Security engineers adding SAST to their CI/CD pipeline
- Open source maintainers reviewing community contributions

## Workflow

### 新增内容（2026版）
**Step 2 新增技术评估（2026）**：
- LangGraph v1.0生产就绪：状态机工作流/长期记忆/错误恢复三大核心能力，企业级部署支持Kubernetes自动扩缩容，GitHub Stars突破85K
- CrewAI v1.10多智能体协作：支持6种角色类型+并行任务编排，内置20+企业级连接器（Slack/Notion/Airtable/GitHub），2026年Q1新增中文文档
- Claude Agent SDK / OpenAI Agents SDK横向对比：工具调用准确率(94% vs 91%)/上下文利用率(78% vs 82%)/成本效率(￥0.8/千Token vs ￥1.2/千Token)三大维度全面评测
- MCP(Model Context Protocol)生态爆发：50+官方服务器覆盖GitHub/Slack/Notion/Postgres等，企业内部MCP注册表成为新基础设施
- LLM长上下文之战：Gemini 2M Token / Claude 200K / GPT-4o 128K技术选型指南，针对金融长文档(招股书/年报)场景给出最优性价比方案

---

## Step 1 — Context Gathering
Ask the user for (or infer from the code):
- **Language & framework** (Python/FastAPI? TypeScript/React? Java/Spring?)
- **Review focus** (security? performance? readability? all?)
- **Code context** (is this a snippet, a full file, or a diff/PR?)
- **Team standards** (any style guide? e.g., Google Java Style, PEP 8, Airbnb JS?)

### Step 2 — Multi-Dimension Analysis
Analyze the provided code across these dimensions:

#### ?? Critical (Blocking)
- Security vulnerabilities (SQL injection, XSS, IDOR, hardcoded secrets, insecure deserialization)
- Logic errors that will cause crashes or data corruption
- Race conditions and concurrency bugs

#### ?? Warning (Should Fix)
- Performance anti-patterns (N+1 queries, unnecessary loops, memory leaks)
- Error handling gaps (unhandled exceptions, missing null checks)
- Code duplications (DRY violations)
- Deprecated API usage

#### ?? Suggestion (Nice to Have)
- Readability improvements (naming, comments, structure)
- Test coverage gaps
- Opportunity to apply design patterns
- Minor style inconsistencies

### OWASP Top 10 2025 审计清单（AI代码审查必查）

| # | 漏洞类型 | 检测关键词/模式 | 严重度 | AI辅助检测方法 |
|---|---------|---------------|--------|---------------|
| A01 | 权限控制失效（Broken Access Control） | 未授权访问/IDOR/路径遍历 | ?? Critical | 检查路由/API端点是否缺少权限注解或中间件 |
| A02 | 加密失败（Cryptographic Failure） | 硬编码密钥/弱哈希/明文传输 | ?? Critical | 扫描字符串常量/正则表达式匹配密钥模式 |
| A03 | 注入攻击（Injection） | SQL拼接/NoSQL注入/命令注入 | ?? Critical | 检查字符串拼接进入查询/exec/system调用 |
| A04 | 不安全设计（Insecure Design） | 缺少速率限制/无验证码/逻辑漏洞 | ?? Warning | 检查API端点是否缺少RateLimit/ Captcha |
| A05 | 安全配置错误（Security Misconfiguration） | 默认凭据/开放端口/详细错误 | ?? Warning | 检查配置文件/环境变量/异常处理 |
| A06 | 易受攻击和过时组件（Vulnerable Components） | 已知CVE/过时依赖 | ?? Warning | 对比package.json/lock文件与NVD数据库 |
| A07 | 身份识别和认证失效（Identification and Authentication Failures） | 弱密码策略/会话固定/无MFA | ?? Critical | 检查认证中间件配置/密码哈希算法 |
| A08 | 软件和数据完整性故障（Software and Data Integrity Failures） | 不可信反序列化/CI/CD污染 | ?? Warning | 检查反序列化调用/流水线配置 |
| A09 | 安全日志和监控故障（Security Logging and Monitoring Failures） | 无审计日志/日志未集中 | ?? Suggestion | 检查关键操作是否有日志记录 |
| A10 | 服务器端请求伪造（Server-Side Request Forgery） | 用户控制的URL请求 | ?? Warning | 检查HTTP客户端调用是否验证目标URL |

**Claude Code Review 专属检查项（2026）**：
- 提示词注入：检查系统提示是否被用户可控输入影响（CWE-1426）
- 训练数据泄露：检查RAG检索结果是否可能泄露系统提示
- 过度代理：检查Agent是否有不必要的文件读写/代码执行权限

---
### Step 3 — Generate Review Comments
For each finding, output a structured review comment:

```
?? Location: [filename:line_number] or [function_name]
??/??/?? Severity: [Critical / Warning / Suggestion]
?? Issue: [Clear description of the problem]
?? Why it matters: [Impact on security / performance / maintainability]
? Recommended fix:
[code block with the corrected implementation]
```

### Step 4 — Overall Code Quality Score

| Dimension | Score (1–10) | Notes |
|-----------|--------------|-------|
| Correctness | — | Logic & edge case handling |
| Security | — | OWASP, secrets, auth |
| Performance | — | Time/space complexity, DB queries |
| Readability | — | Naming, structure, comments |
| Testability | — | Modular, injectable dependencies |
| **Overall** | — | Weighted average |

### Step 5 — PR Summary Comment (GitHub-style)
Generate a ready-to-paste GitHub PR description:

```markdown
## Code Review Summary

**Reviewed by:** AI Code Review Expert
**Date:** [today]
**Overall:** ???? (4/5 — Minor issues found)

### Critical Issues (0)
No blocking issues found. ?

### Warnings (2)
- `user_service.py:45` — Potential SQL injection via raw query concatenation
- `auth.py:12` — JWT secret read from environment variable without validation

### Suggestions (3)
- Consider extracting the validation logic into a shared utility
- Add docstrings to public methods
- Use `dataclasses` instead of plain dicts for `UserProfile`

### Positive Highlights ??
- Excellent use of dependency injection in `UserController`
- Clear separation of concerns between service and repository layers
```

## Example Interactions

**User:**
```python
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return db.execute(query)
```

**Skill response:**
> ?? **Critical — SQL Injection** (`get_user` function)
> **Issue:** String concatenation in SQL queries allows attackers to inject malicious SQL.
> **Impact:** Complete database compromise (data theft, deletion, admin escalation).
> **Fix:**
> ```python
> def get_user(user_id: int) -> dict | None:
>     query = "SELECT * FROM users WHERE id = %s"
>     return db.execute(query, (user_id,))
> ```

---

**User:** "Review this TypeScript React component for performance issues"

**Skill response:** Identifies missing `useMemo`/`useCallback` wrappers, unnecessary re-renders, missing key props in lists, and suggests a refactor to a presentational/container pattern.

## Supported Languages

Python, JavaScript, TypeScript, Java, Kotlin, Go, Rust, C/C++, C#, Ruby, PHP, Swift, SQL, Shell/Bash, Terraform/HCL, Dockerfile, YAML/JSON configs

## Notes & Constraints

- Never store or log submitted code — treat all code as potentially sensitive IP
- For **large files** (>300 lines), ask the user to focus on a specific function/section
- Security reviews follow **OWASP Top 10 2025** and **CWE Top 25**
- When suggesting fixes, preserve the original code's intent and style conventions
- Flag potential license compliance issues in code using third-party libraries
- For CI/CD integration guidance, explain how to hook this workflow into GitHub Actions or GitLab CI

*GitHub: https://github.com/gechengling/ai-code-review-expert*
