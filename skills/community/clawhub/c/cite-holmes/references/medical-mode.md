# 医学研究模式（MEDICAL 模式必读）

> **30 秒导航**：医学证据模式——信源金字塔、CEBM 分级、监管信源清单、--profile medical 与 --easy 的关系；临床决策引用前必读。

> **30 秒入口**：何时读我——临床/医学问题核验前。最短路径：抄「信源金字塔」+ PubMed 检索式，然后 `--profile medical --easy` 一把跑。回 [INDEX.md](INDEX.md)。


适用触发：临床问题、药物疗效/安全性、疾病患病率、诊疗指南、诊断标准、
meta 分析、循证检索、医学文献综述。拿不准是否算"医学"时：凡涉及患者
治疗决策的一律按医学模式处理。

## 启用方式

检索阶段照常（菱形扩展 + 双语矩阵），验证阶段加参数：

```bash
python scripts/verify_refs.py --refs research_refs.json --profile medical --export bibtex,csv
```

## 与通用模式的四点差异

1. **期刊层域名扩展**：Cochrane Library、BMJ Best Practice、Embase、
   ClinicalTrials.gov、ChiCTR、NMPA、CDC/中国疾控、NICE、万方、医脉通指南
   在医学模式下计入权威期刊层。
2. **社区层降级警示**：知乎/微博/公众号/维基/博客层来源自动标注
   "不得支撑医学结论（仅作线索）"——医学主张的引用底线比通用问题更高。
3. **PMID 存在性核实**：PubMed 网页对不存在的 PMID 也返回 2xx，HTTP 检查
   抓不住编造的 PMID。验证器经 NCBI E-utilities 逐条核实 PMID 真实存在。
   引用登记时 pmid-only 条目可直接写 `{"pmid": "36443570", ...}`，无 url/doi
   也能验证（自动解析为 PubMed 页面）。
4. **台账导出**：`--export bibtex,csv` 产出 verified-only 参考文献（BibTeX，
   直接导入论文管理器）+ 全量审计台账（CSV，Excel 打开）。

## 医学信源金字塔

| 层级 | 首选来源 | 用法 |
|---|---|---|
| 系统评价/Meta | Cochrane Library；PubMed 上的 SR/MA（`systematic[sb]` 过滤） | 可直接支撑疗效结论 🟢 |
| 临床指南 | WHO、NICE、中华医学会各分会、国家卫健委、UpToDate / BMJ BP | 支撑诊疗规范类结论 🟢 |
| 原始研究 | PubMed / Embase（RCT > 队列 > 病例系列）；知网/万方/维普（中文） | 按研究设计定 🟢/🟡 |
| 预印本 | medRxiv / bioRxiv | 只标 🟡 并注明"未经同行评审" |
| 权威媒体 | Reuters、丁香园（资讯级） | 背景信息，不作疗效证据 |
| 社区/社交 | 知乎、微博、病友群、公众号 | 仅作线索，禁止支撑任何医学结论 🔴 |

## 检索式要点（PubMed）

- MeSH 主题词 + 自由词组合：`("Tocilizumab"[Mesh]) AND ("Arthritis, Juvenile"[Mesh] OR sJIA)`
- 疗效问题加过滤：`AND (randomized controlled trial[pt])`；病因/患病率换相应过滤
- 中英双语：英文 PubMed，中文知网/万方，两边合并去重（验证器按
  URL/DOI/PMID 自动去重）
- 双源规则在医学场景升级：**疗效结论需 ≥1 个系统评价或 ≥2 个独立 RCT**；
  仅有病例系列支撑的疗效主张标 🟡 并明示证据等级

## 监管与注册信源

- 药械批件/说明书：NMPA（中国）、FDA、EMA
- 临床试验注册：ClinicalTrials.gov、ChiCTR（中国临床试验注册中心）
- "某药是否获批某适应证""某试验是否注册"类事实，优先用监管/注册源核实——
  这类事实比文献更容易被 AI 编造，且编造得最像真的

## 证据分级对照

本 skill 的置信度标记与 CEBM 2009 证据等级的大致映射：

| 标记 | CEBM 等级 | 典型来源 |
|---|---|---|
| 🟢 | 1a–2b | SR/MA、高质量 RCT、官方指南推荐 |
| 🟡 | 3–4 | 队列/病例对照/病例系列、单个专家意见 |
| 🔴 | 5 或存疑 | 传闻、社区层、利益相关方声明、来源冲突 |
