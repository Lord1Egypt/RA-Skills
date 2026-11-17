---
name: cn-med-oa
version: 2.4.1
author: DoctorQ Lab
license: MIT
platforms: [linux, win32, darwin]
description: >
  中文医学文献开放获取(OA)检索下载与引用验证套件。通过维普OA平台(oa.cqvip.com)免登录、
  免费检索中文医学期刊并下载 PDF 全文；输出完整 Vancouver/GB-T7714 元数据（标题/作者/期刊/
  年/卷/期/页/DOI/ISSN/CN刊号/摘要/关键词/基金/分类号），可直拼参考文献行；内置相关性守门
  （防平台OR匹配捞回无关结果）与五态引用验证器 verify_cn_refs（防AI幻觉引用，判定语义与
  pubmed-verifier 一致）。SQLite缓存/重试退避/日配额/控频，零依赖纯标准库。
  触发词："下中文文献"、"找中文文献"、"中文医学文献下载"、"找OA版"、"开放获取"、"免费下载论文"、
  "国内指南共识解读"、"找参考文献"、"中文文献支撑"、"补中文引文"、"验证中文引用"、"核查中文文献"、
  "下载维普文献"、"找几篇中文的"、"写文献综述要中文参考"。
  英文："download chinese paper"、"find OA chinese literature"、"verify chinese citations"。
  即使用户只说"帮我下载这篇中文文献"或"找几篇类风湿的中文论文"也应触发。
---

# cn-med-oa：中文医学文献 OA 检索下载 + 引用验证套件

两个工具，覆盖"获取"与"验证"两半：

| 工具 | 职责 |
|---|---|
| `scripts/cn_med_oa.py` | 检索 + PDF 下载 + Vancouver 元数据 + 相关性守门 |
| `scripts/verify_cn_refs.py` | 五态引用验证（中文版 pubmed-verifier，判定语义一致） |

数据源（双源架构 v2.1）：
1. **维普 OA 平台**（大家·维普期刊OA出版平台 oa.cqvip.com）：期刊文献主源，免登录免费
2. **中华医学期刊全文数据库 yiigle.com**（CMA 系期刊 + 官方指南）：补维普不覆盖的中华医学会核心刊与指南全文；指南/共识类查询自动优先该源

> 双源路由：普通文献查询 → 维普优先；查询含「指南/共识/规范/专家建议」→ yiigle 优先（CMA 官方指南权威源）。前一源无结果自动降级下一源。

> ## 🔎 用什么词搜索（速查）

1. **用规范医学术语**：期刊标题用规范名——「类风湿关节炎」而非「类风湿」，「心肌梗死」而非「心梗」。
2. **一次一个短语**：平台是 OR 匹配，多词互相污染；「类风湿 尿酸高」要拆两次查。
3. **指南/共识直接写类型词**：`--query 痛风 --doc-type 指南`（自动优先中华医学会源）。
4. **口语词拿不准**：`--suggest-terms "你的词"`——内置口语→规范术语映射与歧义提示，纯本地即时返回。
5. **查不到≠没有**：中华系核心刊多数不在 OA 库（仅元数据或指南例外）；平台无「无结果」信号，守门会滤掉不相关项。

## ⛔ 铁律（零例外）
> 1. **不瞎编瞎下**：只输出真实检索结果；下载的 PDF 必须真实存在且可打开；页码/卷期拿不到就如实标"缺失/待核对"，绝不猜一个填上（唯一例外：DOI 正则猜测会显式标记 `vol_source=doi_guess` 且 `needs_human_check=true`）。
> 2. **相关性透明**：平台是 OR 匹配语义，无关结果会被捞回。守门只标记不隐藏——disclosure 必须如实写"⚠️ N 条相关性存疑"。
> 3. **不碰付费/登录墙**：只取 OA 文献。中华医学会系期刊（中华内科杂志等）在登录墙内，本 skill 不覆盖，如实告知用户。
> 4. **控频+配额**：下载间隔 ≥3s（`CN_MED_OA_INTERVAL`），日下载上限默认 50（`CN_MED_OA_DAILY_MAX`，sqlite 跨进程计数）。
> 5. **先确认检索词**：引导用户用规范医学单短语（"类风湿关节炎"而非"关节发炎"）；多词查询守门会拦截并建议拆分。

