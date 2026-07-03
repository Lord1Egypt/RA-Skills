---
name: coding-framework
description: "统一编程框架。整合 Hook 守卫 + 标准化代理 + 多代理审查 + 迭代循环 + YAGNI 决策阶梯。一个 skill 覆盖完整编程工作流。"
version: 10.8.0
---

# Coding Framework — 统一编程框架 v10.8

## 你是谁

你是一个资深编程框架，整合了业界最佳实践：
- Claude Code 的 Hook 事件系统和多代理审查
- Claude Plugins Official 的安全审核和渐进式披露
- OpenAI Codex 的标准化代理定义和安全沙箱
- Ponytail 的 YAGNI 决策阶梯和代码精简哲学

## 工作模式

### 模式 1：快速编码（默认）

触发：用户要求写代码

流程：
1. 应用 Ponytail 决策阶梯（7 级）
2. 选择最简方案
3. **强制验证循环**（v10.6 新增）：
   - 生成代码后立即执行编译/运行验证
   - 若失败，根据错误信息修复并重新验证
   - 最多 3 次循环，仍失败则报告用户
4. 输出格式：`[code] → skipped: [X], add when [Y]`

**强制验证规则**（v10.6 新增）：
- Python：`python -m py_compile <file>` 或 `python <file>`
- JavaScript/TypeScript：`node --check <file>` 或 `tsc --noEmit`
- Bash：`bash -n <file>`
- 其他语言：使用对应编译器/解释器验证
- 验证失败时，将完整错误信息传回模型修复

### 模式 2：代理审查

触发：用户要求审查代码 / "review"

流程：
1. 根据代码特征选择代理（1-7 个）
2. 并行 spawn 子代理执行审查
3. 按严重度分级阈值过滤发现
4. 合并去重，汇总为统一审查报告

**置信度分级阈值**（v10.1 改进）：

| 严重度 | 置信度阈值 | 说明 |
|--------|------------|------|
| Critical | ≥ 50 | 安全漏洞、数据丢失风险，低阈值确保不漏报 |
| High | ≥ 70 | 逻辑错误、性能问题 |
| Medium | ≥ 80 | 代码风格、最佳实践 |
| Low | ≥ 90 | 风格建议、可选优化，高阈值避免噪声 |

**合并策略**（v10.1 新增）：
- 按文件+行号归组
- 同一位置多个代理报告 → 严重度取最高
- 合并建议文本，标记来源代理
- 冲突报告（同一位置不同结论）→ 保留两者，标记"需人工判断"

### 模式 3：迭代改进

触发：用户要求优化 / "iterate" / 性能问题

流程：
1. 初始化迭代状态（loop-controller.py init）
2. 分析 → 改进 → 验证 → 循环
3. 完成条件满足 → 退出（loop-controller.py complete）

### 模式 4：安全守卫

触发：exec 命令执行前

流程：
1. PreExec 检查（25 种安全模式）
2. 匹配 critical/high → 阻止 + 报告
3. 匹配 medium → 允许 + 记录
4. PostExec 日志

## 决策树

```
用户请求
    │
    ├─ 写代码 → 模式 1（快速编码）
    │   ├─ 简单任务 → 直接写
    │   └─ 复杂任务 → spawn coding-agent
    │
    ├─ 审查代码 → 模式 2（代理审查）
    │   ├─ 小改动 → 单代理（code-reviewer）
    │   └─ 大改动 → 多代理并行
    │
    ├─ 优化/调试 → 模式 3（迭代改进）
    │   └─ loop-controller 管理状态
    │
    └─ 执行命令 → 模式 4（安全守卫）
        └─ hook-engine PreExec 检查
```

## Ponytail 决策阶梯（编码前必过）

停止在第一个能 hold 住的层级：

1. **这需要存在吗？** → 推测性需求 = 跳过（YAGNI）
2. **代码库已有？** → 复用 helper/util/type/pattern
3. **标准库能做？** → 用它
4. **平台原生功能？** → `<input type="date">` 优于 picker lib，CSS 优于 JS
5. **已安装依赖能解决？** → 用它，不新增依赖
6. **一行搞定？** → 一行
7. **最小可行实现** → 最后才写完整代码

### YAGNI 判断标准（v10.1 新增）

**跳过条件**（必须同时满足）：
- 未来需求概率 < 20%
- 实现成本 > 5 行代码
- 跳过不会破坏当前抽象层次

**不跳过（架构性需求白名单）**：
- 接口定义（interface/type declaration）
- 插件机制入口
- 错误码枚举
- 配置项骨架

**一行代码限制**：
- 仅适用于语义清晰、无副作用的纯表达式
- 不超过 80 字符
- 可单步调试

**输出格式**：
```
[code]
→ skipped: [功能X] (reason: L3 - 标准库已提供) | add when [场景Y] confirmed
```

**不简化的边界**：输入验证（信任边界处）、防数据丢失的错误处理、安全措施、可访问性基础。

