# 数据源通道分析（ct-safety）

> 备查文档 · 2026-09-06 整理 · 依据当时代码实测（coze_dispatch.py / corroborative_sources.py / fetch_cn_pv.py v2 优化后）

## 1. 通道全景：8 个数据源，两类通道

### ① Coze 统一端点外发（ct-search.coze.site/run，落飞书 searchlog 审计）

| source | 数据源 | 用途 |
|---|---|---|
| `faers` | FDA FAERS（api.fda.gov/drug/event.json） | 不均衡性信号检测主力（ROR/PRR/IC/EBGM） |
| `fda_label` | FDA 说明书（api.fda.gov/drug/label.json） | 风险是否已收录判断 |
| `dailymed` | DailyMed（NIH） | 佐证型 Evidence（说明书文本） |
| `rxclass` | RxClass / RxNav（NIH） | 药物分类佐证（同类药风险） |
| `fda_recall` | FDA 召回（openFDA enforcement） | 召回事件佐证 |
| `hk_pv` | 中国香港 PHR 药物警戒 | 地区性佐证 |
| `nmpa_pv` | NMPA 公报（adapters/nmpa_coze.py） | NMPA 主站 WAF 412，走 Coze 浏览器通道 |

### ② 技能本地直连（不经 Coze，不落飞书日志）

| 脚本 | 站点 | 状态 |
|---|---|---|
| `multi_source.py` | VigiAccess（WHO UMC）/ EU EudraVigilance（adrreports.eu） | ❌ 实测阻断（见 §3） |
| `fetch_canada.py` | Canada Vigilance | ❌ 实测阻断 |
| `kw_localize.py` | Google Translate / MyMemory（翻译辅助，非数据源） | ✅ 可用 |

辅助直连：`query_total` / `fetch_case_reports` / `check_event` 直连 openFDA（本机直连可达，保持本地）。

> **2026-09-07 架构更新**：所有检索（含 CN-PV）已按 ct-base §20.14 改造为轻本地端。
> `fetch_cn_pv.py` 抓取执行器上移 Coze `cn_pv` 节点（payload 契约见 `references/cn_pv_contract.md`），
> 本地仅保留词表扩展（`cn_pv_keywords.py`）、证据分级（`_grade_hit`）、
> 结果组装与 `cn_pv_cache.json` 缓存。`--run` / `--offline` 参数已移除（无本地降级路径）。
> `corroborative_sources.py` 已移除 `DailyMedSource` / `RxClassSource` / `FdaRecallSource` 三个本地抓取类，
> 仅保留 `CozeSource` 薄包装和 `collect()` 汇总判定。

## 2. 本地直连源重要性排序

**只有 CN-PV（cdr-adr.org.cn）真正重要且在用**：

1. **唯一接进主流程的本地直连源**：`ct_safety.py` 直接 `import fetch_cn_pv`，主分析路径跑
   国家药品不良反应监测中心检索（含药物/事件关键词双语扩展）。
2. **数据价值不可替代**：中国申报场景（PSUR、CDE 咨询、中文报告）的本土数据源；
   Coze 端点的 `nmpa_pv` 只覆盖公报检索，CN-PV 补的是官方通报全文维度。
3. **本机直连可达**：无 WAF、无验证码、无 JS 渲染。

其余本地直连源已被实测阻断（见 §3），只在报告中如实披露"被阻断"，不静默假装无数据。

## 3. 实测阻断源清单（corroborative_sources.BLOCKED_SOURCES）

| 源 | 状态 | 阻断原因 |
|---|---|---|
| VigiAccess（WHO UMC） | ❌ | 纯 SPA，无数据 API 端点 |
| EU EudraVigilance（adrreports.eu） | ❌ | 数据在 BusinessObjects 报表内，无 JSON 端点 |
| Health Canada | ❌ | API 连续 ReadTimeout |
| PMDA / JADER（日本） | ❌ | 下载表单需验证码（captchaText） |
| VAERS（美国 CDC） | ❌ | CDC WONDER 返回 403，需 POST XML + 使用协议 |
| UK MHRA（iDAP） | ❌ | ConnectTimeout |

> VigiAccess 理论上数据价值高（WHO 全球最大 PV 库），若官方开放 API 应优先接入；
> 其余阻断源不建议再投入时间。

## 4. 为什么 CN-PV 留在本地、不移交 Coze

分工规则：**无 WAF 静态站 → 本地直连；WAF/动态站 → Coze 浏览器通道**。

给不需要浏览器的站点用浏览器通道是大炮打蚊子。"Coze 端点没有这个深度"的准确表述是：
**深度在技能侧，而不是站点难抓**——

1. **检索深度依赖技能本地资产**：药名双语扩展依赖 `references/drug_name_map.json`
   （单一真源）+ 事件同义词组；证据分级（通报专文 > 数据报告 > 提及）是 ct-safety
   特有业务逻辑。挪到服务端就得双份维护并污染通用检索节点。
2. **运行形态不匹配**：一轮检索（5 栏目 × 翻页 × 逐篇 + 0.6s 礼貌休眠）跑几十秒到几分钟，
   本地长任务无压力；统一端点是同步请求-响应模式，有超时约束。
3. **缓存与安全模型**：`cn_pv_cache.json`（查询指纹缓存 + 24h TTL）、SAFE PREVIEW 门控
   （显式 `--run` 才联网）都是技能本地策略。

审计盲区折中方案（如未来需要）：抓取留本地，完成后向 coze 端点补发
`source=cn_pv_local` 审计记录——零逻辑迁移，落库可查。

## 5. fetch_cn_pv.py v3 优化记录（2026-09-06）

| 优化 | 内容 | 收益 |
|---|---|---|
| 列表页日期预过滤 | 从列表页 HTML 提取 `date_hint`（`_listing_date_hint`），早于日期窗的文章直接跳过正文抓取 | 每篇省 1 次请求 + 0.6s 休眠；date_hint 缺失时不预滤、不漏检 |
| 翻页提前终止 | 列表按日期倒序，某页全部 date_hint 早于 `since` 窗口起点 → 停止翻页（page 1 也适用） | 深翻页场景省大量无效请求 |
| 缓存 TTL | `_cached_at` 时间戳，默认 24h 过期（`_CACHE_TTL_H`）；旧格式条目（无时间戳）保持有效，向后兼容 | 隔月复用不再出脏数据；`--no-cache` 仍可强制刷新 |
| NMPA 主站链接跳过 | 通知通告栏目常引用 nmpa.gov.cn 链接（WAF 412 必然失败），提前跳过计入 `stats.skipped_nmpa_host` 而非 `failed_articles` | 省无效请求 + 重试等待；**不再污染 `degraded` 标志**（0 命中可正确解读为"官方无相关通报"） |
| 结果计时 | 新增 `result.elapsed_sec` | 报告层可展示检索耗时 |

实测验证（奥希替尼 × 肺炎，5 栏目 × 5 篇）：`degraded=False`，
coverage 正确显示"2 篇 NMPA 主站文章跳过（属 Coze nmpa_pv 通道职责，非抓取失败）"。

方法学边界不变（v2 起即明确）：CN-PV 是**叙事性官方通报，非个案计数**，
不可做 disproportionality（PRR/ROR/IC）分析，仅作 FAERS 量化信号的定性佐证。
