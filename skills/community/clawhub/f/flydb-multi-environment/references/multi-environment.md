# 多数据库多环境自动化

> 本文件依据 Flydb `docs/getting-started/multi-environment.md`，结合当前命令、JSON、MCP 与 Web 契约手工维护，适配 CLI 0.3.x。完整参考在同级 `flydb-cli-release/references/`；独立安装时可读取目标发行包 `docs/`。源码同步工具不覆盖本文件。

组织模式为：**一个数据库×环境一份 `flydb.conf`，密码外部注入，所有环境执行同一套命令序列**。Web 中的 profile 是本机配置登记，不是 CLI 配置继承、远程平台或生产审批机制。

## 1. 总体模式

多环境自动化由三块现有能力拼出：

| 能力 | 作用 |
|---|---|
| `-c, --config <file>` | 为每个数据库×环境绑定一份独立配置 |
| `FLYDB_*` 环境变量 | 优先级高于 `flydb.conf`，用于注入密码等环境差异 |
| 稳定退出码 | CI 按校验失败、锁冲突、配置错误等类别分流处理 |

配置优先级统一为 `CLI 参数 > FLYDB_* 环境变量 > flydb.conf > 内置默认值`。

## 2. 配置组织：一个数据库×环境一份 flydb.conf

按 `<数据库>.<环境>` 命名，集中放在迁移仓库的 `deploy/` 目录并纳入版本控制：

```text
deploy/
├── flydb.mysql.uat.conf
├── flydb.mysql.prod.conf
├── flydb.dm.uat.conf
└── flydb.dm.prod.conf
```

示例（只放非敏感项，密码一律不进文件）——MySQL：

```properties
flydb.url=jdbc:mysql://db-uat.example.com:3306/app
flydb.user=flydb_ddl
flydb.database-type=mysql
flydb.locations=filesystem:/opt/deploy/migrations/mysql
```

达梦（`jdbc:dm://` URL，默认端口 5236，需显式指定方言 `dm`）：

```properties
flydb.url=jdbc:dm://db-uat.example.com:5236/demo
flydb.user=flydb_ddl
flydb.database-type=dm
flydb.locations=filesystem:/opt/deploy/migrations/dm
```

要点：

- **自动化中永远显式传 `-c/--config`。** 不传时 CLI 按"当前目录 `flydb.conf` → 安装目录 `conf/flydb.conf`"隐式查找，而 CI 和堡垒机的工作目录不可控，隐式查找是配置漂移的主要来源；隐式查找只适合本地交互使用。
- **`flydb.locations` 写绝对路径。** `filesystem:` 相对路径以执行 CLI 时的工作目录为基准；`init` 生成的配置同样使用绝对路径。
- **未知 `flydb.*` 键直接报 `FLYDB-4001`**，配置文件因此天然是一份可校验的环境清单：拼错键名会在流水线最早一步失败，而不是静默生效。
- SQL 占位符按环境差异化取值时，在各环境 conf 中写 `flydb.placeholders.<key>`，或由流水线统一用 `-D<key>=<value>` 传入；业务运行时模板要原样入库时设置 `flydb.placeholder-replacement=false`。
- 环境细节不能进版本库时，可退化为"一份 `flydb.conf` + 每环境一组 `FLYDB_URL`、`FLYDB_USER`、`FLYDB_LOCATIONS` 环境变量"；可评审性不如每环境一个文件。

## 3. 密码按环境分层注入

| 环境 | 推荐方式 | 说明 |
|---|---|---|
| 本地临时测试 | `flydb.password` 明文 | 仅限本地，不要提交 |
| 测试 / CI | `FLYDB_PASSWORD` 或 `flydb.password=${env:DB_PASSWORD}` | 由 CI secret 系统注入 |
| 生产 / 共享 | `flydb.password.file=/run/secrets/db_password` | 由 Vault、KMS 或部署系统落盘，收紧文件权限 |

- 自动化中不要使用 `-p/--password`：命令行参数会进入进程列表、shell history 和 CI 日志。
- 每个环境使用独立的专用 DDL 账号，迁移账号与业务账号分离；Spring Boot 应用用 `flydb.url/user/password` 做同样的隔离。

## 4. 脚本仓库：按数据库家族分目录