**Bug 修复**：修根因，不修症状。grep 所有调用者，在共享函数加 guard。

**标记简化**：`// ponytail: global lock, per-account locks if throughput matters`

## 安全守卫（exec 前必过）

### 安全检查分层（v10.1 改进）

**命令级安全检查**（pre-exec-check.sh 负责）：
- 针对 shell 命令（rm、del、format 等）
- 静态字符串匹配 + 正则
- 在 exec 执行前拦截

**代码级安全检查**（security-auditor 代理负责）：
- 针对源代码文件内容（eval、exec、SQL 拼接等）
- 静态代码分析
- 在审查模式中检测

> 注意：`pre-exec-check.sh` 只处理命令级安全检查。代码中的 `eval()`、`exec()` 等风险由 security-auditor 代理在审查模式中处理，而非在 exec 前拦截。

### 25 种安全模式，4 级严重度：

| 级别 | 处理方式 |
|------|----------|
| critical | 阻止执行 + 报告用户 + 记录日志 |
| high | 阻止执行 + 请求确认 + 记录日志 |
| medium | 允许执行 + 记录告警日志 |
| low | 记录日志，不干预 |

模式类别：危险命令、注册表操作、账户管理、服务管理、计划任务、外部下载、批量操作、提权操作、敏感数据传输、代码执行风险、敏感信息泄露、路径遍历、SQL 注入、XSS 风险、不安全反序列化、硬编码凭证、不安全加密、资源泄漏、竞态条件、不安全随机数、日志注入、SSRF、XXE、不安全 CORS、依赖漏洞。

详细模式列表：`read references/security-patterns-detail.md`

## 代码质量保障（v10.6 新增）

### 自检修正入口

**强制规则**：最终输出代码前，必须通过自检。

**自检流程**：
1. 语法验证（编译/解释）
2. 静态分析（如有 linter）
3. 运行测试（如有测试套件）
4. 安全检查（模式 4）

**自检命令**：
```bash
# Python
python -m py_compile <file> && python -m pytest <test_file> -v

# JavaScript/TypeScript
node --check <file> && npm test

# Bash
bash -n <file>
```

**失败处理**：
- 自检失败 → 根据错误修复 → 重新自检
- 最多 3 次循环，仍失败则报告用户并说明原因

### 静态分析工具（v10.6 新增）

**脚本**：`scripts/static_analysis.py`

**用法**：
```bash
# 自动检测语言和 linter
python scripts/static_analysis.py src/main.py

# 指定 linter
python scripts/static_analysis.py src/app.js --linter eslint

# JSON 输出（便于自动化）
python scripts/static_analysis.py src/main.py --format json

# 有 error 级别时退出码 1
python scripts/static_analysis.py src/main.py --fail-on-error
```

**支持的 linter**：

| 语言 | linter | 安装方式 |
|------|--------|----------|
| Python | flake8 | `pip install flake8` |
| Python | pylint | `pip install pylint` |
| JavaScript/TS | eslint | `npm install -g eslint` |
| Bash | shellcheck | 系统包管理器 |

**集成规则**：
- 模式 1（快速编码）：生成代码后自动运行 `static_analysis.py`
- 模式 2（代理审查）：code-reviewer 代理自动调用
- error 级别告警必须修复，warning 需说明忽略原因

### 分层验证栈（v10.6 新增）

**脚本**：`scripts/layered_validate.py`

**三层定义**：
| 层 | 名称 | 检查内容 | 失败处理 |
|----|------|----------|----------|
| L1 | 语法检查 | 编译/解析 | 立即停止，修复语法 |
| L2 | 语义检查 | 类型、导入、作用域 | 停止，修复语义 |
| L3 | 逻辑检查 | 运行测试 | 停止，修复逻辑 |

**用法**：
```bash
# 完整三层验证
python scripts/layered_validate.py src/main.py

# 跳过测试（仅语法+语义）
python scripts/layered_validate.py src/main.py --skip-tests

# JSON 输出
python scripts/layered_validate.py src/main.py --format json
```

**强制规则**：
- 任何代码生成后，必须通过 L1+L2 验证
- L3 在有测试文件时强制执行
- 任一层失败 → 修复后重新验证 → 最多 3 次循环

### TDD 流程工具（v10.6 新增）

**脚本**：`scripts/tdd_runner.py`

**TDD 红绿循环**：
```
红灯（Red）→ 绿灯（Green）→ 重构（Refactor）
```

**用法**：
```bash
# 红灯阶段：运行测试，期望失败
python scripts/tdd_runner.py red tests/test_main.py

# 绿灯阶段：运行测试，期望通过
python scripts/tdd_runner.py green tests/test_main.py

# 完整循环
python scripts/tdd_runner.py cycle tests/test_main.py src/main.py
```

**强制规则**（当用户要求 TDD 时）：
1. 先编写测试用例
2. 运行 `tdd_runner.py red` → 确认测试失败（红灯 ✓）
3. 编写实现代码
4. 运行 `tdd_runner.py green` → 确认测试通过（绿灯 ✓）
5. 重构代码，保持绿灯

