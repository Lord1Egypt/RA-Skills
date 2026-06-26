# # 获取证券基本信息get_stock_info

### # 根据股票，获取股票基础的财务数据

```python
get_stock_info(cls,
				stock_code:str,
				field_list: List = []) -> Dict:
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| stock_code | Y | str | 证券代码 |
| field_list | Y | List[str] | 字段筛选，不能为空 |

### # 返回数据

| 数据 | 默认返回 | 数据类型 | 数据说明 |
|---|---|---|---|
| Name | Y | str | 证券名称 |
| Unit | Y | str | 交易单位 |
| VolBase | Y | str | 量比的基量 |
| MinPrice | Y | str | 最小价格变动 |
| XsFlag | Y | str | 价格小数位数 |
| Fz[8] | Y | List[str] | 开收市时间（4段） |
| DelayMin | Y | str | 延时分钟数 |
| QHVolBaseRate | Y | str | 期货期权的每手乘数 |
| HKVolBaseRate | Y | str | 港股/日股/新加坡股 每手股数 |
| BelongHS300 | Y | str | 是否属于沪深300 |
| BelongHasKQZ | Y | str | 是否含可转债 |
| BelongRZRQ | Y | str | 是否是融资融券标的 |
| BelongHSGT | Y | str | 是否属于沪深股通 |
| IsHKGP | Y | str | 是否是港股 |
| IsQH | Y | str | 是否是期货 |
| IsQQ | Y | str | 是否是期权 |
| IsSTGP | Y | str | 是否是ST股票 |
| IsQuitGP | Y | str | 是否是退市整理板股票 |
| TodayDRFlag | Y | str | 当天是否有除权除息(沪深京) |
| HSStockKind | Y | str | 沪深京品种类型 0:指数,1:A股主板,2:北证A股,3:创业板,4:科创板,5:B股,6:债券,7:基金,8:权证,9:其它,10:非沪深京品种 |
| ActiveCapital | Y | str | 流通股本(万股) |
| J_zgb | Y | str | 总股本(万股) |
| J_bg | Y | str | B股(万股) |
| J_hg | Y | str | H股(万股) |
| J_zzc | Y | str | 总资产(万元) |
| J_ldzc | Y | str | 流动资产(万元) |
| J_gdzc | Y | str | 固定资产(万元) |
| J_wxzc | Y | str | 无形资产(万元) |
| J_ldfz | Y | str | 流动负债(万元) |
| J_cqfz | Y | str | 少数股东权益(万元) |
| J_zbgjj | Y | str | 资本公积金(万元) |
| J_jzc | Y | str | 股东权益/净资产(万元) |
| J_yysy | Y | str | 营业收入(万元) |
| J_yycb | Y | str | 营业成本(万元) |
| J_yszk | Y | str | 应收账款(万元) |
| J_yyly | Y | str | 营业利润(万元) |
| J_tzsy | Y | str | 投资收益(万元) |
| J_jyxjl | Y | str | 经营现金净流量(万元) |
| J_zxjl | Y | str | 总现金净流量(万元) |
| J_ch | Y | str | 存货(万元) |
| J_lyze | Y | str | 利润总额(万元) |
| J_shly | Y | str | 税后利润(万元) |
| J_jly | Y | str | 净利润(万元) |
| J_wfply | Y | str | 未分配利益(万元) |
| J_jyl | Y | str | 净资产收益率 |
| J_mgwfp | Y | str | 每股未分配 |
| J_mgsy | Y | str | 每股收益（折算为全年） |
| J_mgsy2 | Y | str | 季报每股收益 (财报中提供的每股收益) |
| J_mggjj | Y | str | 每股公积金 |
| J_mgjzc | Y | str | 每股净资产 |
| J_mgjzc2 | Y | str | 季报每股净资产 (财报中提供的每股收益) |
| J_gdqyb | Y | str | 股东权益比 |
| J_gdrs | Y | str | 股东人数 |
| J_HalfYearFlag | Y | str | 报告期月份(3,6,9,12) |
| J_start | Y | str | 上市日期 |
| tdx_dycode | Y | str | 通达信地域代码 |
| tdx_dyname | Y | str | 通达信地域 |
| rs_hycode_sim | Y | str | 通达信行业代码 |
| rs_hyname | Y | str | 通达信行业 |
| blockzscode | Y | str | 所属的行业板块指数代码 |
| underly_setcode | Y | str | 标的市场代码(比如：当前ETF跟踪的指数市场) |
| underly_code | Y | str | 标的代码(比如：当前ETF跟踪的指数代码) |

### # 接口使用

```python
from tqcenter import tq
tq.initialize(__file__)
fdc = tq.get_stock_info(stock_code='688318.SH', field_list=[])
print(fdc)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
{'Name': '财富趋势',
'Unit': '100',
'VolBase': '102.22',
'MinPrice': '0.01',
'XsFlag': '2',
'Fz': ['570', '690', '780', '900', '900', '900', '900', '900'],
'DelayMin': '0',
'QHVolBaseRate': '0',
'HKVolBaseRate': '0',
'BelongHS300': '0',
'BelongHasKQZ': '0',
'BelongRZRQ': '1',
'BelongHSGT': '1',
'IsHKGP': '0',
'IsQH': '0',
'IsQQ': '0',
'IsSTGP': '0',
'IsQuitGP': '0',
'TodayDRFlag': '0',
'HSStockKind': '4',
'ActiveCapital': '25611.94',
'J_zgb': '25611.94',
'J_bg': '0.00',
'J_hg': '0.00',
'J_zzc': '389036.97',
'J_ldzc': '235598.84',
'J_gdzc': '972.62',
'J_wxzc': '1184.64',
'J_ldfz': '17412.97',
'J_cqfz': '73.15',
'J_zbgjj': '157998.02',
'J_jzc': '370454.03',
'J_yysy': '19827.85',
'J_yycb': '4258.70',
'J_yszk': '2726.99',
'J_yyly': '20836.07',
'J_tzsy': '5091.96',
'J_jyxjl': '5432.08',
'J_zxjl': '9779.30',
'J_ch': '61.84',
'J_lyze': '20829.85',
'J_shly': '18421.45',
'J_jly': '18421.34',
'J_wfply': '175521.63',
'J_jyl': '4.97',
'J_mgwfp': '6.85',
'J_mgsy': '0.96',
'J_mgsy2': '0.00',
'J_mggjj': '6.17',
'J_mgjzc': '14.46',
'J_mgjzc2': '14.46',
'J_gdqyb': '0.95',
'J_gdrs': '24154.00',
'J_HalfYearFlag': '9',
'J_start': '20200427',
'tdx_dycode': '18',
'tdx_dyname': '深圳板块',
'rs_hycode_sim': 'X4202',
'rs_hyname': '软件服务',
'blockzscode': '881355',
'underly_setcode': '0',
'underly_code': '',
'ErrorId': '0'}
```
