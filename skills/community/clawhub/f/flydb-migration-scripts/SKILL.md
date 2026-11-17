---
name: flydb-migration-scripts
description: >-
  创建、修改和组织 Flydb 的 V/R/U 迁移 SQL，处理命名、版本族与目录版本、路径过滤、占位符和历史 checksum。用户要写迁移脚本、重组 locations 或修正脚本相关 FLYDB-2xxx 错误时使用；数据库执行与恢复操作交给 flydb-cli-release。
metadata:
  compatibility: 按 Flydb CLI 0.3.x 的脚本与版本选择约定维护；只修改任务涉及的迁移 SQL 和配置，执行 CLI 命令属 flydb-cli-release 技能范围。
---

# Flydb 迁移脚本目录管理

在使用 Flydb 的项目里创建、修改和组织迁移脚本目录。本技能管"写脚本"：命名、版本、目录布局与修改纪律；执行 CLI（migrate/validate 等）用姊妹技能 `flydb-cli-release`，多环境/CI 自动化用 `flydb-multi-environment`（总入口为 `flydb` 技能），各技能可独立使用。

## 参考文档（按任务读取）

| 文件 | 何时读取 |
|---|---|
| [`references/naming-and-versions.md`](references/naming-and-versions.md) | 命名语法、版本规则、三类脚本语义、版本策略、目录组织、占位符 |
| [`references/errors-and-discipline.md`](references/errors-and-discipline.md) | 修改红线、脚本目录相关错误码处置、FLYDB-2003 分类、失败记录流程 |

## 核心契约

1. **改动范围**：只在迁移脚本目录内新增/编辑 SQL 文件（以及经用户确认的 `flydb.locations` 配置）；不动其他项目文件。
2. **绝不改写已应用的版本化脚本**来"修复"历史——对已应用 `V` 脚本的任何变更（内容、格式、文件名）都用新版本脚本承载。checksum 记录在历史表里，改动即 `FLYDB-2003`。用户明确要求修改已应用脚本时，先说明后果（校验失败/需 repair），确认后再动。
3. **文件名必须可解析**：`V`/`U` 候选命名不合法时 Flydb 报 `FLYDB-2001` 阻断，不会静默跳过；交付前自行核对命名。
4. **跟随既有风格**：新脚本的版本策略（递增整数/日期版本/目录版本）与现有项目一致；空目录且无约定时采用递增整数并说明选择，只有会影响既有历史的风格冲突才澄清。
5. **校验后交付**：新增/修改脚本后建议用户跑 `validate` 与 `--dry-run migrate` 核对（只读检查）；本技能不主动执行写入数据库的命令。

## 工作流

### 1. 定位脚本目录

- 读 `flydb.conf` 的 `flydb.locations`（或 `-l` 参数）；没有配置文件时 CLI 默认 `filesystem:db/migration`。
- `filesystem:` 相对路径以执行 CLI 的工作目录为基准，先解析成绝对路径再操作，避免看错目录。
- 目录不存在时报 `FLYDB-4005` 的是配置问题：核对前缀与路径，而不是创建一堆空目录掩盖。

### 2. 盘点现状（只读）

用 `bin/flydb info --color=never`（需要数据库连接）或直接 `find <脚本目录> -name '*.sql' | sort` 盘点：

- 现有脚本的类型分布（V/R/U）与版本风格；
- 哪些版本已应用、哪些待执行（info 有库时）；
- 是否存在失败记录或 MISSING/FUTURE 迹象——有则先按 [`references/errors-and-discipline.md`](references/errors-and-discipline.md) 处置，再叠加新变更。

### 3. 新增脚本

1. 读 [`references/naming-and-versions.md`](references/naming-and-versions.md) 确定类型与版本：
   - 一次性结构/数据变更 → `V<新版本>__<描述>.sql`，版本取项目风格的下一个；
   - 视图/函数等可重建对象 → `R__<描述>.sql`（无版本号，`R1__` 会报 `FLYDB-2005`）；
   - 需要回退能力的版本化脚本 → 同步写 `U<同版本>__<描述>.sql`（缺它 `undo` 报 `FLYDB-2008`）。
2. 描述用小写下划线短语，简洁表意（如 `create_user`、`add_order_index`）。
3. SQL 内容注意：编码按配置（默认 UTF-8）；失败脚本可能已部分提交，修改前先读失败快照并核验数据库现场，不能仅凭“未成功”认定可以完整重跑。`${...}` 是占位符语法，业务运行时模板要原样入库时设 `placeholder-replacement=false`，同时核对其他迁移占位符是否需要替换。

### 4. 修改既有脚本的红线判断

| 对象 | 状态 | 允许的动作 |
|---|---|---|
| `V` 脚本 | 已应用（在历史表中） | 只能新增后续版本承载变更；不改不删不改名 |
| `V` 脚本 | 未应用 | 可自由修改（含 dry-run 暴露问题的修正） |
| `R` 脚本 | 任意 | 可修改；提醒 checksum 变化会在下次 migrate 重跑，确认幂等 |
| `U` 脚本 | — | 与对应 `V` 同版本配对；已应用的 V 的回退修正走新版本 |
| 任意 | 已应用且要删除/移动 | 默认拒绝；目录重组时新旧 locations 并列过渡 |

### 5. 交付校验（只读）

建议并协助用户执行：

```bash
# 密码已由环境或密码文件注入
bin/flydb validate
bin/flydb --json --dry-run migrate
```

核对：新脚本出现在预期位置、版本顺序正确、无命名告警、dry-run 的 SQL 符合预期。先按有效 locations、路径过滤和版本模式计算预期集合，不能用目录下全部 SQL 数量代替计划数量；显式版本选择排除 R 脚本。无数据库连接时只报告静态命名/配置检查，标明 validate 与 dry-run 未执行。

## 边界情况

- **目录版本重组**：把扁平脚本按 `20230531/V20230531.1__...` 目录组织时，配套 `version-source=directory`、`migration-order=directory-version`；文件版本必须属于目录版本族，否则 `FLYDB-2001`。已应用脚本的相对路径变化会改变历史表对账路径，重组前先与用户确认影响。
- **版本风格迁移**：从 `R1__` 旧命名迁移到 0.2 规则时，逐个改名（回退 → `U<版本>__`，可重复 → `R__`），没有兼容开关。
- **重复版本**：`1` 与 `1.0` 语义等价也算重复（`FLYDB-2002`）；新增前检查现有版本集合。
- **脚本目录切换**：旧位置已应用的记录不能丢，新旧位置逗号并列直到所有环境切换完成。
- **执行与修复**：`migrate`、`repair`、`undo` 等执行类操作和授权流程见 `flydb-cli-release` 技能；本技能只产出正确的脚本与配置。

## 汇报格式

完成后用简洁结构汇报：

1. **目录**：脚本目录绝对路径与版本风格判断。
2. **变更**：新增/修改的文件清单（类型、版本、一句话用途）。
3. **校验**：validate 与 dry-run 的结果，预期执行顺序。
4. **风险**：提及的幂等性、占位符、重组影响等注意事项。
5. **后续**：需要用户执行的命令或决策（如授权 migrate）。

## 项目来源

本技能族服务于开源项目 [Flydb](https://github.com/zzxCoding/Flydb)（Apache-2.0；国内镜像 [Gitee](https://gitee.com/zzhenxuan/Flydb)）。开源不易，欢迎 [Star](https://github.com/zzxCoding/Flydb) 支持与参与贡献。