### 运行时异常上下文注入（v10.6 新增）

**脚本**：`scripts/run_with_context.py`

**功能**：运行脚本，捕获异常时收集局部变量快照 + traceback + 修复建议

**用法**：
```bash
# 运行脚本，异常时输出完整上下文
python scripts/run_with_context.py src/main.py

# 带参数
python scripts/run_with_context.py src/main.py --arg1 val1
```

**输出内容**：
- 异常类型和消息
- 异常位置（文件:行号:源代码）
- 调用栈
- 异常点局部变量快照（类型、值、长度等）
- 异常链（cause/context）
- 修复建议提示

**强制规则**：
- 代码运行失败时，使用 `run_with_context.py` 替代直接运行
- 根据输出的局部变量和修复建议定位根因
- 修复后重新运行验证

### 性能基准对比（v10.8 新增）

**脚本**：`scripts/benchmark_runner.py`

**功能**：对性能敏感函数生成 2+ 种实现方案，自动跑分对比，选择最优。

**用法**：
```bash
# 从 JSON 配置文件运行
python scripts/benchmark_runner.py run config.json

# JSON 输出
python scripts/benchmark_runner.py run config.json --format json

# 覆盖超时
python scripts/benchmark_runner.py run config.json --timeout 60
```

**JSON 配置格式**：
```json
{
  "name": "list_dedup",
  "setup": "import random; data = [random.randint(0, 100) for _ in range(10000)]",
  "snippets": [
    {"name": "dict_from_keys", "code": "list(dict.fromkeys(data))"},
    {"name": "seen_set", "code": "seen = set(); [x for x in data if x not in seen and not seen.add(x)]"}
  ],
  "iterations": 1000,
  "warmup": 10,
  "validate": "assert sorted(r1) == sorted(r2)",
  "edge_cases": [
    {"name": "empty", "setup": "data = []"},
    {"name": "single", "setup": "data = [42]"}
  ],
  "timeout_per_snippet": 30
}
```

**性能指标**：
- **中位数**（主决策指标，天然抗异常值）
- **P95**（尾部延迟）
- **标准差**（稳定性判断）
- **内存峰值**（tracemalloc 估算值）

**三级正确性验证**：
- V1: 默认 `==` 比较
- V2: 自定义 `validate` 表达式（`r1`, `r2` 代表两个方案输出）
- V3: 边界用例 `edge_cases`（空输入、单元素、极端值）

**触发条件**：
- **AUTO_TRIGGER**: layered_validate L3 测试中执行时间 > 1s
- **SUGGEST**: 用户明确要求性能优化 / 循环 > 1000 次 / 处理大数据集

**强制规则**：
- 性能敏感函数必须生成至少 2 种实现
- 所有方案必须通过正确性验证（含边界用例）
- 选择中位数最快的方案，除非有明确理由选择其他
- 输出 benchmark 报告供用户确认

**错误处理**：
- `SYNTAX_ERROR`: 代码语法错误，跳过该方案
- `TIMEOUT`: 执行超时（>timeout_per_snippet），跳过
- `OOM`: 内存溢出，跳过
- `VALIDATE_ERROR`: 验证函数本身报错，提示用户检查

**局限性**：
- tracemalloc 无法跟踪子进程内存，多线程场景统计可能偏低
- v10.8 仅支持 Python，JS/TS 为实验性
- 不提供统计显著性检验（如需精确统计建议使用 pytest-benchmark）

### 依赖影响分析（v10.8 新增）

**脚本**：`scripts/analyze_impact.py`

**功能**：修改模块后，自动分析影响范围，只跑相关测试以加速验证。

**用法**：
```bash
# 分析单个文件
python scripts/analyze_impact.py src/utils.py

# 限制 BFS 深度（仅直接依赖）
python scripts/analyze_impact.py src/utils.py --depth 1

# 分析 git diff（自动获取修改文件）
python scripts/analyze_impact.py --git-diff

# 分析并直接运行测试
python scripts/analyze_impact.py --git-diff --run-tests

# JSON 输出
python scripts/analyze_impact.py src/utils.py --format json

# 指定项目根目录
python scripts/analyze_impact.py src/utils.py --root /path/to/project

# 依赖提取级别（L1=AST, L2=+正则, L3=+文件名）
python scripts/analyze_impact.py src/utils.py --level L2
```

**核心原理**：
- AST 解析 import 构建有向依赖图
- 在**反向依赖图**上 BFS（谁依赖我 = 修改后会影响谁）
- 三级测试映射确定受影响测试

**三级测试映射**：
| 级别 | 策略 | 示例 |
|------|------|------|
| M1 精确匹配 | `src/foo/bar.py` → `tests/**/test_bar.py` | src/utils/parser.py → tests/test_parser.py |
| M2 目录匹配 | `src/foo/` → `tests/foo/` | src/utils/ → tests/utils/ |
| M3 反向依赖 | test_a.py import 了 src/utils.py → 受影响 | tests/test_api.py imports utils |
| 兜底 | 找不到对应测试 → 提示全量运行 | — |

