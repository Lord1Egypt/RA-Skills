# # 格式化K线数据formula_format_data

### # 格式化get_market_data获取的K线数据

```python
def formula_format_data(data_dict: Dict = {}):
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| data_dict | Y | Dict | get_market_data获取格式的K线Dict |

- get_market_data获取的K线数据不能直接用于设置公式参数，须先调用formula_format_data进行格式化
- formula_format_data返回值为List[Dict]，其中Dict的Key须有["Amount", "Volume", "Close", "Open", "High", "Low"]，用户可以直接提供符合条件的List提供给tdx_formula_set_data。

### # 接口使用

```python
from tqcenter import tq

tq.initialize(__file__)

test_md = tq.get_market_data(stock_list=['688318.SH'], count=5, period='1d')
format_md = tq.formula_format_data(test_md)
print(format_md)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
{'688318.SH': [
{'Date': '2026-01-20 00:00:00', 'Amount': 33930.29, 'Volume': 2345401.0, 'Close': 144.4, 'Open': 146.5, 'High': 146.98, 'Low': 142.65},
{'Date': '2026-01-21 00:00:00', 'Amount': 35841.09, 'Volume': 2472760.0, 'Close': 144.77, 'Open': 144.49, 'High': 146.5, 'Low': 143.1},
{'Date': '2026-01-22 00:00:00', 'Amount': 41598.79, 'Volume': 2878793.0, 'Close': 143.03, 'Open': 145.0, 'High': 147.0, 'Low': 142.5},
{'Date': '2026-01-23 00:00:00', 'Amount': 47131.04, 'Volume': 3256538.0, 'Close': 144.39, 'Open': 142.58, 'High': 146.88, 'Low': 142.58},
{'Date': '2026-01-26 00:00:00', 'Amount': 54141.73, 'Volume': 3761141.0, 'Close': 141.84, 'Open': 143.7, 'High': 146.77, 'Low': 141.8}]}
```
