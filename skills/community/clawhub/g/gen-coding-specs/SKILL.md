---
name: gen-coding-specs
description: 基于模板为当前工作空间生成完整技术编码规范，写入 docs/coding-specs/，供 gen-code 与其它技能消费。
aliases:
  - /gen-coding-specs
  - /skills gen-coding-specs
  - /skills/gen-coding-specs
  - 生成编码规范
  - 技术规范
triggerPatterns:
  - "^/gen-coding-specs$"
  - "^/skills\\s*(/|\\s*)gen-coding-specs$"
  - "(生成|创建)\\s*编码规范"
  - "技术规范"
---

# gen-coding-specs - 生成技术编码规范

**技能 ID**: `gen-coding-specs`  
**版本**: 1.3.0  

## 目标

为当前工作空间生成完整的编码规范文档（`docs/coding-specs/coding.*.md`），使 AI 与开发者对技术栈、接口、风格、测试等达成一致；**与 `gen-code` 读取路径一致**（见 `skills/SKILLS-FILE-OUTPUT.md` 第五节）。

## 模板来源（技能自备）

模板与本技能**同目录维护**，路径：

- **本仓库**：`skills/gen-coding-specs/templates/`（与 `SKILL.md` 同级下的 `templates/`）
- **仅拷贝本技能到目标项目时**：请保留 **`gen-coding-specs/templates/`** 整目录，与 `SKILL.md` 一并拷贝；生成时从此目录读取，写入项目内 `docs/coding-specs/`。

执行生成时，以 **`templates/`** 为相对路径（相对于本技能目录）解析各 `coding.*.md` 源文件。

## 执行步骤

完整执行流程、12 分册定制规则、交叉一致性校验见 **[prompt.md](./prompt.md)**。

### 1. 分析工作空间

- **技术栈**：语言、框架、数据库、构建工具等  
- **项目结构**：目录与模块划分  
- **业务领域**：简要背景  
- **现有规范**：是否已有 `docs/coding-specs/` 内容  

### 2. 创建规范目录

若不存在则创建（须先建目录再写文件）：

```bash
mkdir -p docs/coding-specs
```

### 3. 生成规范文档

按模板生成并落盘到 **`docs/coding-specs/`**，文件名固定：

| 输出文件 | 模板 |
|----------|------|
| `coding.index.md` | `templates/coding.index.md` |
| `coding.api.md` | `templates/coding.api.md` |
| `coding.architecture.md` | `templates/coding.architecture.md` |
| `coding.data-models.md` | `templates/coding.data-models.md` |
| `coding.vue.md` | `templates/coding.vue.md` |
| `coding.coding-style.md` | `templates/coding.coding-style.md` |
| `coding.testing.md` | `templates/coding.testing.md` |
| `coding.security.md` | `templates/coding.security.md` |
| `coding.performance.md` | `templates/coding.performance.md` |
| `coding.documentation.md` | `templates/coding.documentation.md` |
| `coding.code-review.md` | `templates/coding.code-review.md` |
| `coding.version-control.md` | `templates/coding.version-control.md` |

### 4. 定制

按项目填充技术栈、示例与团队约定；保持各分册之间无冲突。

### 5. 验证

- [ ] 索引 `coding.index.md` 可导航到各分册  
- [ ] 内容反映真实技术栈与约束  
- [ ] 格式正确、含必要示例  

## 输出与衔接

- **落盘**：遵守 [SKILLS-FILE-OUTPUT.md](../SKILLS-FILE-OUTPUT.md)。
- **后续**：**gen-code** 等技能执行时须**直接读取** `docs/coding-specs/` 下对应 `coding.*.md`（见 `coding.index.md` 索引），无需单独「加载上下文」技能。
- **规范随项目变更**：可再次执行本技能覆盖生成，或直接编辑 `docs/coding-specs/` 下 Markdown。

## 相关技能

### 前置技能

- **gen-design**: 系统设计，提供技术栈和边界定义

### 后续技能

- **gen-code**: 主要消费者，读取技术规范作为编码风格标准
  - **注意**：若项目采用契约驱动开发，`gen-code` 优先读取 `contract-gen` 输出的 YAML 契约
  - 本技能生成的 Markdown 规范作为**风格标准**（命名规范、代码格式等）
- **contract-gen**: 契约生成，生成机器可读的 YAML 契约
  - 本技能生成规范后，可执行 `contract-gen` 生成精确的结构定义
  - 契约应遵循本技能的规范（如 `coding.api.md` 的接口风格、`coding.data-models.md` 的命名规范）
- **review-code**: 审查时对照本规范分册

### 技能分工

| 技能 | 输出 | 用途 | gen-code 读取优先级 |
|------|------|------|-------------------|
| **gen-coding-specs** | `docs/coding-specs/*.md` | 风格规范（命名、格式、代码风格） | 🟡 中（风格） |
| **contract-gen** | `docs/contracts/*.yaml` | 精确结构定义（表名、字段、API 路径） | 🔴 高（优先） |

**建议流程**：
- **标准流程**：`gen-design` → `gen-coding-specs` → `gen-code`
- **契约驱动**：`gen-design` → `gen-coding-specs` → `contract-gen` → `gen-code`

全链路见 [SKILL-VALUE-CHAIN.md](../SKILL-VALUE-CHAIN.md)。

---

*本技能替代原「command + instructions」安装方式；不再向 `.cursor/commands` 等目录安装命令文件。*
