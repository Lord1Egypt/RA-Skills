# 脱敏公开样例

本目录来自 `tests/fixtures/sample_group.jsonl` 的启发式报告。

- **无真实用户私聊**
- **无本机绝对路径**
- 仅用于演示 4 块结构（硬事实 / 矛盾 / 原话墙 / 动作）

生成命令:

```bash
python3 scripts/run.py -i tests/fixtures/sample_group.jsonl --conv 1 --owner-alias '主理人小A' -o /tmp/cvi-ex
```

> 真人群报告默认禁止入库本目录；若要公开真实案例，必须人工脱敏并另开 PR。
