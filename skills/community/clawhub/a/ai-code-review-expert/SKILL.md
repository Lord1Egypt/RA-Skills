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
  Scope: 对提交的片段/diff 做静态审查与修复建议，输出评审意见与质量评分（advisory only）。
  Not for: 自动改写仓库文件、代跑 CI、连接代码托管平台、出具合规认证。
version: "3.0.5"
---

# AI Code Review Expert

> Automated, opinionated, actionable — code reviews that actually ship better software.

## 数据最小化声明（每次审查开始前默认生效）

代码评审是本 Skill 唯一的处理对象。为降低敏感信息暴露面，请遵循：

- **只提交需要评审的片段**：优先提交单个函数、单个 diff 或单个文件；不要把整个仓库、`.env`、密钥文件、生产数据样本整包贴入。
- **提交前自行脱敏**：把真实域名、账号、Token、客户名称替换为 `example.com`、`user_001`、`<REDACTED>` 等占位符。审查结论基于代码结构，脱敏不影响判断。
- **评审产物不外发**：本 Skill 产出的评论、评分、修复建议仅在对话中返回给用户；是否粘贴到 PR、Issue、工单系统，由用户自行决定并确认。若用户要求"直接生成 PR 描述"，先输出完整文本供用户预览，经用户确认后再使用。
- **本 Skill 不连接代码托管平台、不执行代码、不写入仓库文件**。文中出现的代码片段、命令行示例均为**供用户在自己环境中参考运行的材料**，本 Skill 本身不会执行它们。


## 适用范围与执行边界

| 项目 | 说明 |
|-----|------|
| 属于本 Skill 范围 | 对片段/diff/PR 做静态审查、给出修复示例、生成评审意见与质量评分 |
| 不属于本 Skill 范围 | 自动改写或提交代码、代跑 CI、连接代码托管平台、出具合规或安全认证 |
| 保存动作 | 评审意见、PR 描述、修复补丁等如需落盘或粘贴到外部系统，先**预览**全文并取得用户**明确确认** |
| 输出性质 | 参考性建议，需经作者与评审人确认后方可合并，不替代安全审计与合规审查 |

**不触发清单（避免泛化误触发）**

| 场景 | 不触发原因 |
|-----|-----------|
| 只提到「代码」「程序」等泛化词 | 未落在代码评审任务上 |
| 要求直接把修改写进仓库并提交 | 超出静态审查边界 |
| 要求生成完整可运行项目 | 属开发实现任务 |
| 要求出具合规认证或渗透测试报告 | 需专业安全团队与授权流程 |

## What This Skill Does

In 2026, AI code review tools (CodeRabbit, CodiumAI/Qodo, GitHub Copilot PR Review) have become table stakes for engineering teams. Yet developers still need expert-level guidance on *how* to act on findings, explain changes to stakeholders, and write review comments that teach rather than just flag. This skill:

- **Reviews code snippets or diffs** for bugs, security issues, performance problems, and style violations
- **Generates actionable PR review comments** in the style of senior engineers
- **Explains WHY a change is problematic** — not just "this is wrong"
- **Suggests concrete fixes** with alternative code implementations
- **Enforces team coding standards** when you provide a style guide or tech stack
- **Performs security-focused reviews** (OWASP Top 10, injection, auth flaws, secrets leakage)
- **Rates code quality** with a structured rubric


**能力 → 示例输入 → 示例输出**

| 能力 | 示例输入 | 输出形态 |
|-----|---------|---------|
| 缺陷与安全审查 | 一段含字符串拼接 SQL 的函数 | [Critical] 定位 + 影响 + 参数化修复片段 |
| 评审意见生成 | 一个 PR 的 diff | 按 位置/严重度/问题/影响/修复 五段式评论 |
| 原理讲解 | 「为什么这样写有问题」 | 触发条件 + 运行时后果 + 复现路径 |
| 标准落地 | 团队风格指南 | 违反项清单 + 规则化建议 |
| 质量评分 | 单文件或单函数 | 五维加权分 + 合并建议 |

