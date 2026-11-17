# codeql-local-triage

**Reproduce CodeQL alerts locally, locate the taint source with variant bisection, and verify the fix before you push.**
**在本地复现 CodeQL 告警、用「变体二分」定位 taint 源、推送前验证修复。**

> **Language / 语言**：this document is bilingual — **English first, 中文紧随其后**。
> 本文档中英对照：**英文在前、中文在后**，两段讲的是同一件事。
>
> **All examples are synthetic.** Every snippet, fixture and SARIF file in this repository is
> purpose-built sample code. No real project's source, file names or line numbers are included.
> **所有示例均为模拟代码。** 仓库内的代码片段、fixture 与 SARIF 全部为演示而构造，
> 不含任何真实项目的源码、文件名或行号。

GitHub's Code Scanning page **does not tell you where the data came from** — it only marks the sink line.
Remote scanning takes minutes and gives you no way to run a controlled experiment.
This repository turns the investigation into three commands:

GitHub 的 Code Scanning 告警页面**不告诉你数据从哪来**——只标出 sink 那一行。
远端扫描又要等好几分钟，还没法做对照实验。本仓库把排查变成三条命令：

> ### ★ Start here: the zero-dependency fast path
>
> **Steps ① and ② need no download at all** — pure Python stdlib, no CodeQL, no network. The ~400 MB
> CodeQL CLI exists only for step ③, whose single job is to **prove** causation by controlled
> experiment. If you only need to know *whether* the alert comes from a name heuristic and *where* the
> taint starts, steps ①② already answer that. Install the CLI when — and only when — you need the proof.
>
> **从第 ① 步开始：零依赖快速路径。**
>
> **第 ① ② 步完全不需要下载任何东西**——纯 Python 标准库，不装 CodeQL、不联网。那 ~400MB 的
> CodeQL CLI 只服务于第 ③ 步，而第 ③ 步唯一的作用是用对照实验**证明**因果。若你只需要知道
> 「这条告警是否命中名字启发式、污染从哪开始」，前两步已经答完了；等到需要「证明」时再去装 CLI。
>
> | Your question / 你的问题 | Steps / 需要哪步 | Install CodeQL? |
> |---|---|---|
> | Which names could be sensitive sources? / 哪些名字算敏感源 | ① prefilter | **No** |
> | Where does the taint start, what does the path look like? / 污染从哪开始、路径什么样 | ② `read_sarif.py` | **No** |
> | Prove it is a false positive, not infer it / **证明**是误报，而非推测 | ①②③ | Yes |
> | Verify the fix drives results to 0 / 验证修复后归零 | ② `--expect 0` | Only to regenerate SARIF |
>
> The self-test also runs without CodeQL: `python tests/run_tests.py`.
> 自测同样不需要 CodeQL：`python tests/run_tests.py`。

```bash
python scripts/scan_sensitive_sources.py src/     # 1. prefilter, no DB build needed / 免建库预筛
python scripts/read_sarif.py out.sarif            # 2. draw the full source→sink path / 读出完整数据流
python scripts/bisect_taint.py --source f.py --tree . \
    --variant t2=OLD:NEW --codeql <codeql>        # 3. change ONE thing at a time, rerun the query
```

---

## A worked example: from "this looks like a false positive" to the root cause
## 一个完整的排查示例：从「看着像误报」到查出根因

The walkthrough below uses the minimal reproduction that ships with this repository
(`tests/fixtures/repro/scan.py`, 25 lines). Its measured output is checked in under
`tests/fixtures/sarif/`, so you can re-run every command below **without installing CodeQL** —
regenerating the SARIF itself from scratch is the only step that needs it.

下面的过程用的是本仓库自带的**最小复现**（`tests/fixtures/repro/scan.py`，25 行）。
它的实测输出已随仓库提供（`tests/fixtures/sarif/`），所以下面的命令**不装 CodeQL 也能全部复跑**——
只有「从零重新生成 SARIF」这一步才需要 CodeQL。

### The alert / 告警

A file that never stores a credential gets an **error-level** `py/clear-text-storage-sensitive-data`:

