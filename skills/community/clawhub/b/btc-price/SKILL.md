---
name: okx-crypto-price
description: 从 OKX 公开行情接口一次性获取指定币种现货价格（美元展示），按输入顺序输出。适用于用户提到 OKX、币价查询、top-cryptocurrency、指定币种价格等场景。
metadata: { "openclaw": { "emoji": "💱", "requires": { "bins": ["python"] } } }
---

# okx-crypto-price

一次性获取 OKX 指定币种现货价格（`$` 展示），并按你输入的币种顺序输出。每个币种优先选择 `USDT > USDC > USD` 计价对。

## 用法（Windows / PowerShell）

```bash
python ".openclaw/workspace/skills/btc-price/scripts/okx_symbol_prices.py" --symbols BTC,ETH,SOL
```

可选参数：

- 超时（秒）：

```bash
python ".openclaw/workspace/skills/btc-price/scripts/okx_symbol_prices.py" --symbols BTC,ETH,SOL --timeout 20
```

- JSON 输出（方便程序读取）：

```bash
python ".openclaw/workspace/skills/btc-price/scripts/okx_symbol_prices.py" --symbols BTC,ETH,SOL --format json
```