## 架构

```
用户(关键词) ──► cn_med_oa.fetch_cn_oa()
                  ├─ 维普检索(search) ──► 候选 rows
                  ├─ 相关性守门(覆盖率制: ok≥0.80 / low≥0.50，ok优先选片)
                  ├─ 详情(detail, SQLite缓存30天) ──► Vancouver + 卷期(objectInfo.vol/num 权威源)
                  ├─ 下载(previewPath→fileBrowsing, 节流+日配额+PDF缓存去重)
                  └─ PDF后处理(页眉卷期交叉验证 + 页脚页码提取 + sha256)
                  ──► cn_refs.json (manifest) + disclosure + GB/T 7714 引用行

cn_refs.json / 手写引用 ──► verify_cn_refs.verify_entry()
                  ├─ id 回查维普详情（无 id 按标题检索解析）
                  ├─ 标题双重模糊匹配（中文bigram Jaccard + 字级Sequence）
                  ├─ 作者/期刊/年份交叉比对
                  ├─ PDF 首页标题窗口匹配（检测"下错文件"）
                  └─ 卷期三方一致性(objectInfo vs PDF页眉 vs DOI正则)
                  ──► 五态判定 + report.html / report.json
```

## 快速开始

```bash
# 1. 检索 + 下载 PDF（主用法）
python scripts/cn_med_oa.py --query 类风湿关节炎 --field title --max 5 --out-dir ./cn_refs --citation
# 双源筛选：只要 2024+ 的指南类
python scripts/cn_med_oa.py --query 痛风诊疗指南 --doc-type 指南 --year-from 2024 --max 5
# 数据源健康探测 / 人工下载闭环
python scripts/cn_med_oa.py --query x --health
python scripts/cn_med_oa.py --query 强直性脊柱炎指南 --out-dir ./cn_refs --pending-downloads
python scripts/cn_med_oa.py --query x --out-dir ./cn_refs --complete-downloads
# RIS 导出（EndNote/NoteExpress/Zotero 直接导入）
python scripts/cn_med_oa.py --query 强直性脊柱炎 --out-dir ./cn_refs --export-ris
# 批量模式：每行一个检索词（支持 # 注释），逐条检索+汇总+合并 manifest/RIS
python scripts/cn_med_oa.py --batch titles.txt --max 3 --out-dir ./cn_refs --export-ris

# 2. 仅元数据（快速，不消耗下载配额）
python scripts/cn_med_oa.py --query 痛风 --field keyword --max 10 --no-pdf

# 3. 验证 manifest 里的引用（五态判定）
python scripts/verify_cn_refs.py --manifest ./cn_refs/cn_refs.json --output report.html

# 4. 验证手写/AI生成的中文引用（无id也能按标题解析）
python scripts/verify_cn_refs.py --claims '[{"title":"类风湿性关节炎滑膜细胞的病理机制及精准靶向治疗策略","journal":"浙江医学","year":"2026"}]'

# 5. 严格模式：卷期页有缺口也算不通过（CI 用）
python scripts/verify_cn_refs.py --manifest cn_refs.json --strict
```

检索字段：`title`(题名,默认) `keyword`(关键词) `subject`(主题) `author`(作者) `journal`(刊名) `inst`(机构) `fund`(基金)

### Python API
```python
from cn_med_oa import fetch_cn_oa
r = fetch_cn_oa(query="类风湿关节炎", field="title", max_results=5,
                save_dir="./cn_refs", want_pdf=True, min_relevance="low")
r["final_status"]   # full | metadata_only | low_relevance | not_found
r["files"][0]       # 见下方 schema
r["disclosure"]     # 人类可读来源标注

from verify_cn_refs import verify_entry
verdict = verify_entry({"id": "7203426125", "title": "...", "journal": "浙江医学", "year": "2026"})
# verdict["verdict"] ∈ correct | mismatch | partial | invalid | unconfirmed
```

