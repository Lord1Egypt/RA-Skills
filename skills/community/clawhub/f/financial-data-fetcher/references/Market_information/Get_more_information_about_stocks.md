# # 获取股票更多信息get_more_info

### # 获取指定股票更细节的信息

```python
def get_more_info(stock_code:str = '',
					field_list: List = []):
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| stock_code | Y | str | 股票代码 |
| field_list | N | List[str] | 字段筛选，传空则返回全部 |

### # 返回数据

| 数据 | 默认返回 | 数据类型 | 数据说明 |
|---|---|---|---|
| MainBusiness | Y | str | 主营构成 |
| SafeValue | Y | str | 安全分 |
| ShineValue | Y | str | 亮点数 |
| ShapeValue | Y | str | 短期形态+中期形态+长期形态 编号 |
| TPFlag | Y | str | 停牌标识 |
| ZTPrice | Y | str | 涨停价 |
| DTPrice | Y | str | 跌停价 |
| HqDate | Y | str | 行情日期 |
| fHSL | Y | str | 换手率 |
| fLianB | Y | str | 量比 |
| Wtb | Y | str | 委比 |
| Zsz | Y | str | 总市值(亿) |
| Ltsz | Y | str | 流通市值(亿) |
| vzangsu | Y | str | 量涨速 |
| Fzhsl | Y | str | 分钟换手率 |
| FzAmo | Y | str | 2分钟金额(万元) |
| VOpenZAF | Y | str | 抢筹涨幅 |
| ZAF | Y | str | 涨幅 |
| ZAFYesterday | Y | str | 昨日涨幅 |
| ZAFPre2D | Y | str | 前天涨幅 |
| ZAFPre5 | Y | str | 5日涨幅 |
| ZAFPre10 | Y | str | 10日涨幅 |
| ZAFPre20 | Y | str | 20日涨幅 |
| ZAFPre30 | Y | str | 30日涨幅 |
| ZAFPre60 | Y | str | 60日涨幅 |
| ZAFYear | Y | str | 年初至今涨幅 |
| ZAFPreMyMonth | Y | str | 涨幅(本月来) |
| ZAFPreOneYear | Y | str | 涨幅(一年来) |
| Zjl | Y | str | 主买净额(万元) |
| Zjl_HB | Y | str | 主力净流入(万元) |
| TotalBVol | Y | str | 总买量 |
| TotalSVol | Y | str | 总卖量 |
| BCancel | Y | str | 总撤买量 |
| SCancel | Y | str | 总撤卖量 |
| L2TicNum | Y | str | L2逐笔成交数 |
| L2OrderNum | Y | str | L2逐笔委托数 |
| FCAmo | Y | str | 封单额(万元) |
| FCb | Y | str | 封成比 |
| OpenAmo | Y | str | 开盘金额(万元)(A股和板块指数有效) |
| OpenZTBuy | Y | str | 竞价涨停买入金额(万元) |
| OpenAmoPre1 | Y | str | 昨开盘金额(万元) |
| OpenVolPre1 | Y | str | 昨开盘量 |
| CJJEPre1 | Y | str | 昨成交额(万元) |
| CJJEPre3 | Y | str | 3日成交额(万元) |
| FDEPre1 | Y | str | 昨封单额(万元) |
| FDEPre2 | Y | str | 前封单额(万元) |
| ZTGPNum | Y | str | 板块指数的涨停家数 |
| LastStartZT | Y | str | 几天 |
| LastZTHzNum | Y | str | 几板 |
| EverZTCount | Y | str | 连板天 |
| ConZAFDateNum | Y | str | 连涨天数 |
| YearZTDay | Y | str | 年涨停天数 |
| MA5Value | Y | str | 5日均价 |
| HisHigh | Y | str | 52周最高 |
| HisLow | Y | str | 52周最低 |
| IPO_Price | Y | str | 发行价 |
| More_YJL | Y | str | ETF,LOF溢价率 |
| BetaValue | Y | str | 贝塔系数 |
| DynaPE | Y | str | 动态市盈率 |
| MorePE | Y | str | 市盈率(港股:动,其他扩展:静) |
| StaticPE_TTM | Y | str | 市盈率(TTM) |
| DYRatio | Y | str | 股息率 |
| PB_MRQ | Y | str | 市净率(MRQ) |
| IsT0Fund | Y | str | 是否是T+0基金 |
| IsZCZGP | Y | str | 是否是注册制A股 |
| IsKzz | Y | str | 是否是可转债 |
| Kzz_HSCode | Y | str | 可转债对应的正股代码 |
| QHMainYYMM | Y | str | 主力合约关联的月份(期货),主力和次主力 |
| FreeLtgb | Y | str | 自由流通股本(万) |
| Yield | Y | str | 应计利息(债券),占款天数(回购) |
| KfEarnMoney | Y | str | 扣非净利润(万元) |
| RDInputFee | Y | str | 研发费用(万元) |
| CashZJ | Y | str | 货币资金(万元) |
| PreReceiveZJ | Y | str | 合同负债(万元) |
| OtherQYJzc | Y | str | 其它权益工具(万元) |
| StaffNum | Y | str | 员工人数 |
| RecentGGJYDate | Y | str | 最近北上大额交易日 |
| RecentHGDate | Y | str | 最近回购预案日 |
| RecentIncentDate | Y | str | 最近股权激励预案日 |
| NoticeDate_Recent | Y | str | 最近业绩预告日 |
| RecentReleaseDate | Y | str | 最近解禁日 |
| RecentDZDate | Y | str | 最近定增日 |
| ReportDate | Y | str | 最近财报公告日期 |
| ZTDate_Recent | Y | str | 近2年最近涨停板日期 |
| DTDate_Recent | Y | str | 近2年最近跌停板日期 |
| TopDate_Recent | Y | str | 近2年最近龙虎榜日期 |
| StopJYDate_Recent | Y | str | 最近停牌日期 |

### # 接口使用

```python
from tqcenter import tq
tq.initialize(__file__)
more_info = tq.get_more_info(stock_code = '688318.SH', field_list=[])
print(more_info)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
{'MainBusiness': '软件服务收入',
'SafeValue': '98',
'ShineValue': '3',
'ShapeValue': '101308',
'TPFlag': '0',
'ZTPrice': '151.62',
'DTPrice': '101.08',
'HqDate': '20260227',
'fHSL': '0.86',
'fLianB': '0.89',
'Wtb': '-0.66',
'Zsz': '326.91',
'Ltsz': '326.91',
'vzangsu': '2.17',
'Fzhsl': '0.12',
'FzAmo': '514.92',
'VOpenZAF': '0.00',
'ZAF': '1.02',
'ZAFYesterday': '-1.21',
'ZAFPre2D': '1.99',
'ZAFPre5': '-1.56',
'ZAFPre10': '-3.44',
'ZAFPre20': '-10.76',
'ZAFPre30': '-10.13',
'ZAFPre60': '-1.59',
'ZAFYear': '-3.54',
'ZAFPreMyMonth': '-5.23',
'ZAFPreOneYear': '10.27',
'Zjl': '0.00',
'Zjl_HB': '0.00',
'TotalBVol': '1295.00',
'TotalSVol': '3555.00',
'BCancel': '42606.00',
'SCancel': '40266.00',
'L2TicNum': '6880',
'L2OrderNum': '29448',
'FCAmo': '0.00',
'FCb': '0.00',
'OpenAmo': '1069400.00',
'OpenFDE': '0.00',
'OpenAmoPre1': '77.93',
'OpenVolPre1': '61.00',
'CJJEPre1': '26056.68',
'CJJEPre3': '89751.03',
'FDEPre1': '0.00',
'FDEPre2': '0.00',
'ZTGPNum': '0',
'LastStartZT': '0',
'LastZTHzNum': '0',
'EverZTCount': '0',
'ConZAFDateNum': '1',
'YearZTDay': '0',
'MA5Value': '126.56',
'HisHigh': '180.86',
'HisLow': '83.41',
'IPO_Price': '107.41',
'More_YJL': '0.00',
'BetaValue': '2.31',
'DynaPE': '133.10',
'MorePE': '107.56',
'StaticPE_TTM': '94.99',
'DYRatio': '0.28',
'PB_MRQ': '8.82',
'IsT0Fund': '0',
'IsZCZGP': '1',
'IsKzz': '0',
'Kzz_HSCode': '0',
'FreeLtgb': '7935.14',
'Yield': '106.94',
'KfEarnMoney': '9778.22',
'RDInputFee': '5894.58',
'CashZJ': '60954.52',
'PreReceiveZJ': '11281.48',
'OtherQYJzc': '0.00',
'StaffNum': '446',
'RecentGGJYDate': '0',
'RecentHGDate': '0',
'RecentIncentDate': '0',
'NoticeDate_Recent': '0',
'RecentReleaseDate': '20230427',
'RecentDZDate': '0',
'ReportDate': '20251031',
'ZTDate_Recent': '20241008',
'DTDate_Recent': '0',
'TopDate_Recent': '20250625',
'StopJYDate_Recent': '0'}
```
