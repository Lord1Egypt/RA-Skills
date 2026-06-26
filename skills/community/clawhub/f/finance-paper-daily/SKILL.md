---
name: finance-paper-daily
description: 每日金融学术论文自动抓取并生成 Excel 报告。从 arXiv (q-fin)、Semantic Scholar、OpenAlex、Google Scholar 四个来源获取最新金融领域论文（量化金融、资产定价、风险管理、算法交易、FinTech等），整理成格式化 Excel 文件保存到用户桌面，文件名为 YYYY-MM-DD_finance_papers.xlsx。当用户说"抓取今日论文"、"更新论文报告"、"获取金融论文"、"生成论文 Excel"时触发。
---

# Finance Paper Daily

每日金融学术论文抓取 → 桌面 Excel 报告。

## 数据源

| 来源 | API | 覆盖方向 |
|------|-----|----------|
| arXiv | 官方免费 | q-fin 全分类（量化金融） |
| Semantic Scholar | 官方免费 | 金融关键词全文搜索 |
| OpenAlex | 官方免费（无需 key） | Economics/Finance 概念 |
| Google Scholar | scholarly 库（非官方） | 广泛覆盖，尽力而为 |

## 使用方式

运行脚本：

```bash
pip3 install openpyxl scholarly --break-system-packages -q
python3 scripts/fetch_papers.py
```

## 输出

- 路径：`~/Desktop/YYYY-MM-DD_finance_papers.xlsx`
- Sheet1「每日论文」：按日期倒序，含标题/作者/摘要/来源/链接，颜色区分来源
- Sheet2「来源统计」：各来源论文数量汇总

## 注意

- 首次运行需安装依赖：`pip3 install openpyxl scholarly --break-system-packages`
- Google Scholar 抓取不稳定，失败时自动跳过
- 每次运行覆盖同一天的文件（重复运行安全）