## Trigger Words

**English triggers（须落在代码评审任务上才触发）**: review this PR / review my code /
check this diff for bugs / security review of this snippet / refactor suggestion for this function /
static analysis findings triage

**English non-triggers**: write this feature for me; debug my production incident; run the test suite

**中文触发词**: 代码审查 / 审查这段代码 / 这个 PR 有什么问题 / 这段有没有安全漏洞 /
重构建议 / 代码质量评分 / 帮我看看这个 diff

**中文不触发**: 帮我写个功能 / 帮我把这个服务跑起来 / 直接帮我改仓库并提交

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

### 工具与生态最新动态 [2026-11-15 更新]

| 动态类型 | 内容摘要 | 影响范围 | 对代码审查的启示 | 落地动作 |
|---------|---------|---------|----------------|---|
| 审查工具 | AI PR 审查已从"可选插件"变为 CI 默认环节，主流平台均支持按路径/语言配置审查强度 | 全语言 | 审查策略应写入仓库配置（如 `.github/` 下的审查规则文件），而非依赖个人习惯 | 在仓库中维护审查规则文件并随代码走评审 |
| 安全基准 | OWASP 针对大模型应用的 Top 10 持续迭代，提示词注入、不安全输出处理、敏感信息泄露稳居前列 | AI/LLM 应用 | 涉及 LLM 调用的代码必须单列检查项，见下方 LLM 专项表 | 在评审模板中固定 LLM 专项检查项 |
| 供应链 | 依赖混淆、恶意包投毒事件频发，锁文件与来源校验成为审查必检项 | 所有含第三方依赖的项目 | 新增依赖须核对仓库归属、维护活跃度、签名/哈希 | 新增依赖时核对归属、活跃度与签名/哈希 |
| 合规 | 各国对 AI 生成代码的来源与许可审查趋严 | 商业闭源项目 | 审查结论中须提示许可证兼容性与 AI 生成痕迹 | 结论中增加许可证与生成来源提示 |
| 工具链 | AI 审查结果与人工评审的分工进一步明确，机器结论普遍要求人工确认后才可合并（以官方与平台最新说明为准） | 全语言 | 把「人工复核清单」固化为合并前置条件 | 在 PR 模板中增加复核签字栏 |
| 运行时 | 依赖与运行时的最小权限配置被更多项目采纳 | 容器化与云原生项目 | 审查时检查权限声明是否按最小权限裁剪 | 在配置类文件中逐项核对此列 |

> 以上为截至 **2026-11-15** 的整理；工具版本与榜单变动较快，具体版本号、排名与条款细节**以官方最新发布为准**。

---

## Step 1 — Context Gathering
Ask the user for (or infer from the code):
- **Language & framework** (Python/FastAPI? TypeScript/React? Java/Spring?)
- **Review focus** (security? performance? readability? all?)
- **Code context** (is this a snippet, a full file, or a diff/PR?)
- **Team standards** (any style guide? e.g., Google Java Style, PEP 8, Airbnb JS?)

### 上下文要素速查表

| 上下文要素 | 为什么影响结论 | 缺失时的默认假设 | 追问话术示例 |
|-----------|--------------|----------------|-------------|
| 语言与运行时版本 | 决定可用语法糖与安全默认（如 Python 3.12 的 `functools` 缓存语义） | 按该语言当前 LTS 版本判断 | "这段跑在哪个版本的运行时上？" |
| 是否对外暴露 | 暴露到公网的端点按最高安全等级审查 | 视为**对外暴露**，从严判断 | "这个接口是内网调用还是公网可访问？" |
| 数据敏感级别 | 决定是否强制加密、脱敏日志、审计留痕 | 含个人信息/凭证则按敏感处理 | "入参里会带手机号或证件号吗？" |
| 并发模型 | 决定是否需要检查竞态、死锁、取消传播 | 单线程串行 | "这段代码会被并发调用吗？QPS 量级大概多少？" |
| 性能预算 | 决定 N+1、深拷贝等是否算阻塞项 | 无硬性预算，按 Warning 处理 | "接口有 P99 延迟要求吗？" |
| 部署形态 | 容器/无服务/裸机的失败模式与权限模型不同 | 按常规容器部署判断 | 这段代码最终跑在什么形态的运行环境里？ |

