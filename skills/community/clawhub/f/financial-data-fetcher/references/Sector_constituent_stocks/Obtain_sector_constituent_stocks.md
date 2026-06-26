# # 获取板块成份股get_stock_list_in_sector

### # 根据板块代码获取其成份股列表

```python
def get_stock_list_in_sector(block_code: str,
                         block_type: int = 0,
                         list_type: int = 0) -> List:
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| block_code | Y | str | 板块代码 |
| block_type | N | str | 板块类型 |
| list_type | Y | int | 返回数据类型 |

- 获取A股成份股时支持板块名称或板块代码两种方式传入
- block_type=0 表示传入板块指数代码或板块指数名称（默认）
- block_type=1 表示传入自定义板块简称 需要是客户端中预先定义好自定义板块的简称 如果是ZXG表示是自选股；TJG表示是临时条件股
- list_type = 0 只返回代码，list_type = 1 返回代码和名称

### # 接口使用

```python
from tqcenter import tq
tq.initialize(__file__)
#通过板块代码获取成份股
block_stocks = tq.get_stock_list_in_sector('880081.SH')
print(block_stocks)
print(len(block_stocks))

#通过板块名获取成份股
block_stocks = tq.get_stock_list_in_sector('钛金属')
print(block_stocks)
print(len(block_stocks))

block_stocks2 = tq.get_stock_list_in_sector('钛金属',list_type=1)
print(block_stocks2)

#获取自定义板块成份股
block_stocks = tq.get_stock_list_in_sector('CSBK', block_type = 1)
print(block_stocks)
print(len(block_stocks))
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
['159922.SZ', '510500.SH', '512500.SH']
3
['000545.SZ', '000629.SZ', '000635.SZ', '000688.SZ', '000709.SZ', '000962.SZ', '002136.SZ', '002140.SZ', '002145.SZ', '002149.SZ', '002167.SZ', '002386.SZ', '002601.SZ', '002978.SZ', '300402.SZ', '300891.SZ', '600456.SH', '600727.SH', '603067.SH', '603826.SH', '688122.SH', '688750.SH', '920068.BJ']
23
[{'Code': '000545.SZ', 'Name': '金浦钛业'}, {'Code': '000629.SZ', 'Name': '钒钛股份'}, {'Code': '000635.SZ', 'Name': '英 力 特'}, {'Code': '000688.SZ', 'Name': '国城矿业'}, {'Code': '000709.SZ', 'Name': '河钢股份'}, {'Code': '000962.SZ', 'Name': '东方钽业'}, {'Code': '002136.SZ', 'Name': '安 纳 达'}, {'Code': '002140.SZ', 'Name': '东华科技'}, {'Code': '002145.SZ', 'Name': '钛能化学'}, {'Code': '002149.SZ', 'Name': '西部材料'}, {'Code': '002167.SZ', 'Name': '东方锆业'}, {'Code': '002386.SZ', 'Name': '天原股份'}, {'Code': '002601.SZ', 'Name': '龙佰集团'}, {'Code': '002978.SZ', 'Name': '安宁股份'}, {'Code': '300402.SZ', 'Name': '宝色股份'}, {'Code': '300891.SZ', 'Name': '惠云钛业'}, {'Code': '600456.SH', 'Name': '宝钛股份'}, {'Code': '600727.SH', 'Name': '鲁北化工'}, {'Code': '603067.SH', 'Name': '振华股份'}, {'Code': '603389.SH', 'Name': '*ST亚振'}, {'Code': '603826.SH', 'Name': '坤彩科技'}, {'Code': '688122.SH', 'Name': '西部超导'}, {'Code': '688750.SH', 'Name': '金天钛业'}, {'Code': '920068.BJ', 'Name': '天工股份'}]
['600000.SH', '600004.SH', '600006.SH', '600007.SH', '600008.SH', '600009.SH', '600010.SH']
7
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

注意
 get_stock_list_in_sector 入参的板块只能是自定义板块或者15板块指数
 不支持系统 全部A股 沪深A股等板块
