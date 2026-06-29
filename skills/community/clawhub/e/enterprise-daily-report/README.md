---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: e296badcf090102ccb780dbc89230083_ad3e03b5648111f18383525400d9a7a1
    ReservedCode1: ktAzpz6X70009lOt/EzjB43G+XfPRSmB+3P/aXfXhNcwRfjZs1e4orkFt0BhKuH5VQ72xMmcLmn9y8EpveRknwWSuKJMFIaxOCMecBDHMyowD51EqSlpG+FKj93EAhRt3iKHA5/vitg7xXaVi4dWCojZsul/fynsehIwVDo1zFZgz7Y+mUuoz//w6d8=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: e296badcf090102ccb780dbc89230083_ad3e03b5648111f18383525400d9a7a1
    ReservedCode2: ktAzpz6X70009lOt/EzjB43G+XfPRSmB+3P/aXfXhNcwRfjZs1e4orkFt0BhKuH5VQ72xMmcLmn9y8EpveRknwWSuKJMFIaxOCMecBDHMyowD51EqSlpG+FKj93EAhRt3iKHA5/vitg7xXaVi4dWCojZsul/fynsehIwVDo1zFZgz7Y+mUuoz//w6d8=
---

# 企业日报生成器

> AI-Powered Daily Report Generator

## 简介

自动从多个数据源（CSV/JSON/Git）采集工作数据，通过AI智能分类和摘要，生成结构化日报。支持 Markdown / HTML / PDF 三种格式，支持邮件自动发送。

## 功能亮点

- **多源数据集成**：CSV、JSON、Git提交记录一键导入
- **AI智能分类**：自动将任务归类到「今日完成」「进行中」「明日计划」「问题与风险」「需要支持」
- **多格式输出**：Markdown（本地预览）、HTML（邮件/网页）、PDF（正式归档）
- **一键发送**：配置SMTP后自动发送到指定邮箱

## 安装

```bash
# 安装依赖
pip install pandas jinja2 reportlab

# 可选：PDF输出需要 wkhtmltopdf
# Windows: choco install wkhtmltopdf
# macOS: brew install wkhtmltopdf
# Ubuntu: sudo apt install wkhtmltopdf
```

## 使用方法

### 基础用法

```bash
# 从CSV生成日报（Markdown）
python scripts/generate_report.py --csv ./data/today.csv

# 从Git仓库生成日报
python scripts/generate_report.py --git /path/to/repo --format html

# 多数据源 + 发送邮件
python scripts/generate_report.py --csv ./data/tasks.csv --git ./my-project --send
```

### 在OpenClaw中使用

只需说出：
- "帮我生成本日工作日报"
- "生成今日工作汇报"
- "daily report"

技能会自动触发，根据你的数据源配置生成日报。

## 数据格式

### CSV数据源格式

| 字段 | 类型 | 说明 |
|------|------|------|
| type | string | 任务类型（编码/会议/文档/测试） |
| content | string | 任务描述 |
| status | string | 状态（done/in_progress/todo/blocked） |
| author | string | 负责人 |

### 输出示例

```markdown
# 每日工作汇报
**日期**: 2026年06月10日

## 今日完成
- 完成用户登录模块开发（done） - 张三
- 修复订单页面样式问题（done） - 李四

## 进行中
- API接口文档编写（in_progress） - 王五

## 问题与风险
- 支付回调偶发性超时，需排查（blocked） - 张三
```

## 定价

$19.9（一次性购买，终身使用）

## 版本

v1.0.0 — 2026年6月10日发布
*（内容由AI生成，仅供参考）*
