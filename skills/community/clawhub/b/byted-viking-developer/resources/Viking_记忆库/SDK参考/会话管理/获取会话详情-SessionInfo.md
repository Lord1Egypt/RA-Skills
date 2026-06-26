# 接口概述
查询指定session的详细信息，包括生成的事件记忆列表，原始消息，token消耗。
# **请求接口**
| **URL** | /api/memory/session/info | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对记忆库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 基于AK/SK生成的签名信息 |
# 请求参数
| **参数** | **类型** | **是否必须** | **参数说明** |
| --- | --- | --- | --- |
| collection_name  | String  | 否  | 目标记忆库的名称。  |
| project_name | String | 否 | 记忆库所属项目。 |
| resource_id | String | 否 | 记忆库唯一的资源 id。可选择直接传 resource_id，或同时传 collection_name 和 project_name 作为记忆库的唯一标识。 |
| session_id  | String  | 是  | 当前对话或消息批次的会话 ID，长度要求：[1, 128]。  |
# 响应消息
| **参数** | **类型** | **参数说明** |
| --- | --- | --- |
| code  | Integer  | 状态码，0表示成功，其他表示错误。  |
| message  | String  | 返回信息，成功时通常为 "success"。  |
| data  | Object  | 返回的详细数据。  |
| * usage  | Object  | 此session输入的token消耗  |
|    * -embedding_tokens  | Integer  | embedding模型的token总消耗。  |
|    * -llm_input_tokens  | Integer  | LLM输入的token总消耗。  |
|    * -llm_output_tokens  | Integer  | LLM输出的token总消耗。  |
|    * -llm_input_tokens_details | Object | LLM输入的token消耗明细。  |
|    * -cached_tokens  | Integer  | LLM输入的cached token消耗。  |
| * event_memory  | Array of Object  | 生成的事件记忆列表。  |
|    * -event_id  | String  | 事件记忆的id。  |
|    * -event_type  | String  | 事件类型的名称。  |
|    * -memory_info  <br>  <br>   | Object  <br>   | 事件记忆的内容。包含： <br>  <br> * 原始的多轮对话信息。 <br> * 事件的属性：对于内置事件sys_event_v1，只有summary；对于内置事件sys_profile_collect_v1，只有user_profile；对于自定义事件，按照自定义的属性字段展示。  |
|    * -user_id  | Array of String  | 事件归属的user_id。  |
|    * -assitant_id  | Array of String  | 画像归属的assitant_id。  |
|    * -time  | Integer  | 记忆的创建时间，毫秒级时间戳。  |
| * messages  | Array of Object  | 对话消息列表.  |
|    * -content  | String  | 发言内容。  |
|    * -message_id  | String  | 对话id。  |
|    * -role  | String  | 发言人角色。  |
|    * -role_id  | String  | 发言人ID  |
|    * -role_name  | String  | 发言人名称。  |
|    * -time  | Integer  | 发言时间，毫秒级时间戳。  |
| * session_id  | String  | 当前对话或消息批次的会话 ID。  |
| * status  | String  | 当前session的处理进度，枚举值：processing, success, failed。  |
| * time  | Integer  | 当前session的统一发生时间，毫秒级时间戳。  |
| * user_ids  | Array of String  | 当前session关联的user列表。  |
| * assistant_ids  | Array of String  | 当前session关联的assitant列表。  |
| request_id  | String  | 标识每个请求的唯一ID。  |
# 示例代码
## **Python请求**
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
    collection_name="my_first_memory_collection1",  # 用您的记忆库名称替代
    project_name="default"
)

# 获取会话信息
result = collection.get_session_info(
    session_id="session_001",
)

print(f"=== 获取会话信息结果 ===\n{result}")
```

