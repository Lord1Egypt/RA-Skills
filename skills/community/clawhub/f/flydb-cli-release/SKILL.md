---
name: flydb-cli-release
description: >-
  使用和排查 Flydb CLI 发行包，包括安装、迁移预演与执行、本机 Web 工作台、JSON/Plan 输出、MCP 调用和 JDBC 驱动接入。用户提到 bin/flydb、flydb web、flydb.conf、flydb-cli ZIP、FLYDB 错误码、长迁移或失败恢复时使用。自带运行参考；迁移 SQL 编写与多环境流水线分别交给同族专门技能。
metadata:
  compatibility: Flydb CLI 0.3.x，Web 入口需 0.3.5+；Java 8+。MCP 宿主另需 Node.js 20+ 和兼容 Adapter；普通 CLI/Web 无需 Node.js。
---

# Flydb CLI 发布包使用

使用 Flydb 独立 CLI 发行包完成一次可追溯的数据库迁移操作。本技能自包含：命令、配置、错误码参考全部打包在 `references/` 内，复制到任何目录都可独立工作，不依赖 GitHub 文档链接或 Flydb 源码仓库。

本技能属于 Flydb 技能族（总入口为 `flydb` 技能）：写迁移脚本用 `flydb-migration-scripts`，多环境/CI 自动化用 `flydb-multi-environment`。

## 参考文档（按任务读取）

| 文件 | 何时读取 |
|---|---|
| [`references/release-package.md`](references/release-package.md) | 获取/安装发行包、Java 运行环境、配置文件查找顺序 |
| [`references/commands.md`](references/commands.md) | 选择子命令、核对全局选项与参数语义 |
| [`references/configuration.md`](references/configuration.md) | 配置键、环境变量、优先级、版本选择/路径过滤规则 |
| [`references/errors.md`](references/errors.md) | 按错误码（FLYDB-xxxx）与退出码分类处理失败 |
| [`references/drivers.md`](references/drivers.md) | JDBC 驱动解析顺序、厂商驱动接入、FLYDB-1003 排查 |
| [`references/jdbc-integration.md`](references/jdbc-integration.md) | 新数据库接入、驱动与方言区别、SPI JAR 与厂商验证边界 |
| [`references/web.md`](references/web.md) | 启动本机 GUI、管理原配置、查看进度和同机 CLI 记录 |
| [`references/web-api.md`](references/web-api.md) | 直接调用本机 API、配置冲突、确认引用、Run/SSE 状态 |
| [`references/json-output.md`](references/json-output.md) | CI/Agent 读取机器信封、protocolVersion、错误与状态 token |
| [`references/plan-artifact.md`](references/plan-artifact.md) | 核对 plan.id、计划内容摘要及其适用边界 |
| [`references/mcp-tools.md`](references/mcp-tools.md) | MCP 定位与握手、工具白名单、写入开关、超时与诊断 |

## 核心契约

1. **自包含与版本核验**：运行参考随技能打包；先运行目标 CLI 的 `version`，优先采用其发行包内匹配版本的文档，再使用本技能副本。参数差异用 `<命令> --help` 核对，机器 schema 用对应版本文档核对；缺少证据时报告差异，不猜测选项。外部链接用于追溯和扩展阅读，不是常规执行的前置条件。
2. **来源不等于发布**：同步版本、提交和文件哈希见 [`references/upstream-sync.json`](references/upstream-sync.json)。这是源码工作区快照，不证明该版本已公开发布；下载时另行核验实际 Release 资产。旧版本没有 Web 时说明需要 0.3.5+，不要直接套用新接口。
3. **写入需授权**：`migrate`、`baseline`、`repair`、`undo`、`clean` 都会改变数据库。本地/测试库的明确执行请求可作为授权，不重复询问；预发/生产库先展示 dry-run 清单和目标摘要，再取得针对该范围的写入授权。已有授权仅在目标或范围变化时重新核对。目标环境不明时停在只读检查。
4. **密码纪律**：优先 `FLYDB_PASSWORD` 环境变量、`${env:VAR}` 引用或密码文件；不把密码写进命令历史、日志、SQL 或最终汇报；输出中的 JDBC URL 一律脱敏。

## 工作流

### 1. 环境预检与获取发布包

先区分源码仓库、发行包和外部脚本仓库；脚本位于 Flyway 等项目不改变用户指定的 Flydb 执行入口。确认 Java 和 CLI：

