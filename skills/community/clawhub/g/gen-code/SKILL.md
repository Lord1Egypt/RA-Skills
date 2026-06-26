---
name: gen-code
description: 按任务和规范生成高质量代码。支持新项目生成和遗留项目上下文感知生成。默认使用 Vue3 + Ant Design + Spring Boot 3 + MyBatis-Plus，AI 能力使用 LangChain4j + LangGraph4j。
aliases:
  - /gen-code
  - /skills gen-code
  - /skills/gen-code
  - 生成代码
  - 写代码
  - 实现功能
triggerPatterns:
  - "^/gen-code$"
  - "^/skills\\s*(/|\\s*)gen-code$"
  - "(生成 | 写 | 创建)\\s*代码"
  - "实现.*功能"
supportedPlatforms:
  - Cursor (slash-command)
  - GitHub Copilot (slash-command, intent-based)
  - Claude (slash-command, intent-based)
  - 通义灵码 (intent-based)
  - Codeium (slash-command)
---

# /gen-code - 代码生成技能

**技能 ID**: `gen-code`
**技能名称**: 代码生成技能
**版本**: 2.6.0
**描述**: 按任务和规范生成高质量代码；支持单任务或任务范围分批生成；支持设计文档驱动自动执行（自动调用gen-tasks）；支持新项目生成和遗留项目上下文感知生成；生成前强制执行代码复用检测；生成时强制执行质量门禁检查和任务完成度检查；生成后自动更新任务状态；默认从 `docs/coding-specs/` 读取技术规范（与生成规范技能写入路径一致）

---

## 触发条件（多格式兼容）

### 格式 1：斜杠命令（推荐用于 Cursor、GitHub Copilot、Codeium）

```
/gen-code                                    # 交互式选择任务
/gen-code Task-001                           # 单任务
/gen-code Task-001..010                      # 任务范围，按批生成
/gen-code --from-design docs/design/xxx.md   # 直接按设计文档执行
/gen-code --auto                             # 自动执行所有任务
/gen-code --continue                         # 继续执行下一个任务
```

### 格式 2：Skills 前缀（用于支持 /skills 前缀的 AI 助手）

```
/skills gen-code
/skills/gen-code
/skills gen-code Task-001
```

### 格式 3：意图识别（推荐用于 Claude、通义灵码）

```
生成代码
写代码
帮我实现这个功能
为任务 Task-001 生成代码
按设计文档生成代码
自动执行所有任务
```

### 所有触发方式

- `/gen-code`
- `/gen-code Task-001`（单任务）
- `/gen-code Task-001..010`（任务范围，按批生成）
- `/gen-code --from-design <设计文档路径>`（直接按设计文档执行）
- `/gen-code --auto`（自动执行所有任务）
- `/gen-code --continue`（继续执行下一个任务）
- `/skills gen-code`
- `/skills/gen-code`
- `/code`
- `生成代码`
- `写代码`
- `实现功能`
- `按设计文档生成代码`

## 技能边界（防止误触发）

- **本技能适用于**：新项目生成、遗留项目上下文感知生成
- **自动检测项目类型**：通过检测 `docs/design/design-line.md` 或 `docs/analysis/codebase-analysis.md` 自动判断是否为遗留项目
- **遗留项目**：自动使用上下文感知模式，基于设计主线和代码库分析生成与存量风格一致的代码
- **新项目**：使用标准代码生成模式
- **设计文档驱动**：支持直接按设计文档依次执行所有功能模块

---

**文件落盘**：凡写入仓库内文件（含更新 `docs/tasks.md`、生成前后端代码）须遵守 [SKILLS-FILE-OUTPUT.md](../SKILLS-FILE-OUTPUT.md)；新项目前后端目录另见下文「检查 0」。

---

## 输入来源（单一事实来源，强制）

`gen-code` 从以下两个来源读取输入，**优先级明确**：

### 1. 契约文件（机器可读，优先）

若采用契约驱动开发，优先读取机器可读的 YAML 契约文件：

| 契约文件 | 路径 | 用途 | 读取时机 |
|---------|------|------|---------|
| **数据库契约** | `docs/contracts/database-contract.yaml` | 表结构、字段定义、索引、外键 | 数据层任务（Entity/Mapper/SQL） |
| **接口契约** | `docs/contracts/api-contract.yaml` | API 路径、请求/响应定义、错误码 | 接口层任务（Controller/前端 API） |

**读取规则**：
- **若契约文件存在**：优先使用 YAML 契约（结构精确，无歧义）
- **若契约文件不存在**：降级使用设计文档 + 技术规范

### 2. 技术规范（人类可读，风格标准）

`gen-coding-specs` 生成的技术规范，定义编码风格和标准：

| 项 | 路径 | 用途 |
|----|------|------|
| **根目录** | `docs/coding-specs/`（相对仓库根） |
| **索引** | `docs/coding-specs/coding.index.md` | 技术栈概览、规范分册列表 |
| **分册** | `coding.api.md`、`coding.architecture.md`、`coding.data-models.md`、`coding.vue.md`、`coding.coding-style.md`、`coding.testing.md`、`coding.security.md`、`coding.performance.md`、`coding.documentation.md`、`coding.code-review.md`、`coding.version-control.md` | 按任务类型读取对应分册 |