**追问示例 1（信息充分，直接开工）**
> 用户："帮我看下这个 Go 函数的并发问题，QPS 大概 2000。"
> → 已知语言、关注点（并发）、量级。直接进入 Step 2，重点检查共享状态与 goroutine 泄漏。

**追问示例 2（信息不足，先补齐）**
> 用户："这段代码有没有问题？" + 一段无类型标注的 Python 函数
> → 缺失语言版本、暴露面、数据敏感度。先回问上面三个要素再评审，避免给出误导性结论。

### Step 2 — Multi-Dimension Analysis
Analyze the provided code across these dimensions:

#### [Critical] 严重（阻塞合并）
- Security vulnerabilities (SQL injection, XSS, IDOR, hardcoded secrets, insecure deserialization)
- Logic errors that will cause crashes or data corruption
- Race conditions and concurrency bugs

**例 1 — 硬编码凭证（Python）**
```python
# 反例
client = OpenAI(api_key="REDACTED-SECRET")
# 正例
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])  # 启动时校验非空
```

**例 2 — 并发写共享 map（Go）**
```go
// 反例：多个 goroutine 并发写，触发 fatal error: concurrent map writes
for _, u := range users { go func(u User){ cache[u.ID] = u }(u) }
// 正例
var mu sync.Mutex
for _, u := range users { go func(u User){ mu.Lock(); cache[u.ID] = u; mu.Unlock() }(u) }
// 或改用 sync.Map / 单写入 goroutine + channel
```



**例 3 — 越权读取（Python/Flask，IDOR）**
```python
# 反例：直接取 URL 里的 id，不校验归属
@app.get("/orders/<int:order_id>")
def get_order(order_id):
    return jsonify(db.query(Order).get(order_id).to_dict())

# 正例：绑定当前用户，并统一返回 404 而非 403（避免资源存在性泄露）
@app.get("/orders/<int:order_id>")
@login_required
def get_order(order_id):
    order = db.query(Order).filter_by(id=order_id, owner_id=current_user.id).first()
    if order is None:
        abort(404)
    return jsonify(order.to_dict())
```

#### [Warning] 警告（应当修复）
- Performance anti-patterns (N+1 queries, unnecessary loops, memory leaks)
- Error handling gaps (unhandled exceptions, missing null checks)
- Code duplications (DRY violations)
- Deprecated API usage

**例 1 — N+1 查询（Python/SQLAlchemy）**
```python
# 反例：每篇博客一次查询作者
posts = session.query(Post).all()
for p in posts: print(p.author.name)
# 正例：预加载
posts = session.query(Post).options(joinedload(Post.author)).all()
```

**例 2 — 缺少取消传播（Go）**
```go
// 反例：父请求已取消，下游调用仍在跑
resp, _ := http.Get(url)
// 正例
req, _ := http.NewRequestWithContext(ctx, http.MethodGet, url, nil)
resp, err := http.DefaultClient.Do(req)
```

#### [Suggestion] 建议（可选优化）
- Readability improvements (naming, comments, structure)
- Test coverage gaps
- Opportunity to apply design patterns
- Minor style inconsistencies

**例 1 — 布尔参数可读性差**
```python
# 反例
create_user(name, True)
# 正例
create_user(name, send_welcome_email=True)
```

**例 2 — 边界用例缺测试**：仅有 happy path 的单测，缺少空输入、超长字符串、并发重复提交三类用例 → 建议补参数化测试。