一个**从不存任何凭据**的文件，却报了 **error 级** `py/clear-text-storage-sensitive-data`：

```text
scan.py:22  This expression stores sensitive data as clear text.
```

Line 22 is just the tool writing its own result to a JSON file:

第 22 行只是它把自己检查的结果写成 JSON：

```python
findings = {"hit": detect("hello world")}                        # L21
Path(out).write_text(json.dumps(findings), encoding="utf-8")     # L22  <- sink
```

"It looks like a false positive" is **not** a reason to dismiss an alert. Build a local
database, run the single query, and pull the full path out of SARIF's `codeFlows`:

「感觉像误报」**不能**作为 dismiss 的理由。本地建库、单跑这条查询，从 SARIF 的 `codeFlows` 里取出完整路径：

```bash
python scripts/read_sarif.py tests/fixtures/sarif/repro.sarif
```

```text
SOURCE   0. scan.py:10   ControlFlowNode for List
         1. scan.py:10   ControlFlowNode for SECRET_PATTERNS
         2. scan.py:14   ControlFlowNode for SECRET_PATTERNS
         3. scan.py:14   ControlFlowNode for pat
         4. scan.py:16   ControlFlowNode for pat
         5. scan.py:21   ControlFlowNode for detect()
         6. scan.py:21   ControlFlowNode for Dict [Dictionary element at key hit]
         7. scan.py:21   ControlFlowNode for findings [Dictionary element at key hit]
         8. scan.py:22   ControlFlowNode for findings [Dictionary element at key hit]
SINK     9. scan.py:22   ControlFlowNode for Attribute()
```

**The source is the variable name `SECRET_PATTERNS`** — a list that holds nothing but regex strings.
CodeQL's name heuristic (`maybeSecret()`) only looks at whether the name contains `secret`.

**污染源是变量名 `SECRET_PATTERNS`**——那只是个存放正则字符串的列表，里面没有任何凭据。
CodeQL 的名字启发式（`maybeSecret()`）只看名字含不含 `secret`。

### But a conclusion needs a controlled experiment, not a hunch
### 但结论不能靠推理，要靠对照实验

Change exactly one thing at a time, rebuild, and rerun the same query
(this is what `scripts/bisect_taint.py` automates). The two rows below are **measured**, not predicted —
their SARIF output is checked in as `tests/fixtures/sarif/repro.sarif` and `repro_fixed.sarif`:

一次只改一个变量，各自建库跑同一条查询（`scripts/bisect_taint.py` 就是干这个的）。
下面前两行是**实测值**，对应 SARIF 已随仓库提供：

| Variant / 变体 | Change / 改了什么 | Results / 结果数 | Verdict / 判定 |
| --- | --- | --- | --- |
| `t1_control` | none (baseline, added automatically) / 原样（自动添加） | 1 | baseline reproduces ✅ / 基线复现 ✅ |
| `t2_rename` | `SECRET_PATTERNS` → `CREDENTIAL_PATTERNS` | **0** | ✅ this name is the cause / 就是这个名字 |
| `t3_xxx`, `t4_xxx` … | suspects you add yourself / 你自己补的嫌疑项 | — | 0 ⇒ that change is the cause; >0 ⇒ it is not<br>0 处 ⇒ 是成因；仍命中 ⇒ 不是成因 |

Guessing from the query source is unreliable. A `base64.b64decode()`, a `json.dumps()` or an f-string
sitting on the path all *look* like plausible sources, and a single added variant often falsifies the
first hypothesis outright. **Run the experiment before you write the conclusion.**

凭读 QL 源码推断很容易错。路径上的 `base64.b64decode()`、`json.dumps()`、f-string 都**看着**像污染源，
而只要多加一个变体，首选假设常常被直接证伪。**先做对照实验，再下结论。**

### The fix / 修法

Rename it. Behaviour is unchanged, the data flow is unchanged, no public API moves.

改名，逻辑零变更。

```diff
-SECRET_PATTERNS = [...]
+CREDENTIAL_PATTERNS = [...]
```

