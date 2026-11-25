# 命令参考

所有命令都在 Skill 目录运行，或使用绝对脚本路径。公共路径参数：

```bash
--root "<WB_BUS_HOME>"
--ledger "<台账.md>"
--review-dir "<复盘目录>"
```

环境变量：`WB_BUS_HOME`、`WB_BUS_LEDGER`、`WB_BUS_REVIEW_DIR`。

## init

```bash
python3 scripts/wb_bus.py init
```

创建目录、台账头、当月复盘占位和 `bus.json`。重复执行不覆盖已有文件。

## status

```bash
python3 scripts/wb_bus.py status
```

输出 pending/claimed/completed/failed、WAITING_VERIFY、已验证/返工数量和最近任务。只读，不领取任务。

## dispatch

```bash
python3 scripts/wb_bus.py dispatch \
  --id WB-YYYYMMDD-NNN \
  --title "资料整理" \
  --goal "形成带来源和未知项的 Markdown 报告" \
  --workbuddy "检索并写报告" \
  --codex "核对实际来源和最终交付" \
  --input "<输入路径>" \
  --deliverable "<交付路径>" \
  --acceptance "每个事实有来源，未知项明确标注"
```

创建 `WB-*` 执行包，登记台账并放入 pending。重复编号会失败。

## verify：正向 WBV

```bash
python3 scripts/wb_bus.py verify \
  --id WBV-YYYYMMDD-NNN \
  --title "配置修改独立验收" \
  --goal "复跑测试并确认文件未被修改" \
  --changed-file "<改动文件>" \
  --cwd "<项目目录>" \
  --command "python3 -m pytest -q" \
  --evidence "Codex 已执行，EXIT=0，N passed" \
  --acceptance "测试全部通过" \
  --risk "不访问网络"
```

要求：

- `WBV-*` 编号。
- 至少一个 `--changed-file`，文件必须存在。
- 至少一个 `--command`，且不依赖 `rg`、`codex` 或交互式配置。
- `--evidence` 写真实自测结果；没有就写待补充，不伪造。
- 包内记录文件 SHA-256、cwd、命令和只读边界。

## verify：反向 WBC

```bash
python3 scripts/wb_bus.py verify \
  --id WBC-YYYYMMDD-NNN \
  --title "候选 Skill" \
  --candidate-dir "<隔离候选目录>"
```

候选目录必须已有 `验证请求.md`。命令把入口复制到 `待验证/`，状态改为 `WAITING_VERIFY`，不放入 WorkBuddy 执行队列。

## claim

```bash
python3 scripts/wb_bus.py claim --worker workbuddy
```

原子领取最早的 pending 任务并输出 JSON。任务包缺失时移入 failed；已有回执时仍移入 claimed 并返回 `RECEIPT_EXISTS`，随后可直接执行 `complete`。没有任务时输出 `EMPTY`。

## complete

正向任务或验收：

```bash
python3 scripts/wb_bus.py complete --id WBV-YYYYMMDD-NNN
```

- 回执路径来自领取记录；也可用 `--receipt "<文件>"` 覆盖。
- WBV 回执必须包含 `WB_PASS`、`WB_FAIL` 或 `WB_PARTIAL`。
- 完成后更新队列、台账和当月复盘。
- 结论为 `WB_FAIL` 仍然算验收已完成；Codex 修复后新建编号。

反向候选：

```bash
python3 scripts/wb_bus.py complete \
  --id WBC-YYYYMMDD-NNN \
  --result PASS \
  --evidence "Codex 实跑：python3 -m pytest -q，EXIT=0"
```

没有现成 `验证结果.md` 时，脚本使用模板生成。`PASS` 移动到 `已验证/`，`FAIL` 移动到 `返工/`。

## fail

```bash
python3 scripts/wb_bus.py fail --id WB-YYYYMMDD-NNN --error "<真实错误>"
```

只用于流程无法执行或领取项损坏，不用于“交付质量不合格”。质量结论应写回执并 `complete`。

## 人工启动语

```text
执行任务 `<编号>`。读取任务包 `<package_path>`，按其中的角色、命令、验收标准和数据边界完成；只写包内允许的产物，完成后写回执并调用 `complete`。发现问题如实写 FAIL/PARTIAL，不修复、不合并、不发布。
```

## 检查

```bash
python3 -m py_compile scripts/wb_bus.py scripts/self_test.py
python3 scripts/self_test.py
python3 <skill-publisher>/check_integration.py .
python3 <skill-creator>/quick_validate.py .
```

`quick_validate.py` 需要 PyYAML。环境缺少该依赖时记录为“未运行”，不得写成 PASS；同时必须保留已通过的 `check_integration.py` 结果。不要为绕过校验删除合法字段。
