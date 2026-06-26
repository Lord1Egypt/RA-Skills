---
name: decision-briefing-claw
description: 每日经营数据自动汇总与简报推送助手（决策简报虾）。从多个数据源（数据库/API/Excel/飞书多维表格）采集关键业务指标，自动计算同比环比，生成结构化简报，并推送到飞书/邮件/企业微信等渠道。激活场景：(1) 需要每日自动汇总经营数据；(2) 想要定时收到业务进展简报；(3) 需要将散落在多个系统的数据整合到一份报告；(4) 希望决策层快速了解昨日经营状况；(5) 需要追踪关键 KPI 的每日变化。触发关键词：每日简报、经营数据、数据汇总、自动报告、定时推送、业务简报、日报、数据看板、KPI 汇总、经营日报、自动汇报、数据摘要。
---

# 决策简报虾 (decision-briefing-claw)

每日经营数据自动汇总与简报推送。从多数据源采集 → 计算 KPI → 生成简报 → 多渠道推送 → 自动归档。

## 工作流程

### 步骤 1：了解配置需求

首次使用时，询问用户：
- 数据源类型（数据库/API/Excel/飞书多维表格）及连接信息
- 需要监控的核心指标（收入、订单数、用户数等）
- 推送时间（如每天 09:00）和推送渠道（飞书群/个人/邮件）
- 简报模板偏好（极简/标准/详细/高管版）

### 步骤 2：数据采集

使用 `scripts/data-collector.py` 从配置的数据源采集数据：

```bash
# 验证数据源连接
python3 scripts/data-collector.py validate --source <name>

# 采集所有数据源
python3 scripts/data-collector.py collect --all

# 测试单条 SQL
python3 scripts/data-collector.py test --query "SELECT COUNT(*) FROM orders WHERE DATE(created_at) = CURDATE() - INTERVAL 1 DAY"
```

数据源配置详见 `references/data-sources.md`。

### 步骤 3：计算 KPI 与异常检测

- 计算同比（YoY）、环比（MoM/DoD）
- 标记超出阈值或大幅波动的异常数据
- 指标计算规则详见 `references/metrics-calculation.md`

### 步骤 4：生成简报

使用 `scripts/report-generator.sh` 生成并推送简报：

```bash
# 生成简报（指定模板）
./scripts/report-generator.sh generate --template standard

# 推送到飞书
./scripts/report-generator.sh push --channel feishu

# 归档
./scripts/report-generator.sh archive --date $(date +%Y-%m-%d)
```

简报模板详见 `references/report-templates.md`。

### 步骤 5：配置定时任务

使用 OpenClaw cron 或系统 crontab 设置定时触发：

```bash
# 每天早上 9:00 触发（crontab 示例）
0 9 * * * cd /path/to/skill && python3 scripts/data-collector.py collect --all && ./scripts/report-generator.sh generate --template standard && ./scripts/report-generator.sh push --channel feishu
```

### 步骤 6：归档与追溯

简报自动保存到 `reports/YYYY-MM-DD.md`，支持历史查询：

```bash
./scripts/report-generator.sh history --days 7
```

## 配置文件结构

```
config/
├── data-sources.json    # 数据源连接配置
└── channels.json        # 推送渠道配置
reports/                 # 归档简报目录
```

## 与其他 Skill 协作

- 发现异常数据 → 调用 **auto-data-analysis-claw** 深度分析
- 生成正式月报 → 调用 **financial-report-render-claw** 渲染
- 获取战略建议 → 调用 **strategy-advisor-claw**
- 推送到更多平台 → 调用 **cross-platform-messenger-claw**

## 常见问题

- 数据库连接超时 → 检查网络权限，增加 `connect_timeout`
- 推送失败 → 检查 webhook/token 是否有效，配置重试
- 时区错乱 → 统一使用 `Asia/Shanghai`，SQL 中显式转换时区
- SQL 慢 → 添加索引或改用数据仓库查询
