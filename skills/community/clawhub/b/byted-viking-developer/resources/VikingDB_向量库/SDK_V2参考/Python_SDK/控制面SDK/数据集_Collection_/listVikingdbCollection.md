# 概述
ListVikingdbCollection 接口用于查询当前项目下的 Collection 列表，支持分页与名称关键字过滤。
# 方法定义
Python SDK 通过 `VIKINGDBApi().list_vikingdb_collection(request)` 调用，`request` 类型为 `volcenginesdkvikingdb.ListVikingdbCollectionRequest`。
# **请求参数**
| **参数** | **类型** | **是否必选** | **说明** |
| --- | --- | --- | --- |
| project_name | str | 否 | 项目名称，对应 API 字段 `ProjectName`，默认 default。 |
| page_size | int | 否 | 分页大小，对应 API 字段 `PageSize`，取值 1-100，默认 10。 |
| page_number | int | 否 | 分页页码，对应 API 字段 `PageNumber`，从 1 开始。 |
| filter | FilterForListVikingdbCollectionInput | 否 | 过滤条件，对应 API 字段 `Filter`。 |

* FilterForListVikingdbCollectionInput

| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| collection_name_keyword | str | 否 | 集合名称关键字，对应 API 字段 `CollectionNameKeyword`，用于模糊搜索。 |
# 返回参数
接口返回 `ListVikingdbCollectionResponse`，包含分页信息与集合列表。
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| total_count | int | 集合总数，对应 API 字段 `TotalCount`。 |
| page_number | int | 当前页码，对应 API 字段 `PageNumber`。 |
| page_size | int | 本页返回条数，对应 API 字段 `PageSize`。 |
| collections | list[CollectionForListVikingdbCollectionOutput] | 集合详情列表，对应 API 字段 `Collections`。 |

* CollectionForListVikingdbCollectionOutput

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| collection_name | str | 集合名称，对应 API 字段 `CollectionName`。 |
| project_name | str | 所属项目，对应 API 字段 `ProjectName`。 |
| resource_id | str | 集合 ID，对应 API 字段 `ResourceId`。 |
| description | str | 集合描述，对应 API 字段 `Description`。 |
| create_time | str | 创建时间 (RFC3339)，对应 API 字段 `CreateTime`。 |
| update_time | str | 更新时间，对应 API 字段 `UpdateTime`。 |
| update_person | str | 最近操作人，对应 API 字段 `UpdatePerson`。 |
| enable_keywords_search | bool | 是否开启关键词检索，对应 API 字段 `EnableKeywordsSearch`。 |
| index_count | int | 索引数量，对应 API 字段 `IndexCount`。 |
| index_names | list[str] | 索引名称列表，对应 API 字段 `IndexNames`。 |
| fields | list[FieldForListVikingdbCollectionOutput] | 字段列表，对应 API 字段 `Fields`。 |
| collection_stats | CollectionStatsForListVikingdbCollectionOutput | 统计信息，对应 API 字段 `CollectionStats`。 |
| tags | list[TagForListVikingdbCollectionOutput] | 标签信息，对应 API 字段 `Tags`。 |
| vectorize | VectorizeForListVikingdbCollectionOutput | 向量化配置，对应 API 字段 `Vectorize`。 |

* FieldForListVikingdbCollectionOutput

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| field_name | str | 字段名称，对应 API 字段 `FieldName`。 |
| field_type | str | 字段类型，对应 API 字段 `FieldType`。 |
| is_primary_key | bool | 是否主键，对应 API 字段 `IsPrimaryKey`。 |
| dim | int | 向量维度，对应 API 字段 `Dim`。 |
| default_value | object | 默认值，对应 API 字段 `DefaultValue`。 |

* CollectionStatsForListVikingdbCollectionOutput

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| data_count | int | 集合中文档条数，对应 API 字段 `DataCount`。 |
| data_storage | int | 存储量（Byte），对应 API 字段 `DataStorage`。 |

* TagForListVikingdbCollectionOutput

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| key | str | 标签键，对应 API 字段 `Key`。 |
| value | str | 标签值，对应 API 字段 `Value`。 |

* VectorizeForListVikingdbCollectionOutput

| 参数 | 类型 | 说明 |
| --- | --- | --- |
| dense | DenseForListVikingdbCollectionOutput | 稠密向量化配置，对应 API 字段 `Dense`，字段含义同 Get 接口。 |
| sparse | SparseForListVikingdbCollectionOutput | 稀疏向量化配置，对应 API 字段 `Sparse`。 |
# 示例
## 请求示例
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

request = vdb.ListVikingdbCollectionRequest(
    project_name="default",
    page_number=1,
    page_size=10,
    filter=vdb.FilterForListVikingdbCollectionInput(collection_name_keyword="demo"),
)
response = client.list_vikingdb_collection(request)

print("total:", response.total_count)
for item in response.collections or []:
    print(item.collection_name, item.resource_id)
```