```bash
java -version                       # 要求 ≥8；版本输出在 stderr
<发行包目录>/bin/flydb version      # 不连数据库，验证发行包与 Java 均就绪
```

发行包按三步获取（详见 [`references/release-package.md`](references/release-package.md)）：

1. 探测已有安装：先查用户给定路径、`FLYDB_HOME`、PATH 和项目工具目录，再按需搜索常见安装位置。
2. 复用本地 ZIP（如 `~/Downloads/flydb-cli-*.zip`），`unzip` 解压
3. 下载：GitHub URL 模式 `https://github.com/zzxCoding/Flydb/releases/download/v<version>/flydb-cli-<version>.zip`；国内网络 GitHub 不可达时用 Gitee 镜像同型 URL `https://gitee.com/zzhenxuan/Flydb/releases/download/v<version>/flydb-cli-<version>.zip`

Java 缺失时报告并停止（安装任意 JDK 8+ 并设置 `JAVA_HOME` 后重试）；发行包缺失且无法下载时如实报告，不要把源码目录当成已安装的 CLI。

### 2. 建立执行上下文

执行任何数据库命令前，明确并在回复中记录：

- 使用的 CLI 路径或发行包目录；
- `flydb.conf` 或 `--config` 来源；
- JDBC URL 的脱敏摘要、目标数据库与方言标识；
- 迁移脚本位置（通常是 `filesystem:db/migration`；脚本在外部仓库时记录解析后的绝对位置和当前工作目录）；
- 这是本地、测试、预发还是生产数据库；
- 用户要查看、校验、预演还是实际写入。

首次接入可用 `init` 生成 `flydb.conf` 与迁移目录（非交互加 `--yes`；已有文件冲突会报 `FLYDB-4004`，不要删除覆盖绕过）。

### 3. 选择命令

| 用户目标 | 命令 | 默认动作 |
|---|---|---|
| 创建配置和迁移目录 | `init` | 只生成本地文件，不连接数据库 |
| 本机图形化配置与执行进度 | `web` | 启动本机服务，启动本身不连接数据库 |
| 查看迁移状态 | `info` | 读取数据库和本地脚本，不持锁 |
| 校验 checksum、失败记录和迁移集合 | `validate` | 只读校验 |
| 预演迁移 | `--dry-run migrate` | 解析并打印 SQL，不执行 |
| 执行待迁移脚本 | `migrate` | 写入数据库并持锁 |
| 为存量库写入基线 | `baseline` | 写历史记录并持锁 |
| 清理失败记录或对齐 checksum | `repair` | 修改历史表并持锁 |
| 撤销最近一次版本化迁移 | `undo`（支持 `--dry-run`） | 执行 SQL 并持锁 |
| 清空目标 schema | `clean` | 高风险破坏性操作，默认禁用 |

选定命令后到 [`references/commands.md`](references/commands.md) 核对参数；不确定时用 `bin/flydb <命令> --help`。

程序消费使用 `--json`：stdout 单行信封，stderr 为日志与执行遥测；检查进程退出码、`protocolVersion`、`status` 和 `exitCode`，忽略未知新增字段。`web` 不接受 `--json`，`--help` 始终是文本，中断可能没有信封。

### 4. 执行

**只读任务**（`info`、`validate`、`version`）：执行后报告退出码和关键结果；不要把只读任务自行扩展为写库命令。

**迁移任务**：

1. 使用版本选择或路径过滤时，先读配置参考并列出预期集合；`target-version` 默认精确匹配，范围结束值不含该版本的子版本。显式版本选择排除 R 脚本，路径过滤还会改变 info/validate 等命令看到的集合。再运行 `validate`。
2. 再 `--dry-run migrate`，核对目标方言、待执行脚本、SQL 数量与顺序；任何未解释的缺失或多出脚本都应阻断实际写入。
3. 按核心契约第 3 条取得授权后执行 `migrate`。
4. 执行后用 `info --color=never` 与 `validate` 核对状态，报告是否产生失败记录。

迁移失败时读 [`references/errors.md`](references/errors.md) 和诊断通道的“迁移失败执行快照”，核对失败阶段、事务模式、JDBC 确认数、定位可信度及事务结果。确认执行不等于提交；仅明确“已回滚”时才能按整体回滚处理。非事务、提交未知、回滚失败先核验数据库现场，再决定脚本修正与历史修复；不自动重放或 `repair`。