**读取规则**：
- **必须读取**：`coding.index.md`（确认技术栈）
- **按需读取**：按任务类型读取对应分册（如数据层任务读 `coding.data-models.md`）

### 3. 来源优先级与分工

| 信息类型 | 来源 | 优先级 | 说明 |
|---------|------|--------|------|
| 表名、字段名、类型 | `database-contract.yaml` | 🔴 高 | 精确结构定义 |
| 表命名风格（下划线/驼峰） | `coding.data-models.md` | 🟡 中 | 风格规范 |
| API 路径、参数、响应 | `api-contract.yaml` | 🔴 高 | 精确接口定义 |
| 接口风格（POST/GET、URL 格式） | `coding.api.md` | 🟡 中 | 风格规范 |
| 代码格式、命名规范 | `coding.coding-style.md` | 🟡 中 | 编码风格 |
| 测试要求 | `coding.testing.md` | 🟡 中 | 测试规范 |

**缺失时的处理**：

- 若 `docs/coding-specs/` 不存在，或缺少 `coding.index.md`：输出提示 **先执行 `/gen-coding-specs`（或等价技能）生成技术规范**；仅在用户明确选择「跳过规范、高风险继续」时方可仅依赖设计文档与任务描述生成代码。
- 若 `docs/contracts/` 不存在：自动降级使用设计文档中的定义（非契约驱动模式）

---

## 前置条件

- 任务列表已生成，或用户已提供清晰的任务描述
- **遗留项目**：建议先执行 `/analyze --phase=deep` 生成设计主线，以获得最佳生成效果
- **任务范围说明**：支持 `Task-001..010` 形式指定范围，将按批生成（默认每批 3 个任务，可询问用户调整）

---

## 前置检查（增强版）

### 检查 0：新项目仓库布局与前后端目录（强制，空仓库 / 前后端分离）

**问题背景**：从零创建的空仓库通常没有 `src/main/java` 或独立的前后端工程根目录；若仍按单体路径生成，会导致前后端代码混在同一层级或写入失败。

**适用条件**（满足任一即执行本检查）：
- 判定为**新项目**（未检测到 `docs/design/design-line.md` 且未检测到 `docs/analysis/codebase-analysis.md`），且
- PRD/设计文档/任务描述为**前后端分离**（如 Vue + Spring Boot、React + Node），或任务类型列含「前端」「后端」「接口层」「页面」等需分端落位的信息。

**执行步骤**：

1. **读取目录约定**（按优先级）  
   - 优先从 `docs/design/*.md` 的 **「仓库与代码目录结构」**（或等价小节）读取 `frontendRoot` / `backendRoot`（或表格中的前端根目录、后端根目录）。  
   - 若设计文档未写明：从 PRD「技术栈/部署」推断为前后端分离时，**询问用户一次**确认根目录命名，或使用下列**默认约定**（二选一须在后续任务中保持一致）：  
     - **默认 A**：`frontend/`（前端 SPA）、`backend/`（后端 API）  
     - **默认 B**：`web/`、`server/`（若用户更习惯短名）

2. **创建目录（必须先于写文件）**
   - 若 `frontendRoot` 或 `backendRoot` 对应路径在仓库中**不存在**，**必须先创建**该目录（及后续代码所需的最小子路径，例如 `frontend/src`、`backend/src/main/java` 等，按技术栈惯例）。
   - **禁止**在父目录不存在时直接写深层文件；**禁止**因未建目录而仅输出代码到对话中。

