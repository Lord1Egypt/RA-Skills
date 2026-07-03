# Phase 1: 项目初始化

## 目标

建立项目骨架，定义目录结构、配置接口和依赖声明。这是整个 Agent 系统的地基 —— 目录结构决定信息的可发现性，配置接口决定系统的可配置性。

## 前置条件

> 如果用户未提供技术栈、构建规模、LLM 供应商等信息，**必须先确认**（参考 SKILL.md "需求确认"章节），不得自行假设。

确认后锁定以下关键变量，它们直接影响本 Phase 的产物：

| 变量 | 影响 |
|------|------|
| 技术栈 (Python/Node.js/Go) | 决定脚手架语言、包管理器、入口文件格式 |
| 构建规模 (Minimal/Professional/Enterprise) | 决定目录层级深度、配置复杂度、三方库选择 |
| 沙箱隔离需求 | 决定 `sandbox/` 目录是否存在、安全策略文件 |
| 监控需求 | 决定 `logging` 配置复杂度、OpenTelemetry 基础设施 |

---

## Design Principles

### Principle 1: Context Engineering — 目录结构即信息的可访问性

Agent 系统中，**目录结构本身就是上下文工程**。文件存放位置决定了 Agent 能否高效定位信息：

- **静态上下文**（规则、约束、角色定义）放在 `config/`，Agent 在会话初始化时统一加载
- **动态上下文**（workspace 操作结果、skill 产物）放在 `workspace/`，按需读取
- **持久状态**（记忆、会话日志）放在 `memory/` 和 `sessions/`，不可变、只追加

核心原则：**"Agent 无法在上下文中访问的信息不存在"**。如果一个配置文件放在不会被加载的路径，就等于它不存在。

### Principle 2: Architectural Constraints — 通过目录结构建立边界

不使用注释"请勿修改"，而是用**物理分区**强制执行：

- `src/` 目录：框架核心代码，框架升级时会被整体替换。用户不应在其中添加代码
- `config/` 目录：用户配置区域，框架升级时不受影响
- `skills/` 目录：用户自定义能力扩展，与框架代码物理隔离
- `workspace/` 目录：Agent 运行时工作区，每次会话可能被清空

这种设计与宿主系统区分 `system32/` 和 `home/` 的逻辑相同：通过物理隔离防止误操作。

### Principle 3: Session = WAL — 以 WAL 思维设计项目结构

参考三组件虚拟化架构（SKILL.md），**Session 是系统的唯一事实来源**：

- Session（追加式事件日志）→ 对应项目中的 `sessions/` 或 `logs/` 目录
- 事件不可变、可序列化（JSONL）、可回放
- 项目结构应当让 Session 数据与代码完全分离，确保"拷走 Session 日志 = 拷走所有运行状态"

将项目视为微型数据库：`src/` = 查询引擎，`config/` = 模式定义，`sessions/` = WAL 日志，`memory/` = 物化视图。

### Principle 4: 层级化配置覆盖 — 7 级优先级设计

配置加载必须遵循 7 级优先级链（从高到低）：

```
CLI参数 > Feature Flag > Policy规则 > Managed配置 > Local覆盖 > Project默认 > User全局
```

这意味着配置系统必须支持：
1. 多源加载（CLI args、env vars、YAML files、remote config）
2. 逐级合并（浅合并 + 深层合并选择策略）
3. 来源追踪（每个配置值记录来源，便于调试）

---

## Abstract Interface

### 配置文件 Schema（settings 接口规范）

配置文件必须暴露以下顶层命名空间，具体字段由 AI 根据规模和用途生成：

| 命名空间 | 来源 | 内容描述 | 格式 |
|----------|------|---------|------|
| `llm` | YAML | provider, model, temperature, max_tokens, timeout | map |
| `agent` | YAML | name, description, max_turns, system_prompt_path | map |
| `tools` | YAML | enabled 列表, disabled 列表, per-tool 超时配置 | map |
| `permissions` | YAML | default mode (allow/deny/ask), rules list | map |
| `sandbox` | YAML | enabled flag, allowed_paths, denied_patterns, isolation_level | map |
| `memory` | YAML | enabled flag, storage_backend, max_size, auto_compact | map |
| `logging` | YAML | level, format, output targets (file/stdout/otel) | map |

