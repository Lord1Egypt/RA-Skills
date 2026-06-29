---
name: financial-edu-david
description: A股上市公司财务分析全流程工具包。覆盖年报采集、三表提取、指标计算、可视化看板、数据核对的全链路。用于对A股上市公司进行近3-5年财务经营状况综合分析，包括年报PDF下载（巨潮资讯网）、合并资产负债表/利润表/现金流量表提取（PDF→xlsx）、财务指标计算（偿债/营运/盈利/发展/现金流/杜邦分析）、ECharts动态可视化看板（HTML）及东方财富F10数据交叉核对。触发场景：(1) "分析XX公司财务状况""XX股票财务分析""XX年报分析"等财务分析需求 (2) "下载XX年报" (3) "生成财务可视化看板" (4) "核对XX财务数据"。
agent_created: true
version: 1.0.0
author: David
tags:
  - 财务分析
  - A股
  - 年报
  - 可视化
  - 教育
category: finance
---

# A股上市公司财务分析全流程

## 适用场景

对指定A股上市公司进行3-5年财务经营状况综合分析，覆盖从数据采集到可视化交付的完整链路。

## 前置条件

- Python 3.8+，安装依赖：`pip install requests pdfplumber openpyxl`
- 网络可访问 cninfo.com.cn、eastmoney.com、cdn.jsdelivr.net（或备选CDN）
- 工作目录有写权限

---

## 五阶段工作流程

严格按以下顺序执行，每阶段完成后确认数据正确性再进入下一阶段。

### Phase 1: 年报采集

**目标**：从巨潮资讯网下载目标股票近N年（默认4年）年报PDF

**步骤**：
1. 确定股票代码（6位数字）、市场（sh/sz）、年份范围
2. 运行采集脚本：
   ```bash
   python scripts/fetch_annual_reports.py \
     --code {股票代码} --name "{股票名称}" \
     --years {起始年}-{结束年} --dir "{目标目录}" --market {sh|sz}
   ```
3. 若脚本因API变化失败，手动执行以下步骤：
   - 先查 orgId：`GET https://www.cninfo.com.cn/new/information/topSearch/query?key={code}`
   - 再查公告：`POST https://www.cninfo.com.cn/new/hisAnnouncement/query`（参数详见 [cninfo_api.md](references/cninfo_api.md)）
   - 下载PDF：`GET https://static.cninfo.com.cn/{adjunctUrl}`
4. 验证：PDF文件大小 > 100KB，可正常打开

**输出**：目录下 N 份年报 PDF + `采集日志.json`

### Phase 2: 三表提取

**目标**：从PDF提取合并资产负债表、利润表、现金流量表 → xlsx

**步骤**：
1. 先用 pdfplumber 探测每份PDF中三张表所在页码（0索引）：
   ```python
   import pdfplumber
   with pdfplumber.open("年报.pdf") as pdf:
       for i, page in enumerate(pdf.pages):
           text = page.extract_text() or ""
           if "合并资产负债表" in text and "母公司" not in text:
               print(f"资产负债表在第{i}页")
           # 同理探测利润表、现金流量表
   ```
   **重要：每张表可能跨2-3页，需确认起始页和结束页**
2. 构建 `pdf_config.json`（格式见下方示例）
3. 运行提取脚本：
   ```bash
   python scripts/extract_financial_tables.py --dir "{目标目录}" --config pdf_config.json
   ```
4. 若出现科目名缺失（因PDF跨行拆分导致），需手动补全核心科目（资产总计、负债合计、营业收入、净利润等）

**pdf_config.json 格式**：
```json
{
  "2022": {
    "file": "2023-04-21_公司名_2022年度报告.PDF",
    "balance_pages": [104, 105, 106],
    "income_pages": [108, 109, 110],
    "cash_pages": [111, 112, 113],
    "ann_id": "1216492757",
    "ann_url": "https://www.cninfo.com.cn/new/disclosure/detail?annoId=1216492757",
    "raw_url": "https://static.cninfo.com.cn/finalpage/2023-04-21/1216492757.PDF"
  }
}
```

**PDF解析核心问题**：
- 科目名跨行拆分（如"三、营业利润（亏损以"－"号填列）"可能分3行）：脚本使用 `pending_subject` 状态机处理
- 附注引用混入科目名（如"七、74"）：正则清理
- 即使处理仍有遗漏，需要以东方财富F10数据为基准补充核心科目

**输出**：每年一份 xlsx（3个sheet），文件命名：`{股票名}_合并三表_{年份}年.xlsx`

### Phase 3: 财务分析

**目标**：计算完整的财务指标体系 + 杜邦分析

**步骤**：
1. 采集核心数据：从xlsx中提取30+个关键科目值，生成 `_core_data.json`
   - 必含科目：资产总计、负债合计、所有者权益合计、流动资产合计、流动负债合计、存货、货币资金、应收账款、固定资产、短期借款、长期借款、营业收入、营业成本、净利润、归母净利润、归母股东权益、利润总额、销售费用、管理费用、研发费用、财务费用、所得税费用、经营活动/投资活动/筹资活动现金流量净额、销售商品提供劳务收到的现金
   - 注意：单位从"元"转换为"亿元"
