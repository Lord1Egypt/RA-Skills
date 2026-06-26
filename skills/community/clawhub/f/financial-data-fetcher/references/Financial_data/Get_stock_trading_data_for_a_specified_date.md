# # 获取指定日期股票交易数据get_gpjy_value_by_date

### # 根据股票，获取指定时间段内的股票交易数据，需要先在客户端中下载股票数据包

```python
def get_gpjy_value_by_date(stock_list: List[str] = [],
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

同get_gpjy_value一样。

### # 接口使用

```python
from tqcenter import tq

tq.initialize(__file__)

gp_one = tq.get_gpjy_value_by_date(
        stock_list=['688318.SH'],
        field_list=['GP1','GP2','GP3','GP4','GP5'],
        year=0,mmdd=0)
print(gp_one)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
{'688318.SH': {'GP1': ['24154.00', '0.00'], 'GP2': ['20574.12', '18728.85'], 'GP3': ['140464.83', '55043.00'], 'GP4': ['169.80', '5943.00'], 'GP5': ['103.00', '-7000.00']}}
```
