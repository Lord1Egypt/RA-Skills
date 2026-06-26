# 概述
UpdateVikingdbIndex 接口用于修改已存在索引的描述、标量索引、CPU 配额或分片策略。
# 方法定义
Python SDK 通过 `VIKINGDBApi().update_vikingdb_index(request)` 发起调用，`request` 类型为 `volcenginesdkvikingdb.UpdateVikingdbIndexRequest`。
# **请求参数**
| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| project_name | str | 否 | 项目名称，对应 API 字段 `ProjectName`，默认 default。 |
| collection_name | str | 二选一 | 索引所属数据集，对应 API 字段 `CollectionName`。 |
| resource_id | str |  | Collection 资源 ID，对应 API 字段 `ResourceId`。 |
| index_name | str | 是 | 要更新的索引名称，对应 API 字段 `IndexName`。 |
| description | str | 否 | 索引描述，对应 API 字段 `Description`。 |
| cpu_quota | int | 否 | 索引可用 CPU 配额，对应 API 字段 `CpuQuota`，需 >= 1。 |
| scalar_index | list[str] | 否 | 新的标量索引字段列表，对应 API 字段 `ScalarIndex`。 |
| shard_policy | str | 否 | 分片策略，对应 API 字段 `ShardPolicy`，支持 `auto`、`custom`。 |
| shard_count | int | 否 | 分片数，对应 API 字段 `ShardCount`，仅当 `shard_policy`=custom 时生效。 |
# 返回参数
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| message | str | 请求处理结果，对应 API 字段 `Message`。 |
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

request = vdb.UpdateVikingdbIndexRequest(
    project_name="default",
    collection_name="sdk_demo_collection",
    index_name="sdk_demo_index",
    description="Updated description",
    shard_policy="custom",
    shard_count=2,
)

response = client.update_vikingdb_index(request)
print("message:", response.message)
```