## 输出 schema（cn_refs.json → files[]）

```json
{"path": "...pdf", "sha256": "...",
 "title": "类风湿性关节炎滑膜细胞的病理机制及精准靶向治疗策略",
 "authors": ["郑凤钰","黄佳丽","杨玲","陈勇"], "journal": "浙江医学", "journal_en": "Zhejiang Medical Journal",
 "year": "2026", "volume": "48", "issue": "7", "pages": "770-774",
 "vol_source": "api", "vol_consistent": true, "needs_human_check": false,
 "doi": "10.12056/...", "issn": "1006-2785", "cnno": "33-1109/R", "publisher": "浙江省医学会",
 "abstract": "...", "keywords": ["滑膜成纤维细胞"], "fund": ["浙江省中医药科技计划项目(2025ZL119)"],
 "classno": ["R593.22"], "cnki_uri": "https://kns.cnki.net/...",
 "relevance": {"score": 0.8, "state": "ok", "coverage": 0.8, "note": ""},
 "source": "WeipuOA", "license": "OA", "id": "7203426125", "lngid": "7203426125"}
```

直拼引用行（`--citation`）：
> 郑凤钰、黄佳丽、杨玲等. 类风湿性关节炎滑膜细胞的病理机制及精准靶向治疗策略[J]. 浙江医学, 2026, 48(7): 770-774. DOI:10.12056/...

**卷期页可信度分级**（P0-1 修复核心）：`vol_source=api`（维普 objectInfo 权威字段，已实测正确）> `pdf`（页眉"第N卷第M期"）> `doi_guess`（DOI 正则猜测，仅当上两者缺失，**必带 needs_human_check=true**）。页码提取自 PDF 页脚"· NNN"模式，部分期刊文本层无页码 → `pages=""` 且验证器标"页码缺失"。

## 五态判定语义（与 pubmed-verifier 一致）

| 判定 | 含义 | 触发条件 |
|---|---|---|
| ✅ correct | 文献真实且元数据匹配 | 标题匹配 且（作者或期刊匹配） |
| ⚠️ mismatch | 文献存在但指向**另一篇**（AI幻觉最常见） | 标题/作者/期刊均不符；或 PDF 首页标题不匹配 |
| 🔶 partial | 部分匹配 | 标题对但作者期刊都不符，或作者期刊对但标题不同 |
| ❌ invalid | 平台查无此文献 | id 与标题检索均未命中（编造引用） |
| ❓ unconfirmed | 无法交叉比对 / 卷期页缺口(--strict) | 声称元数据不足；strict 模式下有缺口 |

模糊匹配为 pubmed-verifier 双重策略的**中文自适应版**：词级 Jaccard 的 token 集 = 英文词 + 中文相邻二元组（原版按空格分词对中文失效）；字级 SequenceMatcher 直接兼容中文。

## 覆盖边界（诚实声明）

- ✅ **能下全文**：维普 OA 收录期刊（省级医学会刊、临床研究、指南**解读**文章等，千万级 OA 文献）。实测 10 主题×10 条 PDF 可得率 100%。
- 🟡 **仅元数据**：非 OA / 知网万方独家 → 返回元数据 + `cnki_uri` 知网落地页指引。
- ❌ **不覆盖**：①中华医学会核心刊（中华内科/风湿病学/医学杂志等——登录墙，实测刊名检索 0 命中）；③英文文献请用 paper-to-story 的 fulltext_connector（PMC/Unpaywall）。
- 🟢 **例外（v2.3.1）**：CMA 期刊上的指南/共识若在 yiigle 被标为 OA 商品（如《新一代四环素类抗生素儿科应用临床实践指南（2026版）》），可匿名直下**官方排版 PDF**；非 OA 指南仍走 `--pending-downloads` 浏览器兜底。
- ⚠️ **检索语义**：平台是 OR 匹配，无"无结果"信号（"量子纠缠炒股"也返回 20 条）。守门按覆盖率过滤，负例实测全部拦截；多词查询请拆分为单短语。