2.5. **项目脚手架初始化（基于技术栈，强制）**

   **问题背景**：新项目空仓库即使创建了目录结构，也缺少 `pom.xml`、`package.json` 等项目配置文件，导致生成的代码无法构建和运行。本步骤根据设计文档中的技术栈自动生成对应的项目脚手架。

   **触发条件**（前后端独立判断）：
   - 后端：`{backendRoot}` 不存在 **任何** 项目配置文件（`pom.xml` / `build.gradle` / `requirements.txt` / `go.mod`）
   - 前端：`{frontendRoot}` 不存在 `package.json`

   **技术栈识别**（按优先级）：
   1. `docs/coding-specs/coding.index.md` → 「技术栈概览」小节
   2. `docs/design/*.md` → 设计文档中的技术栈定义
   3. 向用户确认

   **支持的后端技术栈**：

   | 技术栈 | 识别特征 | 脚手架产物 |
   |--------|---------|-----------|
   | Spring Boot 3 + Maven | spring-boot-starter | pom.xml、Application.java、application.yml（dev/prod）、CorsConfig、Result、PageResult、GlobalExceptionHandler、.gitignore |
   | Spring Boot 3 + Gradle | build.gradle | build.gradle、settings.gradle、同上配置与代码文件 |
   | Python + FastAPI | fastapi | requirements.txt、main.py、config.py、models/、api/、routers/、.gitignore |
   | Python + Django | django | requirements.txt、manage.py、settings.py、urls.py、wsgi.py、apps/、.gitignore |
   | Python + Flask | flask | requirements.txt、app.py、config.py、blueprints/、.gitignore |
   | Node.js + Express | express | package.json、tsconfig.json、src/app.ts、src/routes/、src/middleware/、.gitignore |
   | Go + Gin | gin | go.mod、main.go、config/、handler/、model/、middleware/、.gitignore |

   **支持的前端技术栈**：

   | 技术栈 | 识别特征 | 脚手架产物 |
   |--------|---------|-----------|
   | Vue 3 + Vite + TypeScript | vue + vite | package.json、vite.config.ts、tsconfig.json、index.html、main.ts、App.vue、router/、stores/、api/request.ts、.env.development、.gitignore |
   | React + Vite + TypeScript | react + vite | package.json、vite.config.ts、tsconfig.json、index.html、main.tsx、App.tsx、router/、api/request.ts、.env.development、.gitignore |
   | Vue 3 + Vite + JavaScript | vue（无 TS） | 同 Vue 3 TS 但去掉 tsconfig.json，使用 .js 文件 |

   **生成规则**：
   - 版本号从 `coding.index.md` 读取（如 Spring Boot 3.2.x、Vue 3.3.x）
   - 包名 / GroupId 从设计文档读取（如 `com.example.points`），或询问用户确认
   - 配置文件内容基于项目定制：数据库/Redis 连接从设计文档读取、代理目标从 API 地址读取
   - 前后端可独立触发（纯后端项目不生成前端脚手架）

   **防重复**：生成后在 `{root}/.scaffold-initialized` 写入时间戳，后续任务检测到该文件则跳过。

   **输出确认示例**：
   ```
   检测到新项目，需要初始化项目脚手架。

   **技术栈识别**：
   - 后端：Spring Boot 3.2 + MyBatis-Plus 3.5 + MySQL 8.0 + Redis 7.x
   - 前端：Vue 3.3 + TypeScript + Vite 5.x + Ant Design Vue 4.x + Pinia

   将生成后端脚手架（backend/）和前端脚手架（frontend/），具体文件清单见 [prompt.md 脚手架模板]。
   是否确认生成？
   Y) 确认  N) 修改技术栈  C) 跳过（不推荐，项目将无法构建）
   ```

   **脚手架模板的完整定义**见 [prompt.md](./prompt.md)「项目脚手架初始化」节。

3. **路径映射规则**（生成时严格遵守）  
   - **后端**：Java/Kotlin Controller、Service、Mapper、Entity、SQL 脚本、Spring 配置等 → 写入 **backendRoot** 下（保持包路径 `src/main/java/...`）。  
   - **前端**：Vue/React 页面、组件、`api/` 调用封装、路由、样式等 → 写入 **frontendRoot** 下。  
   - **任务表驱动**：若 `docs/tasks.md` 中任务标注了「类型：后端 / 前端 / 数据层」或 `layer: backend|frontend`，必须与上述根目录一致；若任务写错层级，应先提醒用户或按设计文档纠正再生成。

4. **与存量项目的区别**  
   - **存量项目**：以现有工程结构为准（上下文感知），不强行改为 `frontend/` + `backend/`，除非设计文档明确要求迁移。  
   - **新项目 + 前后端分离**：必须遵循本节，避免混用仓库根下单一 `src/` 表示全栈。

5. **自检清单（写入每个文件前）**
   - [ ] 已确定 `frontendRoot` 与 `backendRoot`（来自设计文档或用户确认或默认约定）
   - [ ] 根目录已存在或已创建
   - [ ] 项目脚手架已初始化（pom.xml / package.json 等配置文件已生成，或已存在）
   - [ ] 当前任务属于前端或后端之一，路径前缀正确  

---

### 检查 1：存量项目检测（强制）

**检测逻辑**：
```
IF (docs/design/design-line.md EXISTS OR docs/analysis/codebase-analysis.md EXISTS) THEN
  判定为存量项目
  输出提示：「检测到当前项目为存量项目（已存在设计主线或代码库分析报告）」
  给出选项：
    A) 仍使用 /gen-code（自动启用上下文感知模式，确保与现有架构一致）
    B) 强制使用标准模式（不推荐，可能产生边界违规）
  
  IF 用户选择 B THEN
    输出警告：「⚠️ 警告：在存量项目中使用 /gen-code 可能导致：
      - 违反服务边界（跨服务访问数据库或内部实现）
      - 违反微前端边界（破坏子应用独立性）
      - 与现有代码风格不一致
      - 产生技术债务
    
    是否确认继续？（建议先阅读 docs/design/design-line.md）」
    
    IF 用户再次确认 THEN
      继续执行，但在生成代码时增加边界检查
    ELSE
      终止，建议使用 /gen-code（自动检测为遗留项目）
  ELSE
    终止，建议使用 /gen-code（自动检测为遗留项目）
```

### 检查 2：设计文档检查（强制）

**检测逻辑**：
```
IF (用户按任务编号生成 AND 未提供设计文档路径) THEN
  检查 docs/design/ 下是否存在设计文档
  
  IF (设计文档不存在) THEN
    输出提示：「⚠️ 未找到设计文档，无法读取数据流与集成契约」
    给出选项：
      A) 先执行 /gen-design 生成设计文档（推荐）
      B) 提供设计文档路径
      C) 跳过设计文档检查，基于任务描述生成（不推荐）
    
    IF 用户选择 C THEN
      输出警告：「⚠️ 警告：跳过设计文档检查可能导致：
        - 数据流与整体架构不一致
        - 集成点未正确实现
        - 产生技术债务
      
      是否确认继续？」
      
      IF 用户再次确认 THEN
        继续执行，但标记为「高风险生成」
      ELSE
        终止，建议用户先执行 /gen-design
  ELSE
    从设计文档读取数据流与集成契约
```

