# # 获取板块交易数据get_bkjy_value

### # 根据板块代码，获取指定时间段内的板块交易数据，需要先在客户端中下载股票数据包

```python
get_bkjy_value(stock_list: List[str] = [],
				field_list: List[str] = [],
				start_time: str = '',
				end_time: str = '') -> Dict:
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| stock_list | Y | List[str] | 证券代码列表 |
| field_list | Y | List[str] | 字段筛选，不能为空 |
| start_time | N | str | 起始时间 |
| end_time | N | str | 结束时间 |

### # 输出数据

| 名称 | 类型 | 数值 | 说明 |
|---|---|---|---|
| BK5 | double |  | 市盈率TTM 整体法 算术平均 |
| BK6 | double |  | 市净率MRQ 整体法 算术平均 |
| BK7 | double |  | 市销率TTM 整体法 算术平均 |
| BK8 | double |  | 市现率TTM 整体法 算术平均 |
| BK9 | double |  | 涨跌数 上涨家数 下跌家数 |
| BK10 | double |  | 板块总市值(亿元) 整体法 算术平均 |
| BK11 | double |  | 板块流通市值(亿元) 整体法 算术平均 |
| BK12 | double |  | 涨停数 涨停家数 曾涨停家数[注：该指标展示20160926日之后的数据] |
| BK13 | double |  | 跌停数 跌停家数 曾跌停家数[注：该指标展示20160926日之后的数据] |
| BK14 | double |  | 涨停数据 市场高度(不含ST股和未开板新股) 2板及以上涨停个数(不含ST股和未开板新股)[注：该指标展示20180319日之后的数据] |
| BK15 | double |  | 融资融券 沪深京融资余额(万元) 沪深京融券余额(万元) |
| BK16 | double |  | 陆股通资金流入 沪股通流入金额(亿元) 深股通流入金额(亿元) [注：该指标展示20170320日之后的数据] |
| BK17 | double |  | 开盘成交数 开盘成交额(万元) 开盘成交量(万股) |
| BK18 | double |  | 板块股息率(%) 算数平均 整体法 |
| BK19 | double |  | 板块自由流通市值(亿元) 整体法 算术平均 |

### # 接口使用

```python
from tqcenter import tq

tq.initialize(__file__)

bk_data = tq.get_bkjy_value(stock_list=['880660.SH'],
        field_list=['BK5','BK6','BK7','BK8','BK9'],
        start_time='20250101',
        end_time='20250102')
print(bk_data)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
{'880660.SH': {'BK5': [{'Date': '20250102', 'Value': ['55.28', '55.50']}],
'BK6': [{'Date': '20250102', 'Value': ['4.62', '3.79']}],
'BK7': [{'Date': '20250102', 'Value': ['5.25', '8.22']}],
'BK8': [{'Date': '20250102', 'Value': ['46.52', '312.41']}],
'BK9': [{'Date': '20250102', 'Value': ['0.00', '35.00']}, {'Date': '20260130', 'Value': ['10.00', '25.00']}]}}
```
