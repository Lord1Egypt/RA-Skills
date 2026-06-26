# 概述
updateCollection 用于为指定数据集 Collection 增加字段。
Collection 支持新增字段 fields，已定义字段 fields 不支持修改，仅支持修改数据集描述。

# 方法定义
Python SDK 通过 `VIKINGDBApi().update_vikingdb_collection(request)` 调用，`request` 类型为 `volcenginesdkvikingdb.UpdateVikingdbCollectionRequest`。
# **请求参数**
请求参数是 UpdateCollectionParam，UpdateCollectionParam 类包括的参数如下表所示。
| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| project_name | str | 否 | 项目名称，对应 API 字段 `ProjectName`，默认 default。 |
| collection_name | str | 二选一 | 集合名称，对应 API 字段 `CollectionName`。以字母开头，仅可包含字母、数字、下划线，长度 1-128。可与 `resource_id` 二选一。 |
| resource_id | str |  | 集合资源 ID，对应 API 字段 `ResourceId`。与 `collection_name` 二选一，推荐同时填写确保准确。 |
| description | str | 否 | 集合描述，对应 API 字段 `Description`，最长 65535 字节。 |
| fields | list[FieldForUpdateVikingdbCollectionInput] | 是 | 新增字段列表，对应 API 字段 `Fields`。单个集合总字段数上限 128，仅支持追加新字段。 |

* Field 参数结构

| 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- |
| field_name | str | 是 | 新增字段名称，对应 API 字段 `FieldName`。需以字母开头，长度 1-128。 |
| field_type | str | 是 | 字段类型，对应 API 字段 `FieldType`，支持 vector/sparse_vector/string/int64/float32/bool/list<string>/list<int64>/text/image/video/date_time/geo_point。 |
| default_value | object | 否 | 默认值配置，对应 API 字段 `DefaultValue`。vector/sparse_vector/text/image/video 类型不支持。 |
| dim | int | 否 | 向量维度，对应 API 字段 `Dim`。vector 字段需设置 4-4096 且为 4 的倍数。 |
| is_primary_key | bool | 否 | 是否设置为主键，对应 API 字段 `IsPrimaryKey`，仅 string/int64 支持。 |
# 返回参数
| 参数 | 类型 | 示例值 | 描述 |
| --- | --- | --- | --- |
| message | str | success | 操作结果描述，对应 API 字段 `Message`。 |
## 示例
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

request = vdb.UpdateVikingdbCollectionRequest(
    collection_name="sdk_demo_collection",
    description="append new fields",
    fields=[
        vdb.FieldForUpdateVikingdbCollectionInput(
            field_name="new_tag",
            field_type="string",
        ),
        vdb.FieldForUpdateVikingdbCollectionInput(
            field_name="extra_score",
            field_type="float32",
        ),
    ],
)
response = client.update_vikingdb_collection(request)
print(response.message or "update submitted")
```



