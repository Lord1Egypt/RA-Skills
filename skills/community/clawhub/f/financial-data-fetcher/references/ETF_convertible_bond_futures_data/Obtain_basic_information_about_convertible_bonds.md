# # 获取可转债基础信息get_cb_info

### # 根据可转债代码获取可转债基础信息

```python
def get_cb_info(stock_code:str = '',
				field_list: List[str] = []):
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| stock_code | Y | str | 可转债代码 |
| field_list | N | List[str] | 字段筛选，传空则返回全部 |

### # 输出数据

| 名称 | 类型 | 说明 |
|---|---|---|
| SetCode | str | 证券市场 |
| KZZCode | str | 可转债代码 |
| HSCode | str | 正股代码 |
| ZGPrice | str | 转股价格 |
| CurRate | str | 当期利率 |
| RestScope | str | 剩余规模(万) |
| PutBack | str | 回售触发价 |
| ForceRedeem | str | 强赎触发价 |
| ZGDate | str | 转股日 |
| EndPrice | str | 到期价 |
| EndDate | str | 到期日期 |
| ZGRate | str | 转股比率% |
| RealValue | str | 纯债价值 |
| ExpireYield | str | 到期收益率% |
| KZZScore | str | 可转债评级 |
| HSScore | str | 主体评级 |
| RedeemDate | str | 赎回登记日期 |
| RedeemPrice | str | 赎回价格 |
| PutDate | str | 回售申报起始日期 |
| PutPrice | str | 回售价格 |
| ZGCode | str | 转股代码 |
| AGPrice | str | 正股当前价格 |
| KZZPrice | str | 可转债当前价格 |
| KZZYj | str | 溢价率 |
| ZGValue | str | 转股价值 |

### # 接口使用

```python
from tqcenter import tq
tq.initialize(__file__)
cb_info = tq.get_cb_info(stock_code = '123039.SZ')
print(cb_info)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
{'CurRate': '2.80',
'EndDate': '20251226',
'EndPrice': '115.00',
'ExpireYield': '0.00',
'ForceRedeem': '37.90',
'HSCode': '300577',
'HSScore': 'A+',
'KZZCode': '123039',
'KZZScore': 'A+',
'PutBack': '20.41',
'PutDate': '0',
'PutPrice': '0.00',
'RealValue': '0.00',
'RedeemDate': '0',
'RedeemPrice': '0.00',
'RestScope': '22044.02',
'ZGCode': '123039',
'ZGDate': '20200702',
'ZGPrice': '29.15',
'ZGRate': '1.15',
'setcode': '0'}
```
