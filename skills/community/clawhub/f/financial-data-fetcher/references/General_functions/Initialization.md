# # 初始化initialize

```python
initialize(__file__) #所有策略连接通达信客户端都必须调用此函数进行初始化
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 调用方法:

```python
from tqcenter import tq

tq.initialize(__file__)
```

![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABmJLR0QA/wD/AP+gvaeTAAAAEElEQVQokWNgGAWjYBRgBwADHgABW0tfWAAAAABJRU5ErkJggg==)

### # 注意事项:

1."initialize"不可修改。
 2.该函数用于初始化，任何一个策略都必须有该函数。
