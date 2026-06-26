# 概述
用于添加事件记忆。
# **请求接口**
| **URL** | /api/memory/event/add | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对记忆库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 基于AK/SK生成的签名信息 |
# **请求参数**
| **参数** | **类型** | **是否必须** | **参数说明** |
| --- | --- | --- | --- |
| collection_name  | String  |  | 目标记忆库的名称。  |
| project_name | String | 否 | 记忆库所属项目。 |
| resource_id | String | 否 | 记忆库唯一的资源 id。可选择直接传 resource_id，或同时传 collection_name 和 project_name 作为记忆库的唯一标识。 |
| event_type  | String  | 是  | 事件类型。  |
| memory_info | Object | 是   | 事件记忆的内容。对于内置事件sys_event_v1，只有summary；对于自定义事件，按照自定义的属性字段展示。  <br> **需要注意的是，其格式必须遵循在记忆库中已定义的格式。** |
| time | Integer | 否 | 记忆生成的时间戳（毫秒）。不传将以请求时间作为记忆生成时间。 |
| update_profiles | Array of Object | 否 | 需要更新的画像信息列表。 |
| * profile_type | String | 是 | 画像类型名称，必须是当前事件类型关联的画像类型。 |
| * primary_key | String | 否 | 画像主键。对于没有另外设置主键的画像（默认的user_id主键），primary_key 不需要填写。 <br>  <br> * 单一主键：“primary_key1=1” <br> * 联合主键：“primary_key1=1&primary_key2=1” |
| user_id | String  | 否  | 事件关联的用户ID。和assistant_id至少填写一个。 |
| assistant_id | String  | 否  | 事件关联的助手ID。和user_id至少填写一个。 |
| group_id | String  | 否  | 群组ID。用于隔离不同的会话或场景。 |
# 响应消息
| **参数** | **类型** | **参数说明** |
| --- | --- | --- |
| code | Integer | 状态码，0表示成功，其他表示错误。 |
| message | String | 返回信息，成功时通常为 "success"。 |
| data | Object | 返回的详细数据。 |
| * event_id | String | 事件的唯一ID。 |
| * memory_info | Object | 事件记忆的内容。 |
| * event_type | String | 事件类型。 |
| usage | Object | 事件记忆写入消耗的token。 |
| * embedding_tokens | Integer | Embedding token消耗。 |
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

# 添加记忆事件
result = collection.add_event(
    event_type="sys_event_v1",
    memory_info={
        "summary": "小明向助手分享了今年校庆打算和朋友回校重走校园路线、重温美食的计划，还提及朋友曾送的小夜灯，两人回忆起大学室友情。助手提议帮小明整理回忆成一篇名为《403的黄光》的小文送给阿强，小明表示同意并打算拍摄龟背竹新叶续写。最后，两人约定等小明整理好照片后一起把403时间线做成一张长图。"
    },
    user_id="user001"
    )

print("\n=== 格式化结果 ===")
print(json.dumps(result, indent=2, ensure_ascii=False))
```


## 响应消息
### **执行成功返回**
```Shell
{
     'code': 0, 
     'data': {
         'event_id': 'xxxxxxxxxfc4461e36a16_0', 
         'event_type': 'sys_event_v1', 
         'memory_info': {'summary': '小明向助手分享了今年校庆打算和朋友回校重走校园路线、重温美食的计划，还提及朋友曾送的小夜灯，两人回忆起大学室友情。助手提议帮小明整理回忆成一篇名为《403的黄光》的小文送给阿强，小明表示同意并打算拍摄龟背竹新叶续写。最后，两人约定等小明整理好照片后一起把“403时间线”做成一张长图。'}, 
         'usage': {
         'embedding_tokens': 226
         }
     }, 
     'message': 'success', 
     'request_id': 'xxxxxxxxxxf73ed50'
 }
```


