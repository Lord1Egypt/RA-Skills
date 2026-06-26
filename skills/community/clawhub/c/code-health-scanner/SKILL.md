---
name: code-health-scanner
version: 1.0.1
license: MIT
author: sallyface0
description: >
  Privacy-first Spring Boot code health diagnosis. Detects security vulnerabilities, performance anti-patterns, code quality issues, and dependency risks across Java/Spring Boot projects. v1.0.1: narrowed triggers, added PRIVACY.md. Generates a structured health report with severity classification.
---

# Code Health Scanner v1.0.1 — Spring Boot 代码健康扫描

> **一句话：** 一键扫描你的 Spring Boot 项目，找出安全隐患、性能坑、代码坏味道，输出结构化健康报告。

## 🔒 Security & Privacy

> ⚠️ **请在使用前阅读 [PRIVACY.md](PRIVACY.md)**

- 📍 **仅读取项目代码，报告写入项目目录** — 不联网
- ✋ **自动修复前征求确认** — 低风险项的 auto-fix 需你确认后执行
- 🗑️ **扫描报告可随时删除** — 报告文件存放在项目中，随时可删

---

## Overview

Code Health Scanner 是一个轻量单角色扫描器，专为 Java / Spring Boot 项目设计。不需要复杂的多角色协奏——读代码、找问题、出报告、给修复建议，四步完事。

| 角色 | Actor | Responsibility |
|------|-------|----------------|
| **Scanner** | Main AI (you) | 发现代码文件 → 按规则检测 → 分类定级 → 生成报告 → 提供修复建议 |

## Supported Stacks

| Stack | Coverage | Notes |
|-------|----------|-------|
| **Java 8-21** | ✅ Full | 语法、异常处理、资源管理 |
| **Spring Boot 2.x / 3.x** | ✅ Full | 注解、事务、配置、安全 |
| **MyBatis / MyBatis Plus** | ✅ Full | SQL 注入检测、Mapper 规范 |
| **JPA / Hibernate** | ✅ Partial | N+1 查询、懒加载问题 |
| **Maven (pom.xml)** | ✅ Full | 依赖版本、已知 CVE |
| **Gradle** | 🟡 Partial | 基本依赖检测 |

---

## How It Works

```
用户指定项目路径 → Scanner 发现文件 → 逐文件检测 → 聚合分类 → 输出报告 → 可选自动修复
```

### Phase 1: 项目发现

扫描指定目录，识别项目类型：

1. **检测构建工具**：`pom.xml` (Maven) / `build.gradle` (Gradle)
2. **识别源码目录**：`src/main/java/` 为主扫描区域
3. **识别配置目录**：`src/main/resources/` (application.yml/properties)
4. **排除目录**：`target/`, `node_modules/`, `.git/`, `test/`（默认排除，可通过参数包含）

### Phase 2: 分类检测

按 4 大类逐文件扫描。详细规则见 [references/rules/java-spring.md](references/rules/java-spring.md)。

### Phase 3: 报告生成

输出结构化 Markdown 报告，包含：
- 总体健康评分 (0-100)
- 按严重度分组的 Issues
- 每个 Issue 包含：文件位置、代码片段、风险说明、修复建议
- 趋势分析（如果是增量扫描）

### Phase 4: 自动修复 (可选)

低风险 Info 级问题可自动修复（如命名规范、注解缺失）。Critical/Warning 级仅提供修复建议，需用户确认后执行。

---

## Severity Levels

| Level | Label | Meaning | Examples |
|-------|-------|---------|----------|
| 🔴 | **Critical** | 可能导致线上事故或安全漏洞 | SQL 注入、硬编码密码、资源泄漏 |
| 🟡 | **Warning** | 代码坏味道，长期会累积为技术债 | N+1 查询、God Class、异常吞没 |
| 🟢 | **Info** | 风格/规范问题 | 命名不符规范、TODO 堆积 |

---

## Detection Rules Summary

### 🔴 Critical (3 categories, ~12 rules)

#### Security
- **SQL Injection**: 字符串拼接构建 SQL → 使用 `#{param}` 替代 `${param}`
- **Hardcoded Secrets**: 代码/配置中明文密钥 → 环境变量或配置中心
- **Insecure Deserialization**: 不可信数据反序列化 → 白名单校验
- **Mass Assignment**: @RequestBody 无 @Valid 校验 → 添加校验注解
- **Open Redirect**: 用户可控的 redirect URL → URL 白名单

#### Reliability
- **NPE Risk**: Optional.get() 无 isPresent() 检查、返回 null 无 @Nullable
- **Resource Leak**: Stream/Connection 不在 try-with-resources 中
- **Transaction Missing**: 写操作缺少 @Transactional

#### Configuration
- **Debug Mode in Prod**: `debug: true` 在非 dev profile 中
- **Missing CSRF**: 非 REST API 缺少 CSRF 保护
- **Actuator Exposure**: `/actuator` 敏感端点暴露

### 🟡 Warning (4 categories, ~15 rules)

#### Performance
- **N+1 Query**: JPA 关联在循环中懒加载
- **String Concatenation in Loop**: 循环中使用 `+=` 拼接字符串
- **Unnecessary Autoboxing**: 频繁的 int↔Integer 转换
- **Collection Pre-sizing**: new ArrayList<>() 未指定初始容量（已知大小时）

#### Design
- **God Class**: 类 >500 行 或 >20 方法 → 拆分
- **Long Method**: 方法 >50 行 → 提取子方法
- **Too Many Parameters**: 方法参数 >5 个 → 封装为参数对象
- **Circular Dependency**: Bean 循环引用 → 重构或 @Lazy

