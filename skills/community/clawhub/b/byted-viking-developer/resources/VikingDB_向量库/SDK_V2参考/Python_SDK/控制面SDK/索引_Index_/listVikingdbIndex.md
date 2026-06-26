# 概述
ListVikingdbIndex 接口用于查询某个项目下的索引列表，可按 Collection、索引名关键字或状态过滤。
# 方法定义
Python SDK 通过 `VIKINGDBApi().list_vikingdb_index(request)` 发起调用，`request` 类型为 `volcenginesdkvikingdb.ListVikingdbIndexRequest`。
# **请求参数**
| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| project_name | str | 否 | 项目名称，对应 API 字段 `ProjectName`，默认 default。 |
| page_number | int | 否 | 页码，对应 API 字段 `PageNumber`，从 1 开始，允许 0 表示第一页。 |
| page_size | int | 否 | 单页条数，对应 API 字段 `PageSize`，范围 1-100。 |
| filter | FilterForListVikingdbIndexInput | 否 | 过滤条件，对应 API 字段 `Filter`，结构如下。 |

* FilterForListVikingdbIndexInput

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| collection_name | list[str] | 根据 Collection 名称过滤，对应 API 字段 `CollectionName`。 |
| index_name_keyword | str | 索引名关键字匹配，对应 API 字段 `IndexNameKeyword`。 |
| status | list[str] | 索引状态过滤，对应 API 字段 `Status`（如 CREATING、ACTIVE、FAILED）。 |
# 返回参数
返回值类型为 `ListVikingdbIndexResponse`。
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| indexes | list[IndexForListVikingdbIndexOutput] | 索引详情列表，对应 API 字段 `Indexes`。 |
| page_number | int | 当前页码，对应 API 字段 `PageNumber`。 |
| page_size | int | 列表大小，对应 API 字段 `PageSize`。 |
| total_count | int | 满足条件的索引总数，对应 API 字段 `TotalCount`。 |

* IndexForListVikingdbIndexOutput

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
| scalar_index | list[ScalarIndexForListVikingdbIndexOutput] | 标量索引字段定义，对应 API 字段 `ScalarIndex`，结构见下表。 |
| vector_index | VectorIndexForListVikingdbIndexOutput | 向量索引配置，对应 API 字段 `VectorIndex`，结构与创建时一致。 |
| index_names | list[str] | Collection 下的索引名集合，对应 API 字段 `IndexNames`。 |

* ScalarIndexForListVikingdbIndexOutput

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| field_name | str | 字段名称，对应 API 字段 `FieldName`。 |
| field_type | str | 字段类型，对应 API 字段 `FieldType`。 |
| dim | int | 向量维度（如适用），对应 API 字段 `Dim`。 |
| default_value | object | 默认值，对应 API 字段 `DefaultValue`。 |
| is_primary_key | bool | 是否主键，对应 API 字段 `IsPrimaryKey`。 |

* VectorIndexForListVikingdbIndexOutput

| 字段 | 类型 | 描述 |
| --- | --- | --- |
| index_type | str | 索引类型 `IndexType`（如 hnsw、diskann、flat、hnsw_hybrid）。 |
| distance | str | 距离度量 `Distance`（ip/cosine/l2）。 |
| quant | str | 量化方式 `Quant`（int8/fix16/float/pq）。 |
| hnsw_m | int | HNSW 图邻居数，对应 API 字段 `HnswM`。 |
| hnsw_cef | int | HNSW 构图广度 `HnswCef`。 |
| hnsw_sef | int | HNSW 在线检索广度 `HnswSef`。 |
| diskann_m | int | DiskANN 图出度 `DiskannM`。 |
| diskann_cef | int | DiskANN 扩展因子 `DiskannCef`。 |
| cache_ratio | float | 热点缓存比例 `CacheRatio`。 |
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

request = vdb.ListVikingdbIndexRequest(
    project_name="default",
    page_number=1,
    page_size=10,
    filter=vdb.FilterForListVikingdbIndexInput(
        collection_name=["sdk_demo_collection"],
        index_name_keyword="sdk",
    ),
)

response = client.list_vikingdb_index(request)
print("total_count:", response.total_count)
for idx in response.indexes or []:
    print(idx.index_name, idx.vector_index.index_type if idx.vector_index else None)
```


