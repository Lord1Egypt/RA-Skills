# 12306 购票自动化

12306 火车票查询/购票自动化。

## 功能
- ✅ 登录
- ✅ 车票查询
- ✅ 购票

## 使用
```python
from 12306_client import Railway12306Client
client = Railway12306Client()
client.start()
client.login()
tickets = client.search_tickets("北京", "上海", "2026-03-05")
client.close()
```
