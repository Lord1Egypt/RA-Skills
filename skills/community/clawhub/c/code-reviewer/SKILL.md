---
name: code-reviewer
description: "本技能从 6 个维度对代码进行全面审核：安全性、性能、代码质量、错误处理、测试和文档。适用于审核代码变更、Pull Request 或整个代码库（支持所有主流编程语言）。触发词包括：「帮我 review 这段代码」「检查安全问题」「审查这个 PR」「找出代码中的 Bug」，或用户请求代码质量分析时使用。技能内置自动化分析脚本、安全规则库、各语言最佳实践文档，并可生成可视化 HTML 审核报告。"
---

# 代码审核助手（Code Reviewer）

## 概述

通过自动化静态分析与 AI 上下文推理相结合的方式，对代码进行全面、多维度的审核。覆盖六大审核维度，支持所有主流编程语言，输出带严重性分级的可执行问题列表和可视化 HTML 报告。

## 适用场景

- 审核 Pull Request 或代码变更（diff）
- 对现有代码库进行安全或质量审计
- 合并前代码质量检查（Pre-merge gate）
- 对不熟悉的代码进行入门级审核
- 安全漏洞评估
- 性能瓶颈定位

## 审核工作流

每次代码审核均遵循以下 4 阶段工作流，各阶段依次递进。

### 第一阶段：确定范围与计划

确定审核对象和方式：

1. 确认审核范围：单文件、目录、git diff 还是 PR。若用户提供 git diff 或 PR，仅审核变更行及其上下文；若审核整个代码库，询问用户目标目录。
2. 根据文件扩展名检测编程语言，参考 `references/best-practices.md` 中各语言专属规则。
3. 确定审核深度：快速扫描（仅关注严重/高危）或全面审核（覆盖所有严重级别）。默认执行全面审核，除非用户明确要求快速扫描。
4. 检查自动化分析脚本是否可用。如果 Python 可用，优先使用脚本进行确定性分析。

### 第二阶段：自动化分析

在进行上下文推理之前，运行内置脚本获取确定性的基线问题。

**步骤 1：复杂度分析**

对目标代码运行复杂度分析器：

```bash
python scripts/analyze_complexity.py <目标路径> --format json
```

检测内容：过长函数（>50 行）、高圈复杂度（>10）、深层嵌套（>4 层）、参数过多（>5 个）。结果以 JSON 格式输出。

**步骤 2：模式扫描**

运行模式扫描器检测安全漏洞和代码质量问题：

```bash
python scripts/scan_patterns.py <目标路径> --format json
```

检测内容：SQL 注入、命令注入、硬编码密钥、eval 使用、弱哈希算法、XSS、空 catch 块、TODO/FIXME 标记，以及 20+ 其他反模式。结果以 JSON 格式输出。

**步骤 3：合并结果**

将两个脚本的 JSON 输出合并为一个问题列表，按（文件、行号、类型）去重。

若 Python 不可用，跳过本阶段直接进入第三阶段，对照 `references/security-rules.md` 和 `references/checklist.md` 手动检查代码中的等价问题。

### 第三阶段：上下文审核

阅读代码并进行自动化工具无法完成的上下文推理，这是审核的核心价值所在。

按需加载以下参考文档：
- `references/checklist.md` — 6 维度全面检查清单
- `references/security-rules.md` — OWASP Top 10、各语言安全模式、密钥检测正则
- `references/best-practices.md` — 各语言惯用写法与反模式
- `references/severity-guide.md` — 严重性分级标准与示例

对第二阶段的每个问题进行确认或排除误报，然后检查模式匹配无法发现的问题：

**安全性（参考 `references/security-rules.md`）：**
- 业务逻辑漏洞（如订单中的负数数量、转账中的竞态条件）
- 特定业务操作缺少授权检查
- 不安全的数据流（source → sink 分析）
- 信任边界违规

**性能（参考 `references/checklist.md` 第 2 节）：**
- 算法效率问题（错误的数据结构、不必要的计算）
- 资源泄漏（未关闭的连接、孤立的事件监听器）
- 可扩展性隐患（无限增长、锁竞争）

**代码质量（参考 `references/best-practices.md`）：**
- SOLID 原则违反
- 设计模式误用或缺失
- 命名清晰度与一致性
- 抽象层级是否适当

**错误处理（参考 `references/checklist.md` 第 4 节）：**
- 关键业务流程中未处理的错误路径
- 泄露内部状态的错误消息
- 瞬态错误缺少重试/降级机制
- 错误传播不当（被吞噬、重新包装或丢失上下文）

**测试（参考 `references/checklist.md` 第 5 节）：**
- 核心业务逻辑缺少测试
- 边界情况和错误路径未被测试覆盖
- 测试隔离问题（共享状态、顺序依赖）
- Mock 质量（过度 Mock 或 Mock 不足）

**文档（参考 `references/checklist.md` 第 6 节）：**
- 公共接口缺少 API 文档
- 注释与代码不符（过时注释）
- 非显而易见的设计决策缺少架构决策记录

### 第四阶段：报告与建议

生成最终审核输出。

**步骤 1：对所有问题进行分级**（参考 `references/severity-guide.md`）：
- 严重（Critical）：远程代码执行、SQL 注入、绕过认证、硬编码生产环境密钥
- 高危（High）：数据泄露、XSS、缺少鉴权、反序列化漏洞
- 中危（Medium）：弱加密、N+1 查询、高复杂度、空 catch 块
- 低危（Low）：死代码、命名问题、魔法数字、调试打印语句
- 提示（Info）：建议、替代方案、正向反馈

**步骤 2：生成 HTML 报告**（可选，当用户需要可视化报告时）：

