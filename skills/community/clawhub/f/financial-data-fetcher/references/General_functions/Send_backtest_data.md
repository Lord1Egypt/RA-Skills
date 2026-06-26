# # 发送回测数据send_bt_data

### # 往客户端发送指定股票的回测数据

```python
send_bt_data(stock_code:          str  = '',
			time_list:         List[str] = [],
			data_list:         List[List[str]] = [],
			count:        int  = 1) -> Dict:
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| stock_code | Y | List[str] | 证券代码 |
| time_list | Y | List[str] | 时间列表 |
| data_list | N | List[List[str]] | 回测数据列表 |
| count | N | int | 有效数据个数 |

- data_list为二维List，每个子元素对应time_list的一个元素时间点，且每个子元素最多有16个有效纯数字字符串，即data_list每个子List的前16个数据为一个时间点的有效数据
- count限定入参中每个list中的有效数据个数，即每个list前count个数据会传给客户端

### # 接口使用

```python
from tqcenter import tq

tq.initialize(__file__)

bt_data = tq.send_bt_data(stock_code = '688318.SH',
                          time_list = ['20251215141115'],
                          data_list = [['11']],
                          count = 1)
print(bt_data)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
{'Error': '发送回测结果成功.', 'ErrorId': '0', 'run_id': '1'}
```