**字段设计原则**：
- 所有 API 密钥通过 `${ENV_VAR}` 占位符引用，绝不硬编码
- 每个字段必须有合理默认值，允许新用户仅配置 `llm.provider` 和 `llm.model` 即可启动
- 嵌套深度不超过 3 层，避免配置迷宫
- Minimal 规模可省略 `sandbox`、`memory` 命名空间

**⚠ AI构建提示**：阅读 technology-stack.md，根据用户选择的规模选择配置加载方案。Minimal 用 `python-dotenv` + 简单 YAML 读取；Professional 用 `pydantic-settings` (Python) 或 `zod` (Node.js) 进行 schema 验证；Enterprise 加 remote config 后端（etcd/consul）和配置热重载。生成具体的 `settings.yaml` 时，只包含用户所选规模需要的命名空间和字段。

### 环境变量 Schema（env 接口规范）

环境变量**仅用于两类场景**：
1. **Secret**：API 密钥、Token（绝对不能出现在 YAML 中）
2. **部署差异**：不同环境的端点 URL、日志级别

| 变量模式 | 类型 | 说明 |
|----------|------|------|
| `<PROVIDER>_API_KEY` | secret | LLM 供应商 API 密钥 |
| `<PROVIDER>_BASE_URL` | url | 自定义 API 端点（本地模型） |
| `LOG_LEVEL` | enum | 运行环境覆盖 |
| `ENV` | enum | `development` / `staging` / `production` |

**规则**：如果一个配置值在相同规模的所有部署中都相同，它属于 YAML。只有因部署环境而异的配置才属于环境变量。

**⚠ AI构建提示**：生成 `.env.example` 文件，包含所有 secret 占位符 + 部署差异化变量。每个占位符用 `your_xxx_here` 占位，并注释说明获取方式。Minimal 规模约 5-8 个变量，Professional 约 10-15 个，Enterprise 约 20-30 个（多供应商 + 监控 + 审计）。

### 目录接口规范（Directory Contract）

所有规模的目录结构必须遵循以下不变约束。**每个目录有明确的类型标签**：

| 目录 | 类型 | 生命周期 | 升级行为 | Git 跟踪 |
|------|------|---------|---------|----------|
| `src/` | 框架代码 | 跟随框架版本 | **覆盖替换** | 跟踪（可能 submodule） |
| `config/` | 用户配置 | 跟随项目演进 | **保持不变** | 跟踪 |
| `skills/` | 用户扩展 | 按需增删 | **保持不变** | 跟踪 |
| `workspace/` | 运行时 | 单次会话 | **会话结束清理** | 忽略 |
| `memory/` | 持久状态 | 长期累积 | **追加保留** | 忽略 |
| `sessions/` | WAL 日志 | 追加不删 | **追加保留** | 忽略（或归档） |
| `tests/` | 测试代码 | 跟随项目演进 | 框架版本增量合并 | 跟踪 |
| `scripts/` | 运维工具 | 按需增删 | **保持不变** | 跟踪 |

**⚠ AI构建提示**：根据用户选择的规模和技术栈，生成完整的目录树（包括所有必要的文件占位符）。参考 below 的三级结构描述，但需根据具体用途（编码助手 / 运维 / 数据分析）调整 `src/` 下的子模块划分。

---

## AI Build Prompts

以下每个提示对应一个产出物。AI 必须在生成代码前回答提示中的"设计问题"，然后根据答案和所选规模生成定制化代码。

### 提示 1: 目录结构生成

```
你需要为用户的 Agent 项目生成目录结构。

设计问题（在生成前回答）：
1. 技术栈是 Python / Node.js / Go？入口文件和包管理器不同
2. 构建规模是 Minimal / Professional / Enterprise？
3. 主要用途是编码助手 / 运维 / 数据分析？决定 `src/` 下需要哪些子模块
4. 是否需要沙箱？决定是否有 `sandbox/` 或 `sandbox-configs/` 目录
5. 是否需要多Agent？决定是否有 `agents/` 角色定义目录

生成要求：
- 必须标注每个目录的类型（框架代码 / 用户配置 / 运行时 / 持久状态）
- 必须生成 .gitignore，覆盖所有运行时和 Secret 目录
- Professional 和 Enterprise 规模必须包含 `docs/adr/`（架构决策记录）
- 目录深度不超过 4 层
```

### 提示 2: 配置文件生成

