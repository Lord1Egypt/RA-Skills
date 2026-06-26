---
name: agent-skills-collector
description: 根据Agent业务类型，从SkillHub (skillhub.tencent.com) 实时搜索收集相关的AI Skills并导出为Excel清单。支持交互式选择数据源。
---

# Agent Skills 收集

根据Agent的业务类型，实时从 SkillHub 搜索收集相关Skills。

## 前置要求

```bash
# 安装 skillhub CLI
npm install -g skillhub

# 安装 Python 依赖
pip3 install openpyxl requests
```

## 快速开始

### 方式1：直接搜索

```bash
skillhub search "hr" --json --search-limit 30
skillhub search "feishu" --json --search-limit 30
```

### 方式2：使用脚本

```bash
python3 scripts/collect_agent_skills.py <agent类型> --keywords "关键词1,关键词2" -o <输出路径>

# 示例
python3 scripts/collect_agent_skills.py hr --keywords "hr,招聘,考勤" -o hr_skills.xlsx
python3 scripts/collect_agent_skills.py it --keywords "k8s,docker,运维" -o it_skills.xlsx
```

## 支持的Agent类型和关键词

| 类型 | 关键词 |
|------|--------|
| hr | hr, resume, recruit, employee, payroll, 招聘, 考勤, 绩效 |
| sales | crm, sales, customer, lead, 销售, 客户, 商机 |
| customer_service | support, ticket, service, 客服, 工单 |
| data_analysis | sql, database, analytics, bi, data, 分析 |
| finance | finance, invoice, tax, 报销, 发票, 税务 |
| it | cloud, k8s, docker, monitoring, security, 运维 |
| marketing | marketing, seo, ads, 营销, 推广 |
| legal | legal, contract, 合规, 合同 |
| content | writing, content, 写作, 文案 |

## 输出格式

Excel包含以下列：名称、关联度、类别、描述、安装命令、标签

## 注意事项

- 每次搜索后等待3-5秒，避免API限流
- 优先使用summary字段（中文描述）
- 根据slug去重