```text
migrations/
├── mysql/    V1__init.sql   V2__add_order.sql
├── dm/       V1__init.sql   V2__init_data.sql
└── oracle/   V1__init.sql
```

每个 conf 的 `flydb.locations` 指向自己家族的顶层目录。各数据库的版本流互相独立，历史表位于各自的目标库，天然隔离，这是推荐做法。

- 同一数据库内多个应用共用 schema 时，用 `flydb.table` 区分历史表。
- `directory-glob`/`path-glob` 等路径过滤也能在同一 locations 下切分子集，但过滤会影响 `info`、`validate`、`repair`、`undo` 看到的全部本地集合；能用分 locations 解决就不要用过滤。
- 调整脚本目录期间，把新旧 locations 逗号并列过渡，避免已应用记录变 `MISSING` 报 `FLYDB-2003`。

## 5. 流水线：所有环境同一套命令序列

拆成两个 CI job/stage，由平台真实审批门连接；注释本身不是门禁。两个阶段使用相同的绝对配置路径、工作目录、CLI、脚本与过滤/版本参数，密码由 CI secret 注入。以下示例需要 `jq`。

预检阶段（任一 CLI 非零退出立即阻断；把输出目录交给受控制品存储）：

```bash
set -eu
umask 077
CONF=/opt/deploy/deploy/flydb.dm.prod.conf
ARTIFACT_DIR=$(mktemp -d "${TMPDIR:-/tmp}/flydb-review.XXXXXXXX")
bin/flydb -c "$CONF" --json version > "$ARTIFACT_DIR/version.json" 2> "$ARTIFACT_DIR/version.log"
bin/flydb -c "$CONF" --json info > "$ARTIFACT_DIR/target.json" 2> "$ARTIFACT_DIR/info.log"
bin/flydb -c "$CONF" --json validate > "$ARTIFACT_DIR/validate.json" 2> "$ARTIFACT_DIR/validate.log"
bin/flydb -c "$CONF" --json --dry-run migrate > "$ARTIFACT_DIR/plan.json" 2> "$ARTIFACT_DIR/plan.log"
jq -e '.protocolVersion == 1 and .status == "success" and .exitCode == 0
  and .dryRun == true and .plan.algorithm == "flydb-plan-v1"' "$ARTIFACT_DIR/plan.json"
```

审批材料包括目标摘要、环境、版本、计划 SQL/顺序和 `plan.id`、配置及脚本产物身份。JSON 计划含业务 SQL；使用受控存储，不能默认作为公开制品。

执行阶段仅在对应环境审批通过后启动（CI 传入审批制品目录与相同配置）：

```bash
set -eu
: "${ARTIFACT_DIR:?CI 传入本次审批的制品目录}"
: "${CONF:?CI 传入已批准的绝对配置路径}"
bin/flydb -c "$CONF" --json --dry-run migrate > "$ARTIFACT_DIR/rechecked-plan.json" 2> "$ARTIFACT_DIR/rechecked-plan.log"
jq -e '.protocolVersion == 1 and .status == "success" and .exitCode == 0
  and .dryRun == true and .plan.algorithm == "flydb-plan-v1"' "$ARTIFACT_DIR/rechecked-plan.json"
approved_id=$(jq -er '.plan.id' "$ARTIFACT_DIR/plan.json")
current_id=$(jq -er '.plan.id' "$ARTIFACT_DIR/rechecked-plan.json")
[ "$approved_id" = "$current_id" ] || { echo "计划变化，返回预检与审批阶段" >&2; exit 2; }
bin/flydb -c "$CONF" --json migrate > "$ARTIFACT_DIR/migrate.json" 2> "$ARTIFACT_DIR/migrate.log"
bin/flydb -c "$CONF" --json info > "$ARTIFACT_DIR/after.json" 2> "$ARTIFACT_DIR/after.log"
bin/flydb -c "$CONF" --json validate > "$ARTIFACT_DIR/after-validate.json" 2> "$ARTIFACT_DIR/after-validate.log"
```

这只是外部流程核对：`plan.id` 不包含数据库目标，普通 CLI/MCP 写入没有批准摘要参数；核对与写入之间也不具备原子绑定。CI 还需固定并核对目标、配置、环境覆盖、脚本、驱动和回调，变化时回到预检。不能杜撰 `--plan-id`；Web 内部的锁内确认与临时 `planId` 也不能直接用于 CLI。

