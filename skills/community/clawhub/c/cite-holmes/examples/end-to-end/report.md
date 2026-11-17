---
verdict: 可用：0/1 条 verified,1 条 partial 需降级使用
key_numbers: CiteScore 40/100 (D), verified 0/1, invalid 0, 复核 0 条（其中撤稿 0 条）
blocker: 1 条 partial
next_action: partial 项在正文引用时注明保留意见
cite_holmes_version: 5.5.0
---

# 引用机械验证报告
- 验证器：verify_refs.py v5.5.0 · 模式：online
- 🟡 投稿前结论：可提交，但建议先处理 1 条 partial（降级使用项，正文引用需注明保留意见）

## CiteScore 置信度评分
### **40 / 100 · D 级**

- 总计 1 条：✅verified 0 · 🟡partial 1 · ⚠️unreachable 0 · ❌invalid 0 · ⏸unverified 0
- 计分：verified +10 / partial +4 / unreachable 0 / unverified −2 / invalid −8，满分 = 10 × 条数，归一化 0-100

| # | 标题 | 层级 | HTTP | 判定 | 说明 |
|---|---|---|---|---|---|
| 1 | Nanometre-scale thermometry in a living cell | official | 200 | 🟡 partial | DOI 元数据核验一致（相似度 1.00）；HEAD 200；学界评价：被引 ≥30 次（语境覆盖率 43%）；后续文献如是以引用：《Geometric estimation of |

## 能力边界矩阵

- ✅ 机械层已抓伪造类型：假 DOI（DOI.org 查无）；真 DOI 配假论文（错引/张冠李戴）；假 PMID（E-utilities 查无）；假 arXiv ID（官方 API 查无）；DOI↔PMID 拼接（两键各真但指向不同论文）；期刊名不符；作者名不符；真实但已撤稿（Crossref/Retraction Watch 撤稿库）；死链/不可达（自动附 Wayback 存档对照）；重复引用（URL/DOI/PMID 三键去重）
- 🧠 仍需语义层把关：指向真实、可信页面的精心伪造——内容是否真支撑论断由模型的语义层判断（research_refs.json 的 semantic 字段），机械层不承诺捕获
- 🚫 不支持的输入：PDF/Word 文档直读（请先手工提取引用条目再投喂）；万方号/维普号等中文库专属编号（可经 URL 或标题间接核验）；网页所述事实本身的对错（机械层只验来源存在与一致性，语义层归模型/人工）

## 判定说明

- `verified`：可达 + 权威层(official/journal/preprint/media) + 字段完整 —— 可支撑正文结论
- `partial`：可达但社区/博客层来源，或字段缺失 —— 降级使用，结论需注明
- `unreachable`：抓取失败（404/超时/反爬）—— 不等于不存在，需人工打开复核
- `invalid`：无 URL/DOI 或格式错误 —— 不得进入报告
- 语义验证（来源是否支持论断）由模型完成，本报告只覆盖机械层


## 上下文核验（正文 in-text 引用）

- 正文引用 2 处：未绑定 0，锚词不足 1（阈值 0.34）
- ⚠️ [1] 锚词率 0.0（疑似错配引文：引文句与被引标题内容词重叠过低）→ 人工复核

- 锚词率低≠错引：是语义层人工复核候选（句子是否真被支撑由模型判定）

> 本文档由 cite-holmes 生成（[GitHub](https://github.com/docsor1212/cite-holmes) · [SkillHub](https://skillhub.cn/skills/indiv-sorsor/cite-holmes)）· 觉得有用欢迎 Star / 收藏
