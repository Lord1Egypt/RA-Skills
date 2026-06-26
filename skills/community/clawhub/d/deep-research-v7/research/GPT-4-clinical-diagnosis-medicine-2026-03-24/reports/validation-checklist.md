# 人工验证清单

## 数据源

| 类型 | 数量 | 获取方式 |
|------|------|----------|
| arXiv | 见sources/ | PDF提取脚本 |
| PubMed | 见sources/ | Web Fetcher抓取 |
| Web（可选）| 手动添加 | batch-fetch批量抓取 |

## 缺失指标汇总

| 优先级 | 缺失指标 | 来源卡片 | 获取路径 |
|--------|----------|----------|----------|
| P0 | 样本量 | 待提取 | 运行提取脚本 |
| P0 | AUC/准确率 | 待提取 | 运行提取脚本 |
| P1 | 成本影响 | 待提取 | Web Fetcher |

## 验证方法

### arXiv论文
```bash
python3 scripts/extract-from-pdf.py card-xxx <pdf_url>
```

### PubMed论文
```bash
python3 scripts/fetch-card-from-web.py card-xxx "<pubmed_url>" --domain healthcare
```

### 网页内容
```bash
# 单URL
python3 scripts/fetch-card-from-web.py card-web-001 "<url>" --domain healthcare

# 批量
echo "<url1>" > urls.txt
echo "<url2>" >> urls.txt
python3 scripts/batch-fetch.py urls.txt --domain healthcare
```

---

*验证清单 - 执行者专用*