- **环境晋升就是换一个 `-c`。** 测试与生产使用同一份脚本产物、同一个发行包 ZIP，只替换 conf 路径。各环境统一锁定同一个 Flydb 版本，流水线开头的 `version` 即检查点；发行包自带版本匹配的 `docs/` 与 Skill。
- **退出码做门禁**：`2` 校验失败直接阻断，`3` 锁冲突可配置自动重试与告警（`flydb.lock-timeout-seconds` 按最长迁移时长设置），`4` 配置错误回退到配置阶段修复；`1` 为一般错误兜底（连接失败、SQL 执行失败、`FLYDB-20xx` 业务失败等），阻断并展示错误详情，按错误码参考细分处理。
- **机器结果**：stdout 为一行 JSON，stderr 单独记录；核对 protocolVersion/status/exitCode，忽略新增未知字段，退出码仍是第一层门禁。错误信封读取 error.code；中断或 Adapter 错误可能没有完整 CLI 信封。
- **迁移只能有一个执行者。** 要么 CI 统一执行 CLI，要么应用启动时由 Spring Boot starter 执行；两边都跑虽然会被迁移锁串行，但结果依赖时序。常见分工是测试环境用 starter 省事、生产走 CI 加审批，生产应用可用 `flydb.enabled=false` 关闭自动迁移。
- 远程库大批量数据迁移用 `--batch-size` 提速，MySQL 家族同时在 URL 上加 `rewriteBatchedStatements=true`。
- 可选：对生产定时执行只读 `validate`，checksum 不一致通常意味着有人绕过工具手工修改脚本，可作为漂移告警。
- **长迁移与未知结果**：CI 保持前台运行并设置大于预期时长的 Job 超时。执行遥测的 confirmed 不等于提交；超时、进程消失且无终态、提交未知先核验现场，不自动重试或 repair。终端/SSH 的 nohup 方案见 CLI 命令参考，不直接搬入 CI 掩盖退出状态。

## 6. 存量库先 baseline 再自动化

已有历史的生产库接入前，先人工对账已应用到的版本，写入基线后再交给流水线：

```bash
bin/flydb -c "$CONF" baseline --baseline-version 20260801
```

非空库首次接入也可以在 conf 中设置 `flydb.baseline-on-migrate=true`；两种方式都应先在测试环境演练。迁移失败留下的失败记录会阻断后续 `migrate`（`FLYDB-2004`）；不要在流水线里自动 `repair`——它修改历史表，必须先由人确认修复策略。

## 7. 驱动分发与离线执行机

- CI runner 与生产执行机的镜像中预置安装目录 `drivers/`，或把厂商驱动发布到企业私服，conf 写 `flydb.driver-coordinate` 并用 `--maven-settings` 指向私服 settings。
- 网络受限的生产执行机设置 `flydb.offline=true`，禁止一切远程驱动解析。
- 达梦、KingbaseES、openGauss 的驱动需写完整坐标；驱动解析不处理 Maven 传递依赖，需要伴随 JAR 的厂商驱动应把所有 JAR 一并放入 `drivers/`。CI 可缓存 `~/.flydb/drivers` 减少下载。
- 遵守厂商许可，不重新分发驱动 JAR。

## 8. 当前能力边界

- **MCP 已提供独立 Adapter**：宿主使用白名单 tools 消费 CLI 信封；写工具默认不注册，启用开关不提供逐次审批。调用超时会终止子进程，结果需核验；不用它承诺长任务自动恢复。
- **没有配置继承或模板**：多份 conf 之间的重复内容，可在流水线中用模板生成后作为制品管理，而不是等待工具内置 profile。
- **`undo` 只回退最近一次版本化迁移，`clean` 是破坏性操作**（默认禁用，非交互需双开关）：两者都不应出现在自动化脚本中，仅在本地排障时人工执行。
- **信创数据库的验证层级**：达梦、KingbaseES、openGauss 目前为方言与驱动元数据契约测试，接入生产前应先在授权实例完成最小验证清单（见 Flydb 仓库 JDBC 数据库快速接入指南），不要把单测通过当作厂商兼容证明。