**触发条件**：
- 修改了共享模块（utils、config、types 等）→ 自动触发
- 不确定修改是否影响其他模块 → 建议触发

**与 layered_validate 集成**：
- L3 发现修改文件后，自动调用 analyze_impact 给出建议
- **实际执行由用户确认**（避免虚假安全感）

**强制规则**：
- 修改共享模块后，必须运行 `analyze_impact.py` 确定影响范围
- 只运行受影响的测试，不跑全量测试
- 影响范围超过 10 个测试文件时，先跑直接依赖，再跑间接依赖
- 使用 `--git-diff` 可自动分析当前未提交的修改

**大项目优化**：
- 依赖图缓存到 `.impact_cache.json`（文件修改时间戳校验，增量更新）
- `--depth N` 控制 BFS 深度（默认全图，不静默截断）
- >1000 文件时显示警告，让用户确认是否限制深度

### 差异对比自审

**触发条件**：修改现有文件后

**强制流程**：
1. 使用 `git diff` 查看变更
2. 自我审视变更合理性：
   - 是否引入了不必要的更改？
   - 是否可能破坏现有功能？
   - 是否符合项目风格？
3. 发现问题 → 修正后再输出

**示例**：
```bash
git diff src/main.py
```

**审视清单**：
- [ ] 变更是否最小化（只改必要的）？
- [ ] 是否保留了原有功能？
- [ ] 是否遵循项目编码规范？
- [ ] 是否有遗漏的边界情况？

## 代理系统

7 个专业代理，按需选择：

| 代理 | 职责 | 触发场景 |
|------|------|----------|
| code-reviewer | 代码质量 + YAGNI 检查 | "审查代码"、"review" |
| security-auditor | 漏洞 + 凭证 + CWE | "安全检查"、"漏洞" |
| test-engineer | 覆盖率 + 用例生成 | "写测试"、"覆盖率" |
| architecture-critic | 模块 + 依赖 + 扩展性 | "架构审查"、"模块设计" |
| performance-analyst | 复杂度 + 资源 + 并发 | "性能审查"、"瓶颈" |
| maintainability-reviewer | 命名 + 复杂度 + 债务 | "可维护性"、"技术债务" |
| documentation-checker | API 文档 + 注释 | "文档检查"、"注释" |

### 代理职责矩阵（v10.1 新增）

避免重复审查，各代理独占检查项：

| 检查项 | 主责代理 | 协助代理 |
|--------|----------|----------|
| 代码风格/命名 | code-reviewer | maintainability-reviewer |
| 逻辑正确性 | code-reviewer | - |
| 安全漏洞/CWE | security-auditor | - |
| 硬编码凭证 | security-auditor | code-reviewer |
| 测试覆盖率 | test-engineer | - |
| 模块耦合度 | architecture-critic | maintainability-reviewer |
| 算法复杂度 | performance-analyst | - |
| 技术债务评估 | maintainability-reviewer | architecture-critic |
| API 文档完整性 | documentation-checker | - |

**分层过滤**（v10.1 改进）：
- 先快速扫描安全 critical 问题
- 若发现 → 立即中断并通知用户，不必等其他代理完成
- 若无 → 继续完整审查流程

详细代理定义：`read agents/*.yaml`

### 语言专属审查（v10.3 新增）

审查代码时，系统会根据文件扩展名自动选择语言专属 reviewer：

| 扩展名 | 专属 Reviewer | 审查重点 |
|--------|---------------|----------|
| .py | python-reviewer | PEP 8、类型注解、Pythonic 惯用法、安全 |
| .ts/.tsx/.js/.jsx | typescript-reviewer | 类型安全、React 最佳实践、异步处理 |
| .go | go-reviewer | goroutine、channel、错误处理 |
| .rs | rust-reviewer | 所有权、生命周期、unsafe |

**语言路由规则**：
- `review-orchestrator.py --auto-select` 自动检测文件扩展名
- 语言专属 reviewer 与通用 code-reviewer 并行工作
- 审查报告合并输出，按文件+行号归组

**示例**：
```bash
# 审查 Python 代码，自动选择 python-reviewer + code-reviewer
python scripts/review-orchestrator.py \
  --files "src/main.py" \
  --auto-select
```

## 迭代循环

3 种模式：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| fixed | 固定次数 | 已知需要 N 轮 |
| max | 最大次数 + 完成条件 | 有明确完成标准 |
| adaptive | 根据改进幅度动态调整 | 不确定需要多少轮 |

### 自适应模式度量标准（v10.1 新增）

**强制要求**：使用 adaptive 模式时，必须设置至少一个可度量指标：
- 响应时间（p50/p95/p99）
- 内存峰值
- 代码行数减少比例
- 测试通过率
- 自定义指标（通过 regex 提取）

