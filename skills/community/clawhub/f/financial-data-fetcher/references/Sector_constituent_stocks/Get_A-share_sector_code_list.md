# # 获取A股板块代码列表get_sector_list

### # 获取A股全部板块代码列表

```python
def get_sector_list(list_type: int = 0) -> List:
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| list_type | Y | int | 返回数据类型 |

- list_type = 0 只返回代码，list_type = 1 返回代码和名称

### # 接口使用

```python
from tqcenter import tq
tq.initialize(__file__)
block_list = tq.get_sector_list()
print(block_list)
block_list2 = tq.get_sector_list(list_type = 1)
print(block_list2)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

注：此接口相当于 get_stock_list('10')

### # 数据样本

```text
['880081.SH', '880082.SH', '880201.SH', '880202.SH', '880203.SH', '880204.SH', '880205.SH', '880206.SH', '880207.SH', '880208.SH', ...]

[{'Code': '880081.SH', 'Name': '轮动趋势'}, {'Code': '880082.SH', 'Name': '板块趋势'}, {'Code': '880201.SH', 'Name': '黑龙江'}, {'Code': '880202.SH', 'Name': '新疆板块'}, {'Code': '880203.SH', 'Name': '吉林板块'}, {'Code': '880204.SH', 'Name': '甘肃板块'}, {'Code': '880205.SH', 'Name': '辽宁板块'}, {'Code': '880206.SH', 'Name': '青海板块'}, {'Code': '880207.SH', 'Name': '北京板块'},...]
```
