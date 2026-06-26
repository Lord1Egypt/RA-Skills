# 🔍 Code Health Report

> **生成时间:** 2026-05-18 11:30 CST
> **扫描范围:** `src/` (1,247 个文件 | 89,632 行代码)
> **扫描引擎:** Code Health Scanner v1.2.0

---

## Report Metadata

| 元数据项 | 值 |
|---------|-----|
| **项目名称** | OnlineExamSystem |
| **扫描分支** | `feature/exam-module` |
| **最新提交** | `a3f2b9c` — "fix: 修复选择题答案校验越界问题" |
| **扫描时间** | 2026-05-18 11:30:02 |
| **耗时** | 3.2s |
| **扫描规则数** | 48 条 |
| **对比基准** | `main` (2026-05-17 扫描) |

---

## Health Score Gauge

```
┌────────────────────────────────────────────╮
│                                            │
│              ████████░░░░                  │
│              ██  78/100  ██                │
│              ████████░░░░                  │
│          ⚠️ 需要关注 · 可提升空间大          │
│                                            │
│   ┌──────┬──────┬──────┬──────┬──────┐     │
│   │  0   │  25  │  50  │  75  │ 100  │     │
│   └──────┴──────┴──────┴──────┴──────┘     │
│    🔴危急    🟠较差    🟡一般    🟢良好    🟢优秀   │
│                                            │
╰────────────────────────────────────────────┘
```

### 评分说明

| 等级 | 分数区间 | 含义 |
|------|---------|------|
| 🟢 **优秀** | 90–100 | 代码质量高，可安全交付 |
| 🟢 **良好** | 75–89 | 少量问题，建议修复后合并 |
| 🟡 **一般** | 60–74 | 存在较多问题，建议修复后再发布 |
| 🟠 **较差** | 40–59 | 存在严重问题，必须修复 |
| 🔴 **危急** | 0–39 | 代码不可用，需全面重构 |

#### 评分公式

```
Health Score = MAX(0, 100 - (critical_weight + warning_weight + info_weight))

其中：
  critical_weight = critical_count × 10
  warning_weight  = warning_count  × 3
  info_weight     = info_count     × 0.5

总量惩罚 = MIN(weight_total × 0.1, 20)  // 文件量大时最多扣 20 分
```

**评分示例：**

```
场景 A：0 critical + 2 warning + 8 info
  → 100 - (0 × 10 + 2 × 3 + 8 × 0.5)
  → 100 - (0 + 6 + 4)
  → 90  ✅ 优秀

场景 B：3 critical + 12 warning + 25 info
  → 100 - (3 × 10 + 12 × 3 + 25 × 0.5)
  → 100 - (30 + 36 + 12.5)
  → 21.5 → 22  🔴 危急

场景 C：1 critical + 6 warning + 15 info, 文件量 = 1247
  → 100 - (10 + 18 + 7.5) = 64.5
  → 总量惩罚 = MIN(35.5 × 0.1, 20) = MIN(3.55, 20) = 3.55
  → 64.5 - 3.55 ≈ 61  🟡 一般
```

---

## Issue Distribution

| 严重级别 | 数量 | 占比 | 本周期变化 |
|----------|------|------|-----------|
| 🔴 **Critical** | 3 | 5.2% | +1 (新增) |
| 🟠 **Warning** | 12 | 20.7% | −3 ↓ |
| ℹ️ **Info** | 43 | 74.1% | +5 ↑ |
| **总计** | **58** | **100%** | **+3 ↑** |

### 按类别分布

| 类别 | Critical | Warning | Info | 合计 |
|------|----------|---------|------|------|
| ❌ 错误处理 | 2 | 3 | 5 | 10 |
| 🔐 安全漏洞 | 1 | 2 | 4 | 7 |
| ⚡ 性能问题 | 0 | 3 | 8 | 11 |
| 📐 代码风格 | 0 | 0 | 12 | 12 |
| 🧪 测试覆盖 | 0 | 2 | 6 | 8 |
| 📦 依赖问题 | 0 | 2 | 8 | 10 |
| **合计** | **3** | **12** | **43** | **58** |

---

## 🔴 Critical Issues

> 必须立即修复，可能引发系统故障或安全漏洞。

### CRIT-001: SQL 注入风险 — `UserController.java:47`

```java
// ❌ 危险：直接拼接 SQL 字符串
String sql = "SELECT * FROM users WHERE username = '" + username + "'";
```

- **文件:** `src/main/java/com/exam/controller/UserController.java`
- **行号:** 47
- **规则:** `security/sql-injection` (严重度: critical)
- **检测时间:** 2026-05-18 11:30:01