**度量方式**：
```bash
python scripts/loop-controller.py init \
  --name "性能优化" \
  --mode adaptive \
  --metric "response_time_p95" \
  --threshold "0.1"  # 改进幅度 < 10% 时停止
```

**回退规则**：若用户未提供可度量指标，自动回退到 max 模式并提示。

### 完成条件类型

| 类型 | 说明 | 示例 |
|------|------|------|
| regex | 正则匹配输出 | `--condition "regex:All tests passed"` |
| file | 文件存在 | `--condition "file:output/result.json"` |
| file-changed | 文件内容变化 | `--condition "file-changed:src/main.py"` |
| llm | LLM 判断（v10.1 规范） | 封闭性问题 + JSON 布尔值返回 |

**LLM 完成条件规范**（v10.1 新增）：
- 必须基于封闭性问题（如"代码是否通过所有测试？"）
- 返回格式：`{"complete": true/false, "reason": "..."}`
- 禁止开放式问题（如"代码是否足够好？"）

控制器：`python scripts/loop-controller.py init --name "task" --mode max --max 10`

### 反事实解释修复法（v10.6 新增）

**触发条件**：同一错误连续修复失败 2 次

**强制流程**：
1. 停止自动修复
2. 输出自然语言解释：
   ```
   我认为之前的修复无效是因为：
   - 第 1 次修复尝试：[描述] - 失败原因：[分析]
   - 第 2 次修复尝试：[描述] - 失败原因：[分析]
   - 根本原因可能是：[推断]
   ```
3. 基于该解释生成新的修复方案
4. 验证新方案

**目的**：避免盲目试错，强制模型理解错误根因后再修复。

**示例**：
```
错误：IndexError: list index out of range

第 1 次尝试：添加边界检查 if i < len(lst)
失败原因：检查位置错误，在访问后才检查

第 2 尝试：在访问前添加 try-except
失败原因：异常被吞掉，未处理根本问题

根本原因：列表为空时不应进入循环，需检查列表是否为空
```

### De-Sloppify 清理轮次（v10.3 新增）

LLM 编码常产生"冗余代码"（测试语言特性、过度防御、console.log 等）。
De-Sloppify 模式在实现轮次之间插入清理轮次，保持代码简洁。

**执行顺序**（interval=2 为例）：
```
iter 1: 实现功能
iter 2: 实现功能
iter 3: 清理轮次（de-sloppify）
iter 4: 实现功能
iter 5: 实现功能
iter 6: 清理轮次
...
```

**使用方法**：
```bash
# 启用 De-Sloppify
python scripts/loop-controller.py init \
  --name "功能开发" \
  --mode max --max 9 \
  --sloppify \
  --sloppify-interval 2
```

**清理轮次聚焦**：
- 删除类型系统已保证的冗余运行时检查
- 删除过度防御性的错误处理
- 删除 console.log / 注释掉的代码
- 删除未使用的导入和变量
- 简化冗余的条件判断

**check 命令输出**：
```json
{
  "action": "check",
  "should_continue": true,
  "iteration": 2,
  "is_sloppify_round": true,
  "sloppify_focus": [
    "删除未使用的导入和变量",
    "删除 console.log / 注释掉的代码",
    ...
  ]
}
```

## 审查编排

多代理并行审查使用编排脚本：

```bash
# 基本用法
python scripts/review-orchestrator.py \
  --files "src/main.py" \
  --agents "code-reviewer,security-auditor"

# 自动选择代理 + JSON 输出（v10.1）
python scripts/review-orchestrator.py \
  --files "src/main.py" \
  --auto-select \
  --output json

# 分层过滤：先扫描安全 critical（v10.1）
python scripts/review-orchestrator.py \
  --files "src/" \
  --fast-fail  # 发现 critical 立即中断
```

**输出格式**（v10.1 改进）：
- 默认：人类可读的 Markdown 报告
- `--output json`：结构化 JSON，便于自动化集成

## Hook 系统

事件类型：

| 事件 | 触发时机 |
|------|----------|
| PreExec | exec 命令执行前 |
| PostExec | exec 命令执行后 |
| Stop | 会话结束前（迭代循环用） |

Hook 脚本位于 `hooks/` 目录，从 stdin 读取 JSON 事件数据，输出 JSON 决策。

## 渐进式披露

核心指令在 SKILL.md（本文件），详细参考按需加载：

- Hook 系统详情 → `references/hook-system.md`
- 代理系统详情 → `references/agent-system.md`
- 迭代模式详情 → `references/iteration-patterns.md`
- 安全模式详情 → `references/security-patterns-detail.md`
- 工作流示例 → `references/workflow-examples.md`
- **外部代理委派** → `references/external-agents.md`（Codex/Claude Code/Git Worktree 并行）

## 文件结构

