# # 获取公式中的设置数据formula_get_data

### # 获取目前公式设置中的K线数据，使用前须先调用formula_set_data或formula_set_data_info设置公式数据

```python
def formula_get_data(cls):
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 接口使用

```python
from tqcenter import tq

tq.initialize(__file__)

formula_set_res = tq.formula_set_data_info(stock_code='688318.SH',stock_period='1d', count=5,dividend_type=1)
formula_kline = tq.formula_get_data()
print(formula_kline)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
{'Code': '688318.SH', 'Data': [
{'Amount': 339302880.0, 'Close': 144.4, 'Date': '2026-01-20 00:00:00', 'High': 146.98, 'Low': 142.65, 'Open': 146.5, 'Volume': 2345401.0},
{'Amount': 358410880.0, 'Close': 144.77, 'Date': '2026-01-21 00:00:00', 'High': 146.5, 'Low': 143.1, 'Open': 144.49, 'Volume': 2472760.0},
{'Amount': 415987840.0, 'Close': 143.03, 'Date': '2026-01-22 00:00:00', 'High': 147.0, 'Low': 142.5, 'Open': 145.0, 'Volume': 2878793.0},
{'Amount': 471310432.0, 'Close': 144.39, 'Date': '2026-01-23 00:00:00', 'High': 146.88, 'Low': 142.58, 'Open': 142.58, 'Volume': 3256538.0},
{'Amount': 541417344.0, 'Close': 141.84, 'Date': '2026-01-26 00:00:00', 'High': 146.77, 'Low': 141.8, 'Open': 143.7, 'Volume': 3761141.0}], 'ErrorId': '0'}
```
