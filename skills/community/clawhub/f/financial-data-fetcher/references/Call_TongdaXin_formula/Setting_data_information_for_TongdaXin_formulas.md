# # 向通达信公式设置数据信息formula_set_data_info

### # 在调用公式前须先设置公式参数，此接口与formula_set_data作用一样，会互相覆盖

```python
def formula_set_data_info(stock_code: str = '',
                stock_period: str = '1d',
                start_time: str = '',
                end_time: str = '',
                count: int = -1,
                dividend_type: int = 0):
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| stock_code | Y | str | 股票代码 |
| stock_period | Y | str | K线周期 |
| start_time | Y | str | 起始时间 |
| end_time | Y | str | 结束时间 |
| count | Y | int | 截取K线数量 |
| dividend_type | Y | int | 复权类型 |

- dividend_type的取值为：0不复权 1前复权 2后复权
- count为截取最新交易日开始往前的n条K线，当count参数不为0时，start_time和end_time失效
- count=-1时，获取所有数据，count=-2时，使用无序列数据
- 当count为0时，start_time和end_time生效，指定K线为对应时间段内
- count最大值为24000，count为-1时为获取对应股票全部K线
- 设置的数据在断开连接前一直生效，后设置的数据会覆盖前面设置的数据

### # 接口使用

```python
from tqcenter import tq

tq.initialize(__file__)

formula_set_res = tq.formula_set_data_info(stock_code='688318.SH',stock_period='1d', count=100,dividend_type=1)
print(formula_set_res)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
{'ErrorId': '0', 'Msg': '向通达信公式系统设置数据信息成功！', 'run_id': '1'}
```
