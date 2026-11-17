# 使用说明

## 1. 前置条件

- Python 3.9 及以上，只使用标准库。
- 已知要审计的 Home。Codex 可用 `CODEX_HOME` 或 `--home`；其他 Agent 用 `--home` 指到它的配置根目录，认不出时用 `--layout` 描述（见第 3 节）。
- 先读 `docs/safety.md`，确认哪些内容允许移动、哪些只能人工复核。
- 所有命令默认只读或 dry-run；实际改动必须显式增加 `--apply`。

在项目根目录执行：

```sh
python3 scripts/agent_slim.py --version
```

## 2. 查看宿主能力：`host`

```sh
python3 scripts/agent_slim.py host --home <agent-home> [--layout layout.json] --output host.json
```

输出能力三态：

- `supported`：本机文件证据或实现路径已证明可用。
- `unknown`：目录、索引或测试命令缺失，不能据此执行破坏性动作。
- `unsupported`：本技能明确不实现，例如插件管理与插件停用。

该命令只探测本地元数据，不读取正文，也不在报告中输出 Home 绝对路径。

## 3. 让工具认识一个新 Agent：`layout.json`

内置分支认不出的 Agent，写一份布局描述即可，不需要改代码：

```json
{
  "host": "my-agent",
  "hot": [
    {"path": "config/rules.md", "category": "instructions", "loadedWhen": "every-turn"},
    {"path": "state/MEMORY.md", "category": "memory", "loadedWhen": "startup-memory-summary"}
  ],
  "skillRoots": ["skills"],
  "ruleRoots": ["rules"],
  "sessionRoots": ["state/sessions"],
  "logRoots": ["logs", "traces"],
  "backupRoots": ["backups"]
}
```

规则：

- 所有路径都是**相对审计根目录**的路径；绝对路径、`~` 开头和含 `..` 的条目会被拒绝并报 `LAYOUT_PATH_REJECTED`（退出码 64）。
- 只写确认存在的路径。漏写某一层只会让该层记 `unknown`，不会静默当成 0。
- 布局只改变"东西在哪"，不改变分层判定、动作白名单和验收门槛。
- 字段定义见 `schemas/layout.schema.json`；`host` 命令会回显声明内容，便于核对。

实测提醒：不声明 `hot` 时，常驻的记忆与身份文件若不在厂商默认路径里就完全不会入账。基线偏小会让后面所有百分比虚高。

## 4. 只读审计：`audit`

```sh
python3 scripts/agent_slim.py audit --home <agent-home> [--layout layout.json] --json --output audit.json
```

审计产出 Hot/Warm/Cold 分层、体积、近似 Token、引用图、插件只读清单、warning、unknown 和候选动作。会话、备份、日志和数据库只统计元数据，不读正文。

需要“有 warning 即非零退出”时增加 `--fail-on-warning`，此时返回码为 `2`。

## 5. 审阅并生成计划：`plan`

```sh
python3 scripts/agent_slim.py plan --audit audit.json --output plan.json
```

- 自动可执行的候选标为 `ready`；证据不足的项标为 `pending-confirmation`。
- 目标路径或目录前缀可用 `--confirm` 显式确认，参数可重复。
- 先人工审阅动作、原因、收益口径、风险、隔离路径和验证方法，再考虑 apply。
- `expectedDiskSavings` 不把“移动”包装成“已释放”；Cold 内容不产生 Token 收益。

事务根默认位于被审计 Home 同级的 `.agent-slim-transactions/<home-name>/`；也可用 `--state-root` 指向 Home 外目录。不要把事务根放进 Home 本身。

## 6. 预览执行：`apply` dry-run

```sh
python3 scripts/agent_slim.py apply --plan plan.json
```

不带 `--apply` 时只显示将移动的项目，不创建事务目录、不写审计日志，也不改变被审计 Home。先确认预览与计划一致。

## 7. 显式执行：`apply --apply`

```sh
python3 scripts/agent_slim.py apply --plan plan.json --apply --audit-log audit.log
```

执行前会重新核对计划、目标范围和 SHA-256；随后创建唯一事务目录，写入 `manifest.json`、`manifest.sha256`、`payload/`、`restore.py`、`restore.sh`、恢复说明和 `result.json`，再移动文件并逐项复核哈希。