### 检查 3：设计验证检查（推荐）

**检测逻辑**：
```
IF (设计文档存在) THEN
  检查是否已执行设计验证（查看 docs/reviews/ 下是否有验证报告）
  
  IF (设计验证未执行) THEN
    输出提示：「💡 建议先执行 /validate --mode=dataflow 验证设计文档」
    给出选项：
      A) 先执行 /validate --mode=dataflow（推荐）
      B) 跳过验证，直接生成代码
    
    IF 用户选择 B THEN
      输出提示：「好的，将跳过设计验证直接生成代码。若后续发现设计问题，可能需要重新生成。」
```

### 检查 4：任务 - 数据流映射检查（推荐）

**检测逻辑**：
```
IF (docs/tasks.md 存在) THEN
  检查任务是否标注所属数据流（dataflow: DF-XXX）
  
  IF (任务未标注数据流) THEN
    输出提示：「💡 任务未标注所属数据流，可能导致生成的代码与整体数据流不一致」
    给出选项：
      A) 先执行 /gen-tasks 重新生成任务列表（推荐）
      B) 手动指定数据流编号
      C) 跳过检查，直接生成代码
    
    IF 用户选择 C THEN
      输出提示：「好的，将跳过数据流映射检查直接生成代码。」
```

---

## 阻断策略说明

**P0 阻断（必须修复）**：
- 存量项目未确认边界约束 → 阻断
- 设计文档不存在且用户拒绝生成 → 阻断

**P1 阻断（强烈建议修复）**：
- 设计验证未执行 → 警告，用户确认后可继续
- 任务未标注数据流 → 警告，用户确认后可继续

**P2 提示（可选修复）**：
- 代码风格与存量不一致 → 提示，生成后建议 review

---

## 上下文感知模式

### 自动检测

技能会自动检测项目类型：

```
检测到当前项目为遗留项目（已存在设计主线或代码库分析报告）。
将自动启用上下文感知模式，基于现有架构和代码风格生成代码。

设计主线: docs/design/design-line.md
代码分析: docs/analysis/codebase-analysis.md

是否继续？
```

### 上下文感知生成规则

在上下文感知模式下，生成的代码将遵循：

1. **风格一致性**
   - 命名风格（驼峰/下划线）
   - 代码格式（缩进、换行、括号）
   - 注释风格（Javadoc/行内注释）
   - 日志规范

2. **架构一致性**
   - 分层结构（Controller/Service/Repository）
   - 设计模式（策略、工厂等）
   - 异常处理方式
   - 事务处理机制

3. **技术栈一致性**
   - 使用项目已有的依赖库
   - 遵循项目配置（Spring、数据库等）
   - 使用项目的工具类
   - 遵循安全规范

4. **边界约束**
   - **服务边界**：微服务架构下，不跨服务直接访问其他服务的数据库或内部实现
   - **微前端边界**：微前端架构下，不破坏子应用边界

---

## 技能行为

### 任务范围（分批）模式（仅当用户指定 Task-XXX..YYY 时）

当用户指定任务范围（如 `/gen-code Task-001..010`）时：

1. **解析范围**：从 `docs/tasks.md` 确认 Task-001 至 Task-010 存在且顺序明确。
2. **分批计划**：默认每批 3 个任务（可询问用户「分批大小：3 个任务/批，是否修改？」），输出分批计划。
3. **确认后按批执行**：每批内对每个任务依次执行「阶段零」→「阶段一」→「阶段二」→「阶段二点五」→「阶段三」，完成一批后询问「是否继续下一批？」直至全部完成。

### 设计文档驱动模式

当用户使用 `/gen-code --from-design docs/design/xxx-design.md` 时：

**功能**：直接按设计文档依次执行所有功能模块，自动调用 gen-tasks 生成任务列表。

**核心改进（v2.4）**：
- **不再自己生成执行计划**，而是调用 gen-tasks 生成标准任务列表
- 复用 gen-tasks 的实现点清单，确保任务完成度检查正常工作
- 任务列表格式与手动执行 /gen-tasks 完全一致

**执行流程**：

```
/gen-code --from-design docs/design/points-design.md
        │
        ▼
┌───────────────────────┐
│ 阶段一：前置检查      │
│ - 检查设计文档存在    │
│ - 检查设计验证报告    │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ 阶段二：调用 gen-tasks│  ← 复用 gen-tasks 能力
│ - 生成标准任务列表    │
│ - 包含实现点清单      │
│ - 包含功能单元划分    │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ 阶段三：用户确认      │
│ - 展示任务列表        │
│ - 确认是否开始执行    │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ 阶段四：依次执行任务  │
│ - 代码复用检测        │
│ - 生成代码            │
│ - 完成度检查          │
│ - 更新任务状态        │  ← v2.4 新增
│ - 质量门禁检查        │
│ - 自动进入下一任务    │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ 阶段五：完成报告      │
│ - 汇总所有任务结果     │
│ - 列出遗留问题         │
│ - 提供下一步建议       │
│ - 更新任务列表状态     │  ← v2.4 新增
└───────────────────────┘
```