Rerunning the same query on the renamed tree returns **0 results** — that is the second checked-in SARIF
file, `tests/fixtures/sarif/repro_fixed.sarif`. Two things about this fix are worth keeping in mind:

改名后在同一棵树上重跑同一条查询，结果是 **0 处**——就是仓库里第二份 SARIF
（`tests/fixtures/sarif/repro_fixed.sarif`）。这个修法有两点值得注意：

1. It is a **rename, not a suppression**. No `# lgtm` comment, no dismissal — so the alert can never
   come back, and the next reader does not have to re-investigate.
   **是改名，不是抑制**：不写 `# lgtm`、不 dismiss，告警不会复发，下一个人也不用重查一遍。
2. Leave a comment at the definition saying **"do not rename this back"** plus the rule that caused it —
   otherwise somebody will helpfully undo your fix.
   在定义处留一句「**勿改回去**」+ 规则出处，否则下一个人会顺手把名字改回来。

> This class of false positive is common in exactly the tools that have to deal with
> credential-shaped strings: compliance checkers, log scrubbers, secret scanners, redaction utilities.
> They trip the rule not because they handle secrets, but because their variables are *named* that way.
>
> 这类误报最常出现在**必须处理「密钥形态字符串」的工具**里：合规检查器、日志脱敏器、密钥扫描器、
> 打码工具。它们触发规则不是因为真的处理了密钥，而是因为变量**名字**长这样。

---

## Repository contents / 仓库内容

| File / 文件 | What it does / 作用 |
| --- | --- |
| `scripts/scan_sensitive_sources.py` | **Prefilter, no DB build required.** Re-implements CodeQL's name heuristic as a Python `ast` check and statically lists every name/literal that could become a taint source — saving one ~9-minute database build.<br>**免建库预筛**。把名字启发式等价移植成 `ast` 检查，静态列出所有可能成为 taint 源的名字/字面量，省掉一次 ~9 分钟的整仓建库。 |
| `scripts/read_sarif.py` | **Reads `codeFlows` from SARIF** and prints the whole source→sink path, step by step. This step is usually where the answer is. Supports `--expect N` for assertions.<br>**读 SARIF 的 `codeFlows`**，按步打印 source→sink 全路径。这一步通常就是答案所在。支持 `--expect N` 做断言。 |
| `scripts/bisect_taint.py` | **Variant bisection.** Generates "one change only" copies of the tree → builds and analyses each → prints a verdict table. Aborts if the baseline does not reproduce, so you never trust an invalid conclusion.<br>**变体二分**。生成「只改一处」的副本 → 逐个建库+分析 → 输出判定表。基线没复现就直接报错，避免采信无效结论。 |
| `references/sensitive-data-heuristics.md` | Cheat sheet for the name heuristics: 5 regex groups, the exclusion regex, 7 source categories, and the CWE-312 source/sink special cases.<br>名字启发式速查表：5 组正则、反向排除器、7 类 source、CWE-312 的 source/sink 特例。 |
| `references/faq.md` | **High-frequency questions in one place**: what to do when the baseline does not reproduce, how to make a variant for a complex change, whether you can just dismiss an alert, which names are *not* sensitive.<br>**高频问题集中收口**：基线没复现怎么办、复杂改动怎么做变体、能不能直接 dismiss、哪些名字不算敏感源。 |
| `references/ci-integration.md` | **CI gate recipes**: minimal GitHub Actions / GitLab CI snippets that turn "result count must be 0" into an automated check.<br>**CI 门禁配方**：GitHub Actions / GitLab CI 最小片段，把「结果数必须归零」变成自动门禁。 |
| `references/README.md` | Index of the `references/` directory: what each file is for and when to read it.<br>`references/` 目录索引：每个文件的用途与适用场景。 |
| `SKILL.md` | The skill definition for AI agents (Claude Code / WorkBuddy / …); installable as a whole.<br>给 AI agent 用的技能定义，可整套安装。 |
| `tests/` | Self-test that needs **no CodeQL**: two *measured* SARIF fixtures plus per-item assertions.<br>不需要 CodeQL 的自测：两份**实测** SARIF fixture + 逐项断言。 |

