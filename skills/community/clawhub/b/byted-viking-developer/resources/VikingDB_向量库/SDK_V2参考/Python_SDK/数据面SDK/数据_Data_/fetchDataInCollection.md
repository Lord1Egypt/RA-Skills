# 概述
根据主键在指定的 Collection 中查询单条或多条数据，单次最多可查询100条数据。
Collection 数据写入/删除后，可以实时查询数据。
# **请求参数**
| 参数名 | 类型 | 必选 | 默认值 | 备注 |
| --- | --- | --- | --- | --- |
| collection_name | str | 2选1 | - | Collection 名称，与 resource_id 二选一。 |
| resource_id | str |  | - | Collection 资源 ID。 |
| ids | List[Any] | 是 | - | * 要查询的主键列表，最多100条。 |
# 返回参数
响应体包含公共参数（见下方“响应体公共参数介绍”）。其中 `result` 字段类型为 FetchDataInCollectionResult：

* FetchDataInCollectionResult

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| items | List[DataItem] | 命中的数据列表，结构见下。 |
| ids_not_exist | List[Any] | 未命中的主键列表。 |

* DataItem

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| id | Any | 数据的主键。 |
| fields | Dict[str, Any] | 全部标量字段，key 为字段名。 |
## 响应体公共参数介绍
| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| request_id | string | 请求 ID。 |
| code | string | 操作状态码。成功为`Success`，否则为错误码短语。 |
| message | string | 执行信息。成功则为 `The API call was executed successfully.`。 |
| result | map | 操作结果。若无需返回数据，则 `result = null`。 |
# 示例
## 请求参数
```python
import os

from vikingdb import IAM
from vikingdb.vector import FetchDataInCollectionRequest, VikingVector

auth = IAM(
    ak=os.environ["VIKINGDB_AK"],
    sk=os.environ["VIKINGDB_SK"],
)
client = VikingVector(
    host=os.environ["VIKINGDB_HOST"],
    region=os.environ["VIKINGDB_REGION"],
    auth=auth,
    scheme="https",
)

collection_client = client.collection(collection_name=os.environ["VIKINGDB_COLLECTION"])
request = FetchDataInCollectionRequest(
    ids=[4798786918981052481, 8517775955036588997], # get ID from console or searchByRandom API
)
response = collection_client.fetch(request)
print(f"request_id={response.request_id}")
if response.result:
    for item in response.result.items:
        print(item.id, item.fields)
```



