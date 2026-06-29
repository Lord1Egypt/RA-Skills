---
name: financial-report-fetcher
description: 上市公司年报/研报自动抓取。覆盖巨潮资讯、东方财富等数据源，支持按公司代码/名称/年份/行业批量下载 PDF。内置反爬绕过、PDF 解析。
version: 0.2.0
---

# 上市公司年报/研报抓取 Skill

> **目标**：通过自然语言指令，自动从东方财富、巨潮资讯、上交所、深交所等权威财经网站获取上市公司年报、季报、研报等 PDF 文档。
> **核心能力**：智能数据源路由 + 反爬绕过 + 登录模拟 + 批量下载 + PDF 解析

---

## 架构总览

```
用户指令 → 参数解析 → 数据源路由 → 抓取执行 → 反爬/登录处理 → 下载存储 → (可选) PDF解析 → 结果交付
```

## 依赖模块（复用现有技能）

| 依赖 | 用途 | Skill/工具 |
|------|------|-----------|
| smart-search | 公司代码/名称查询、公告页面定位 | `skills/smart-search` |
| scrapling | 反爬绕过（隐身/动态模式） | `skills/scrapling-web-scraper` |
| Crawl4AI | 深度页面抓取 + 结构化提取 | `skills/crawl4ai` |
| Firecrawl | 搜索 + 单页抓取降级 | `skills/firecrawl-cli` |
| web_fetch | Agent 内置抓取降级 | 内置工具 |
| Playwright | 登录态模拟、动态内容等待 | 已安装 |
| PyMuPDF | PDF 解析/文本提取 | 已安装 |
| requests | 原始 HTTP 请求、PDF 下载 | Python 标准库 |

## 已验证的 API（2026-06-18 实测通过）

### 巨潮资讯 — 年报/公告 PDF
- **搜索 API**: `POST http://www.cninfo.com.cn/new/hisAnnouncement/query`
  - 需要 `stock` 参数格式：`{code},{orgId}`，orgId 格式 `gssz{code}`（深）/ `gssh{code}`（沪）
  - `seDate` 需覆盖发布窗口：`{year}-01-01~{year+1}-06-30`
  - `searchkey` 精准匹配：`{year}年年度报告`
- **PDF 直链**: `http://static.cninfo.com.cn/{adjunctUrl}`
- **反爬**: UA 轮换 + 1-3s 随机延迟，无需登录

### 东方财富 — 行业/个股研报
- **列表 API**: `GET https://reportapi.eastmoney.com/report/list`
  - `qType`: 0=个股研报, 1=行业研报, 2=策略报告, 3=宏观研究, 4=券商晨会
  - `industryCode`: 行业分类 ID（旅游及景区=1272, 酒店餐饮=1271）
  - `code`: 股票代码（个股研报时用）
  - `beginTime`/`endTime`: 日期范围
  - 返回 JSONP 格式，需剥离 callback 包装
- **PDF 直链**: `https://pdf.dfcfw.com/pdf/H3_{infoCode}_1.pdf`
  - 无需登录，直接 GET 即可下载
  - 需检查 content-type 是否为 `application/pdf`，防止 404 返回 HTML
- **详情页**: `https://data.eastmoney.com/report/info/{infoCode}.html`
- **反爬**: 列表 API 无需登录、无反爬；PDF 直链也无需登录。页面抓取需 Playwright（JS 渲染）

### 行业代码参考
| 行业代码 | 行业名称 | 行业代码 | 行业名称 |
|---------|---------|---------|--------|
| 1272 | 旅游及景区 | 1271 | 酒店餐饮 |
| 420 | 航空机场 | 1268 | 互联网电商 |
| 1287 | 工业金属 | 1238 | IT服务Ⅱ |
| 422 | 物流 | 1221 | 数字媒体 |

## 支持的数据源（已验证 ✅ 未验证 ❌）

| 数据源 | 年报 | 季报 | 研报 | 反爬强度 | 需要登录 |
|--------|------|------|------|---------|---------|
| 巨潮资讯 (cninfo.com.cn) | ✅ | ✅ | ❌ | 中 | 否 |
| 东方财富 (eastmoney.com) | ✅ | ✅ | ✅ | 低(列表API)/高(页面) | 否(列表+PDF)/部分(页面) |
| 上交所 (sse.com.cn) | ❌ | ❌ | ❌ | 低 | 否 |
| 深交所 (szse.cn) | ❌ | ❌ | ❌ | 低 | 否 |
| 慧博投研 (hibor.com) | ❌ | ❌ | ❌ | 高 | ✅ |
| 萝卜投研 (robo.datayes.com) | ❌ | ❌ | ❌ | 中 | 部分 |

