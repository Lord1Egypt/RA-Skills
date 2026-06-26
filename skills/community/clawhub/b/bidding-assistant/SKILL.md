---
name: bidding-assistant
description: 自动采集盐南高新区、经开区招投标信息；当用户需要定时采集招标网站、筛选特定区域项目、生成PDF日报/月报、推送报到飞书时使用
---

# 招投标信息采集技能

## 概述

自动化采集盐南高新区、经开区相关招投标信息，支持：多网站并行采集、智能区域筛选、数据去重存储、PDF日报/月报生成、飞书推送。

**触发场景**：用户需要监控招标信息、采集特定区域项目、生成招投标日报/推送飞书

## 数据来源（固定排序）

按以下顺序排列，PDF所有页面均遵循此顺序：

1. 盐城市政府采购网
2. 苏服采（API直连）
3. 城南新区公共资源交易网
4. 开发区公共资源交易网
5. 盐城市大数据集团
6. 盐城市都市建设投资集团
7. 盐城市东方集团
8. 江苏世纪新城
9. 经开城发集团
10. 悦达集团

## 核心工作流程

### 1. 执行采集
```bash
cd /Users/ycaz/.openclaw/workspace/skills/bidding-assistant
/usr/bin/python3 scripts/run_daily_collection.py --force
```

### 2. 生成PDF月报
```bash
cd /Users/ycaz/.openclaw/workspace/skills/bidding-assistant
/usr/bin/python3 -c "
import sys; sys.path.insert(0, 'scripts')
from pdf_generator import PDFGenerator
gen = PDFGenerator()
gen.generate_monthly_report(2026, 5)  # 生成指定月份
"
```

### 3. 发送飞书通知
```bash
cd /Users/ycaz/.openclaw/workspace/skills/bidding-assistant
/usr/bin/python3 scripts/generate_and_send_monthly_report.py
```

## PDF报告结构

### 第1页：招标信息概况（日报）
- 标题：招投标信息概况
- 汇总表格（5列）：网站名称 | 当日条数 | 当月条数 | 爬虫策略 | 筛选策略
- 当日总计 + 当月总计

### 第2页：月度概况（月报）
- 标题：招投标信息月度报告
- 统计范围：当月第一天 至 最后一天
- 汇总表格（6列）：网站名称 | 数据条数 | 当日数据 | 前一日数据 | 爬虫策略 | 筛选策略
- 底部求和行
- 按 SITE_ORDER 固定顺序排列

### 第3页：月度平台明细（月报）
每个网站独立一页，表格（4列）：网站 | 日期 | 项目名称 | 链接

- 项目名称列：Paragraph 包裹，触发自动换行（wordWrap='CJK'）
- 链接列：可点击超链接（`<link href="...">` XML 标签）
- 整表：VALIGN=TOP，无固定行高

## 技术要点（PDF生成）

**ReportLab 表格自动换行关键规则**：
1. 表格单元格必须是 `Paragraph` 对象，普通字符串不会触发换行
2. `ParagraphStyle` 必须设置 `wordWrap='CJK'`（中文）或 `wordWrap='LTR'`
3. `TableStyle` 设为 `VALIGN='TOP'`（不能用 MIDDLE）
4. **禁止**设置固定 `ROWHEIGHT`，否则换行失效
5. 可点击链接用 `Paragraph` + `<link href="url" color="blue" underline="yes">text</link>`

## 数据库路径

- 数据库：`~/.openclaw/workspace/skills/bidding-assistant/招投标数据/history.db`
- 表结构：`bidding_projects`（source_site, publish_date, project_name, detail_url）

## 区域筛选规则

- **目标区域**：盐南高新区、经开区
- **排除区域**：亭湖、盐都、响水、滨海、建湖、大丰、射阳、阜宁、东台
- 筛选基于项目标题关键词匹配

## 飞书推送配置

- 目标群 ID：`oc_7cecd47c4c8e7fdb5233f8343df7d59f`
- 私发用户 ID：`oc_a06e78cf3e4b06479ec27c54af2a5623`
- 使用 IM API 上传文件（不是 Drive API）
- 上传：`POST /im/v1/files` → 返回 `file_key`
- 发送：`POST /im/v1/messages` → `content: {"file_key": xxx}`

详细配置见 `references/飞书企业自建应用配置指南.md`

## Cron 定时任务

Job ID：`27f7ac6354da`
- 调度：每天 `0 7 * * *`
- 执行：采集 + PDF生成 + 飞书群推送
- 推送目标：飞书群 `oc_7cecd47c4c8e7fdb5233f8343df7d59f`

## 项目结构

```
bidding-assistant/
├── SKILL.md
├── references/
│   ├── 飞书企业自建应用配置指南.md
│   ├── 飞书推送配置说明.md
│   └── PDF报告排版说明.md          # 当前PDF排版规范
└── scripts/
    ├── crawler.py                    # 采集器基类和所有网站采集器
    ├── sufu_crawler_final.py         # 苏服采采集器（API直连版）
    ├── pdf_generator.py              # PDF日报/月报生成器（核心）
    ├── feishu_enterprise_app.py      # 飞书开放平台API客户端
    ├── generate_and_send_monthly_report.py  # 生成并发送月报
    ├── generate_monthly_pdfs.py       # 月报PDF生成入口
    └── run_daily_collection.py        # 每日采集任务入口
```

## 依赖

```
requests>=2.28.0
beautifulsoup4>=4.11.0
lxml>=4.9.0
reportlab>=4.0.0
openpyxl>=3.1.0
apscheduler>=3.10.0
```

## Python 环境

**必须使用 `/usr/bin/python3`**，系统默认 `python3` 在 macOS 上指向不同路径，reportlab 等库安装在此路径下。

