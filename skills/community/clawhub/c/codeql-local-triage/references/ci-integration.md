# CI 集成 · 把「结果数必须归零」变成自动门禁

<!-- locale-policy note · 语言政策声明
此文件有意中英混排：本技能的读者群体**同时**包含中文使用者与英文使用者，且**不强制任一语言**（中文使用者可直接读本文件，英文使用者亦然）。单语版本见 README → "Language selection"，亦可用 --lang en 显式指定语言。
This file is intentionally bilingual: the audience is both Chinese- and English-speaking, and neither language is imposed. A single-language edition is selectable — see README → "Language selection"; the CLI takes --lang en to pin the language explicitly.
-->

> 面向想把告警修复验收**自动化**的用户。三步里只有第 ①② 步适合进 CI（零依赖、不需要装 CodeQL）；
> 第 ③ 步建库耗时且依赖 CLI，**不建议放进流水线**——它属于「本地做一次」的深度排查。
>
> Two of the three steps fit in CI (zero-dependency, no CodeQL install). Step ③ builds a database
> and needs the CLI — keep it out of the pipeline; it is a local, one-off deep investigation.

---

## 0. 三步各自的 CI 适配性 / CI fitness by step

| Step | 进 CI? | 原因 |
|---|---|---|
| ① `scan_sensitive_sources.py` | ✅ 推荐 | 秒级、零依赖；退出码 1/0 直接可作门禁 |
| ② `read_sarif.py --expect N` | ✅ 推荐 | 有 SARIF 产物时最精确的断言 |
| ③ `bisect_taint.py` | ❌ 不建议 | 每次建库 ~9 min、需 400MB CLI、**结论本就是一次性的** |

---

## 1. 先跑通这条命令 / First make this command pass locally

**不要**在本地没跑通就写进 CI。CI 只是把你已经验证过的命令搬过去。

```bash
# 门禁 A：预筛——没有候选源才通过（0=干净，1=有候选源，2=输入错误）
python scripts/scan_sensitive_sources.py src/ --summary

# 门禁 B：验收——重跑同一查询后结果数必须为 0
python scripts/read_sarif.py out.sarif --expect 0
```

两条都满足退出码 `0` 才算通过。**退出码 `2` 是「输入/运行错误」，不是「通过」**——
路径写错、文件不存在都会归到 2，务必让 CI 在 2 时失败而不是悄悄放过。

---

## 2. GitHub Actions / GitHub Actions

```yaml
# .github/workflows/codeql-triage.yml
name: codeql-local-triage
on:
  pull_request:
  push:
    branches: [main]

jobs:
  triage-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      # ① 脚本零第三方依赖，不需要 pip install
      - name: Prefilter gate (candidate sources must be 0)
        run: |
          python scripts/scan_sensitive_sources.py . --summary

      # ② 若你已把 CodeQL 的 SARIF 产物随构建上传为 artifact：
      #    artifacts/download/codeql/out.sarif
      - name: SARIF result count must be 0
        if: ${{ hashFiles('**/*.sarif') != '' }}
        run: |
          python scripts/read_sarif.py out.sarif --expect 0
```

**要点**
- `run` 步骤默认就是 `set -e`，脚本返回非 0 会让 job 失败——**不需要额外写 `if` 判断**。
- 想并行扫大量文件时加 `--jobs 4`（Python 标准库，无需装包）。
- 建议把 `_bisect/` 加进 `.gitignore`，避免产物被提交。

---

## 3. GitLab CI / GitLab CI

```yaml
# .gitlab-ci.yml
codeql-triage:
  image: python:3.12-slim
  script:
    - python scripts/scan_sensitive_sources.py . --summary
    - python scripts/read_sarif.py out.sarif --expect 0
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
```

---

## 4. 退出码契约 / Exit-code contract（CI 判据的唯一真相）

三个脚本统一约定，**CI 只认这个表**：

| 退出码 | 含义 | CI 应视为 |
|---|---|---|
| `0` | 成功 / 未发现候选源 / 断言通过 | ✅ 通过 |
| `1` | 发现候选源、基线未复现、或 `--expect` 断言失败（**是判定结果**） | ❌ 失败 |
| `2` | 输入 / 运行错误（路径不存在、SARIF 非法、参数格式错、`codeql` 失败或超时） | ❌ **失败**（且应报警：这不是「干净」） |

> ⚠️ **最危险的误判**：把「路径不存在」（2）当成「干净」（0）。v1.0.2 起缺失路径**必定**返回 2，
> 就是为了堵这个洞。CI 里**绝不要**把 2 当成通过。

---

## 5. 校验变更是否只改了一处 / Guard the "one variable per variant" rule

变体实验的前提是「每个变体只改一处」。仓库自带的自测里有一条**严格字节比对**断言守着这条不变量，
可以直接进 CI：

```bash
python tests/run_tests.py     # 退出码 0 = 全部用例通过（含 fixture 字节比对、SARIF 校验、参数校验）
```

它**不需要 CodeQL**，几秒就能跑完，适合放在每次提交的检查里。

---

## 6. 与 GitHub Code Scanning 原生告警的关系 / Relation to GitHub Code Scanning

本技能的 SARIF 读取步骤**不替代** Code Scanning：
- **Code Scanning** 负责扫、决定告警的 `state`（关闭与否）；
- **本技能**负责在推送前把「为什么报、改哪一行才会消失」查清楚。

不要试图用 CI 里的脚本去关告警——告警只能由 GitHub 自己的扫描关闭。
详见 `SKILL.md` §7「Post-fix acceptance checklist」第 5 项。

---

## 相关文件 / Related

- `SKILL.md` §1 — 三条命令与退出码契约（主干定义）
- `SKILL.md` §9 — 常见坑（并发编辑会让结论失效，CI 上尤其要注意）
- `references/faq.md` — 基线不复现怎么办