**输出示例**：

```
正在检查设计文档...

✅ 设计文档存在：docs/design/points-design.md
✅ 设计验证通过：docs/reviews/points-design-validation.md

正在调用 gen-tasks 生成任务列表...

**任务列表已生成**（docs/tasks.md）

## 功能单元概览
| 功能单元 | 描述 | 任务数 | 状态 |
|----------|------|--------|------|
| FU-001 | 积分获取 | 6 | ⏳ 待执行 |
| FU-002 | 积分消费 | 4 | ⏳ 待执行 |
| FU-003 | 积分查询 | 3 | ⏳ 待执行 |

## 任务列表
| 序号 | 任务编号 | 任务名称 | 类型 | 工时 | 依赖 | 状态 |
|------|----------|----------|------|------|------|------|
| 1 | Task-001 | 积分表设计 | 数据层 | 2h | - | ⏳ 待执行 |
| 2 | Task-002 | 积分实体与Mapper | 数据层 | 4h | Task-001 | ⏳ 待执行 |
| 3 | Task-003 | 积分计算服务 | 业务层 | 4h | Task-002 | ⏳ 待执行 |
| 4 | Task-004 | 积分API实现 | 接口层 | 4h | Task-003 | ⏳ 待执行 |
| 5 | Task-005 | 积分展示组件 | 前端 | 3h | Task-004 | ⏳ 待执行 |
| 6 | Task-006 | FU-001集成测试 | 集成 | 4h | Task-001~005 | ⏳ 待执行 |

**总任务数**：13（含集成任务）
**预计总工时**：42h

是否开始执行？
A) 开始执行所有任务（推荐）
B) 选择部分任务执行
C) 查看详细任务清单（含实现点）
```

**执行过程**：

```
正在执行任务 [1/13]：Task-001 积分表设计

[阶段零：代码复用检测]
检测到可复用组件：DateUtils、StringUtils、Result
是否复用？ A) 确认  B) 说明原因

[阶段一：任务上下文确认]
任务描述：设计用户积分表结构
所属数据流：DF-002 积分获取与扣减流
所属功能单元：FU-001 积分获取

实现点清单：
- [ ] IP-001: 创建 points_balance 表
- [ ] IP-002: 创建 points_record 表
- [ ] IP-003: 设计索引（user_id, created_at）
- [ ] IP-004: 添加外键约束

[阶段二：生成代码]
✅ 已生成：V1__create_points_tables.sql

[阶段二点五：任务完成度检查]
实现点完成度：100%（4/4）
✅ 任务完成度检查通过

[阶段三：代码质量门禁检查]
✅ 质量门禁检查通过

[阶段四：更新任务状态]  ← v2.4 新增
✅ 已更新 docs/tasks.md：Task-001 状态 → ✅ 已完成

────────────────────────────────────

正在执行任务 [2/13]：Task-002 积分实体与Mapper
...

────────────────────────────────────

正在执行任务 [13/13]：Task-013 FU-003集成测试
...

────────────────────────────────────

**执行完成报告**

## 执行概览
- 总任务数：13
- 成功：11
- 部分完成：1
- 失败：0
- 跳过：1
- 总耗时：约 38h

## 任务执行详情
| 任务 | 状态 | 完成度 | 备注 |
|------|------|--------|------|
| Task-001 | ✅ 已完成 | 100% | - |
| Task-002 | ✅ 已完成 | 100% | - |
| Task-003 | ✅ 已完成 | 100% | - |
| Task-004 | ⚠️ 部分完成 | 85% | 缺少异常处理 |
| Task-005 | ✅ 已完成 | 100% | - |
| Task-006 | ✅ 已完成 | 100% | - |
| ... | ... | ... | ... |

## 遗留问题
1. Task-004 积分API实现缺少异常处理（建议补充）
2. 建议执行 /validate --mode=integration 进行完整集成验证

## 下一步建议
1. 补充积分API异常处理
2. 执行 /review-code src/ 进行代码审查
3. 执行 /gen-test src/ 生成测试用例
```

### 自动执行模式（v2.4 新增）

当用户使用 `/gen-code --auto` 时：

**功能**：自动读取任务列表并依次执行所有任务。

**执行流程**：

```
/gen-code --auto
        │
        ▼
┌───────────────────────┐
│ 读取 docs/tasks.md    │
│ 识别所有任务          │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ 检查已完成任务        │
│ 确定起始任务          │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ 依次执行未完成任务    │
│ - 代码复用检测        │
│ - 生成代码            │
│ - 完成度检查          │
│ - 质量门禁检查        │
│ - 更新任务状态        │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ 遇到问题暂停          │
│ 用户确认后继续        │
└───────────────────────┘
```

**输出示例**：

```
正在读取任务列表...

**任务列表概览**
- 总任务数：13
- 已完成：3
- 待执行：10

**待执行任务**
| 序号 | 任务编号 | 任务名称 | 状态 |
|------|----------|----------|------|
| Task-004 | 积分计算服务 | ⏳ 待执行 |
| Task-005 | 积分API实现 | ⏳ 待执行 |
| Task-006 | 积分展示组件 | ⏳ 待执行 |
| ... | ... | ... |

是否开始自动执行？
A) 开始执行（推荐）
B) 从指定任务开始
C) 查看详细任务清单
```