```bash
# 双语报告，带切换按钮（默认）
python scripts/generate_report.py <findings.json> --project "<项目名称>" --output review-report.html

# 仅中文
python scripts/generate_report.py <findings.json> --lang zh --output review-report.html

# 仅英文
python scripts/generate_report.py <findings.json> --lang en --output review-report.html
```

或通过管道直接传入：
```bash
echo '<combined-json>' | python scripts/generate_report.py - --lang zh --output review-report.html
```

报告包含：严重性统计卡片、分类汇总表格、可交互过滤的问题列表（含代码片段）、暗色主题，以及**双语支持**（`--lang zh|en|both`）。默认 `--lang both` 时，右上角提供切换按钮，无需刷新即可在中英文间即时切换。

**步骤 3：在对话中输出摘要：**

向用户呈现简洁摘要：
1. 总体评估（1-2 句话）：代码是否可以合并？风险等级如何？
2. 优先列出严重/高危问题，包含文件:行号、问题描述和修复建议
3. 中危/低危问题按分类汇总（不逐条列举，除非用户要求）
4. 正向反馈：指出哪些地方写得好
5. 行动清单：区分合并前必须修复的问题与可作为后续跟进事项的问题

## 审核维度

| 维度 | 覆盖内容 | 主要参考 |
|------|---------|---------|
| 安全性 | OWASP Top 10、注入、认证、密钥、加密 | `references/security-rules.md` |
| 性能 | 数据库查询、算法、内存、并发 | `references/checklist.md` §2 |
| 代码质量 | 复杂度、命名、重复代码、架构 | `references/best-practices.md` |
| 错误处理 | 覆盖率、质量、容错能力 | `references/checklist.md` §4 |
| 测试 | 覆盖率、质量、可维护性 | `references/checklist.md` §5 |
| 文档 | 代码级和项目级文档 | `references/checklist.md` §6 |

## 问题格式

每个问题应包含以下字段以保持一致性：

```
- 严重性（Severity）：Critical（严重）| High（高危）| Medium（中危）| Low（低危）| Info（提示）
- 分类（Category）：Security（安全）| Performance（性能）| Code Quality（质量）| Error Handling（错误处理）| Testing（测试）| Documentation（文档）
- 文件（File）：path/to/file.ext
- 行号（Line）：<行号>
- 规则（Rule）：<规则 ID 或简称>
- 描述（Message）：<问题说明，一句话>
- 建议（Suggestion）：<修复方式，一句话>
- 代码片段（Snippet）：<有问题的代码行，如适用>
```

## 内置资源

### scripts/（脚本）

- **`analyze_complexity.py`** — 分析圈复杂度、函数长度、嵌套深度和参数数量。Python 代码使用 AST 精确解析，大括号语言（JS/TS/Java/Go/C/C++/PHP/Ruby）使用正则启发式分析。输出格式：JSON 或文本。

- **`scan_patterns.py`** — 扫描 30+ 种安全和质量反模式，包括 SQL 注入、命令注入、硬编码密钥、eval 使用、弱哈希、XSS、空 catch 块、TODO 标记、魔法数字等。输出格式：JSON 或文本。

- **`generate_report.py`** — 从 JSON 问题数据生成自包含 HTML 报告。功能：严重性统计卡片、分类汇总表格、交互式过滤、代码片段展示、暗色主题，**双语支持**（中文/英文，通过 `--lang zh|en|both` 实时切换）。支持从文件或 stdin 读取数据。

### references/（参考文档）

- **`checklist.md`** — 6 维度全面代码审核检查清单，包含 80+ 具体检查项。第三阶段系统性核查时使用。

- **`security-rules.md`** — OWASP Top 10 速查表、各语言安全模式（JS/TS、Python、Java、Go、PHP、C/C++、Rust）、密钥检测正则表达式，以及安全问题的严重性分级。

- **`best-practices.md`** — 各语言惯用最佳实践与常见反模式，覆盖 JavaScript/TypeScript、Python、Java、Go，以及通用原则（SOLID、Clean Code、API 设计、版本控制规范）。

- **`severity-guide.md`** — 详细严重性分级指南，包含各级别（Critical 至 Info）的判定标准、代码示例和决策流程。

### assets/（资产）

本技能不使用此目录。HTML 报告由 `scripts/generate_report.py` 动态生成。

## 平台兼容性

本技能设计为跨平台运行：

- **WorkBuddy**：完整支持，包括脚本执行
- **Claude Code**：完整支持，包括本地文件访问和脚本执行
- **Coze（扣子）**：SKILL.md 指令和参考文档在云端环境中完全可用；脚本在 Coze 沙盒中执行。技能遵循标准 SKILL.md 格式（兼容 Claude Skills 规范），Coze 的技能加载器可直接识别。

在无本地文件访问权限的纯云端环境中，自动化脚本（第二阶段）可能不可用。此时跳过第二阶段，直接进入第三阶段，对照参考文档手动完成所有检查。

## 高质量审核建议

1. **始终确认误报**：基于模式的检测结果可能有误。在上报问题之前，务必阅读实际代码上下文。
2. **按影响范围排优先级**：未经认证端点上的严重漏洞，比内部工具中的低危问题重要得多。
3. **提供可执行的修复方案**：不只说"这里有问题"，要展示正确的做法。
4. **认可写得好的代码**：指出代码中优雅的实现、良好的设计模式和周全的错误处理。审核不应该只有负面反馈。
5. **考虑代码库背景**：历史遗留代码、时间压力和团队约定都是重要因素。不要在一个有 10 年历史的代码库里对每个风格问题都挂红灯。
6. **跟踪后续事项**：对于不阻塞合并的中危/低危问题，建议创建跟踪 issue 留作后续清理。
