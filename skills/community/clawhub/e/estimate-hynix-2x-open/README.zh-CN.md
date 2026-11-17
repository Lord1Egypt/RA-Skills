# 海力士两倍做多产品开盘估值

[English README](README.md)

用于估算港股 **南方两倍做多海力士（HKEX：07709）** 合理开盘价或盘中价值的 Agent Skill。它综合：

- 07709最新NAV及二级市场价格；
- 韩国交易所SK海力士普通股（`000660`）；
- 纳斯达克SK海力士ADS（`SKHY`）；
- ADS换股比例及USD/KRW汇率；
- 07709上一交易日的市场折溢价。

该Skill把 **NAV理论价值** 和 **实际成交情景** 分开计算：韩国000660实时涨跌是主锚，美股SKHY隔夜涨跌只做方向验证，ADR绝对平价仅用于诊断跨市场价格失真。

## 输出内容

- 按韩国开盘价或最新价计算的NAV理论价
- 延续07709昨日折溢价的实际成交情景
- 按SKHY隔夜涨跌计算的方向信号价
- ADR隐含韩国普通股价格及跨市场溢价
- 数据过期、跨市场背离、韩国正股极端波动和二级市场折价风险提示

## 运行要求

- Agent能够取得带时间戳的市场行情
- Python 3.9或以上版本
- 内置计算脚本不依赖第三方Python包，也不需要API Key

脚本只负责确定性计算，不自动抓取行情、不保存凭证、不会下单。行情获取和交叉验证由调用该Skill的Agent完成。

## 从ClawHub安装

```bash
clawhub install estimate-hynix-2x-open
```

然后向Agent发送：

```text
使用 $estimate-hynix-2x-open 估算港股07709今天的合理开盘价。
```

## 计算脚本示例

在Skill目录中执行：

```bash
python3 scripts/estimate_open.py \
  --nav-hkd 27.249 \
  --product-prev-market 25.36 \
  --kr-prev-close 1322000 \
  --kr-open 1697000 \
  --kr-current 1628000 \
  --adr-prev-close 126.79 \
  --adr-close 149 \
  --usdkrw 1427.68
```

Windows PowerShell：

```powershell
py -3.10 .\scripts\estimate_open.py `
  --nav-hkd 27.249 `
  --product-prev-market 25.36 `
  --kr-prev-close 1322000 `
  --kr-open 1697000 `
  --kr-current 1628000 `
  --adr-prev-close 126.79 `
  --adr-close 149 `
  --usdkrw 1427.68
```

## 估值模型

```text
韩国正股涨幅 = 韩国锚点价格 ÷ 韩国昨收 - 1
NAV理论价 = 昨日NAV ×（1 + 2 × 韩国正股涨幅 + 跟踪调整）

ADR涨幅 = ADR收盘价 ÷ ADR前收盘价 - 1
ADR信号价 = 昨日NAV ×（1 + 2 × ADR涨幅）

ADR隐含普通股价格 = ADR收盘价 × 每股对应ADS数量 × USDKRW
ADR跨市场溢价 = ADR隐含普通股价格 ÷ 韩国锚点价格 - 1

07709昨日折价 = 昨日市场收盘价 ÷ 昨日NAV - 1
折价延续价 = NAV理论价 ×（1 + 昨日折价）
```

不能用07709昨日市场收盘价作为两倍杠杆计算基准，因为该价格已经包含二级市场折溢价。

## 数据优先级

1. 港股开盘前最新的韩国000660实时价格
2. 韩国000660当日开盘价或盘中最新价
3. 美股SKHY隔夜百分比涨跌
4. 仅在ADR平价偏差较小时使用ADR绝对价格

当ADR绝对平价偏差超过5%时，Skill会把SKHY降级为方向信号，不再作为公平价值锚。

## 风险和限制

- 07709追踪的是 **单日两倍收益**，不是长期持有期间的固定两倍收益。
- Swap和Option容量、做市商库存、申购赎回状态及买卖价差可能导致成交价长期偏离NAV。
- 韩国市场熔断、涨跌停、停牌或延迟行情可能使估值失效。
- ADR发行/注销、结算、流动性和交易时段差异可能造成SKHY平价失真。
- 输出是带时间戳的估值，不是保证成交价格，也不构成投资建议。

数据源优先级和官方产品文件见[方法论说明](references/methodology.md)。

## 许可证

Skill发布到ClawHub后采用MIT-0许可证。