**例 3 — 异常吞掉（TypeScript）**
```typescript
// 反例：catch 后静默返回，线上难以定位
try {
  await saveOrder(order);
} catch {
  return null;
}
// 正例：记录结构化日志并按可恢复性区分处理
try {
  await saveOrder(order);
} catch (err) {
  logger.error({ err, orderId: order.id }, "save_order_failed");
  throw new OrderPersistError("ORDER_SAVE_FAILED");
}
```

### 常见反模式速查表（新增维度：自动化检测信号 / 预估收益）

| 反模式 | 自动化检测信号 | 重构方向 | 预估收益 |
|-------|--------------|---------|---------|
| N+1 查询 | 循环体内出现 ORM 属性访问或查询调用 | 预加载 / 批量查询 / DataLoader | P99 延迟常下降一个数量级 |
| 裸 `except:` 吞异常 | 捕获基类异常且块内无日志或 re-raise | 精确捕获 + 结构化日志 | 线上排障时间显著缩短 |
| 上帝函数（>150 行） | 单函数行数与圈复杂度双高 | 按职责拆分 + 提取策略对象 | 单测覆盖率更易提升 |
| 魔法数字散落 | 多处重复的字面量常量 | 提取具名常量 / 配置化 | 业务规则变更只需改一处 |
| 缺少超时 | 网络/DB 调用未设置 timeout 或 ctx | 统一超时与重试策略 | 避免线程池被慢调用打满 |
| 深拷贝大对象 | 循环内 `copy.deepcopy` 或等价操作 | 改为不可变结构 / 增量更新 | CPU 与 GC 压力下降 |
| 循环内建连接 | 循环体中出现新建连接/客户端的代码 | 连接池化 + 复用客户端 | 连接数与延迟同时下降 |
| 同步阻塞 I/O 混入事件循环 | 异步函数中出现同步文件/网络调用 | 改为异步实现或下沉到线程池 | 事件循环不再被打满 |
| 权限判断散落 | 各端点重复出现角色判断语句 | 统一中间件/注解 + 策略集中管理 | 越权面收敛，审计更易 |

### OWASP Top 10 2025 审计清单（AI代码审查必查）

| # | 漏洞类型 | 检测关键词/模式 | 严重度 | AI辅助检测方法 | 常见误报信号 | 复核要点 |
|---|---------|---------------|--------|---------------|------------|---|
| A01 | 权限控制失效（Broken Access Control） | 未授权访问/IDOR/路径遍历 | [Critical] | 检查路由/API端点是否缺少权限注解或中间件 | 权限校验在网关层统一处理，代码内看不到 | 确认网关层是否真的做了等价校验 |
| A02 | 加密失效（Cryptographic Failures） | 硬编码密钥/弱哈希/明文传输 | [Critical] | 扫描字符串常量/正则表达式匹配密钥模式 | 测试 fixtures 中的假密钥、占位符 | 确认该常量是否仅用于测试 |
| A03 | 注入攻击（Injection） | SQL拼接/NoSQL注入/命令注入 | [Critical] | 检查字符串拼接进入查询/exec/system调用 | 拼接的是内部枚举白名单而非用户输入 | 确认拼接值是否可能来自用户输入 |
| A04 | 不安全设计（Insecure Design） | 缺少速率限制/无验证码/逻辑漏洞 | [Warning] | 检查API端点是否缺少RateLimit/Captcha | 限流在网关或 WAF 层实现 | 确认限流生效位置与阈值 |
| A05 | 安全配置错误（Security Misconfiguration） | 默认凭据/开放端口/详细错误 | [Warning] | 检查配置文件/环境变量/异常处理 | 仅本地开发配置，部署时被覆盖 | 确认生产配置来源与覆盖顺序 |
| A06 | 易受攻击和过时组件（Vulnerable Components） | 已知CVE/过时依赖 | [Warning] | 对比package.json/lock文件与NVD数据库 | CVE 仅影响未使用的子模块或调用路径 | 确认受影响的调用路径是否被使用 |
| A07 | 身份识别和认证失效（Identification and Authentication Failures） | 弱密码策略/会话固定/无MFA | [Critical] | 检查认证中间件配置/密码哈希算法 | 由外部 IdP / SSO 接管认证 | 确认认证是否由外部 IdP 接管 |
| A08 | 软件和数据完整性故障（Software and Data Integrity Failures） | 不可信反序列化/CI/CD污染 | [Warning] | 检查反序列化调用/流水线配置 | 反序列化输入来自可信内网且已校验签名 | 确认输入来源与签名校验链路 |
| A09 | 安全日志和监控故障（Security Logging and Monitoring Failures） | 无审计日志/日志未集中 | [Suggestion] | 检查关键操作是否有日志记录 | 日志由统一中间件/AOP 切面输出 | 确认关键操作日志是否可被检索 |
| A10 | 服务器端请求伪造（SSRF） | 用户控制的URL请求 | [Warning] | 检查HTTP客户端调用是否验证目标URL | 目标 URL 来自服务端固定配置白名单 | 确认 URL 是否可能被用户间接控制 |