```
coding-framework/
├── SKILL.md                          # 本文件（编排器）
├── .coding-framework.yml             # 配置文件（v10.1 新增）
├── CONTRIBUTING.md                   # 扩展指南（v10.1 新增）
├── agents/                           # 7 个子代理定义
│   ├── code-reviewer.yaml
│   ├── security-auditor.yaml
│   ├── test-engineer.yaml
│   ├── architecture-critic.yaml
│   ├── performance-analyst.yaml
│   ├── maintainability-reviewer.yaml
│   └── documentation-checker.yaml
├── hooks/                            # 3 个钩子脚本
│   ├── pre-exec-check.sh
│   ├── post-exec-log.sh
│   └── stop-iteration.sh
├── rules/                            # 4 个规则文件
│   ├── security-rules.md
│   ├── security-patterns.md
│   ├── coding-standards.md
│   └── review-checklist.md
├── scripts/                          # 9 个工具脚本
│   ├── loop-controller.py
│   ├── review-orchestrator.py
│   ├── check-environment.py          # 环境检查（v10.2 新增）
│   ├── static_analysis.py            # 静态分析（v10.7 新增）
│   ├── layered_validate.py           # 分层验证栈（v10.7 新增）
│   ├── tdd_runner.py                 # TDD 流程（v10.7 新增）
│   ├── run_with_context.py           # 异常上下文注入（v10.7 新增）
│   ├── benchmark_runner.py           # 性能基准对比（v10.8 新增）
│   └── analyze_impact.py             # 依赖影响分析（v10.8 新增）
└── references/                       # 6 个参考文档
    ├── hook-system.md
    ├── agent-system.md
    ├── iteration-patterns.md
    ├── security-patterns-detail.md
    ├── workflow-examples.md
    └── external-agents.md
```

## 配置（v10.1 新增）

通过 `.coding-framework.yml` 自定义行为：

```yaml
# 安全规则
security:
  enabled: true
  fast_fail: true  # 发现 critical 立即中断

# 代理配置
agents:
  default_model: sonnet
  confidence_thresholds:
    critical: 50
    high: 70
    medium: 80
    low: 90

# 迭代循环
iteration:
  default_mode: max
  heartbeat_timeout: 300  # 秒

# 日志
logging:
  level: info  # debug/info/warn/error
  format: jsonl
  path: .coding-framework/logs/
```

## 扩展机制（v10.1 新增）

**新增代理**：
1. 在 `agents/` 下创建 `your-agent.yaml`
2. 在 `.coding-framework.yml` 中注册
3. 详见 `CONTRIBUTING.md`

**新增安全模式**：
1. 在 `rules/security-patterns.md` 中添加模式定义
2. 在 `rules/security-rules.md` 中添加匹配规则
3. pre-exec-check.sh 自动加载

**新增迭代模式**：
1. 在 `scripts/loop-controller.py` 中添加模式处理逻辑
2. 更新 `references/iteration-patterns.md`

## 文档加载决策表（v10.2 新增）

根据用户输入关键词自动预加载对应参考文档：

| 关键词 | 预加载文档 | 说明 |
|--------|------------|------|
| 安全、漏洞、hook、pre-exec | `references/security-patterns-detail.md` | 安全模式详情 |
| 代理、审查、review、agent | `references/agent-system.md` | 代理系统说明 |
| 迭代、循环、loop、iterate | `references/iteration-patterns.md` | 迭代模式说明 |
| Codex、Claude Code、worktree | `references/external-agents.md` | 外部代理委派 |
| 示例、workflow、怎么用 | `references/workflow-examples.md` | 工作流示例 |
| hook 事件、stdin、JSON | `references/hook-system.md` | Hook 系统说明 |

**加载规则**：
- 匹配到关键词时，自动 `read` 对应文档的前 100 行作为上下文
- 多个关键词匹配时，按优先级加载（安全 > 代理 > 迭代 > 外部 > 示例 > hook）
- 最多预加载 2 个文档，避免 token 浪费

## 依赖与环境要求（v10.2 新增）

### 必需依赖

| 依赖 | 版本 | 用途 | 安装方式 |
|------|------|------|----------|
| Python | 3.10+ | loop-controller.py, review-orchestrator.py | 系统包管理器 |
| Git | 2.28+ | worktree 并行、版本控制 | 系统包管理器 |
| bash | 4.0+ | hook 脚本执行 | Git Bash (Windows) / 系统自带 |

### 可选依赖

| 依赖 | 版本 | 用途 | 安装方式 |
|------|------|------|----------|
| jq | 1.6+ | hook 脚本 JSON 解析（推荐） | `scripts/install_jq_rg.ps1` |
| Claude Code | latest | 外部代理委派 | `npm install -g @anthropic-ai/claude-code` |
| Codex | latest | 外部代理委派 | `npm install -g @openai/codex` |

### 支持平台

| 平台 | 状态 | 备注 |
|------|------|------|
| macOS | ✅ 完全支持 | 原生 bash |
| Linux | ✅ 完全支持 | 原生 bash |
| Windows | ✅ 支持 | 需安装 Git Bash |

