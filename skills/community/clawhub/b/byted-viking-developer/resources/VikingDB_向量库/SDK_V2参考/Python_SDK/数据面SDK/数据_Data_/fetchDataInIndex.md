# 概述
fetchData 用于 Index 数据查询。根据主键 id，在指定的 Index 查询单条或多条数据，单次最多可查询100条数据。
Collection 数据写入/删除后，Index 数据更新时间有同步延迟，一般在10s左右，不能立即在 Index 查询到。


# **请求参数**
| 参数名 | 类型 | 必选 | 备注 |
| --- | --- | --- | --- |
| collection_name | str | 2选1 | Collection 名称，与 resource_id 二选一。 |
| resource_id | str |  | Collection 资源 ID。 |
| index_name | str | 是 | 索引名称。 |
| ids | List[Any] | 是 | 点查的主键列表，最多100条。 |
| partition | Optional[str] | 否 | 按分区过滤索引数据。 |
| output_fields | Optional[List[str]] | 否 | 控制返回的标量字段： <br>  <br> 1. 未传时返回全部标量字段。 <br> 2. 传空列表则仅返回向量与 id。 <br> 3. 字段不存在或格式错误会直接报错。 |
# 返回参数
响应体包含公共参数（见下方“响应体公共参数介绍”）。其中 `result` 字段类型为 FetchDataInIndexResult：

* FetchDataInIndexResult

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| items | List[IndexDataItem] | 命中的索引数据。 |
| ids_not_exist | List[Any] | 未命中的主键。 |

* IndexDataItem

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| id | Any | 数据主键。 |
| fields | Dict[str, Any] | 标量字段。 |
| dense_vector | Optional[List[float]] | 落盘的稠密向量。 |
| dense_dim | Optional[int] | 向量维度。 |
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
from vikingdb.vector import FetchDataInIndexRequest, VikingVector

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

index_client = client.index(
    collection_name=os.environ["VIKINGDB_COLLECTION"],
    index_name=os.environ["VIKINGDB_INDEX"],
)
request = FetchDataInIndexRequest(
    ids=[4798786918981052481, 8517775955036588997], # get ID from console or searchByRandom API
    output_fields=["title", "score"],
)
response = index_client.fetch(request)
print(f"request_id={response.request_id}")
if response.result:
    for item in response.result.items:
        print(item.id, item.dense_dim, len(item.dense_vector or []))
```