```
你需要为用户的 Agent 项目生成主配置文件。

设计问题：
1. 用户用哪个 LLM 供应商？决定 `llm` 命名空间字段
2. 规模是什么？决定加载方案（dotenv / pydantic-settings / remote config）
3. 是否需要沙箱？决定 `sandbox` 命名空间是否存在
4. 是否需要记忆？决定 `memory` 命名空间是否存在和字段复杂度

生成要求：
- API 密钥字段必须是 "${ENV_VAR}" 引用，不得出现明文
- 所有字段必须有注释说明其作用和有效值范围
- 按"核心 (llm/agent) → 功能 (tools/permissions) → 辅助 (memory/logging)"排序
- 困难的配置值（如 system_prompt）提供指向外部文件的路径引用
```

### 提示 3: README 生成

```
你需要生成项目的 README.md 文档。

设计问题：
1. 构建规模是什么？Minimal 只需安装+启动；Professional 需要配置说明+API文档链接；Enterprise 需要架构图+部署指南+监控配置
2. 技术栈是什么？决定安装命令（pip install / npm install / go mod）
3. 是否需要 Docker？决定是否有 Docker 启动方式章节

生成要求：
- 必须包含：项目简介、快速开始（安装+配置+启动，约5步以内）
- 各规模差异：
  - Minimal: 快速开始 + 一个示例
  - Professional: 快速开始 + 配置选项表 + 工具列表 + 架构概览链接
  - Enterprise: 以上全部 + 部署拓扑 + 监控指标说明 + 运维手册链接
- 禁止包含具体的 API 密钥值或示例密钥
```

### 提示 4: 依赖声明生成

```
你需要生成项目的依赖声明文件（pyproject.toml / package.json / go.mod）。

设计问题：
1. 技术栈和规模是什么？参考 references/11-technology-stack.md 选择对应级别的三方库
2. Minimal: 仅 SDK（如 anthropic）+ dotenv，共 1-3 个依赖
   Professional: SDK + pydantic-settings/zod + structlog/pino + httpx/axios + pyyaml + docker-py，共 5-8 个
   Enterprise: 以上 + opentelemetry + prometheus-client + fastapi/express + redis + sqlalchemy/prisma，共 10-15 个

生成要求：
- 版本号使用 caret/tilde 范围，不用固定版本
- 按类别分组注释（# LLM / # Config / # Observability）
- Node.js 项目需区分 dependencies 和 devDependencies
```

---

## Scale-Specific Guidance

### Minimal (~300-500 行总代码)

**目录特征**：
- 单入口文件或 `src/main.py` + `config/settings.yaml` + `.env.example`
- 不需要 `src/` 下的子目录分层，所有逻辑可放在 1-3 个文件中
- 不需要 `sessions/`、`memory/`、`sandbox/` 目录

**配置特征**：
- `python-dotenv` / `dotenv` 直读 `.env`
- YAML 文件可省略高级命名空间（sandbox, memory）
- 无 schema 验证，启动时做个基本 `assert` 检查即可

**依赖特征**：
- 仅 LLM SDK（如 `anthropic`）+ `python-dotenv` + `pyyaml`
- Python 用 `requirements.txt`（单文件，无需 pyproject.toml）

```bash
# Minimal 参考结构 (Python)
my-agent/
├── main.py                  # 入口 + Agent循环 + 工具（全部在此）
├── requirements.txt         # 2-4 个依赖
├── .env.example             # 5-8 个变量
├── config/
│   └── settings.yaml        # 仅 llm + agent + tools + logging
└── workspace/               # 运行时工作目录
```

**⚠ AI构建提示**：Minimal 规模的目标是"最快从 0 到运行"。生成 1 个可以 `python main.py` 直接启动的文件，不需要类继承体系，不需要工厂模式。所有逻辑可以是简单的函数组合。

### Professional (~2000-4000 行总代码)

**目录特征**：
- 标准 `src/` 分层：`agent/`, `tools/`, `llm/`, `permissions/`, `utils/`
- `config/` 包含 `settings.yaml`, `agents/` 角色定义，可选 `hooks/`
- `sessions/`, `memory/` 存在，使用文件系统存储
- `tests/` 目录必需，包含至少 smoke test
- `docs/` 包含 `architecture.md`

**配置特征**：
- `pydantic-settings` (Python) 或 `zod` (Node.js) 进行 schema 验证
- 配置加载失败时报错，明确列出缺失/无效字段
- YAML 支持环境变量引用和默认值回退

**依赖特征**：
- 5-8 个三方库，`pyproject.toml` 或 `package.json` 完整定义
- 按功能分组：LLM Clients, Config, Validation, Logging, Testing