## Quick start / 快速开始

> 命令的**权威参考与参数契约**（含三步依赖矩阵、退出码、产物命名）见 `SKILL.md`（英文）/ `SKILL.zh.md`（中文）。本节的「快速开始」是给人类读者的实操流程，命令与上面保持一致；要看「为什么这样跑」的完整教程，也回到这两份文件。

### 0. Install the CodeQL CLI (once, ~15 min) / 安装 CodeQL CLI（一次性，约 15 分钟）

Download the archive for your platform from
[github/codeql-cli-binaries](https://github.com/github/codeql-cli-binaries/releases):

```bash
gh release download v2.27.1 --repo github/codeql-cli-binaries --pattern "codeql-win64.zip"
python -c "import zipfile; zipfile.ZipFile('codeql-win64.zip').extractall('.')"
./codeql/codeql version
```

| Platform / 平台 | `--pattern` |
| --- | --- |
| Windows x64 | `codeql-win64.zip` |
| Linux x64 | `codeql-linux64.zip` |
| macOS | `codeql-osx64.zip` (Intel) / `codeql-osx-arm64.zip` (Apple silicon) |

> The zip contains **extractors only**; the query packs (`codeql/python-queries`) are pulled
> automatically by `database analyze --download`. Expect ~400 MB — run it in the background,
> and prefer Python's `zipfile` over `unzip` for large archives.
>
> 该 zip **只含提取器**，查询包（`codeql/python-queries`）会在 `database analyze --download` 时自动拉取。
> 约 400MB，建议后台跑；大文件用 Python `zipfile` 解压比 `unzip` 稳。

If you only need `scan_sensitive_sources.py` and `read_sarif.py`, **you can skip CodeQL entirely** —
that is enough to run the self-test.

只要 `scan_sensitive_sources.py` 和 `read_sarif.py` 的话，**不装 CodeQL 也能用**（自测就跑得起来）。

> 国内网络下载慢 / 想离线？`references/running-codeql-cli.md` 的 **§5 国内与离线选项** 给了镜像、预建 DB 随附查询包、`--codeql` 免联网免 PATH 等方案；该文件的 §1–§4 是面向新手的「从零安装并验证」完整步骤链。
>
> Slow download in your region / want offline? `references/running-codeql-cli.md` **§5 Domestic & offline options** covers mirrors, carrying pre-built DBs + packs, and `--codeql` (no network, no PATH); its §1–§4 is the complete from-scratch install-and-verify chain for beginners.

### 1. Prefilter / 预筛

```bash
python scripts/scan_sensitive_sources.py src/             # recurses into a directory / 目录会递归
python scripts/scan_sensitive_sources.py $(git ls-files '*.py')
python scripts/scan_sensitive_sources.py src/ --json      # machine-readable / 机器可读
```

Exit codes: `0` clean / `1` candidate sources found — usable directly as a CI gate.

退出码：`0` 干净 / `1` 发现候选源 —— 可以直接当 CI 门禁。

### 2. Run a single query / 跑单条查询

Run only the rule you care about — **never** the whole **query suite** (a CodeQL *query collection* — unrelated to system services or scheduled tasks; `python-code-scanning.qls` takes tens of minutes).

只跑目标那一条，**别**跑整个 **query suite（查询套件，CodeQL 的查询集合概念，与系统服务/计划任务无关）**（`python-code-scanning.qls` 要几十分钟）：

```bash
codeql database create  ./_db_triage --language=python --source-root=src --overwrite --threads=0
codeql database analyze /tmp/db --download --format=sarif-latest --output=/tmp/out.sarif \
    --threads=0 "codeql/python-queries:Security/CWE-312/CleartextStorage.ql"
```

### 3. Read the data flow / 读数据流

```bash
python scripts/read_sarif.py /tmp/out.sarif
python scripts/read_sarif.py /tmp/out.sarif --json
python scripts/read_sarif.py /tmp/out.sarif --expect 0    # assert zero alerts, CI-friendly / 断言清零
```

### 4. Variant bisection / 变体二分

```bash
# Inspect the change first, without building any database / 先只看改动对不对（不建库）
python scripts/bisect_taint.py --source scan.py --tree . --dry-run \
    --variant t2_rename=SECRET_PATTERNS:CREDENTIAL_PATTERNS

# Full run / 完整跑
python scripts/bisect_taint.py --source scan.py --tree . \
    --variant t2_rename=SECRET_PATTERNS:CREDENTIAL_PATTERNS \
    --codeql /path/to/codeql --workdir /tmp/taint_bisect
```

When a change is too complex for a literal replacement (regex surgery, restructuring),
produce the edited file by hand and swap the whole file in:

复杂改动（正则手术、结构调整）做不了字面量替换时，手工产出一份改好的文件再整份替换：

```bash
python scripts/bisect_taint.py --source scan.py --tree . \
    --variant-file t3=/tmp/t3_scan.py --codeql /path/to/codeql
```

## JSON output / JSON 输出（language-neutral / 语言中立）

Both readers emit English JSON keys, so scripts and agents can consume them regardless of locale.
All CLI *messages* follow the user's chosen language (`--lang {zh,en}` / `TRIAGE_LANG` /
`AGENT_UI_LANG`, default English); `--json` is the locale-independent interface.

