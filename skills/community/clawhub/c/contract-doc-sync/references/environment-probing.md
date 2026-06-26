# 环境探测 (Environment Probing)

> Contract Doc Sync 的启动阶段——在执行任何同步操作之前，先理解项目文档系统。

---

## 1. 概述

环境探测是 Contract Doc Sync 的**第一个执行阶段**。它通过扫描项目中的关键文件，自动构建 `ProjectDocProfile`，回答以下核心问题：

1. **项目使用什么文档系统？**（三轨 Contract/Constraint/Intent？通用 docs/？无文档？）
2. **文档遵循什么模板？**（固定章节、半固定章节、自由章节）
3. **代码如何映射到文档？**（Controller → API 参考？Service → 技术设计？）
4. **可用的解析工具有哪些？**（`scripts/md-sections.sh`？skill 内置 fallback？）

探测结果直接影响后续所有同步操作的行为：选错文档系统会导致错误的章节定位、无效的模板验证、甚至破坏项目文档结构。

---

## 2. 探测流程

探测按以下 5 步顺序执行，每步的输出作为下一步的输入：

```
┌─────────────────────────────────────────────────────────────┐
│  Step 1: 检查 AGENTS.md / CLAUDE.md                         │
│  → 提取文档引用规则、分层披露原则                            │
├─────────────────────────────────────────────────────────────┤
│  Step 2: 扫描索引文档（README / SUMMARY / _sidebar / toc…） │
│  → 识别文档系统类型、轨定义、模板结构                        │
├─────────────────────────────────────────────────────────────┤
│  Step 3: 检测可用工具                                       │
│  → md-sections（项目版本 > skill 内置版本 > 退化）          │
├─────────────────────────────────────────────────────────────┤
│  Step 4: 识别技术栈                                         │
│  → pom.xml / package.json / build.gradle → 确定代码结构模式  │
├─────────────────────────────────────────────────────────────┤
│  Step 5: 构建 ProjectDocProfile                             │
│  → 聚合所有探测结果，项目规则覆盖默认基线                    │
└─────────────────────────────────────────────────────────────┘
```

### Step 1: 检查 AGENTS.md / CLAUDE.md

- **目标**：提取文档引用规则、加载策略、维护职责
- **优先级**：AGENTS.md > CLAUDE.md > GEMINI.md
- **关键信息**：
  - 文档引用规则（如：禁止全文加载、必须先看结构）
  - `scripts/md-sections.sh` 的使用约定
  - 文档索引（哪些文档是 MUST/SHOULD/MAY）
  - 文档与代码的对齐机制

### Step 2: 扫描索引文档

- **目标**：识别文档系统类型，建立轨定义
- **方法**：扫描所有类型的索引文件（不仅限于 README.md），按路径+类型联合分类
- **探测模式**：
  ```bash
  # 扫描所有索引文档（不限于 README.md）
  find . \( -name "README.md" -o -name "SUMMARY.md" -o -name "_sidebar.md" \
    -o -name "_toc.md" -o -name "toc.md" -o -name "mkdocs.yml" -o -name "_toc.yml" \
    -o -name "CHANGELOG.md" \) \
    -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/target/*" | sort
  
  # 前端文档框架配置
  find . -path "*/.vitepress/config.*" -o -name "docusaurus.config.*" 2>/dev/null
  ```
