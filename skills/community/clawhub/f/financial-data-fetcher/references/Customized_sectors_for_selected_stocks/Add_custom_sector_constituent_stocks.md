# # 添加自定义板块成份股send_user_block

### # 往指定自定义板块中添加成份股

```python
send_user_block(block_code: str = '',
                stocks: List[str] = [],
                show: bool = False) -> Dict:
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| block_code | Y | str | 自定义板块简称 |
| stocks | Y | List[str] | 添加的自选股 |
| show | N | str | 客户端是否切换至对应板块界面 |

- block_code 为客户端已有的自定义板块简称，如果不存在则无效果，空则为添加到临时条件股
- block_code存在，传入空列表则表示清空该板块所有股票，否则为添加新股票
- 自选股的block_code为ZXG

### # 接口使用

```python
from tqcenter import tq
tq.initialize(__file__)
zxg_result = tq.send_user_block(block_code='CSBK', stocks=["600000.SH","600004.SH","000001.SZ","000002.SZ"])
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
{'Error': 'Add User Block Completed', 'ErrorId': '0', 'run_id': '1'}
```