**✅ 修复建议：**

```java
// ✅ 安全：使用参数化查询
String sql = "SELECT * FROM users WHERE username = ?";
// 或使用 JPA / MyBatis 的内置参数绑定
```

**🔗 相关资源：**
- [OWASP SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)

---

### CRIT-002: 空指针风险 — `ExamService.java:102`

```java
// ❌ 危险：未判空直接调用
return examService.findById(examId).getQuestions();
```

- **文件:** `src/main/java/com/exam/service/ExamService.java`
- **行号:** 102
- **规则:** `null-safety/dereference` (严重度: critical)
- **检测时间:** 2026-05-18 11:30:01

**✅ 修复建议：**

```java
// ✅ 安全：判空 + 异常或 Optional
Optional<Exam> exam = examService.findById(examId);
return exam.map(Exam::getQuestions)
           .orElseThrow(() -> new ExamNotFoundException(examId));
```

---

### CRIT-003: 硬编码密码 — `application-dev.properties:25`

```properties
# ❌ 危险：明文密码硬编码
spring.datasource.password=admin123
```

- **文件:** `src/main/resources/application-dev.properties`
- **行号:** 25
- **规则:** `security/hardcoded-secret` (严重度: critical)

**✅ 修复建议：**

```properties
# ✅ 安全：使用环境变量或密钥管理服务
spring.datasource.password=${DB_PASSWORD}
```

---

## 🟠 Warning Issues

> 建议在下一轮迭代中修复，长期积累会降低代码可维护性。

### WARN-001: 未使用的方法参数 — `PaperController.java:135`

```java
public ResultVO createPaper(@RequestBody CreatePaperDTO dto, HttpServletRequest request) {
    // request 参数未被使用
}
```

- **文件:** `src/main/java/com/exam/controller/PaperController.java`
- **行号:** 135
- **规则:** `java/unused-parameter` (严重度: warning)
- **标签:** `dead-code`

**✅ 修复建议：** 移除未使用的参数，或添加 `@SuppressWarnings("unused")` 注解（如确为框架需求）。

---

### WARN-002: 大循环内执行 SQL 查询 — `ExamServiceImpl.java:210`

```java
for (Long questionId : questionIds) {
    Question q = questionMapper.selectById(questionId); // N+1 查询
    result.add(q);
}
```

- **文件:** `src/main/java/com/exam/service/impl/ExamServiceImpl.java`
- **行号:** 210–213
- **规则:** `performance/n-plus-one` (严重度: warning)
- **复杂度:** 3 处相似模式

**✅ 修复建议：** 使用 `IN` 查询代替循环单条查询：

```java
List<Question> questions = questionMapper.selectBatchIds(questionIds);
result.addAll(questions);
```

---

### WARN-003: 未处理的异常 — `FileUploadService.java:78`

- **文件:** `src/main/java/com/exam/service/FileUploadService.java`
- **行号:** 78
- **规则:** `error-handling/uncaught-exception` (严重度: warning)

**✅ 修复建议：** 添加 try-catch 或 throws 声明，记录错误日志并返回友好的错误消息。

---

### WARN-004 ~ WARN-012

> 完整列表见 `E:\A工作文档\skills\code-health-scanner\reports\2026-05-18_warnings.json`

| # | 文件 | 行号 | 规则 | 标签 |
|---|------|------|------|------|
| 4 | `ExamDTO.java` | 32 | `naming/convention` | `style` |
| 5 | `RedisConfig.java` | 17 | `performance/unbounded-cache` | `performance` |
| 6 | `SecurityConfig.java` | 44 | `security/csrf-disabled` | `security` |
| 7 | `QuestionMapper.xml` | 89 | `mybatis/slow-query` | `performance` |
| 8 | `GradeController.java` | 55 | `architecture/tight-coupling` | `design` |
| 9 | `ExamServiceImpl.java` | 301 | `code-smell/long-method` (45行) | `design` |
| 10 | `pom.xml` | 78 | `dependency/outdated` | `deps` |
| 11 | `logback.xml` | 5 | `config/hardcoded-path` | `config` |
| 12 | `ExamServiceImpl.java` | 154 | `naming/magic-number` | `style` |

---

## ℹ️ Info Issues

> 轻微建议，可视作代码审查清单。

### INFO-001: 未使用的导入 — `ExamController.java:1-12`

```java
import java.util.ArrayList;    // 未使用
import java.util.HashMap;      // 未使用
import java.util.Collections;  // 未使用
```

