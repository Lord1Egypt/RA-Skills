# DataVault OpenClaw 安装指南

> 全球领先的 Web3 Data Value 平台 - 已在 OpenClaw 中开箱即用

---

## 📋 安装步骤

### 方式一：使用 ClawHub（推荐）

```bash
clawhub install datavault
```

### 方式二：手动安装

```bash
# 1. 克隆项目
git clone https://github.com/wangshuniguang/DataVault.git

# 2. 进入目录
cd DataVault

# 3. 安装依赖
pip install -r requirements.txt
```

---

## 🚀 快速使用

### 在 OpenClaw 中直接调用

```
# 获取 BTC 价格
调用 datavault.get_price(symbol="BTC/USDT")

# 获取 ETH 价格  
调用 datavault.get_price(symbol="ETH/USDT")

# 获取市场摘要
调用 datavault.get_market_summary()

# 获取最佳价格
调用 datavault.get_best_price(symbol="BTC/USDT")
```

---

## 📊 全部可用工具（13 个）

### 市场数据（5）
| 工具 | 说明 | 示例 |
|------|------|------|
| `get_price` | 获取单个币种价格 | `symbol="BTC/USDT"` |
| `get_all_prices` | 获取全部价格 | - |
| `get_funding_rate` | 资金费率 | `symbol="BTC/USDT"` |
| `get_market_summary` | 市场摘要 | - |
| `get_best_price` | 跨交易所最优价 | `symbol="BTC/USDT"` |

### 链上数据（3）
| 工具 | 说明 | 示例 |
|------|------|------|
| `get_eth_balance` | ETH 余额 | `address="0x..."` |
| `get_eth_transactions` | ETH 交易历史 | `address="0x..."`, `limit=20` |
| `get_gas_price` | 当前 Gas 价格 | - |

### DeFi 数据（5）
| 工具 | 说明 | 示例 |
|------|------|------|
| `get_defi_tvl` | DeFi 总锁仓量 | `chain="ethereum"` |
| `get_protocol_tvl` | 协议锁仓量 | `protocol="aave"` |
| `get_chain_tvl` | 各链 TVL 排名 | - |
| `get_yields` | 收益率数据 | `protocol="aave"` |
| `get_stablecoins` | 稳定币数据 | - |

---

## 💡 使用示例

### 获取实时价格

```
用户: BTC 现在多少钱?
AI: 
调用 datavault.get_price(symbol="BTC/USDT")
→ 返回: {"symbol": "BTC/USDT", "last": 74350.0, "bid": 74345.0, "ask": 74355.0, ...}
```

### 获取ETH余额

```
用户: 看看 Vitalik 的 ETH 地址有多少钱
AI:
调用 datavault.get_eth_balance(address="0xd8dA6BF26964aF9D7eEd002fE87A6555f0aBc6f8")
→ 返回: {"eth_value": 2445.32, "usd_value": 约 1817 万美元}
```

### 获取DeFi TVL

```
用户: 现在 Defi 市场怎么样?
AI:
调用 datavault.get_defi_tvl()
→ 返回: [{"protocol": "MakerDAO", "tvl": 120亿}, {"protocol": "Aave", "tvl": 95亿}, ...]
```

---

## ⚙️ 配置（可选）

如需使用链上功能，可以配置以下环境变量：

```bash
# .env 文件
ETHERSCAN_API_KEY=your_etherscan_key
```

---

## 🧪 测试

```bash
# 测试 Skill 是否正常工作
cd DataVault
python -c "from skill import get_skill; print(get_skill().health())"
# 输出: {'status': 'healthy', 'version': '1.1.0', 'tools': 13}
```

---

## 📞 支持

- GitHub: https://github.com/wangshuniguang/DataVault
- Discord: https://discord.gg/datavault

---

*DataVault - 全球领先的 Web3 Data Value 平台*