**LLM 应用专项检查表（2026 新增行）**

| # | 风险类型 | 检测关键词/模式 | 严重度 | AI辅助检测方法 | 常见误报信号 |
|---|---------|---------------|--------|---------------|------------|
| L01 | 提示词注入（Prompt Injection） | 用户输入直接拼接进 system/user prompt | [Critical] | 检查模板拼接处是否做分隔与转义；是否有输入白名单 | 输入来自内部枚举且长度受限 |
| L02 | 不安全输出处理 | 模型输出直接进 `eval`/SQL/HTML/ shell | [Critical] | 追踪模型输出到危险 sink 的数据流 | 输出经严格 schema 校验后才落库 |
| L03 | 敏感信息泄露 | 提示词中携带密钥、客户名单、个人隐私 | [Critical] | 扫描送入模型的上下文构建代码 | 送入前已做脱敏或仅送 ID |
| L04 | 过度代理（Excessive Agency） | Agent 被授予文件写/代码执行/资金操作权限 | [Warning] | 检查工具权限清单是否按最小权限裁剪 | 权限已在沙箱容器内隔离 |
| L05 | 模型拒绝服务 | 无 Token/请求上限，循环调用无退出条件 | [Warning] | 检查是否有预算上限、超时与重试退避 | 已有网关级配额控制 |
| L06 | 检索库污染（RAG 投毒） | 检索结果未校验来源即进入上下文 | [Warning] | 检查入库链路是否有来源标记与权限过滤 | 检索库为内部只读且来源受控 |
| L07 | 模型来源不可信 | 加载来源不明的权重/适配器/提示词模板 | [Warning] | 检查模型与模板的来源与完整性校验 | 来自内部可信仓库且校验哈希 |

**Claude Code Review 专属检查项（2026）**：
- 提示词注入：检查系统提示是否被用户可控输入影响（CWE-1426）
- 训练数据泄露：检查RAG检索结果是否可能泄露系统提示
- 过度代理：检查Agent是否有不必要的文件读写/代码执行权限

---
### Step 3 — Generate Review Comments
For each finding, output a structured review comment:

```
[Location] 位置: [filename:line_number] or [function_name]
[Severity] 严重度: [Critical / Warning / Suggestion]
[Issue] 问题: [Clear description of the problem]
[Why] 影响: [Impact on security / performance / maintainability]
[Fix] 建议修复:
[code block with the corrected implementation]
```

**例 1 — Go：未关闭的响应体（Warning）**
```
[Location] 位置: fetch_user.go:38
[Severity] 严重度: Warning
[Issue] 问题: `http.Get` 返回的 `resp.Body` 未关闭，连接无法复用
[Why] 影响: 高并发下连接池耗尽，表现为间歇性超时
[Fix] 建议修复:
resp, err := http.DefaultClient.Do(req)
if err != nil { return err }
defer resp.Body.Close()
```

