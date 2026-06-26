# # 刷新历史K线缓存refresh_kline

### # 根据股票和周期刷新历史K线缓存，如果本地没有下载完整的日线等数据，则可以调用这个函数定向下载某些品种某些周期的历史K线数据

```python
refresh_kline(stock_list: List[str] = [], period: str = '')
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| stock_list | Y | List[str] | 证券代码列表，证券代码格式为6位数+市场后缀（.SH/.SZ/.BJ等） |
| period | Y | str | 周期 1d为日线、1m为一分钟线、5m为五分钟线，只支持这三种，其它周期的数据均由这三种数据生成 |

### # 接口使用

```python
from tqcenter import tq
tq.initialize(__file__)
refresh_kline = tq.refresh_kline(stock_list=['688318.SH'],period='1d')
print(refresh_kline)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 数据样本

注：如果在盘中交易时间段下载1m和5m分钟线，只能下载到截止上个交易日的数据
 使用后会在客户端弹出刷新数据的加载界面，加载完成后才会有返回

```text
{
   "Error" : "refresh kline cache success.",
   "ErrorId" : "0",
   "run_id" : "1"
}
```
