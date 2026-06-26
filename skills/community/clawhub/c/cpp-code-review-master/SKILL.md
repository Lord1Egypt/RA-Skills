---
name: cpp-code-review-master
displayName: C++ Code Review Master
description: |
  组合式 C++ 代码评审方案 — 融合静态分析、AI 推理、多轮迭代评审、C++ 专项检查。
  适用于：PR review、增量代码审查、全量项目评审、代码质量评分。
  触发词：review cpp、cpp 代码评审、C++ review、代码审查。
license: MIT
version: 1.0.0
metadata:
  {"openclaw":{"emoji":"🔍","category":"code-quality","languages":["cpp","c"]}}
---

# C++ Code Review Master

组合式 C++ 代码评审方案，整合静态分析、C++ 专项检查、多轮迭代评审与 AI 推理能力。

---

## 架构

```
用户发起 C++ 代码评审
         │
         ▼
┌─────────────────────────┐
│  1. C++ 专项检查          │  ← cpp skill（内存安全、悬垂引用、UB、所有权）
│     + 静态分析预检         │  ← code-review-sr（本地 regex 预检）
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  2. 三路并行 AI 评审       │  ← iterative-code-review（3 个 reviewer 并行）
│                           │
│   Reviewer-1 → 功能正确性  │
│   Reviewer-2 → 性能与内存  │
│   Reviewer-3 → 安全与最佳实践│
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  3. 汇总 + 评分报告       │  ← modified-code-review（评分、性价比）
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│  4. 可选自动修复          │  ← code-review-fix（自动修复 bug/安全/风格）
└─────────────────────────┘
```

---

## 评审维度

| 维度 | C++ 专项关注点 |
|------|---------------|
| **内存安全** | 内存泄漏、悬垂引用、野指针、double-free、use-after-free |
| **未定义行为** | 未初始化变量、数据竞争、整数溢出、类型双关 |
| **RAII / 所有权** | 构造/析构顺序、智能指针误用、锁粒度 |
| **性能** | 不必要的拷贝、临时对象、虚函数开销、内联建议 |
| **安全** | 缓冲区溢出、格式化字符串、指针运算、原始 new/delete |
| **可读性** | 命名规范、头文件组织、模板复杂度、注释完整性 |
| **最佳实践** | 现代 C++（C++17/20/23）特性、constexpr、 Concepts |

---

## 工作流程

### Step 1 — 收集代码上下文

- 用户指定文件、目录或 git diff
- 检测是否 PR 场景（`gh pr status` / `git log`）
- 判断增量审查还是全量审查

### Step 2 — C++ 专项预检

执行本地静态分析（code-review-sr 的 regex 预检 + cpp skill 规则）：

```javascript
// 检测 C++ 常见问题模式
const cppPatterns = [
  { pattern: /new\s+\w+\s*\[/, severity: 'high', type: 'memory', message: 'Consider using std::vector or smart pointers instead of raw new[]' },
  { pattern: /delete\s+\w+\s*\[/, severity: 'high', type: 'memory', message: 'Use RAII: prefer smart pointers or containers' },
  { pattern: /memcpy\s*\(/, severity: 'medium', type: 'security', message: 'Check buffer sizes carefully; prefer std::copy or std::memmove for overlapping regions' },
  { pattern: /sprintf\s*\(/, severity: 'high', type: 'security', message: 'sprintf is unsafe; use snprintf or std::format (C++20)' },
  { pattern: /std::auto_ptr/, severity: 'medium', type: 'modern-cpp', message: 'std::auto_ptr is deprecated; use std::unique_ptr' },
  { pattern: /virtual\s+\w+\s*\([^)]*\)\s*const\s*\{\s*return\s+0\s*;/, severity: 'medium', type: 'modern-cpp', message: 'Pure virtual should be = 0, not return 0' },
  { pattern: /mutable\s+\w+;/, severity: 'low', type: 'concurrency', message: 'mutable member in const method; ensure thread safety if accessed from multiple threads' },
  { pattern: /#define\s+\w+\s+\w+/, severity: 'low', type: 'modern-cpp', message: 'Prefer constexpr or const variables over macros' },
];
```

### Step 3 — 三路并行 AI 评审

启动 3 个独立 reviewer，每个关注不同维度：

- **Reviewer-1（功能正确性）**：逻辑错误、边界条件、断言、异常处理
- **Reviewer-2（性能与内存）**：内存分配、拷贝语义、算法复杂度、缓存友好性
- **Reviewer-3（安全与最佳实践）**：缓冲区安全、输入验证、C++ modern guidelines

### Step 4 — 汇总报告

综合所有 reviewer 意见，输出统一报告：

```markdown
## C++ Code Review Report

### 项目概览
- 评审范围：<文件/目录/diff>
- 评审模式：<全量/增量/PR>
- 评审时间：<timestamp>

### C++ 专项问题
| 严重性 | 类型 | 位置 | 问题描述 |
|--------|------|------|----------|
| 🔴 High | Memory | foo.cpp:42 | Raw new[] without corresponding delete[] |
| 🟡 Medium | UB | bar.cpp:87 | Uninitialized member variable |
| 🟡 Medium | Security | baz.cpp:23 | sprintf usage — buffer overflow risk |
| 🟢 Low | Modern C++ | utils.cpp:15 | Consider using std::string_view instead of const std::string& |

### 功能问题
...

### 性能问题
...

### 代码评分（百分制）
| 维度 | 得分 |
|------|------|
| 内存安全 | XX/100 |
| 逻辑正确性 | XX/100 |
| 性能 | XX/100 |
| 安全 | XX/100 |
| 可读性 | XX/100 |
| **总分** | **XX/100** |

### 修复优先级
1. [P0 - 必须修复] ...
2. [P1 - 强烈建议] ...
3. [P2 - 建议优化] ...
4. [P3 - 可选改进] ...
```

### Step 5 — 自动修复（可选）

用户确认后，使用 code-review-fix 执行修复：

```bash
# 只检查
/cpp-review --security

# 审查并修复
/cpp-review --fix

# 学习模式
/cpp-review --explain
```

---

## 触发方式

| 命令 | 场景 |
|------|------|
| `/cpp-review` | 评审当前打开的 C++ 文件 |
| `/cpp-review <file>` | 评审指定文件 |
| `/cpp-review --diff` | 评审当前 git diff |
| `/cpp-review --pr` | 评审当前 PR |
| `/cpp-review --fix` | 评审并自动修复 |
| `/cpp-review --full` | 全量项目评审 |

---

## 依赖的 Skills

| Skill | 用途 |
|-------|------|
| `cpp` | C++ 专项规则（内存、UB、所有权） |
| `code-review-sr` | 本地静态分析 + AI 深度评审 |
| `iterative-code-review` | 多轮迭代 + 多 reviewer 并行 |
| `modified-code-review` | 评分报告 + 性价比分析 |
| `code-review-fix` | 自动修复 |

---

## 限制与注意

- **并发限制**：同时最多 3 个 subagent 并行评审
- **最大轮次**：10 轮迭代（防止无限循环）
- **安全模式**：默认每步需用户确认，不会自动修改代码
- **代码不外传**：不向外部 API 发送时使用本地分析模式
