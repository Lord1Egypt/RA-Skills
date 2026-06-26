---
name: bid-watcher
description: |
  投标情报监控系统。监控锂电池/储能/装配段行业招标信息，追踪4家竞争对手（无锡先导、海目星、赢合科技、联赢激光）的投标动态。每周自动采集、生成表格报告并发送邮件。
---

# 投标情报监控 Skill

## 目标公司

| 编号 | 公司名称 | 关键词 |
|------|---------|--------|
| 1 | 无锡先导智能装备股份有限公司 | 先导智能 |
| 2 | 海目星激光科技集团股份有限公司 | 海目星 |
| 3 | 深圳市赢合科技股份有限公司 | 赢合科技 |
| 4 | 深圳市联赢激光股份有限公司 | 联赢激光 |

## 监控关键词

- `锂电池`
- `储能`
- `装配段`
- `锂电设备`
- `电池生产设备`

## 信息来源

1. **搜索引擎**: Bing 搜索（按关键词 + "招标" 搜索）
2. **待扩展**: 政府采购平台、招标雷达、剑鱼标讯 API

## 采集字段

每个招标机会记录以下字段：
- `投标时间`: 招标截止时间/开标时间
- `预算`: 项目预算金额
- `公司名称`: 招标方/采购方
- `公司背景`: 采购方主营业务、规模
- `是否有采购历史`: 之前是否采购过同类设备
- `历史供应商`: 之前在哪家供应商采购的
- `原文链接`: 招标公告链接
- `发现时间`: 抓取时间
- `竞争公司`: 关联哪家竞争公司
- `优先级`: S/A/B/C 四级评分
- `相关性`: 高/低

## 工作流程（TaskFlow）

```
[每周定时触发]
     ↓
[Step 1] search_bids.py     搜索招标信息（行业平台）
     ↓
[Step 2] enrich_bids.py    提取公司/预算 + 优先级评分
     ↓
[Step 3] generate_report.py  生成周报（Markdown + Excel）
     ↓
[Step 4] 历史存档            data/history/
```

## 文件结构

```
bid-watcher/
├── SKILL.md
├── flows/
│   └── bid-monitor.lobster   # TaskFlow 定义
├── scripts/
│   ├── search_bids.py        # 搜索招标信息
│   ├── enrich_bids.py        # 提取公司/预算 + 优先级评分
│   ├── generate_report.py   # 生成周报（Markdown/Excel）
│   └── send_email.py        # 发送邮件
└── data/
    ├── bids_raw_YYYYMMDD.json         # 原始搜索结果
    ├── bids_parsed_enriched_YYYYMMDD.json  # 补充背景后数据
    ├── bid_report_W*.md            # 周报 Markdown
    ├── bid_report_W*.xlsx        # 周报 Excel
    └── history/
        └── week_YYYYWW.json            # 每周完整数据存档
```

## 优先级评分规则

| 维度 | 加分 | 说明 |
|------|------|------|
| 有预算金额 | +1 | |
| 大预算（≥1000万） | +1 | |
| 公司在已知背景库中 | +1 | |
| 有明确投标时间 | +1 | |
| 标题含"储能"/"锂电"/"动力电池" | +1 | |
| 竞争公司自身招标 | -2 | 排除 |

最终评分：S(≥4分) / A(3分) / B(2分) / C(≤1分)

## 使用方式
```bash
# 搜索招标信息
python scripts/search_bids.py

# 提取公司/预算 + 优先级评分
python scripts/enrich_bids.py

# 生成报告（Excel格式，默认）
python scripts/generate_report.py --format excel

# 生成报告（Markdown + Excel）
python scripts/generate_report.py --format both
```

### 参数
| 参数 | 说明 | 默认值 |
|------|------|-------|
| --format | 输出格式 | excel |

### 自动触发
- **手动触发**: "运行投标监控" 或直接执行 `python scripts/*.py`
- **自动**: 每周一 09:00 自动执行，通过 cron 调度

## 邮件配置

需要配置以下环境变量：
- `BID_SMTP_HOST`: 邮件服务器（如 smtp.gmail.com）
- `BID_SMTP_PORT`: 端口（如 587）
- `BID_SMTP_USER`: 用户名
- `BID_SMTP_PASS`: 密码
- `BID_REPORT_TO`: 收件人邮箱（多个用逗号分隔）

配置示例：
```bash
export BID_SMTP_HOST=smtp.gmail.com
export BID_SMTP_PORT=587
export BID_SMTP_USER=your-email@gmail.com
export BID_SMTP_PASS=your-app-password
export BID_REPORT_TO=team@company.com
```

## 状态输出

采集完成后输出：
- 本周新发现机会数量
- 各竞争公司相关机会数
- 优先级分布（S/A/B/C 各多少条）
- 高相关招标数量
- 报告文件路径
- 邮件发送状态