## eval 基线（eval/run_eval.py，2026-08-14）

| 指标 | 结果 |
|---|---|
| 检索 recall（26 正例） | 100% |
| 相关性精度硬断言（条目级，v1 盲区） | 100% |
| 负例拦截率（3 负例：乱词/无关/多词） | 100% |
| 卷期权威源(api)占比 | 100%（73/73） |
| Vancouver 完整率（5 字段） | 97% |
| 下载成功率 / 内容匹配率 | 100% / 100%（24/24） |
| 页码提取率 | 21%（期刊 PDF 文本层差异，缺失时如实标注） |

回归：`python eval/run_eval.py --quick`（全量，仅元数据）；`--limit 8`（含下载抽样，注意日配额）。

## 与生态的关系

- **pubmed-verifier**（同作者生态）：英文 PMID 引用验证。本 skill 的 verify_cn_refs 是其中文对偶——判定语义、阈值哲学、报告风格一致，pipeline 可组成双通道验证 Gate（英文→PMID，中文→维普回查）。移植部分：重试退避、SQLite 缓存、双重模糊匹配（已做中文 bigram 兼容改造，阈值体系不同：那边是等长标题比对用 Jaccard≥0.5，这边是短查询vs长标题用覆盖率制）。
- **paper-to-story / immuno-article-pipeline**：可作为中文文献支撑的获取层（本文档发布时**尚未接线**，集成方式见 README"集成"节）。

## 合规

仅取 OA 文献（平台定位即开放获取）；下载控频 ≥3s + 日配额 50；robots.txt 未设限但遵守 ToS，不做批量轰炸；零凭证零 PII，无第三方网关中转。API 契约与踩坑记录见 `references/weipu-oa-api-contract.md`。

## 环境变量

| 变量 | 默认 | 说明 |
|---|---|---|
| `CN_MED_OA_INTERVAL` | 3.0 | 下载间隔秒数 |
| `CN_MED_OA_DAILY_MAX` | 50 | 日下载配额（sqlite 跨进程） |
| `CN_MED_OA_META_TTL` | 30 | 元数据缓存天数 |
| `CN_MED_OA_CACHE` | ~/.cache/cn-med-oa | 缓存目录 |
| `CN_MED_OA_VERIFY_SSL` | 0 | 置 1 开启 SSL 证书校验 |

## 文件结构

```
cn-med-oa/
├── SKILL.md                          # 本文件
├── README.md                         # 发布说明(SkillHub/ClawHub)
├── skillhub-meta.json                # 发布元数据
├── scripts/
│   ├── cn_med_oa.py                  # 检索下载连接器 v2.0.0 (~600行, 纯stdlib)
│   └── verify_cn_refs.py             # 五态引用验证器 v1.0
├── eval/
│   ├── golden.jsonl                  # 26正例+3负例(乱词/无关/多词语义)
│   └── run_eval.py                   # 回归评测 v2
└── references/
    └── weipu-oa-api-contract.md      # 维普OA API契约(逆向实测+踩坑)
```

## 🔒 安全与行为声明

- 网络访问仅限两个数据源：`oa.cqvip.com`（维普 OA）与 `yiigle.com`（中华医学期刊全文数据库）；SSL 证书恒校验，不提供关闭选项。
- 本地只写入两类位置：`--out-dir` 指定的下载目录与 `~/.cache/cn-med-oa` 元数据缓存；无遥测、无后台上报。
- 零第三方依赖，纯 Python 标准库；不创建进程、不读写系统敏感目录、不请求任何系统权限。
- `--suggest-terms` 为纯本地词表映射，不发任何网络请求。

## 版本历史

- v2.4.0 (2026-09-22) — 「检索词助手+白话报错」（评测 4.8：R「报错专业看不懂」/C「缺用什么词搜索速查」/E「检索词须规范」三维同治）：
  - **`--suggest-terms`**：口语→规范术语映射（22 组高置信词条+2 组歧义词消歧提示，纯本地零网络）；多词查询自动建议拆单短语（平台 OR 匹配）
  - **空结果自动给对策**：常见原因四条+可复制命令；网络失败自动附白话层（发生了什么/能做什么）
  - **SKILL.md 新增「用什么词搜索」速查与「安全与行为声明」**；数据源注记补中华医学期刊网官方域名 medjournals.cn
  - 风险清扫收尾：评测/测试工件移出发布源目录（发布源目录=包边界）