只允许三种动作：

- `quarantine-redundant-backup`
- `archive-verified-old-session`
- `quarantine-low-frequency-file`

删除、密钥/provider 修改、数据库 VACUUM、系统配置修改和云端外发没有执行路径。

## 8. 验证：`verify`

```sh
python3 scripts/agent_slim.py verify --plan plan.json --phase applied
python3 scripts/agent_slim.py verify --plan plan.json --phase applied --test-prompts prompts.json
```

`verify` 检查目标状态与隔离副本 SHA-256、保留文件、引用完整性、JSON/受限 YAML frontmatter，以及可选的触发/路由回归。

`test-prompts` 由调用方提供可执行路由检查命令，命令通过 `AGENT_SLIM_PROMPT` 和 `AGENT_SLIM_CASE_ID` 接收输入，不经 shell。缺少 test-prompts 时触发检查为 `SKIPPED`，总体只能是 `PARTIAL`；不能把 fixture 路由结果或“看起来正常”写成真实宿主 PASS。

## 9. 恢复：`restore`

```sh
python3 scripts/agent_slim.py restore --manifest <transaction>/manifest.json
python3 scripts/agent_slim.py restore --manifest <transaction>/manifest.json --apply
```

- 默认 dry-run；`--apply` 才移动。
- 先验证 `manifest.sha256` 和每个隔离副本哈希。
- 恢复后路径、SHA-256、大小、mode、mtime 应与事务前一致。
- 第二次恢复返回 `already-restored`，不重复移动。
- 原目标已有用户后改内容时返回 `SOURCE_CONFLICT`，保留用户新内容与隔离副本，不覆盖。

也可运行事务目录内生成的 `python3 restore.py --apply` 或 `sh restore.sh --apply`。

## 10. 退出码

唯一事实源是 [安全执行契约](execution-contract.md) 的“退出码”一节；本节不再复制表格，避免两处漂移。速记：`0` 完成，`1` FAIL，`2` PARTIAL 或 warning 门禁，`3` 冲突，`4` 事务失败，`64` 参数或白名单错误，`74` 输入输出错误。

## 11. 冲突与安全处理

- 计划生成后目标文件被改动：`PLAN_STALE`，停止且不创建事务。
- 事务目录已存在：`TRANSACTION_EXISTS`，不复用、不覆盖。
- 恢复时原位置出现新内容：`SOURCE_CONFLICT`，停止并保留双方内容。
- 任一移动失败：用同一 manifest 回滚已移动项；回滚失败必须阻断并人工处理。
- 审计日志只记录动作、Home 相对路径、哈希和结果，不写文件正文、会话正文或秘密。

## 12. 结果如何判定

- `PASS`：目标状态、哈希、保留文件、引用、结构与调用方提供的回归全部通过。
- `FAIL`：关键检查失败；先恢复，再修复并重跑。
- `PARTIAL`：缺少 test-prompts，路由能力未实测；不能作为发布或“能力未回退”的完整证据。

## 13. 固定注入测量与发布闸门

0.2.0 新增一组只读命令，用于 Codex 固定注入测量和 Skill 发布前闸门。完整口径见 `docs/injection-measurement.md`。

```sh
python3 scripts/measure_prompt.py --gate 57344
python3 scripts/injection_state.py --check
python3 scripts/injection_state.py --record
python3 scripts/injection_state.py --check
python3 scripts/scan_layers.py --summary
python3 scripts/budget_dashboard.py --no-measure --out /tmp/budget.md
python3 scripts/mcp_probe.py --stdio --name svc -- <启动命令>
python3 scripts/token_experiment.py --help
python3 scripts/self_test.py
```

发布前必须全过：`description` ≤45 字、`SKILL.md` 目标 ≤8 KB、文本块闸门 PASS、状态机 `overall: OK`、`self_test.py` ALL PASS。`UNMEASURED` 和 `UNKNOWN` 不得写成 PASS。

这些命令不修改记忆、AGENTS、rules、插件缓存、MCP 配置、provider 或认证；`injection_state.py --record` 只更新状态文件，并在写前自动备份。