#### Error Handling
- **Exception Swallowing**: 空 catch 块
- **printStackTrace in Prod**: 生产代码中的 e.printStackTrace()
- **Generic Exception Catch**: catch(Exception e) 过于宽泛
- **Throws Exception**: 方法抛出 Exception 而非具体异常

#### Testing (when test files are included)
- **Missing Assert**: 测试方法无 assert 语句
- **Sleep in Test**: Thread.sleep() 替代 awaitility

### 🟢 Info (2 categories, ~8 rules)

#### Convention
- **Naming**: 类名非 PascalCase、方法名非 camelCase
- **Package Structure**: 非标准 Spring Boot 分层
- **Comment Debt**: TODO/FIXME/HACK 数量 >5
- **Missing Javadoc**: public API 缺少文档注释

#### Dependencies
- **Version Lag**: 依赖版本落后 latest release >2 个大版本
- **Unused Dependency**: pom.xml 中声明但未使用的依赖
- **Snapshot in Prod**: 生产构建使用 SNAPSHOT 版本
- **Transitive Conflict**: 传递依赖版本冲突

---

## Report Format

完整报告模板见 [references/report-template.md](references/report-template.md)。

```markdown
# 🔍 Code Health Report — [项目名]

**扫描时间:** 2026-05-18 11:00
**项目路径:** /path/to/project
**扫描范围:** 42 文件, 8,500 LOC
**健康评分:** 72/100 (🔴 2 | 🟡 7 | 🟢 12)

---

## 📊 总览

| 类别 | 🔴 Critical | 🟡 Warning | 🟢 Info |
|------|:-----------:|:----------:|:-------:|
| Security | 2 | 0 | 0 |
| Reliability | 0 | 1 | 2 |
| Performance | 0 | 3 | 0 |
| Design | 0 | 2 | 3 |
| Error Handling | 0 | 1 | 2 |
| Convention | 0 | 0 | 5 |

## 🔴 Critical Issues

### C-1: SQL Injection in UserMapper.java:34
- **Risk:** 用户输入直接拼入 SQL，可能导致数据泄露
- **Code:** `@Select("SELECT * FROM user WHERE name = '${name}'")`
- **Fix:** 改用 `@Select("SELECT * FROM user WHERE name = #{name}")`

...

## 🟡 Warning Issues
...

## 🟢 Info Issues
...

## 💡 Quick Wins (Top 3)
1. 修复 2 个 SQL 注入 → +10 分
2. 迁移 3 个硬编码密钥到环境变量 → +5 分
3. 为 public API 添加 Javadoc → +3 分
```

---

## Health Score Formula

```
Health Score = 100 - (Critical × 15) - (Warning × 5) - (Info × 1)

Bounded: 0-100
Score ≥ 85: ✅ Healthy
Score 70-84: 🟡 Needs Attention
Score < 70: 🔴 At Risk
```

---

## Auto-Fix Protocol

### 可自动修复的 Info 级问题

| Issue | Auto-Fix | Confidence |
|-------|----------|------------|
| 类名非 PascalCase | 重命名文件 + 更新引用 | 高 |
| @Override 缺失 | 添加注解 | 极高 |
| 未使用的 import | 删除 import 行 | 极高 |
| `new ArrayList<>()` → `new ArrayList<>(N)` | 自动推断 N 后替换 | 中（需确认 N） |
| 空 catch 块 | 添加 `log.error(...)` | 低（需了解业务意图） |

### 自动修复工作流

```
Scanner 提示可修复项 → 用户 review → 逐项执行修复 → 输出变更摘要
```

---

## Usage Modes

### Mode 1: Quick Scan (默认)
- 只扫 `src/main/java/` 和 `src/main/resources/`
- 跳过测试目录
- 适合日常开发

### Mode 2: Full Scan
- 包含测试代码
- 包含构建配置文件
- 适合代码审查/发布前

### Mode 3: Incremental Scan
- 只扫 git diff 变更文件
- 适合 CI 流水线
- 需要 git 仓库

### 触发

```
用户说: "扫描这个项目" / "代码健康检查" / "check my code" / "code health scan"
+ 明确的项目路径（如 "E:\my-project" 或当前工作目录）

⚠️ 不再触发: "代码有没有问题" — 过于宽泛，可能匹配日常代码讨论
```

---

## Model Configuration

| Mode | Recommended Model | Reason |
|------|-------------------|--------|
| Quick Scan | `deepseek-v4-flash` | 速度快、成本低，适合日常使用 |
| Full Scan | `deepseek-v4-pro` | 推理能力强，适合全面审查 |
| Large Project (>500 files) | Sub-agent 分模块并发 | 避免单次扫描超时 |

---

## Workspace

扫描报告默认输出到 `{项目路径}/code-health-reports/`，命名格式：
```
code-health-report-{YYYY-MM-DD_HHmm}.md
```

---

## File References

| File | Description |
|------|-------------|
| [references/rules/java-spring.md](references/rules/java-spring.md) | 完整检测规则库（Java/Spring Boot 专项） |
| [references/report-template.md](references/report-template.md) | 健康报告模板与评分标准 |

---

## Extending to Other Stacks

Skill 设计为 Java/Spring Boot 优先，但规则引擎设计为可扩展。要支持新语言/框架：

1. 在 `references/rules/` 新增对应规则文件（如 `python-django.md`）
2. 在 SKILL.md 的 "Supported Stacks" 表中新增行
3. 在报告模板中追加对应语言的 Issue 示例

欢迎贡献额外语言规则。