两个读取脚本的 JSON key 都是英文，脚本与 agent 可跨语言直接消费。
CLI 的**提示文字**跟随用户所选语言（`--lang {zh,en}` / `TRIAGE_LANG` / `AGENT_UI_LANG`，默认英文）；
`--json` 是与语言无关的接口。

```jsonc
// scripts/scan_sensitive_sources.py --json
{
  "files": [{
    "file": "path/to/file.py",
    "sources": [{ "class": "SensitiveVariableAssignment",
                  "line": 10, "label": "LHS=SECRET_PATTERNS",
                  "hits": ["secret"], "text": "SECRET_PATTERNS = [...]" }],
    "sensitive_literals": ["api_key"]
  }],
  "total_sources": 1
}

// scripts/read_sarif.py --json
{
  "sarifs": [{
    "file": "...", "tool": "CodeQL", "version": "2.27.1", "artifacts": 1,
    "results": [{
      "rule": "py/clear-text-storage-sensitive-data", "level": "error", "message": "...",
      "sink": { "file": "scan.py", "line": 22, "col": 26, "role": "", "snippet": "..." },
      "flows": [[ { "file": "scan.py", "line": 10, "role": "ControlFlowNode for List", "snippet": "..." } ]]
    }]
  }],
  "total_results": 1
}
```

## Language selection / 语言选择

The CLI scripts are **not** hard-wired to one language — this is a deliberate, documented
constraint, not an accident. The language is always **user-selectable**:

- `--lang {zh,en}` on any script, or the `TRIAGE_LANG` / `AGENT_UI_LANG` environment variable.
- `auto` (the default) resolves to a *single* language from the agent UI language or OS locale,
  falling back to **English**; it never emits both languages at once.
- `scripts/i18n.py` is the four-tier resolver (see its module docstring for full precedence).

Why mono-language by design: these messages land in CI logs and terminals that are grepped, so one
predictable language per stream is the useful default. Bilingual output is avoided because it risks a
natural-language policy violation on generated content. **Chinese is fully supported** — a complete,
equally authoritative Chinese rendering of this skill is `SKILL.zh.md`.

本技能的命令行脚本**不**写死某一种语言——这是经过设计、明确记录的约束，并非疏漏。
语言**始终由用户选择**：

- 任意脚本加 `--lang {zh,en}`，或设置 `TRIAGE_LANG` / `AGENT_UI_LANG` 环境变量。
- `auto`（默认）依据 agent 界面语言或系统 locale 解析出**单一**语言，默认回退**英文**；
  绝不会中英同时输出。
- `scripts/i18n.py` 是四级解析器（完整优先级见其模块文档字符串）。

为何设计成单一语言：提示会出现在 CI 日志与终端里、常被 grep，所以每条流一种可预期的语言最实用。
避免双语是因为它可能在生成内容上触发自然语言策略违规。**中文完全受支持**——本技能的完整、
同等权威中文版是 `SKILL.zh.md`。

