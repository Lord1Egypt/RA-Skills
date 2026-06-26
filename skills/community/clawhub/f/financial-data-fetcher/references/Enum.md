### # 市场类型

| 名称 | 类型 | 数值 | 说明 |
|---|---|---|---|
| .SZ | int | 0 | 深圳交易所 |
| .SH | int | 1 | 上海交易所 |
| .BJ | int | 2 | 北京交易所 |
| .NQ | int | 44 | 新三板 |
| .SHO | int | 8 | 上海个股期权 |
| .SZO | int | 9 | 深圳个股期权 |
| .HK | int | 31 | 港股个股 |
| .US | int | 74 | 美国股票 |
| .CSI | int | 62 | 中证指数 |
| .CNI | int | 102 | 国证指数 |
| .HG | int | 38 | 国内宏观指标 |
| .CFF | int | 47 | 中金期货 |
| .CZC | int | 28 | 郑州期货 |
| .DCE | int | 29 | 大连期货 |
| .SHF | int | 30 | 上海期货 |
| .GFE | int | 66 | 广州期货 |
| .INE | int | 30 | 上海能源 |
| .HI | int | 27 | 港股指数 |

### # dividend_type复权类型

| 名称 | 类型 | 数值 | 说明 |
|---|---|---|---|
| type | str | none | 不复权 |
| type | str | front | 前复权 |
| type | str | back | 后复权 |

### # period周期入参类型

| 名称 | 类型 | 数值 | 说明 |
|---|---|---|---|
| period | str | 1m | 1分钟 |
| period | str | 5m | 5分钟 |
| period | str | 15m | 15分钟 |
| period | str | 30m | 30分钟 |
| period | str | 1h | 60分钟（1小时） |
| period | str | 1d | 1天 |
| period | str | 1w | 1周 |
| period | str | 1mon | 1月 |
| period | str | 1q | 1季 |
| period | str | 1y | 1年 |
| period | str | tick | 分笔 |
