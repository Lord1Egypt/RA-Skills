# # 向通达信公式设置数据formula_set_data

### # 在调用公式前须先设置公式参数，此接口与formula_set_data_info作用一样，会互相覆盖

```python
def formula_set_data(stock_code: str = '',
                stock_period: str = '1d',
                stock_data: List = [],
                count: int = 1,
                dividend_type: int = 0):
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| stock_code | Y | str | 股票代码 |
| stock_period | Y | str | K线周期 |
| stock_data | Y | List | 指定格式的K线数据 |
| count | Y | int | 选取的K线数量 |
| dividend_type | Y | int | 复权类型 |

- dividend_type的取值为：0不复权 1前复权 2后复权
- count为设定stock_data中生效的K线数据，即stock_data中有效数据不能小于count
- count须大于0，且最大不超过24000
- 设置的数据在断开连接前一直生效，后设置的数据会覆盖前面设置的数据

### # 接口使用

```python
from tqcenter import tq

tq.initialize(__file__)

test_md = tq.get_market_data(stock_list=['688318.SH'], count=5, period='1d')
format_md = tq.tdx_formula_format_data(test_md)
formula_set_k = tq.formula_set_data(stock_code='688318.SH', stock_period='1d', stock_data=format_md['688318.SH'], count=len(format_md['688318.SH']))
print(formula_set_k)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
{'ErrorId': '0', 'Msg': '向通达信公式系统设置数据成功！', 'run_id': '1'}
```