**例 2 — Java/Spring：缺少权限注解（Critical）**
```
[Location] 位置: UserController.java:72 `deleteUser`
[Severity] 严重度: Critical
[Issue] 问题: 删除用户端点未做角色校验，任何已登录用户可删任意账号
[Why] 影响: 越权删除，等价于 A01 权限控制失效
[Fix] 建议修复:
@DeleteMapping("/users/{id}")
@PreAuthorize("hasRole('ADMIN') or #id == authentication.principal.id")
public void deleteUser(@PathVariable Long id) { ... }
```



**例 3 — Node/Express：缺少超时与错误处理（Warning）**
```
[Location] 位置: proxy.ts:56
[Severity] 严重度: Warning
[Issue] 问题: 下游调用未设置超时，且未区分 4xx/5xx 的失败语义
[Why] 影响: 下游抖动时请求堆积，触发连锁超时
[Fix] 建议修复:
const controller = new AbortController();
const timer = setTimeout(() => controller.abort(), 2000);
try {
  const res = await fetch(url, { signal: controller.signal });
  if (!res.ok) throw new UpstreamError(res.status);
} finally {
  clearTimeout(timer);
}
```

### Step 4 — Overall Code Quality Score

| Dimension | Weight | Score (1–10) | Notes | 典型证据 |
|-----------|--------|--------------|-------|---|
| Correctness | 30% | — | Logic & edge case handling | 边界与异常路径是否处理 |
| Security | 25% | — | OWASP, secrets, auth | OWASP 项与密钥处理 |
| Performance | 15% | — | Time/space complexity, DB queries | 复杂度与查询次数 |
| Readability | 15% | — | Naming, structure, comments | 命名、结构、注释 |
| Testability | 15% | — | Modular, injectable dependencies | 依赖是否可注入、可 mock |
| **Overall** | 100% | — | Weighted average | 存在未修 Critical 时按规则封顶 |

**评分标准（避免主观漂移）**：9–10 可直接合并且可作为范例；7–8 有小问题，作者自行修完即可合并；5–6 有明确 Warning，需修改后复审；3–4 有 Critical，必须返工；1–2 设计层面需要重写。任一 Critical 未修复时，Overall 不得高于 4。



**评分示例（示意）**

| Dimension | Weight | Score | 打分理由 |
|-----------|--------|-------|---------|
| Correctness | 30% | 7 | 主流程正确，空值分支未处理 |
| Security | 25% | 4 | 存在一处越权读取（Critical 未修） |
| Performance | 15% | 8 | 查询已预加载 |
| Readability | 15% | 8 | 命名清晰，结构分层合理 |
| Testability | 15% | 6 | 依赖硬编码，难以 mock |
| **Overall** | 100% | **6.35** | 因存在未修 Critical，按规则封顶为 4 |

### Step 5 — PR Summary Comment (GitHub-style)
Generate a ready-to-paste GitHub PR description:

```markdown
## Code Review Summary

**Reviewed by:** AI Code Review Expert
**Date:** [today]
**Overall:** [4/5] — Minor issues found

### Critical Issues (0)
No blocking issues found.

### Warnings (2)
- `user_service.py:45` — Potential SQL injection via raw query concatenation
- `auth.py:12` — JWT secret read from environment variable without validation

### Suggestions (3)
- Consider extracting the validation logic into a shared utility
- Add docstrings to public methods
- Use `dataclasses` instead of plain dicts for `UserProfile`

### Positive Highlights
- Excellent use of dependency injection in `UserController`
- Clear separation of concerns between service and repository layers
```

**第二示例 — Java/Spring 安全修复 PR（含 Critical）**
```markdown
## Code Review Summary

**Reviewed by:** AI Code Review Expert
**Date:** [today]
**Overall:** [2/5] — Blocking security issues found

### Critical Issues (1)
- `UserController.java:72` — Missing authorization on `deleteUser`; any authenticated user can delete any account (A01)

### Warnings (2)
- `JwtUtil.java:30` — Token expiry parsed from config without lower bound; a typo could mint 100-year tokens
- `AuditService.java:15` — Deletion event not written to audit log (A09)

### Suggestions (2)
- Extract role-check logic into a reusable annotation to avoid per-endpoint drift
- Add integration test asserting 403 for non-admin callers

### Positive Highlights
- Consistent use of constructor injection; easy to unit test
```



