# 接口概述
从指定记忆库中检索相关的事件记忆信息，可依据用户提问进行语义相似度检索，并根据查询条件划定查询范围。
# **请求接口**
| **URL** | /api/memory/event/search | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对记忆库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 基于AK/SK生成的签名信息 |
# 请求参数
| **参数** | **类型** | **是否必须** | **描述** |
| --- | --- | --- | --- |
| collection_name | String | 否 |  要检索的记忆库名称。 |
| project_name | String | 否 | 记忆库所属项目。 |
| resource_id | String | 否 | 记忆库唯一的资源 id。可选择直接传 resource_id，或同时传 collection_name 和 project_name 作为记忆库的唯一标识。 |
| query <br>  | String <br>  | 否 |  用户的检索查询语句（最大长度 4000 字符） <br>  <br> * 当传输 query 时，会针对 query 内容对记忆进行语义化匹配召回，召回记忆数量与 limit 值有关； <br> * 当不传 query 时，会返回符合 filter 条件的记忆列表，按照时间顺序返回（优先取最近的），召回记忆数量与 limit 值有关。 |
| filter | Object | 是 |  检索过滤条件和返回设置。 |
| * user_id |  String or Array of String |  否 |  用户 ID，支持单个 ID 或 ID 列表。 |
| * assistant_id |  String or Array of String |  否 |  助手 ID，支持单个 ID 或 ID 列表。 |
| * start_time |  Integer |  否 |  检索记忆的起始时间，毫秒级时间戳。 |
| * end_time |  Integer |  否 |  检索记忆的终止时间，毫秒级时间戳。 |
| * memory_type |  String or Array of String |  是 |  要检索的事件类型名称或它们的列表。 |
| * group_id |  String or Array of String |  否 |  用于过滤的群组ID。可以是单个ID或ID列表。 |
| * session_id  |  String or Array of String |  否 | 用于过滤的session ID。可以是单个ID或ID列表 |
| limit | Integer | 否 | 返回的检索结果条数，默认为10，取值范围[1, 5000]。 |
| time_decay_config | Object | 否 | 时间衰减配置。仅针对事件检索，对画像不生效。 |
|     weight | Float | 是 | 用于调节时间衰减影响力的权重，取值范围[0,1)。 |
|     no_decay_period | Integer | 否 | 无衰减期。即多长时间内的记忆权重相同，不衰减。配置单位为天，范围[0,10000]。默认值为 0。 |
| custom_weight | Float | 否 | 用于调节业务字段的重要程度，取值范围[0,1)。 |
**说明：**

*  **检索事件**：user_id 和 assistant_id 至少填写一个，也可同时填写。

# 响应消息
| **字段** | **类型** | **描述** |
| --- | --- | --- |
| code | Integer | 状态码，0 表示成功，其他表示错误。 |
| message | String | 返回信息。 |
| data | Object | 返回的详细检索结果。 |
| * collection_name |  String | 被检索的记忆库名称。 |
| * count |  Integer | 返回的检索结果数量。 |
| * result_list |  Array of Object | 检索结果列表。 |
|    * -id |  String | 事件实例的唯一ID。 |
|    * -score |  Float | 与查询的相关性得分。 |
|    * -origin_score | Float | 原始的向量检索分数。 |
|    * -time_score | Float | 时间衰减分数。 |
|    * -custom_weight_score | Float | 自定义权重分数 |
|    * -memory_type |  Array of String | 记忆类型名称。 |
|    * -user_id |  Array of String | 关联的用户ID列表。 |
|    * -assistant_id |  Array of String | 关联的助手ID列表。 |
|    * -session_id |  String | 关联的会话ID。 |
|    * -group_id |  String | 关联的群组ID。 |
|    * -time |  Integer | 记忆发生或最后更新的时间戳（毫秒）。 |
|    * -status |  String | 记忆条目的状态（预留字段）。 |
|    * -labels |  String | 记忆条目的标签（预留字段）。 |
|    * -memory_info <br>  <br>  |  Object <br>  | 额外的详细信息。其结构取决于memory_type。 <br> 对于事件，是事件的属性，再加上原始的多轮对话信息，例如： <br> ```JSON <br> { <br>     "IMAGE_URL": "https://memorydb-memory-image-dev-cn-beijing-2108758172.tos-cn-beijing.volces.com/15ff67c6-41c8-4b56-92f3-76e2874b9f58.jpeg",// 当写入数据时store_file为true，相关的图片会一起被检索并返回 <br>     "original_messages": "tutor_001(assistant):Okay, let's talk about weather. How would you say “今天天气多云但很暖和” in English?\nstudent_A(user):Today is cloudy but very warm.\ntutor_001(assistant):That's a good start! You can also say, “It's cloudy but warm today”. Your sentence structure was correct. Great job!", <br>     "answer": "Today is cloudy but very warm.", <br>     "knowledge_point_name": "天气相关表达", <br>     "question": "How would you say “今天天气多云但很暖和” in English?", <br>     "rating": "good", <br>     "rating_reasoning": "学生能够正确地用英语描述天气，符合该知识点能够基本正确描述天气的良好评价标准", <br>     "rating_score": 7 <br> } <br> ``` <br>  |
| * token_usage |  Integer | 本次检索消耗的token数量。 |
| request_id | String | 标识每个请求的唯一ID。 |
# 示例代码
## **Python请求**
```Python
import os
import requests
import json

API_KEY = os.getenv("MEMORY_API_KEY", "your_key")
url = "https://api-knowledgebase.mlp.cn-beijing.volces.com/api/memory/event/search"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "collection_name": "my_first_memory_collection",
    "query": "你猜猜那个比赛最后谁赢了",
    "limit": 5,
    "filter": {
        "user_id": "user1",
        "memory_type": ["sys_event_v1"]
    }
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print("Status Code:", response.status_code)
print("Response:", response.text)
```