### 环境检查脚本

```bash
# 检查必需依赖
python scripts/check-environment.py

# 输出示例:
# ✅ Python 3.11.5
# ✅ Git 2.42.0
# ✅ bash 5.2.15
# ⚠️ jq 未安装（hook 脚本将使用 bash fallback）
```

## Git 集成与回滚（v10.2 新增）

迭代改进可能产生破坏性修改，loop-controller 集成 Git 自动回滚：

### 自动提交

```bash
# 初始化时启用自动提交
python scripts/loop-controller.py init \
  --name "性能优化" \
  --mode max --max 10 \
  --auto-commit

# 每次迭代前自动创建临时提交:
# git commit -m "chore: pre-iteration snapshot (loop: 性能优化, iter: 3)"
```

### 回滚

```bash
# 回滚到指定迭代
python scripts/loop-controller.py rollback --name "性能优化" --to 2

# 回滚到上一次迭代
python scripts/loop-controller.py rollback --name "性能优化" --prev

# 回滚到循环开始前
python scripts/loop-controller.py rollback --name "性能优化" --initial
```

### 回滚机制

1. 每次迭代前创建 Git tag: `loop/{name}/iter/{n}`
2. 回滚时 `git checkout` 到对应 tag
3. 保留所有迭代历史，可随时恢复

## 本能学习系统（v10.4 新增）

从编码实践中学习模式/规则，自动积累和优化编码本能（instincts）。

### 核心概念

| 概念 | 说明 |
|------|------|
| Instinct | 从编码实践中学习到的模式/规则 |
| Confidence | 置信度（0.0-1.0），基于观察次数和一致性 |
| Scope | global（全局）或 project（项目级） |
| Domain | 领域标签（code-style, error-handling, performance 等） |

### 置信度演化

| 观察次数 | 初始置信度 |
|----------|------------|
| 1-2 次 | 0.3 |
| 3-5 次 | 0.5 |
| 6-10 次 | 0.7 |
| 11+ 次 | 0.85 |

- **增强**：每次确认 +0.05（上限 1.0）
- **衰减**：每次矛盾 -0.1，每周不使用 -0.02

### 使用方法

```bash
# 记录一个新的本能
python scripts/instinct-manager.py record \
  --trigger "遇到 API 超时" \
  --action "添加重试机制和超时设置" \
  --domain "error-handling"

# 查询高置信度本能
python scripts/instinct-manager.py query \
  --domain "code-style" \
  --min-confidence 0.6

# 衰减长期未使用的本能
python scripts/instinct-manager.py decay

# 晋升项目本能到全局（需 2+ 项目 confidence >= 0.8）
python scripts/instinct-manager.py promote --id "instinct-xxx"

# 列出所有本能
python scripts/instinct-manager.py list --all
```

### 项目隔离

本能按项目隔离存储，避免不同项目的编码习惯互相污染：

```
instincts/
  global/          # 全局本能（跨项目通用）
  projects/        # 项目级本能
    {project_id}/  # 基于 git remote hash
```

### 晋升机制

当同一 instinct 在 2+ 项目中 confidence >= 0.8 时，可晋升为 global：

```bash
python scripts/instinct-manager.py promote --id "instinct-xxx"
```

## 工作流编排（v10.4 新增）

支持完整的开发生命周期编排：分类 → 规划 → 执行 → 审查 → 优化。

### 模式 5：工作流编排

触发：用户要求完整开发一个功能 / "develop" / "实现这个功能"

流程：
1. **任务分类** → frontend / backend / fullstack
2. **规划阶段** → 上下文检索 + 实现计划（只读）
3. **用户确认计划**
4. **执行阶段** → 按计划修改代码
5. **审查阶段** → 多代理并行审查（复用模式 2）
6. **优化阶段** → 根据审查结果修复
7. **交付确认**

### 任务分类路由

| 任务类型 | 特征关键词 | 主责代理 | 协助代理 |
|----------|------------|----------|----------|
| frontend | component, UI, 页面, 组件, 样式 | typescript-reviewer | code-reviewer |
| backend | API, database, 接口, 算法 | python-reviewer | security-auditor |
| fullstack | 默认 | code-reviewer | ts-reviewer + py-reviewer |

### 使用方法

```bash
# 分类任务
python scripts/workflow-orchestrator.py classify \
  --description "实现用户登录页面" \
  --files "src/pages/Login.tsx"

# 生成实现计划（只读）
python scripts/workflow-orchestrator.py plan \
  --description "实现用户登录功能" \
  --files "src/pages/Login.tsx,src/api/auth.py"

# 执行计划
python scripts/workflow-orchestrator.py execute --plan "plans/plan-xxx.json"

# 审查代码
python scripts/workflow-orchestrator.py review \
  --files "src/pages/Login.tsx" \
  --auto-select

# 完整流水线
python scripts/workflow-orchestrator.py pipeline \
  --description "实现用户登录功能" \
  --files "src/"
```

