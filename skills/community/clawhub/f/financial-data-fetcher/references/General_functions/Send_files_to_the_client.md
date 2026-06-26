# # 发送文件到客户端send_file

### # 往通达信客户端发送文件名，可由TQ策略数据浏览中打开

```python
send_file(file: str) -> Dict:
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| file | Y | str | 文件路径 |

- 文件放于 .\PYPlugins\file\ 文件夹中时，file可仅传入文件名
- 文件放于其他位置时，file需要传入绝对路径
- 目前支持的文件类型：txt，pdf，html

### # 接口使用

```python
from tqcenter import tq
tq.initialize(__file__)
file = "test.txt"
tq.send_file(file)
```
