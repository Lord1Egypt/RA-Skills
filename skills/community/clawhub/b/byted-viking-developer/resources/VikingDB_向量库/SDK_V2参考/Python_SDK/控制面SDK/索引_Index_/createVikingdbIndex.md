# 概述
CreateVikingdbIndex 接口用于为指定的数据集 Collection 创建索引，以提升向量检索性能。
创建索引可以加速向量的相似度搜索，它根据指定的索引算法和数据结构将向量库中的原始数据进行分组排序，提高相似度搜索的效率和准确性，是驱动向量数据库在短时间内筛选出候选的核心所在。
对于索引的数据集只存在稠密向量（即 vector 类型字段）的情况，我们称这种索引为纯稠密索引；对于索引的数据集中存在稠密向量和稀疏向量（vector 和 sparse_vector 类型字段）的情况，我们称这种索引为混合索引。
# 方法定义
Python SDK 通过 `VIKINGDBApi().create_vikingdb_index(request)` 发起调用，`request` 类型为 `volcenginesdkvikingdb.CreateVikingdbIndexRequest`。
# **请求参数**
下表列出了 CreateVikingdbIndexRequest 可配置的字段，字段含义可结合 `examples/vikingdb_examples.py` 中的示例理解。
| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| project_name | str | 否 | 项目名称，对应 API 字段 `ProjectName`，默认为 default。 |
| collection_name | str | 二选一 | 数据集名称，对应 API 字段 `CollectionName`，与 `resource_id` 至少填写一个。 |
| resource_id | str |  | Collection 的资源 ID，对应 API 字段 `ResourceId`。 |
| index_name | str | 是 | 要创建的索引名，对应 API 字段 `IndexName`。 <br>  <br> * 以字母开头，可包含字母、数字、下划线，长度 1-128 字节。 <br> * 同一 Collection 内必须唯一。 <br> * 同账号下，index 数量不超过200个 |
| description | str | 否 | 索引描述，对应 API 字段 `Description`，最长 65535 字节。 |
| cpu_quota | int | 否 | 创建/检索索引使用的 CPU 配额，对应 API 字段 `CpuQuota`，需 >= 1。 |
| scalar_index | list[str] | 否 | 要建立标量索引的字段名列表，对应 API 字段 `ScalarIndex`，仅支持集合中已存在的字段。 |
| shard_policy | str | 否 | 分片策略，对应 API 字段 `ShardPolicy`，支持 `auto`（默认）与 `custom`。 |
| shard_count | int | 否 | 索引分片数，对应 API 字段 `ShardCount`，当 `shard_policy` 为 `custom` 时生效。 |
| vector_index | VectorIndexForCreateVikingdbIndexInput | 否 | 向量索引配置，对应 API 字段 `VectorIndex`，见下表。 |

* VectorIndexForCreateVikingdbIndexInput 参数结构

| 参数 | 类型 | 是否必选 | 默认值 | 描述 |
| --- | --- | --- | --- | --- |
| index_type | str | 否 | - | 索引类型，对应 API 字段 `IndexType`。常见取值：`hnsw`、`hnsw_hybrid`、`flat`、`diskann`。 |
| distance | str | 否 | - | 向量距离类型，对应 API 字段 `Distance`，支持 `ip`、`cosine`、`l2`。 |
| hnsw_m | int | 否 | - | HNSW 图的最大邻居数，对应 API 字段 `HnswM`。 |
| hnsw_cef | int | 否 | - | HNSW CEF（构建图时的搜索广度），对应 API 字段 `HnswCef`。 |
| hnsw_sef | int | 否 | - | HNSW SEF（在线检索的搜索广度），对应 API 字段 `HnswSef`。 |
| diskann_m | int | 否 | - | DiskANN 图每个节点的出度，对应 API 字段 `DiskannM`，仅 DiskANN 索引生效。 |
| diskann_cef | int | 否 | - | DiskANN 构建/查询时的扩展因子，对应 API 字段 `DiskannCef`。 |
| cache_ratio | float | 否 | - | 磁盘索引的热点缓存比例，对应 API 字段 `CacheRatio`。 |
| pq_code_ratio | float | 否 | - | PQ 压缩比例，对应 API 字段 `PqCodeRatio`。 |
| quant | str | 否 | - | 量化类型，对应 API 字段 `Quant`，支持 `int8`、`fix16`、`float`、`pq`。 |
# 返回参数
返回值类型为 `CreateVikingdbIndexResponse`。
| 参数 | 类型 | 示例值 | 描述 |
| --- | --- | --- | --- |
| message | str | success | 请求状态描述，对应 API 字段 `Message`。 |
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

request = vdb.CreateVikingdbIndexRequest(
    project_name="default",
    collection_name="sdk_demo_collection",
    index_name="sdk_demo_index",
    description="Demo HNSW index",
    shard_policy="auto",
    vector_index=vdb.VectorIndexForCreateVikingdbIndexInput(
        index_type="hnsw",
        distance="cosine",
        hnsw_m=32,
        hnsw_cef=200,
    ),
)

response = client.create_vikingdb_index(request)
print("message:", response.message)
```


