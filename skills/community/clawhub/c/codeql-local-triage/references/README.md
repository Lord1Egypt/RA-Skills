# references/ · 目录索引

本目录存放「深读材料」，SKILL.md / README.md 正文只引用、不重复其内容。
按需查阅即可，不必通读。

## 怎么读 / How to read this directory

**按你此刻的目的选一条路，不必通读：**

| 你现在的目的 | 建议阅读顺序 | 预计耗时 |
|---|---|---|
| **只想判断「这条告警是不是误报」** | `SKILL.md` §0 零依赖快速路径 → `README.md` 的 worked example → 跑 `scan_sensitive_sources.py` + `read_sarif.py` | **零安装、几分钟** |
| 第 ③ 步报「codeql 不存在」 | 只读 [`running-codeql-cli.md`](./running-codeql-cli.md) §1–§4 | 首次 ~15 min（国内见 §5） |
| 国内网络 / 想离线 | 只读 [`running-codeql-cli.md`](./running-codeql-cli.md) §5 | 几分钟 |
| 想知道某名字为何被判敏感 | 只读 [`sensitive-data-heuristics.md`](./sensitive-data-heuristics.md) | 10 min |
| 基线不复现 / 复杂改动 / 能否 dismiss | 只读 [`faq.md`](./faq.md) 对应小节 | 5 min |
| 接入 CI / 流水线门禁 | 只读 [`ci-integration.md`](./ci-integration.md) | 10 min |
| 系统性读一遍 | 按 `running-codeql-cli.md` → `sensitive-data-heuristics.md` → `faq.md` → `ci-integration.md` | ~1 h |

> **不确定该看哪个？** 先看 `SKILL.md` §0「Zero-dependency fast path」——多数问题在那里就结束了，
> 根本不需要进本目录。

## 文件清单 / Files

| 文件 | 用途 | 适合什么场景 |
|---|---|---|
| [`running-codeql-cli.md`](./running-codeql-cli.md) | 安装 / 验证 CodeQL CLI 的完整步骤链；§5 为国内与离线选项（镜像、预建 DB、免联网） | 第 ③ 步 `bisect_taint.py` 报「codeql 不存在」，或你从未装过 CodeQL |
| [`sensitive-data-heuristics.md`](./sensitive-data-heuristics.md) | 名字启发式规则原理速查（正向 7 类 source + 反向排除器） | 想搞懂 `scan_sensitive_sources.py` 为什么把某些名字判成敏感、某些不算 |
| [`faq.md`](./faq.md) | 高频问题集中收口 | 基线没复现怎么办 / 复杂改动怎么做变体 / 能不能直接 dismiss / 哪些名字不算敏感源 |
| [`ci-integration.md`](./ci-integration.md) | CI 流水线门禁接入：GitHub Actions / GitLab CI 最小可用片段 | 想把「结果数必须归零」变成自动门禁 |

> 三步工作流、退出码契约、命令模板等「主干内容」在 `SKILL.md`（英文规范版）与 `SKILL.zh.md`（中文翻译版）以及仓库根 `README.md`；
> 这里只放「展开讲才清楚」的支线材料。
>
> 语言：本技能拆分为 `SKILL.md`（英文，agent 实际加载）与 `SKILL.zh.md`（中文，内容镜像一致）两份并列文件，按需取用；
> 脚本运行时输出可用 `--lang {auto,zh,en}` 指定（`auto` 按当前 agent 上用户实际语言选择，默认英文，绝不中英混排）。