## 实测验证记录（2026-06-18）

### ✅ 验证通过：巨潮资讯 + 万科A 历年年报
- 下载 6 份年报 PDF（2019-2024），全部可正常解析
- 关键发现：`stock` 参数需 `{code},{orgId}` 格式（如 `000002,gssz0000002`）
- `seDate` 需覆盖次年发布窗口（如 2024 年报在 2025 年 4 月发布）
- `category` 参数过滤过严，改用 `searchkey` 精准匹配更可靠
- 文件：`downloads/000002_万科A/annual/` 共 66 MB

### ✅ 验证通过：东方财富 + 旅游行业研报
- 列表 API 无需登录，直接 GET 返回 JSONP 格式数据
- PDF 直链 `pdf.dfcfw.com/pdf/H3_{infoCode}_1.pdf` 无需登录直接下载
- 下载 5 份 PDF，4 份成功（1 份 PDF URL 无效→需加 404 校验重试）
- 携程集团研报 61 页 / 10.7 MB，内容完整可解析
- `industryCode` 参数：旅游及景区=1272, 酒店餐饮=1271
- 文件：`downloads/旅游行业研报_PDF/` 共 14 MB

---

## 使用方法

### 自然语言指令

```
# 按公司下载
"下载腾讯2025年年报PDF"
"下载贵州茅台2023-2025年所有年报"
"下载平安银行最新季度报告"

# 按行业/批量下载
"下载所有银行板块公司的2024年年报"
"下载沪深300成分股2024年年报（限前10家）"

# 研报抓取
"下载茅台的券商研报，最近3个月"
"抓取东方财富上宁德时代的所有研报"

# 解析提取
"下载腾讯2024年年报并提取财务数据"
"抓取茅台年报PDF，提取营收和净利润"
```

### 脚本调用

```bash
# 基本下载（巨潮资讯优先）
python3 scripts/financial_report_fetcher.py --stock "000858" --year 2024

# 多公司批量下载
python3 scripts/financial_report_fetcher.py --stocks "000858,600519,000001" --years "2023,2024"

# 指定数据源
python3 scripts/financial_report_fetcher.py --stock "0700.HK" --source eastmoney

# 下载报告类型（年报/季报/半年报/研报）
python3 scripts/financial_report_fetcher.py --stock "600519" --type "annual" --years "2022,2023,2024"

# 仅搜索不下载
python3 scripts/financial_report_fetcher.py --stock "600519" --dry-run

# 下载后解析PDF
python3 scripts/financial_report_fetcher.py --stock "600519" --year 2024 --parse-pdf

# 研报模式
python3 scripts/financial_report_fetcher.py --research --stock "000858" --months 3
```

---

## 核心流程

### Phase 1: 参数解析

将自然语言指令转换为结构化参数：

```python
{
    "stocks": ["000858", "600519"],    # 股票代码
    "years": ["2023", "2024"],          # 年份范围
    "report_types": ["annual"],         # annual|semi-annual|quarterly|research
    "source": "auto",                   # auto|cninfo|eastmoney|sse|szse|hibor
    "action": "download",               # download|search|parse
    "parse_fields": [],                 # 需要提取的PDF字段
    "output_dir": "./downloads/",       # 输出目录
    "max_concurrent": 3,                # 并发数
}
```

### Phase 2: 数据源路由（智能降级）

```
1. cninfo（巨潮资讯）    ← 法定披露平台，覆盖最全，无登录要求
   ↓ 失败或无结果
2. sse.com.cn（上交所）   ← 上交所上市公司
   ↓ 失败或无结果
3. szse.cn（深交所）      ← 深交所上市公司
   ↓ 失败或无结果
4. eastmoney（东方财富）  ← 研报+年报，部分需登录
   ↓ 失败或无结果
5. hibor（慧博投研）      ← 研报为主，需登录
```

### Phase 3: 抓取执行（按数据源）

#### 3A. 巨潮资讯（首选，无需登录）

**API 接口**：
```python
import requests

# 搜索公告
search_url = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
payload = {
    "stock": "000858",              # 股票代码
    "tabName": "fulltext",
    "pageSize": 30,
    "pageNum": 1,
    "column": "szse",               # szse/sse
    "category": "category_ndbg_szsh",  # 年报: category_ndbg_szsh
    "seDate": "2024-01-01~2024-12-31",
    "searchkey": "年度报告"
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Referer": "http://www.cninfo.com.cn/new/disclosure",
    "Content-Type": "application/x-www-form-urlencoded"
}

resp = requests.post(search_url, data=payload, headers=headers)
announcements = resp.json()["announcements"]

# 下载 PDF
for ann in announcements:
    adjunct_url = ann["adjunctUrl"]  # 如: finalpage/2025-04-01/123456.PDF
    pdf_url = f"http://static.cninfo.com.cn/{adjunct_url}"
    pdf_resp = requests.get(pdf_url, headers=headers)
    with open(f"downloads/{ann['secCode']}_{ann['announcementTitle']}.pdf", "wb") as f:
        f.write(pdf_resp.content)
```

