# FAQ · 高频问题

<!-- locale-policy note · 语言政策声明
此文件有意中英混排：本技能的读者群体**同时**包含中文使用者与英文使用者，且**不强制任一语言**（中文使用者可直接读本文件，英文使用者亦然）。单语版本见 README → "Language selection"，亦可用 --lang en 显式指定语言。
This file is intentionally bilingual: the audience is both Chinese- and English-speaking, and neither language is imposed. A single-language edition is selectable — see README → "Language selection"; the CLI takes --lang en to pin the language explicitly.
-->

> 评测指出：高频问题分散在脚本注释或段落里，没有集中收口。本文件统一回答实战中最常被问到的几类问题。
> 本 skill 只做**告警定位与成因验证**，不是扫描器、不是整库审计工具——下面第 4 条尤其重要。

---

## 1. 基线（t1_control）没复现告警，怎么办？

**这是设计意图，不是 bug。**

变体二分的第一步 `t1_control` 是源文件的**原样复制**，它必须先在本地复现出那条远程告警。
如果 `t1_control` 就 0 结果，说明**你本地环境与当初产生告警的远端环境不一致**：

- CodeQL CLI 版本不同（查询语义有差异）；
- `--language` / 查询套件版本不同；
- 包依赖、编译开关、构建环境不同导致抽取到的代码图不同。

此时后面的 `t2_xxx / t3_xxx` 判定**全部不可信**——脚本会打印 `⛔ 基线未复现！结论不可信`
并以退出码 `1` 结束。正确做法：**先对齐 CodeQL 版本与查询套件**，让 `t1_control` 能稳定复现，
再谈定位。强行在「基线不复现」的前提下下结论，等于在错误的地基上盖楼。

---

## 2. 改动比较复杂，怎么做变体？

**铁律：一次只改一个变量。** 多变量同时改，你就说不清「是哪一个生效」。

- **字面量替换**（最常见的改名）：用 `--variant t2_rename=SUSPECT_A:SUSPECT_B`，
  脚本会把源文件里所有 `SUSPECT_A` 替换成 `SUSPECT_B` 生成变体。判定规则：
  - 替换后告警**消失** → 该名字就是 taint 源；
  - 替换后**仍在** → 这个名字不是成因，换下一个嫌疑。
- **复合改动**（正则手术、跨多处逻辑）：把改好的文件单独写出来，用
  `--variant-file t3=/path/to/t3.py` 整份替换进去。这样改动内容由你完全掌控，
  脚本只负责把它 staged 进去跑同一条查询。

无论哪种，控制变量是关键：每个变体相对 `t1_control` **只允许有一处差异**，
否则「告警消失 / 仍在」无法归因到具体改动。

---

## 3. 为什么这叫「variant bisection」，跟 Trail of Bits 的 variant-analysis 是一回事吗？

**不是一回事。**

- **Trail of Bits 的 variant-analysis**：给定一处已知漏洞，在代码库里**搜索同类新漏洞**
  （横向找兄弟）。本质是「以洞找洞」的模式匹配。
- **本 skill 的 variant bisection**：针对**同一条已存在的告警**，通过逐一改掉候选源、
  重建、跑同一条查询，用「告警是否消失」来**定位这条告警的成因变量**（纵向定位）。

两者都用「variant」这个词，但目标相反：一个是扩散找新洞，一个是收敛定老洞。
本 skill 不做横向漏洞挖掘，只回答「这条具体告警，到底是哪个变量引起的」。

---

## 4. 我「感觉」这条告警是误报，能不能直接 dismiss？

**不建议直接 dismiss，先用对照实验验证。**

「感觉像误报」往往来自直觉，而 CodeQL 的 source 判定有它自己的规则（按名字，不看内容）。
在没做变体二分之前 dismiss，可能：
- 漏掉一个**真实**的污染源（你以为的误报其实是真漏）；
- 或只是把告警从面板挪走，根因没动，下次换条路径又冒出来。

正确姿势：跑一遍三步流程——`scan_sensitive_sources.py` 预筛 → `read_sarif.py` 看实际命中
→ `bisect_taint.py` 定位成因。等你有**可复现的因果结论**（某个变量去掉告警就消失），
再去 dismiss 才站得住脚，也方便在 PR 里写清理由。

---

## 5. 哪些名字**不该**算敏感源？为什么 `[REDACTED_SECRET]` 没被标红？

这正是 `scan_sensitive_sources.py` 的**反向排除器**（`NOT_SENSITIVE`，抄自 CodeQL 的
`SensitiveDataHeuristics.qll` 的 `notSensitiveRegexp()`）在起作用。

名字里出现以下片段会被**排除**，不算敏感 source：

- `redact` / `censor` / `obfuscate` —— 你在**处理/脱敏**敏感数据，不是在使用它；
- `hash` / `md5` / `sha` / `random` —— 已做了不可逆变换或随机化；
- `(?<!unen)crypt` / `(?<!un)encode` —— 已经在加密/编码，**不是明文落库**；
- `path` / `url` / `file` 等 —— 路径/地址类，不属于 CWE-312 关心的明文敏感数据。

所以 `"[REDACTED_SECRET]"` 这种**占位符**会被 `redact` 排除，不应该被当成污染源去追 taint。
完整规则与「正向 7 类 source」对照见 [`sensitive-data-heuristics.md`](./sensitive-data-heuristics.md)。

---

## 6. 三步各自需要什么依赖？

| 步骤 | 需要 CodeQL CLI? | 需要联网? | 读 | 写 |
|---|---|---|---|---|
| ① 预筛 `scan_sensitive_sources.py` | 否 | 否 | 源码 | stdout / `--json` |
| ② 读 SARIF `read_sarif.py` | 否 | 否 | `.sarif` | stdout / 断言 |
| ③ 变体二分 `bisect_taint.py` | **是** | 仅首次下载 CLI 时需 | 源码 | `<tree>/_bisect` 临时库 + `.sarif` |

也就是说，**只有第 ③ 步必须装 CodeQL CLI**；前两步纯 Python 标准库，离线即可跑。
第 ③ 步缺 `--codeql` 时脚本会自动降级为「只生成变体目录，不跑分析」，方便你先检查改动对不对。

所有写盘都只发生在 `<tree>/_bisect/`（或你 `--workdir` 指定的目录）——即 `SKILL.md` 的 H5 与「能力边界」所约束的写盘面，绝不会写到仓库之外或系统目录；这与任何「跨会话持久化 agent 状态」无关。
All writes stay under `<tree>/_bisect/` (or your `--workdir`): the write surface bounded by H5 / "Capability boundary" in `SKILL.md` — never outside the repo or a system directory, and unrelated to any cross-session persistent agent state.
