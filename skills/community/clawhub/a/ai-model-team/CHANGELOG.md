# AI Model Team Changelog

## [2.9.0] - 2026-04-16

### 🐛 Fixed

#### CL 原油数据源修复
- **问题**: CL 被误路由到 Yahoo Finance，`CL`=Colgate股票，价格 $83
- **修复**: 将 CL 加入 `CRYPTO_EXCLUSIONS`，走 OKX 原生价格 $88
- **同时修复**: 新增 19 个大宗商品代码排除（CL/NG/HG/PL/PA/ZC/ZS/ZW/ZL/ZO/ZR/CC/CT/LB/OJ/KC/SB/RC）

### 📝 Kronos 数据不足处理策略
- **决策**: 不调低 lookback 阈值，保持 400 根 K线要求
- **原因**: 宁可缺少一个模型信号，也不牺牲准确率
- **表现**: 数据不足时 Kronos 返回"数据不足"，不强行计算

---

## [2.8.0] - 2026-04-16

### 🐛 Fixed

#### Yahoo Finance ETH 价格 bug
- **问题**: `get_data('ETH-USDT-SWAP')` 返回 $22（Grayscale Ethereum Mini ETF），而不是 ETH 加密货币（$2,349），差 100 倍
- **根因**: `STOCK_SYMBOLS` 变量名语义反了——把"不是股票的币"放在 `STOCK_SYMBOLS` 里，导致 ETH 被误判为股票
- **修复**: 新增 `CRYPTO_EXCLUSIONS` 排除列表，逻辑取反

---

## [2.6.0] - 2026-04-16

### 🆕 Added (Testing & Reliability)

#### 1. 单元测试
- 新增 `tests/` 目录
- 9个单元测试 (pytest)
- 覆盖: Kronos, OKX Data, VADER, Social Sentiment

#### 2. HTTP 缓存
- 新增 `get_data_cached()` 函数
- `lru_cache(maxsize=128)` 避免重复请求
- TTL 支持 (默认60秒)
- `clear_data_cache()` 清除缓存

#### 3. Reddit API 重试机制
- 最多3次重试
- 429限流时自动等待并重试
- 指数退避 (2s, 4s, 6s)

---

## [2.5.0] - 2026-04-16

### 🐛 Fixed (Code Robustness)

#### 1. Kronos Adapter 错误处理
- 添加完整的 try/except 错误处理
- 数据获取失败、模型预测失败时优雅降级
- 返回结构化错误结果而非崩溃

#### 2. Reddit User-Agent 增强
- 增强 User-Agent 字符串（完整浏览器信息）
- Reddit API 被拒时返回 `{"error": "HTTP xxx", "posts_analyzed": 0}`
- 避免崩溃，保证情绪分析继续运行

#### 3. 美股数据支持 (Yahoo Finance)
- 新增 `get_stock_klines()` 函数支持 NVDA/AAPL/MSFT 等美股
- 新增 `get_data()` 自动检测股票/加密货币
- 自动选择 OKX API 或 Yahoo Finance
- 支持: NVDA, AAPL, MSFT, GOOGL, AMZN, TSLA, META 等
- Chronos-2 可对 NVDA 进行预测

---

## [2.4.0] - 2026-04-15

### 🐛 Fixed (Critical - FinBERT 模型加载超时)

#### FinBERT Adapter 重构
- **替换 ProsusAI/finbert** → **VADER (Valence Aware Dictionary)**
  - ProsusAI/finbert 因 `proxies` 参数错误持续加载失败
  - DistilBERT SST2 也加载超时（>60秒）
  - VADER: <1秒加载，即时分析
- **新增金融关键词增强**
  - 30+ bullish 关键词 (surge,rally,pump,breakout,adoption...)
  - 30+ bearish 关键词 (crash,dump,bear,decline,ban...)
  - VADER 70% + 金融关键词 30% 综合评分
- **新增依赖**
  - `vaderSentiment==3.3.2`

### ✅ Other
- FinBERT adapter 重写为 VADER-based 情感分析器
- 移除 `timeout=15` 参数（原用于神经模型超时保护）

---

## [2.3.0] - 2026-04-15

### 🐛 Fixed (CryptoPanic Scraper + FinBERT Timeout)

#### CryptoPanic RSS 替换
- **移除**: `cryptopanic` Python 包（JS动态加载，已损坏）
- **新增**: 10个直接RSS源
  - coindesk, cointelegraph, decrypt (加密)
  - bloomberg, wsj, cnbc, ft (财经)
  - bbc_business, economist, nytimes (综合)
- FinBERT 15秒超时 + 关键词分析回退
- FinBERT 适配器稳定版

