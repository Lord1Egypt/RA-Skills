# 研究布局 vs 疾病负担对标方法学（JCE 2026 复用模板）

> 来源：*Journal of Clinical Epidemiology* 2026 —— 对 AI 干预性试验的「资源投入 vs 全球疾病负担」错配分析。
> 复用目的：给 `ct-registry` 的注册检索加一个**可复用**的「资源是否投向高负担领域」分析模板与图表输出。
> 本文件为方法学说明（本地、零联网），不含真实 GBD 数据——GBD DALYs 需由用户自备 CSV 输入。

## 1. 背景证据（JCE 2026）

- 2,771 个 AI 试验对标 GBD 病因谱。
- **log-log 斜率仅 0.31**：疾病负担每高 10 倍，试验量仅约高 2 倍（理想斜率≈1 表示资源随负担线性投放）。
- **56 / 160 个 GBD 病因零试验**，合计占全球 **14.4% DALYs**（其中腹泻病单项 5,650 万 DALYs、0 试验）。
- 2023 年 WHO 的 **GI-AI4H** 倡议之后**未观察到**向高负担病种重定向。

## 2. 三个复用指标

| 指标 | 定义 | 解读 |
|---|---|---|
| **log-log 斜率 β** | `log10(试验数_i)` 对 `log10(DALYs_i)` 的 OLS 斜率 | β≈1 资源随负担线性；β<1 高负担领域投入不足 |
| **错配比 mismatch** | 实际试验份额 `(T_i/ΣT)` 对负担份额 `(D_i/ΣD)` 的偏离；或 `T_i / 预测_T_i`（预测来自 β 拟合） | >1 超额投入；<1 投入不足 |
| **零试验病种占比** | `T_i=0` 的病因数 / 总病因数；及其合计 DALYs 份额 | 直接暴露"被忽视的高负担病种" |

## 3. 输入约定

- `--trials`：注册检索归一化结果（`normalized.json` 或聚合后的 `{etiology: trial_count}`）。
- `--dalys`：GBD 风格 CSV，列 `etiology,dalys`（或其它负担指标如 prevalence、mortality）。
- 病因对齐：试验的 `condition` 经 `references/term_map.json` 归一后映射到 GBD 病因；未匹配病因计入 `unmatched`。

## 4. 输出

- `burden_comparison.json`：β、各病因 mismatch、零试验清单、合计 DALYs 份额。
- `burden_comparison.png`（可选，需 `matplotlib`）：log-log 散点 + 拟合线 + 对角参考线（β=1）。

## 5. 局限与诚实披露

- 斜率为观察性关联，不证明因果；高负担低试验可能源于可行性（如罕见病数据稀缺），脚本须如实标注。
- GBD 年份与试验检索年份需对齐；年份错配须在输出 `_provenance` 声明。
- 零联网：GBD 数据不随技能内置，用户自备。
