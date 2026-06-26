---
name: crypto-market
description: "加密货币行情分析：本技能自带 Binance 公开行情 + 指标脚本；资讯用 web_search/web_fetch。"
version: 1.0.0
metadata:
  openclaw:
    requires:
      anyBins:
        - python3
        - python
---

# 加密货币行情分析

## OpenClaw 内置工具

| 用途 | 工具 |
|------|------|
| 行情与技术指标 JSON | **`exec`** + `{baseDir}/crypto_market_snapshot.py` |
| 资讯 | **`web_search`**、**`web_fetch`**（重要链接必须 **fetch** 正文） |

说明：

- OpenClaw **不**内置 **`ccxt`**。本包脚本使用 **Binance 公开 REST**（`api.binance.com`），**标准库**，无需 `pip install ccxt`。
- 若你的网关另有 **`ccxt`** 工具，可改用网关实现；字段语义以你方工具文档为准，本技能脚本输出结构见下节。

### 代理（可选）

脚本会读取 **`CRYPTO_HTTP_PROXY`** 或系统 **`HTTPS_PROXY`/`HTTP_PROXY`**，与容器访问外网一致即可。

---

## 调用本包脚本（exec）

```bash
python3 "{baseDir}/crypto_market_snapshot.py" BTCUSDT 1d 200
```

参数：`SYMBOL`（如 `BTCUSDT`，无斜杠）、`interval`（如 `1d`、`4h`）、`limit`（K 线条数，默认 200）。

### 输出 JSON 要点

- **ticker_24h**：Binance `/api/v3/ticker/24hr`
- **ohlcv_meta.last_row**：最后一根 OHLCV
- **indicators**：`sma_20`、`rsi_14`、`macd_12_26_9`、`bollinger_20_2`、`atr_14` 的 **latest**
- 分析须基于上述字段，**勿编造**未返回的数值

---

## 分析流程

1. 解析用户币种：默认现货 **`BTCUSDT`** 形式（用户说 BTC 则映射 `BTCUSDT`）。
2. **`exec`** 拉取脚本 JSON；可按需多次换 `interval`。
3. 技术面归纳（趋势、超买超卖、波动等）。
4. **`web_search`** + **`web_fetch`** 做资讯与情绪侧写。
5. 在对话中整合输出完整分析结论与风险提示。

---

## 合规与约束

- **不构成投资建议**；若 Binance 不可用，说明原因并可部分依赖资讯。
- 新闻结论须有 **`web_fetch`** 正文依据，不得仅用搜索摘要。
