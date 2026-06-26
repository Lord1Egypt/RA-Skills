# C++ Code Review Master 使用手册

> 组合式 C++ 代码评审方案 — 融合静态分析、AI 推理、多轮迭代评审、C++ 专项检查。

---

## 目录

1. [方案概述](#1-方案概述)
2. [快速开始](#2-快速开始)
3. [完整工作流程](#3-完整工作流程)
4. [使用案例](#4-使用案例)
5. [命令参考](#5-命令参考)
6. [评审维度详解](#6-评审维度详解)
7. [评分体系](#7-评分体系)
8. [安全模式](#8-安全模式)
9. [常见问题](#9-常见问题)

---

## 1. 方案概述

### 1.1 解决什么问题？

C++ 是最容易引入隐蔽 bug 的语言之一——内存泄漏、悬垂指针、未定义行为、数据竞争等问题往往在运行时才暴露。本方案通过**多层检查**在代码合并前发现这些问题。

### 1.2 核心能力

| 能力 | 说明 |
|------|------|
| **C++ 专项检查** | 内存安全、RAII、UB、Modern C++ 合规 |
| **静态分析** | 本地 regex 预检，无需网络 |
| **AI 深度评审** | 三路并行 reviewer，覆盖功能/性能/安全 |
| **多轮迭代** | 持续评审直到问题收敛 |
| **自动修复** | 发现问题后可直接修复 |
| **评分报告** | 百分制评分 + 修复优先级 |

### 1.3 技术架构

```
┌─────────────────────────────────────────────────────────┐
│                  C++ Code Review Master                 │
│                                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │   cpp       │ +  │code-review  │ →  │ C++ 专项预检│ │
│  │  skill      │    │    -sr      │    │             │ │
│  └─────────────┘    └─────────────┘    └──────┬──────┘ │
│                                                │        │
│                                                ▼        │
│  ┌─────────────────────────────────────────────────────┐ │
│  │          三路并行 AI 评审（iterative-review）        │ │
│  │                                                     │ │
│  │  Reviewer-1        Reviewer-2        Reviewer-3     │ │
│  │  功能正确性         性能与内存         安全与最佳实践  │ │
│  │  - 逻辑错误         - 内存分配          - 缓冲区安全   │ │
│  │  - 边界条件         - 拷贝语义          - UB 风险     │ │
│  │  - 异常处理         - 算法复杂度        - Modern C++  │ │
│  └─────────────────────────────────────────────────────┘ │
│                        │                                 │
│                        ▼                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │ modified    │ →  │  评分报告    │ →  │code-review  │ │
│  │ -code-review│    │  + 性价比    │    │   -fix      │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
└─────────────────────────────────────────────────────────┘
```

---

## 2. 快速开始

### 2.1 安装依赖 Skill

本方案依赖以下 skill（已包含在 `cpp-code-review-master/` 同级目录）：

```bash
# 确保以下 skill 已安装
code-review-sr          # 本地静态分析 + AI 推理
iterative-code-review   # 多轮迭代 + 多 reviewer
modified-code-review    # 评分报告 + 性价比
code-review-fix         # 自动修复
cpp                     # C++ 专项规则
```

### 2.2 基本用法

```bash
# 评审单个文件
/cpp-review src/memory_pool.cpp

# 评审当前 git diff
/cpp-review --diff

# 评审并自动修复
/cpp-review --fix

# 全量项目评审
/cpp-review --full
```

### 2.3 首次使用检查清单

- [ ] OpenClaw 已正常运行
- [ ] `cpp-code-review-master` skill 已加载
- [ ] （可选）配置 `ANTHROPIC_API_KEY` 以启用 AI 评审
- [ ] （可选）配置 `OLLAMA_HOST` 使用本地模型

---

## 3. 完整工作流程

```
Step 1: 上下文收集
   ├── 识别评审范围（文件/diff/PR/全项目）
   ├── 判断评审模式（增量/全量/PR）
   └── 检测 C++ 版本和编译标准

Step 2: C++ 专项预检
   ├── 运行 cpp skill 规则
   ├── 本地 regex 静态分析
   └── 收集初步问题列表

Step 3: 三路并行 AI 评审
   ├── Reviewer-1: 功能正确性
   ├── Reviewer-2: 性能与内存
   └── Reviewer-3: 安全与最佳实践

Step 4: 问题汇总与去重
   ├── 合并三路结果
   ├── 去除重复问题
   └── 按严重性排序

Step 5: 生成评审报告
   ├── 各维度评分
   ├── 修复优先级
   └── 性价比分析

Step 6: 用户确认
   ├── 展示报告
   └── 选择下一步（修复/继续/结束）

Step 7: 验证修复（可选）
   ├── 执行自动修复
   └── 确认问题已解决
```

---

## 4. 使用案例

### 案例 1：评审 Pull Request

**场景：** 同事提交了一个 PR，修改了 `src/auth/session.cpp`，需要你 review。

**触发命令：**
```bash
/cpp-review --pr
```

**系统行为：**

1. **上下文收集** — 检测当前 PR 信息（通过 `gh pr status`）
2. **预检** — 运行 C++ 专项检查，发现：
   - `session.cpp:156` — 使用了 `strcpy`，缓冲区溢出风险 🔴 P0
   - `session.cpp:203` — `std::auto_ptr` 已废弃 🟡 P1
3. **AI 评审** — 三路 reviewer 并行工作
4. **汇总报告** — 合并所有问题，输出评分

**典型输出：**
````markdown
## C++ Code Review Report

### 评审范围
- 文件：src/auth/session.cpp
- 模式：PR review（分支：feature/refresh-token）

### 🔴 P0 — 必须修复
| 位置 | 问题 | 风险 |
|------|------|------|
| session.cpp:156 | `strcpy(user, input)` — 用户输入未验证 | 缓冲区溢出，可导致 RCE |
| session.cpp:201 | `delete p` 后未置空，存在 use-after-free 风险 | 崩溃或数据损坏 |

### 🟡 P1 — 强烈建议
| 位置 | 问题 | 建议 |
|------|------|------|
| session.cpp:203 | `std::auto_ptr` 已废弃 | 改用 `std::unique_ptr` |
| session.cpp:89 | 未初始化成员 `m_lastRefresh` | 可能导致UB |

### 代码评分
| 维度 | 得分 |
|------|------|
| 内存安全 | 45/100 |
| 逻辑正确性 | 72/100 |
| 性能 | 68/100 |
| 安全 | 35/100 |
| 可读性 | 70/100 |
| **总分** | **56/100 — D 级** |

### 修复优先级
1. [P0] session.cpp:156 — 使用 `strncpy` 或 `std::string`
2. [P0] session.cpp:201 — delete 后立即置空 `p = nullptr`
3. [P1] session.cpp:203 — `std::auto_ptr` → `std::unique_ptr`
4. [P1] session.cpp:89 — 初始化列表中添加 `m_lastRefresh(0)`
````

---

### 案例 2：评审 Git Diff（提交前自检）

**场景：** 你刚写完一段内存管理的代码，准备提交前想自己 review 一下。

**触发命令：**
```bash
# 先查看 diff
git diff src/core/buffer_pool.cpp

# 评审 diff
/cpp-review --diff
```

**系统行为：**

1. **检测改动** — 识别新增/修改的代码行
2. **增量评审** — 仅评审变动的部分（而非整个文件）
3. **快速预检** — 发现明显问题

**典型场景 — buffer_pool.cpp 的问题：**

```cpp
// 你写的代码（diff 中新增的部分）
void BufferPool::allocate() {
    m_buffer = new char[BUFFER_SIZE];  // 🔴 P1: 裸 new，无异常安全
    // ...
}

void BufferPool::release() {
    delete[] m_buffer;                  // 🔴 P0: delete 后未置空
    // 函数结束但 m_buffer 仍指向已释放内存
}
```

**评审输出：**
```markdown
## Diff Review — buffer_pool.cpp

### 新增代码问题
| 严重性 | 行 | 问题 |
|--------|----|------|
| 🔴 P0 | 42 | `delete[] m_buffer` 后未置空，use-after-free 风险 |
| 🟠 P1 | 38 | 裸 `new char[]` 无异常安全，建议用 `std::vector<char>` |
| 🟡 P2 | 45 | `BUFFER_SIZE` 为 magic number，建议定义为常量 |

### 修复建议
```cpp
// P0 修复
void BufferPool::release() {
    delete[] m_buffer;
    m_buffer = nullptr;  // ✅ delete 后立即置空
}

// P1 修复 — 推荐方案
std::vector<char> m_buffer;  // RAII，自动管理内存

void BufferPool::allocate() {
    m_buffer.resize(BUFFER_SIZE);  // ✅ 无需手动 delete
}
```
```

---

### 案例 3：全量项目评审

**场景：** 新接手一个 C++ 项目，需要全面了解代码质量和潜在风险。

**触发命令：**
```bash
/cpp-review --full --dir ./src
```

**系统行为：**

1. **全量扫描** — 遍历所有 `.cpp` / `.h` / `.hpp` 文件
2. **多轮迭代** — 最多 10 轮，直到问题收敛
3. **Final Round** — 全量复审 + 编译验证

**典型输出：**
```markdown
## Full Project Review Report

### 项目概览
- 路径：./src
- 文件数：47
- 代码行数：12,384
- 评审轮次：3 轮

### 问题统计
| 严重性 | 第一轮 | 第二轮 | 第三轮（Final） |
|--------|--------|--------|----------------|
| P0 | 8 | 2 | 0 |
| P1 | 23 | 9 | 3 |
| P2 | 45 | 18 | 5 |
| P3 | 67 | 31 | 12 |

### 评分趋势
| 轮次 | 总分 | 内存安全 | 性能 | 安全 |
|------|------|----------|------|------|
| Round 1 | 52/D | 38 | 55 | 41 |
| Round 2 | 71/C | 62 | 70 | 65 |
| Round 3 | 84/B | 79 | 78 | 82 |

### Final Round — 剩余问题
仅剩 3 个 P1/P2 问题，均为代码风格和 minor 优化建议，不阻止合并。

### 结论
✅ 项目可以合并，建议在后续迭代中处理剩余 3 个优化点。
```

---

### 案例 4：评审单个文件（日常开发）

**场景：** 你在实现一个复杂的模板类，希望在提交前确保没问题。

**触发命令：**
```bash
/cpp-review src/utils/factory.h
```

**典型输出：**
```markdown
## File Review — factory.h

### 🔴 P0 — Critical
| 位置 | 问题 | 风险 |
|------|------|------|
| factory.h:67 | 模板参数 `T` 未约束，可能在编译期产生大量无用实例 | 编译时间爆炸、代码膨胀 |

### 🟡 P2 — Medium
| 位置 | 问题 | 建议 |
|------|------|------|
| factory.h:34 | `create()` 返回原始指针，建议返回 `std::unique_ptr` | RAII 化 |
| factory.h:89 | `std::map::find()` 返回的迭代器未检查是否等于 `end()` | 潜在 UB |

### 🟢 P3 — Low
| 位置 | 问题 | 建议 |
|------|------|------|
| factory.h:12 | 缺少 Doxygen 注释 | 添加文档 |

### 代码评分：68/100 — C 级
### 建议：修复 P0（添加 Concepts 约束）和 P2（RAII 化）后再合并。
```

---

### 案例 5：评审 + 自动修复

**场景：** 代码中有多个明确的 style 和安全小问题，你想直接修复而不手动处理。

**触发命令：**
```bash
# 先审查了解问题
/cpp-review src/utils/string_helper.cpp

# 确认后执行修复
/cpp-review src/utils/string_helper.cpp --fix
```

**系统行为：**

1. **审查模式** — 先运行完整评审，展示报告
2. **修复确认** — 用户确认是否执行修复
3. **自动修复** — 使用 `code-review-fix` 逐个修复
4. **验证** — 修复后重新评审确认问题已解决

**修复示例：**

修复前：
```cpp
void process(const std::string& input) {
    char buf[256];
    sprintf(buf, "Input: %s", input.c_str());  // 🔴 P0: sprintf 不安全
    strcpy(buf, input.c_str());                  // 🔴 P0: 缓冲区溢出
}
```

修复后：
```cpp
void process(const std::string& input) {
    std::string buf = std::format("Input: {}", input);  // ✅ C++20 std::format
    // 或兼容方案：
    // char buf[256];
    // snprintf(buf, sizeof(buf), "Input: %s", input.c_str());  // ✅ 有边界保护
}
```

---

### 案例 6：学习模式（--explain）

**场景：** 你想通过评审来学习 C++ 最佳实践，理解每个问题的原因。

**触发命令：**
```bash
/cpp-review src/core/data_processor.cpp --explain
```

**典型输出：**
```markdown
## C++ Code Review — Learning Mode

### 🔴 P1: Raw new[] detected
**位置：** data_processor.cpp:45

**问题代码：**
```cpp
int* buffer = new int[1024];
// ... 使用 buffer ...
delete[] buffer;
```

**为什么有问题？**
1. **异常不安全**：如果 `new` 和 `delete` 之间抛出异常，内存会泄漏
2. **责任分散**：开发者必须记住每个路径都 `delete[]`，容易遗漏
3. **现代 C++ 原则**：优先使用 RAII，让对象管理自己的资源

**最佳实践：**
```cpp
// 方案 1: std::vector（推荐）
std::vector<int> buffer(1024);
// vector 在离开作用域时自动释放内存，无论是否发生异常

// 方案 2: std::unique_ptr（数组特化）
std::unique_ptr<int[]> buffer(new int[1024]);
// unique_ptr 在离开作用域时自动 delete[]
```

**相关原则：**
- C++ Core Guidelines: `R.1: Manage resources by RAII objects`
- C++ Core Guidelines: `ES.46: Avoid `new` and `delete`

---
```

---

## 5. 命令参考

| 命令 | 说明 | 典型场景 |
|------|------|----------|
| `/cpp-review` | 评审当前打开的文件 | 快速检查 |
| `/cpp-review <file>` | 评审指定文件 | 单文件 review |
| `/cpp-review --diff` | 评审当前 git diff | 提交前自检 |
| `/cpp-review --pr` | 评审当前 PR | PR review |
| `/cpp-review --full` | 全量项目评审 | 新项目接手 |
| `/cpp-review --fix` | 评审 + 自动修复 | 修复已知问题 |
| `/cpp-review --explain` | 学习模式（带解释） | 提升 C++ 能力 |
| `/cpp-review --security` | 仅检查安全相关 | 快速安全扫描 |

---

## 6. 评审维度详解

### 6.1 内存安全（权重 30%）

**这是 C++ 最重要的维度**，也是本方案的核心关注点。

| 问题类型 | 示例 | 严重性 |
|----------|------|--------|
| use-after-free | delete 后继续使用指针 | P0 |
| 内存泄漏 | new 后忘记 delete | P1 |
| 悬垂指针 | 返回局部变量地址 | P0 |
| double-free | 同一指针 delete 两次 | P0 |
| 缓冲区溢出 | strcpy/sprintf 越界写入 | P0 |

**检查规则：**
```cpp
// 🔴 禁止（除非有充分理由）
int* p = new int[100];
delete[] p;
p[0] = 1;  // use-after-free!

// ✅ 推荐
auto p = std::make_unique<int[]>(100);
// 或 std::vector<int> p(100);
```

### 6.2 未定义行为（UB）（权重独立但影响所有维度）

UB 是 C++ 最危险的问题，因为它可能在某些编译器/平台下"看起来正常"，但在其他环境下崩溃。

| UB 类型 | 示例 | 严重性 |
|---------|------|--------|
| 未初始化变量 | `int x; return x;` | P0 |
| 数组越界 | `arr[n]` 当 `n >= size` | P0 |
| 数据竞争 | 两个线程同时写同一变量 | P0 |
| 有符号整数溢出 | `INT_MAX + 1` | P1 |
| 空指针解引用 | `p->method()` 当 `p == nullptr` | P0 |

### 6.3 性能（权重 20%）

| 问题类型 | 示例 | 建议 |
|---------|------|------|
| 不必要的拷贝 | `void f(std::string s)` 传值 | 改用 `const std::string&` |
| 缺少 move | `return obj`（大型对象） | 确保有 move 构造函数 |
| 循环内分配 | `for (...) { new T(); }` | 移到循环外或用对象池 |
| 错误的容器 | `std::list` 当可以用 `std::vector` | 通常 vector 更快 |

### 6.4 安全（权重 15%）

| 问题类型 | 危险代码 | 安全替代 |
|---------|---------|---------|
| 缓冲区溢出 | `strcpy(dst, src)` | `strncpy` / `std::string` |
| 格式化字符串 | `printf(user_input)` | `printf("%s", user_input)` |
| 整数溢出 | `size + user_val` | 提前检查 `size > SIZE_MAX - user_val` |
| 指针运算 | `ptr + user_offset` | 严格边界检查 |

### 6.5 可读性 / Modern C++（权重 10%）

| 问题 | 旧代码 | 现代 C++ |
|------|--------|---------|
| 宏定义常量 | `#define BUFFER_SIZE 1024` | `constexpr size_t BUFFER_SIZE = 1024;` |
| 原始指针 | `T* p = new T;` | `auto p = std::make_unique<T>();` |
| auto_ptr | `std::auto_ptr<T> p;` | `std::unique_ptr<T> p;` |
| C 风格数组 | `int arr[100];` | `std::array<int, 100> arr;` |
| nullptr | `NULL` / `0` | `nullptr` |

---

## 7. 评分体系

### 7.1 评分公式

```
总分 = 内存安全 × 0.30
     + 逻辑正确性 × 0.25
     + 性能 × 0.20
     + 安全 × 0.15
     + 可读性 × 0.10
```

### 7.2 扣分规则

| 问题级别 | 扣分 |
|----------|------|
| P0 | -25 分 |
| P1 | -15 分 |
| P2 | -5 分 |
| P3 | -1 分 |

### 7.3 等级对照

| 分数 | 等级 | 含义 | 操作建议 |
|------|------|------|----------|
| 90–100 | A | 优秀 | 直接合并 |
| 75–89 | B | 良好 | 可合并，有优化空间 |
| 60–74 | C | 合格 | 修复 P0/P1 后合并 |
| 40–59 | D | 需改进 | 存在明显问题，需修改 |
| 0–39 | E | 不达标 | 严重问题，需重构 |

---

## 8. 安全模式

**默认启用安全模式**，保护你的代码和系统。

### 8.1 默认行为（安全模式）

```
✅ 允许：
   - 读取代码文件
   - 运行只读命令（git diff、ls 等）
   - Spawn subagent 进行并行评审
   - 生成评审报告

⚠️ 需要确认：
   - 修改任何文件
   - 执行 git commit
   - 安装 npm 包或运行 build
   - Spawn Fixer subagent 执行修复

❌ 禁止：
   - 未经用户明确同意修改代码
   - 自主执行多轮修复循环
   - 向未知第三方服务发送代码
```

### 8.2 自动化模式（可选）

用户可通过配置文件启用 `autoFix`：

```json
// .cpp-review-config.json
{
  "autoFix": true,
  "autoContinue": false,
  "severityThreshold": "P2"
}
```

⚠️ **警告**：启用 `autoFix` 后会自动修改代码，请确保有 git 备份。

---

## 9. 常见问题

### Q1: 报 "No API key configured" 怎么办？

A: 本地静态分析（regex 预检）无需 API key 即可工作。若想启用 AI 深度评审：

```bash
# 使用 Anthropic Claude
export ANTHROPIC_API_KEY=sk-ant-...

# 或使用本地 Ollama
export OLLAMA_HOST=http://localhost:11434

# 然后重新运行评审
/cpp-review --diff
```

### Q2: 评审一个很大的项目会超时吗？

A: 全量评审有 10 轮上限，每轮内部有超时控制。对于超大项目建议：
- 先用增量模式 `/cpp-review --diff` 评审近期改动
- 全量评审建议在 CI/CD 环境中运行

### Q3: 如何忽略某些文件或目录？

A: 在项目根目录创建 `.cpp-reviewignore`：

```
# 忽略第三方库
vendor/
third_party/

# 忽略生成文件
*.gen.cpp
 moc_*.cpp
```

### Q4: 评分太主观？觉得某些问题不应该扣分？

A: 评分权重可在 `SKILL.md` 中调整。P3 问题只扣 1 分，主要影响在 P0/P1。评审结果仅供参考，最终决定权在开发者。

### Q5: 能否集成到 CI/CD？

A: 可以。将评审命令添加到 GitHub Actions：

```yaml
name: C++ Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run C++ Code Review
        run: |
          /cpp-review --diff --output report.md
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: cpp-review-report
          path: report.md
```

### Q6: 某些 skill 被标记为可疑，还能用吗？

A: `quack-code-review` 和 `code-review-fix` 被 VirusTotal 标记，是因为它们包含外部 API 调用模式（用于计费）。这些是正常的付费 skill 功能，不是恶意代码。使用前建议审查代码确认行为符合预期。

---

## 附录：快速检查清单

### 提交前必查

- [ ] 运行 `/cpp-review --diff`
- [ ] 无 P0 问题
- [ ] 无 P1 问题（或有明确记录跟踪）
- [ ] 代码评分 >= 60 分
- [ ] 重要路径有测试覆盖

### PR Review 必查

- [ ] 运行 `/cpp-review --pr`
- [ ] 所有 P0 已修复
- [ ] P1 有合理理由或跟踪记录
- [ ] 性能问题已评估
- [ ] 安全问题已清零

---

_最后更新：2026-04-07 — C++ Code Review Master v1.0.0_