2. 逐项计算指标 → 生成 `_metrics.json`
   - 指标计算公式详见 [metrics_guide.md](references/metrics_guide.md)
   - 杜邦分析：ROE = 净利率 × 总资产周转率 × 权益乘数
3. 对每个指标标注判定（好/中/差），判定标准参考 `metrics_guide.md`

**输出**：`_core_data.json` + `_metrics.json`

### Phase 4: 可视化看板

**目标**：生成HTML格式的动态财务分析数据可视化看板

**看板结构**（必须包含以下全部模块）：

| 模块 | 内容 | 图表类型 |
|------|------|----------|
| 页头 | 公司名、代码、年份、数据来源 | 静态HTML |
| 核心结论 | 5条关键发现（好/中/差三色标注） | 静态HTML |
| 数据核对 | 与东方财富F10对比表 | 静态表格 |
| 指标一览 | 偿债/营运/盈利/发展 四类指标汇总 | 彩色标注表格 |
| 图表1 | 资产负债趋势 | ECharts分组柱状图 |
| 图表2 | 营收与净利润趋势 | ECharts多线图 |
| 图表3 | 经营/投资/筹资现金流 | ECharts分组柱状图 |
| 图表4 | 盈利能力指标趋势 | ECharts多线图 |
| 图表5 | 偿债能力指标趋势 | ECharts多线图 |
| 图表6 | 营运能力指标 | ECharts柱+线混合图 |
| 图表7 | 增长率指标 | 分组柱状图 |
| 图表8 | 费用率结构 | 堆叠柱状图 |
| 杜邦分析 | ROE分解树形图（东方财富风格） | 纯HTML+CSS |
| 风险预警 | 高中低三类风险 + 改进建议 | 彩色卡片 |

**技术规范**：
- 使用 ECharts 5.x CDN（5个源自动回退）
- 所有数据内嵌在 `<script>` 中，无外部JSON依赖
- 使用 IIFE 封装避免全局变量污染
- 参考设计：[generate_dashboard.py](scripts/generate_dashboard.py)

**杜邦分析实现**：
- 纯 HTML+CSS（不用 ECharts graph），更接近东方财富F10风格
- 5层树形结构：ROE → 净利率/周转率/权益乘数 → 净利润÷营收 | 资产÷权益 → ...
- 支持年份切换
- 每个节点显示数值 + 运算符（× ÷ + −）
- 底部多列明细列表

### Phase 5: 数据核对

**目标**：确保分析数据与官方公开数据一致

**步骤**：
1. 调用东方财富F10接口核对（详见 [eastmoney_api.md](references/eastmoney_api.md)）
2. 核心核对科目：资产总计、负债合计、所有者权益合计、经营/投资/筹资现金流净额（必须100%一致）
3. 利润表科目允许±5%误差（因PDF解析跨行问题）
4. 将核对结果写入看板的"数据核对"区
5. 若数据不一致，以东方财富F10为准修正 `_core_data.json`

---

## 关键注意事项

### PDF解析常见陷阱

1. **科目名跨行**：A股年报PDF中，部分科目名被排版引擎拆分为2-3行，需使用 `pending_subject` 状态机处理
2. **附注引用**：科目名后常跟"七、74"等附注引用，需正则清理
3. **单位混淆**：三张表单位均为"元"，分析时需转为"亿元"
4. **页码探测**：三张表页码每年不同，必须逐份PDF人工或程序探测

### 数据模板

`_core_data.json` 示例结构：
```json
{
  "2022": {
    "资产总计": 10309876543.21,
    "负债合计": 6615432109.87,
    "营业收入": 6165432109.87,
    ...
  }
}
```

`_metrics.json` 示例结构：
```json
{
  "2022": {
    "流动比率": 0.65,
    "资产负债率%": 64.17,
    "销售毛利率%": 14.83,
    "ROE_归母%": 0.87,
    "杜邦ROE": 0.87,
    "杜邦净利率": 0.35,
    "杜邦总资产周转率": 0.60,
    "杜邦权益乘数": 3.47,
    ...
  }
}
```

### 参考文件

- [cninfo_api.md](references/cninfo_api.md) — 巨潮资讯网API详细参数
- [eastmoney_api.md](references/eastmoney_api.md) — 东方财富F10核对接口
- [metrics_guide.md](references/metrics_guide.md) — 财务指标计算公式与标准值

### 脚本文件

- `scripts/fetch_annual_reports.py` — 年报下载脚本（接受命令行参数）
- `scripts/extract_financial_tables.py` — PDF三表提取脚本（接受命令行参数）
- 可视化看板由AI直接生成HTML（参考 `scripts/generate_dashboard.py` 中的模式），不依赖独立脚本
