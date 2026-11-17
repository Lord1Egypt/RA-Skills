---
name: gate-switch
description: "Claim-verification gate engine for LLM agent workflows. Whenever an agent claims 'X is done / written / synced / verified', write X as a spec JSON of mechanical checks; the engine verifies each check and returns a verdict (A=pass / B=block with violations / CLARIFY / VIOLATION). Cures three chronic LLM failures: skipped work, partial delivery, fabricated claims. 声称 X 已满足，就机械核验 X——判定禁止手写，照抄输出。"
---

# gate-switch — Claim-Verification Gate Engine / 声称即核验门禁引擎

**English**: LLM agents routinely claim "tests passed" / "file written" / "synced" without actually doing it. gate-switch takes the verdict out of the model's hands: you declare *what must be true* as a spec JSON (file exists, min size, JSON field value, glob count, grep count, mtime freshness, script exit code), and the engine mechanically checks every item. All pass → verdict **A** (proceed). Any failure → verdict **B** with a violation list that doubles as the fix instruction. Every flip is logged to an append-only JSONL ledger for later audit.

**中文**：治 LLM 三类顽疾——该做的没做、缺斤短两、伪造声称。把"声称 X 已满足"写成检查项 spec JSON，引擎逐项机械核验：全过→判 A 放行；任一失败→判 B 阻断并列出违例（violations 即修复指令）。判定权收归机械门禁，模型只能照抄结论。全程留痕 `~/.agents/logs/gate_switch.jsonl`，供复盘审计。

## Install / 安装

```bash
cp -R gate-switch ~/.agents/skills/   # Kimi Code skills directory / 技能目录
```

Zero dependencies (pure Python stdlib). / 零依赖（纯 Python 标准库）。

## Usage / 用法

```bash
python3 ~/.agents/skills/gate-switch/scripts/gate_switch.py --spec <spec.json> [--set key=value ...]
```

Exit codes / 退出码：`0`=A all checks passed / 全部通过放行 · `2`=B violations block / 有违例阻断 · `3`=CLARIFY insufficient input / 信号不足 · `4`=VIOLATION illegal spec / spec 非法。

## Bundled specs / 自带两个通用 spec

- **`zero_residual`** — prove a pattern is *gone*: rename cleanups, rollback residue, forbidden `>/dev/null` silencers. 零残留核验（改名/回滚/禁令兜底）。
- **`no_abs_path`** — zero hardcoded `/Users/*` absolute paths in living code. 活体代码零绝对路径硬编码。

```bash
python3 ~/.agents/skills/gate-switch/scripts/gate_switch.py \
  --spec ~/.agents/skills/gate-switch/scripts/specs/zero_residual.json \
  --set "pattern=<正则>" --set "path=<目标glob>"

python3 ~/.agents/skills/gate-switch/scripts/gate_switch.py \
  --spec ~/.agents/skills/gate-switch/scripts/specs/no_abs_path.json \
  --set src=<项目根>
```

## spec format / spec 格式

```json
{
  "gate": "gate-name",
  "desc": "what A/B mean / A/B 语义",
  "checks": [
    {"type": "file_exists",   "path": "...", "label": "..."},
    {"type": "file_min_size", "path": "...", "bytes": 100},
    {"type": "json_field",    "path": "...", "field": "a.b.0.c", "op": "exists|not_empty|equals|in|min_len|min|max", "value": 0},
    {"type": "glob_count",    "pattern": "...", "op": "min|max|eq", "value": 1},
    {"type": "grep_count",    "pattern": "...", "path": "...", "op": "min|max|eq", "value": 1},
    {"type": "mtime_after",   "path": "...", "ref_path": "..."},
    {"type": "script_exit",   "cmd": "...", "expect": 0}
  ]
}
```

`{key}` placeholders are injected via `--set key=value`. New scenario = new spec; the engine never changes. / `{key}` 占位符由 `--set` 注入；新场景 = 写新 spec，引擎零改动。

`templates/` contains reusable gate-skeleton templates (L3 framework gate / CLAIM-GATE). / `templates/` 附两个可克隆的闸骨架模板。

License: MIT-0 (attribution optional). / 许可证：MIT-0（署名可选）。
