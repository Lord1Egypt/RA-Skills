# cn-med-oa — 中文医学文献 OA 检索下载 + 引用验证套件

[![eval](eval/)] 免费 · 免登录 · 零凭证 · 零依赖（纯 Python 标准库）

一个命令：检索中文医学期刊 → 下载 PDF 全文 → 输出可直拼的参考文献行；再一个命令：验证这些引用（或 AI 写的引用）是真是假、是否指对了论文。

## 为什么需要它

- 中文医学文献的免费获取长期被商业付费墙（10次/月试用）或登录墙（中华医学会系）把持。
- AI 写综述时最容易在**中文引用**上幻觉：编造标题、张冠李戴的卷期页、引用不存在的文献。
- 现有验证工具（如 pubmed-verifier）只认英文 PMID，中文引用无验证通道。

本 skill 一半解决"获取"，一半解决"验证"。

## 安装

```bash
# SkillHub / ClawHub 安装到 skills 目录即可（SKILL.md + scripts/ + eval/ + references/）
# 无需任何 API key、账号、邮箱绑定。唯一可选依赖：pymupdf（PDF 内容校验/页码提取）
唯一可选依赖 PyMuPDF：缺失时自动降级（跳过 PDF 内容校验），是否安装由使用者自行决定
```

## 快速开始

```bash
# 检索 + 下载 5 篇 + 输出 GB/T 7714 引用行
python scripts/cn_med_oa.py --query 类风湿关节炎 --out-dir ./cn_refs --citation
# ✅ 下载 5 篇全文
#    类风湿性关节炎滑膜细胞的病理机制及精准靶向治疗策略 | 浙江医学 2026;48(7) p=770-774
#    引用: 郑凤钰、黄佳丽、杨玲等. 类风湿性关节炎滑膜细胞的病理机制及精准靶向治疗策略[J].
#          浙江医学, 2026, 48(7): 770-774. DOI:10.12056/...

# 双源筛选 + 核心期刊标注：只要 2024+ 的指南类（自动路由 yiigle 优先）
python scripts/cn_med_oa.py --query 痛风诊疗指南 --doc-type 指南 --year-from 2024 --max 5
# ⭐中华内科杂志 2024;63(11) p=1059-1077 | doi=10.3760/...

# 导出 RIS（EndNote/NoteExpress/Zotero 直接导入）
python scripts/cn_med_oa.py --query 强直性脊柱炎 --out-dir ./cn_refs --export-ris
# 📄 RIS 已导出: ./cn_refs/cn_refs.ris（5 条）

# 批量模式：每行一个检索词（支持 # 注释），逐条检索 + 汇总
python scripts/cn_med_oa.py --batch titles.txt --max 3 --out-dir ./cn_refs --export-ris
# 1/3 [metadata_only] 2024中国类风湿关节炎诊疗指南 → 2 条
# 汇总: 3 条检索 | 命中 4 条 | full=0 metadata=2 low=0 not_found=1

# 数据源健康探测 / 人工下载闭环（登录墙 PDF 用浏览器下载后入库）
python scripts/cn_med_oa.py --query x --health
python scripts/cn_med_oa.py --query 指南 --out-dir ./cn_refs --pending-downloads
python scripts/cn_med_oa.py --query x --out-dir ./cn_refs --complete-downloads

# 验证引用（manifest 或手写 claims，五态判定；维普未命中自动回退 yiigle）
python scripts/verify_cn_refs.py --manifest cn_refs/cn_refs.json --output report.html
python scripts/verify_cn_refs.py --claims '[{"title":"某AI编造的中文标题","journal":"中华内科杂志","year":"2026"}]'
# ❌ 无效 —— 维普OA与yiigle均查无此文献
```

## 核心特性

