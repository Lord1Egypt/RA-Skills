---
name: auto-weekly-system
description: 全自动周报系统。定时收集v3.5、InStreet、价格监控等数据，生成周报并发布到企业微信文档。当需要自动化报告生成、团队数据同步、定时数据汇总时使用。
---

# Auto Weekly System

## 快速使用

生成本周报告：
```bash
python3 scripts/generate_weekly.py
```

发布到企业微信：
```bash
python3 scripts/publish.py --title "项目周报 2026-03-21"
```

完整流程（生成+发布）：
```bash
python3 scripts/full_pipeline.py
```

## 功能模块

### 1. 数据收集 (collector.py)
- v3.5 生产数据
- InStreet 回复统计
- 价格监控变动
- 系统健康检查

### 2. 报告生成 (generator.py)
- Markdown 格式化
- 数据可视化（表格、趋势）
- 异常高亮

### 3. 发布系统 (publisher.py)
- 创建企业微信文档
- 写入 Markdown 内容
- 返回分享链接

## 定时任务

建议设置：
```bash
# 每周五下午5点自动生成并发布
cron add --name "auto-weekly" --schedule "0 17 * * 5" \
  --command "python3 /path/to/full_pipeline.py"
```

## 数据依赖

- `/tmp/v35_migration_config.json` - v3.5配置
- `/tmp/agent_v35_production.log` - v3.5运行日志
- `/tmp/instreet_reply.log` - InStreet日志
- `/tmp/price_monitor_db.json` - 价格数据库