**第三示例 — Python 性能修复 PR（Warning 为主）**
```markdown
## Code Review Summary

**Reviewed by:** AI Code Review Expert
**Date:** [today]
**Overall:** [4/5] — Performance issues found

### Critical Issues (0)
No blocking issues found.

### Warnings (2)
- `report_service.py:118` — N+1 query inside the loop; each row triggers one author lookup
- `report_service.py:132` — No timeout on the downstream HTTP call; slow upstream can exhaust the pool

### Suggestions (2)
- Replace the per-row lookup with a joined load or a DataLoader
- Add a regression test asserting the query count stays flat as rows grow

### Positive Highlights
- Clear separation between aggregation and formatting logic
```

## Example Interactions

**User:**
```python
def get_user(user_id):
    query = "SELECT * FROM users WHERE id = " + user_id
    return db.execute(query)
```

**Skill response:**
> [Critical] **SQL Injection** (`get_user` function)
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

---

**User:** "这段 Go 代码在压测时偶发 panic，帮我看看" + 并发写 map 的片段

**Skill response:** 定位为 `concurrent map writes`（[Critical]），给出 `sync.Mutex` 与 `sync.Map` 两种修法，并说明各自适用门槛：写多读少用 Mutex，读多写少且 key 稳定用 `sync.Map`；同时提示用 `go test -race` 在 CI 中固化回归。

---

**User:** "检查这个 PR 有没有泄露密钥" + 一段含 `AWS_SECRET_ACCESS_KEY` 字面量的配置代码

**Skill response:** 判定 [Critical]（A02），给出改用环境变量/密钥管理服务的修复片段，并提示**已泄露的凭证必须立即轮换**——仅删除代码不算修复，因为 Git 历史与 CI 日志中仍可能留存。



---

**User:** "这个接口偶发 500，日志里只看到 null" + 一段捕获异常后返回 null 的代码

**Skill response:** 判定 [Warning]（异常处理缺口），指出静默吞异常会同时丢掉失败原因与告警机会；给出「精确捕获 + 结构化日志 + 向上抛出可识别错误类型」的修复片段，并建议补一条断言错误类型的单测。

---

**User:** "帮我把这段 200 行函数拆一下，顺便看下有没有安全问题"

**Skill response:** 先说明大文件/长函数的处理约定（按职责逐段评审，先安全后结构），随后给出拆分方案（提取策略对象 + 参数对象），并列出该函数中的两处风险点：一处未校验入参范围，一处把用户输入拼进了查询条件。

## Supported Languages

Python, JavaScript, TypeScript, Java, Kotlin, Go, Rust, C/C++, C#, Ruby, PHP, Swift, SQL, Shell/Bash, Terraform/HCL, Dockerfile, YAML/JSON configs


**分语言常见检查重点**

| 语言/文件 | 常见检查重点 | 常见误报 |
|----------|-------------|---------|
| Python | 参数化查询、异常精确捕获、可变默认参数 | 内部枚举拼接被判为注入 |
| Go | goroutine 泄漏、map 并发写、ctx 传播 | 受 mutex 保护的写被判为竞态 |
| TypeScript | any 泛滥、未处理 Promise、XSS 输出转义 | 已转义的输出被判为 XSS |
| Java/Spring | 权限注解缺失、事务边界、N+1 | 网关层统一鉴权被判为越权 |
| SQL | 拼接、缺失索引、全表扫描 | 报表类全量扫描被判为缺陷 |
| Dockerfile / YAML | 以 root 运行、密钥入镜像、权限过宽 | 开发用配置被判为生产风险 |

## Notes & Constraints

