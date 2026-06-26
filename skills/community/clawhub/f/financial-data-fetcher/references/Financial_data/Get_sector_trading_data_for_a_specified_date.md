# # 获取指定日期板块交易数据get_bkjy_value_by_date

### # 根据板块代码，获取指定日期的板块交易数据，需要先在客户端中下载股票数据包

```python
get_bkjy_value_by_date(stock_list: List[str] = [],
							field_list: List[str] = [],
							year: int = 0,
							mmdd: int = 0) -> Dict:
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| stock_list | Y | List[str] | 证券代码列表 |
| field_list | Y | List[str] | 字段筛选，不能为空 |
| year | Y | int | 指定年份 |
| mmdd | Y | int | 指定月日 |

当year和mmdd默认为0时返回最近一条数据。

### # 输出数据

同get_bkjy_value一样。

### # 接口使用

```python
from tqcenter import tq

tq.initialize(__file__)

bk_one = tq.get_bkjy_value_by_date(stock_list=['880660.SH'],
                                   field_list=['BK9','BK10','BK11','BK12','BK13'],
                                   year=0,mmdd=0)
print(bk_one)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
{'880660.SH': {'BK10': ['6705.83', '191.60'], 'BK11': ['6183.65', '176.68'], 'BK12': ['0.00', '0.00'], 'BK13': ['0.00', '0.00'], 'BK9': ['3.00', '31.00']}}
```