| 特性 | 说明 |
|---|---|
| **免登录免费下载** | 维普 OA 平台开放接口（逆向实测的官方在线阅读链路），无凭证/无配额弹窗/无邮箱绑定 |
| **双源检索** | 维普 OA（省级医学会刊）+ yiigle（中华医学会系期刊/指南，ISSN/CN刊号补全）；指南类自动路由 yiigle 优先；DOI/标题双源去重 |
| **Vancouver/GB-T 7714 全字段** | 标题/作者/期刊/年/卷/期/页/DOI/ISSN/CN刊号/摘要/关键词/基金/分类号，直拼引用行 |
| **卷期可信度分级** | API 权威字段(vol_source=api) > PDF页眉 > DOI正则猜测(显式标记 needs_human_check) |
| **核心期刊标注** | ⭐ 北大核心/CSCD 标注（内置高置信参考表 150+ 医学期刊，宁缺毋滥不误导，未收录不标注） |
| **RIS 导出** | `--export-ris` 一键导出 EndNote/NoteExpress/Zotero 可导入的 cn_refs.ris |
| **批量任务** | `--batch titles.txt` 每行一个检索词（支持 # 注释），逐条检索+汇总+合并 manifest/RIS |
| **相关性守门** | 平台是 OR 匹配语义（无关词也返回结果），覆盖率制守门拦截并标记，负例拦截率 100% |
| **五态引用验证** | ✅正确/⚠️不匹配(下错或引用错)/🔶部分/❌无效(编造)/❓待确认——判定语义与 pubmed-verifier 一致；维普未命中自动回退 yiigle（中华系期刊可验证） |
| **PDF 内容验证** | 首页标题窗口匹配，能抓住"元数据对但下错文件"；sha256 去重 |
| **工程健壮性** | SQLite 缓存(元数据30天/PDF去重) · 重试退避(1s/2s/4s) · 日下载配额(默认50) · 控频3s · `--health` 双源探测 · SSL 默认校验 |

## eval 基线（2026-08-14 · v2.3.0）

| 指标 | 结果 |
|---|---|
| 检索 recall（27 个医学主题正例） | **100%** |
| 相关性精度（条目级硬断言） | **100%** |
| 负例拦截（乱词/无关词/多词语义塌陷） | **100%** |
| 卷期权威源占比 | **92%** (69/75) |
| Vancouver 完整率 | 97% |
| 页码提取率 | 21%* |

\* 部分期刊 PDF 文本层无页码页脚，提取不到时**如实标注"页码缺失"**而非猜测——这是设计原则：宁可留白待核对，不编数据。

回归测试：`python eval/run_eval.py --quick`（约 3 分钟，不消耗下载配额）。

## 覆盖边界（读我，重要）

- ✅ 维普 OA 收录期刊全文（省级医学会刊、临床研究、指南解读文章等）
- ✅ **中华医学会系期刊（yiigle 源）**：元数据 + ISSN/CN 刊号全字段；PDF 走浏览器下载（登录墙内不硬闯，best-effort 后给 download_url）
- 🟡 **原版 CMA 指南全文**——yiigle 内可在线阅读，自动下载受登录墙限制 → `--pending-downloads` 清单 + `--complete-downloads` 人工入库闭环
- 🟡 非 OA 文献 → 返回元数据 + 知网落地页指引（cnki_uri）
- 检索请用**规范医学单短语**（"类风湿关节炎"✓，"专家共识 风湿"会被守门拦截并建议拆分）
- ⭐ 核心期刊标注为**内置参考表**（非官方目录），可能滞后于最新版，以官方目录为准

## 设计原则

1. **不瞎编瞎下**：拿不到的字段留白+标记，绝不猜数据填坑。
2. **透明降级**：每个结果带 relevance 标记和 disclosure 来源说明，无关结果不隐藏只标记。
3. **获取与验证分离**：fetcher 只管拿，verifier 独立回查——和 pubmed-verifier 组成英文/中文双通道引用审计。

## 与其他工具的关系

- **pubmed-verifier**（推荐同装）：英文 PMID 引用验证。两者判定语义/阈值哲学/报告风格一致。
- **fulltext_connector**（paper-to-story skill）：英文 OA 全文获取（PMC/Unpaywall）。中英文各用各的。

## 集成到自己的 pipeline

```python
import sys; sys.path.insert(0, "<skill>/scripts")
from cn_med_oa import fetch_cn_oa
from verify_cn_refs import verify_entry

r = fetch_cn_oa("系统性红斑狼疮", max_results=5, save_dir="./cn_refs")
for e in r["files"]:
    if e["relevance"]["state"] == "ok" and e.get("path"):
        v = verify_entry(e)
        assert v["verdict"] == "correct"
```

## 合规

仅获取 OA（开放获取）文献；遵守平台服务条款；内置控频（≥3s）与日配额（50）防止滥用；零凭证设计，不收集任何用户信息。

## License

MIT


## 用什么词搜索？（速查）

| 你会说 | 该查的词 |
|---|---|
| 类风湿 | 类风湿关节炎 |
| 心梗 / 中风 | 心肌梗死 / 脑卒中 |
| 尿酸高 | 高尿酸血症（有痛风史直接查「痛风」）|
| 老慢支 | 慢性阻塞性肺疾病 |
| 小孩发烧 | 儿童发热 |

拿不准就问工具：`python scripts/cn_med_oa.py --suggest-terms "你的词"`（纯本地即时返回，含歧义词消歧与多词拆分建议）。记住两条：**一次只查一个短语**（平台是 OR 匹配）；**查不到≠没有**（中华系核心刊多数不在 OA 库）。
