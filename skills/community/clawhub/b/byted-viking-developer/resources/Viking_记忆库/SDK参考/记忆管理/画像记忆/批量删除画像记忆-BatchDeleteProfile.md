# 概述
用于批量删除已写入记忆库的画像记忆。
# **请求接口**
| **URL** | /api/memory/profile/batch_delete | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对记忆库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 基于AK/SK生成的签名信息 |
# **请求参数**
| **参数** | **类型** | **是否必须** | **参数说明** |
| --- | --- | --- | --- |
| collection_name  | String  | 否 | 目标记忆库的名称。  |
| project_name | String | 否 | 记忆库所属项目。 |
| resource_id | String | 否 | 记忆库唯一的资源 id。可选择直接传 resource_id，或同时传 collection_name 和 project_name 作为记忆库的唯一标识。 |
| filter  | Object  | 是  | 删除记忆的过滤条件。  |
| * user_id  | String or Array of String  | 是 | 用于过滤的用户ID。可以是单个ID或ID列表。 |
| * assistant_id | String or Array of String  | 否  | 用于过滤的助手ID。可以是单个ID或ID列表。 |
| * profile_type  | String or Array of String  | 否  | 用于过滤的画像类型。  |
# 响应消息
| **参数** | **类型** | **参数说明** |
| --- | --- | --- |
| code | Integer | 状态码，0表示成功，其他表示错误。 |
| message | String | 返回信息，成功时通常为 "success"。 |
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

# 批量删除用户画像
result = collection.batch_delete_profile(
    filter={
        "user_id": ["student_A"],
        "profile_type": ["english_knowledge_point"]
    }
)

print("\n=== 批量删除用户画像结果 ===")
print(json.dumps(result, indent=2, ensure_ascii=False))
```


## 响应消息
### **执行成功返回**
```Shell
{
    "code":0,
    "message":"success",
    "request_id":"021695029537650fd001de666660000000000000000000230da93"
}
```


