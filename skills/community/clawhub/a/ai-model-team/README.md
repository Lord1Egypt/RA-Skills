# AI Model Team

**Version:** 2.9.2
**Release Date:** 2026-04-16

---

## v2.9.2 技能目录结构修复 (2026-04-16)

### 🏗️ 结构优化

**问题：** `ai-model-team` 原位于 `okx-agent-trade-kit/skills/` 嵌套目录，OpenClaw 无法识别。

**修复：** 将 6 个 OKX 技能移至 `skills/` 根目录：
- `okx-cex-market/` — 行情数据
- `okx-cex-trade/` — 交易执行
- `okx-cex-portfolio/` — 账户查询
- `okx-cex-bot/` — 网格/DCA机器人
- `okx-cex-earn/` — 赚币产品
- `okx-cex-skill-mp/` — MCP工具

**影响：** OpenClaw `skills list` 现在可正确显示所有 OKX 技能。

---

## v2.9.1 数据分页 + Chronos 兼容性修复 (2026-04-16)

### 🐛 修复内容

#### 1. OKX 数据分页（核心修复）

**问题：** OKX `/market/history-candles` 单次最多返回 300 条数据。Kronos 需要 400 条，导致 BTC 等长上线标的也报"数据不足"。

**修复：** `_fallback_klines` 实现分页逻辑，用 `after` 参数翻页，最多可获取 600+ 条数据。

```python
# 修复前：单次请求，最多 300 条
df = get_klines("BTC-USDT-SWAP", bar="4H", limit=500)  # 永远只有 300 条

# 修复后：自动分页，500 条全部取回
# _fallback_klines 内部循环请求，拼满 limit=500 为止
```

#### 2. Chronos `dtype` 参数兼容性

**问题：** `chronos-forecasting >= 2.0` 的 `Chronos2Pipeline.from_pretrained()` 不再支持 `dtype` 参数，传入后报错：

```
TypeError: Chronos2Model.__init__() got an unexpected keyword argument 'dtype'
```

**修复：** 移除 `Chronos2Pipeline` 和 `ChronosPipeline` 调用中的 `dtype` 参数。

```diff
# chronos_adapter.py
- Chronos2Pipeline.from_pretrained(self.hf_name, device_map='cpu', dtype=torch.float32)
+ Chronos2Pipeline.from_pretrained(self.hf_name, device_map='cpu')

- ChronosPipeline.from_pretrained(self.hf_name, dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32)
+ ChronosPipeline.from_pretrained(self.hf_name)

- forecast = pipeline.predict([torch.tensor(context, dtype=torch.float32)], ...)
+ forecast = pipeline.predict([torch.tensor(context)], ...)
```

#### 3. TimesFM 源码永久化

**问题：** TimesFM 源码 patch（修复 `proxies`/`dtype` 等参数兼容）放在 `/tmp` 目录，机器重启后丢失，TimesFM 重新报错。

**修复：** patch 后的 TimesFM 源码复制到 `skills/ai-model-team/.venv/src/timesfm`，通过 editable install 永久加载。

```
skills/ai-model-team/.venv/src/timesfm/  ← 永久存储，含所有 patch
```

#### 4. `okx_data_provider` 分页触发条件

**问题：** 原来只有 `not candles` 时才走分页，但 OKX CLI 返回数据量可能少于 limit 但非空。

**修复：** 改为 `if not candles or len(candles) < limit`，数据量不足即触发分页。

---

### 📋 本次修改的文件

| 文件 | 修改内容 |
|------|---------|
| `scripts/okx_data_provider.py` | 分页逻辑 + 触发条件修复 |
| `scripts/chronos_adapter.py` | 移除 dtype 参数 |
| `.venv/src/timesfm/` | TimesFM patch 永久化 |

---

### ⚠️ 安装注意事项

**本 skill 不支持 `pip install -r requirements.txt` 直接安装**，因为：

1. TimesFM 的 `huggingface_hub` 版本要求与 `transformers` 存在冲突
2. 需要使用本 skill 自带的 `.venv` 虚拟环境

**正确安装方式：**

```bash
cd skills/ai-model-team

# 1. 创建虚拟环境（已在 .gitignore 中，不会被提交）
python3 -m venv .venv

# 2. 安装依赖（自动跳过冲突包）
.venv/bin/pip install numpy pandas requests PyYAML httpx httpcore vaderSentiment tqdm click rich joblib
.venv/bin/pip install torch transformers huggingface_hub tokenizers huggingface_hub==0.34.1 transformers==4.52.0
.venv/bin/pip install einops feedparser pytest scipy scikit-learn
.venv/bin/pip install "chronos-forecasting>=2.0"

# 3. 安装 TimesFM（从 patch 后的源码）
# 源码已保存在 .venv/src/timesfm/，通过 editable install 加载
.venv/bin/pip install -e . --no-deps
```

**或使用一键安装：**

```bash
cd skills/ai-model-team
./scripts/install.sh
```

---

## v2.9.0 CL数据源路由修复 (2026-04-16)

### 🐛 Bug 修复

| 问题 | 修复前 | 修复后 |
|------|--------|--------|
| **CL 原油价格** | Yahoo Finance `CL`=Colgate股票 $83 | OKX 原生价格 $88 |
| **Kronos 数据不足** | 84 bars (误路由) | 254 bars (OKX数据) |

### ⚠️ Kronos 数据不足说明

**不调低 lookback 阈值，保持 400 根 K线要求。**

某些标的（如 CL-USDT-SWAP）在 OKX 上线时间较短，历史数据不足 400 根 4H K线。Kronos 会直接返回"数据不足"而不强行计算，以保护预测准确性。

这不是 bug，是**有意为之的设计决策**：宁可缺少一个模型信号，也不牺牲准确率。

