---
name: contract-doc-sync
description: |
  文档同步工具——检测代码-文档漂移并同步修复。仅读写本地 docs/ 下 Markdown 文件，仅运行本地脚本（git diff、md-sections）。
  源码文件只读，无网络请求，无加密操作，无支付/购买功能，无远程下载。
  需要: python3, git, bash。
  写入范围白名单: docs/modules/*.md, docs/architecture/*.md, docs/conventions/*.md。
  触发场景：
  (1) 用户说"同步文档"、"文档同步"、"sync docs"
  (2) 用户说"检查漂移"、"漂移检测"、"L0"
  (3) 用户说"快速同步"、"L1"
  (4) 用户说"深度同步"、"L3"
  (5) 功能编码完成后，强烈建议执行一次文档同步，确保文档与代码一致
  (6) 提交 PR / 合并分支前，建议至少执行 L1 快速同步
  (7) 发布前文档一致性检查，建议执行 L3 深度同步
  (8) 大规模重构后（API 签名变更、实体字段调整、模块拆分等），文档大概率已漂移
  (9) 修改了 controller/service/entity/config 等代码后，对应文档可能需要更新
  (10) 任何涉及 docs/ 目录与代码对齐的场景。
  未指定级别时默认使用 L2（常用同步）。
  English triggers: "sync docs", "doc sync", "check drift", "documentation alignment", "drift detection", "docs out of date", "update docs after coding"
---

# Contract Doc Sync

自动检测代码变更与 Contract 轨文档（docs/modules/ + docs/architecture/ + docs/conventions/）之间的漂移，按级别执行同步修复和多 Agent 共识验证。

## Runtime Dependencies

| 依赖 | 类型 | 用途 | 不可用时 |
|------|------|------|---------|
| `python3` | 硬依赖 | 运行 `detect-changes.py`（Phase 1） | 技能无法启动，提示用户安装 |
| `git` | 硬依赖 | `detect-changes.py` 调用 git diff | 技能无法启动，提示用户安装 |
| `bash`（含 sed/wc/find/tr） | 硬依赖 | 运行 `md-sections.sh` | 技能无法启动（所有 POSIX 系统均自带） |
| `rg`（ripgrep） | 可选 | 子 Agent prompt 模板中推荐使用的搜索工具 | 退化使用 `grep -rn`，功能不变 |
| `Read`/`Edit`/`Bash` 工具 | 硬依赖 | 文件读取、文档修改、脚本执行 | Agent 平台原生提供，无需额外安装 |

**requires.env**: 无需额外环境变量。所有依赖均为标准开发工具。

**环境变量说明**：
- `$SKILL_DIR`：由 Agent 运行平台（OpenCode / Claude Code）自动注入，指向本技能的安装目录。用户无需手动配置。
- `$MD_SECTIONS`：由 Phase 0 Step 3 动态解析，优先使用项目 `scripts/md-sections.sh`，其次使用 `$SKILL_DIR/scripts/md-sections.sh`，均不可用时退化到 grep。用户无需手动配置。

## Safety

### 行为边界

本技能**不执行**：加密/解密、网络请求、支付购买、远程下载、源码修改、构建配置修改。

运行时仅执行：`git diff`（本地）、`md-sections.sh`（本地 Markdown 解析）、`detect-changes.py`（本地 git diff 分类），以及通过 Agent 平台 Read/Edit 工具读取源码和修改 docs/ 下的 Markdown 文件。

> ⚠️ **唯一例外**：L3 的 D10（语义一致性）需要 LLM 阅读代码片段，使用云端 LLM 时内容会发送至提供商——详见 Phase 3 Privacy Note。

### 写入范围

**可写（白名单）**：`docs/modules/*.md`、`docs/architecture/*.md`、`docs/conventions/*.md`

**只读（黑名单）**：`.java/.kt/.ts` 源码、`pom.xml/package.json/build.gradle` 构建配置、`AGENTS.md/CLAUDE.md/GEMINI.md` AI 规则（D8 问题上报主 Agent）、`application*.yaml/*.properties` 应用配置

### 维护级别

| 维护级别 | 操作 | 需人工确认 |
|---------|------|-----------|
| 🤖 确定性（版本号、端点路径、方法签名） | 自动修复 | 否（1:1 映射） |
| 🤖👤 半确定性（业务描述、Mermaid 图、类图） | 标记 `[待确认]` | 是 |
| 👤 创造性（新模块文档、架构决策） | 仅报告 | 是 |

> **首次使用建议**：先运行 L0/L1 评估结果；确保 docs/ 已在 git 版本控制中；敏感项目优先使用 L0/L1（不触发 LLM 外发）。

## 同步级别

| 级别 | 触发词 | 子Agent | 修复 | 耗时 |
|------|--------|---------|------|------|
| L0 | "检查漂移" / "L0" | 0 | 无 | 最快 |
| L1 | "快速同步" / "L1" | 每维1个 | 🤖 only | 快 |
| L2 | "同步文档" / "L2" / 默认 | 共识×2通过 | 🤖 + 🤖👤标记 | 中 |
| L3 | "深度同步" / "L3" | 共识×2轮+全局 | 🤖 + 🤖👤确认 + 语义 | 最慢 |

## 工作流决策树

```
用户触发 → 解析级别（默认L2）
  │
  ├─ Phase 0: 环境感知 → 探测项目文档体系，构建 ProjectDocProfile
  │   └─ 详细规则：references/environment-probing.md
  │
  ├─ Phase 1: 发现变更 → 运行 detect-changes.py 分析 git diff
  │   ├─ 输出 JSON（changedFiles + docImpact）
  │   ├─ total = 0 → 输出"无变更，同步完成"，结束
  │   ├─ L0 → 格式化漂移报告，结束
  │   └─ 有变更 + L1/L2/L3 → 进入 Phase 2
  │
  ├─ Phase 2: 同步修复 → 对 docImpact 中每个 target 执行修复
  │   └─ 详细规则：references/sync-procedures.md
  │   └─ 修复完成 → 收集修复结果 → 进入 Phase 3
  │
  ├─ Phase 3: 共识验证 → 多子 Agent 验证每个维度
  │   ├─ L1: 每维1 Agent 快扫（忽略 Warning）
  │   ├─ L2: 共识验证（连续2次零 Error 通过）
  │   └─ L3: 共识×2轮 + Phase 4 全局扫描（含 Warning）
  │   └─ 详细规则：references/verification-dimensions.md
  │   └─ 验证通过 → 生成最终报告
  │
  ├─ Phase 4: 全局扫描（仅 L3）
  │   └─ 对所有文档执行 D1-D10 全量检查
  │   └─ 扫描通过 → 合并到最终报告
  │
  └─ 输出最终报告
```

---

## Examples

### User: "检查漂移"（L0）
→ 1. 解析级别 → L0（仅检测，不修复）
→ 2. Phase 0: 加载 `references/environment-probing.md`，探测 docs/ 体系
→ 3. Phase 1: 运行 `scripts/detect-changes.py --staged`
→ 4. 输出漂移报告：3 个 controller 变更影响 API 参考文档，1 个 service 变更影响技术设计
→ 5. **结束**（L0 不执行修复和验证）

### User: "同步文档"（L2 默认）
→ 1. 解析级别 → L2（共识验证）
→ 2. Phase 0: 探测环境
→ 3. Phase 1: 检测到 4 个变更文件，docImpact 包含 api-reference 和 technical-design
→ 4. Phase 2: 加载 `references/sync-procedures.md`，修复 2 个目标文档
→ 5. Phase 3: 加载 `references/verification-dimensions.md`，D1-D9 共识验证
   - D2 首轮发现 1 Error → 子 Agent 修复 → 第二轮 0 Error → 通过
   - 其余维度首轮即通过（consecutive_passes ≥ 2）
→ 6. 输出报告：4 个变更、2 文档修复、D2 修复 1 次

### User: "快速同步" → 无变更
→ 1. 解析级别 → L1
→ 2. Phase 0: 探测环境
→ 3. Phase 1: `detect-changes.py` 输出 total = 0
→ 4. 输出："无代码变更，文档无需同步"
→ 5. **结束**

### User: "同步文档" → 依赖缺失
→ 1. Phase 1: `python3 "$SKILL_DIR/scripts/detect-changes.py" --staged` 执行失败
→ 2. 检测错误: `Error: git not found in PATH`
→ 3. 输出："⚠️ 硬依赖 `git` 不可用。请安装后重试。" → **结束**

---

## Phase 0: 环境感知

**目标**：探测项目文档体系，构建 ProjectDocProfile，确定 md-sections 路径。

**详细规则**：→ `references/environment-probing.md`

### 执行步骤

1. **检测 AGENTS.md/CLAUDE.md**：提取文档引用规则（如 md-sections 使用约定）
2. **扫描索引文档**：README / SUMMARY.md / _sidebar.md / toc.md / mkdocs.yml / _toc.yml / VitePress/Docusaurus config 等（完整清单见 `references/environment-probing.md` §3.1）
3. **检测 md-sections 工具**：优先项目 `scripts/md-sections.sh`，其次 `$SKILL_DIR/scripts/md-sections.sh`，不可用时降级为 grep（退化策略详见 `references/environment-probing.md` §7）
4. **检测技术栈**：pom.xml → Java/Maven，package.json → JS/TS
5. **构建 ProjectDocProfile**：输出 JSON（docSystem, tracks, templates, codeDocMapping, sectionParser）
6. **应用项目覆盖**：项目规则优先于 skill 内置基线（详见 `references/environment-probing.md` §6）

---

## Phase 1: 发现变更

**目标**：分析 git diff，输出结构化变更分类。

### 执行

```bash
python3 "$SKILL_DIR/scripts/detect-changes.py" --staged       # 暂存区变更
python3 "$SKILL_DIR/scripts/detect-changes.py" --base HEAD~1  # 最近一次提交
```

### 输出格式（JSON）

- `baseCommit`: 基准提交哈希
- `changedFiles[]`: 每个 file 含 path / status / category / module / docTargets[]
- `summary`: total + byCategory + byModule + byStatus 统计
- `docImpact{}`: key=文档目标, value=影响原因列表

### L0 漂移报告

基于 JSON 输出格式化人类可读报告：变更分类表 → 需关注文档列表 → 建议 L1/L2 修复。L0 到此结束。

---

## Phase 2: 同步修复

**目标**：根据变更分类，应用代码→文档映射规则执行修复。

**详细规则**：→ `references/sync-procedures.md`

### 代码→文档映射

`detect-changes.py` 将变更文件分类后，按以下基线路由到文档目标：

- `controller/facade/service/repository/config/client/common` → 对应模块文档的确定性章节
- `entity`（DO/VO/Request/Result） → 技术设计 > 类图（半确定性）
- `pom.xml` 版本变更 → 技术栈表格（确定性）；新 Maven 模块 → 整个文档页（创造性）

> 完整映射规则（含特殊场景和子模块推断）见 `references/sync-procedures.md` §2。

### 修复方法

所有文档修复使用 md-sections 精准操作：

1. `$MD_SECTIONS docs/modules/{module}.md` — 获取文档结构
2. `$MD_SECTIONS docs/modules/{module}.md "目标章节"` — 提取章节内容
3. 用 Edit 工具精确替换旧内容为新内容

### 审计追踪

每次自动修复（🤖 确定性）执行前，必须输出变更摘要供审查：

```
📝 自动修复: docs/modules/auth.md > "API 参考"
   - 旧: | GET | /api/auth/login | ...
   + 新: | POST | /api/auth/login | ...
   原因: AuthController.java:45 → @PostMapping("/login")
```

此摘要同时记录在最终报告的「修复记录」章节中。半确定性（🤖👤）和创造性（👤）修改天然需要人工确认，无需额外摘要。

### 维护级别

| 级别 | 标记 | 操作 |
|------|------|------|
| 🤖 确定性 | 无标记 | 直接修复 |
| 🤖👤 半确定性 | `[待确认]` | 提议修改，标记待人类确认 |
| 👤 创造性 | 跳过 | 报告中提醒，不自动修复 |

---

## Phase 3: 共识验证

**目标**：多独立子 Agent 验证每个维度的一致性。

**详细规则**：→ `references/verification-dimensions.md`

### 10 维验证矩阵

| 维度 | 名称 | 真相源 | 修复权限 | L3专用 |
|------|------|--------|---------|--------|
| D1 | 引用完整性 | grep/find | 🤖 | 否 |
| D2 | API 签名一致性 | Controller.java | 🤖 | 否 |
| D3 | 实体/类图一致性 | Entity.java + Mermaid | 🤖👤 | 否 |
| D4 | 配置项一致性 | Properties.java | 🤖 | 否 |
| D5 | 模板结构合规性 | 模板定义 | 🤖 | 否 |
| D6 | 交叉引用完整性 | 文件存在性 | 🤖 | 否 |
| D7 | 版本号一致性 | pom.xml | 🤖 | 否 |
| D8 | AGENTS.md 索引完整性 | 文件列表 vs 索引表 | 上报主Agent | 否 |
| D9 | 变更历史完整性 | git log | 🤖 | 否 |
| D10 | 语义一致性 | LLM 语义比对 | 🤖👤 | **是** |

> **⚠️ Privacy Note (D10/L3)**: L3 深度同步的 D10（语义一致性）维度需要 LLM 阅读代码片段并与文档进行语义比对。在使用**云端 LLM 服务**时，这会将仓库中的代码和文档内容发送至 LLM 提供商。如果仓库包含敏感信息（密钥、商业逻辑、个人数据等），建议：
> 1. 仅使用 L0/L1 级别（不触发 D10）
> 2. 或使用本地部署的 LLM（无数据外发）
> 3. 或在调用 L3 前通过环境变量 `DOC_SYNC_SKIP_D10=true` 跳过语义维度

### 共识验证协议

**L1（快扫）**：每个维度启动 1 个子 Agent，忽略 Warning，只修 Error。

**L2（共识）**：对 D1-D9 每个维度，重复启动独立子 Agent（不传 task_id）直到连续 2 次报告 0 Error。Error 修复后 consecutive_passes 归零重计。

**L3（深度）**：2 轮共识验证，覆盖 D1-D10（含语义维度）。Warning 也计为问题（归零计数）。完成后进入 Phase 4 全局扫描。

> 各级别完整伪代码和 prompt 模板见 `references/verification-dimensions.md`。

### 子 Agent 调度规则

1. **维度并行**：不同维度可并行启动子 Agent
2. **同维度串行**：同一维度的多个子 Agent 串行执行（共识需要顺序）
3. **隔离规则**：每次 Task 调用不传 task_id，确保独立会话
4. **prompt 自包含**：每个子 Agent 的 prompt 包含完整的维度定义、检查步骤、输出格式

### 子 Agent 修复权限

- **可修改**：docs/ 下的文档文件（通过 md-sections 精准操作）
- **禁止修改**：.java / pom.xml / AGENTS.md（安全规则：源代码和构建配置是只读真相源）
- **AGENTS.md 问题**：子 Agent 报告给主 Agent，由主 Agent 统一处理

---

## Phase 4: 全局扫描（仅 L3）

**目标**：对所有 Contract 轨文档进行全局仔细扫描，不仅限变更影响的文档。

### 执行步骤

1. 列出所有 docs/modules/*.md、docs/architecture/*.md、docs/conventions/*.md
2. 对每个文档执行 D1-D10 全量检查（D10 含语义比对）
3. Warning 也计为问题，需要修复或标记
4. 输出全局扫描报告

---

## 最终报告格式

```markdown
## 文档同步报告

**级别**: L{level} | **项目**: {docSystem} | **基准提交**: {baseCommit}

### 变更概况
- 变更文件: {total} 个（controller: {n}, service: {n}, ...）
- 影响文档: {docCount} 个

### 验证矩阵
| 维度 | 状态 | Error | Warning | 修复 |
|------|------|-------|---------|------|
| D1 引用完整性 | ✅/❌ | {n} | {n} | {n} |
| ... | ... | ... | ... | ... |

### 修复记录
#### 🤖 自动修复 ({count})
- [文件] 修复描述

#### 🤖👤 待确认 ({count})
- [文件] `[待确认]` 提议描述

#### 👤 需人工处理 ({count})
- [文件] 原因描述

### 共识验证统计
- 总验证轮次: {rounds} | 一次通过维度: {firstPass}/{total}

### 建议后续操作
1. 审查 `[待确认]` 标记的修改
2. 处理 👤 创造性维护项
```

---

## 验证检查清单

同步完成后，逐项确认：

1. **变更覆盖**：docImpact 中所有 docTarget 均已处理（修复或标记）
2. **修复确认**：每个 Edit 操作目标章节存在且内容已更新
3. **共识通过**：所有验证维度 consecutive_passes ≥ 2（L2/L3）
4. **无遗留 `[待确认]`**：报告中列出所有半确定性修改，确保不遗漏
5. **报告完整**：最终报告包含变更概况 + 验证矩阵 + 修复记录 + 建议操作
6. **references 完整**：所有 `references/*.md` 引用的文件均存在

任何检查失败 → 诊断原因 → 修复 → 重新验证对应项。

---

## 资源文件索引

| 文件 | 用途 | 何时加载 |
|------|------|---------|
| `references/environment-probing.md` | 环境感知探测规则 | Phase 0 |
| `references/sync-procedures.md` | 同步操作规程 + 代码→文档映射 | Phase 2 |
| `references/verification-dimensions.md` | D1-D10 定义 + 子Agent prompt | Phase 3 |
| `scripts/detect-changes.py` | Git diff 预处理 | Phase 1 |
| `scripts/md-sections.sh` | Markdown 章节解析（兜底） | 全流程 |
