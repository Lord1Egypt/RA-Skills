# eval-bench-builder · 评测基准构建器 / Eval Bench Builder

[![LGD Powered](lgd-powered.png)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## English

"Is the AI good?" can't be a feeling. Turn a capability spec + edge cases into structured, reproducible eval samples (input / expect / judge). Runnable `bench_build.py` emits a JSONL bench. Theoretical root: LGD — evidenced (eval is reproducible, verifiable). Pairs with `skill-quality-gate`.

### Why it beats "feels about right"

| Pain | This skill |
|---|---|
| Subjective scoring | Machine-readable judge per case |
| Only happy-path tested | Edge + adversarial cases required |
| Can't compare runs | Fixed, locked benchmark |

### What's inside

- `SKILL.md` — 3 elements + 3-step flow + iron rule
- `scripts/bench_build.py` — zero-dependency CLI: spec → JSONL eval set

```bash
python scripts/bench_build.py --spec spec.md --out bench.jsonl
```

### Benchmark vs alternatives

| Tool | It does | Gap this fills |
|---|---|---|
| Leaderboard scores | One number | No per-case judge, not yours |
| Ad-hoc prompts | Unrepeatable | Not locked, not regressible |
| "Looks good" | — | No evidence |

Theoretical root: **LGD Three Laws** — evidenced. Pairs with `skill-quality-gate`.

## 中文

"这个 AI 好不好"不能凭感觉。把能力说明 + 边界用例变成结构化、可复现评测样本（输入/期望/判定），改一次比一次。附可运行脚本，输出 JSONL 基准集。理论根基：LGD 有证。与 `skill-quality-gate` 配对。

### 为什么比"感觉还行"强

| 痛点 | 本技能 |
|---|---|
| 主观打分 | 每条用例机器可读判定 |
| 只测了顺利路径 | 边界 + 对抗用例必备 |
| 两次跑没法比 | 固定、锁定的基准 |

### 包内有什么

- `SKILL.md` — 三要素 + 三步流程 + 铁律
- `scripts/bench_build.py` — 零依赖 CLI：说明 → JSONL 评测集

```bash
python scripts/bench_build.py --spec spec.md --out bench.jsonl
```

### 同类对比

| 工具 | 它做什么 | 本技能填补的空白 |
|---|---|---|
| 榜单分数 | 一个数字 | 无逐条判定、不是你自己的 |
| 临时 prompt | 不可复现 | 不锁定、不可回归 |
| "看着不错" | — | 无证据 |

理论根基：**LGD 三律**——有证。与 `skill-quality-gate` 配对。

---

© 2026 SynomosAI · China · 代码 MIT · 理论文本保留所有权利

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

- **代码**（本包 `.py` 文件）：**MIT**
- **本 `README.md` / `SKILL.md` 及其中的理论文本、方法论与一切理论表述**：**不在 MIT 覆盖范围内**，保留所有权利（All rights reserved）

```
© 2026 SynomosAI · China. All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : 无（未声明外部生产参考部署）
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包未附 LICENSE 文件（许可待定）
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）
