# 数据源与取数策略（实测验证版 · 2026-08-07）

> 本节所有端点均经实际抓取验证。默认免费、无需 Key。

## 0. 取数架构（agent 取数 + 脚本仅解析）⚠️

**设计原则**：取数是 agent 的受控动作，脚本 `scripts/fetch_ccgp.py`（ccgp 源）与 `scripts/fetch_ceb.py`（cebpubservice / 省级平台源）**不擅自联网**，只负责解析落 JSON。`fetch_ceb.py` 用 `--merge` 把 ceb 解析结果并入 ccgp 记录，统一交给机会引擎去重。

**标准流程（主路径）：**
1. agent 用 WebFetch / Bash(python urllib | curl) 把**原始 HTML** 落盘到工作目录（注意：WebFetch 工具默认返回 markdown，解析清单需要原始 HTML，故请用 Bash 取原始页面）。
2. 用脚本解析：
   ```bash
   # 解析 listing
   python scripts/fetch_ccgp.py --html-file listing.html --out records.json
   # 批量解析目录
   python scripts/fetch_ccgp.py --html-dir ./ccgp_html/ --out records.json
   # 补全详情（detail 落盘 HTML 需带原 source_url 以便合并）
   python scripts/fetch_ccgp.py --html-file listing.html \
       --detail detail_1.html::https://www.ccgp.gov.cn/cggg/.../t1.htm \
       --out records.json
   # 落 JSON 后直接跑机会引擎
   python scripts/fetch_ccgp.py --html-file listing.html --profile ~/.bidprofile.json --run
   # ceb 详情页解析并并入 ccgp 记录
   python scripts/fetch_ceb.py --html-dir ./ceb_html/ --merge records.json --out all_records.json --run
   ```
3. `--kw` 直连 bxsearch 作为**离线补充**（可能限流），非主推。

## 1. 中国政府采购网（主数据源 · listing）✅

**端点**（GET）：
```
https://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=1
  &start_time=&end_time=&timeType=2&searchparam=
  &searchchannel=0&dbselect=bidx&kw=<关键词>
  &bidSort=0&pinMu=0&bidType=0&buyerName=&projectId=
  &displayZone=&zoneId=&agentName=
```

**必填/关键参数：**
- `kw`：搜索关键词（**必填，空则无结果**）。可填产品/行业，如 `智慧校园`、`服务器`。
- `dbselect=bidx`：标讯库。
- `timeType=2`：时间范围（实测返回近当期数据，如 2026-08）。
- `bidType=0`：全部公告类型；`4`=招标、`7`=中标（对应业务阶段）。
- `page_index`：翻页（从 1 起）。

**实测返回字段（可直接解析）：** 标题、发布时间、采购人、代理机构、公告类型（中标/招标/更正/成交）、省份、行业分类、详情链接。

**解析方式：** WebFetch 直接可拿结构化清单；也可用 HTTP GET 后抽取列表项。

## 2. 中国政府采购网（详情页）✅

listing 中每条带详情 URL，形如：
```
http://www.ccgp.gov.cn/cggg/dfgg/zbgg/202608/t20260806_27087921.htm
```
**实测（经 WebSearch 全文）：** 正文含 项目编号、中标/成交供应商、中标金额、评审总得分、主要标的信息（品牌/型号/数量/单价）、代理费。→ 用于补全金额、供应商、评分。

## 3. 中国招标投标公共服务平台（工程建设类）⚠️ 需换入口

- **首页 `https://www.cebpubservice.com/` 是 JS 门户**，WebFetch 只能拿到营销栏目，"招标公告公示查询"无数据行 → **不可直接用作 listing**。
- **正确入口：** `https://bulletin.cebpubservice.com/`（全国招标公告公示标准发布工具），或 WebSearch `site:bulletin.cebpubservice.com "<关键词>"`。
- 覆盖工程建设、货物、服务采购（超出政府集中采购范围）。
- **详情页解析**：agent 用 Bash 取 `bulletin.cebpubservice.com` 详情页原始 HTML 落盘（或 WebSearch 找到的详情 URL），再用 `scripts/fetch_ceb.py` 解析（兼容「表格 `<td>`」与「标签：值」两种形态）：
  ```bash
  python scripts/fetch_ceb.py --html-dir ./ceb_html/ --merge records.json --out all_records.json --run
  ```
  `--merge` 将 ceb 记录并入已有 ccgp `records.json`，统一交给机会引擎按（项目名 + 采购人 + 日期）去重。

## 4. WebSearch 兜底 ✅（跨源保底，且更细）

- `site:ccgp.gov.cn "<关键词>" 中标` → 返回公告全文（金额/供应商/评分更全）。
- `site:bulletin.cebpubservice.com "<关键词>"` → 工程建设类公告。
- 作为多源聚合与字段补全的兜底。

## 取数注意事项

- bxsearch 的 `kw` 必须非空，否则返回空。
- 生产环境该端点可能要求 Cookie/Referer 或限频；若 WebFetch 失败，回退 WebSearch。
- 同一项目可能同时出现在 ccgp 与 cebpubservice → 按（项目名 + 采购人 + 日期）去重。
- 金额格式多样（"332.000000 万元" / "5,981,300.00元"）→ 归一化为整数元（参考 decision_framework 的金额处理）。
- 登录墙/反爬导致字段缺失时，如实标注，不伪造。
