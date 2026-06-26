# A 股分析系统 - 安装完成

**安装时间**: 2026-03-01 13:12:12
**安装版本**: v2.9.1 PDF 修复版

## 目录结构

```
workspace/
├── a-share-analysis/          # 技能主目录
│   ├── scripts/               # 脚本文件 (15 个)
│   │   ├── analyze_stock_pro.py      # 主入口
│   │   ├── fetch_realtime_data.py    # 实时行情
│   │   ├── fetch_technical_indicators_free.py  # 技术分析
│   │   ├── fetch_news_sentiment.py   # 新闻情绪
│   │   ├── generate_report_pro.py    # 专业版报告
│   │   ├── generate_report_detailed.py # 详细版报告
│   │   ├── generate_report_commercial.py # 商业版报告
│   │   ├── generate_pdf_report.py    # PDF 报告 (已修复)
│   │   ├── memory_store.py           # 记忆存储
│   │   ├── analysis_tools.py         # 分析工具
│   │   ├── utils.py                  # 通用工具
│   │   ├── organize_reports.py       # 报告整理
│   │   └── firecrawl_auto_auth.py    # Firecrawl 认证
│   ├── README.md              # 使用手册
│   └── ...                    # 其他文档 (20 个)
├── a-share-reports/           # 报告输出 (按股票代码分类)
└── memory/
    └── a-share/               # 股票记忆
```

## 使用方法

### 分析单只股票
```bash
cd workspace/a-share-analysis/scripts
python analyze_stock_pro.py 600519 贵州茅台
```

### 详细版报告
```bash
python analyze_stock_pro.py 600519 贵州茅台 --detailed
```

### 商业版报告
```bash
python analyze_stock_pro.py 600519 贵州茅台 --commercial
```

### 批量分析
```bash
python analyze_stock_pro.py --batch
```

## 依赖要求

- Python 3.8+
- requests
- reportlab

安装依赖：
```bash
pip install requests reportlab
```

## 系统特性

### 核心功能
- ✅ 实时行情（新浪财经 API）
- ✅ 技术分析（东方财富 API）
- ✅ 新闻情绪（Firecrawl，可选）
- ✅ 记忆存储（Elite Memory）
- ✅ 专业版报告（2-3 页）
- ✅ 详细版报告（5-6 页）
- ✅ 商业版报告（8-10 页）
- ✅ PDF 报告（6-8 页，已修复）
- ✅ 错误重试（3 次）
- ✅ 数据缓存（5 分钟）
- ✅ 日志系统
- ✅ 批量分析
- ✅ 报告目录整理

### 报告版本
| 版本 | 章节 | 页数 | 适用场景 |
|------|------|------|----------|
| 专业版 | 10 个 | 2-3 页 | 快速查看 |
| 详细版 | 12 个 | 5-6 页 | 深度研究 |
| 商业版 | 18 个 | 8-10 页 | 商业使用 |
| PDF | 11 个 | 6-8 页 | 专业打印 |

### 目录优化
- ✅ 按股票代码分类存储
- ✅ 自动创建二级目录
- ✅ 所有版本集中管理
- ✅ 便于查找和备份

## 技术支持

详见 `docs/` 目录中的文档。

---

**安装成功！** 🎉

**系统版本**: v2.9.1 PDF 修复版
**最后更新**: 2026-03-01
