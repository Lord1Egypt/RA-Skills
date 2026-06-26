---
name: btc-chain-data-api
display_name: BTC链上数据查询
description: 查询比特币链上结构数据（UTXO、大额流出、筹码分布、持仓结构、链上指标等）
metadata:
  openclaw:
    emoji: "📊"
    requires:
      bins: ["python3"]
      env: []
---

# 🚀 BTC Chain Data API 使用方式

所有表统一支持以下三种基础查询方式：

---

## 1️⃣ 默认查询（最新1条）
python btc_api.py <table>

示例：
python btc_api.py bigamountvoutv3e

---

## 2️⃣ limit查询（最近N条）
python btc_api.py <table> <limit>

示例：
python btc_api.py bigamountvoutv3e 10

---

## 3️⃣ 时间查询（指定日期数据）
python btc_api.py <table> <YYYY-MM-DD>

示例：
python btc_api.py bigamountvoutv3e 2026-03-31

---

## 4️⃣ 字段查询（最新1条）
python btc_api.py <table> <field>

示例：
python btc_api.py dailyindsv3e1 price
python btc_api.py holder3 holder_30

---

## 5️⃣ 字段 + limit查询（最近N条）
python btc_api.py <table> <field> <limit>

示例：
python btc_api.py dailyindsv3e1 price 10

---

## 6️⃣ 字段 + 日期查询（当天数据）
python btc_api.py <table> <field> <YYYY-MM-DD>

示例：
python btc_api.py dailyindsv3e1 price 2026-03-31

---

## ⚠️ 注意
- 同一请求仅支持单一附加参数
- 不支持 limit + date 同时使用
- 参数顺序固定：table → field → limit/date
---

# API地址
http://10.168.1.162:9000

# 数据表与字段说明

---

## bigamountvoutv3e（大额UTXO输出记录）
- vout
- voutn
- vouttype
- amount
- height
- txid
- days
- buyprice
- sellprice
- profit

---

## dailyindsv3e1（链上日级指标）
- height_begin
- height_end
- profitrate
- fees
- txs
- new_address
- total_address
- new_address_volume
- active_address
- send_address
- receive_address
- volume
- eavolume
- sopr：SOPR
- asopr
- easopr
- lthsopr
- sthsopr
- asol
- eaasol
- dormancy
- adormancy
- eadormancy
- cdd
- sacdd
- eacdd
- day1
- day7
- day30
- day60
- day90
- day180
- day365
- day730
- csupply
- mintusd
- sumcsupply
- sumcdd
- sumeacdd
- liveliness
- ealiveliness
- rprofit
- rloss
- rplrate
- price
- marketcap
- rcap
- earcap
- mvrv
- nupl
- vdd
---

## dailyindsv3e2（扩展估值指标）
- height_begin
- height_end
- lth_volume
- frm
- cvdd
- realized_price
- transferred_price
- balanced_price
- nvt_ratio
- velocity
---

## holder3（持币人数结构）
- holder_0
- holder_1
- holder_2
- holder_3
- holder_4
- holder_5
- holder_6
- holder_7
- holder_15
- holder_30
- holder_60
- holder_90
- holder_180
- holder_360
- holder_540
- holder_720
- holder_1080
- holder_1440
- holder_1800
- holder_2160
- holder_2520
- holder_2880
- holder_3240
- holder_3600
- holder_3960

---

## holder_balance3（持币资金结构）
- holder_balance_0
- holder_balance_1
- holder_balance_2
- holder_balance_3
- holder_balance_4
- holder_balance_5
- holder_balance_6
- holder_balance_7
- holder_balance_15
- holder_balance_30
- holder_balance_60
- holder_balance_90
- holder_balance_180：
- holder_balance_360
- holder_balance_540：
- holder_balance_720
- holder_balance_1080
- holder_balance_1440
- holder_balance_1800
- holder_balance_2160
- holder_balance_2520
- holder_balance_2880
- holder_balance_3240
- holder_balance_3600
- holder_balance_3960

---

## realtimeindsv3（实时链上指标）
- mempool_size
- mempool_fees

---

## rt_bigamountvoutv3e（实时大额UTXO输出记录）
- vout
- voutn
- vouttype
- amount
- height
- txid
- days
- buyprice
- sellprice
- profit

---

## rt_dailyindsv3e1（实时链上日级指标）
- height_begin
- height_end
- profitrate
- fees
- txs
- new_address
- total_address
- new_address_volume
- active_address
- send_address
- receive_address
- volume
- eavolume
- sopr
- asopr
- easopr
- lthsopr
- sthsopr
- asol
- eaasol
- dormancy
- adormancy
- eadormancy
- cdd
- sacdd
- eacdd
- day1
- day7
- day30
- day60
- day90
- day180
- day365
- day730
- csupply
- mintusd
- sumcsupply
- sumcdd
- sumeacdd
- liveliness
- ealiveliness
- rprofit
- rloss
- rplrate
- price
- marketcap
- rcap
- earcap
- mvrv
- nupl
- vdd
---

## rt_dailyindsv3e2（实时扩展估值指标）
- height_begin
- height_end
- lth_volume
- frm
- cvdd
- realized_price
- transferred_price
- balanced_price
- nvt_ratio
- velocity
---

## utxos3nd（UTXO余额分布结构）
- balance_amount_0
- balance_amount_001
- balance_amount_01
- balance_amount_1
- balance_amount_10
- balance_amount_100
- balance_amount_1000
- balance_amount_10000

---

## utxosv3（UTXO结构统计）
- total_address
- total_balance
- total_rcap
- miner_address
- miner_balance
- balance_0
- balance_001
- balance_01
- balance_1
- balance_10
- balance_100
- balance_1000
- balance_10000
- uprofit
- uloss
- lthnupl
- sthnupl
- lthmarketcap
- lthrcap
- sthmarketcap
- sthrcap
- lthmvrv
- sthmvrv

---

## utxosv4（UTXO盈利与供给结构）
- profit_addresses
- loss_addresses
- profit_ratio
- lth_supply
- sth_supply
- realized_price
- relative_lth_sth
- lth_profit_supply
- lth_loss_supply
- lth_profit_ratio
- sth_profit_supply
- sth_loss_supply
- sth_profit_ratio
- slrv_ratio
---