### 📝 Documentation
- **docs/KRONOS_MODEL_CARD.md** - 模型透明度文档
- README.md 更新 `post_install.py` 说明
- README.md 更新 `scripts/` 目录列表

---

## [2.2.0] - 2026-04-15

### 🐛 Fixed (Critical - Reproducibility)

#### Dependency Installation
- **timesfm**: `file:///tmp/timesfm` → `git+https://github.com/google-research/timesfm.git@f085b90`
  - 本地路径安装导致其他机器无法复现
  - 改用 GitHub commit hash 确保可复现性
- **chronos-forecasting**: 添加明确的 `git+https` 安装指令
  - 原 requirements.txt 只有注释
  - 补充: `git+https://github.com/amazon-science/chronos-forecasting.git@6d68ed7c4ed2805d122d77b4660765b4089de5ca`
- **Python 版本要求**: `3.14+` → `3.11+`
  - Python 3.14 过于激进，扩大兼容范围

### ✅ Other
- `psutil==7.2.2` 已锁定版本 (审核报告有误)

#### New Files
- **scripts/post_install.py** - 安装后自动修复脚本
  - 自动修复 timesfm 的 `proxies` 参数兼容性问题
  - 验证依赖安装完整性
- **docs/KRONOS_MODEL_CARD.md** - Kronos 模型透明度文档
  - 训练数据说明
  - 模型架构
  - 评估指标
  - 风险提示

---

## [2.1.0] - 2026-04-15

### 🆕 Added

#### Social Sentiment Provider (Major Enhancement)
- **Multi-Subreddit Reddit** - 股票/加密货币多板块搜索
  - Stock symbols: `stocks`, `investing`, `wallstreetbets`, `StockMarket`
  - Crypto symbols: `cryptocurrency`, `BitCoin`, `ethereum`
  - 100 posts fetched (up from 25)
- **General News / International News** - 对股市和数字货币影响极大
  - Reuters World/Business/Markets RSS
  - BBC World/US RSS
  - CNN Business, Guardian Business, WSJ World
- **Four Major News Agencies RSS**
  - Bloomberg (30 entries)
  - WSJ (20 entries)
  - CNBC (30 entries)
  - FT (11 entries)
- **Relevance-Weighted Sentiment**
  - News items scored by relevance to symbol
  - Expanded bullish/bearish keywords (40+)
  - Per-item sentiment score (not just label)

#### FinBERT Enhancement
- **Timeout Protection** - 15秒超时防止无限等待
- **Fallback to Keyword Analysis** - 模型加载失败时自动回退
- **20 News Items Analyzed** - 支持更多新闻源

#### leak_audit.py - 数据泄漏审计
- Timestamp alignment check
- Time window sliding verification
- Future data leakage detection
- Feature leakage check
- Random seed verification

### 🐛 Fixed

- **CryptoPanic Scraper** - 移除broken的JS动态加载爬虫
  - Replaced with extended RSS sources
- **Reddit Sentiment** - 从单一板块扩展到多板块
- **get_news_sentiment()** - 修复调用broken的CryptoPanic
- **FinBERT Model Cache** - 修复不完整的HuggingFace缓存

### 🔧 Changed

- **RSS Sources** - 从5个扩展到10个
- **Reddit Posts** - 从25条扩展到100条
- **Sentiment Weighting** - Reddit 25%, 加密货币 20%, 通用财经 30%, 四大新闻 25%

---

## [2.0.0] - 2026-04-15

### 🆕 Added

#### 模型层
- **FinBERT Adapter** - 新增 FinBERT 金融情绪分析模型
  - `finbert-base` (ProsusAI/finbert)
  - `finbert-crypto` (burakutf/finetuned-finbert-crypto)
  - `finbert-twitter` (StephanAkkerman/FinTwitBERT-sentiment)
- **Four-Model Ensemble** - 四模型协同预测
  - Kronos-base, TimesFM-2.5, Chronos-2, FinBERT-sentiment

#### 数据层
- **OKX Data Provider** - 丰富的市场数据源
  - K线、订单簿、资金费率、持仓量、70+ 技术指标
- **Social Sentiment Provider (增强版)** - 社会情绪数据
  - CryptoPanic 新闻聚合 + 社区投票
  - Reddit r/cryptocurrency 情绪分析
  - CoinDesk/Cointelegraph RSS
  - **去重机制** (精确匹配 + 相似度)
  - **垃圾过滤** (推广帖、机器人检测)
  - **来源权重** (不同来源不同权重)
  - **时间衰减** (半衰期 180 分钟)

