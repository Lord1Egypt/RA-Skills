# 人工验证清单

> 用于执行者快速补全关键缺失数据

## 缺失指标汇总

| 优先级 | 缺失指标 | 来源卡片 | 数据源 | 获取路径 | 预计耗时 |
|--------|----------|----------|--------|----------|----------|
{{#each missing_items}}
| {{priority}} | {{metric}} | {{card_id}} | {{source_type}} | {{verification_path}} | {{time_estimate}} |
{{/each}}

## 通用验证方法

### arXiv 论文
1. 访问 `https://arxiv.org/abs/{id}`
2. 点击 "PDF" 下载全文
3. 搜索关键词：{{key_metrics}}

### PubMed 论文
1. 访问 PubMed 链接
2. 点击 "Full Text" 或 "Free PMC Article"
3. 如付费：尝试作者机构仓库 / ResearchGate / 邮件联系

### 行业报告
1. 访问官网查找 "Resources" / "Publications"
2. 使用 Wayback Machine 查历史版本
3. 联系机构获取完整版

---

*验证清单格式：操作导向，可复制粘贴*
