# Handoff 维护

日常接力见 `../PROTOCOL.md`；本页只用于安装接线、升级、旧入口块清理、旧部署清理和旧账本查询。
这些维护操作不控制任务能否继续，任务数据不需要迁移。旧入口块清理需要 Python 3，
旧部署清理还需要 Git，旧账本查询需要 Git 与 sh；日常记录不要求安装这些维护工具。

## 安装与接线

安装全局 Skill：

```sh
npx skills add SnowsonZ/agent-handoff-skill --skill handoff-installer --global
```

zcode 与 Kimi Code CLI 直接读取 `~/.agents/skills/`；Claude Code 通过
`~/.claude/skills/handoff-installer` 软链接到全局安装（`npx skills` 自动创建）。
Codex 的全局目录是 `~/.codex/skills/`，需要时补一条软链：

```sh
ln -s ~/.agents/skills/handoff-installer ~/.codex/skills/handoff-installer
```

规程只在用户明确请求（接手、保存交接、整理任务记录）时经 Skill 调用生效；存在任务数据不触发加载，
也不向业务仓库分发任何载荷。

## 旧入口块清理

0.4 及更早版本会在各客户端全局约束文件写入带 `handoff:global` 标记的入口块，新版本不再使用。
升级后检查并清理：

```sh
python3 "<skill-dir>/scripts/setup.py" status
python3 "<skill-dir>/scripts/setup.py" disable --agents codex claude
```

`disable` 需要对应请求；`status` 只读。二者定位以下文件（`CODEX_HOME`、`CLAUDE_CONFIG_DIR`、
`KIMI_CODE_HOME` 环境变量重定向均生效；codex 存在非空 `AGENTS.override.md` 时以该文件为准）：

| 客户端 | 文件 |
|---|---|
| codex | `~/.codex/AGENTS.md` |
| claude | `~/.claude/CLAUDE.md` |
| zcode | `~/.zcode/AGENTS.md` |
| kimi | `~/.kimi-code/AGENTS.md` |

`disable` 只剥离标记块并保留文件其余内容；剥离后为空的文件（如仅含入口块的 zcode/kimi 文件）会被删除。
`status` 全部 `clean` 时退出码为 0，报 `legacy` 表示仍有残留。维护请求不创建或接手任务。
跨客户端验证见 [compatibility.md](compatibility.md)。

## 旧部署清理

用户要求清理或迁移指定旧仓库时，先检查：

```sh
python3 "<skill-dir>/scripts/migrate.py" status [repo-root]
```

返回 `clean` 时无需操作；`legacy` 或新清理事务的 `interrupted` 可执行 `migrate [repo-root]`，
完成后确认 `clean`。只读请求只检查；`blocked` 或失败时报告具体原因并停止清理。
旧 `.agents/handoff.transaction` 必须由原版本恢复，不能自动调用旧安装器。

迁移只清理旧锁证明属于协议的文件及标记块，保留任务、归档、业务 CLAUDE 导入、其他业务规则和
Git 历史。无锁、本地修改或不明归属内容不删除。清理改动留给项目正常审阅提交。

可选开发协调器 `tools/upgrade-skill.py` 默认只更新全局 Skill，显式 `--repo` 才清理所选旧仓库。
不扫描其他仓库。`--copy-to` 可同步技能留存副本。

## 旧账本

新记录不使用 hop 或 commit trailer。需要查询旧任务账本时，在相应 Git 仓库执行：

```sh
sh "<skill-dir>/scripts/ledger.sh" <task-id>
```

该命令只读提交摘要，不自动读取历史正文。它是兼容查询工具，不是交接验收步骤。