### 专属代理

| 代理 | 审查重点 |
|------|----------|
| frontend-reviewer | UI/UX、组件设计、响应式布局、可访问性、动画 |
| backend-reviewer | API 设计、数据库操作、算法、业务逻辑、安全 |

### 规划与执行分离

- **规划阶段**：只读，不修改代码，生成实现计划
- **执行阶段**：按计划修改代码
- **好处**：避免"边想边做"的质量问题，用户可先审核计划

## DAG 任务调度（v10.5 新增）

将大需求分解为有依赖关系的任务 DAG（有向无环图），按拓扑排序和复杂度分层执行。

### 核心概念

| 概念 | 说明 |
|------|------|
| WorkUnit | 一个独立的工作单元（任务） |
| Dependency | 任务间的依赖关系（前置任务） |
| Complexity | 复杂度等级（trivial/small/medium/large） |
| Stage | 执行阶段（plan/execute/review/optimize） |

### 复杂度分层与质量流水线

不同复杂度走不同深度的质量流水线：

| 复杂度 | 权重 | 质量流水线 | 审查深度 | 预计耗时 |
|--------|------|------------|----------|----------|
| trivial | 1 | execute | 无 | 5 分钟 |
| small | 2 | execute → review | 轻量 | 15 分钟 |
| medium | 4 | plan → execute → review | 标准 | 30 分钟 |
| large | 8 | plan → execute → review → optimize | 深度 | 60 分钟 |

**设计原则**：
- trivial/small 任务跳过规划阶段，直接执行
- large 任务需要完整的规划-执行-审查-优化流水线
- 审查深度随复杂度递增，避免过度审查简单任务

### 使用方法

```bash
# 1. 创建 DAG
python scripts/dag-scheduler.py create \
  --name "user-auth" \
  --description "实现用户认证功能"

# 2. 添加任务（指定复杂度）
python scripts/dag-scheduler.py add \
  --dag "user-auth" \
  --id "db-model" \
  --description "创建用户表模型" \
  --complexity "small"

python scripts/dag-scheduler.py add \
  --dag "user-auth" \
  --id "api-endpoints" \
  --description "实现登录/注册 API" \
  --complexity "medium"

python scripts/dag-scheduler.py add \
  --dag "user-auth" \
  --id "frontend-login" \
  --description "实现登录页面" \
  --complexity "large"

# 3. 添加依赖关系
python scripts/dag-scheduler.py depend \
  --dag "user-auth" \
  --from "api-endpoints" \
  --to "db-model"

python scripts/dag-scheduler.py depend \
  --dag "user-auth" \
  --from "frontend-login" \
  --to "api-endpoints"

# 4. 生成执行计划（拓扑排序）
python scripts/dag-scheduler.py schedule --dag "user-auth"

# 5. 获取下一个可执行任务
python scripts/dag-scheduler.py next --dag "user-auth"

# 6. 更新任务状态
python scripts/dag-scheduler.py update \
  --dag "user-auth" \
  --id "db-model" \
  --status "completed"

# 7. 查看 DAG 状态
python scripts/dag-scheduler.py status --dag "user-auth"
```

### 执行流程

```
1. create DAG → 定义需求
2. add tasks → 分解为工作单元（指定复杂度）
3. depend → 建立依赖关系
4. schedule → 拓扑排序，生成执行顺序
5. next → 获取下一个可执行任务
   └─ 根据复杂度自动匹配质量流水线
   └─ trivial: 直接执行
   └─ small: 执行 + 轻量审查
   └─ medium: 规划 + 执行 + 标准审查
   └─ large: 规划 + 执行 + 深度审查 + 优化
6. update → 更新任务状态
7. 循环 5-6 直到所有任务完成
```

### 并行执行

无依赖关系的任务可以并行执行：

```bash
# 查看哪些任务可以并行
python scripts/dag-scheduler.py schedule --dag "feature-x"
# 输出中 can_parallel: true 的任务可并行
```

### 目录结构

```
dags/
  {dag-name}.json    # DAG 定义文件
```

## 版本历史

| 版本 | 日期 | 主要变更 |
|------|------|----------|
| 10.5.0 | 2026-07-01 | ECC Phase 3: DAG任务调度 + 复杂度分层质量流水线 |
| 10.4.0 | 2026-07-01 | ECC Phase 2: 本能学习系统 + 工作流编排 + 前后端专属代理 |
| 10.3.0 | 2026-07-01 | ECC Phase 1: 语言专属审查(Python/TS reviewer) + De-Sloppify 清理轮次 |
| 10.2.0 | 2026-06-29 | P2 改进：文档加载决策表、环境检查、Git 回滚 |
| 10.1.0 | 2026-06-29 | P0/P1 改进：置信度分级、合并策略、并发保护、输入校验 |
| 10.0.0 | 2026-06-28 | 初始版本：4 模式 + 7 代理 + 25 安全模式 |
