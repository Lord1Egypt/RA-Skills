# AI doctor versus human doctor diagnosis accuracy benchmark 深度研究 - 执行摘要

> 生成时间: 2026-03-24 | 领域: healthcare

## 核心结论

### ✅ 已验证结论
- [待填充] 需运行提取脚本获取具体数据

### ⚠️ 待验证结论
- [待填充] 基于摘要的线索

## 可直接行动
- [P0] 运行 `python3 scripts/extract-from-pdf.py` 提取arXiv论文
- [P1] 访问PubMed链接获取摘要详情
- [P1] 使用Web Fetcher抓取网页内容（如有Web源）

## Web Fetcher使用
```bash
# 单URL抓取
python3 scripts/fetch-card-from-web.py card-web-001 "<url>" --domain healthcare

# 批量抓取
python3 scripts/batch-fetch.py urls.txt --domain healthcare --prefix web
```

---

*执行摘要 - 决策者专用*