---

## 使用说明

### 快速开始

```bash
cd skills/ai-model-team

# 激活虚拟环境
source .venv/bin/activate

# 四模型分析（4H周期）
python scripts/model_team.py BTC-USDT-SWAP --models kronos,chronos-2,timesfm,finbert

# 指定周期（15m / 30m / 1H / 4H）
python scripts/model_team.py CL-USDT-SWAP --timeframe 1H --models kronos,chronos-2,timesfm,finbert

# 仅看信号（简洁模式）
python scripts/model_team.py BTC-USDT-SWAP --signal-only

# JSON 输出（程序化使用）
python scripts/model_team.py BTC-USDT-SWAP --json
```

### 多周期对比

```bash
# 对比不同周期的 Kronos 信号
for tf in 15m 30m 1H 4H; do
  python scripts/model_team.py BTC-USDT-SWAP --models kronos --timeframe $tf
done
```

### 支持的交易对

| 格式 | 类型 | 示例 |
|------|------|------|
| `XXX-USDT-SWAP` | 永续合约 | `BTC-USDT-SWAP`, `ETH-USDT-SWAP` |
| `XXX-USDT` | 现货 | `BTC-USDT` |
| `CL-USDT-SWAP` | 商品指数 | 原油（CL）|

### 支持的时间周期

| 周期 | 适用场景 | 说明 |
|------|---------|------|
| `15m` | 短线精细分析 | 数据量大，但噪音多 |
| `30m` | 短线参考 | 平衡精度与噪音 |
| `1H` | 中线分析 | CL 等上线较短的合约推荐 |
| `4H` | 主用周期 | 噪音少，信号稳定（**推荐**）|

### 周期与数据量

OKX `/market/history-candles` 单次最多 300 条，通过分页可获取 600+ 条。

| 周期 | 300 条覆盖时间 | 600 条覆盖时间 |
|------|--------------|--------------|
| `15m` | ~3 天 | ~6 天 |
| `30m` | ~6 天 | ~12 天 |
| `1H` | ~12 天 | ~25 天 |
| `4H` | ~50 天 | ~100 天 |

---

## 模型详情

| 模型 | 机构 | 专长 | 权重 |
|------|------|------|------|
| **Kronos-base** | NeoQuasar | 加密K线（庄家行为/洗盘识别） | 30% |
| **Chronos-2** | Amazon | 宏观周期 / 分位数预测 | 25% |
| **TimesFM-2.5-200M** | Google | 通用时序 | 25% |
| **FinBERT-sentiment** | HuggingFace | 金融情绪分析 | 20% |

### Kronos 特殊说明

Kronos 需要 **≥400 条 K线**才能计算。如果 OKX 历史数据不足，Kronos 会返回 `neutral (30/100)` 并标注"数据不足"。这是有意为之，不强行降低阈值。

**解决方案：** 对于历史数据较短的合约（如 CL），使用更小周期（如 `1H`）来获得足够数据量。

---

## 信号阈值

```python
BULLISH_THRESHOLD = 2.0   # 看多：预测涨幅 > +2.0%
BEARISH_THRESHOLD = -2.0 # 看空：预测跌幅 > -2.0%
# ±2.0% 区间内 → neutral
```

**风控闸门：** 综合置信度 < 0.6 时阻止交易。

---

## 目录结构

```
ai-model-team/
├── SKILL.md
├── README.md                   # 本文档
├── CHANGELOG.md
├── requirements.txt
│
├── .venv/                     # Python 虚拟环境（不在 git 中）
│   └── src/timesfm/           # TimesFM 永久化 patch 源码
│
└── scripts/
    ├── model_team.py          # ⭐ 主入口
    ├── kronos_adapter.py      # Kronos
    ├── chronos_adapter.py    # Chronos-2
    ├── timesfm_adapter.py    # TimesFM
    ├── finbert_adapter.py    # VADER 情绪
    └── okx_data_provider.py  # OKX 数据 + 分页
```

---

## 故障排除

### TimesFM 加载失败

```bash
# 检查 TimesFM 源码是否在正确位置
ls .venv/src/timesfm/__init__.py

# 如果不存在，从 /tmp 重新复制
cp -r /tmp/timesfm-repo/src/timesfm .venv/src/

# 验证
.venv/bin/python -c "from timesfm import TimesFM_2p5_200M_torch; print('OK')"
```

### Chronos dtype 报错

```bash
# 检查 chronos_adapter.py 中是否还有 dtype 参数
grep "dtype=" scripts/chronos_adapter.py

# 应该无输出（dtype 已全部移除）
```

### Kronos 数据不足

```bash
# 检查 OKX 实际数据量
curl "https://www.okx.com/api/v5/market/history-candles?instId=BTC-USDT-SWAP&bar=4H&limit=300"
# 如果 data 数组 < 300 条，说明历史确实不足

# 换更小周期
python scripts/model_team.py BTC-USDT-SWAP --timeframe 1H --models kronos
```

---

## 更新日志

| 版本 | 日期 | 内容 |
|------|------|------|
| v2.9.2 | 2026-04-16 | 技能目录结构修复（从嵌套目录移至 skills/ 根目录，OpenClaw 可识别） |
| v2.9.1 | 2026-04-16 | OKX分页+Chronos dtype兼容+TimesFM永久化+完整文档 |
| v2.9.0 | 2026-04-16 | CL数据源路由修复 |
| v2.8.0 | 2026-04-16 | ETH数据源路由修复 |
| v2.7.0 | 2026-04-16 | 单元测试+缓存+重试 |
| v2.2.0 | 2026-04-15 | 可复现性修复 |

---

## 许可证

MIT License

---

⚠️ **免责声明**：本工具仅供参考，不构成投资建议。模型预测存在不确定性，请理性投资。
