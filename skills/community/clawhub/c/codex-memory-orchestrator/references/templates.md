# 恢复包模板

## 模板说明

当用户说“总结 / 压缩 / 恢复 / 交接 / 开新对话”，或对话累计轮数达 8 轮（或提前 1 轮已提醒，或单轮内容极大）时，按下面模板生成恢复包。目标：新对话只读此文件即可 5 行以内接续。

## recovery-package.md

```markdown
# 恢复包：<主题>

- 会话日期：YYYY-MM-DD
- 最近一次更新：YYYY-MM-DD HH:mm
- 状态：进行中 / 待核对 / 已完成

## 1 目标
一句话说明本次任务目标。

## 2 已完成
- 关键成果 1（含文件路径）
- 关键成果 2

## 3 关键决策与依据
| 决策 | 依据 | 状态 |
|---|---|---|
| xxx | 用户要求/规范/经验 | 已定/待确认 |

## 4 下一步（可执行）
- [ ] 具体动作 1（命令或文件路径）
- [ ] 具体动作 2

## 5 未决 / 风险
- 需用户确认事项
- 环境或数据风险

## 6 交接
- 交接对象：新对话 / 用户
- 验证方式：读恢复包后向用户复述 5 行摘要
```

## 跨对话框轮数监测

```sh
python3 <CODEX_HOME>/skills/memory-orchestrator/scripts/monitor_dialogs.py --days 14 --write-state
# 输出：扫描文件数、⏳ 接近阈值列表、🔴 已超阈值列表
# 对每个已超阈值对话框，按下方恢复包模板单独生成恢复包并提醒开新对话
```

## ctxcompress 使用

```sh
# 0) 先确认 active_project（state.py get），只导出该项目的会话目录/文件
export ACT="<项目标识>"   # 与 state.py 的 active_project 一致，须先征得用户同意
# 1) 项目限定导出（含 --project 校验，不使用全目录 **/*.jsonl 通配）
mkdir -p "${TMPDIR:-/tmp}/memorch-$$" && export OUT="${TMPDIR:-/tmp}/memorch-$$/chat.json"
python3 <CODEX_HOME>/skills/memory-orchestrator/scripts/export_ctx.py --project "$ACT" -i "$HOME/.codex/sessions/**/rollout-*.jsonl" -o "$OUT"
# 2) 压缩
<CTXCOMPRESS_PATH> --input "$OUT" --ratio 0.3 --format compact --output "$(dirname "$OUT")/compact.txt"
# 3) 用后立即清理临时原始压缩文件
rm -f "$OUT" "$(dirname "$OUT")/compact.txt" && rmdir "$(dirname "$OUT")" 2>/dev/null || true
```

ctxcompress 不可用时，手写 5-8 行摘要，包含：目标、已完成、关键决策、下一步、未决；同样只针对 active_project。

## create_thread 提示词（recovery_prompt.py）

```sh
# 已有恢复包时，把它变成新 Codex 对话的首条 user 消息（create_thread prompt）
python3 <CODEX_HOME>/skills/memory-orchestrator/scripts/recovery_prompt.py \
  --recovery-path <恢复包.md> --project <项目> --thread-id <原对话框ID> [--json]
```
`--json` 输出 `{prompt, recovery_path, project, thread_id}` 便于程序调用；输出可直接作为
本 app `create_thread` / `fork_thread` 的首条 user 消息。

## 不可写降级

state.json / recovery-index.md 主路径（`$CODEX_HOME/memory/`）不可写时，自动写入
`$TMPDIR/memory-orchestrator/`，可用 `CODEX_MEMORY_STATE_FALLBACK` / `RECOVERY_INDEX_FALLBACK` 覆盖；
输出 JSON 的 `storage.mode` 为 `primary` 或 `fallback`，`storage.path` 为实际落盘位置。

## hot.md 最低降级格式

```markdown
# 最近进行中任务

- 主题：
- 目标：
- 已完成（最近）：
- 下一步：
- 未决：
- 时间：
```

新对话优先读 cp-memory；读不到再读 hot.md。
