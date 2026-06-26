# # 发送消息到通达信客户端send_message

### # 发送消息给通达信客户端的TQ策略界面

```python
send_message(msg_str: str) -> Dict:
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 输入参数

| 参数 | 是否必选 | 参数类型 | 参数说明 |
|---|---|---|---|
| msg_str | Y | str | 消息字符串 |

- 传入的字符串使用 | 可以让客户端将其分为两条（插入 \n 也可以分行显示）

### # 接口使用

```python
from tqcenter import tq
tq.initialize(__file__)
msg_str = "这是第一行. | 这是第二行. "
tq.send_message(msg_str)
```
