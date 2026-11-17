# Test fixtures / 测试夹具

> **⚠️ 这些 fixture 是刻意构造的模拟样本 / These fixtures are synthetic by design.**
> `repro/scan.py` 里的 `SECRET_PATTERNS` **不是真凭据**——只是「`sk-…` / `ghp_…` 形状」的
> **正则 pattern 字符串**，里面**没有任何真实 token 或密钥**（free of any real credential）。
> 它之所以被保留，是为了复现「名字命中 CodeQL 名字启发式」这一最小误报，供教学与可复现验证使用，
> 不涉及任何真实凭据的读取或流转。

> These files are **measured artifacts with local paths sanitized**, not hand-written examples.
> The two `.sarif` files were produced by the commands below; absolute paths in their
> `extensions[].locations[].uri` fields were replaced with the neutral placeholder
> `file:///path/to/.codeql/packages/…` so that no machine-specific path is published. Nothing else
> was altered.
>
> 这些文件是**实测产物（本地绝对路径已脱敏）**，不是手写的示例。两份 `.sarif` 由下面的命令真实生成，
> 仅把 `extensions[].locations[].uri` 里的绝对路径替换为中性占位符 `file:///path/to/.codeql/packages/…`，
> 以免发布任何与本机相关的路径。除此之外未作改动。

> **Language / 语言**：本文档为双语，仅为可读性；工具运行时的输出语言由用户通过 `--lang` 控制（默认英文，详见 README「Language selection」）。
> This document is bilingual for readability only; the tool's runtime output language is user-controlled via `--lang` (default English — see README "Language selection").

## `repro/` and `repro_fixed/` / 最小复现与对照

A pair of minimal reproductions, 25 lines each / 一对最小复现，各 25 行：

```python
SECRET_PATTERNS     = ["sk-[A-Za-z0-9]{20,}", "ghp_[A-Za-z0-9]{36}"]   # repro/        -> error
CREDENTIAL_PATTERNS = ["sk-[A-Za-z0-9]{20,}", "ghp_[A-Za-z0-9]{36}"]   # repro_fixed/  -> clean
```

**The two files are byte-identical apart from that variable name** (`tests/run_tests.py` has an
assertion guarding this: replacing the name globally in `repro` must yield exactly `repro_fixed`).
Neither file **contains any credential** — only pattern strings. All it does is
"match text → write JSON".

**两份文件除这个变量名外逐字节相同**（`tests/run_tests.py` 里有一项断言守着：
把 `repro` 里的这个名字全局替换掉后必须与 `repro_fixed` 完全相等）。
两份都**不含任何凭据**——只有模式字符串，逻辑是「匹配文本 → 写 JSON」。

### Why it fires / 为什么会触发

CodeQL picks its source through the **name heuristic**, not the content:

CodeQL 的 source 走**名字启发式**，不看内容：

```text
shared/concepts/codeql/concepts/internal/SensitiveDataHeuristics.qll
  maybeSecret() = (?is).*((?<!is|is_)secret|(?<!un|un_|is|is_)trusted(?!_iter)|confidential).*
```

`SECRET_PATTERNS` matches, so "the list assigned to it" becomes the source; the taint then propagates
through the loop variable → `dict` → `json.dumps(...)` and lands on `Path.write_text` (the sink).
Rename it to `CREDENTIAL_PATTERNS` and the name stops matching, so the whole path disappears.

`SECRET_PATTERNS` 命中，于是「赋值给它的那个列表」成为 source；
taint 沿循环变量 → `dict` → `json.dumps(...)` 传播，最后落到 `Path.write_text`（sink）。
换成 `CREDENTIAL_PATTERNS` 后名字不再命中，整条路径消失。

See [`../../references/sensitive-data-heuristics.md`](../../references/sensitive-data-heuristics.md).
详见该速查表。

## `sarif/`

For each of the two directories above: one database build, one run of the same query, giving the
**real SARIF**.

对上面两个目录各建库、跑同一条查询得到的**真实 SARIF**：

| File / 文件 | Query / 查询 | Results / 结果数 |
| --- | --- | --- |
| `repro.sarif` | `codeql/python-queries:Security/CWE-312/CleartextStorage.ql` | 1 |
| `repro_fixed.sarif` | same / 同上 | 0 |

Generated with / 生成环境：CodeQL CLI **2.27.1** / `codeql/python-queries` **1.8.11**。

Because these files are checked in, `tests/run_tests.py` and CI can verify `read_sarif.py`'s behaviour
**without installing CodeQL** (including parsing the source line out of `codeFlows` and the flow's
end point).

因为有这两份文件，`tests/run_tests.py` 和 CI **不需要安装 CodeQL** 就能验证 `read_sarif.py` 的行为
（含 `codeFlows` 里 source 行与流终点的解析）。

> ⚠️ If you change the number of lines in `repro/scan.py`, the line numbers inside these two SARIF
> files become stale (and the tests go red). Regenerate them as shown below.
>
> ⚠️ 若你改动了 `repro/scan.py` 的行数，这两份 SARIF 里的行号就失效了（测试会红）。重新生成即可，见下。

## Regenerating / 重新生成

```bash
# Requires an installed CodeQL CLI / 需要已安装 CodeQL CLI
python scripts/bisect_taint.py \
    --source scan.py \
    --tree tests/fixtures/repro \
    --workdir /tmp/taint_bisect \
    --variant t2_rename=SECRET_PATTERNS:CREDENTIAL_PATTERNS \
    --codeql /path/to/codeql

cp /tmp/taint_bisect/t1_control.sarif   tests/fixtures/sarif/repro.sarif
cp /tmp/taint_bisect/t2_rename.sarif    tests/fixtures/sarif/repro_fixed.sarif
python tests/run_tests.py

# Then re-sanitize the local absolute paths before committing / 提交前记得再脱敏一次本地绝对路径：
#   <your-codeql-home>/.codeql  ->  path/to/.codeql
```

As a side effect this command also verifies `bisect_taint.py` itself: `t1_control` must report 1
result, `t2_rename` must report 0, and `t2_rename/scan.py` must be byte-identical to
`repro_fixed/scan.py`.

顺带一提：这条命令同时验证了 `bisect_taint.py` 自己 —— `t1_control` 必须报 1 条，
`t2_rename` 必须报 0 条，且 `t2_rename/scan.py` 应与 `repro_fixed/scan.py` 逐字节相同。
