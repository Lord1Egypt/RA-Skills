# AI Data Delivery · 0.3.10

**把表结构变成可追溯的语义模型，让接手的 Agent 离线读取定义和原文依据。**

[English](README.md) · [发布记录](https://github.com/franklinxkk/ai-data-delivery/releases) · [安全说明](SECURITY.zh-CN.md)

## 导入结构，读取第一份模型

解压 ZIP，进入含有 `requirements.txt` 和 `scripts/` 的目录，使用 Python 3.10 或更高版本。Windows 可将 `python` 换成 `py -3` 或虚拟环境内的 Python。首次使用先安装指定版本的依赖。

```bash
python -m pip install -r requirements.txt
```

要检查安装，可运行 `python scripts/smoke.py`。它在临时目录内导入合成表，并读取导出的包。要保留一份可编辑的模型，请运行下面的命令。

以下示例使用新的项目目录。第一条命令将随包合成 SQL 作为文本解析并保存结构草稿。第二条导出 ZIP，第三条用独立进程读取该包。全程可在本机运行，无需服务或模型密钥。

```bash
python -X utf8 scripts/knowledge.py --project "./work/transport" --language zh import --file "examples/semantic-workbench/transport.sql" --seed-draft
python -X utf8 scripts/knowledge.py --project "./work/transport" export --out "./work/transport.zip" --draft
python -X utf8 scripts/semantic_read.py --package "./work/transport.zip" verify
```

导入回执的 `result.result.seeded.counts` 为 `{"dataset": 2, "field": 5, "relation": 1}`，对应两张表、五个字段和一条外键。读取器返回的部分字段如下。

```json
{"status": "verified", "draft": true, "asset_count": 8, "complete": false}
```

包通过了完整性校验，八项定义均为草稿。要查看车辆表，可在包中搜索。

```bash
python -X utf8 scripts/semantic_read.py --package "./work/transport.zip" search --query vehicle --kind dataset
```

样例返回一个匹配项。取 `matches[0].asset.id`，用 `sources --id ID` 读取原始 `CREATE TABLE vehicle` 片段，可以核实 `vehicle.company_id` 引用 `company.id`。车辆归属和维护责任还需要各自的业务依据。换用自己的 DDL 时，请替换文件路径，并搜索实际表名。[离线读取与分页](references/agent-reader.md)

## 从字段引用追到业务责任

可以问 Agent：“哪家企业负责车辆维护？请给出依据原文。”在**同一项目**中导入随包合成业务说明。

```bash
python -X utf8 scripts/knowledge.py --project "./work/transport" import --file "examples/semantic-workbench/transport-v1.txt"
```

取回执中的 `result.result.batch_id`，让 Agent 用 `task --batch 批次ID` 读取“企业负责本企业车辆维护。”这段原文。将该引文及来源修订附在业务关系上，再核对依赖。获得确认授权前保留草稿。原先导出的 ZIP 仍对应旧修订，交付新模型时应使用新文件名。[建模与按范围导出](references/modeling.md)

需要看图时，运行 `python -X utf8 scripts/start.py --project "./work/transport" --language zh`，打开终端打印的本机网址。点表查看字段，点**新建对象**补充业务对象。选择**连线**后依次点两端，保存前核对箭头方向。选择 **3D 关系图**可查看改动涉及的对象。用 **Ctrl+C** 停止服务。需要离线图时，运行 `python scripts/knowledge.py --project "./work/transport" --language zh graph-view --out 变更.html`，分享前核对所含引文。

## 常见问题

| 遇到的情况 | 处理办法 |
| --- | --- |
| 内网机器无法联网安装 | 在联网且操作系统、架构和 Python 版本一致的机器执行 `python -m pip download --only-binary=:all: -r requirements.txt -d wheels`。将下载的 wheels 带入目标环境，再执行 `python -m pip install --no-index --find-links ./wheels -r requirements.txt`。 |
| 建模 CLI 返回 `argument_error` | 全局选项 `--project`、`--language zh`、`--revision`、`--progress` 放在子命令前面。`--file`、`--seed-draft`、`--out` 放在各自的子命令后面。`--progress` 在标准错误显示阶段，标准输出仍是一份 JSON 回执。 |
| 已有项目，或源表结构更新了 | 用原目录重开。再次导入时省略 `--seed-draft` 并核对变化。定期导出的 DDL 可从首次导入起复用固定 `--source-key`，已登记来源可用 `--source-id` 更新。GBK 文件使用 `import --encoding gb18030 --file 文件`。 |
| 写入结果未知，或遇到修订冲突 | 需支持重试的写入先指定唯一全局 `--operation-id`。中断后在同一项目运行 `receipt 操作ID` 查回执。遇到 `status: conflict` 时，用 `state --summary` 看修订号，再用 `state` 读取受影响对象，比较并合并当前输入，携带核对过的修订号重试。 |
| 导出失败 | 选择已有目录中的新文件名。若返回 `details.code: NOT_PUBLISHABLE`，按所列问题核对相应定义与依赖。接手方需要草稿时使用 `--draft`。 |
| 收到的包查不到词或 ID | 无匹配时，从 `fallback.candidates` 查看当前范围内的用词。遇到 `error.code: UNKNOWN_ID` 时，重新搜索本次快照，使用匹配项返回的实际 ID。 |

## 其他入口

| 目标 | 使用入口 |
| --- | --- |
| 源表很少声明外键，想找可能的连接 | `knowledge.py --project DIR relation-hints` 列出字段组合和元数据线索，保存关系前核对业务依据。 |
| 读取指定 SQLite、PostgreSQL、MySQL 表的结构 | [只读目录接入](references/readonly-metadata.md) |
| 交接某个问题或核对变更影响 | [问题交付与影响检查](references/question-delivery.md) |
| 与 Neo4j 或 ontology-graph-spec 交换模型 | [离线交换](references/neo4j-interop.md) |

宿主 Agent 解读材料，本工具在本机保存模型与依据。生产查询、企业权限和多人管理需由相应系统承担。已有项目升级前请保留备份。分发包内可打开 `LICENSE.md` 阅读 MIT 许可证。[架构](references/architecture.md) · [源码许可证](https://github.com/franklinxkk/ai-data-delivery/blob/main/LICENSE) · [Skill 指令](SKILL.zh-CN.md) · [改动历史](CHANGELOG.md)