#### P0 基础设施 (生产级)
- **CI/CD** - GitHub Actions 冒烟测试
  - 全新环境安装测试
  - 端到端预测链路测试
  - Lock 文件生成
- **data_quality.py** - 数据质量与校验
  - UTC 时区统一
  - 数据完整率检查 (≥98%)
  - Schema 校验 (OHLC 关系)
  - 多源时间对齐 (容忍 60s)
- **risk_control.py** - 风控闸门与熔断
  - 仓位限制 (单标 10%)
  - 止损/止盈 (2%/4%)
  - 日内回撤熔断 (3%)
  - 连亏熔断 (4次 → 60min冷却)
- **observability.py** - 可观测性
  - JSON 结构化日志
  - trace_id/request_id 追踪
  - 指标埋点 (延迟/失败率/新鲜度)
  - Webhook 告警系统
  - 敏感信息脱敏
- **retry.py** - 重试策略
  - 指数退避 (base × 2^attempt)
  - 超时控制 (默认 20s)
  - 熔断模式
- **config.py** - 统一配置管理
  - 所有参数支持环境变量
  - 运行时配置校验
  - 生产环境检查

#### P1 策略增强
- **trading_cost.py** - 交易成本模型
  - 手续费计算 (双向收取)
  - 滑点估算 (按流动性分层)
  - 市场冲击成本
  - 成本后盈利判断
- **validation.py** - Walk-Forward 验证
  - 时序交叉验证 (无数据泄漏)
  - 方向准确率
  - Brier Score (概率校准)
  - Sharpe Ratio / 最大回撤
- **ensemble.py** - 动态加权融合
  - Isotonic 置信度校准
  - 市场状态检测 (趋势/震荡/高波动)
  - 动态权重调整
  - 各模型贡献分析

#### P2 生产级
- **model_registry.py** - 模型注册表
  - 版本追踪 (version/训练数据区间)
  - 特征签名 (SHA256)
  - 状态管理 (active/deprecated)
  - 元数据存储
- **drift_detection.py** - 漂移检测
  - PSI (Population Stability Index)
  - KL 散度
  - 命中率漂移监控
  - 连续漂移告警 (3次触发)
- **execution.py** - 智能订单执行
  - 订单类型选择 (limit/market/post_only)
  - 大单拆分优化
  - 滑点估算
  - 执行重试
- **security.py** - 安全与合规
  - API Key 轮换 (90天)
  - 最小权限原则
  - 审计日志
  - 敏感数据脱敏
- **runbook.py** - 运行手册
  - 常见故障排查指南
  - 配置回滚管理
  - 值班健康检查清单
  - 升级联系人

#### 依赖
- **requirements.txt** - 精确版本锁定
  - 所有依赖使用 `==` 精确版本
  - 可重现构建环境

### 🔧 Changed

- **Chronos Adapter** - 完整重写
  - 支持 `Chronos2Pipeline` (amazon/chronos-2)
  - 正确处理 3D tensor 输出
  - 修复 `torch_dtype` → `dtype`
- **OKX Data Provider** - 修复数据格式兼容
  - 支持 list 和 dict 返回格式
- **All Adapters** - 移除硬编码路径
  - 使用环境变量
- **Error Handling** - 增强错误处理
  - try/except 全覆盖
  - raise_for_status() 检查

### 🐛 Fixed

- `timesfm_adapter.py` - `ForecastConfig` 导入, `tfm.compile()`
- `kronos_adapter.py` - 时间戳列名兼容
- `moirai_adapter.py` - `torch_dtype` 弃用警告
- `model_team.py` - `--social` 参数

### 📦 Files Structure

```
ai-model-team/
├── .github/workflows/ci.yml          # NEW: CI 冒烟测试
├── scripts/
│   ├── data_quality.py              # NEW: P0 数据质量
│   ├── risk_control.py             # NEW: P0 风控
│   ├── observability.py             # NEW: P0 可观测
│   ├── retry.py                    # NEW: P0 重试
│   ├── trading_cost.py              # NEW: P1 成本
│   ├── validation.py                # NEW: P1 验证
│   ├── ensemble.py                 # NEW: P1 融合
│   ├── model_registry.py           # NEW: P2 注册表
│   ├── drift_detection.py          # NEW: P2 漂移
│   ├── execution.py                 # NEW: P2 执行
│   ├── security.py                 # NEW: P2 安全
│   └── runbook.py                  # NEW: P2 手册
```

## [1.0.0] - 2024-XX-XX

### 🎉 Initial Release
- Kronos-base 模型支持
- Chronos-t5-base 模型支持
- TimesFM-2.5 模型支持
- MOIRAI 模型支持
- 基础三模型协同预测