### 继续执行模式（v2.4 新增）

当用户使用 `/gen-code --continue` 时：

**功能**：继续执行下一个待执行的任务。

**适用场景**：
- 上次执行中断后继续
- 单任务执行后想继续下一个
- 逐步执行任务

**输出示例**：

```
正在查找下一个待执行任务...

**下一个任务**
- 任务编号：Task-004
- 任务名称：积分计算服务
- 所属功能单元：FU-001 积分获取功能

是否开始执行？
A) 开始执行  B) 跳过此任务  C) 查看任务详情
```

### 阶段零：代码复用检测（v2.4 新增，强制执行）

**重要**：在生成代码前，必须先执行代码复用检测，确保不会重复造轮子。

**检测内容**：
1. **可复用组件检测**：扫描项目中的工具类、基础组件、业务服务
2. **相似代码检测**：检测与当前任务功能相似的现有代码
3. **现有依赖检测**：分析项目已有依赖，避免引入重复依赖

**输出示例**：
```
正在执行代码复用检测...

**可复用组件检测报告**

## 检测概览
- 扫描目录：src/
- 检测到可复用组件：23 个
- 与当前任务相关：5 个

## 推荐复用组件

### 工具类（强烈推荐复用）

| 组件名 | 路径 | 功能描述 | 复用建议 |
|--------|------|----------|----------|
| DateUtils | src/main/java/com/example/util/DateUtils.java | 日期格式化、解析 | ⭐ 直接使用 |
| StringUtils | src/main/java/com/example/util/StringUtils.java | 字符串处理 | ⭐ 直接使用 |
| EncryptUtils | src/main/java/com/example/util/EncryptUtils.java | MD5/AES加密 | ⭐ 直接使用 |

### 基础组件（必须使用）

| 组件名 | 路径 | 功能描述 | 复用建议 |
|--------|------|----------|----------|
| Result | src/main/java/com/example/common/Result.java | 统一响应类 | ⭐ 必须使用 |
| PageResult | src/main/java/com/example/common/PageResult.java | 分页响应类 | ⭐ 必须使用 |
| GlobalExceptionHandler | src/main/java/com/example/exception/GlobalExceptionHandler.java | 全局异常处理 | ⭐ 必须使用 |

### 相似代码检测

| 相似代码 | 相似度 | 建议 |
|----------|--------|------|
| PointsService.java | 85% | 可参考现有积分计算逻辑 |
| OrderService.java | 60% | 可参考订单处理流程 |

## 禁止重复实现

⚠️ 以下组件已存在，**禁止重新实现**：

1. **DateUtils** - 已有日期工具类，禁止新建 DateUtil、DateHelper 等
2. **StringUtils** - 已有字符串工具类，禁止新建 StringHelper 等
3. **Result** - 已有统一响应类，禁止新建 Response、ApiResponse 等

## 复用确认

请确认以下事项：
- [ ] 我已阅读可复用组件清单
- [ ] 我将在代码中使用现有工具类
- [ ] 我不会重新实现已存在的组件

是否确认？
A) 确认，开始生成代码
B) 我有特殊原因需要重写（需说明）
C) 查看更多详情
```

**强制阻断规则**：

| 情况 | 处理 |
|------|------|
| 检测到可复用工具类但用户选择重写 | 阻断，要求说明原因 |
| 检测到相似度 > 80% 的代码 | 阻断，要求确认是否复用 |
| 尝试引入禁止依赖 | 阻断，要求使用替代方案 |

### 阶段一：任务上下文确认（含契约文件读取）

若存在设计文档（`docs/design/*.md`），**必须**先从中读取「数据流主线」「集成点清单」。
若存在契约文件（`docs/contracts/*.yaml`），**必须优先读取**契约文件中的精确结构定义。

```
正在分析 Task-001：用户积分表设计

**任务描述**：
设计用户积分表结构，包括字段定义、索引设计。

**数据流与集成契约**（从设计文档读取）：
- 所属数据流：DF-001 积分获取流
- 所属功能单元：FU-001 积分管理
- 上游输入：用户签到事件
- 下游输出：积分余额更新、积分流水记录

**契约文件检测**：
- ✅ 检测到数据库契约：docs/contracts/database-contract.yaml
  - 表定义：points_balance、points_record
  - 字段数：6 字段 + 9 字段
  - 索引定义：3 个索引
- ✅ 检测到接口契约：docs/contracts/api-contract.yaml
  - API 定义：3 个接口（GET /api/points/balance、POST /api/points/sign-in、...）

**实现点清单**（来自 gen-tasks）：
- [ ] IP-001: 创建 points_balance 表（对照契约：6 字段）
- [ ] IP-002: 创建 points_record 表（对照契约：9 字段）
- [ ] IP-003: 设计索引（idx_user_id、idx_created_at）
- [ ] IP-004: 添加外键约束（fk_user → user.id）

**验收标准**：
- 表结构与契约文件一致（优先）或设计文档一致（无契约时）
- 索引覆盖常用查询
- 字段类型与契约定义的 javaType 一致

**技术栈确认**：
- ✅ 前端：Vue 3 + Ant Design Vue
- ✅ 后端：Spring Boot 3 + MyBatis-Plus
- ✅ AI 能力：LangChain4j（如需要）

**技术规范（已读文件）**：
- ✅ `docs/coding-specs/coding.index.md`（技术栈概览）
- ✅ `docs/coding-specs/coding.data-models.md`（数据模型规范：命名风格、索引规范）
- ✅ `docs/coding-specs/coding.coding-style.md`（编码风格：Java 命名规范）

**数据来源优先级**：
1. **结构定义**（表名、字段名、类型）：使用 `database-contract.yaml`（机器可读，精确）
2. **命名风格**（下划线/驼峰）：遵循 `coding.data-models.md`（人类可读，风格）
3. **代码格式**：遵循 `coding.coding-style.md`

**项目类型**：遗留项目（自动启用上下文感知模式）
- 设计主线：docs/design/design-line.md
- 代码分析：docs/analysis/codebase-analysis.md

生成代码时将遵循上述数据流、契约定义与技术规范，并保持与现有代码风格一致。是否按此设计生成代码？
```