```bash
# Professional 参考结构 (Python)
my-agent/
├── pyproject.toml
├── README.md
├── .env.example
├── .gitignore
├── src/
│   ├── main.py
│   ├── agent/               # Agent核心循环、状态机
│   ├── tools/               # 工具注册表 + 内置工具
│   ├── llm/                 # LLM抽象 + 供应商适配器
│   ├── permissions/         # 权限模型 + Hook系统
│   └── utils/               # 日志、错误定义
├── config/
│   ├── settings.yaml
│   ├── agents/              # Agent角色定义 (*.md)
│   └── hooks/               # Pre/post tool-use hooks
├── skills/                  # 用户自定义 Skill
├── sessions/                # Session WAL (JSONL)
├── memory/                  # 持久记忆
├── workspace/
├── tests/
├── docs/
│   ├── architecture.md
│   └── adr/                 # 架构决策记录
└── scripts/                 # 运维脚本
```

**⚠ AI构建提示**：Professional 规模的目标是"团队可维护的生产级项目"。需要生成：抽象基类（ABC）、接口定义、工厂模式。每个模块应有自己的 `__init__.py` 暴露公共 API。日志使用 `structlog` (Python) / `pino` (Node.js)。沙箱至少包含路径白名单检查。

### Enterprise (~6000-10000+ 行总代码)

**目录特征**：
- Monorepo 结构：`packages/core`, `packages/cli`, `packages/server`
- `config/` 支持多环境（`development.yaml`, `staging.yaml`, `production.yaml`）
- `sessions/` 和 `memory/` 使用外部存储（PostgreSQL / Redis），目录仅用于开发阶段
- `tests/` 包含 unit, integration, e2e, load 子目录
- `deploy/` 目录包含 Dockerfile, docker-compose, k8s manifests, terraform
- `docs/` 必须包含 `adr/` 决策记录、API 文档、部署指南、监控配置说明

**配置特征**：
- `pydantic-settings` + remote config backend（etcd / Consul / AWS Parameter Store）
- 7级层级化配置完全实现，配置来源追踪
- 配置热重载（SIGHUP 或 file watcher）
- 配置变更审计日志

**依赖特征**：
- 10+ 三方库，严格分组管理
- Server 模块：FastAPI / Express / Fiber
- Observability：OpenTelemetry SDK + Prometheus client + Grafana agents
- Database：SQLAlchemy / Prisma + Alembic / Prisma Migrate

```bash
# Enterprise 参考结构 (Python monorepo)
my-agent-platform/
├── pyproject.toml
├── README.md
├── .env.example
├── .gitignore
├── packages/
│   ├── core/                # 共享抽象和接口
│   ├── agent/               # Agent核心循环
│   ├── server/              # API服务（FastAPI）
│   ├── cli/                 # 交互式CLI（rich + typer）
│   └── observability/       # OpenTelemetry + Prometheus
├── config/
│   ├── development.yaml
│   ├── staging.yaml
│   └── production.yaml
├── deploy/
│   ├── docker-compose.yml
│   ├── k8s/
│   └── terraform/
├── skills/
├── sessions/                # 开发环境本地存储
├── memory/                  # 开发环境本地存储
├── workspace/
├── tests/                   # unit / integration / e2e / load
├── docs/
│   ├── architecture.md
│   ├── adr/
│   ├── api.md
│   └── deployment.md
└── scripts/
```

**⚠ AI构建提示**：Enterprise 规模的目标是"企业级平台"。需要生成：完整的项目分层（至少 3 个独立包/模块）、依赖注入（dependency_injector / tsyringe）、7 级配置覆盖框架、OpenTelemetry 探针配置、数据库迁移脚本。CLI 使用 `rich` (Python) / `ink` (Node.js) 提供交互式体验。配置管理参考 7 级优先级链，实现 source-tracked config loading。

---

## Checklist

### Minimal 规格
- [ ] 项目可以 `python main.py` / `node main.js` 直接启动（不需要安装额外工具）
- [ ] `.env.example` 包含所有必需的 secret 变量
- [ ] 配置文件不包含任何硬编码的 API 密钥
- [ ] `.gitignore` 排除了 `.env`, `workspace/`, `__pycache__` / `node_modules`
- [ ] README 包含：`安装依赖 → 配置环境变量 → 启动` 三步

