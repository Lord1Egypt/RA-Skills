# Stock Monitor Pro

> 全功能智能股票监控预警系统 - A股投资者的得力助手

## ✨ 核心功能

### 🔔 七大预警规则

| 规则 | 说明 | 示例 |
|------|------|------|
| 成本百分比 | 盈利/亏损达到设定比例 | 盈利15%提醒，亏损12%止损 |
| 日内涨跌幅 | 单日涨跌超过阈值 | 个股±4%，ETF±2% |
| 成交量异动 | 放量/缩量异常 | 放量>2倍均量 |
| 均线金叉死叉 | MA5上穿/下穿MA10 | 金叉买入信号 |
| RSI超买超卖 | RSI>70超买，<30超卖 | 超卖反弹机会 |
| 跳空缺口 | 向上/向下跳空>1% | 缺口回补预期 |
| 动态止盈 | 盈利后回撤提醒 | 盈利10%后回撤5%减仓 |

### 🤖 AI 深度分析（付费版）

- **技术面分析**：价格走势、支撑压力位
- **消息面分析**：新闻影响、市场情绪
- **操作建议**：买入/持有/卖出建议

### 📊 交易信号（付费版）

基于多指标生成交易信号：
- signal: buy / sell / hold
- confidence: 0.0-1.0 置信度
- target_price: 目标价
- stop_loss: 止损价

## 🚀 快速开始

### 安装

```bash
npx clawhub@latest install stock-monitor-pro
```

### 配置

编辑 `scripts/monitor.py`，修改 `WATCHLIST`：

```python
WATCHLIST = [
    {
        "code": "002459",
        "name": "晶澳科技",
        "market": "sz",
        "type": "individual",
        "cost": 16.275,        # 持仓成本
        "shares": 16900,       # 持仓数量
        "alerts": {
            "cost_pct_above": 25.0,   # 盈利25%提醒
            "cost_pct_below": -20.0,  # 亏损20%止损
            "change_pct_above": 3.0,  # 日内异动
            "change_pct_below": -3.0,
            "volume_surge": 2.0       # 放量2倍
        }
    }
]
```

### 运行

```bash
cd scripts
./control.sh start    # 启动监控
./control.sh status   # 查看状态
./control.sh log      # 查看日志
```

## 💰 版本对比

| 功能 | 免费版 | 付费版 |
|------|--------|--------|
| 预警规则 | 3 个 | 7 个 |
| AI 分析 | ❌ | ✅ |
| 交易信号 | ❌ | ✅ |
| 价格 | ¥0 | ¥19.9/月 |

## 📖 文档

- [SKILL.md](./SKILL.md) - 完整使用文档
- [VERSIONS.md](./VERSIONS.md) - 版本说明

## 📝 更新日志

- **v3.1** - 增加 AI 深度分析、交易信号
- **v3.0** - 完成 7 大预警规则
- **v2.0** - 新闻舆情分析

## 📄 License

MIT

---

**作者**: 小柏 (xiaobai-ai)  
**联系方式**: ClawHub Issues