- **文件:** `src/main/java/com/exam/controller/ExamController.java`
- **行号:** 1–12
- **规则:** `java/unused-import` (严重度: info)
- **标签:** `style`, `auto-fixable`

**✅ 自动修复:** 运行 IDE 优化导入，或配置 `saveActions` 自动清理。

---

### INFO-002: 缺少 JavaDoc — `ExamService.java`

- **文件:** `src/main/java/com/exam/service/ExamService.java`
- **行号:** 15, 32, 48, 67, 89, 101
- **规则:** `documentation/missing-javadoc` (严重度: info)
- **影响范围:** 6 个公开方法缺少 JavaDoc

**✅ 建议：** 为所有公开 API 方法添加 JavaDoc，描述参数、返回值和异常。

---

### INFO-003: 硬编码字符串 — `PaperServiceImpl.java:22`

```java
if (status.equals("submitted")) { ... }
```

- **文件:** `src/main/java/com/exam/service/impl/PaperServiceImpl.java`
- **行号:** 22
- **规则:** `code-smell/magic-string` (严重度: info)

**✅ 建议：** 提取为常量 `public static final String STATUS_SUBMITTED = "submitted"`。

---

### INFO-004 ~ INFO-043

> 完整列表见 `E:\A工作文档\skills\code-health-scanner\reports\2026-05-18_infos.json`

| 范围 | 条数 | 主要类别 |
|------|------|---------|
| 未使用导入 | 8 | `style` |
| 缺少注释 | 12 | `documentation` |
| 命名不规范 | 5 | `style` |
| 硬编码值 | 6 | `code-smell` |
| 缩进/格式 | 7 | `style` |
| 其他 | 5 | — |

---

## Quick Wins

> 🔥 低投入高回报，建议优先处理。

### 🏆 Quick Win 1: 自动修复未使用导入

- **涉及文件:** 8 个
- **预估耗时:** 2 分钟
- **健康分提升:** +4 分 (修复后 78 → 82)
- **操作:** `mvn spotless:apply` 或 IDE `Organize Imports`

### 🏆 Quick Win 2: 修复硬编码密码

- **涉及文件:** `application-dev.properties`
- **预估耗时:** 5 分钟
- **健康分提升:** +10 分 (修复后 82 → 92 🟢 优秀)
- **操作:** 将密码移至环境变量，确保 `.gitignore` 排除配置

### 🏆 Quick Win 3: 提取 magic strings 为常量

- **涉及文件:** 6 个
- **预估耗时:** 10 分钟
- **健康分提升:** +3 分
- **操作:** 逐个文件提取常量和枚举

### 📊  Quick Wins 汇总

| 优先级 | 任务 | 耗时 | 健康分提升 | 累计分 |
|--------|------|------|-----------|--------|
| 🔴 P0 | 修复 CRIT-002 空指针 | 15min | +10 | 88 |
| 🔴 P0 | 修复 CRIT-001 SQL 注入 | 20min | +10 | 98 |
| 🟠 P1 | 修复 CRIT-003 硬编码密码 | 5min | +10 | → 🟢 |
| 🟡 P2 | 修复 WARN-002 N+1 查询 | 30min | +3 | — |
| 🟢 P3 | 自动修复未使用导入 | 2min | +4 | — |

---

## Trend Analysis

> 与上一次扫描 (`2026-05-17`) 对比。

```text
健康分变化: 72 → 78 (+6 ↑)
┌─────────────────────────────────────────────────────────┐
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓        72      │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓    78  ↑  │
│  ─────────────────────────────────────────────          │
│  05-12   05-13   05-14   05-15   05-16   05-17  05-18   │
└─────────────────────────────────────────────────────────┘
```

### 近期趋势数据

| 日期 | 健康分 | Issues | 备注 |
|------|--------|--------|------|
| 2026-05-12 | 65 🟡 | 82 | 初始基线扫描 |
| 2026-05-13 | 68 🟡 | 76 | 修复 NPE 问题 |
| 2026-05-14 | 71 🟡 | 70 | 引入 Checkstyle |
| 2026-05-15 | 70 🟡 | 72 | 新增模块导致回弹 |
| 2026-05-16 | 73 🟡 | 63 | 清除死代码 |
| 2026-05-17 | 72 🟡 | 62 | SQL 优化 |
| 2026-05-18 | **78 🟢** | **58** | 本次扫描 |

### 变化摘要

| 指标 | 上期 | 本期 | 变化 |
|------|------|------|------|
| Critical | 2 | 3 | +1 🔴 |
| Warning | 15 | 12 | −3 🟢 |
| Info | 45 | 43 | −2 🟢 |
| **总计** | **62** | **58** | **−4 🟢** |
| **健康分** | **72** | **78** | **+6 ↑** |

