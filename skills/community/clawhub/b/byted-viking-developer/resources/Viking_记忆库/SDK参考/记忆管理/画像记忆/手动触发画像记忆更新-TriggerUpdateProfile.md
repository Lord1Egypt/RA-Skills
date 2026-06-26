# 概述
用于手动触发画像记忆的更新。
# **请求接口**
| **URL** | /api/memory/profile/trigger_update | 统一资源标识符 |
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
| update_profile_type | Array of String | 否 | 需要更新的画像记忆类型。不传时默认会更新所有画像类型。 |
| filters  | Object | 否 |  |
| * user_id | String or Array of String | 否 | 需要更新画像的用户范围，不传时默认更新全部用户。最多传1000个，超过时建议并行调用。 |
| * end_time | Integer | 否 | 更新画像的记忆截止时间。即此次事件记忆的数据范围为“上次更新的时间戳至end_time”。建议设置比当前时间早，确保更新数据的完整性。 |

# 响应消息
| **参数** | **类型** | **参数说明** |
| --- | --- | --- |
| code | Integer | 状态码，0表示成功，其他表示错误。 |
| message | String | 返回信息，成功时通常为 "success"。失败则返回原因。 |
| data | Object | 返回的详细数据。 |
| request_id | String | 标识每个请求的唯一ID。 |

# 完整示例
## 请求消息
### **Python请求**
```Python
import os
import json
import requests

API_KEY = os.getenv("MEMORY_API_KEY", "your_key")
url = "https://api-knowledgebase.mlp.cn-beijing.volces.com/api/memory/profile/trigger_update"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "collection_name": "my_first_memory_collection",
    "project_name": "default",
    "update_profile_type": ["profile_v1","social network"]  # 替换为需要更新的画像类型
 
}

response = requests.post(url, headers=headers, data=json.dumps(data, ensure_ascii=False))

print("Status Code:", response.status_code)
print("Response:", response.text)
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


