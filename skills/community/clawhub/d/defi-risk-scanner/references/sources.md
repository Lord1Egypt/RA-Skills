# DeFi Risk Scanner - 参考数据源与检查清单

## 免费 API 汇总

### TVL / 协议数据
- **DefiLlama**: `https://api.llama.fi/protocol/{name}` — 无需 Key，返回 TVL、chain、category
- **DeBank**: `https://api.debank.com/v1/protocol?id={id}` — 需 Key，免费注册
- **DappRadar**: `https://api.dappradar.com/v2/{chain}/protocols` — 需 Key

### 代币安全
- **Token Sniffer**: `https://token-sniffer.com/api/v2/token/{address}` — 无需 Key，返回 scamScore、honeypot
- **Rug Check**: `https://rugcheck.xyz/tokens/{address}` — 无需 Key

### 合约分析
- **Etherscan API**: `https://api.etherscan.io/api` — 免费 Key 有频率限制
- **Tenderly**: `https://api.tenderly.co/api/v1/public_contract/{chain}/{address}` — 需注册
- **Blockscout** (L2): `https://blockscout.com/{chain}/api` — 免费

### 解锁/归属
- **Token Unlocks API**: `https://token.unlocks-api.com/v1/protocol/{name}` — 免费
- **Vest.watch**: `https://vest.watch/api/projects` — 免费

### 审计报告
- **Immunefi**: `https://immunefi.com/` — Bug Bounty 列表
- **OpenZeppelin**: `https://blog.openzeppelin.com/security-audits/` — 公开审计

## 常见高风险模式清单

### 🔴 立即排除
- [ ] 合约未开源/未验证
- [ ] 无 Timelock，管理员可直接提取资金
- [ ] LP 代币未锁定
- [ ] 总供应量无上限
- [ ] Honeypot（只能买不能卖）
- [ ] 无 Vesting，团队/私募立即解锁
- [ ] 仅有 Telegram 群，无任何公开身份
- [ ] 审计报告中有未修复高危漏洞

### 🟡 需要深入调查
- [ ] 团队匿名（但有公开代码贡献记录）
- [ ] 预挖超过 15%
- [ ] TVL < $100k（容易被操控）
- [ ] 仅有小所上线
- [ ] 无活跃 Bug Bounty
- [ ] 合约使用复杂代理模式但未解释原因

### 🟢 加分项
- [ ] 知名审计公司（ToB, OZ, Certik, Spearbit）
- [ ] 活跃 Bug Bounty >$1000
- [ ] 多签 + Timelock
- [ ] TVL 稳定增长 >6个月
- [ ] 开源代码 + 文档完善
- [ ] 公开团队身份（LinkedIn 可查）
- [ ] 已上线主流交易所/CEX

## 评分权重参考

| 维度 | 权重 |
|------|------|
| 合约安全（审计、验证、权限） | 30% |
| Tokenomics（分配、Vesting、通胀） | 25% |
| 流动性与 TVL | 20% |
| 团队与社区 | 15% |
| 市场数据（交易量、价格稳定性） | 10% |

## 常用快捷查询 URL

- Etherscan: `https://etherscan.io/address/{address}`
- DexScreener: `https://dexscreener.com/` — DEX 实时数据
- CoinGecko: `https://www.coingecko.com/en/coins/{id}` — 代币基础数据
- DeFi Llama: `https://defillama.com/protocol/{name}` — 协议 TVL
- RugCheck: `https://rugcheck.xyz/tokens/{address}` — Rug Pull 检查
- Token Unlocks: `https://token.unlocks.io/` — 代币解锁日历