**长迁移**：预计超过终端/SSH/工具存活时间时，先读 [长时间迁移与后台运行](references/commands.md#长时间迁移与后台运行)，用其包装器启动已授权迁移，保留工作目录及完全一致的配置、版本选择和过滤参数，记录运行目录、日志、PID 与原子 `exit-code` 文件。工具超时或无新日志时保持进程，做有界状态检查；终止进程需明确授权。进程结束且退出码可读后再核验，PID 消失但无完成标记是结果未知，不重跑。CI 保持前台执行并设置足够的 Job 超时。

### 5. Web 工作台与 MCP

**Web**：按 [`references/web.md`](references/web.md) 启动，仅报告普通 `127.0.0.1` 地址与进程状态。已有配置直接导入，新建复用 init 规则；表单和文件编辑作用于原文件，外部修改先合并修订。文件编辑可能显示原文凭据，不复制到对话或报告。启动 GUI、修改配置、打开浏览器均不扩大数据库写入授权。

预览后使用对应确认引用执行；配置、目标或脚本变化、`FLYDB-2011` 或确认过期均需重新预览。Web `planId` 是临时确认引用，CLI `plan.id` 是内容摘要，两者不能互换。HTTP 200 只代表操作已提交，继续观察 Run 终态及独立 verification；关闭浏览器不取消任务，无可信终态按 UNKNOWN 核验。Web 不提供 clean。

**MCP**：先读 [`references/mcp-tools.md`](references/mcp-tools.md)，检查 CLI 版本握手与宿主现有配置。数据库工具只接收绝对 `workingDirectory`、`configPath`；密码由宿主环境或密码文件注入，驱动提前准备（调用固定 `--driver-download never`）。默认仅有只读/计划工具；启用 `FLYDB_MCP_ENABLE_WRITES=true` 只是开放工具，不能替代本次写入授权。先 plan 核对 `plan.id`、SQL 与目标，再按授权调用写工具；不臆造 clean/init/execute_sql/rawArgs。

MCP 超时/取消会终止 CLI 子进程，与后台 CLI 分支不同；收到 `FLYDB_MCP-0002/0003` 后保留诊断并核验数据库，不能推断已回滚或自动重试。预计超出调用期限时先选择合适执行方式，不能静默更换用户指定的 MCP 入口。

### 6. 驱动与错误处理

- 驱动相关（`FLYDB-1003`）按 [`references/drivers.md`](references/drivers.md) 的解析轨迹排查。
- 连接失败（`FLYDB-1001`）先查 URL、账号、密码、网络与数据库状态，不要先改方言。
- 探测歧义（`FLYDB-1002`）显式 `--database-type`，不要把未识别数据库强标为 `mysql`/`oracle`。
- JDBC 驱动只负责连接，方言负责历史表、锁、事务、引号和语句切分。复用兼容家族前核对这些语义；专有差异按 JDBC 接入指南使用独立 SPI。报告时区分本地模拟、MySQL 冒烟与目标厂商实例验证。

## 边界情况

- **参考与实际不符**：以 `bin/flydb --help` 为准执行，并向用户报告差异（参考副本可能滞后于已安装的 CLI 版本）。
- **clean**：默认禁用。除非用户明确要求并完成目标确认，不得追加 `--clean-disabled=false --force`（`FLYDB-4003` 是防呆，不是故障）。
- **业务模板占位符**：`${workDate}` 等要原样入库的运行时模板报 `FLYDB-2009` 时，用 `--placeholder-replacement=false`，不要为模板变量随意赋值。
- **迁移目录切换**：新旧位置逗号并列，避免已应用记录变 `MISSING`（`FLYDB-2003`）。
- **不下载、提交或重新分发厂商 JDBC 驱动**；遵守厂商许可证与企业制品库规则。

## 汇报格式

完成后用简洁结构汇报：

1. **目标**：脱敏后的 CLI 路径、数据库/方言、环境和命令。
2. **动作**：实际执行的命令，是否包含 dry-run，是否写入数据库。
3. **结果**：退出码、预期与实际迁移集合核对、迁移数量/状态、失败记录或锁结果。
4. **验证**：`info`、`validate` 或 dry-run 分别验证了什么。
5. **后续**：只给与当前失败或用户目标直接相关的下一步。

## 项目来源

本技能族服务于开源项目 [Flydb](https://github.com/zzxCoding/Flydb)（Apache-2.0；国内镜像 [Gitee](https://gitee.com/zzhenxuan/Flydb)）。开源不易，欢迎 [Star](https://github.com/zzxCoding/Flydb) 支持与参与贡献。
