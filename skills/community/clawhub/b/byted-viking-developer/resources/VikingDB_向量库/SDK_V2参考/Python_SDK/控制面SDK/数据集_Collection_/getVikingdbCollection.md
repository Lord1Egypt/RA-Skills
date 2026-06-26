# 概述
GetVikingdbCollection 接口用于查询指定 Collection 的元信息、字段配置以及向量化设置。
# 方法定义
Python SDK 通过 `VIKINGDBApi().get_vikingdb_collection(request)` 调用，`request` 类型为 `volcenginesdkvikingdb.GetVikingdbCollectionRequest`。
# **请求参数**
| **参数** | **类型** | **是否必选** | **参数说明** |
| --- | --- | --- | --- |
| project_name | str | 否 | 项目名称，对应 API 字段 `ProjectName`，默认值为 default。 |
| collection_name | str | 2选1 | 集合名称，对应 API 字段 `CollectionName`。需以字母开头，只能包含字母/数字/下划线，长度 1-128。 |
| resource_id | str |  | 集合资源 ID，对应 API 字段 `ResourceId`。可与 `collection_name` 二选一或同时传递以保证精确定位。 |
# 返回参数
成功响应返回 `GetVikingdbCollectionResponse`，包含如下字段：
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| project_name | str | 集合所属项目，对应 API 字段 `ProjectName`。 |
| resource_id | str | 集合资源 ID，对应 API 字段 `ResourceId`。 |
| collection_name | str | 集合名称，对应 API 字段 `CollectionName`。 |
| description | str | 集合描述，对应 API 字段 `Description`。 |
| create_time | str | 创建时间 (RFC3339)，对应 API 字段 `CreateTime`。 |
| update_time | str | 最后更新时间，对应 API 字段 `UpdateTime`。 |
| update_person | str | 最近操作人，对应 API 字段 `UpdatePerson`。 |
| enable_keywords_search | bool | 是否开启关键词检索，对应 API 字段 `EnableKeywordsSearch`。 |
| index_count | int | 集合下索引数量，对应 API 字段 `IndexCount`。 |
| index_names | list[str] | 索引名称列表，对应 API 字段 `IndexNames`。 |
| fields | list[FieldForGetVikingdbCollectionOutput] | 字段定义列表，对应 API 字段 `Fields`。 |
| collection_stats | CollectionStatsForGetVikingdbCollectionOutput | 数据量统计，对应 API 字段 `CollectionStats`。 |
| vectorize | VectorizeForGetVikingdbCollectionOutput | 向量化配置，对应 API 字段 `Vectorize`。 |

* FieldForGetVikingdbCollectionOutput

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| field_name | str | 字段名称，对应 API 字段 `FieldName`。 |
| field_type | str | 字段类型，对应 API 字段 `FieldType`。 |
| dim | int | 当字段类型为 vector 时表示稠密向量维度，对应 API 字段 `Dim`。 |
| is_primary_key | bool | 是否为主键，对应 API 字段 `IsPrimaryKey`。仅 string / int64 字段可设置为主键。 |
| default_value | object | 字段默认值，对应 API 字段 `DefaultValue`。 |

* CollectionStatsForGetVikingdbCollectionOutput

| 参数 | 类型 | 描述 |
| --- | --- | --- |
| data_count | int | 集合内数据条数，对应 API 字段 `DataCount`。 |
| data_storage | int | 集合占用存储量（Byte），对应 API 字段 `DataStorage`。 |

* VectorizeForGetVikingdbCollectionOutput 参数结构

| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| dense | VectorizeForGetVikingdbCollectionOutput | 是 | 稠密向量化配置，对应 API 字段 `Dense`，用于指定 embedding 模型、维度与输入字段。 |
| sparse | SparseForGetVikingdbCollectionOutput | 否 | 稀疏向量化配置，对应 API 字段 `Sparse`。 |

* DenseForGetVikingdbCollectionOutput 和 SparseForGetVikingdbCollectionOutput 参数结构

| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| model_name | str | 是 | 模型名称，对应 API 字段 `ModelName`。可选值见下方 embedding 模型列表。 |
| model_version | str | 否 | 模型版本，对应 API 字段 `ModelVersion`。Doubao 系模型必填，bge 系默认 `default`。 |
| dim | int | 否 | 稠密向量维度。各模型支持的维度见embedding模型列表。 |
| text_field | str | 否 | 文本向量化字段名，对应 API 字段 `TextField`。 |
| image_field | str | 否 | 图片向量化字段名，对应 API 字段 `ImageField`。 |
| video_field | str | 否 | 视频向量化字段名，对应 API 字段 `VideoField`。 |
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

request = vdb.GetVikingdbCollectionRequest(
    collection_name="sdk_demo_collection",
    project_name="default",
)
response = client.get_vikingdb_collection(request)

print("collection:", response.collection_name)
print("fields:", [f.field_name for f in (response.fields or [])])
if response.collection_stats:
    print("doc count:", response.collection_stats.data_count)
```


