# Bitget 网格交易技能 🟦

专业的 Bitget 交易所网格交易自动化系统，支持多币种并发交易、动态调仓和风险控制。

---

## 🚀 快速开始

### 1. 检查配置

```bash
cd /Users/zongzi/.openclaw/workspace/bitget_data
node bitget-cli.js status
```

### 2. 启动交易

```bash
# 方式 1: 使用 CLI
node bitget-cli.js start

# 方式 2: 直接运行
node start-simple.js

# 方式 3: 交互向导
node quick-start.js
```

### 3. 监控状态

```bash
# 实时监控
node bitget-cli.js monitor

# 查看日志
tail -f grid_monitor.log
```

### 4. 停止交易

```bash
node bitget-cli.js stop
```

---

## 📋 可用命令

### 核心交易命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `monitor` | 监控所有网格 | `node bitget-cli.js monitor` |
| `start` | 启动所有网格 | `node bitget-cli.js start` |
| `stop` | 停止所有网格 | `node bitget-cli.js stop` |
| `balance` | 查询余额 | `node bitget-cli.js balance` |

### 分析优化命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `optimize` | 优化网格参数 | `node bitget-cli.js optimize` |
| `analyze` | 分析交易历史 | `node bitget-cli.js analyze` |
| `kline` | 分析 K 线数据 | `node bitget-cli.js kline` |
| `report` | 生成快速报告 | `node bitget-cli.js report` |

### 动态调整命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `dynamic` | 动态网格调整 | `node bitget-cli.js dynamic` |
| `rebalance` | 组合再平衡 | `node bitget-cli.js rebalance` |
| `scheme-a` | 应用方案 A | `node bitget-cli.js scheme-a` |

### 单币种命令

| 命令 | 说明 | 示例 |
|------|------|------|
| `start-btc` | 启动 BTC 网格 | `node bitget-cli.js start-btc` |
| `start-eth` | 启动 ETH 网格 | `node bitget-cli.js start-eth` |
| `start-sol` | 启动 SOL 网格 | `node bitget-cli.js start-sol` |
| `start-bnb` | 启动 BNB 网格 | `node bitget-cli.js start-bnb` |

---

## 📊 当前配置

### 网格策略 (grid_settings.json)

| 币种 | 网格数 | 价格范围 | 每单金额 | 最大持仓 |
|------|--------|----------|----------|----------|
| BTCUSDT | 50 | 63,000 - 70,000 USDT | 20 USDT | 400 USDT |
| SOLUSDT | 50 | 75 - 95 USDT | 15 USDT | 400 USDT |
| ETHUSDT | 30 | 1,800 - 2,700 USDT | 4 USDT | 150 USDT |
| BNBUSDT | 20 | 610 - 660 USDT | 90 USDT | 600 USDT |

**总需求资金**: ~1,550 USDT

---

## 🔧 配置文件

### config.json - API 凭证

```json
{
  "apiKey": "bg_your_api_key",
  "secretKey": "your_secret_key",
  "passphrase": "your_passphrase",
  "isSimulation": false
}
```

### grid_settings.json - 网格配置

```json
{
  "btc": {
    "symbol": "BTCUSDT",
    "gridNum": 50,
    "priceMin": 63000,
    "priceMax": 70000,
    "amount": 20,
    "maxPosition": 400,
    "sellOrders": 10,
    "buyOrders": 10
  }
}
```

---

## 📁 文件结构

```
bitget_data/
├── config.json                    # API 凭证
├── grid_settings.json             # 网格配置
├── bitget-cli.js                  # 统一 CLI 工具 ⭐
├── quick-start.js                 # 快速启动向导 ⭐
├── setup-cron.js                  # 定时任务设置
│
├── monitor-grid.js                # 监控脚本
├── start-simple.js                # 启动脚本
├── cancel-all.js                  # 取消订单
├── check-balance.js               # 查询余额
│
├── grid-optimizer.js              # 网格优化
├── trade-analyzer.js              # 交易分析
├── kline-analyzer.js              # K 线分析
├── quick-report.js                # 快速报告
│
├── dynamic-adjust.js              # 动态调整
├── dynamic-rebalance.js           # 再平衡
├── apply-scheme-a.js              # 方案 A
│
├── grid_monitor.log               # 监控日志
└── SKILL.md                       # 详细文档
```

---

## ⏰ 定时任务

设置每 5 分钟自动监控：

```bash
node setup-cron.js setup
```

查看定时任务状态：

```bash
node setup-cron.js status
```

---

## 📊 监控与报告

### 实时监控

```bash
# 监控所有网格
node monitor-grid.js

# 查看日志
tail -f grid_monitor.log
```

### 生成报告

```bash
# 快速报告
node quick-report.js

# 交易分析
node trade-analyzer.js

# 网格优化建议
node grid-optimizer.js
```

---

## ⚠️ 风险提示

- **加密货币交易风险极高**，可能导致本金损失
- **先用小额资金测试**，确认策略有效后再增加投入
- **API 密钥只开启现货交易权限**，切勿开启提现权限
- **设置合理的价格区间**，避免网格击穿
- **定期检查网格状态**，确保正常运行

---

## 🔐 安全最佳实践

1. **API 权限**: 仅启用 Spot Read + Spot Trade
2. **IP 白名单**: 限制 API 访问 IP
3. **禁止提现**: 永远不要启用提现权限
4. **文件权限**: `chmod 600 config.json`
5. **定期备份**: 备份 grid_settings.json 和 config.json

---

## 🆘 故障排除

### 签名错误 (Signature Mismatch)

```bash
# 检查 API 密钥格式 (应以 bg_ 开头)
cat config.json | jq .apiKey

# 检查系统时间是否同步
date
```

### 代理连接失败

```bash
# 检查代理是否运行
curl -x http://127.0.0.1:7897 https://api.bitget.com

# 重启代理 (ClashX/Shadowrocket)
```

### 余额不足

```bash
# 检查余额
node check-balance.js

# 减少每单金额或网格数
# 编辑 grid_settings.json
```

### 订单未成交

```bash
# 检查网格价格范围是否覆盖当前市价
node monitor-grid.js

# 调整网格间距 (可能太紧或太宽)
```

---

## 📚 相关文档

- [SKILL.md](./SKILL.md) - 完整技能文档
- [QUANT_STRATEGY.md](./QUANT_STRATEGY.md) - 量化策略说明
- [GRID_OPTIMIZATION_REPORT.md](./GRID_OPTIMIZATION_REPORT.md) - 优化报告

---

## 🎯 常用命令速查

```bash
# 一站式命令
node bitget-cli.js status      # 查看状态
node bitget-cli.js monitor     # 监控
node bitget-cli.js start       # 启动
node bitget-cli.js stop        # 停止
node bitget-cli.js balance     # 余额

# 交互向导
node quick-start.js

# 直接运行
node monitor-grid.js
node start-simple.js
node cancel-all.js
```

---

**版本**: 1.0.0  
**交易所**: Bitget  
**类型**: 现货网格交易  
**最后更新**: 2026-03-10  
**文档**: `/Users/zongzi/.openclaw/workspace/bitget_data/README.md`