### 阶段二：生成代码

根据项目类型选择生成模式：

**新项目模式**：
- 使用标准技术栈和最佳实践
- 遵循默认编码规范

**遗留项目模式（上下文感知）**：
- 读取设计主线和代码库分析
- 学习现有代码风格
- 生成与存量风格一致的代码

```
正在生成代码...

✅ 已生成以下文件：

【后端代码】
**实体类**：
- src/main/java/com/example/points/entity/PointsBalance.java

**Mapper 接口**：
- src/main/java/com/example/points/mapper/PointsBalanceMapper.java

**Service 层**：
- src/main/java/com/example/points/service/PointsService.java
- src/main/java/com/example/points/service/impl/PointsServiceImpl.java

**Controller 层**：
- src/main/java/com/example/points/controller/PointsController.java

**配置文件**：
- src/main/resources/application.yml
- src/main/resources/mapper/PointsBalanceMapper.xml

【前端代码】（如需要）
**Vue 组件**：
- src/views/points/PointsQuery.vue
- src/api/points.ts

**单元测试**：
- src/test/java/com/example/points/mapper/PointsBalanceMapperTest.java
```

### 阶段二点五：任务完成度检查

**重要**：生成代码后，必须对照实现点清单检查任务完成度。完成度 < 80% 必须补充实现。

```
正在执行任务完成度检查...

**实现点完成情况**：

| 实现点 | 状态 | 说明 |
|--------|------|------|
| IP-001: 创建 points_balance 表 | ✅ 已完成 | V1__create_points_tables.sql |
| IP-002: 创建 points_record 表 | ✅ 已完成 | V1__create_points_tables.sql |
| IP-003: 设计索引（user_id, created_at） | ✅ 已完成 | 已添加索引 |
| IP-004: 添加外键约束 | ✅ 已完成 | 已添加外键 |

**完成度统计**：
- 总实现点：4
- 已完成：4
- 未完成：0
- 完成度：100%

✅ 任务完成度检查通过（≥ 80%）

**若完成度 < 80%**：
```
⚠️ 任务完成度检查未通过

**完成度统计**：
- 总实现点：4
- 已完成：2
- 未完成：2
- 完成度：50%（< 80%）

**未完成的实现点**：
- IP-003: 设计索引（user_id, created_at）
- IP-004: 添加外键约束

正在自动补充遗漏的实现点...

补充完成后重新检查...
```

### 阶段三：代码质量门禁检查（生成后必须执行）

**重要**：生成代码后，必须执行以下质量门禁检查。任何 P0 检查项不通过，必须重新生成代码。

```
正在执行代码质量门禁检查...

**P0 强制检查项**：

□ 复杂度检查
  - 方法长度 ≤ 80 行
  - 嵌套深度 ≤ 3 层
  - 参数数量 ≤ 5 个
  - 圈复杂度 ≤ 10

□ 安全检查
  - SQL 使用 #{} 而非 ${}（防止注入）
  - 无 XSS 漏洞（用户输入已转义）
  - 无敏感信息硬编码（密码、密钥等）
  - 接口有权限控制

□ 空指针防护
  - 外部输入有 null 检查
  - 集合操作前有判空
  - Optional 使用正确

□ 事务正确性
  - 多表操作在事务中
  - 事务范围合理（无远程调用在事务内）
  - 异常回滚配置正确

□ 测试覆盖
  - 核心业务逻辑有测试
  - 异常分支有测试

**P1 设计一致性检查**：

□ 接口一致性
  - API 路径与设计文档一致
  - 请求/响应字段与设计一致

□ 数据一致性
  - 数据库字段与设计一致
  - 数据类型与设计一致

□ 数据流一致性
  - 输入来源与设计一致
  - 输出目标与设计一致
  - 集成点实现正确

□ 上下文一致性（遗留项目模式）
  - 代码风格与现有项目一致
  - 架构分层与现有项目一致
  - 命名规范与现有项目一致
```

### 阶段四：更新任务状态

**重要**：任务执行完成后，必须更新 docs/tasks.md 中的任务状态。

```
正在更新任务状态...

✅ 已更新 docs/tasks.md：
- Task-001 状态：⏳ 待执行 → ✅ 已完成
- 完成度：100%
- 完成时间：2026-03-07 14:30:00

