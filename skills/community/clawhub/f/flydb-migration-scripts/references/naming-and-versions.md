# 迁移脚本命名与版本规则

> 本文件随 `flydb-migration-scripts` 打包，按 Flydb CLI 0.3.x 的命令与配置参考整理；与目标版本不一致时核对该发行包文档和 `--help`，并报告差异。

## 目录与发现

- 迁移位置由 `flydb.locations`（CLI 选项 `-l, --locations`）决定，CLI 默认 `filesystem:db/migration`；逗号分隔多个位置。
- 每个位置**递归扫描所有子目录**；历史表中的 `script` 字段记录相对位置路径，例如 `tenant/a/V2__tenant.sql`。
- `filesystem:` 相对路径以执行 CLI 时的当前工作目录为基准；`flydb init` 生成的配置写入绝对路径避免漂移，手工配置相对路径时需保持固定 CWD。
- SQL 文件编码由 `flydb.encoding` 控制，默认 UTF-8。

## 文件命名

```text
V1__create_user.sql        版本化迁移
V20260327-b06.4__data.sql  含字母/连字符 token 的版本化迁移
R__refresh_user_view.sql   可重复迁移（无版本）
U1__create_user.sql        撤销 V1 的回退脚本
```

语法为 `<前缀><版本>__<描述>.<后缀>`：`V`/`U` 带版本号，`R` 不带。前缀、分隔符、后缀均可配置：

| 配置键 | 默认值 | 含义 |
|---|---|---|
| `flydb.sql-migration-prefix` | `V` | 版本化脚本前缀 |
| `flydb.repeatable-migration-prefix` | `R` | 可重复脚本前缀 |
| `flydb.undo-migration-prefix` | `U` | 撤销脚本前缀 |
| `flydb.sql-migration-separator` | `__` | 版本与描述分隔符 |
| `flydb.sql-migration-suffix` | `.sql` | 脚本后缀 |

## 版本语法与排序

- 版本必须以**数字开头**，可包含字母数字 token，用点、下划线或连字符分隔，例如 `1.2`、`20260327-b06.4`。
- 数字 token 按数值排序，字母 token 按不区分大小写的字典序排序。
- 语义等价的版本（如 `1` 与 `1.0`）按**重复版本**阻断（`FLYDB-2002`）。
- 以 `V`/`U` 开头且以 `.sql` 结尾、但无法解析为版本化迁移的候选文件会报 `FLYDB-2001`，**不会静默跳过**。注意 `clean`、`baseline` 不解析本地迁移集合，非法文件名不阻断它们；其余命令都会。

## 三类脚本的语义

| 类型 | 执行时机 | 修改的后果 |
|---|---|---|
| `V<版本>__` | 每个版本只执行一次，按版本顺序 | 已应用后再修改 → checksum 不一致（`FLYDB-2003`），变更必须用新版本承载 |
| `R__`（无版本） | 每次 migrate 时若 checksum 与上次不同则重新执行，按描述排序在版本化迁移之后 | 修改即重跑；修改前确认脚本幂等/可重建 |
| `U<版本>__` | `undo` 命令撤销最近一次版本化迁移时执行 | 与 `V<版本>__` 配对；最近版本缺对应 U 脚本报 `FLYDB-2008` |

0.2 起 `R` 不带版本号：扫描到 `R1__...sql` 会报 `FLYDB-2005` 并阻断，没有兼容开关。旧式 `R<version>__` 回退脚本改名为 `U<version>__...sql`，可重复脚本改为 `R__...sql`。

## 版本策略选择

新增脚本时跟随项目既有风格；从零开始时可参考：

- **递增整数**（`1`、`2`、`3`…）：小型项目、线性演进，简单直接。
- **日期/复合版本**（`20260327`、`20260327-b06.4`）：按发布日组织，适合定期发布；token 语法同上。
- **目录版本模式**：`flydb.version-source=directory` 时版本从相对父目录提取，一个精确目录版本会一次选择该目录下的多个文件版本：

```text
db/migration/20230531/
├── V20230531.1__schema.sql
├── V20230531.2__data.sql
└── V20230531.3__index.sql
```

配合 `flydb.target-version=20230531` 与 `flydb.migration-order=directory-version` 使用。规则：

- 默认目录提取器寻找离文件最近的纯数字或点分数字目录；自定义目录名（如 `release-20230531`）用 `flydb.directory-version-regex` 提取（`version` 命名组或第一个捕获组）。
- 选择目录版本或 `directory-version` 排序时，每个版本化文件都必须能提取目录版本，且**文件版本必须属于该目录版本族**；不一致报 `FLYDB-2001`，不会静默排序。

## 子目录组织与路径过滤

- 子目录按租户/模块/环境组织均可（递归扫描），历史表以相对路径记账，路径即身份的一部分。
- `--directory-glob/--file-glob/--path-glob` 与对应 regex 可缩小发现范围；同一维度 glob 与 regex 互斥，不同维度取交集；匹配对象是 location 下以 `/` 分隔的相对路径。
- 路径过滤影响所有读取本地迁移的命令，包括 info、validate、repair、undo；版本选择只影响 migrate 和其 dry-run。先核对完整历史可见性，不能靠过滤隐藏失败或 MISSING。

## 版本选择与预期集合

| 模式 | 输入 | 含义 |
|---|---|---|
| `exact` | `target-version` | 精确一个文件版本；不会自动执行此前所有版本 |
| `range` | `start-version` / `end-version` 至少一个 | 含边界的版本范围；结束 `20260625` 不含 `20260625.3` |
| `family` | `target-version` | 目标及其 token 子版本，`202305310.1` 不属于 `20230531` |
| `family-range` | 起止边界至少一个 | 包含结束版本族的子版本 |
| `regex` | `version-regex` | 规范化版本文本整串匹配 |

省略模式时有 target 推断为 exact，有起止边界推断为 range；均无则不筛选版本。`version-source=directory` 改为比较目录版本，因此 exact 也可选中同目录版本下多个文件版本。显式选择版本时不执行 R 脚本，不绕过 checksum、失败记录或 out-of-order。

用有效 locations → 路径过滤 → 版本选择与历史状态 → 排序得到预期清单，再与 dry-run 逐项核对；不能只统计递归发现的 `.sql` 文件数。

## 占位符

- 默认 `flydb.placeholder-replacement=true`：脚本中的 `${key}` 在词法解析前替换，未定义报 `FLYDB-2009`。
- `${workDate}`、`${taskDate}` 等业务运行时模板必须原样入库时，设置 `flydb.placeholder-replacement=false`；该开关同时作用于真实迁移和 dry-run。
