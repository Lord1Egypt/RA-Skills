# GPT-4 clinical diagnosis medicine 深度研究报告

> **版本**: v6.0 Universal  
> **生成时间**: 2026-03-24  
> **领域**: healthcare

---

## 方法论说明

- **检索策略**: arXiv + PubMed + Web（可选）多源检索
- **数据来源**: 见 sources/ 目录
- **提取逻辑**: 
  - arXiv/PMC: PDF全文提取
  - PubMed: Web Fetcher抓取
  - Web: Web Fetcher抓取

---

## 集成工具

### Web Fetcher
- **用途**: 抓取网页/PubMed内容
- **命令**: `python3 scripts/fetch-card-from-web.py <card_id> <url> --domain healthcare`
- **批量**: `python3 scripts/batch-fetch.py urls.txt --domain healthcare`

### PDF提取
- **用途**: 提取arXiv/PMC论文全文
- **命令**: `python3 scripts/extract-from-pdf.py <card_id> <pdf_url>`

---

## 卡片索引

[见 sources/ 目录]

---

**报告版本**: v6.0 Universal + Web Fetcher集成  
**溯源验证**: 待完成
