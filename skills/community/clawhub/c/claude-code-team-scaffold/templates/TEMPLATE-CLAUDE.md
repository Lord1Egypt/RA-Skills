# {{PROJECT_NAME}} — Project Guidelines

> 根目录 CLAUDE.md — 全局规则，适用于所有模块。Claude Code 自动加载本文件到上下文。
> 子模块细节见各目录下的 `CLAUDE.md`。

## 项目概述

{{PROJECT_DESCRIPTION}}

## 架构

{{ARCHITECTURE_DESCRIPTION}}

### 模块划分

<!-- 列出本项目的主要模块、目录、职责 -->
<!-- 例：src/api/ — REST 端点层；src/services/ — 业务逻辑层；src/models/ — 数据模型层 -->

## 安全合规

- 禁止硬编码敏感信息（密码、密钥、token、连接串）— 用环境变量
- 日志脱敏：用户邮箱、手机号、密码、身份证字段不写日志
- 所有外部输入必须校验（pydantic / zod / validator）
- `.env` 不入库（确认 `.gitignore` 已加）
- SQL 用参数化查询，禁止字符串拼接
- 文件上传/下载校验类型与大小

## 配置管理

- 配置从环境变量读取，禁止硬编码
- 12-factor：一份代码库、多份配置（dev/staging/prod 通过环境变量区分）
{{ADDITIONAL_CONFIG_NOTES}}

## 代码质量

- **类型安全**：Python 用 type hints；TypeScript 严禁 `any`
- **异步**：所有 I/O 操作 async/await
- **错误处理**：捕获后必须处理（重试 / 上报 / 降级），禁止静默 `except: pass`
- **结构化日志**：禁止 `print` 调试；用 `logger.info(...)` 等结构化 API
- **代码简洁性**：DRY 但不过度抽象；一个函数一个职责
- **依赖管理**：第三方库用项目包管理工具（pip / npm / go mod / cargo），禁止手动下载 jar/wheel

## 数据库

{{DB_NOTES}}

### 表前缀

{{TABLE_PREFIX — 如 custom_xxx_}}

### 数据隔离

- 多租户数据按 `tenant_id` 隔离，所有查询必须带 `tenant_id` 过滤
- 软删除：核心业务表用 `deleted_at` 而非物理删除

### 迁移

- 所有 schema 变更走迁移工具（alembic / flyway / migrate 等）
- 迁移脚本提交到代码库，与代码同步部署
- 破坏性变更先写双写方案

## 测试策略

| 模式 | 适用场景 | 工具 |
|------|----------|------|
| TDD | 纯逻辑、算法、边界条件多 | pytest / vitest |
| 边写边测 | REST 端点、Service 层、业务流程 | pytest / vitest + http test client |
| 实现后补 | AI 输出、UI 交互、临时脚本 | manual / e2e |

### 覆盖率目标

- 核心业务逻辑：≥ 80%
- 工具/帮助函数：≥ 60%
- 集成测试：覆盖所有 REST 端点（happy path + 关键 error path）

## Agent 分配规则

| 任务类型 | 分配 Agent |
|----------|-----------|
{{AGENT_ASSIGNMENT_TABLE}}

## Subagent 执行约定

1. **执行前**：读取目标模块的 `CLAUDE.md`（门控要求）
2. **执行中**：遵守本文件的"安全合规"与"代码质量"要求
3. **联合开发**：涉及多个模块时，读取各模块 `CLAUDE.md`，确保接口兼容
4. **自动分发**：根据任务类型，通过 `Task` 工具分发给对应 subagent
5. **跨模块感知**：识别所有受影响模块，分别调度对应 subagent
6. **CLAUDE.md 同步**：代码改动后必须同步更新涉及模块的 `CLAUDE.md`（Stop hook 会检查）

## 模块 CLAUDE.md 规则

- 每个模块开发前**必须**先创建该模块的 `CLAUDE.md`
- 必须包含：模块功能、技术栈、接口定义、数据模型、注意事项
- 功能变更后**同步更新**（硬约束：Stop hook 会检查）
- 模板见：`{{MODULE_CLAUDE_MD_TEMPLATE_PATH}}`

## 构建与运行

{{BUILD_RUN_COMMANDS}}

### 常用命令

```bash
# 安装依赖
{{INSTALL_CMD}}

# 启动开发服务器
{{DEV_CMD}}

# 运行测试
{{TEST_CMD}}

# 代码检查
{{LINT_CMD}}

# 类型检查
{{TYPE_CHECK_CMD}}
```

## CI/CD

{{CI_CD_DESCRIPTION}}

## 文档

- `docs/` — 项目文档
- `.spec-flow/active/{{PROJECT_SLUG}}/` — 当前迭代的需求/设计/任务
- `AGENTS.md` / `CLAUDE.md` — AI agent 规则（本文件 + 各模块）

## 紧急联系 / 升级路径

<!-- 列出关键人员 / 升级路径 / 值班安排 -->

---

**最后更新**：{{LAST_UPDATED_DATE}}
**维护者**：{{MAINTAINER}}
