# # 获取系统分类成份股get_stock_list

### # 根据入参返回指定证券代码列表

```python
def get_stock_list(market = None,
                   list_type: int = 0) -> List:
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| market | Y | str | 指定代码 |
| list_type | Y | int | 返回数据类型 |

- list_type = 0 只返回代码，list_type = 1 返回代码和名称

```text
默认为全部A股
    0:自选股 1:持仓股
    5:所有A股 6:上证指数成份股 7:上证主板 8:深证主板 9:重点指数
    10:所有板块指数 11:缺省行业板块 12:概念板块 13:风格板块 14:地区板块 15:缺省行业分类+概念板块 16:研究行业一级 17:研究行业二级 18:研究行业三级
    21:含H股 22:含可转债 23:沪深300 24:中证500 25:中证1000 26:国证2000 27:中证2000 28:中证A500
    30:REITs 31:ETF基金 32:可转债 33:LOF基金 34:所有可交易基金 35:所有沪深基金 36:T+0基金
    49:金融类企业 50:沪深A股 51:创业板 52:科创板 53:北交所
    101:国内期货 102:港股 103:美股
	91:ETF追踪的指数
	92:国内期货主力合约
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 接口使用

```python
from tqcenter import tq
tq.initialize(__file__)
stock_list = tq.get_stock_list('16')
print(stock_list)

stock_list2 = tq.get_stock_list('16',list_type=1)
print(stock_list2)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
['881001.SH', '881006.SH', '881015.SH', '881061.SH', '881070.SH', '881090.SH', '881105.SH', '881129.SH', '881150.SH', '881166.SH', '881183.SH', '881199.SH', '881211.SH', '881230.SH', '881260.SH', '881286.SH', '881292.SH', '881318.SH', '881337.SH', '881351.SH', '881368.SH', '881385.SH', '881393.SH', '881405.SH', '881417.SH', '881426.SH', '881441.SH', '881458.SH', '881469.SH', '881477.SH']

[{'Code': '881001.SH', 'Name': '煤炭'}, {'Code': '881006.SH', 'Name': '石油'}, {'Code': '881015.SH', 'Name': '化工'}, {'Code': '881061.SH', 'Name': '钢铁'}, {'Code': '881070.SH', 'Name': '有色'}, {'Code': '881090.SH', 'Name': '建材'}, {'Code': '881105.SH', 'Name': '农林牧渔'}, {'Code': '881129.SH', 'Name': '食品饮料'}, {'Code': '881150.SH', 'Name': '纺织服饰'}, {'Code': '881166.SH', 'Name': '轻工制造'}, {'Code': '881183.SH', 'Name': '家电'}, {'Code': '881199.SH', 'Name': '商贸'}, {'Code': '881211.SH', 'Name': '汽车'}, {'Code': '881230.SH', 'Name': '医药医疗'}, {'Code': '881260.SH', 'Name': '电力设备'}, {'Code': '881286.SH', 'Name': '国防军工'}, {'Code': '881292.SH', 'Name': '机械设备'}, {'Code': '881318.SH', 'Name': '电子'}, {'Code': '881337.SH', 'Name': '通信'}, {'Code': '881351.SH', 'Name': '计算机'}, {'Code': '881368.SH', 'Name': '传媒'}, {'Code': '881385.SH', 'Name': '银行'}, {'Code': '881393.SH', 'Name': '非银金融'}, {'Code': '881405.SH', 'Name': '建筑'}, {'Code': '881417.SH', 'Name': '房地产'}, {'Code': '881426.SH', 'Name': '社会服务'}, {'Code': '881441.SH', 'Name': '交通运输'}, {'Code': '881458.SH', 'Name': '公用事业'}, {'Code': '881469.SH', 'Name': '环保'}, {'Code': '881477.SH', 'Name': '综合'}]
```
