# PDF 解析站点 profile —— Zotero 翻译器研读笔记（B 路线：当地图读）

- 日期：2026-10-27
- 素材：github.com/zotero/translators（master 快照，313 个翻译器）
  - 已复制到 `C:\Users\Wintone\WorkBuddy\_reference\zotero-translators`（AGPL-3.0，勿复制代码进 ct-literature / 任何发布物，只读参考）
  - 原始 tarball 备份：`ct-registry/_research/zt.tar.gz`

## 核心结论（指导 site_profiles.json + pdf_download.py 实现）

1. **Highwire 元标签是最大公约数**：绝大多数出版商 landing 页含
   `<meta name="citation_pdf_url">`。Zotero 的通用兜底 `Embedded Metadata.js`
   就是靠它覆盖全站长尾。→ 我们实现为通用 L1：`_extract_pdf_candidates()`。
2. **显式用 citation_pdf_url 的翻译器只有 7 个**（BioMed Central / Cambridge
   Core / Cairn 等），其余站点同样被 EM 兜底覆盖——证明"一份通用模板 > N 个
   站点模板"。
3. **构造式 URL 模板稀少但极稳**：全库仅 5 个翻译器用模板字符串构造 PDF 直链，
   其中 Frontiers：`{base}/articles/{doi}/pdf`。→ L2 profile 模板机制。
4. **Europe PMC 走官方 REST**（articleApi?resultType=core → fullTextUrlList），
   ct-literature 已有原生通道（`_epmc_lookup_pdf_url`），无需重复建设。
5. **无 ScienceDirect/MDPI/PLOS/PMC 专属翻译器**：付费墙站 Zotero 也不硬刚；
   MDPI/PLOS 等全靠 EM 兜底。PLOS landing 页实测有 citation_pdf_url，
   L1 直接命中（已端到端验证：下载 7 页有效 PDF）。

## 已落地实现（全部自研，无 AGPL 衍生）

- `adapters/site_profiles.json`：profile 数据文件（改规则不动代码）
  - frontiersin.org：url_template 模板（该域在 _WAF_HOSTS，禁 landing 抓取）
  - europepmc.org / www.mdpi.com：备注项（已有原生通道 / 反爬禁抓）
- `adapters/pdf_download.py` 新增：
  - `_load_site_profiles()` / `_profile_for()` / `_host_of()`
  - `_extract_pdf_candidates(html, base_url)`：三级提取
    landing_meta > landing_link(`type=application/pdf`) > landing_anchor
    （锚点同域优先）
  - `_telemetry_pdf_resolve()`：遥测追加 `out_dir/.pdf_resolver_log.jsonl`
    （ts/doi/domain/layer/url/result）
  - `PdfDownloader._resolve_landing_pdf(doi, url)`：A=profile 模板构造，
    B=通用 landing 解析；反爬域与 landing_fetch=false 跳过
  - `_classify` 新增 **⑤.5**：`oa 为 landing 且 (is_oa or preprint) 且
    非 explicit_non_oa` 时才解析（红线对齐 coze lit_route，不为注定 skip
    的条目白抓页面）
- 位置：本地优先链 ①EPMC → ②OpenAlex → ③非WAF直链 → ④预印本 →
  ⑤WAF直链 → **⑤.5 landing 解析（新）** → ⑥coze 路由

## 验证记录（2026-10-27）

- 单测：profile 加载 / Frontiers 模板命中 / meta+link+anchor 三级提取全对
- 活体：Frontiers 模板构造 ✓；PLOS landing → citation_pdf_url 提取 ✓ →
  下载 285KB / 7 页有效 PDF ✓
- 发布包：build_publish 重建后 site_profiles.json + 新代码均在，加载正常

## 后续

- 遥测积累几轮后按 (domain, layer, result) 统计命中率，为失败大头站点
  增补 profile 模板
- 若长尾命中率不足，再评估真 translation-server sidecar（独立 AGPL 进程，
  URL 引用不进发布包）
