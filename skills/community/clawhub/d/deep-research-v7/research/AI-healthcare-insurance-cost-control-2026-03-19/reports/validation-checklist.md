# 人工验证清单

> 用于执行者快速补全关键缺失数据

---

## 缺失指标汇总

| 优先级 | 缺失指标 | 来源卡片 | 数据源 | 获取路径 | 预计耗时 |
|--------|----------|----------|--------|----------|----------|
| **P0** | 样本量 | card-001 | arXiv | 运行提取脚本 | 5分钟 |
| **P0** | AUC/准确率 | card-001 | arXiv | 运行提取脚本 | 5分钟 |
| **P0** | 成本节省 | card-002 | arXiv | 运行提取脚本 | 5分钟 |
| **P1** | 模型性能 | card-006 | PubMed | 访问原文 | 10分钟 |
| **P1** | 样本量 | card-007 | PubMed | 访问原文 | 10分钟 |

---

## arXiv论文验证方法

### 提取命令
```bash
# 提取arXiv论文
python3 scripts/extract-from-pdf.py card-001 "https://arxiv.org/pdf/xxxx.pdf"

# 查看结果
cat /tmp/card-001_extracted.json
```

### 手动验证
1. 访问 `https://arxiv.org/abs/{id}`
2. 点击 "PDF" 下载全文
3. 搜索关键词：accuracy, AUC, cost, sample

---

## PubMed论文验证方法

### 获取全文步骤
1. 访问 PubMed 链接
2. 点击 "Full Text" 或 "Free PMC Article"
3. 如付费：
   - 尝试作者机构仓库
   - 搜索 ResearchGate
   - 邮件联系通讯作者

### 关键数据查找位置
- **样本量**: Methods → Study Population
- **AUC/准确率**: Results → Performance
- **成本**: Results → Cost Analysis

---

## 行业报告验证方法

### 搜索路径
1. Google搜索: `healthcare AI cost savings report 2024`
2. 访问咨询公司官网（McKinsey, BCG, Deloitte）
3. 查找 "Publications" / "Research" 板块

### 验证数据
- 对比多个来源
- 检查数据来源和方法论
- 注意发布日期

---

*验证清单 | 执行者专用*