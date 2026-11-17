---
name: buyback-screen
description: >-
  筛选A股（沪深北交所）最近发布回购公告（回购计划/预案）的上市公司，并按市盈率(PE-TTM)、
  市净率、总市值、回购金额、用途、进度等条件过滤，输出清单表格。数据来自东方财富数据中心。
  当用户提到"回购公告/回购预案/回购进展/筛选回购/回购名单/哪些公司最近回购"、
  "回购+市盈率/PE/估值过滤"、"注销式回购"、"大额回购"、或"最近有哪些公司回购了"
  等需求时，务必使用此技能，即使没有明确说"skill"。也适用于把回购公司按 PE≤X 进一步筛选、
  按回购金额/用途/进度筛选、导出回购清单 CSV/TSV 等场景。
compatibility:
  - Python 3（仅用标准库 urllib/json，无需第三方依赖）
  - 需要网络访问 datacenter-web.eastmoney.com（东方财富数据中心）
---

# A股回购公告筛选

## 它能做什么

给定一个时间窗口，拉取 A 股（沪深 + 北交所）在这期间**发布过回购公告**的上市公司，
自动联表获取**滚动市盈率(PE-TTM)、市净率、现价、总市值**，并支持按以下条件过滤：

- 市盈率上限 / 下限（`--max-pe` / `--min-pe`）
- 拟回购金额下限（`--min-amount-wan`，单位万元）
- 用途：员工持股/股权激励、注销减资、市值管理、可转债转股、其他（`--purpose`）
- 进度：预案 / 进展 / 完成（`--progress`）
- 只显示前 N 条（`--top`）

## 快速开始

```bash
python "C:\Users\85446\.claude\skills\buyback-screen\scripts\screen_buybacks.py" \
  --from 2026-07-27 --max-pe 15
```

- **窗口**：默认回溯 14 天；用 `--days N` 或 `--from YYYY-MM-DD` 指定。
- **输出**：stdout 打印 markdown 表格，同时把明细写入 `buyback_screen_<日期>.tsv`（UTF-8）。
- **注意**：Windows 控制台可能无法正常显示中文（会乱码），这是编码显示问题而非数据问题。
  **务必用 Read 工具读取生成的 TSV 文件**，再把内容整理成清晰的 markdown 表格回复给用户。

## 完整用法

```bash
# 近30天所有回购公告
python .../screen_buybacks.py --days 30

# 近7天，拟回购5亿以上
python .../screen_buybacks.py --days 7 --min-amount-wan 50000

# 市盈率(TTM)<=15（正盈利），只看"注销减资"用途
python .../screen_buybacks.py --max-pe 15 --purpose 注销减资

# 只看新发预案（进度=001）
python .../screen_buybacks.py --progress 001

# 自定义输出文件
python .../screen_buybacks.py --days 30 --out 我的回购清单.tsv
```

所有参数：`--days`、`--from`、`--max-pe`、`--min-pe`、`--include-loss`、
`--min-amount-wan`、`--purpose`、`--progress`、`--top`、`--out`。

## 汇报时注意

1. **亏损股要单列**。PE(TTM)<0 的公司是亏损股，不要和低市盈率混在一起说"市盈率15以下"。
   脚本会把亏损股单独打印在表格后面。
2. **给用户突出价值点**，不要只丢表格：
   - 大额回购（金额占比、占市值比例）
   - **注销式回购**（注销减资，对股东最友好）的公司单独标注
   - 回购价格上限显著高于现价的（说明公司认为低估，安全边际高）
   - 低估值（PE 低）+ 回购的组合
3. 如果用户没说窗口，先按默认 14 天出结果，再问是否要拉长。
4. 用户可能随后追问某只股票（如"里面有XX吗"），可用下面"单只查询"的方法回答。

## 单只股票追问（可选）

用东方财富个股公告接口核验某只股票是否在近期发过回购公告（含**进展类**，这类在"回购计划"
列表里可能不占新行）：

```bash
curl -s "https://np-anotice-stock.eastmoney.com/api/security/ann?sr=-1&page_size=50&page_index=1&ann_type=A&client_source=web&stock_list=000333"
```

返回的 `list` 里按 `notice_date` 找标题含"回购"的公告（如"关于以集中竞价交易方式回购A股股份进展公告"）。

## 数据源与已知坑（重要）

- **回购计划**：`RPTA_WEB_GETHGLIST_NEW`，按 `DIM_DATE` 降序分页。
  - `DIM_DATE` = 该条回购计划的记录/方案日期；`REMARK` 里带真正的公告日期，格式
    `2026.07.31公告`（脚本已自动提取到"公告日"列）。
  - 进度码：`001`预案、`004/006`进展、`007`完成、`002`审议、`003`股东大会。
  - 金额字段 `REPURAMOUNTLOWER`/`REPURAMOUNTLIMIT` 单位是**元**，脚本已换算成万元。
  - **不要用 `NOTICEDATE` 字段筛选**——它含批量导入日期（例如某天对一大片股票同时打上
    同一日期），不可靠。按 `DIM_DATE`（方案日期）筛窗口即可。
- **估值**：`RPT_VALUEANALYSIS_DET`，用 `filter=(SECURITY_CODE in (...))` 一次查多只，
  按 `TRADE_DATE` 降序取每只最近一条。字段：`PE_TTM`（滚动市盈率）、`PB_MRQ`（市净率）、
  `CLOSE_PRICE`、`TOTAL_MARKET_CAP`（元）。
- 板块从 `SECUCODE` 后缀判断：`.SH`沪、`.SZ`深、`.BJ`北交所。
- 两个接口都是公开数据接口，加 `User-Agent` 请求头即可，无需登录。
