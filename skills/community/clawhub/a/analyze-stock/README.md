# 📈 stock-analysis

股票分析技能 - 提供买卖点判断、仓位管理、基本面分析

## 🚀 快速开始

### 1. 安装技能

```bash
# 从 ClawHub 安装
openclaw skill install stock-analysis

# 或从本地安装
openclaw skill install ~/.openclaw/workspace/skills/stock-analysis
```

### 2. 配置 API Key

**必需配置：** TUSHARE_TOKEN

```bash
# 复制示例文件
cd ~/.openclaw/workspace/skills/stock-analysis
cp .env.example .env

# 编辑 .env 文件，填入你的 TUSHARE_TOKEN
nano .env
```

**可选配置：** BAIDU_API_KEY、TAVILY_API_KEY（用于消息面分析）

### 3. 使用技能

#### 方式 1：对话触发
```
分析股票 601117
股票分析 中国化学
看股票 300515
```

#### 方式 2：命令行
```bash
python3 scripts/analyze_stock.py --stock 601117
python3 scripts/analyze_stock.py --stock 601117 --style balanced
```

#### 方式 3：OpenClaw 调用
```python
ctx.claw.skills.run("stock-analysis", {
    "stock_code": "601117",
    "style": "balanced"
})
```

## 📊 功能特性

1. **核心价格区间与买卖点** - 基于 PE 分位计算 5 档估值区间
2. **仓位管理策略** - 三步建仓法 + 止损止盈
3. **关键观察信号** - 量能、均线、消息面实时分析
4. **基本面分析** - 最新一期财报 + 前两年年报
5. **一致性预期** - 机构评级、目标价、业绩预测
6. **利好与风险** - 5 维度深度分析（各 5 点）
7. **投资总结** - 机会点、风险点、操作建议

## 📁 文件结构

```
stock-analysis/
├── SKILL.md              # 技能描述
├── __init__.py           # 技能入口
├── scripts/
│   └── analyze_stock.py  # 核心分析脚本
├── references/           # 参考资料
│   ├── fundamental_analysis.md
│   ├── position_management.md
│   └── valuation_zones.md
├── .env.example          # 环境变量示例
├── .gitignore            # Git 忽略文件
└── README.md             # 使用说明（本文件）
```

## ⚙️ 配置说明

### 环境变量

| 变量 | 用途 | 必需 | 获取方式 |
|------|------|------|----------|
| `TUSHARE_TOKEN` | 获取财务数据 | ✅ | https://tushare.pro |
| `BAIDU_API_KEY` | 百度搜索新闻 | ❌ | 百度智能云 |
| `TAVILY_API_KEY` | 深度分析 | ❌ | https://tavily.com |
| `TUSHARE_API_URL` | API 地址 | ❌ | 默认官方 API |

### 投资风格

| 风格 | 参数 | 说明 |
|------|------|------|
| 保守型 | `conservative` | 只做超低估/低估区，仓位≤50% |
| 平衡型 | `balanced` | 低估/合理区操作，仓位 50%-80% |
| 进取型 | `aggressive` | 合理区顺势加仓，仓位最高 80% |

## 📝 输出示例

```
📈 个股分析报告
股票代码：601117.SH
股票名称：中国化学
当前价格：¥9.10
PE 分位：31.3%

一、核心价格区间与买卖点
...
七、投资总结
【机会点】
1. 估值合理（PE 分位 31.3%），具备配置价值
2. 高成长性（营收增速 39.5%），业绩弹性大

【风险点】
1. 毛利率偏低（11.0%），议价能力弱

【操作建议】
• 策略：逢低吸纳，稳健加仓
• 仓位：建议 40%-60%
```

## 🔧 开发调试

```bash
# 测试运行
cd ~/.openclaw/workspace/skills/stock-analysis
python3 scripts/analyze_stock.py --stock 601117

# 查看日志
tail -f /tmp/stock-analysis.log
```

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📞 支持

- 问题反馈：ClawHub Issue
- 讨论交流：OpenClaw 社区
