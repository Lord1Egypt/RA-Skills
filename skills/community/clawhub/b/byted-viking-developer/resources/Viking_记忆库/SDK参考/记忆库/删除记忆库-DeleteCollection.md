# 接口概述
删除一个已存在的记忆库。此操作不可逆，记忆库中的所有数据都将被永久删除。
# **请求接口**
| **URL** | /api/memory/collection/delete | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对记忆库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 基于AK/SK生成的签名信息 |
# 请求参数
| **参数名** | **类型** | **是否必须** | **描述** |
| --- | --- | --- | --- |
| CollectionName | String | 否 | 要删除的记忆库的唯一名称。 |
| ProjectName | String | 否 | 项目名称。默认为 default。 |
| ResourceId | String | 否 | 资源 ID。唯一标识符。 |
# 响应消息
操作成功时，HTTP状态码为200。
| **字段** | **类型** | **描述** |
| --- | --- | --- |
| ResponseMetadata | Object | 响应元数据信息。 |
| * Region | String | 服务区域，例如"cn-beijing"。 |
| * RequestId | String | 请求唯一标识符。 |
| * Service | String | 服务名称，如"knowledge_base_server"。 |
| * Version | String | API版本号。 |
| Result | Object | 成功与否，例如"success"。 |
# 示例代码
## **Python请求**
```Python
import volcenginesdkcore
import volcenginesdkvikingdb
from volcenginesdkcore.rest import ApiException
from volcenginesdkvikingdb import MemoryCollectionDeleteRequest, MemoryCollectionDeleteResponse
host="vikingdb.cn-beijing.volcengineapi.com"
# 全局设置
configuration = volcenginesdkcore.Configuration()
configuration.ak =  "your_ak"
configuration.sk = "your_sk"
configuration.debug = True
configuration.host = host
configuration.region = "cn-beijing"
configuration.scheme="https"
configuration.client_side_validation = True
volcenginesdkcore.Configuration.set_default(configuration)
api_instance = volcenginesdkvikingdb.VIKINGDBApi()
try:
    body:MemoryCollectionDeleteRequest = MemoryCollectionDeleteRequest(collection_name="my_first_memory_collection")
    res:MemoryCollectionDeleteResponse = api_instance.memory_collection_delete(body)
    print(res.to_dict())
except ApiException as e:
    pass
```

