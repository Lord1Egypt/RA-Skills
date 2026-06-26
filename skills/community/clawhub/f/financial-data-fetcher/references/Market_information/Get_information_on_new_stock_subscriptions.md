# # 获取新股申购信息get_ipo_info

### # 获取今天及未来的新股或新发债申购信息

```python
get_ipo_info(ipo_type:int = 0,
             ipo_date:int = 0):
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| ipo_type | Y | str | 自定义板块简称 |
| ipo_date | Y | int | 自定义板块名称 |

- ipo_type=0 表示获取新股申购信息
- ipo_type=1 表示获取新发债信息
- ipo_type=2 表示获取新股和新发债信息
- ipo_date=0 表示只获取今天信息
- ipo_date=1 表示获取今天及以后信息

### # 接口使用

```python
from tqcenter import tq
tq.initialize(__file__)
ipo_info = tq.get_ipo_info(ipo_type=2, ipo_date=1)
print(ipo_info)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
[{'MaxSG': '0.00', 'PE_Issue': '0.00', 'SGCode': '371036', 'SGDate': '20251226', 'SGPrice': '100.00', 'code': '301036', 'name': '双乐转债', 'setcode': '0'},
{'MaxSG': '0.00', 'PE_Issue': '0.00', 'SGCode': '718676', 'SGDate': '20251225', 'SGPrice': '100.00', 'code': '688676', 'name': '金05转债', 'setcode': '1'}]
```
