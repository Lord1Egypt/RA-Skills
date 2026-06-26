# # 获取跟踪指数的ETF信息get_trackzs_etf_info

### # 根据指数代码获取跟踪它的ETF的信息

```python
def get_trackzs_etf_info(zs_code: str = ''):
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| zs_code | Y | str | 指数代码 |

### # 输出数据

| 名称 | 类型 | 说明 |
|---|---|---|
| Code | str | 证券代码 |
| Name | str | 证券名称 |
| NowPrice | str | 现价 |
| PreClose | str | 昨收 |
| IOPV | str | 净值 |
| Zgb | str | 净额（万份） |
| Sz | str | 规模（亿元） |

### # 接口使用

```python
from tqcenter import tq
tq.initialize(__file__)

trackzs_etf_info = tq.get_trackzs_etf_info(zs_code='950162.CSI')
print(trackzs_etf_info)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
[{'Code': '589210.SH', 'Name': '科创芯片设计ETF', 'NowPrice': '1.208', 'PreClose': '1.192', 'IOPV': '1.2071', 'Zgb': '7646.90', 'Sz': '0.92'},
{'Code': '589070.SH', 'Name': '科创芯片设计ETF', 'NowPrice': '0.954', 'PreClose': '0.942', 'IOPV': '0.9547', 'Zgb': '65129.30', 'Sz': '6.21'},
{'Code': '588780.SH', 'Name': ' 科创芯片设计ETF', 'NowPrice': '0.875', 'PreClose': '0.866', 'IOPV': '0.8756', 'Zgb': '106790.20', 'Sz': '9.34'},
{'Code': '589170.SH', 'Name': '科创芯片设计ETF', 'NowPrice': '0.969', 'PreClose': '0.956', 'IOPV': '0.9685', 'Zgb': '37890.90', 'Sz': '3.67'},
{'Code': '589250.SH', 'Name': '芯设计PY', 'NowPrice': '0.000', 'PreClose': '0.000', 'IOPV': '0.0000', 'Zgb': '0.00', 'Sz': '0.00'},
{'Code': '589030.SH', 'Name': '科创芯片设计ETF', 'NowPrice': '1.013', 'PreClose': '1.000', 'IOPV': '1.0130', 'Zgb': '48407.70', 'Sz': '4.90'}]
```
