# 维普 OA 平台 API 契约（2026-08-14 实测逆向，v2 增补）

> 来源：probe1–15 + v2 QA 探针实测。全部端点 **POST JSON**（下载第3步为 GET blob），**免登录、免费、无凭证**。
> 平台：大家·维普期刊OA出版平台 https://oa.cqvip.com （Nuxt.js SPA，后端 Spring Boot，baseURL `https://oa.cqvip.com/dajia-oa-app/`）

## 0. 基础

- **API 前缀**：`https://oa.cqvip.com/dajia-oa-app`（⚠️ 必须带 `/dajia-oa-app`，根路径 `/api/...` 返回 404）
- **请求头**：`Content-Type: application/json` + 浏览器 UA + `Origin/Referer: https://oa.cqvip.com`
- **认证**：无
- **Python 实现**：纯 stdlib（urllib.request + ssl + json + sqlite3），禁代理 opener + 可选 SSL 校验 + 3 次指数退避

## 1. 检索（成果库）

```
POST /api/paperSearchApi/search
{"advancedSearchList": [{"field": "T", "content": "关键词", "logicalOperator": "AND"}],
 "aggsParams": {"C": [], "I": []}, "page": 1, "size": 20}
```

**field 代码**（实测）：`T`题名 `K`关键词 `M`主题 `A`作者 `J`刊名 `S`机构 `F`基金

> ⚠️ 坑1：参数不是 `conditions:[{content,searchField}]`（会被整体忽略、返回默认列表）——正确结构是 `advancedSearchList:[{field,content,logicalOperator}]`。
> ⚠️ 坑2：**平台是 OR 匹配语义且无"无结果"信号**——"量子纠缠炒股"也返回 20 条（量子纠缠物理论文）；"专家共识 风湿"会丢弃"风湿"返回肿瘤共识。必须在上层做覆盖率制相关性守门（见 cn_med_oa.relevance_gate，ok≥0.80/low≥0.50，多词按词取最小覆盖率）。
> ⚠️ 坑3：rows 里**没有 doi 字段**（None），DOI 只在详情接口——每条结果必须调详情。

rows[] 关键字段：`id/lngid/fullTextId`(通常相等)、`title/name`、`abstr`、`pubDate/year`、`isPdf`(1=有PDF)、`pdfPath`(OSS key)、`keywordInfo/authorInfo/organInfo/fundInfo`、`isOa/cqvipIsOa`、`copyRight/allowTransmission`

## 2. 详情（Vancouver 元数据主源）

```
POST /api/paperSearchApi/literatureBaseDetails  {"id": <论文id>}
→ {success, data: [{...}]}
```

**v2 关键发现——objectInfo 藏着权威卷期 + 刊物信息**（v1 曾漏读，导致误用 DOI 正则）：

```json
"objectInfo": {"name": "浙江医学", "year": 2026, "vol": "48", "num": "7",
               "issn": "1006-2785", "cnno": "33-1109/R", "publisher": "浙江省医学会",
               "isCore": 0, "range": ["CA","CSTPCD","JST"], "gch": "90622X",
               "nameAlt": [{"lang":"en","_v":["Zhejiang Medical Journal"]}]}
```

- `vol`/`num` = **权威卷/期**（实测浙江医学 48(7)✓、医学临床研究 43(2)✓——后者 DOI 正则会误析为 02(001)）
- `providerSource[].uri` 含**同文献的知网落地页**（kns.cnki.net，可作指引，不抓取）

## 3. PDF 下载（三步链路）

1. 检索拿 `id/lngid/year/name`
2. `POST /api/paperSearchApi/previewPath` `{"lngId","paperYear","weiPuPaperId","name"}` → `entity`（内容 hash 文件名，可作缓存键）
3. `GET /api/attachmentApi/fileBrowsing?hash=<entity>` → **PDF 二进制流**（head=`%PDF`）

实测样本：id=7203426125 → 994KB，pymupdf 提取首页标题/期刊/DOI 全部吻合。

> ⚠️ 已废弃路径（踩坑记录）：`downloadPdf({id})` 对 2026 新文献 entity:null；`fanyu-static.oss.../oa-pdf/{id}.pdf` 老数据专用已 404；`getDownloadLink` 需登录态；`attachmentApi/download({hash})` entity:null。

## 4. PDF 文本陷阱（卷期/页码提取，v2 实测）

- **卷期交叉验证只看页眉**（首页前 220 字的"第N卷第M期"）——正文中引用的其他文献也含"第N卷"，全文匹配会误判不一致（医学临床研究实测踩坑）。
- **页码在页脚**，模式为"点+数字"且逐页递增：`·\n· 770`（浙江医学实测 770-774）。无尾点；仅部分期刊文本层有页码（提取率 ~21%，缺失时如实标注）。
- 中文 PDF 文本为字形索引编码，直接 grep 中文会全部落空——必须用 pymupdf 提取。

## 5. 合规与边界

- 仅取 OA 文献；`isPdf=1` 才有 PDF
- 控频 ≥3s（`CN_MED_OA_INTERVAL`）+ 日配额 50（`CN_MED_OA_DAILY_MAX`，sqlite 跨进程）
- robots.txt 404（未设限）；遵守 ToS，不做批量轰炸
- 中华医学会系期刊（中华内科杂志等）**不在本平台**（实测刊名检索 0 命中，在 yiigle 登录墙内）

## 6. 依赖

- 连接器/验证器：纯 Python stdlib
- PDF 文本提取（内容校验/页码/页眉卷期）：pymupdf ≥1.27（缺失自动降级，跳过 PDF 相关校验）