- v2.3.1 (2026-09-12) — yiigle 链路修复（实战发现：2026版四环素指南匿名可下却误判登录墙）：
  - **resource/auth 改回前端真实参数 `reduceTimes=true`**：`false` 时接口只返回 hasPerm 不签发 token，OA 商品（开放获取指南等）被误判为登录墙、永远走人工兜底；`true` 后匿名即可下载 OA 商品官方 PDF
  - **人工清单建议文件名改用文献标题**：原 `yiigle_源_序号.pdf` 与标题的模糊匹配 ratio≈0，`--complete-downloads` 永远匹配不上；改用标题命名（非法字符清洗，80字截断）
  - 实测：新一代四环素类抗生素儿科应用临床实践指南（2026版）匿名直下官方排版 PDF 2.8MB/19页成功
- v2.3.0 (2026-08-14) — 用户高频需求三件套：
  - **RIS/EndNote 导出**：`--export-ris` 一键导出 EndNote/NoteExpress/Zotero 可导入的 cn_refs.ris（TY/AU/PY/JO/VL/IS/SP/EP/DO/UR/L1 全字段）
  - **核心期刊标注**：⭐ 北大核心/CSCD 标注（内置高置信参考表 150+ 医学期刊，宁缺毋滥不误导，未收录不标注，以官方目录为准）
  - **批量任务**：`--batch titles.txt` 每行一个检索词（支持 # 注释），逐条检索+汇总报告+合并 manifest/RIS
  - 修复 Python 3.12 DeprecationWarning（unicode_escape 解码路径）
- v2.2.0 (2026-08-14) — 验证双源化 + 完整性增强：
  - **verify_cn_refs 双源**：维普未命中自动回退 yiigle（中华医学会系期刊可验证）；期刊感知解析（防同名解读文章顶替真文，优先级：期刊匹配维普行 > yiigle > 任意标题匹配）
  - **yiigle 详情补全**：ISSN/CN 刊号/英文刊名（rs.yiigle.com JATS 解析，SQLite 缓存）
  - **PDF best-effort + 人工兜底**：yiigle 三步下载链路（token→auth→download，匿名遇登录墙不硬闯）；`--pending-downloads` 生成人工下载清单 + `--complete-downloads` 扫描入库（标题模糊匹配+sha256）
  - **页码提取增强**：DOI 末段页码/页眉"第N卷第M期·NNN"多模式（原仅页脚·NNN）
  - **检索增强**：`--year-from/--year-to/--doc-type` 筛选 + DOI/标题双源去重
  - **`--health`** 数据源健康探测；**SSL 校验默认开**（三源证书实测有效，`CN_MED_OA_VERIFY_SSL=0` 可关）
  - eval：27 正例 + 2 负例全绿
- v2.1.0 (2026-08-14) — **双源架构**：新增 yiigle（中华医学期刊全文数据库）源，覆盖 CMA 系期刊与官方指南（维普不覆盖）；指南/共识类查询自动优先 yiigle；`sources` 参数可控制源优先级；eval 扩至 27 正例 + 2 负例全绿。
- v2.0.0 (2026-08-14) — P0/P1/P2 全修复：覆盖率制相关性守门（ok优先选片）、卷期权威化（objectInfo.vol/num 主源+PDF页眉交叉+DOI猜测显式标记）、页脚页码提取、SQLite 缓存（元数据 30d/PDF 去重）、重试退避、日配额、SSL 开关、五态验证器 verify_cn_refs、eval v2（负例/多词/条目断言/卷期源断言）。
- v1.0.0 (2026-08-14) — 维普 OA 三步下载链路逆向 + 基础 eval。已知问题（已于 v2 修复）：DOI 卷期正则误析（10.3969 前缀）、无相关性守门、无缓存。
