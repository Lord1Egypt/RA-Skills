# 概述
GetVikingdbIndex 接口用于查询单个索引的详细配置，包含分片、scalar 索引及向量索引参数。
# 方法定义
Python SDK 通过 `VIKINGDBApi().get_vikingdb_index(request)` 发起调用，`request` 类型为 `volcenginesdkvikingdb.GetVikingdbIndexRequest`。
# **请求参数**
| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| project_name | str | 否 | 项目名称，对应 API 字段 `ProjectName`，默认 default。 |
| collection_name | str | 二选一 | 索引所属的数据集名称，对应 API 字段 `CollectionName`。 |
| resource_id | str |  | Collection 资源 ID，对应 API 字段 `ResourceId`。 |
| index_name | str | 是 | 要查询的索引名，对应 API 字段 `IndexName`。 |
# 返回参数
返回值类型为 `GetVikingdbIndexResponse`。
| 字段 | 类型 | 描述 |
| --- | --- | --- |
| index_name | str | 索引名称，对应 API 字段 `IndexName`。 |
| collection_name | str | 所属 Collection，对应 API 字段 `CollectionName`。 |
| project_name | str | 项目名称，对应 API 字段 `ProjectName`。 |
| resource_id | str | 索引资源 ID，对应 API 字段 `ResourceId`。 |
| description | str | 索引描述，对应 API 字段 `Description`。 |
| cpu_quota | int | 配置的 CPU 配额，对应 API 字段 `CpuQuota`。 |
| actual_cu | int | 实际使用的计算单元，对应 API 字段 `ActualCU`。 |
| shard_policy | str | 分片策略，对应 API 字段 `ShardPolicy`。 |
| shard_count | int | 分片数量，对应 API 字段 `ShardCount`。 |
| scalar_index | list[ScalarIndexForGetVikingdbIndexOutput] | 标量索引定义，对应 API 字段 `ScalarIndex`，结构见下表。 |
| vector_index | VectorIndexForGetVikingdbIndexOutput | 向量索引参数，对应 API 字段 `VectorIndex`。 |

* ScalarIndexForGetVikingdbIndexOutput

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| field_name | str | 字段名，对应 API 字段 `FieldName`。 |
| field_type | str | 字段类型，对应 API 字段 `FieldType`。 |
| dim | int | 维度（仅向量字段有值），对应 API 字段 `Dim`。 |
| default_value | object | 默认值，对应 API 字段 `DefaultValue`。 |
| is_primary_key | bool | 是否主键，对应 API 字段 `IsPrimaryKey`。 |

* VectorIndexForGetVikingdbIndexOutput

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| index_type | str | 索引类型 `IndexType`。 |
| distance | str | 距离度量 `Distance`。 |
| quant | str | 量化方式 `Quant`。 |
| hnsw_m | int | HNSW 邻居数 `HnswM`。 |
| hnsw_cef | int | HNSW 构图广度 `HnswCef`。 |
| hnsw_sef | int | HNSW 检索广度 `HnswSef`。 |
| diskann_m | int | DiskANN 图出度 `DiskannM`。 |
| diskann_cef | int | DiskANN 扩展因子 `DiskannCef`。 |
| cache_ratio | float | 缓存比例 `CacheRatio`。 |
| pq_code_ratio | float | PQ 压缩比例 `PqCodeRatio`。 |
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

request = vdb.GetVikingdbIndexRequest(
    project_name="default",
    collection_name="sdk_demo_collection",
    index_name="sdk_demo_index",
)

response = client.get_vikingdb_index(request)
print("index_name:", response.index_name)
print("vector index type:", response.vector_index.index_type if response.vector_index else None)
```


