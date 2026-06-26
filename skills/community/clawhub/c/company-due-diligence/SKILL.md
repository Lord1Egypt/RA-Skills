---
name: company-due-diligence
description: 企业尽职调查自动化工具。基于 Playwright/agent-browser 实现多数据源自动抓取，支持企查查、天眼查、东方财富、中国裁判文书网四个网站的综合信息抓取，生成专业尽调报告（含截图+Markdown+PDF）。
---

# 企业尽职调查 Skill (v3.1)

基于 agent-browser (Playwright CLI) 的自动化尽职调查工具，支持企查查、天眼查、东方财富、中国裁判文书网四个数据源的综合查询和报告生成。

## 核心能力

| 功能 | 数据源 | 需登录 | 说明 |
|------|--------|--------|------|
| 工商信息 + 截图 | 企查查/qcc.com | ✅ | 搜索结果截图 + 详情页截图 |
| 工商信息 + 截图 | 天眼查/ty.com | ✅ | 搜索结果截图 + 详情页截图 |
| 股票行情 | 东方财富/eastmoney.com | ❌ | 市值、财务数据 |
| 诉讼记录 | 裁判文书网/wenshu.court.gov.cn | ✅ | 案件数量、案由 |
| **报告生成** | Markdown + PDF | ❌ | 自动生成专业尽调报告 |

## 快速开始

### 1. 安装依赖

```bash
# 安装 agent-browser
npm install -g agent-browser

# 安装 pandoc（用于生成 PDF）
brew install pandoc
```

### 2. 登录数据源（首次使用）

```bash
# 启动浏览器并手动登录
agent-browser --session-name due-diligence --headed open https://www.qcc.com/
agent-browser --session-name due-diligence --headed open https://www.tianyancha.com/

# 登录完成后保存状态
agent-browser --session-name due-diligence state save ~/clawd/skills/company-due-diligence/session/due-diligence.json
```

### 3. 执行尽调

```bash
# 基本用法 - 生成 Markdown + PDF 报告
python3 scripts/query_all_v2.py "xxxxx公司"

# 指定股票代码（上市公司）
python3 scripts/query_all_v2.py "xxxxx公司" --code=sh600816

# 跳过 PDF 生成（仅查询）
python3 scripts/query_all_v2.py "公司名称" --skip-pdf
```

## 输出文件

执行后会在以下位置生成文件：

```
/Users/sunguangning/clawd/reports/due-diligence/
├── xxxxx公司_尽调报告_20260319.md     # Markdown 报告
├── xxxxx公司_尽调报告_20260319.pdf     # PDF 报告
├── xxxxx公司_20260319/               # 截图文件夹
│   ├── 01_qcc_search.png          # 企查查搜索结果
│   ├── 02_qcc_company_detail.png  # 企查查公司详情
│   ├── 03_tyc_search.png          # 天眼查搜索结果
│   ├── 04_tyc_company_detail.png  # 天眼查公司详情
│   ├── 05_eastmoney.png           # 东方财富股票页面
│   ├── 06_wenshu_home.png         # 裁判文书网首页
│   └── 07_wenshu_result.png       # 裁判文书网搜索结果
└── data/                           # 原始数据 JSON
```

## 四网站查询流程

### 企查查 (qcc.com)

1. 打开搜索页并截图
2. 获取搜索结果文本
3. 自动点击进入公司详情页
4. 截图详情页
5. 提取工商信息

### 天眼查 (tianyancha.com)

1. 打开搜索页并截图
2. 获取搜索结果文本
3. 自动点击进入公司详情页
4. 截图详情页
5. 提取工商信息

### 东方财富 (eastmoney.com)

1. 打开股票页面（需指定 --code）
2. 截图
3. 提取市值、财务数据

### 裁判文书网 (wenshu.court.gov.cn)

1. 打开首页并截图
2. 搜索公司名称
3. 截图搜索结果
4. 提取案件数量

## 报告内容

### Markdown 报告包含

1. **公司基本信息** - 工商、注册资本、法人、地址
2. **截图证据** - 所有查询截图的引用
3. **数据摘要** - 各数据源的关键信息
4. **数据来源** - 查询时间和渠道

### PDF 报告

- 自动从 Markdown 转换
- 保持格式完整
- 适合打印和分享

## 会话管理

### 保存登录状态

```bash
agent-browser --session-name due-diligence state save ./session/due-diligence.json
```

### 恢复登录

```bash
agent-browser --session-name due-diligence state load ./session/due-diligence.json
```

## 目录结构

```
company-due-diligence/
├── SKILL.md                    # 本文件
├── scripts/
│   ├── query_all_v2.py         # 四网站整合查询 + 报告生成
│   ├── query_qcc.py           # 企查查查询（独立脚本）
│   ├── query_tyc.py           # 天眼查查询（独立脚本）
│   └── generate_report.py     # 报告生成（备用）
├── session/                   # 登录状态
│   └── due-diligence.json
├── data/                      # 原始数据 JSON
├── references/
│   ├── data_sources.md        # 数据源说明
│   └── framework.md           # 尽调框架
└── assets/
    └── report_template.md     # 报告模板
```

## 报告目录配置

报告中所有路径均使用绝对路径：

| 配置项 | 路径 |
|--------|------|
| 截图目录 | `/Users/sunguangning/clawd/reports/due-diligence/screenshots/` |
| 报告目录 | `/Users/sunguangning/clawd/reports/due-diligence/` |
| 原始数据 | `/Users/sunguangning/clawd/skills/company-due-diligence/data/` |

## 注意事项

### 1. 登录状态

- 企查查、天眼查、裁判文书网需要登录
- 首次使用请手动登录并保存状态
- 定期刷新登录状态

### 2. PDF 生成

- 需要安装 pandoc
- macOS 推荐安装 xelatex：`brew install caskroom/fonts/font-xelatex`
- 如 PDF 生成失败，仍会生成 Markdown 报告

### 3. 截图命名规范

```
01_qcc_search.png           # 企查查搜索结果
02_qcc_company_detail.png  # 企查查公司详情
03_tyc_search.png          # 天眼查搜索结果
04_tyc_company_detail.png   # 天眼查公司详情
05_eastmoney.png           # 东方财富
06_wenshu_home.png         # 裁判文书网首页
07_wenshu_result.png       # 裁判文书网结果
```

## PDF 生成说明

PDF 报告使用专业 HTML 模板生成，流程：
1. Markdown → HTML（pandoc）
2. 应用 CSS 样式模板
3. Chrome 打印为 PDF

**模板特性**：
- A4 页面尺寸
- 渐变色标题和表格
- 响应式布局
- 表格斑马纹
- SWOT 分析卡片样式
- 统计数字高亮

**PDF 工具要求**：
- `pandoc` - Markdown 转 HTML
- `Google Chrome` - HTML 打印为 PDF

---

**版本**: 3.1.0  
**更新**: 2026-03-19  
**功能**: 四网站查询 + 截图 + Markdown报告 + 专业PDF报告