**报告类型 category 映射**：
- 年报: `category_ndbg_szsh`
- 半年报: `category_bndbg_szsh`
- 季报: `category_jdbg_szsh`
- 招股书: `category_first_szsh`

**反爬策略**：
- 每次请求间隔 1-3 秒随机延迟
- 轮换 User-Agent（5 组常见 UA）
- 使用 Referer 伪装
- 批量下载时并发 ≤ 3
- 如返回 403，启用 Scrapling stealth 模式

#### 3B. 上交所 SSE

**API 接口**：
```python
# 搜索公告
search_url = "http://query.sse.com.cn/sseQuery/commonQuery.do"
params = {
    "jsonCallBack": "jsonpCallback",
    "isPagination": "true",
    "stockCode": "600519",
    "companyCode": "",
    "pageHelp.pageSize": 25,
    "pageHelp.pageNo": 1,
    "pageHelp.beginPage": 1,
    "product": "600519",
    "bulletintype": "periodic",    # 定期报告
    "filetype": "PDF",
    "sqlId": "common_ssepany_disclosure_info_product_bulletin_index",
    "_": int(time.time() * 1000)
}
headers = {
    "Referer": "http://www.sse.com.cn/disclosure/listedinfo/announcement/",
    "User-Agent": "..."
}
```

#### 3C. 深交所 SZSE

**API 接口**：
```python
# 搜索公告
search_url = "https://disc.szse.cn/api/disc/info/ann/twoCategory"
params = {
    "random": str(time.time()),
    "seDate": "",
    "channelCode": "listedNotice",
    "bigCategoryId": "category_ndbg_szsh",  # 年报
    "subBigCategoryId": "",
    "stock": "000858",
    "pageNum": 1,
    "pageSize": 30
}
```

#### 3D. 东方财富（研报 + 年报）

**挑战**：部分页面需登录，有反爬机制。

**解决方案**：
```python
# 方式1：直接 API（无需登录）
research_url = "https://np-anotice-stock.eastmoney.com/api/security/ann"
# 类似 cninfo 的 POST 请求

# 方式2：Scrapling stealth 模式（需要登录/有反爬时）
from scrapling.fetchers import StealthyFetcher
page = StealthyFetcher.fetch(
    "https://data.eastmoney.com/report/{stock_code}.html",
    headless=True,
    solve_cloudflare=False,
    timeout=30
)

# 方式3：Playwright 登录态（慧博等需登录平台）
# 见下方"登录态管理"部分
```

**东方财富研报页面解析**：
```python
# 研报列表页
url = f"https://data.eastmoney.com/report/{stock_code}.html"
# CSS 选择器提取研报标题、日期、机构、PDF链接
selectors = {
    "title": ".report-title a::text",
    "date": ".report-date::text",
    "org": ".org-name::text",
    "pdf_link": "a[href*='.pdf']::attr(href)"
}
```

#### 3E. 慧博投研（需登录，研报为主）

**登录态管理**：
```python
from playwright.sync_api import sync_playwright

def login_hibor(username: str, password: str, storage_state: str = "hibor_state.json"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=storage_state if os.path.exists(storage_state) else None)
        
        if not os.path.exists(storage_state):
            page = context.new_page()
            page.goto("https://www.hibor.com.cn/login")
            page.fill("#username", username)
            page.fill("#password", password)
            page.click("button[type='submit']")
            page.wait_for_url("**/user/**", timeout=10000)
            context.storage_state(path=storage_state)
        
        return context
```

### Phase 4: 反爬/登录策略矩阵

| 挑战 | 应对方案 | 工具 |
|------|---------|------|
| User-Agent 检测 | 轮换 UA 池（5-10组） | requests + 自定义 headers |
| IP 频率限制 | 随机延迟 1-3s + 并发≤3 | time.sleep(random) |
| Cloudflare 验证 | Scrapling stealth 模式 | scrapling |
| 动态加载（JS） | Crawl4AI / Playwright | crawl4ai / playwright |
| 需要登录 | Playwright 登录态持久化 | playwright + storage_state |
| 验证码 | 人工介入提示 + Playwright 截图等待输入 | playwright |
| Cookie 过期 | 自动检测 + 重新登录 | playwright |

