# 企业尽职调查 Skill

基于 agent-browser (Playwright CLI) 实现企查查、天眼查、东方财富、中国裁判文书网四网站综合查询 + 自动截图。

## 快速开始

### 1. 安装

```bash
# 安装 agent-browser
npm install -g agent-browser

# 安装 pandoc 和 wkhtmltopdf（用于生成PDF）
brew install pandoc wkhtmltopdf
```

### 2. 登录数据源

```bash
# 启动浏览器会话
agent-browser --session-name due-diligence --headed open https://www.qcc.com/

# 登录企查查、天眼查、东方财富、裁判文书网

# 登录完成后保存状态
agent-browser --session-name due-diligence state save ./session/due-diligence.json
```

### 3. 执行查询

```bash
# 四网站整合查询 + 自动截图 + 生成Markdown和PDF报告
python3 scripts/query_all_v2.py "建元信托股份有限公司"

# 跳过PDF生成（仅查询+截图）
python3 scripts/query_all_v2.py "公司名称" --skip-pdf
```

## 支持的数据源

| 数据源 | 功能 | 需登录 |
|--------|------|--------|
| 企查查 | 工商信息、股东、风险 | ✅ |
| 天眼查 | 工商信息、股东、风险 | ✅ |
| 东方财富 | 股票行情、市值、财务 | ❌ |
| 裁判文书网 | 诉讼记录 | ✅ |

## 截图功能

- 截图保存到：`/Users/sunguangning/clawd/reports/due-diligence/screenshots/`
- 文件夹命名：`公司名称_YYYYMMDD`
- 每次查询自动创建新文件夹

## 查询示例

```bash
# 查询公司
python3 scripts/query_all_v2.py "中国银联股份有限公司"

# 指定股票代码（上市公司）
python3 scripts/query_all_v2.py "建元信托股份有限公司" --code=sh600816
```

## 文件结构

```
company-due-diligence/
├── SKILL.md
├── README.md
├── scripts/
│   ├── query_all_v2.py    # 四网站整合查询 + 截图
│   └── generate_report.py  # 报告生成
├── session/               # 登录状态
│   └── due-diligence.json
└── data/                   # 查询结果

/reports/due-diligence/
├── screenshots/
│   └── 公司名称_YYYYMMDD/  # 每个公司一个文件夹
│       ├── 01_qcc_search.png
│       ├── 02_qcc_company_detail.png
│       ├── 03_tyc_search.png
│       ├── 04_eastmoney.png
│       ├── 05_wenshu_home.png
│       └── 06_wenshu_result.png
└── due-diligence/
    └── 报告.md
```

## 注意事项

1. 首次使用需登录企查查、天眼查、裁判文书网
2. 使用 `agent-browser state save` 保存登录状态
3. 截图自动保存到 reports/due-diligence/screenshots/ 目录