Exit codes / 退出码:

| Script / 脚本 | `0` | `1` | `2` |
| --- | --- | --- | --- |
| `scan_sensitive_sources.py` | no candidate source / 未发现候选源 | candidates found / 发现候选源 | usage error / 参数错误 |
| `read_sarif.py` | 0 results (or `--expect` matched) / 无结果或断言通过 | has results / `--expect` failed · 有结果或断言失败 | bad input / 输入错误 |
| `bisect_taint.py` | finished, baseline reproduced / 跑完且基线复现 | baseline did NOT reproduce / 基线未复现（结论不可信） | runtime error / 运行出错 |

## Verification / 验证

```bash
python tests/run_tests.py        # or: pytest tests/run_tests.py -q
```

> Note: pytest will **not** auto-collect this file — its name is `run_tests.py`, not `test_*.py`.
> You must pass the path explicitly (`pytest tests/run_tests.py`); `pytest tests/` collects nothing.
>
> 注意：pytest **不会**自动收集这个文件——它叫 `run_tests.py`，不匹配 `test_*.py`。
> 必须显式指定路径（`pytest tests/run_tests.py`）；`pytest tests/` 会一条用例都收集不到。

No CodeQL installation required. It asserts against the two **measured** SARIF files checked in under
`tests/fixtures/sarif/`, and covers:

不需要装 CodeQL。它用仓库内两份**实测 SARIF**（`tests/fixtures/sarif/`）做断言，覆盖：

- prefilter regex self-test (the classifier agrees with the QL definitions)
  预筛正则自检（分类器与 QL 定义一致）
- `repro/scan.py` yields exactly 1 candidate source, `repro_fixed/scan.py` is clean — and the two files
  are **byte-identical apart from the variable name** (so the experiment really has one variable)
  `repro/scan.py` 命中 1 处、`repro_fixed/scan.py` 干净 —— 且两份**除变量名外逐字节相同**
- `read_sarif.py` reads 1 / 0 results correctly, and `--expect` asserts as documented
  `read_sarif` 判读 1 条 / 0 条正确，`--expect` 断言生效
- the source line can be recovered from `codeFlows` and mapped back to the file to confirm it is
  that sensitive-name assignment
  能从 `codeFlows` 取回 source 行，并比对回源文件确认就是那行敏感名赋值

`tests/fixtures/repro/` is a **25-line reproduction containing no credential at all** that still
triggers an error-level alert.

`tests/fixtures/repro/` 是一个 **25 行、不含任何凭据**的最小复现，同样触发 error 级告警。

## CI 门禁示例 / CI gate example

把「预筛 + 读 SARIF」直接接进 CI：预筛命中候选源时退出码为 `1`（构建即失败），读 SARIF 用 `--expect 0` 做断言。两条都**零依赖**，可在没装 CodeQL CLI 的 runner 上跑。
Wire the prefilter + SARIF reader straight into CI: the prefilter exits `1` when it finds candidate sources (failing the build), and `read_sarif.py --expect 0` asserts a clean result. Both are **zero-dependency** and run on a runner without the CodeQL CLI.

```yaml
# .github/workflows/triage-gate.yml
name: codeql-local-triage gate
on: [push, pull_request]
jobs:
  triage:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.x" }
      # 1) zero-dependency prefilter: fails the build if candidate sources appear
      #    零依赖预筛：出现候选源即让构建失败
      - run: python scripts/scan_sensitive_sources.py path/to/file.py
      # 2) if you already have a SARIF from CodeQL, assert zero results
      #    若已有 CodeQL 产出的 SARIF，断言清零
      - run: python scripts/read_sarif.py results.sarif --expect 0
```

> 两点提醒 / Two notes:
> - 预筛只用名字启发式做**预验**，不是最终判定；真要关单仍以 GitHub 自己的 CodeQL 扫描为准。
>   The prefilter is a **pre-check** by name heuristic, not the final verdict; closing an alert still defers to GitHub's own CodeQL scan.
> - 这两条都**零依赖**，可在没装 CodeQL CLI 的 runner 上直接跑。
>   Both steps are **zero-dependency** and run on a runner without the CodeQL CLI installed.

