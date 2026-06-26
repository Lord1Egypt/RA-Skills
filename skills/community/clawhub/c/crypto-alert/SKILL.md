# crypto-alert

加密貨幣價格監控與提醒技能

## 功能

- 取得加密貨幣現價
- 顯示 24 小時漲跌幅
- 支援多種主流幣種
- 暴漲/大跌提醒

## 安裝依賴

```bash
pip3 install requests
```

## 使用方式

```bash
# 查看所有熱門幣種
python3 crypto.py

# 查詢特定幣種
python3 crypto.py 比特幣
python3 crypto.py 以太坊
python3 crypto.py btc
```

## 支援幣種

| 指令 | 幣種 |
|------|------|
| 比特幣 / btc | Bitcoin (BTC) |
| 以太坊 / eth | Ethereum (ETH) |
| sol | Solana (SOL) |
| bnb | Binance Coin (BNB) |
| xrp | XRP (XRP) |
| doge | Dogecoin (DOGE) |
| ada | Cardano (ADA) |
| dot | Polkadot (DOT) |

## API 數據源

使用 Binance API 獲取即時價格數據

---

*版本：1.0 | 建立日期：2026-03-16*

## Author
- Kuanlin (GitHub: kuanlin)

