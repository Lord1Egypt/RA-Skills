# 概述
DeleteVikingdbIndex 接口用于删除指定 Collection 下的索引，删除后无法恢复。
# 方法定义
Python SDK 通过 `VIKINGDBApi().delete_vikingdb_index(request)` 发起调用，`request` 类型为 `volcenginesdkvikingdb.DeleteVikingdbIndexRequest`。
# **请求参数**
| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| project_name | str | 否 | 项目名称，对应 API 字段 `ProjectName`，默认 default。 |
| collection_name | str | 二选一 | 索引所属的 Collection 名称，对应 API 字段 `CollectionName`。 |
| resource_id | str |  | Collection 资源 ID，对应 API 字段 `ResourceId`。 |
| index_name | str | 是 | 需要删除的索引名称，对应 API 字段 `IndexName`。 |
# 返回参数
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| message | str | 状态信息，对应 API 字段 `Message`。 |
# 示例
## Python 示例
```python
import os
import volcenginesdkcore
import volcenginesdkvikingdb as vdb
from volcenginesdkvikingdb.api.vikingdb_api import VIKINGDBApi

configuration = volcenginesdkcore.Configuration()
configuration.ak = os.environ["VIKINGDB_AK"]
configuration.sk = os.environ["VIKINGDB_SK"]
configuration.region = os.environ["VIKINGDB_REGION"]
configuration.host = os.environ["VIKINGDB_HOST"]
configuration.scheme = "https"
volcenginesdkcore.Configuration.set_default(configuration)

client = VIKINGDBApi()

request = vdb.DeleteVikingdbIndexRequest(
    project_name="default",
    collection_name="sdk_demo_collection",
    index_name="sdk_demo_index",
)

response = client.delete_vikingdb_index(request)
print("message:", response.message)
```