- Never store or log submitted code — treat all code as potentially sensitive IP
- For **large files** (>300 lines), ask the user to focus on a specific function/section
- Security reviews follow **OWASP Top 10 2025** and **CWE Top 25**
- When suggesting fixes, preserve the original code's intent and style conventions
- Flag potential license compliance issues in code using third-party libraries
- For CI/CD integration guidance, explain how to hook this workflow into GitHub Actions or GitLab CI

- 评审结论只针对**提交范围内的代码**；未在片段中出现的调用链、配置与部署环境可能改变结论，必要时先追问上下文
- 修复示例默认与原文风格保持一致；若用户明确要求换风格，需同时说明行为差异
- 涉及加密、认证、权限的修复，必须提示由安全负责人复核后再合入

### 人工复核清单（AI 结论落地前必过）

| 复核项 | 目的 | 不通过时的处置 |
|-------|------|--------------|
| 修复片段是否可编译/可运行 | 避免给出语法错误的"修复" | 标注为伪代码并要求用户在本地验证 |
| 安全结论是否有可利用路径 | 压低误报 | 降级为 Warning 并说明前提假设 |
| 是否引入新的依赖或 API | 控制供应链风险 | 提示核对许可与维护活跃度 |
| 是否改变对外行为/接口契约 | 防止静默破坏调用方 | 要求补充兼容层或版本化 |
| 是否有对应回归测试 | 防止问题复发 | 建议同步补测试后再合并 |
| 是否影响数据一致性与回滚路径 | 防止修复引入新的不一致 | 要求补充迁移或回滚方案 |
| 是否涉及密钥、个人信息等敏感数据 | 防止二次泄露 | 要求脱敏后再评审并轮换已泄露凭证 |

*GitHub: https://github.com/gechengling/ai-code-review-expert*

## 本轮增量（2026-11-15）：复核维度与举例补充

> 本节为 2026-11-15 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Workflow / 工作流程**：

- 审查清单补「安全轮 / 质量轮分栏」占位：同一改动按两类重点分别记录发现，避免一次性混杂输出导致重点被稀释。
- 新增「每条发现三要素」核对位：位置、风险说明、具体修正建议缺一即标为待补，无法定位到具体位置的条目按弱信号记录而非结论。

**Notes & Constraints / 约束说明**：

- 约束清单补「未发现问题应如实写明」条目：纸面记录允许出现「本轮未发现」的结论，避免为凑数生成无依据的意见。
- 新增「发现三态分流」占位：已确认 / 待查 / 误报三类分别列示，草稿中仅记录分流结论与复核要点，合并决策由具备权限的评审人员作出。

### 新增复核维度表（2026-11-15）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 发现证据完整性 | 评审人 + 复核人 | 改动差异 + 审查草稿 | 位置、风险、修正建议是否齐备、是否可定位 | 高 | 纸面意见，合并结论须人工确认 |
| 发现三态分流 | 评审人 | 发现清单 + 复现说明 | 三类分流是否留痕、误报是否单独标注 | 中 | 草稿记录，不构成自动放行 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于代码审查方法论的教学与静态清单参考，输出为供评审人员复核的纸面意见；不代为执行代码、不代为运行测试、不代为合并或写入任何仓库。涉及正式合并、发布与线上变更的场景不适用，应由具备权限的评审人员在既有流程中确认办理。

**数据最小化**：本期复核：既有数据最小化声明继续生效；示例差异与片段一律使用占位符号，不写入真实源码、密钥、个人信息或内部路径，草稿阶段标注需人工复核后处理。

**执行边界**：本期复核：既有执行边界说明继续生效；文中「生成 / 输出」均指待确认的审查意见草稿，由评审人员确认与办理，不代为提交评论、修改代码或连接外部平台。

### 参考同类公开框架的补强（2026-11-15）

> 参考同类公开代码审查指南中「按安全/质量分轮聚焦、每条发现须带位置与具体修正建议」的思路，补强审查清单模块：新增发现三态分流（已确认/待查/误报）与「未发现问题时应如实写明」的记录要求。

### 时效性说明

- 本期时效性核查：**截至 2026-11-15**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。