### Professional 规格
- [ ] 所有 Minimal 检查项
- [ ] 目录结构区分 `src/`（框架代码）和 `config/`（用户配置）
- [ ] 配置文件加载时有 schema 验证，格式错误时给出明确报错
- [ ] `pyproject.toml` / `package.json` 包含完整的项目元数据（author, license, version）
- [ ] `tests/` 目录存在，至少有一个 smoke test 可以验证启动
- [ ] 日志系统（structlog / pino）已配置，输出包含时间戳和模块名
- [ ] `sessions/` 目录存在，Agent 运行后产生 JSONL 会话日志
- [ ] `docs/architecture.md` 描述系统组件和数据流

### Enterprise 规格
- [ ] 所有 Professional 检查项
- [ ] 多环境配置文件存在（development / staging / production）
- [ ] 配置加载支持至少 3 级优先级（env > local yaml > project yaml）
- [ ] OpenTelemetry tracer 和 meter 已初始化
- [ ] 健康检查端点存在（`/health` 或 CLI `--health-check`）
- [ ] `deploy/` 目录包含 Dockerfile 和 docker-compose.yml
- [ ] 数据库 migration 脚本存在（Alembic / Prisma Migrate）
- [ ] `docs/adr/` 包含至少 1 个架构决策记录
- [ ] 配置变更审计能力（记录每次配置读取的来源和时间）

---

## Common Pitfalls

### 陷阱 1: 目录没有"类型边界"

**症状**：框架代码和用户配置混在同一目录，用户不知道哪些文件可以修改，升级时误删用户数据。

**原因**：没有遵循 Architectural Constraints 原则。目录结构缺乏明确的"系统区"和"用户区"物理隔离。

**修复**：严格划分 `src/`（只读，升级覆盖）和 `config/`, `skills/`（用户域，永久保留）。在 `.gitignore` 和脚手架文档中明确标注。

### 陷阱 2: API Key 出现在 YAML 中

**症状**：新手为了方便把 `ANTHROPIC_API_KEY: "sk-ant-xxx"` 写在 settings.yaml 里，没改 `.gitignore`，然后提交到 Git。

**原因**：配置文件和环境变量的职责边界模糊。

**修复**：配置文件中的密钥字段必须使用 `${ENV_VAR}` 引用。生成 `.env.example` 模板时每个密钥占位符值设为 `your_xxx_key_here`。在 README 中明确警告。

### 陷阱 3: 跨规模的"一刀切"结构

**症状**：Professional 规模生成了 Enterprise 才需要的目录（如 `deploy/`, `packages/`），或 Minimal 规模生成了 Professional 的 `src/` 分层。

**原因**：AI 没有根据用户选择的规模裁剪目录树。生成了"最大实现"的项目骨架。

**修复**：在生成目录结构前，确认用户的规模选择。以该规模的最小可行目录集为基准，仅当用户明确需求时才扩展。

### 陷阱 4: 配置文件 Schema 过度设计

**症状**：Minimal 规模下使用 pydantic-settings 定义了 20 个配置字段，用户需要填 15 项才能启动。10 个字段从未被代码使用。

**原因**：复制了 Professional 或 Enterprise 的配置模板，没有精简。

**修复**：根据规模选择配置复杂度。Minimal 仅需 3-5 个必需字段（provider, model, api_key, max_turns），其他全部用合理默认值。代码中只声明会实际使用的字段。

### 陷阱 5: README 生成信息不足

**症状**：生成的 README 只有目录结构图，缺少"如何启动"、"需要配置什么"、"遇错怎么办"。

**原因**：README 被当作模板生成，而不是功能文档。AI 只填充了项目名和描述，没有填写实际使用信息。

**修复**：README 必须包含可验证的启动步骤（从 git clone 到首次运行）。每个步骤用代码块标注确切的命令。配置表格说明每个字段的作用和有效值。

### 陷阱 6: 忽略 .gitignore 覆盖运行时目录

**症状**：`workspace/`、`sessions/`、`memory/`、`.env` 被提交到 Git。项目仓库膨胀，或密钥泄露。

**原因**：目录生成时漏了 `.gitignore`，或 `.gitignore` 规则不完整。

**修复**：`.gitignore` 必须在所有三个规模的 checklist 中作为强制性验收项。规则必须覆盖：环境文件、运行时目录、IDE 配置、OS 垃圾文件、Python/Node 缓存。

---

## 下一步

完成 Phase 1 后，进入 **Phase 2: LLM 抽象层**（打开 `references/02-phase-llm.md`）。Phase 2 的 LLM 抽象层将使用本 Phase 中定义的配置接口来初始化客户端。