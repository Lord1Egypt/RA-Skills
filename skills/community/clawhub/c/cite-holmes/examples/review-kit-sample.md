<!-- 样例来源：真实公开数据，非模拟。数据通路=PubMed E-utilities（题录）+ DOI.org/Crossref 注册库（判定）+ Semantic Scholar Graph API（被引数）。
复现命令：python3 scripts/verify_refs.py --discover "bronchiolitis infant diagnosis" --discover-limit 6 --discover-sort cited --review-kit --cn
生成：2026-10-24 真实运行产物（判定逻辑与当前版本一致；正文中的引擎版本号为生成时点快照）。被引数随时间自然增长、S2/OpenAlex 限流时个别条目显示「—」（诚实降级设计）——重跑数值略有差异属预期。 -->

# 文献综述工作台（review-kit）

- 主题：bronchiolitis infant diagnosis｜生成：2026-10-24（历史样例）
- 核验总览：共 5 条——✅ verified 5
- 判定语义：verified=官方注册库核验一致；partial=部分确认，引用前请人工过目；invalid=编造或错引（不得引用）；unverified/unreachable=未能核验（查无永不判死）

## 一、综述表格（verified 优先，同判定保持原序）

| # | 文献 | 年份 | 出处 | 被引 | 判定 |
|---|---|---|---|---|---|
| 1 | Comparative Efficacy of Bronchiolitis Interventions in Acute Care: A Network Meta-analysis. | 2021 | Pediatrics | — | ✅ verified |
| 2 | Australasian bronchiolitis guideline. | 2019 | J Paediatr Child Health | — | ✅ verified |
| 3 | Diagnosis and management of bronchiolitis. | 2006 | Pediatrics | — | ✅ verified |
| 4 | Incidental diagnosis of cardiac fibroma in an infant with acute viral bronchiolitis. | 2024 | Rev Paul Pediatr | 2（Semantic Scholar） | ✅ verified |
| 5 | Bronchiolitis: update 2001. | 2002 | Curr Opin Pulm Med | 27（Semantic Scholar） | ✅ verified |

## 二、标注书目

**[1] Comparative Efficacy of Bronchiolitis Interventions in Acute Care: A Network Meta-analysis.**  
ELLIOTT S A, GAUDET L A, FERNANDES R M，et al. — Pediatrics — 2021
  - 判定：✅ verified——DOI 元数据核验一致（相似度 0.99）；DOI↔PMID 交叉一致（两键指向同一论文）；HTTP 403（站点拒绝或页面不存在）；着陆页反爬（HTTP 403），但 DOI 注册元数据核验一致——存在性已确认；磁盘缓存命中（0h 前验证；--refresh-cache 强制重
  - DOI: https://doi.org/10.1542/peds.2020-040816
  - PMID: https://pubmed.ncbi.nlm.nih.gov/33893229/
**[2] Australasian bronchiolitis guideline.**  
O'BRIEN S, BORLAND M L, COTTERELL E，et al. — J Paediatr Child Health — 2019
  - 判定：✅ verified——DOI 元数据核验一致（相似度 0.99）；DOI↔PMID 交叉一致（两键指向同一论文）；HTTP 403（站点拒绝或页面不存在）；着陆页反爬（HTTP 403），但 DOI 注册元数据核验一致——存在性已确认；磁盘缓存命中（0h 前验证；--refresh-cache 强制重
  - DOI: https://doi.org/10.1111/jpc.14104
  - PMID: https://pubmed.ncbi.nlm.nih.gov/30009459/
**[3] Diagnosis and management of bronchiolitis.**  
Pediatrics — 2006
  - 判定：✅ verified——DOI 元数据核验一致（相似度 0.99）；DOI↔PMID 交叉一致（两键指向同一论文）；HTTP 403（站点拒绝或页面不存在）；着陆页反爬（HTTP 403），但 DOI 注册元数据核验一致——存在性已确认；磁盘缓存命中（0h 前验证；--refresh-cache 强制重
  - DOI: https://doi.org/10.1542/peds.2006-2223
  - PMID: https://pubmed.ncbi.nlm.nih.gov/17015575/
**[4] Incidental diagnosis of cardiac fibroma in an infant with acute viral bronchiolitis.**  
PIGOSSO Y G, FOGIATO I M, VIEIRA G G，et al. — Rev Paul Pediatr — 2024
  - 判定：✅ verified——DOI 元数据核验一致（相似度 0.99）；DOI↔PMID 交叉一致（两键指向同一论文）；HEAD 200；学界评价：被引 2 次（语境覆盖率 0%）；磁盘缓存命中（0h 前验证；--refresh-cache 强制重验）
  - DOI: https://doi.org/10.1590/1984-0462/2024/42/2022157
  - PMID: https://pubmed.ncbi.nlm.nih.gov/38808864/
**[5] Bronchiolitis: update 2001.**  
SCHLESINGER C, KOSS M N — Curr Opin Pulm Med — 2002
  - 判定：✅ verified——DOI 元数据核验一致（相似度 0.98）；DOI↔PMID 交叉一致（两键指向同一论文）；HEAD 200；学界评价：被引 27 次（语境覆盖率 30%）；后续文献如是以引用：《Recent advances in the management of acute bronchi
  - DOI: https://doi.org/10.1097/00063198-200203000-00006
  - PMID: https://pubmed.ncbi.nlm.nih.gov/11845006/

## 三、即贴参考文献表（GB/T 7714-2025，宁缺毋错：仅收 verified与元数据一致的 partial）

[1] ELLIOTT S A, GAUDET L A, FERNANDES R M, et al. Comparative Efficacy of Bronchiolitis Interventions in Acute Care: A Network Meta-analysis[J]. Pediatrics, 2021, 147(5). https://doi.org/10.1542/peds.2020-040816.
[2] O'BRIEN S, BORLAND M L, COTTERELL E, et al. Australasian bronchiolitis guideline[J]. Journal of Paediatrics and Child Health, 2018, 55(1): 42-53. https://doi.org/10.1111/jpc.14104.
[3] Diagnosis and Management of Bronchiolitis[J]. Pediatrics, 2006, 118(4): 1774-1793. https://doi.org/10.1542/peds.2006-2223.
[4] PIGOSSO Y G, FOGIATO I M, VIEIRA G G, et al. Incidental diagnosis of cardiac fibroma in an infant with acute viral bronchiolitis[J]. Revista Paulista de Pediatria, 2024, 42. https://doi.org/10.1590/1984-0462/2024/42/2022157.
[5] SCHLESINGER C, KOSS M N. Bronchiolitis: update 2001[J]. Current Opinion in Pulmonary Medicine, 2002, 8(2): 112-116. https://doi.org/10.1097/00063198-200203000-00006.

---
使用说明：partial/⚠ 条目引用前须人工核对；本表由机械核验生成，「核验一致」≠「支撑你的论点」——语义支撑请自行判断或用语境层（citation contexts）复核。复跑加 --refresh-cache 可强制重验。