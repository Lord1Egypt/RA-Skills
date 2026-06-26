# # 调用通达信公式进行计算formula_zb/xg/exp

### # 调用通达信三种类型的公式

```python
	#调用技术指标公式
    def formula_zb(formula_name: str = '',
                   formula_arg: str = '',
                   xsflag: int = -1):
	#调用条件选股公式
    def formula_xg(formula_name: str = '',
                   formula_arg: str = ''):
	#调用专家系统公式
    def formula_exp(formula_name: str = '',
                    formula_arg: str = ''):
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| formula_name | Y | str | 公式名称 |
| formula_arg | Y | str | 公式参数 |
| xsflag | Y | int | 数据精度 |

- 目前支持调用技术指标公式、条件选股公式和专家系统公式，调用公式时请注意对应不同的调用接口和公式名
- formula_arg格式为"arg1,arg2,arg3,arg4,arg5"，arg须为纯数字字符串，最多支持16个。
- xsflag小于0时返回默认精度，最大可返回8位小数。

### # 接口使用

```python
from tqcenter import tq

tq.initialize(__file__)

formula_set_res = tq.formula_set_data_info(stock_code='688318.SH',stock_period='1d', count=20,dividend_type=1)
#技术指标公式MACD
formula_zb = tq.formula_zb(formula_name='MACD', formula_arg='12,26,9')
print(formula_zb)
#条件选股公式UPN
formula_xg = tq.formula_xg(formula_name='UPN', formula_arg='3')
print(formula_xg)
#专家系统公式CCI
formula_exp = tq.formula_zb(formula_name='CCI', formula_arg='12')
print(formula_exp)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
{'Data': {'DEA': [0.0, 0.01, -0.01, 0.03, 0.29, 0.63, 0.93, 1.25, 1.77, 2.27, 2.72, 3.08, 3.4, 3.57, 3.62, 3.58, 3.46, 3.3, 3.09, 2.83], 'DIF': [0.0, 0.05, -0.07, 0.19, 1.33, 1.96, 2.16, 2.52, 3.84, 4.25, 4.55, 4.54, 4.64, 4.27, 3.81, 3.44, 2.97, 2.68, 2.21, 1.83], 'MACD': [0.0, 0.07, -0.13, 0.32, 2.07, 2.67, 2.46, 2.54, 4.13, 3.98, 3.65, 2.91, 2.49, 1.39, 0.38, -0.29, -0.98, -1.25, -1.74, -2.02]}, 'ErrorId': '0'}
{'Data': {'UP3': [None, None, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}, 'ErrorId': '0'}
{'Data': {'ENTERLONG': [None, None, None, None, None, None, None, None, None, None, None, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'EXITLONG': [None, None, None, None, None, None, None, None, None, None, None, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}, 'ErrorId': '0'}
```
