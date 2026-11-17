# 能力边界 (Capabilities & Boundaries)

> 本文件由 `SKILL.md` 引用，集中定义 catalyst-search 的能力边界，便于每次输出前核查。
> Referenced by `SKILL.md`; defines catalyst-search's capability boundaries for pre-output checks.

## 可获取 | Obtainable
- ✅ 开放获取（OA Gold/Green/Hybrid）论文：经 WebFetch 可获取全文
  - Open-access (OA Gold/Green/Hybrid) papers: full text retrievable via WebFetch
- ✅ 付费墙内论文：可获取摘要、元数据、DOI（ScienceDirect/Elsevier/Wiley/Nature/Springer 等）
  - Paywalled papers: abstract, metadata, and DOI retrievable (ScienceDirect/Elsevier/Wiley/Nature/Springer, etc.)
- ✅ **仅凭摘要即可判断是否为目标文献**，无需下载或引用全文
  - **Abstracts alone are sufficient to judge relevance**; full-text download or citation is unnecessary

## 不可为 | Out of scope
- ❌ 不能"API 直连"批量下载付费墙内全文（需机构订阅凭证，本环境无）
  - Cannot "API-direct" bulk-download paywalled full texts (requires institutional subscription credentials, unavailable here)
- ❌ 不得编造文献；引用必须 WebFetch 实证 DOI/摘要
  - Must not fabricate literature; citations must be WebFetch-verified at DOI/abstract level
- ❌ 不提供催化剂设计建议（由 catalyst-design 负责）
  - Does not provide catalyst design advice (handled by catalyst-design)

## 与其他能力分工 | Division of labor
- 仅使用 WebSearch(academic) 与 WebFetch 两类通用工具能力
  - Uses only the two generic tools WebSearch(academic) and WebFetch
- 不内置、不复制任何其他专用检索工具的内部接口与字段定义
  - Does not build in or copy the internal interfaces/field definitions of any other specialized search tool

## 注意事项 | Notes
- 多重 AND 组合过苛易返回空，宜放宽或拆组
  - Over-strict AND combinations easily return empty; relax or split groups
- 输出末尾注明检索来源（开放网络）与可获取状态（已获取 / 在线 / 付费 / 手动）
  - Note search source (open web) and availability (obtained / online / paywalled / manual) at end of output
- 检索结果字段差异大，WebSearch 返回块需自行解析标题/作者/来源/年份
  - Search-result fields vary widely; parse title/authors/source/year from WebSearch blocks yourself
