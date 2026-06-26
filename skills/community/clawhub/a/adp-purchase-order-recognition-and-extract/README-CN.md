## 🚀 关于来也ADP

ADP是来也科技公司**智能体文档处理产品 (Agentic Document Processing，简称 ADP)**， 基于大模型的通用理解能力，不依赖规则与标注，具备对多语言、多模态、多场景的通用理解能力；智能体的自主规划与执行，能够理解任务目标、自主规划步骤、调用工具、完成复杂任务；端到端的业务自动化，从文档输入到业务决策再到人机协同，形成完整闭环。

**agentic-doc-parse-and-extract** 是 ADP 官方开源 CLI 工具，同时支持人工终端调用 + AI Skill 自动调用。一条命令即可完成：文档结构化解析 + 关键字段智能抽取，覆盖发票、订单、证件、票据、通用文档全场景，输出标准 JSON，无缝对接自动化与 AI 流程。

---

## 💡 核心功能

agentic-doc-parse-and-extract 聚焦文档全流程智能处理，兼顾人工终端调用与 AI Agent 自动调用，核心功能覆盖解析、抽取、批量处理全场景，无需复杂配置，一条命令即可完成操作：

| 功能名称 | 功能描述 | 最佳场景 |
|---------|------------------|----------|
| **文档解析** | 自动识别 PDF、图片等多格式文档，将杂乱的非结构化内容（如扫描件、手写体、复杂排版文档）转化为标准化结构化数据，保留原始文档层级与关键关联关系 | 将非结构化文档转换为结构化数据，供 LLM 阅读和后续抽取使用 |
| **开箱即用文档抽取** | 基于 ADP 大模型原生 AI 能力，内置发票、收据、订单、中国地区常用证件等标准化抽取模型，无需配置规则、无需人工标注，一键提取各类通用单据关键字段，输出标准 JSON | 应付账款自动化、费用管理、采购自动化、卡证信息快速录入系统 |
| **自定义文档抽取** | 支持自主创建、编辑与管理个性化抽取应用，可针对企业专属单据、行业定制表单配置专属抽取字段与识别逻辑 | 企业专属单据、行业定制表单、非标准化文档的私有化抽取需求 |
| **任务查询** | 支持异步任务提交与状态查询，可快速查看任务执行进度、成功/失败状态，以及任务最终处理结果 | 批量任务处理、异步文档处理、问题排查与处理记录追溯 |
| **应用管理** | 提供完整的应用管理能力，可查看所有可用的抽取应用（系统内置 + 自定义）、查询应用详情、应用标签 | 多场景业务切换、应用全生命周期管控、自定义应用管理 |

## 安装
```bash
# 方法 1: npm（推荐，全平台通用）
npm install -g @laiye-adp/agentic-doc-parse-and-extract-cli
```

```bash
# 方法 2: Shell 脚本（Linux / macOS，无 npm 环境时使用）
curl -fsSL https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.sh | bash
```

```bash
# 方法 3: PowerShell 脚本（Windows，无 npm 环境时使用）
irm https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.ps1 | iex
```

