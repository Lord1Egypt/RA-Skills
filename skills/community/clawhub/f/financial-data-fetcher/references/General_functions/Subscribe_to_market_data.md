# # 订阅行情subscribe_hq

### # 订阅股票实时更新

```python
subscribe_hq(stock_list: List[str] = [],callback = None):
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| stock_list | Y | List[str] | 订阅的证券代码 |
| callback | Y | str | 回调函数 |

- 订阅股票更新 传入回调函数，订阅的股票有更新时，系统会调用回调函数，最多订阅100条
- 回调函数格式定义为on_data(datas) datas格式为 {"Code":"XXXXXX.XX","ErrorId":"0"}

### # 接口使用

```python
from tqcenter import tq

tq.initialize(__file__)

# 回调函数 功能为收到更新后请求最新的report数据
def my_callback_func(data_str):
    print("Callback received data:", data_str)
    code_json = json.loads(data_str)
    print(f"codes = {code_json.get('Code')}")
    report_ptr = tq.get_report_data(code_json.get('Code'))
    print(report_ptr)
    return None

sub_hq = tq.subscribe_hq(stock_list=['688318.SH'], callback=my_callback_func)
print(sub_hq)

# 收到更新时策略需要正在运行
#while True:
#	time.sleep(1)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

```text
{
   "Error" : "订阅688318.SH更新成功.",
   "ErrorId" : "0",
   "run_id" : "1"
}
```
