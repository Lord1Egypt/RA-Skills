---
name: debug-pro
displayName: debug-pro
slug: debug-pro
author: 诺声(Logos)@SynomosAI
copyright: SynomosAI
version: 2.0.0
license: MIT
description: "A language-agnostic 7-step debugging protocol (reproduce -> locate the layer -> minimize -> hypothesize -> verify -> fix -> regress) with a zero-dependency, offline toolchain that turns 'I reproduced it' into checkable evidence: triage extracts exception type, last stack frame, exit code, HTTP status and timestamps from raw logs; envsnap builds a paste-ready environment block with every key containing KEY/TOKEN/SECRET/PASS/CRED/AUTH/COOKIE redacted; reprocheck grades the five minimum elements of a reproduction report and names the missing ones. Ships a 10-case golden set with a re-executable runner, a real error-log demo, a layered symptom lookup, a 5-item pre-delivery self-check and degradation rules. Generic methodology tool - not a medical device, no clinical or efficacy claims. Triggers: debug, bug, error, exception, reproduce, root cause, minimal reproduction, regression, git bisect."
description_zh: 调试 / bug 排查 / 代码报错 / 定位原因 —— 提供 7 步标准调试协议（复现→定位层→最小化→假设→验证→修复→回归）+ 分层速查 + 零依赖可跑工具链（triage 日志分诊 / envsnap 环境快照 / reprocheck 复现五要素检查）+ 10 条黄金集自检，把「我复现了」变成可核对的事实，用于回答「代码报错怎么查」「这个 bug 到底在哪」「改了还是不对怎么办」这类问题
description_en: "A language-agnostic 7-step debugging protocol (reproduce -> locate the layer -> minimize -> hypothesize -> verify -> fix -> regress) with a layered symptom lookup and a zero-dependency, runnable toolchain (triage / envsnap / reprocheck) plus a 10-case golden set - making 'I reproduced it' checkable evidence rather than a claim."
displayName_zh: 调试专家
displayName_en: debug-pro
tags:
- 调试
- bug排查
- 代码排错
- 开发工具
- debug-pro
agent_created: true
category: 开发工具
updated: 2026-11-18
fingerprint: FP-MX-F7C2B8ABE794
governance: SynomosAI XCGS / A³ Laws / AI Passport Regime / AI-world coinhabitation
languages:
- zh-CN
- en
- ja
- ko
- es
- fr
- de
- ar
aliases:
- 调试专家
- debug pro
- bug排查
brand: SynomosAI
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 诺声(Logos)@SynomosAI. Copyright: SynomosAI. License: MIT.'
ambassador: 诺声
trigger_keywords:
- debug
- pro
- 调试
- bug排查
- 代码报错
- 定位
- 复现
- 修复
- 回归测试
---

# 7-Step Debugging Protocol

## Overview (English)

A language-agnostic protocol for finding root cause without guessing, plus a zero-dependency offline toolchain that makes the claim "I reproduced it" checkable.

**Seven steps, each with a completion signal.** 1) reproduce a minimal sequence; 2) locate the layer (UI / API / logic / data / environment); 3) minimize until the defect still fires; 4) write 1-3 falsifiable hypotheses; 5) change one variable at a time; 6) fix the verified root cause only; 7) regress, and keep a test that failed before the fix and passes after.

**Three non-negotiables.** Reproduce before touching code. One variable per verification. Never ship without a regression case.

**What is machine-checkable (v2.0).**

| Command | What it proves | Artifact |
|---|---|---|
| `python tools/debughunt.py triage --file err.log` | The error was actually captured: exception type, last stack frame, exit code, HTTP status, timestamps | `.triage.md` + `.facts.json` |
| `python tools/debughunt.py reprocheck --file steps.md` | Someone else can follow the steps: the five minimum elements are present, missing ones are named | `PASS` / `FAIL` + missing list |
| `python tools/debughunt.py envsnap` | Environment differences are ruled out; secret-bearing variables are redacted | paste-ready env block |

