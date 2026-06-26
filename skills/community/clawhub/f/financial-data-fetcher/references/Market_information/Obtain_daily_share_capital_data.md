# # 获取每天的股本数据get_gb_info

### # 获取指定股票的股本数据

```python
def get_gb_info(stock_code:str = '',
                date_list: List[str] = [],
                count: int = 1):
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| stock_code | Y | str | 股票代码 |
| date_list | Y | List[str] | 日期数组 |
| count | Y | int | 日期有效个数 |

- date_list传入的日期须从小到大排序
- date_list有效数据个数须不小于count，且不能小于1

### # 输出数据

| 名称 | 类型 | 数值 | 说明 |
|---|---|---|---|
| Date | double |  | 日期 |
| Zgb | double |  | 总股本 |
| Ltgb | double |  | 流通股本 |

### # 接口使用

```python
from tqcenter import tq
tq.initialize(__file__)
gb_info = tq.get_gb_info(stock_code = '688318.SH', date_list=['20250101','20250601'], count=2)
print(gb_info)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
[{'Date': 20250101, 'Zgb': 182942480.0, 'Ltgb': 182942480.0},
{'Date': 20250601,  'Zgb': 182942480.0, 'Ltgb': 182942480.0}]
```
