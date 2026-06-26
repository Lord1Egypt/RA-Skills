# A股收盘报告 Skill

基于 A股早盘提醒 skill 改造，增加主力资金状况分析。

## 功能

- 获取四大指数（上证、深证、创业板、沪深300）收盘数据
- 涨跌分布统计
- **主力资金净流入/净流出分析**
- 热门板块追踪
- 成交额汇总
- 智能操作建议

## 快速开始

```bash
# 测试运行（不发送）
node scripts/closing-summary.mjs

# 发送到飞书
node scripts/closing-summary.mjs --send
```

## 数据来源

- 东方财富股票 API
- 腾讯股票 API（备用）

## 文件结构

```
a-stock-evening/
├── SKILL.md           # Skill 定义
├── README.md          # 说明文档
└── scripts/
    └── closing-summary.mjs  # 主脚本
```

## Cron 配置

```bash
openclaw cron add "10 15 * * 1-5" --skill a-stock-evening -- --send
```

每天 15:10（A股收盘后）自动执行。