Run `python tests/run_golden.py` for the 10-case golden set (10/10 PASS locally) and `python demo/run_demo.py` for the end-to-end proof. Zero dependencies, no network, standard library only. Generic methodology tool - not a medical device, no clinical or efficacy claims.

**中文正文如下。**

# 7 步标准调试协议

遇到 bug 时，**先别急着改代码**。按下面 7 步走，每一步有明确的「完成信号」，做完再进下一步。

## 30 秒速查（先看这里）

| 你的处境 | 直接做什么 | 看哪节 |
|---|---|---|
| 报错了但看不出哪层出问题 | 先跑「复现→定位层」，不要先改代码 | 七步流程 §1–2 |
| 改了还是不对 | 回到「最小化」，把用例砍到 1 条能复现的 | 七步流程 §3 |
| 时好时坏、偶发 | 按分层速查查并发/缓存/超时 | 分层速查 |
| 已经改好、要交付 | 过「交付前自检」5 项再交 | 执行自检 |
| 拿不到日志 / 环境复现不了 | 按降级协议给出可查方向，不猜原因 | 失败与降级处理 |

三条铁律：**先复现再动手**｜**一次只改一个变量**｜**修完必回归**。

## 什么时候用

- 「代码报错怎么查」「这个 bug 到底在哪」「改了还是不对」「线上偶发问题怎么定位」。

## 七步流程

| 步 | 动作 | 完成信号 |
|---|---|---|
| 1 复现 | 拿到可稳定复现的最小操作序列 | 你能在自己机器上按步骤 100% 复现一次 |
| 2 定位层 | 判断 bug 在哪一层：UI / 接口 / 业务逻辑 / 数据 / 环境 | 能说出「问题出在 X 层」，并有一条证据（日志/请求/数据） |
| 3 最小化 | 删掉无关输入/分支/配置，把用例缩到最小 | 删掉一半代码/数据后 bug 仍在 |
| 4 假设 | 写下 1-3 个「如果是 X 导致的，应该看到 Y」的可证伪假设 | 每个假设都能被一条观测证伪 |
| 5 验证 | 一次只改一个变量去验证假设 | 观测结果与 Y 一致或不一致，二选一 |
| 6 修复 | 针对已验证的根因修，不顺手重构 | 最小改动让用例通过 |
| 7 回归 | 跑相关测试 + 补一条能复现原 bug 的用例 | 原 bug 用例在修复前失败、修复后通过 |

**关键纪律**：第 5 步一次只动一个变量；同时改三处，好了也不知道是哪处好的。

## 分层速查

| 症状 | 先怀疑哪层 | 第一条证据怎么拿 |
|---|---|---|
| 页面白屏/样式错 | UI | 打开浏览器 Console 看第一个红字 |
| 接口返回 500 | 接口/业务逻辑 | 看服务端日志该请求的 stack |
| 接口返回 200 但数据不对 | 业务逻辑/数据 | 直接查库该条记录的真实值 |
| 本地好的、线上坏的 | 环境/配置 | diff 两边配置与依赖版本 |
| 偶发、时好时坏 | 并发/时序/缓存 | 加日志打时间戳，连抓 10 次样本 |

## 本地工具链（v2.0，零依赖、不联网）

三个子命令，各管一件机械活；判断仍由你做。

| 子命令 | 作用 | 输出 |
|---|---|---|
| `triage` | 从日志/报错文本抽故障要素：异常类型、栈首帧（文件:行:函数）、退出码、HTTP/业务状态、时间戳、涉及路径、端口 | 分诊卡 `.triage.md` + 事实 `.facts.json` |
| `envsnap` | 生成可粘贴的环境块（OS/机器/解释器/工作目录/PATH 条目数/git 版本） | 环境块；**含 KEY/TOKEN/SECRET/PASS/CRED/AUTH/COOKIE 的环境项强制剔除** |
| `reprocheck` | 检查复现步骤是否具备最小五要素：版本环境 / 操作或命令 / 输入 / 期望与实际 / 证据 | `PASS` 或 `FAIL` + 缺项名列 |

