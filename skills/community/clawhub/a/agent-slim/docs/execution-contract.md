# 安全执行契约

版本：`schemaVersion=1.0`。所有新命令输出 JSON；默认 dry-run，只有 `--apply` 才改动。

## 命令

```sh
# 1. 只读审计
python3 scripts/agent_slim.py audit --json --output audit.json

# 2. 生成机器可读计划；未证明的项保持 pending-confirmation
python3 scripts/agent_slim.py plan --audit audit.json --output plan.json

# 3. 显式确认某目标（可重复）；目录前缀可确认其下文件
python3 scripts/agent_slim.py plan --audit audit.json \
  --confirm "sessions/2019/01/old.jsonl" \
  --confirm "skills/demo/references/rare.md" \
  --output plan.json

# 4. 默认 dry-run；显式 --apply 才事务化移动
python3 scripts/agent_slim.py apply --plan plan.json
python3 scripts/agent_slim.py apply --plan plan.json --apply --audit-log <audit.log>

# 5. 能力回归；test-prompts 缺省时为 PARTIAL，不伪造 PASS
python3 scripts/agent_slim.py verify --plan plan.json --test-prompts prompts.json

# 6. 默认 dry-run；显式 --apply 才恢复
python3 scripts/agent_slim.py restore --manifest <transaction>/manifest.json
python3 scripts/agent_slim.py restore --manifest <transaction>/manifest.json --apply
```

事务目录默认放在被审计 Home 的同级 `.agent-slim-transactions/<home-name>/`，避免恢复后向原 Home 留下事务文件。

## Plan

必需字段：

| 字段 | 含义 |
|---|---|
| `planId` / `createdAt` | 计划标识与生成时间 |
| `sourceAudit.sha256` | 输入 audit 文件 SHA-256 |
| `actions[]` | 每个动作的目标、原因、收益、风险、隔离路径与验证方法 |
| `actions[].status` | `ready` 或 `pending-confirmation` |
| `actions[].executable` | 是否进入 allowlist 执行器 |
| `expectedContextSavings` | Token 收益；未知或未实测时不得包装成已实现收益 |
| `expectedDiskSavings` | 磁盘净收益；移动不释放空间，首版固定为 0 |
| `preservedFiles[]` | 瘦身后必须保持 SHA-256 不变的文件 |
| `parseChecks[]` | JSON 或受限 YAML frontmatter 检查清单；不声明完整 YAML/TOML 解析能力 |
| `referenceGraph[]` | 来自 audit 的引用边快照 |

排序依次考虑：可执行优先、风险低优先、上下文估算收益、可恢复字节、目标路径。排序不是收益承诺。

## 首版可执行动作

| 动作 | 证据门槛 | 改动 |
|---|---|---|
| `quarantine-redundant-backup` | 至少两个备份 SHA-256 相同，保留一份 | 把其余副本移入事务隔离区 |
| `archive-verified-old-session` | `sessions/` 文件超过年龄阈值，调用方显式确认已关闭且已交接 | 移入事务归档区，不删除 |
| `quarantine-low-frequency-file` | Skill 文件未被正文引用，调用方显式确认低频 | 移入事务隔离区 |

`delete-original`、provider/认证/密钥修改、`base_url` 修改、系统配置、数据库 VACUUM 和云端外发均被阻断。

## Apply 与 Manifest

显式 `--apply` 的执行顺序：

1. 重验 plan 结构、目标范围、SHA-256、事务目录和隔离目标。
2. 在唯一事务目录写 `manifest.json` 与 `manifest.sha256`。
3. 写独立 `restore.py`、`restore.sh` 和恢复说明。
4. 移动文件并逐项复核 SHA-256。
5. 写 `result.json` 与审计日志。
6. 任一移动失败时，用同一 manifest 回滚已移动项。

目标或隔离目标已存在时停止，不静默覆盖。事务目录已存在时停止，不创建第二份不一致事务。

## Verify

检查项：

- 目标在 applied/restored 阶段的存在性与 SHA-256；
- 隔离副本 SHA-256；
- `preservedFiles[]` 保留清单；
- audit 引用边仍可解析；
- JSON 与受限 YAML frontmatter 可解析；
- 可选 `test-prompts` 命令回归。

`test-prompts` 格式：

```json
{
  "test_cases": [
    {
      "id": "trigger-positive",
      "prompt": "给这个 Agent 整体瘦身",
      "command": ["python3", "route_check.py"],
      "expect": {"exitCode": 0, "stdoutContains": "agent-slim"}
    }
  ]
}
```

命令通过环境变量 `AGENT_SLIM_PROMPT` 和 `AGENT_SLIM_CASE_ID` 接收输入，不经 shell。报告只保存 prompt 哈希，不保存 prompt 或命令输出正文。

缺少 `test-prompts` 时触发/路由检查为 `SKIPPED`，总体为 `PARTIAL`。受限 frontmatter 解析器只支持本项目使用的 YAML 子集，不声明完整 YAML 能力。

## Restore

- `restore` 默认 dry-run，只有 `--apply` 才移动。
- 先核对 `manifest.sha256`，再核对每个隔离副本 SHA-256。
- 原目标已有用户后改内容时停止，绝不覆盖。
- 第二次 restore 返回 `already-restored`，不重复移动。
- 生成的 `restore.py` 默认 dry-run；执行 `python3 restore.py --apply` 才恢复。

## 退出码

| 退出码 | 含义 |
| ---: | --- |
| `0` | 命令完成；verify 仅在完整 PASS 时返回 0 |
| `1` | verify FAIL |
| `2` | audit warning 门禁或 verify PARTIAL |
| `3` | 目标、事务或恢复冲突 |
| `4` | 事务失败或审计日志不可写 |
| `64` | 参数、plan schema 或动作白名单错误 |
| `74` | 输入 JSON、Home 或输出 IO 错误 |