> **分析:** 新功能提交引入了 1 个 Critical 安全问题（SQL 注入），但 Warning 减少了 3 个，Info 减少了 2 个。总体趋势向好，但需关注 Critical 的反升。

---

## Recommendations

### 🔴 必须立即处理

1. **[CRIT-001] SQL 注入风险** — `UserController.java:47`
   - 使用参数化查询替换字符串拼接
   - 添加输入校验白名单
   - 责任人: @张三

2. **[CRIT-002] 空指针风险** — `ExamService.java:102`
   - 添加 Optional 或 null-check
   - 建议在代码审查中增加空安全检查清单
   - 责任人: @李四

3. **[CRIT-003] 硬编码密码** — `application-dev.properties:25`
   - 使用环境变量或 Vault
   - 审查 Git 历史中是否已泄露
   - 责任人: @王五

### 🟠 建议本轮迭代处理

4. **[WARN-001] 未使用的参数** — 移除或注解
5. **[WARN-002] N+1 查询** — 改为批量查询
6. **[WARN-005] CSRF 关闭** — 启用 CSRF 保护或明确文档说明
7. **[WARN-009] 长方法重构** — 拆分 `ExamServiceImpl.java:301` 的 45 行方法

### 🟡 可加入下期迭代计划

8. **[INFO-001] 清理未使用导入** — 自动化格式化
9. **[INFO-002] 补充 JavaDoc** — 公共 API 文档
10. **[INFO-003] 提取 magic strings** — 常量重构

### 📋 工程实践建议

| 领域 | 建议 |
|------|------|
| 🔧 **工具链** | 配置 Git Pre-commit Hook 自动运行扫描，阻止 Critical 问题入库 |
| 📐 **代码规范** | 引入 Checkstyle + SpotBugs 作为 CI 质量门禁 |
| 📝 **文档** | 建立 Errors.md 记录常见错误模式及修复方案 |
| 👥 **流程** | 每周 Code Review 前先跑一次扫描，Review 时重点关注 Critical 和 Warning |
| 🧪 **测试** | 对 N+1 查询添加数据库集成测试，验证查询次数 |

---

## Appendices

### A. 扫描规则配置

```
rules:
  active: 48/72
  custom:
    - security/hardcoded-secret
    - performance/n-plus-one
    - null-safety/dereference
  disabled:
    - naming/camel-case (与项目约定冲突)
    - style/line-length (已有 Prettier 管理)
```

### B. 忽略列表

以下文件和模式已配置为忽略：

- `**/*.generated.*`
- `**/test/**`
- `**/resources/static/**`
- `**/target/**`

### C. 完整报告

- 详细 JSON: `E:\A工作文档\skills\code-health-scanner\reports\2026-05-18_full.json`
- 增量报告: `E:\A工作文档\skills\code-health-scanner\reports\2026-05-18_diff.md`

---

## Markdown Rendering Guidelines

> 该模板遵循以下规则以确保在所有 Markdown 渲染器中获得一致效果：

### 📏 格式规范

| 元素 | 规范 |
|------|------|
| **标题层级** | `#` 总报告标题 → `##` 大节 → `###` 小节 → `####` 子节 |
| **代码块** | 始终标注语言 (`java`, `properties`, `sql`, `bash`, `json`, `text`) |
| **表格** | 必须含表头分隔线，列内避免过宽内容（超过 60 字考虑换行） |
| **分隔线** | `---` 用于分隔不同 issue，前后各留空行 |
| **引用块** | `>` 用于报告元数据、引用说明 |
| **列表** | 三级以内嵌套，每层级使用不同标记：`1.` → `-` → `  *` |

### 🎨 视觉增强（支持时可用）

- 使用 Emoji 作为视觉标记，保持语义清晰 👉 `🔴` `🟠` `🟡` `🟢`
- 关键数字使用 **加粗** 突出
- 变化趋势使用颜色 emoji: `↑` / `↓` / `→`
- ASCII 图示仅在纯 Markdown 环境中退而求其次

### ✅ 自动化友好

- `## CRIT-NNN` / `## WARN-NNN` / `## INFO-NNN` 格式便于 grep 和 CI 解析
- 支持 `<!-- scan-meta -->` 注释块注入元数据
- 每节末尾可添加 `<!-- autogenerated -->` 标记
- JSON 导出关联通过文件路径链接

---

<sub>📋 本报告由 Code Health Scanner 自动生成 | 如需忽略规则请修改 `.code-health.yml`</sub>