### Phase 5: 下载与存储

```
downloads/
├── {公司代码}/
│   ├── annual/
│   │   ├── 2024_{股票简称}_年报.pdf
│   │   └── 2023_{股票简称}_年报.pdf
│   ├── semi-annual/
│   ├── quarterly/
│   └── research/
│       ├── 2026-06_{机构}_{标题}.pdf
│       └── ...
├── metadata.json          # 下载元数据记录
└── download_log.md        # 本次下载摘要
```

**metadata.json 格式**：
```json
{
    "downloads": [
        {
            "stock_code": "600519",
            "stock_name": "贵州茅台",
            "report_type": "annual",
            "year": "2024",
            "source": "cninfo",
            "file_path": "downloads/600519/annual/2024_贵州茅台_年报.pdf",
            "title": "贵州茅台2024年年度报告",
            "announcement_id": "12345678",
            "download_time": "2026-06-18T10:00:00+08:00",
            "file_size_mb": 5.2
        }
    ]
}
```

### Phase 6: PDF 解析（可选）

```python
import fitz  # PyMuPDF

def extract_financial_data(pdf_path: str, fields: list = None) -> dict:
    """从年报PDF中提取关键财务数据"""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    
    # 关键词定位提取
    data = {}
    patterns = {
        "营收": r"营业收入[：:]\s*([\d,\.]+)\s*元",
        "净利润": r"归属于.*?[：:]\s*([\d,\.]+)\s*元",
        "总资产": r"资产总计[：:]\s*([\d,\.]+)\s*元",
        "每股收益": r"基本每股收益[：:]\s*([\d,\.]+)\s*元",
        "ROE": r"加权平均净资产收益率[：:]\s*([\d,\.]+)%",
    }
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        if match:
            data[key] = match.group(1)
    return data
```

---

## 错误处理

```python
ERROR_CODES = {
    "CNINFO_403": "巨潮反爬触发，切换 Scrapling stealth 模式重试",
    "CNINFO_EMPTY": "未找到相关年报，检查股票代码/年份是否正确",
    "EASTMONEY_LOGIN": "东方财富需要登录，请配置 cookies 或使用 Playwright 登录",
    "PDF_DOWNLOAD_FAIL": "PDF 下载失败，尝试备用数据源",
    "STOCK_NOT_FOUND": "未找到该公司，使用 smart-search 确认股票代码",
    "RATE_LIMIT": "请求过于频繁，等待 10 秒后重试",
}
```

---

## Agent 集成工作流

```
用户: "下载贵州茅台2024年年报"
    ↓
1. 解析 → stock_code=600519, year=2024, type=annual
2. 首选巨潮资讯:
   a. POST hisAnnouncement/query 搜索
   b. 返回结果 → 提取 PDF URL
   c. GET PDF → 保存
3. 巨潮失败 → 尝试上交所
4. 上交所失败 → 尝试东方财富
5. 所有数据源失败 → 报错告知用户

用户: "下载并分析腾讯2024年报的营收结构"
    ↓
1. 下载 PDF（港股→优先东方财富/港交所）
2. PyMuPDF 提取文本
3. 关键词定位"营业收入"+"分部收入"
4. 返回结构化数据
```

---

## 快速开始

```bash
# 1. 安装依赖（已有大部分）
pip3 install requests playwright PyMuPDF

# 2. 安装浏览器（如果未安装）
python3 -m playwright install chromium

# 3. 运行测试
python3 scripts/financial_report_fetcher.py --stock "600519" --year 2024 --dry-run
```

---

## 注意事项

1. **合规使用**：仅下载公开披露的年报/研报，不用于商业再分发
2. **频率控制**：巨潮资讯建议 ≤10 次/分钟，东方财富 ≤5 次/分钟
3. **登录态安全**：cookies 和 storage_state 文件不提交到代码库
4. **数据源时效性**：年报披露有固定时间窗口（每年 1-4 月年报，7-8 月半年报）
5. **港股/美股**：需要额外数据源（HKEX披露易、SEC EDGAR）
6. **反爬升级**：如果巨潮 API 返回结构变化，需要更新 payload 参数

---

## TODO / 扩展方向

- [ ] 增加 HKEX 披露易支持（港股年报）
- [ ] 增加 SEC EDGAR 支持（美股 10-K/10-Q）
- [ ] 增加研报 AI 摘要（用 LLM 自动总结研报观点）
- [ ] 增加财报数据对比（多年度趋势分析）
- [ ] 增加飞书多维表格存储（自动同步下载记录）
- [ ] 增加定时任务（财报季自动监控披露）

---

_创建于：2026-06-18 by 小七_
_版本：0.1.0（方案设计）_
