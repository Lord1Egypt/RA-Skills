# Sample-Size Justification Templates / 样本量论证段落模板

> ct-update upgrade J2（2026-09-29）。实现：`scripts/justify_text.py`（纯标准库、
> 零联网、规划层文本生成）；本文件说明骨架来源与使用约束。SKILL.md 入口：
> `--justify`（计算后自动附加，n 自动填充）或独立预览
> `python scripts/justify_text.py --test <t> [--mcid … --sd … | 参数…]`。

## 骨架来源（逐句可追溯，非第三方模板拷贝）

| 结构 | 用途 | 出处 |
|:---|:---|:---|
| **CONSORT-SPIRIT Item 14 + DELTA2 Box 4** | 英文段落语序：主要终点→α/power→目标差值按终点类型（连续=自然尺度+共同SD+标准化d；二分类=绝对/相对+两组率；生存=HR+事件率+随访+入组）→分配比→公式/软件+脱落校正→敏感性→差值依据 | consort-spirit.org item16a-samplesize；Delta 报告清单（Cook et al.） |
| **CDE《药物临床试验样本量估计指导原则（试行）》**（2024-12-23 发布施行） | 中文口径：试验设计→检验水准与效能→统计方法假设→预期治疗效应及**变异的参数设置依据**→样本量调整与监管沟通 | CDE 通告（药监综药管〔2020〕9号程序发布） |
| **ICH E9** | α/power 惯例表述（0.025/0.05、0.8/0.9） | ICH E9 §4.1–4.2 |

## 设计变体（`_VARIANTS` 按 test 自动选）

1. **优效-连续/比例**（ttest/anova/proportion/roc 等）——MCID 叙事的主要承载
2. **非劣效/等效**（non_inferiority/equivalence/be_tost/ni_survival 等）——界值=临床-监管假设，强制暴露"保留对照疗效%"推导占位
3. **生存/事件驱动**（survival 系/gsd_survival 等）——事件数驱动叙事 + 入组-随访计划 + 事件率敏感性预设规则
4. **通用回退**（其余 test）——最小六要素单段

## MCID 联动（J1）

`--mcid <Δ原始单位> --sd <SD> [--mcid-source "anchor:/distribution:/expert: …出处"]`：
- 折算 d = MCID/SD（复用既有 Δ/sd 通道），输出回显折算过程与依据声明
- `--audit` 下 MCID 有来源声明 → 效应量假设升 known；未声明 → 仍按启发式判 weak/unknown
- MCID 三流派提示：anchor-based（临床锚定，如 PASS cut-point）/ distribution-based（如 0.5×SD，Jaeschke 等）/ expert-consensus；分布法数值恰为 0.5×SD 时仍属"拍值"嫌疑，需 anchor 佐证

## 使用约束（写死在输出横幅里）

- 段落是**可审计骨架不是成品**：所有 `[__填写]` / `___` 占位（依据引用、机构信息、
  不等分配理由、随访月数等）必须由研究者填实后提交——anti fake-precision。
- 不替代监管沟通：NI 界值、借用对照、样本量调整等按 CDE 指导原则应在方案定稿前
  与药审中心沟通（§五（五））。
- n 自动填充时按引擎返回字段判定口径（`n_per_group`→"per group/例/组"；
  其余→"in total/例"）。
- **引擎声明口径（2026-09-29 修订）**：段落中的软件环境渲染为 `R <版本号> +
  rpact <版本> + TrialSize <版本>`——版本取自计算信封 `repro.r_version/packages`
  并透传进 meta；**不标注云端/本地**（对监管文书无意义），mock 版本视同缺失渲染
  为占位由研究者按 `sessionInfo()` 填实。
- **默认隐藏**：`--justify` 不默认开启；单次计算成功后主流程输出一行提示
  （i18n key `offer.justification`），用户确认后加 `--justify` 重跑生成段落。
