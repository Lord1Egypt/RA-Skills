# # 发送预警信号send_warn

### # 往客户端发送指定股票的预警信号

```python
send_warn(stock_list:        List[str] = [],
			time_list:         List[str] = [],
			price_list:        List[str] = [],
			close_list:        List[str] = [],
			volum_list:        List[str] = [],
			bs_flag_list:      List[str] = [],
			warn_type_list:    List[str] = [],
			reason_list:       List[str] = [],
			count:        int  = 1) -> Dict:
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| stock_list | Y | List[str] | 证券代码列表 |
| time_list | Y | List[str] | 时间列表 |
| price_list | N | List[str] | 现价列表 |
| close_list | N | List[str] | 收盘价列表 |
| volum_list | N | List[str] | 成交额列表 |
| bs_flag_list | N | List[str] | 买卖标志：0买1卖2未知 |
| warn_type_list | N | List[str] | 预警类型：0常规预警（目前仅支持） |
| reason_list | N | List[str] | 预警原因 |
| count | N | int | 有效数据个数 |

- price_list、close_list、volum_list、bs_flag_list、warn_type_list 均要求为纯数字字符串List
- bs_flag_list 0买1卖2未知，长度小于count的会自动补为2。
- reason_list每个元素有效长度为25个汉字（50个英文）|
- count限定入参中每个list中的有效数据个数，即每个list前count个数据会传给客户端
- stock_list与其他list的元素数据是一一对应的，即stock_list的第一个元素对应的预警信息是其他list的第一个元素，同一只股票的多个预警信息，则在stock_list中加入多次该股票

### # 接口使用

```python
from tqcenter import tq
tq.initialize(__file__)
warn_res = tq.send_warn(stock_list = ['688318.SH','688318.SH','600519.SH'],
             time_list = ['20251215141115','20251215142100','20251215143101'],
             price_list= ['123.45','133.45','1823.45'],
             close_list= ['122.50','132.50','1822.50'],
             volum_list= ['1000','2000','15000'],
             bs_flag_list= ['0'],
             warn_type_list= ['0'],
             reason_list= ['价格突破预警线','收盘价突破预警线','成交量突破预警线'],
             count=3)
print(warn_res)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
{'Error': '发送预警信号成功.', 'ErrorId': '0', 'run_id': '1'}
```