## Directory layout / 目录结构

```text
.
├── scripts/
│   ├── scan_sensitive_sources.py   prefilter (no deps) / 预筛
│   ├── read_sarif.py               data-flow reader (no deps) / 数据流读取
│   └── bisect_taint.py             variant bisection (needs CodeQL) / 变体二分
├── references/
│   └── sensitive-data-heuristics.md
├── tests/
│   ├── run_tests.py
│   └── fixtures/
│       ├── README.md               fixture notes + regeneration / 夹具说明与重生成方法
│       ├── repro/scan.py           triggers the alert (25-line repro) / 命中
│       ├── repro_fixed/scan.py     control (renamed only) / 对照
│       └── sarif/                  two measured SARIF files / 两份实测 SARIF
├── SKILL.md
├── NOTICE                          third-party attribution / 第三方署名
└── LICENSE
```

## Scope and limitations / 适用范围与限制

Read this before you rely on it. / 用之前先看这一段。

- **Only name-heuristic false positives.** A real vulnerability (a credential actually written to disk
  in clear text) must be fixed in code — renaming it would be hiding it. Look at what the source in
  `read_sarif.py`'s path actually is before deciding.
  **只处理名字启发式这一类误报。** 真漏洞（凭据真的被明文写盘）当然要改代码，改名只是掩盖。
  先看 `read_sarif.py` 打出的路径里源是什么，再决定。
- **The prefilter supports Python only** (`py/*` queries). `read_sarif.py` and `bisect_taint.py` are
  language-agnostic.
  **预筛脚本目前只支持 Python**（`py/*` 查询）。另两个脚本与语言无关。
- **The regexes mirror one specific CodeQL version.** The measured baseline is CodeQL CLI 2.27.1 /
  `codeql/python-queries` 1.8.11. After an upstream update, `references/` and
  `scan_sensitive_sources.py` need to follow — always treat your local
  `SensitiveDataHeuristics.qll` as authoritative.
  **正则抄的是特定版本的 CodeQL。** 实测基线是 CodeQL CLI 2.27.1 / `codeql/python-queries` 1.8.11。
  上游更新后需同步——请以你本地的 `SensitiveDataHeuristics.qll` 为准。
- **This is "pre-verify and locate", not a replacement for CI.** The final state of an alert is decided
  by GitHub's own scan. Note that the `updated_at` of `code-scanning/alerts/<n>` **only refreshes when
  the state changes** — it cannot tell you whether a rescan happened. Look at `state` or whether the
  line numbers moved.
  **本项目定位是「本地预验 + 定位」，不替代 CI。** 告警最终状态由 GitHub 自己的扫描决定。
  注意 `updated_at` **只在状态变化时刷新**，不能用它判断「有没有重扫」；看 `state` 或行号是否变了。
- When local and remote disagree, first make sure no **concurrent edits** were happening during your
  local build (another process writing files will desynchronise your conclusion).
  本地与远端结论不一致时，先确认本地建库时工作区没有**并发改动**。

## Attribution / 署名

The regexes and QL snippets in `references/sensitive-data-heuristics.md` and
`scripts/scan_sensitive_sources.py` are taken from [github/codeql](https://github.com/github/codeql)
(MIT License, Copyright GitHub, Inc.). This project is a **readable restatement and equivalent port**
of those definitions — it is not an official GitHub artifact. Per-file mapping is in [NOTICE](NOTICE);
where the two disagree, **upstream wins**.

`references/sensitive-data-heuristics.md` 与 `scripts/scan_sensitive_sources.py` 中的正则、QL 片段取自
[github/codeql](https://github.com/github/codeql)（MIT License，Copyright GitHub, Inc.），
本项目是对这些定义的**可读重述与等价移植**，非 GitHub 官方产物。
逐文件对应关系见 [NOTICE](NOTICE)；若与上游不一致，以**上游为准**。

Released under the [MIT License](LICENSE).
本项目以 [MIT License](LICENSE) 发布。
