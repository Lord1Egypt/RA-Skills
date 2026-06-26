# 概述
用于更新已写入记忆库的事件记忆。
# **请求接口**
| **URL** | /api/memory/event/update | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对记忆库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 基于AK/SK生成的签名信息 |
# **请求参数**
| **参数** | **类型** | **是否必须** | **参数说明** |
| --- | --- | --- | --- |
| collection_name | String | 否 | 目标记忆库的名称。 |
| project_name | String | 否 | 记忆库所属项目。 |
| resource_id | String | 否 | 记忆库唯一的资源 id。可选择直接传 resource_id，或同时传 collection_name 和 project_name 作为记忆库的唯一标识。 |
| event_id | String | 是 | 需要更新的事件记忆id。 |
| memory_info <br>  | Object <br>  | 否 | 事件记忆的内容。对于内置事件sys_event_v1，只有summary；对于内置事件sys_profile_collect_v1，只有user_profile；对于自定义事件，按照自定义的属性字段展示。 <br> **需要注意的是，其格式必须遵循在记忆库中已定义的格式。如：** <br>  <br> * 内置事件sys_event_v1： <br>  <br> { <br> "summary": "今天我和好朋友一起过生日。" <br> } <br>  <br> * 自定义事件： <br>  <br> { <br> "knowledge_point_name": "今天我和好朋友一起过生日。", <br> "rating_score": 9 <br> } |
| user_id | Array of String | 否 | 事件关联的user_id。 |
| assistant_id | Array of String | 否 | 事件关联的assitant_id。 |
# 响应消息
| **参数** | **类型** | **参数说明** |
| --- | --- | --- |
| code | Integer | 状态码，0表示成功，其他表示错误。 |
| message | String | 返回信息，成功时通常为 "success"。失败则返回原因。 |
| data | Object | 返回的详细数据，成功添加消息时此字段通常为空。 |
| request_id | String | 标识每个请求的唯一ID。 |

# 完整示例
## 请求消息
### **Python请求**
```Python
import os
import time
from vikingdb.memory import VikingMem
from vikingdb import APIKey

API_KEY = os.getenv("MEMORY_API_KEY", "your_key")

client = VikingMem(
    host = "api-knowledgebase.mlp.cn-beijing.volces.com",
    region = "cn-beijing",
    auth= APIKey(api_key=API_KEY),
    scheme="http",
)

# 获取记忆库集合
collection = client.get_collection(
    collection_name="my_first_memory_collection",  # 用您的记忆库名称替代
    project_name="default"
)

# 更新事件数据
memory_info = {
    "original_messages": (
        "周一, 2025-08-18 02:58 下午\n"
        "user1(user): 我特别喜欢看比赛，明天又有比赛看了！\n"
        "user1(user): 小A为了跟小B的这场比赛，练了整整半年。\n"
        "assistant1(assistant): 这么励志！那这次肯定稳了吧？\n"
        "user1(user): 我也觉得，小B根本就没咋准备\n"
        "assistant1(assistant): 哈哈，一起期待一下小A的表现"
    ),
    "summary": (
        "2025年8月18日下午，用户表示特别喜欢看比赛，称8月19日有小A和小B的比赛，"
        "小A为此练了半年，小B没咋准备，助理期待小A表现。"
    )
}

# 调用 update_event 接口
result = collection.update_event(
    event_id="xxxxxxxxx", # 修改为您要更新的事件ID
    memory_info=memory_info
)

print("\n=== 格式化结果 ===")
print(json.dumps(result, indent=2, ensure_ascii=False))
```


## 响应消息
### **执行成功返回**
```Shell
{
    "code":0,
    "message":"success",
    "request_id":"0216950295xxxxxxx"
}
```