```bash
# 1) 分诊一份报错日志（自动落盘 md + json）
python tools/debughunt.py triage --file demo/sample_error.txt --out out

# 2) 环境快照（贴进 issue 前先跑这个，杜绝「在我机器上能跑」）
python tools/debughunt.py envsnap

# 3) 复现步骤体检（缺哪条写哪条，不靠感觉）
python tools/debughunt.py reprocheck --file demo/repro_steps.md
```

- 机器可读：加 `--json`，固定输出 `{ok, data}`；失败时 `{ok:false, error_id}`。
- 错误码：`D001` 文件不存在 · `D002` 编码不可读 · `D003` 内容为空 · `D004` 无错误特征（这不像故障日志）· `D005` 输出目录不可写。
- 退出码：0 成功 / 1 判定失败（如 reprocheck FAIL） / 2 参数错误。

**一键自证**（本机实测通过，任何人都可复跑）：

```bash
python tests/run_golden.py   # 10/10 PASS：错误抽取、栈首帧、退出码、HTTP 状态、时间戳、非日志拒答、复现五要素正负控、快照零泄漏
python demo/run_demo.py      # 分诊真日志 → 合格步骤 PASS → 残缺步骤 FAIL 并指名缺项 → 快照零泄漏
```

保留的旧版清单一键脚本（向后兼容）：

```bash
python tools/debug_check.py checklist   # 打印七步清单
python tools/debug_check.py card        # 生成 bug 记录卡草稿
```

## Worked example

**现象**：用户登录后偶尔跳回登录页。

1. **复现**：同事反馈后连续登录 20 次，复现 3 次，都是在「记住我」勾选时。
2. **定位层**：登录接口 200，但下次请求 cookie 没带上 → 数据/会话层。
3. **最小化**：去掉其它中间件，只留鉴权，仍复现。
4. **假设**：a) cookie 过期时间算错；b) 跨域被浏览器拦；c) HTTPS 下 Secure 属性丢了。
5. **验证**：一次只看一条 → 发现响应头里 `Set-Cookie` 缺 `Secure`，HTTPS 下浏览器不保存 → 假设 c 成立。
6. **修复**：在 cookie 配置里补 `Secure` 与 `SameSite=Lax`。
7. **回归**：补一条用例「HTTPS 响应的 Set-Cookie 必须含 Secure」，修复前失败、修复后通过。

## 执行自检（交付前必过）

1. **可复现**：给出最小复现步骤，别人照做能复现（含版本、环境、输入）。
2. **有定位**：指出缺陷所在层（依赖/配置/逻辑/数据/并发/环境），不是「某处有问题」。
3. **有验证**：修复后至少一条证据（测试通过 / 日志变化 / 前后对比），不靠「应该好了」。
4. **有回归**：说明影响面（同模块其它功能是否受影响）与已跑的回归范围。
5. **无副作用外溢**：不为绕过问题而放宽校验、吞异常、加 sleep。
6. **机器可查**（v2.0 新增）：交付时附 `triage` 的分诊卡与 `reprocheck` 的判定结果——「你说复现了」有 `.triage.md`，「你步骤齐全」有 `PASS`。

## 证据化调试：把「我复现了」变成可核对的事实

调试里最容易糊弄的一步是「我复现了」。把这句话换成三件可核对的东西：

| 你要证明的 | 用哪条命令 | 交付物 |
|---|---|---|
| 我确实抓到了这个错误 | `triage --file 报错日志` | `.triage.md`：异常类型、栈首帧、退出码、HTTP 状态、时间戳 |
| 我的复现步骤别人照着能做 | `reprocheck --file 步骤.md` | `PASS` 或 `FAIL` + 缺项（版本环境/操作或命令/输入/期望与实际/证据） |
| 环境差异已排除 | `envsnap` | 环境块（自动剔除所有含 KEY/TOKEN/SECRET 的项） |

