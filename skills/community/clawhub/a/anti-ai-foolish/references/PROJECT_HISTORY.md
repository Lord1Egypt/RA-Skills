# 工程历史档案（原名：去AI-Harness 工程 → anti-ai-foolish）

一个规则即数据、引擎即代码、语料即测试床的去AI味工程。**1108条规则，1080条已在52个朱雀实测片段上完成A/B验证并回写状态**。

## 架构

```
（原始目录结构记录，现仓库即skill本身）
├── engine/
│   ├── harvest.py      # 从23个已装skill机器收割词表 → rules_pool.json（720唯一词条）
│   ├── gen_rules.py    # 规则池+内置定义 → rules/ 分库（1108条）
│   └── scanner.py      # 规则引擎：加载→剥信源→豁免→扫描→报告+Z分
├── rules/              # 13个分库（规则即数据，JSON）
│   R_标点(25) R_句法(71) R_内容在场(35)
│   R_词表*(849条：unclecheng338/libai222/网文166/程式77/模板词54/书面腔49/人味指南36/踩雷7)
│   R_豁免用户指纹(13) R_工程纪律文体(15) + INDEX.json
├── validation/
│   ├── corpus/zhuque_corpus.json   # 52片段朱雀标签语料（21份报告OCR）
│   ├── abtest.py       # 全量规则A/B验证 → 回写status
│   └── results/abtest_results.json
├── pipelines/
│   └── preflight.py    # 发文前一键快筛：6硬门+Z分+人味弹药 → 发/改/停
└── docs/               # 评估矩阵、学习报告（链接 skills-eval）
```

## 规则字段

每条规则：`id / name / category / pattern(正则) / mode(any|density) / threshold / severity / direction(AI|人味|警惕|meta) / status / evidence / fix / exempt_when / source`

**status 五态（诚实标注，由验证回写）**：
- `confirmed` — AI信号过95%CI（8条：冒号/冒号密度/编号后冒号/破折号OCR形/概念引用腔密度/疑问句密度/问号密度/词条"AI"）
- `reversed` — 人味信号过CI（10条：实际上/我说/可能/直接引语/真实地名/顶真/三连短语/叙事重复排比/对仗分句/词条"我说"）
- `directional` — 方向性未确证（13条，CI含0但|差|≥0.15）
- `no_signal` — 实测无信号（68条）
- `insufficient` — 语料覆盖不足（981条，多为书面套话词在评论文体不出现——**测不到≠证伪**，换文体可重验）

## 用法

```bash
# 扫描一篇文章（AI命中按危级分层，带修法与豁免提示）
python engine/scanner.py 文章.md

# 发文前快筛（6硬门 + Z分 + 人味弹药 → ✅可发/⚠️改后复检/❌停下手术）
python pipelines/preflight.py 文章.md

# 语料更新后重验证全量规则（新报告OCR进 corpus 后跑一次）
python validation/abtest.py
```

## Z分（发筛主力）

`Z = Σ确认AI规则命中 − Σ人味确认规则命中`。r=+0.813（52片段），固定规则集LOO稳定；Z>0判AI侧26/30、human侧11/12。**只能抓AI不能证人工**；机械上限≈0.8，剩余方差靠人工判据（经历我vs姿态我、人当主体、论证对称排比——见 docs）。

## 端到端验证记录（2026-09-16）

| 文本 | 朱雀实测 | preflight | 判定 |
|---|---|---|---|
| 文章一·张家齐（未手术） | 0.93 | Z=+2，门3/7 | ❌ 停下手术 ✓ |
| 文章二·枕头（未手术） | 0.91 | Z=+1，门3/7 | ❌ 停下手术 ✓ |
| 文章十四V7（手术后） | 待测 | Z=−2，门7/7 | ✅ 可发 ✓ |

## 知识来源（为什么是这些规则）

1. 52片段朱雀实测语料（本项目OCR 21份报告）——唯一"标准答案"级证据
2. 六变体消融实验（删结构-21.6/标点清零-34.3/词表-4.7）
3. 用户口述人类基线（李白54-72%）与语言指纹豁免体系
4. 微信五层信号模型（本工程管L1；发布纪律见 qu-ai-fingerprint）
5. 23个第三方skill规则库机器收割（含全部词表）

详见 `../skills-eval/规则AB测试评估矩阵.md`、`../skills-eval/朱雀语料学习报告.md`、`../skills-eval/@custom/qu-ai-fingerprint/SKILL.md`（方法论层，与本工程互补）。

## 维护

- 新朱雀报告 → OCR进 `validation/corpus/`（复用 skills-eval/zhuque_corpus 流水线）→ 跑 `abtest.py`，全部status自动重估
- 新skill想纳入 → 词表文件放好 → 重跑 `harvest.py` + `gen_rules.py` + `abtest.py`
- 规则修法建议（fix字段）人工维护；豁免清单以用户口述实测密度为准