- **分类规则**：见 [索引文档探测映射表](#3-索引文档探测映射表-index-document-detection-table)
- **信号优先级**：专用目录文件（SUMMARY.md / _sidebar.md）> 框架配置（mkdocs.yml）> 通用 README.md

### Step 3: 检测可用工具

- **目标**：确定章节解析能力
- **优先级**：项目 `scripts/md-sections.sh` > skill 内置 `scripts/md-sections.sh` > 退化到 grep

### Step 4: 识别技术栈

- **目标**：理解代码结构模式，为 codeDocMapping 提供依据
- **检测文件**：`pom.xml`（Maven）、`package.json`（Node）、`build.gradle`（Gradle）
- **推断内容**：模块结构、分层架构、包命名约定

### Step 5: 构建 ProjectDocProfile

- **目标**：聚合所有探测结果，输出标准化配置
- **规则**：项目规则始终覆盖 skill 默认基线
- **格式**：见 [ProjectDocProfile 格式](#5-projectdocprofile-格式-output-format)

---

## 3. 索引文档探测映射表 (Index Document Detection Table)

> **核心原则**：索引文档不止 `README.md`，而是**所有可能承载文档体系元信息的文件**。
> README.md 只是其中最常见的一种。探测时必须扫描所有类型的索引文件。

### 3.1 索引文件类型与探测模式

| 类型 | 文件名模式 | 探测 glob | 信号强度 |
|------|-----------|-----------|---------|
| **README** | `README.md`, `README.*` | `**/README.md` | 中（通用描述，需路径+内容联合判断） |
| **文档目录** | `SUMMARY.md`, `toc.md`, `_toc.md` | `**/SUMMARY.md`, `**/toc.md`, `**/_toc.md` | 高（专门用于目录索引） |
| **配置化目录** | `mkdocs.yml`, `_toc.yml` | `mkdocs.yml`, `_toc.yml` | 高（结构化导航定义） |
| **前端文档框架** | `config.*`（在 .vitepress/ / docusaurus/ 下） | `.vitepress/config.*`, `docusaurus.config.*` | 高（含 sidebar/nav 定义） |
| **docsify 侧边栏** | `_sidebar.md` | `**/_sidebar.md` | 高（直接定义文档导航） |
| **AI 规则入口** | `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` | 根目录下直接检测 | 高（含文档索引和引用规则） |
| **编辑器规则** | `.cursorrules`, `.windsurfrules` | 根目录下直接检测 | 低（偶尔含文档约定） |
| **变更追踪** | `CHANGELOG.md`, `CHANGES.md` | `CHANGELOG.md`, `CHANGES.md` | 低（辅助时间线信息） |
| **Intent 冻结** | `openspec/specs/*/spec.md` | `openspec/specs/*/spec.md` | 高（冻结的设计意图） |
| **构建元数据** | `pom.xml`, `package.json`, `build.gradle*` | 根目录下直接检测 | 中（隐含模块结构） |

### 3.2 路径+类型联合分类（按角色）

对每个探测到的索引文件，按**路径位置 + 文件类型**联合判断其角色：

| 路径模式 | 文件类型 | 角色 | 关键信息 |
|----------|---------|------|----------|
| `docs/README.md` | README | **文档系统描述** | 轨定义、维护规则、对齐机制、反模式警示 |
| `docs/modules/README.md` | README | **模块文档模板** | 固定/半固定章节结构、命名规范 |
| `docs/architecture/README.md` | README | **架构文档模板** | 章节结构、C4 图约定 |
| `docs/conventions/README.md` | README | **规范文档模板** | 章节结构、强制/推荐分级 |
| `SUMMARY.md` | GitBook 目录 | **文档导航** | 章节层级、文件路径映射 |
| `_sidebar.md` | docsify 侧边栏 | **文档导航** | 侧边栏结构、链接映射 |
| `mkdocs.yml` | MkDocs 配置 | **文档导航+结构** | nav 定义、页面层级 |
| `_toc.yml` | Jupyter Book 目录 | **文档导航** | 章节树、文件路径映射 |
| `.vitepress/config.*` | VitePress 配置 | **文档导航+结构** | sidebar 定义、导航树 |
| `docusaurus.config.*` | Docusaurus 配置 | **文档导航+结构** | 侧边栏、插件配置 |
| `toc.md` | 通用目录 | **文档导航** | 章节列表、链接 |
| `AGENTS.md` | AI 规则 | **编码规则入口** | 文档索引表、引用规则、维护职责 |
| `CLAUDE.md` | AI 规则 | **编码规则入口** | Claude 专用文档约定 |
| `GEMINI.md` | AI 规则 | **编码规则入口** | Gemini 专用文档约定 |
| `openspec/specs/*/spec.md` | Intent 冻结 | **设计意图** | 冻结的能力描述、需求定义 |
| `README.md`（根目录） | README | **项目概览** | 技术栈、项目结构、快速开始 |
| `CHANGELOG.md` | 变更日志 | **变更追踪** | 版本历史、变更时间线 |
| `pom.xml` | 构建配置 | **模块结构** | Maven 模块列表、版本号 |
| `package.json` | 构建配置 | **模块结构** | 项目结构、scripts |

### 3.3 分类逻辑

```python
def classify_index_doc(path: str) -> dict:
    """根据路径+文件类型对索引文档进行联合分类"""
    
    # 1. 按文件名确定类型
    filename = path.split("/")[-1]
    type_map = {
        "README.md": "readme",
        "SUMMARY.md": "gitbook-toc",
        "_sidebar.md": "docsify-sidebar",
        "_toc.md": "jupyterbook-toc",
        "toc.md": "generic-toc",
        "mkdocs.yml": "mkdocs-config",
        "_toc.yml": "jupyterbook-config",
        "AGENTS.md": "ai-rules",
        "CLAUDE.md": "ai-rules",
        "GEMINI.md": "ai-rules",
        "CHANGELOG.md": "changelog",
        "pom.xml": "build-config",
        "package.json": "build-config",
    }
    doc_type = type_map.get(filename, "unknown")
    
    # 2. 按路径+类型联合判断角色
    role_map = {
        # docs/ 下的 README → 文档体系描述/模板
        ("readme", "docs/README.md"): {"role": "system-description", "docSystem": "auto-detect"},
        ("readme", "docs/modules/README.md"): {"role": "template-definition", "track": "Contract"},
        ("readme", "docs/architecture/README.md"): {"role": "template-definition", "track": "Constraint"},
        ("readme", "docs/conventions/README.md"): {"role": "template-definition", "track": "Constraint"},
        ("readme", "README.md"): {"role": "project-overview"},
        # 文档导航类
        ("gitbook-toc", "SUMMARY.md"): {"role": "doc-navigation", "format": "gitbook"},
        ("docsify-sidebar", "**/_sidebar.md"): {"role": "doc-navigation", "format": "docsify"},
        ("mkdocs-config", "mkdocs.yml"): {"role": "doc-navigation", "format": "mkdocs"},
        ("jupyterbook-config", "_toc.yml"): {"role": "doc-navigation", "format": "jupyterbook"},
        ("generic-toc", "**/toc.md"): {"role": "doc-navigation", "format": "generic"},
        # AI 规则类
        ("ai-rules", "AGENTS.md"): {"role": "ai-rules-entry"},
        ("ai-rules", "CLAUDE.md"): {"role": "ai-rules-entry"},
        ("ai-rules", "GEMINI.md"): {"role": "ai-rules-entry"},
    }
    
    # 3. 精确匹配 → 路径前缀匹配 → 类型兜底
    key = (doc_type, path)
    if key in role_map:
        return role_map[key]
    # 尝试路径前缀匹配
    for (t, p), v in role_map.items():
        if t == doc_type and path.endswith(p.replace("**/", "")):
            return v
    # 类型兜底
    fallback = {
        "readme": {"role": "section-readme", "extracts": ["section_overview"]},
        "gitbook-toc": {"role": "doc-navigation"},
        "docsify-sidebar": {"role": "doc-navigation"},
        "mkdocs-config": {"role": "doc-navigation"},
        "ai-rules": {"role": "ai-rules-entry"},
        "changelog": {"role": "change-tracking"},
        "build-config": {"role": "module-structure"},
    }
    return fallback.get(doc_type, {"role": "unknown"})
```

---

## 4. 关键文件探测清单 (Key File Checklist)

### 4.1 AI 规则入口

| 文件 | 用途 | 是否必须 | 探测失败处理 |
|------|------|----------|-------------|
| `AGENTS.md` | AI 编码规则、文档引用约定 | 否 | 尝试 CLAUDE.md |
| `CLAUDE.md` | Claude 专用规则 | 否 | 尝试 GEMINI.md |
| `GEMINI.md` | Gemini 专用规则 | 否 | 跳过 |
| `.cursorrules` / `.windsurfrules` | 其他 AI 规则文件 | 否 | 跳过 |

### 4.2 文档体系索引

| 文件 | 用途 | 是否必须 | 探测失败处理 |
|------|------|----------|-------------|
| `docs/README.md` | 文档系统架构定义 | 三轨模式必须 | 降级为通用模式 |
| `docs/modules/README.md` | 模块文档模板 | 否 | 使用 skill 默认模板 |
| `docs/architecture/README.md` | 架构文档模板 | 否 | 使用 skill 默认模板 |
| `docs/conventions/README.md` | 规范文档模板 | 否 | 使用 skill 默认模板 |

### 4.3 文档导航/目录文件

| 文件 | 文档框架 | 用途 | 探测失败处理 |
|------|---------|------|-------------|
| `SUMMARY.md` | GitBook | 文档目录结构 | 尝试其他导航文件 |
| `_sidebar.md` | docsify | 侧边栏导航 | 尝试其他导航文件 |
| `mkdocs.yml` | MkDocs | 导航+站点结构 | 尝试其他导航文件 |
| `_toc.yml` / `_toc.md` | Jupyter Book | 目录结构 | 尝试其他导航文件 |
| `.vitepress/config.*` | VitePress | 侧边栏+导航 | 尝试其他导航文件 |
| `docusaurus.config.*` | Docusaurus | 侧边栏+配置 | 尝试其他导航文件 |
| `toc.md` | 通用 | 目录列表 | 跳过 |

### 4.4 工具与构建

| 文件 | 用途 | 是否必须 | 探测失败处理 |
|------|------|----------|-------------|
| `scripts/md-sections.sh` | 章节解析工具 | 否 | 使用 skill 内置版本 |
| `pom.xml` | Maven 模块结构、版本 | 否 | 尝试其他构建文件 |
| `package.json` | JS/TS 项目结构 | 否 | 尝试其他构建文件 |
| `build.gradle` / `build.gradle.kts` | Gradle 项目结构 | 否 | 跳过 |
| `CHANGELOG.md` | 变更历史追踪 | 否 | 跳过 |

---

## 5. ProjectDocProfile 格式 (Output Format)

探测完成后输出的标准化配置对象：

```json
{
  "$schema": "ProjectDocProfile",
  "docSystem": "three-track | generic | unknown",
  "tracks": [
    {
      "name": "Contract",
      "path": "docs/modules/",
      "sourceOfTruth": "code",
      "alignmentDirection": "code→doc",
      "description": "与代码直接对应的模块文档，代码为唯一事实来源"
    },
    {
      "name": "Constraint",
      "path": "docs/architecture/, docs/conventions/",
      "sourceOfTruth": "doc",
      "alignmentDirection": "doc→code",
      "description": "架构约束和编码规范，文档为事实来源"
    },
    {
      "name": "Intent",
      "path": "openspec/specs/",
      "sourceOfTruth": "doc",
      "alignmentDirection": "frozen",
      "description": "冻结的设计意图，不可变更"
    }
  ],
  "templates": {
    "module": {
      "fixedSections": ["API 参考", "技术设计", "变更历史"],
      "semiFixedSections": ["概述", "相关文档"],
      "freeSections": true
    },
    "architecture": {
      "fixedSections": ["概述", "设计决策"],
      "semiFixedSections": [],
      "freeSections": true
    },
    "convention": {
      "fixedSections": ["规则", "示例"],
      "semiFixedSections": ["背景", "例外"],
      "freeSections": false
    }
  },
  "codeDocMapping": {
    "controller": "API 参考",
    "service": "技术设计",
    "entity": "技术设计 > 类图",
    "mapper": "技术设计 > 数据访问",
    "config": "配置参考",
    "facade": "API 参考",
    "dto": "API 参考 > 请求/响应",
    "exception": "错误处理",
    "test": "测试覆盖"
  },
  "sectionParser": {
    "path": "scripts/md-sections.sh",
    "available": true,
    "source": "project | skill-builtin | none",
    "capabilities": ["list-sections", "extract-section", "line-lookup"]
  },
  "projectOverrides": [
    {
      "field": "codeDocMapping.controller",
      "defaultValue": "API 参考",
      "projectValue": "API 规范",
      "source": "AGENTS.md"
    }
  ],
  "agentsMd": {
    "found": true,
    "path": "AGENTS.md",
    "docReferenceRules": "分层披露原则：必须先 md-sections 看结构，禁止全文加载",
    "docIndex": ["docs/architecture/system-overview.md:⛔ MUST", "..."],
    "maintenanceResponsibilities": ["🤖 确定性", "🤖👤 半确定性", "👤 创造性"]
  },
  "techStack": {
    "type": "maven",
    "modules": ["common", "clients", "app"],
    "basePackage": "org.smm.archetype"
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `docSystem` | enum | `three-track`（三轨系统）/ `generic`（通用 docs/）/ `unknown`（无法识别） |
| `tracks` | array | 文档轨定义，每轨含名称、路径、事实来源、对齐方向 |
| `templates` | object | 各类型文档的模板定义（固定/半固定/自由章节） |
| `codeDocMapping` | object | 代码元素到文档章节的映射关系 |
| `sectionParser` | object | 章节解析工具信息 |
| `projectOverrides` | array | 项目自定义规则覆盖 skill 默认值的记录 |
| `agentsMd` | object | AGENTS.md/CLAUDE.md 的提取信息摘要 |
| `techStack` | object | 技术栈识别结果 |

---

## 6. 项目规则覆盖策略 (Override Strategy)

### 核心原则

> **项目规则始终优先于 skill 默认基线。**

### 覆盖优先级

```
AGENTS.md/CLAUDE.md 显式规则  >  docs/README.md 轨定义  >  模板文件隐含结构  >  skill 默认基线
```

### 覆盖场景与处理

| 场景 | 处理方式 | 示例 |
|------|----------|------|
| 项目有自定义模板 | 使用项目模板，不使用 skill 默认模板 | `docs/modules/README.md` 定义了不同章节结构 |
| 项目有自定义 codeDocMapping | 扩展或替换默认映射 | AGENTS.md 指定 Controller → "API 规范" 而非 "API 参考" |
| 项目有自定义文档引用规则 | 严格遵循项目规则 | AGENTS.md 要求必须先 `md-sections` 看结构 |
| 项目定义了新的轨 | 添加到 tracks 数组 | 项目有 `docs/guides/` 作为 Guide 轨 |
| 项目禁止某些操作 | 记录为约束 | AGENTS.md 禁止全文加载文档 |

### 覆盖记录

所有覆盖项记录在 `projectOverrides` 数组中：

```json
{
  "field": "被覆盖的字段路径",
  "defaultValue": "skill 默认值",
  "projectValue": "项目自定义值",
  "source": "来源文件",
  "reason": "覆盖原因（可选）"
}
```

### 冲突检测

当项目规则与 skill 基线冲突时：
1. **记录冲突**：写入 `projectOverrides`
2. **项目优先**：使用项目规则
3. **通知用户**：在同步报告中标注 "项目自定义规则生效"

---

## 7. 退化策略 (Degradation Strategy)

当项目文档系统无法识别时，按以下策略逐步退化：

### 退化级别

| 级别 | 触发条件 | 行为 |
|------|----------|------|
| **L0: 完整识别** | `docs/README.md` 存在且含轨定义 | 完整三轨模式，所有能力可用 |
| **L1: 部分识别** | `docs/` 存在但无轨定义 | 通用 docs/ 模式，基于目录结构推断 |
| **L2: 最小识别** | 仅有 `README.md` 或 `AGENTS.md` | 仅文档引用规则生效，无模板验证 |
| **L3: 退化模式** | 无任何文档系统信号 | 退化到通用基线 |

### L3 退化模式行为

当达到 L3 时：

1. **文档系统**：`docSystem = "unknown"`
2. **轨定义**：空数组（无轨概念）
3. **模板验证**：跳过（不验证固定章节是否存在）
4. **章节解析**：
   - 有 `scripts/md-sections.sh` → 正常使用
   - 无 `scripts/md-sections.sh` → 使用 skill 内置版本
   - 内置版本也不可用 → 基于正则的 grep 退化
5. **codeDocMapping**：使用 skill 默认映射
6. **同步操作**：仅执行基础的"代码变更 → 文档存在性检查"

### 退化模式报告

在退化模式下，同步报告必须包含：

```
⚠️ 环境探测结果：退化模式 (L3)
原因：未检测到文档系统定义文件
影响：模板验证已禁用，使用 skill 默认 codeDocMapping
建议：在 docs/README.md 中定义文档系统以启用完整功能
```

---

## 8. 探测步骤详细指令 (Detailed Probing Steps for Skill Execution)

以下为编排 Agent 执行探测时应运行的具体命令。按顺序执行，每步的结果用于下一步判断。

### Step 1: 查找 AGENTS.md / CLAUDE.md

```bash
# 查找 AI 规则文件（按优先级）
for f in AGENTS.md CLAUDE.md GEMINI.md; do
  if [ -f "$f" ]; then
    echo "FOUND:$f"
  fi
done
```

**结果处理**：
- 找到 AGENTS.md → 使用 `md-sections` 提取"文档索引"和"文档引用规则"章节
- 仅找到 CLAUDE.md → 提取文档相关规则
- 均未找到 → 跳过此步

### Step 2: 扫描索引文档

```bash
# 扫描所有索引文档（不限于 README.md）
echo "=== 扫描索引文档 ==="

# 2a. README 类
echo "--- README 文件 ---"
find . -name "README.md" \
  -not -path "*/node_modules/*" -not -path "*/.git/*" \
  -not -path "*/target/*" -not -path "*/dist/*" | sort

# 2b. 文档目录/导航类
echo "--- 目录与导航文件 ---"
find . \( -name "SUMMARY.md" -o -name "_sidebar.md" \
  -o -name "_toc.md" -o -name "toc.md" -o -name "mkdocs.yml" -o -name "_toc.yml" \) \
  -not -path "*/node_modules/*" -not -path "*/.git/*" | sort

# 2c. 前端文档框架
echo "--- 文档框架配置 ---"
find . -path "*/.vitepress/config.*" -o -name "docusaurus.config.*" 2>/dev/null | sort

# 2d. 变更追踪
echo "--- 变更追踪 ---"
for f in CHANGELOG.md CHANGES.md; do
  [ -f "$f" ] && echo "  → $f"
done
```

**结果处理**：
- 对每个探测到的索引文件，根据 [索引文档探测映射表](#3-索引文档探测映射表-index-document-detection-table) 按路径+类型联合分类
- 对 `docs/README.md` 使用 `md-sections` 提取轨定义
- 对模板类 README.md 提取章节结构
- 对导航文件（SUMMARY.md / _sidebar.md / mkdocs.yml）提取文档结构树
- 对 AI 规则文件提取文档引用约定和索引

### Step 3: 检测 md-sections 工具

```bash
# 检查项目版本
if [ -x "scripts/md-sections.sh" ]; then
  echo "PROJECT_VERSION:scripts/md-sections.sh"
  scripts/md-sections.sh --help 2>&1 | head -5
else
  echo "NO_PROJECT_VERSION"
fi

# 检查 skill 内置版本
SKILL_MD_SECTIONS="$HOME/.config/opencode/skills/contract-doc-sync/scripts/md-sections.sh"
if [ -x "$SKILL_MD_SECTIONS" ]; then
  echo "SKILL_BUILTIN:$SKILL_MD_SECTIONS"
else
  echo "NO_SKILL_BUILTIN"
fi
```

**选择逻辑**：
1. 项目版本存在且可执行 → 使用项目版本
2. 项目版本不存在，skill 内置版本存在 → 使用 skill 内置版本
3. 均不存在 → 退化到 grep

### Step 4: 检测技术栈

```bash
# 检测构建系统
if [ -f "pom.xml" ]; then
  echo "BUILD:maven"
  # 提取模块列表
  grep -oP '<module>\K[^<]+' pom.xml 2>/dev/null || echo "NO_MODULES"
elif [ -f "package.json" ]; then
  echo "BUILD:npm"
  cat package.json | head -20
elif [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]; then
  echo "BUILD:gradle"
else
  echo "BUILD:unknown"
fi
```

### Step 5: 构建并输出 ProjectDocProfile

将前 4 步结果聚合为 JSON 格式的 `ProjectDocProfile`。构建逻辑：

```python
def build_profile(step1_result, step2_result, step3_result, step4_result):
    profile = {
        "docSystem": determine_doc_system(step2_result),
        "tracks": extract_tracks(step1_result, step2_result),
        "templates": extract_templates(step2_result),
        "codeDocMapping": DEFAULT_CODE_DOC_MAPPING,  # 可被 step1 覆盖
        "sectionParser": determine_parser(step3_result),
        "projectOverrides": [],
        "agentsMd": extract_agents_info(step1_result),
        "techStack": extract_tech_stack(step4_result)
    }

    # 应用项目规则覆盖
    apply_overrides(profile, step1_result, step2_result)

    return profile
```

### 完整探测脚本（一键执行）

```bash
#!/bin/bash
# environment-probe.sh — Contract Doc Sync 环境探测
set -euo pipefail

echo "=== Contract Doc Sync 环境探测 ==="
echo ""

# Step 1
echo "--- Step 1: AI 规则文件 ---"
RULES_FILE=""
for f in AGENTS.md CLAUDE.md GEMINI.md; do
  if [ -f "$f" ]; then
    echo "  ✓ $f"
    RULES_FILE="$f"
    break
  fi
done
[ -z "$RULES_FILE" ] && echo "  ✗ 未找到 AI 规则文件"

# Step 2
echo "--- Step 2: 索引文档扫描 ---"
INDEX_COUNT=0
# 扫描所有类型的索引文件（不限于 README.md）
while IFS= read -r idxfile; do
  echo "  → $idxfile"
  INDEX_COUNT=$((INDEX_COUNT + 1))
done < <(find . \( -name "README.md" -o -name "SUMMARY.md" -o -name "_sidebar.md" \
  -o -name "_toc.md" -o -name "toc.md" -o -name "mkdocs.yml" -o -name "_toc.yml" \
  -o -name "CHANGELOG.md" \) \
  -not -path "*/node_modules/*" \
  -not -path "*/.git/*" \
  -not -path "*/target/*" \
  -not -path "*/dist/*" \
  2>/dev/null | sort)
# 文档框架配置
while IFS= read -r fwconfig; do
  echo "  → $fwconfig"
  INDEX_COUNT=$((INDEX_COUNT + 1))
done < <(find . -path "*/.vitepress/config.*" -o -name "docusaurus.config.*" 2>/dev/null | sort)
echo "  共 $INDEX_COUNT 个索引文件"
[ -f "docs/README.md" ] && echo "  ✓ docs/README.md 存在（文档系统信号）"
[ -f "SUMMARY.md" ] && echo "  ✓ SUMMARY.md 存在（GitBook 信号）"
[ -f "_sidebar.md" ] && echo "  ✓ _sidebar.md 存在（docsify 信号）"
[ -f "mkdocs.yml" ] && echo "  ✓ mkdocs.yml 存在（MkDocs 信号）"

# Step 3
echo "--- Step 3: 章节解析工具 ---"
if [ -x "scripts/md-sections.sh" ]; then
  echo "  ✓ 项目版本: scripts/md-sections.sh"
elif [ -x "$HOME/.config/opencode/skills/contract-doc-sync/scripts/md-sections.sh" ]; then
  echo "  ⚡ Skill 内置版本（项目版本不可用）"
else
  echo "  ✗ 无可用版本（将退化到 grep）"
fi

# Step 4
echo "--- Step 4: 技术栈 ---"
if [ -f "pom.xml" ]; then
  echo "  ✓ Maven 项目"
elif [ -f "package.json" ]; then
  echo "  ✓ Node.js 项目"
elif [ -f "build.gradle" ] || [ -f "build.gradle.kts" ]; then
  echo "  ✓ Gradle 项目"
else
  echo "  ✗ 未识别构建系统"
fi

echo ""
echo "=== 探测完成 ==="
```

---

## 附录：默认基线 (Skill Baseline)

当项目未提供自定义规则时，skill 使用以下默认值：

### 默认 codeDocMapping

```json
{
  "controller": "API 参考",
  "service": "技术设计",
  "entity": "技术设计 > 类图",
  "mapper": "技术设计 > 数据访问",
  "config": "配置参考",
  "facade": "API 参考",
  "dto": "API 参考 > 请求/响应",
  "exception": "错误处理",
  "test": "测试覆盖"
}
```

### 默认模板章节

```json
{
  "module": {
    "fixedSections": ["概述", "API 参考", "技术设计", "变更历史"],
    "semiFixedSections": ["相关文档", "配置参考"]
  }
}
```

### 默认轨定义

```json
{
  "name": "Contract",
  "path": "docs/modules/",
  "sourceOfTruth": "code",
  "alignmentDirection": "code→doc"
}
```