**当前进度**：
- 总任务数：13
- 已完成：1
- 待执行：12
- 完成率：7.7%
```

### 阶段五：代码健康度评分

```
**代码健康度评分**：

| 维度 | 得分 | 说明 |
|------|------|------|
| 可读性 | 95/100 | 命名清晰，注释完整 |
| 可维护性 | 88/100 | 方法适中，结构清晰 |
| 安全性 | 100/100 | 无安全风险 |
| 测试覆盖 | 90/100 | 核心路径已覆盖 |
| 复杂度 | 92/100 | 整体简洁 |
| 上下文一致性 | 96/100 | 与现有项目风格一致（遗留项目模式） |

**综合得分**：93/100 (A)

✅ 质量门禁检查通过

是否继续 Task-002？
```

**若质量门禁不通过**：
```
⚠️ 代码质量门禁检查未通过

| 检查维度 | 结果 | 问题详情 |
|----------|------|----------|
| 复杂度 | ❌ 不通过 | processOrder() 方法 120 行，超过 80 行限制 |
| 嵌套深度 | ❌ 不通过 | 第 45 行嵌套深度 4 层，超过 3 层限制 |
| 上下文一致性 | ❌ 不通过 | 命名风格与现有项目不一致（应使用下划线而非驼峰） |

**代码健康度评分**：72/100 (C)

正在分析问题并重新生成代码...
```

---

## 质量门禁标准

### 复杂度标准

| 指标 | 阈值 | 说明 |
|------|------|------|
| 方法长度 | ≤ 80 行 | 超过则拆分方法 |
| 嵌套深度 | ≤ 3 层 | 超过则使用提前返回或提取方法 |
| 参数数量 | ≤ 5 个 | 超过则封装为 DTO |
| 圈复杂度 | ≤ 10 | 超过则拆分方法或使用策略模式 |

### 安全标准

| 检查项 | 要求 | 违规示例 | 正确示例 |
|--------|------|----------|----------|
| SQL 注入 | 使用 #{} | `WHERE id = ${id}` | `WHERE id = #{id}` |
| XSS | 输入转义 | 直接输出用户输入 | `HtmlUtils.htmlEscape()` |
| 敏感信息 | 禁止硬编码 | `password = "123456"` | 使用配置或密钥管理 |
| 权限控制 | 接口鉴权 | 无鉴权直接暴露 | `@PreAuthorize("hasRole('ADMIN')")` |

### 代码健康度等级

| 等级 | 分数范围 | 说明 | 处理建议 |
|------|----------|------|----------|
| A+ | 95-100 | 优秀 | 可直接使用 |
| A | 90-94 | 良好 | 可直接使用 |
| B+ | 85-89 | 较好 | 建议优化后使用 |
| B | 80-84 | 合格 | 需小幅优化 |
| C | 70-79 | 需改进 | 必须优化后使用 |
| D | 60-69 | 较差 | 需要重构 |
| E | <60 | 不合格 | 需要重新生成 |

**强制要求**：代码健康度评分必须 ≥ 80 分（B 级及以上）才能输出，否则必须重新生成。

---

## 相关技能

### 前置技能

- **gen-design**: 系统设计，提供设计文档（数据流、集成点）
- **gen-coding-specs**: 技术规范生成，提供 **`docs/coding-specs/`**（编码风格、API 规范、数据模型规范）
  - 无则须提示用户先执行或接受高风险跳过（见上文「输入来源」）
- **contract-gen**: 契约生成，提供 **`docs/contracts/*.yaml`**（数据库契约、接口契约）
  - 若采用契约驱动开发，本技能优先读取 YAML 契约
  - 若无契约文件，自动降级使用设计文档 + 技术规范
- **gen-tasks**: 任务拆解，提供 `docs/tasks.md`（任务列表、实现点清单）
- **analyze**: 存量分析，遗留项目的前置技能（生成设计主线、代码库分析）

### 后续技能

- **validate --mode=task-completion**: 任务完成度验证
- **validate --mode=contract-consistency**: 代码与契约一致性验证（契约驱动模式）
- **review-code**: 代码审查

衔接总览见 [SKILL-VALUE-CHAIN.md](../SKILL-VALUE-CHAIN.md)。

---

## 版本历史

| 版本 | 日期 | 变更说明 |
|------|------|----------|
| 2.5.0 | 2026-03-24 | 新增步骤 2.5：基于技术栈的项目脚手架自动初始化（Spring Boot/Python/Node.js/Go + Vue/React） |
| 2.4.1 | 2026-03-24 | 新增「检查 0」：新项目空仓库前后端分离时的目录创建与 frontend/backend 根路径落位 |
| 2.4.0 | 2026-03-07 | 设计文档驱动模式（自动调用gen-tasks）、自动执行模式、继续执行模式、代码复用检测（强制）、任务完成度检查（强制）、任务状态自动更新 |
| 2.3.0 | 2026-03-06 | 新增代码复用检测阶段、任务完成度检查阶段 |
| 2.0.0 | 2026-03-05 | 新增设计主线驱动模式、存量项目支持增强 |
| 1.0.0 | 2026-03-01 | 初始版本 |

---

*本技能是 AI Speckits 技能体系的编码实现阶段。*