或从 [GitHub Releases](https://github.com/laiye-ai/adp-cli/releases) 下载预编译二进制文件包。

## 配置
### 1. 访问 ADP 门户获取凭证
我们为国内和海外用户提供了独立的公有云访问地址，需按地区分别配置。就近访问可更好地保障高速稳定的网络调用。

| 地区 | 登录地址 | API Base URL |
|-----|----------|--------------|
| 中国大陆 | [https://adp.laiye.com/](https://adp.laiye.com/?utm_source=clawhub) | `https://adp.laiye.com/` |
| 海外地区 | [https://adp-global.laiye.com/](https://adp-global.laiye.com/?utm_source=clawhub) | `https://adp-global.laiye.com/` |

### 2. 注册/登录后获取 API Key
新用户需先注册 ADP 账号，注册后即可获得每月 100 免费积分。
- 登录后，点击个人头像，即可直接进入 `API_Key` 入口。

### 3. 完成认证配置
```bash
adp config set --api-key <your-api-key>
adp config set --api-base-url https://adp.laiye.com
```

### 4. 验证配置
```bash
adp config get
```

**注意事项**：
1. 如果 API Key 和 API Base URL 已配置完成，建议将配置信息存储到环境变量中，避免每次使用时重复配置。
2. 如果 API Key 和 API Base URL 尚未配置，请按照以上步骤完成配置。


## 快速示例

```bash
# 查看可用应用
adp app-id list

# 解析本地文档
adp parse local ./invoice.pdf --app-id <app-id>

# 抽取关键字段
adp extract local ./invoice.pdf --app-id <app-id>

# 异步解析目录
adp parse local ./documents/ --app-id <app-id> --async

# 处理远程 URL
adp extract url https://example.com/file.pdf --app-id <app-id>

# 查询异步任务
adp parse query <task-id>

# 两阶段异步（分开提交和查询，支持断点续传）
adp extract local ./documents/ --app-id <app-id> --async --no-wait --export tasks.json
adp extract query --watch --file tasks.json

# 失败自动重试（最多 2 次）
adp parse local ./documents/ --app-id <app-id> --retry 2

# 查看剩余积分
adp credit
```

## 命令

> AI Agent 应调用 `adp schema` 获取机器可读的权威命令规格。下表仅供人类速查。

| 命令 | 说明 |
|---|---|
| `adp version` | 显示版本号 |
| `adp config set` | 设置 API Key / 服务地址 |
| `adp config get` | 查看当前配置 |
| `adp config clear` | 清除配置 |
| `adp app-id list` | 列出可用应用 |
| `adp app-id cache` | 从本地缓存读取应用列表 |
| `adp parse local <path>` | 解析本地文件/目录 |
| `adp parse url <url>` | 解析远程文件（支持 URL 列表文件） |
| `adp parse base64 <data>` | 解析 Base64 编码内容 |
| `adp parse query <task-id...>` | 查询异步解析任务（支持多个 ID 或 `--file`） |
| `adp extract local <path>` | 抽取本地文件/目录 |
| `adp extract url <url>` | 抽取远程文件 |
| `adp extract base64 <data>` | 抽取 Base64 编码内容 |
| `adp extract query <task-id...>` | 查询异步抽取任务（支持多个 ID 或 `--file`） |
| `adp custom-app create` | 创建自定义抽取应用 |
| `adp custom-app update` | 更新自定义应用配置 |
| `adp custom-app get-config` | 查看应用配置 |
| `adp custom-app delete` | 删除自定义应用 |
| `adp custom-app delete-version` | 删除指定配置版本 |
| `adp custom-app ai-generate` | AI 推荐抽取字段 |
| `adp credit` | 查看剩余积分 |
| `adp schema` | 输出命令 Schema（供 AI Agent 使用） |

## 参数

| 参数 | 说明 |
|---|---|
| `--json` | 以 JSON 格式输出 |
| `--quiet` | 静默模式，仅输出结果 |
| `--lang <en\|zh>` | 指定界面语言 |
| `--app-id` | 应用 ID（parse / extract 必填） |
| `--async` | 异步模式 |
| `--no-wait` | 仅提交任务，不等待结果（与 `--async` 配合使用） |
| `--export <path>` | 导出结果到文件（单文件）或目录（批量） |
| `--timeout <seconds>` | 超时时间（默认 900 秒） |
| `--retry <n>` | 可重试错误的重试次数（默认 0） |
| `--file <path>` | 从 JSON 文件读取任务 ID（`--no-wait` 的输出文件，仅 query 可用） |

## 异步工作流

处理大文件或批量任务时，使用 `--async` 提交任务，CLI 返回 `task-id`，再用 `parse query` / `extract query` 轮询结果：

```bash
adp parse local ./big.pdf --app-id <app-id> --async
# 返回一个 task-id

adp parse query <task-id>
```

### 两阶段异步（`--no-wait`）

默认情况下，`--async` 会提交并轮询直到完成——适合 AI Agent 使用。对于可恢复的工作流，使用两阶段模式：

**第一阶段：提交任务**

```bash
adp extract local ./documents/ --app-id <app-id> --async --no-wait --export tasks.json
```

输出为包含任务 ID 的 JSON 数组：

```json
[
  {"path": "invoice.pdf", "task_id": "task_abc123"},
  {"path": "contract.pdf", "task_id": "task_def456"}
]
```

**第二阶段：查询结果**

```bash
adp extract query --watch --file tasks.json
adp extract query --watch --file tasks.json --export ./results/
```

即使 CLI 中途崩溃，`tasks.json` 中的任务 ID 也会被保留——随时可用 `query --file` 恢复查询。

## 批量处理

处理多个文件/URL 时，CLI 会将每个结果写入单独的文件：

```
adp_results_20250417_153020/
├── _summary.json              # 汇总（总数、成功、失败、每文件状态）
├── invoice_01.pdf.json        # 成功结果
├── contract_02.docx.json
└── report_03.pdf.error.json   # 错误详情
```

- `--export <dir>` — 指定输出目录
- 不加 `--export` — 自动创建 `adp_results_<timestamp>/`
- 单文件 — 输出到 stdout 或 `--export` 指定的文件路径

## 退出码

| 退出码 | 含义 |
|------|---------|
| `0` | 全部成功 |
| `1` | 全部失败 / 系统错误 |
| `2` | 参数错误 |
| `3` | 资源未找到 |
| `4` | 权限不足 |
| `5` | 冲突 |
| `6` | 部分失败（批量中部分任务失败） |

## 环境变量

| 变量 | 说明 |
|---|---|
| `ADP_API_KEY` | API Key（优先于配置文件） |
| `ADP_API_BASE_URL` | 服务地址 |
| `ADP_LANG` | 界面语言（`en` / `zh`） |
| `ADP_LOG_LEVEL` | 日志级别（`debug` / `info` / `warn` / `error`） |

## 配置存储

- 配置目录：`~/.adp/`
- 配置文件：`~/.adp/config.json`
- 加密的 API Key：`~/.adp/key.enc`（AES-256-GCM）
- 应用缓存：`~/.adp/app_cache.json`
- 版本检查缓存：`~/.adp/version_check.json`（每 24 小时刷新）

## 📜 授权许可

我们采用 开源工具 + 付费服务 的组合模式：CLI 工具完全免费开源，方便大家快速接入；而核心的 ADP 智能解析能力为公有云商业服务，按实际使用量计费，旨在为用户提供高精准、高稳定的文档处理体验。

- **CLI 工具**：MIT License 开源许可，可自由使用、修改和分发
- **ADP 服务**：基于公有云的 AI 文档处理服务，按使用量计费

免费额度：新用户注册后每月可获得 **100 免费积分**，可体验完整功能


## 📞 支持与联系
- **CLI 使用指南：** [ADP CLI 使用指南](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- **API 接口文档：** [Open API 使用指南](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)
- **ADP 产品操作手册：** [公有云操作手册](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh)
- **问题反馈：** [GitHub Issues](https://github.com/laiye-ai/adp-cli/issues)
- **邮箱：** global_product@laiye.com
- **官网：** [来也科技](https://laiye.com/product/adp-platform)

Copyright © 2026 [来也科技（北京）有限公司] 保留所有权利。
