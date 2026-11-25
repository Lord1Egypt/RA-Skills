# 9 条自检覆盖表

`tests/run_golden.py` 里的每条用例都造一个临时包，真跑 `scripts/audit.py`，断言输出与退出码。

| 用例 | 断言什么 |
|---|---|
| G01 | 声明 2/2、实际 2/2 → OK，退出码 0 |
| G02 | 声明 2/2、实际 1/2 → MISMATCH，退出码 1 |
| G03 | 文件数 3 与实际 3 一致 → OK |
| G04 | 声明 9 个文件、实际 1 个 → MISMATCH |
| G05 | 列表项里的 `references/rules.md` 不存在 → MISMATCH |
| G06 | 正文举例里的路径 → 不产生 MISMATCH |
| G07 | 有声明无 runner → UNVERIFIABLE，退出码 0 |
| G08 | 同上但加 `--strict` → 退出码 1 |
| G09 | `list` 只列不跑；根目录不存在 → 退出码 2 |

## 为什么是这 9 条

覆盖三个结论（OK / MISMATCH / UNVERIFIABLE）与三个退出码（0 / 1 / 2），外加两条最容易误判的排除规则（G06 正文举例、G07 缺 runner）。改动 `audit.py` 后跑一次；再拿 `evidence-anchor` 与 `skill-improver` 两个真实包跑一次，确认假阳性为零。