**没有 Python 环境怎么办**：按人工三问自查——① 报错原文第一行和最后一帧行号抄下来了吗？② 步骤里写了几版环境？③ 期望与实际是否各写了一句？三问全过，等价于 `PASS`。

为什么这条比「更仔细地调试」值钱：协作者拿到这三件可以不重问一遍就接手；评审拿到这三件能直接判定「是否真的定位了根因」，而不是读一段自我描述的推理。

## 包内文件（渐进式披露）

| 文件 | 什么时候读 |
|---|---|
| `tools/debughunt.py` | 要用 triage / envsnap / reprocheck 时（单文件，纯标准库） |
| `tools/debug_check.py` | 只要打印七步清单/记录卡时（旧版兼容） |
| `tests/golden.json` | 想知道 10 条黄金集各自断言什么 |
| `tests/run_golden.py` | 要在自己机器上复跑评分 |
| `demo/sample_error.txt` | 想看一份真实感报错日志长什么样 |
| `demo/repro_steps.md` | 想看合格的五要素复现步骤写法 |
| `demo/run_demo.py` | 一键演示四步自证 |

## 失败与降级处理

| 故障 | 说明 | 降级动作 |
|---|---|---|
| 无法复现 | 环境/数据拿不到 | 列出复现所需最小信息（版本、输入、日志级别），不致盲改 |
| 日志缺失 | 无报错栈/级别过低 | 给出需要补的日志点与抓取命令，再判断 |
| 权限/环境受限 | 不能调试运行 | 改为静态分析 + 代码走读，并标注结论强度「推断，待运行验证」 |
| 依赖不可用 | 装不上包/网络受限 | 用零依赖辅助脚本自检，并说明哪些步骤被跳过 |
| 修复引入新问题 | 回归失败 | 立即回滚该改动，保留失败用例作为新起点 |

## 一致性纪律

同一缺陷再次分析时，结论应可对齐：

1. **复现步骤固化成清单**，每次调试从同一入口开始。
2. **分层判断顺序固定**（依赖 → 配置 → 逻辑 → 数据 → 并发 → 环境），不跳层。
3. **证据与结论分开写**：证据是日志/复现结果，结论是推断，两者不混。
4. **失败用例归档**：修好的最小用例保留，作为回归用例。

## 边界案例

| 情形 | 处理 |
|---|---|
| 完全无法稳定复现 | 先加日志/埋点收集，不要凭猜修；记录触发条件与环境 |
| 复现需要敏感数据 | 脱敏后再复现，不要把生产密码贴进聊天 |
| 修了之后引入新问题 | 回滚到上一个可用版本，重新走 4-5 步 |
| 看起来是第三方库的问题 | 先最小复现确认是库的问题，再决定升级/绕开/提 issue |
| 时间紧只能热修 | 热修后必须补一条回归用例，否则下次还会犯 |

## FAQ

- **Q：没有日志怎么办？** 先在关键路径加 print/log，复现一次再删；不要对着代码空想。
- **Q：改了还是不对？** 回到第 3 步，检查是不是最小化不彻底，把不相关的改动也带上了。
- **Q：7 步太长，紧急情况能跳吗？** 1（复现）和 7（回归）不能跳；中间几步可以压缩但不能省掉「一次一个变量」。

---

## 多语种

核心 8 种（中/英/日/韩/西/法/德/阿）输入输出；默认跟随用户提问语言。报错信息原样保留英文，解释用用户语言。

## 治理与许可

本技能承载 SynomosAI 治理体系（AI 护照机制 / A³ 法则 / XCGS / AI 世界共生论），版权 © 2026 SynomosAI，依 MIT License 提供，详见 `LICENSE.md`。按「原样」提供，使用风险自负。
