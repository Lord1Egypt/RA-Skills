# 概述
DeleteCollection 用于删除已创建的数据集 Collection。
* 执行 Collection 删除将会永久删除指定 Collection 下的所有数据，请谨慎操作。
* 在删除 Collection 之前，必须先删除 Collection 关联的所有 Index，才能成功删除 Collection。

# 方法定义
Python SDK 通过 `VIKINGDBApi().delete_vikingdb_collection(request)` 调用，`request` 类型为 `volcenginesdkvikingdb.DeleteVikingdbCollectionRequest`。
# **请求参数**
| **参数** | **类型** | **是否必选** | **参数说明** |
| --- | --- | --- | --- |
| project_name | str | 否 | 项目名称，对应 API 字段 `ProjectName`，默认 default。 |
| collection_name | str | 2选1 | 待删除集合名称，对应 API 字段 `CollectionName`。 <br>  <br> * 以字母开头，仅可包含字母、数字、下划线，长度 1-128。 <br> * 服务端允许与 `resource_id` 二选一，但当前 Python SDK 强制要求填写 `collection_name`。 |
| resource_id | str |  | 集合资源 ID，对应 API 字段 `ResourceId`。可与 `collection_name` 组合使用，帮助在控制面追踪。 |
# 返回参数
| 参数 | 类型 | 示例值 | 描述 |
| --- | --- | --- | --- |
| message | str | success | 操作结果描述，对应 API 字段 `Message`。 |
# 示例
## 请求参数
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

request = vdb.DeleteVikingdbCollectionRequest(
    collection_name="sdk_demo_collection",
    project_name="default",
)
response = client.delete_vikingdb_collection(request)
print(response.message or "delete request finished")
```



