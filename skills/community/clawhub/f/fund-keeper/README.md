# Fund Keeper v2.7 🦞

国内场外基金智能顾问 - 帮你省时间、赚外快

## 功能特性

### 📊 核心功能
- **实时估值** - 多数据源获取基金净值
- **买卖建议** - 基于技术指标和历史分位
- **止盈止损** - 自动提醒，不错过机会
- **离线模式** - 户外工作也能用

### 💰 收益管理
- **收益统计** - 总投入、总收益、收益率
- **可视化图表** - 持仓分布、收益对比、趋势图
- **买卖记录** - 完整交易历史追踪

### 🌟 特色功能
- **贵金属投资** - 黄金、白银实时价格 + 投资建议
- **定投管理** - 设置定投计划，自动提醒
- **基金搜索** - 按名称/代码搜索基金
- **持仓管理** - 编辑、删除基金

## 快速开始

```bash
# 查看持仓
py fund_keeper.py portfolio

# 收益统计（含图表）
py fund_keeper.py stats --chart

# 贵金属投资报告
py fund_keeper.py gold

# 搜索基金
py fund_keeper.py search --name 芯片

# 买卖建议
py fund_keeper.py advice

# 离线模式
py fund_keeper.py portfolio --offline
```

## 安装

```bash
# 克隆或下载
git clone https://github.com/your-username/fund-keeper.git

# 安装依赖
pip install requests pandas

# 运行
cd fund-keeper
py fund_keeper.py portfolio
```

## 命令列表

| 命令 | 说明 |
|------|------|
| `portfolio` | 查看持仓和实时估值 |
| `advice` | 买卖建议 |
| `stats` | 收益统计 |
| `trend` | 收益趋势 |
| `gold` | 贵金属投资报告 |
| `search` | 搜索基金 |
| `edit` | 编辑持仓 |
| `remove` | 删除持仓 |
| `buy` | 买入记录 |
| `sell` | 卖出记录 |
| `history` | 交易历史 |
| `sip` | 定投管理 |
| `alert` | 止盈止损提醒 |
| `config` | 配置管理 |

## 配置

首次运行会自动创建配置文件：

```
funds/
  ├── my-funds.md         # 持仓数据
  ├── config.json         # 配置
  ├── cache.json          # 缓存
  ├── transactions.json   # 交易记录
  └── stats_history.json  # 收益历史
```

## 数据源

- 天天基金网（主）
- 东方财富（备）
- 新浪财经（备）
- AKShare（备）

## 适用人群

- 户外工作者（支持离线模式）
- 基金小白（零代码操作）
- 定投党（自动提醒）
- 搞钱党（收益可视化）

## 许可证

MIT License

## 作者

皮儿 🦞