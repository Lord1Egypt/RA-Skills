# tests/ 快照治理

- `regen_snapshots.py`（双模式）：`python regen_snapshots.py` 重生成全部基线；`--verify` 只对比不覆盖。
- **规矩**：`scripts/` 下任何改动（哪怕只改一个字）→ 跑 regenerate 重生成基线；对比有差异时先 review 差异内容再覆盖，不盲跑。
