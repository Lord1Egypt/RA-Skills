# C++ Code Review Master

**组合式 C++ 代码评审方案** — 整合多个 skill 的优势，专门针对 C++ 代码设计。

---

## 组合架构

```
┌──────────────────────────────────────────────┐
│            C++ Code Review Master             │
│                                              │
│  ① C++ 专项检查    → cpp + code-review-sr   │
│  ② 多路并行评审    → iterative-code-review   │
│  ③ 评分报告        → modified-code-review   │
│  ④ 可选自动修复    → code-review-fix         │
└──────────────────────────────────────────────┘
```

---

## 支持的评审场景

| 场景 | 命令 | 说明 |
|------|------|------|
| 单文件评审 | `/cpp-review <file.cpp>` | 评审指定 C++ 文件 |
| Git Diff | `/cpp-review --diff` | 评审当前工作区改动 |
| PR 评审 | `/cpp-review --pr` | 评审 GitHub PR 内容 |
| 全量评审 | `/cpp-review --full` | 扫描整个项目 |
| 审查 + 修复 | `/cpp-review --fix` | 发现问题并自动修复 |
| 深度学习 | `/cpp-review --explain` | 附带详细解释的评审 |

---

## C++ 专项检查维度

### 🔴 内存安全（Memory Safety）
- 裸 `new[]` / `delete[]` → 推荐 `std::vector` / `std::unique_ptr`
- 悬垂指针 / 野指针
- Double-free / use-after-free
- 内存泄漏（缺少析构清理）

### 🟡 未定义行为（Undefined Behavior）
- 未初始化变量
- 数据竞争（data race）
- 整数溢出
- 类型双关（type punning）

### 🟡 RAII / 所有权（Ownership）
- 构造/析构顺序问题
- 智能指针误用（`std::auto_ptr` 已废弃）
- 锁的粒度与死锁风险

### 🟢 性能（Performance）
- 不必要的拷贝（缺少 `std::move`）
- 临时对象开销
- 虚函数表开销
- 内联优化建议

### 🔵 安全（Security）
- 缓冲区溢出（`strcpy`/`sprintf` → `snprintf`/`std::format`）
- 格式化字符串漏洞
- 指针运算安全性
- 原始 `new`/`delete` 风险

### 🟢 现代 C++（Modern C++）
- C++17/20/23 新特性使用检查
- `constexpr` 建议
- Concepts（C++20）使用
- 弃用特性警告（`std::auto_ptr`、宏定义常量）

---

## 评分体系

| 维度 | 权重 |
|------|------|
| 内存安全 | 30% |
| 逻辑正确性 | 25% |
| 性能 | 20% |
| 安全 | 15% |
| 可读性 | 10% |

| 分数区间 | 等级 | 含义 |
|----------|------|------|
| 90–100 | A | 优秀，可直接合并 |
| 75–89 | B | 良好，有改进空间 |
| 60–74 | C | 合格，需修复高优先级问题 |
| 40–59 | D | 需改进，存在明显问题 |
| 0–39 | E | 不达标，需重构 |

---

## 目录结构

```
cpp-code-review-master/
├── SKILL.md          # 主 skill 定义
├── README.md          # 本文档
└── references/
    ├── workflow.md    # 详细工作流程
    ├── cpp-checklist.md  # C++ 专项检查清单
    └── severity.md     # 问题严重级别定义
```

---

## 依赖的子 Skills

| Skill | 版本 | 用途 |
|-------|------|------|
| `cpp` | 1.0.1 | C++ 常见错误专项检查 |
| `code-review-sr` | 1.0.4 | 本地静态分析 + AI 推理 |
| `iterative-code-review` | 1.2.1 | 多轮迭代 + 多 reviewer 并行 |
| `modified-code-review` | 1.0.0 | 评分报告 + 性价比分析 |
| `code-review-fix` | 1.0.0 | 自动修复 bug / 安全 / 风格问题 |

---

## 安全模式

默认启用**安全模式**，每步需用户确认：

```
✅ 读取代码、运行只读命令、Spawn subagent 分析、报告问题
⚠️  修改文件、git commit、Spawn Fixer（需用户同意）
❌  未经同意修改代码、自主运行多轮修复、自主提交
```

---

## 使用示例

### 1. 评审当前 git diff
```
/cpp-review --diff
```

### 2. 评审指定文件
```
/cpp-review src/utils/memory_pool.cpp
```

### 3. 评审 PR 并自动修复
```
/cpp-review --pr --fix
```

### 4. 全量项目评审
```
/cpp-review --full
```

---

## 局限性

- 并发限制：最多 3 个 subagent 并行
- 最大轮次：10 轮（防止无限循环）
- 代码外传：使用本地分析模式时不向外部发送代码
- 评分主观：评分算法基于规则，实际效果需根据项目调整
