> 📢 公告  
来也 ADP 全球发票提取功能限时免费，名额有限，先到先得：[ADP 全球发票提取免费技能](../adp-global-invoice-extraction-free/SKILL.md)
---

# 🚀 来也 ADP 全球票据智能抽取 · 高速版
由来也科技 ADP 智能文档处理团队重磅出品，面向**全球跨境财务、自动化、系统集成、高并发生产**场景，提供低延迟、高吞吐、全版式、多语种的发票、账单、收据智能抽取能力。全面兼容结构化标准票据、非结构化海外采购发票、消费小票，不论是电子 PDF、扫描件、还是图片文件，均可以**单页最快5秒输出标准化 JSON 结构化数据**，支撑企业级批量处理与7×24小时稳定服务，彻底打通业务自动化、智能对账、数据入库全流程。

## ⭐ 高速版核心优势
⚡ 极速处理体验：单页最快5秒完成解析，支持大规模并发调用，满足生产环境高强度处理需求。  
✅ 企业级高吞吐架构，低延迟响应，大规模文件稳定处理。  
🌐 支持上百种语言：可识别英语、日语、韩语、德语、法语、泰语等主流语种的发票与收据。  
📄 全版式兼容：适配各国标准增值税发票、东南亚税务单据、非结构化收据及混合版式凭证。  
🎯 抽取准确率超99%：精准提取关键字段，大幅削减人工核验、翻译与数据录入成本。  
🤖 AI 持续优化：模型可基于业务数据迭代调优，识别效果持续提升，支持企业级个性化适配。  

## 📌 适用场景
| 用户群体 | 使用场景 |
| ---- | ---- |
| 企业财务/共享中心 | 大规模多语言票据批量处理，自动化入账、结算与对账。 |
| 系统集成厂商 | 支持最高10并发、低延迟文档解析接口集成，满足生产级SLA要求。 |
| 开发者/技术团队 | 接入高性能ADP API，快速构建稳定、高效的文档自动化处理流程。 |

## 安装

```bash
# npm（推荐）
npm install -g @laiye-adp/agentic-doc-parse-and-extract-cli

# Linux / macOS
curl -fsSL https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.sh | bash

# Windows（PowerShell）
irm https://raw.githubusercontent.com/laiye-ai/adp-cli/main/scripts/adp-init.ps1 | iex
```

或从 [GitHub Releases](https://github.com/laiye-ai/adp-cli/releases) 下载预编译二进制。

## 配置

访问 [https://adp.laiye.com/](https://adp.laiye.com/?utm_source=clawhub) 注册并获取 API Key（新用户每月 100 免费积分）。

```bash
adp config set --api-key <your-api-key>
adp config set --api-base-url https://adp.laiye.com
adp config get
```

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
| `--concurrency <n>` | 并发数（免费用户最大 1，付费用户最大 2） |
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
- **ADP 服务**：基于公有云的 AI 文档处理服务，按使用量计费，[计费规则](#credit)

免费额度：新用户注册后每月可获得 **100 免费积分**，可体验完整功能


## 📞 支持与联系
- **CLI 使用指南：** [ADP CLI 使用指南](https://laiye-tech.feishu.cn/wiki/Hz3Vw1IQki3YQtk33gLcSdwSndc)
- **API 接口文档：** [Open API 使用指南](https://laiye-tech.feishu.cn/wiki/PO9Jw4cH3iV2ThkMPW2c539pnkc)
- **ADP 产品操作手册：** [公有云操作手册](https://laiye-tech.feishu.cn/wiki/UDYIwG42pisBbFkJI39ctpeKnWh)
- **问题反馈：** [GitHub Issues](https://github.com/laiye-ai-repos/adp-skill/issues)
- **邮箱：** global_product@laiye.com
- **官网：** [来也科技 ADP](https://laiye.com/product/adp-platform)
