# 概述
接口适用于含有 int64/float32 类型标量索引字段的索引。向量数据库中的标量检索指的是基于标量值的检索方法。在向量数据库中，每个向量都有一个或多个标量值，标量检索可以基于这些标量值进行检索，找到与查询相关的数据。例如文档检索中的作者特征检索。
`search_by_scalar` 按标量字段进行排序/分页返回结果。
# 请求参数
请求参数是 `SearchByScalarRequest`，其字段如下表所示。
| **名称** | **类型** | **必选** | **描述** |
| --- | --- | --- | --- |
| field | str | 是 | 排序使用的标量字段，需为 int64/float32 且已建立标量索引。 |
| order | Optional[str] | 否 | 排序方向，取值 `asc`/`desc`，默认 `desc`。 |
| filter | Optional[Dict[str, Any]] | 否 | 标量过滤条件，详见**标量过滤**。 <br>  <br> * 不填表示对全量索引进行排序。 <br> * 支持 must、must_not、range、range_out 等算子，可用 and / or 组合。 |
| output_fields | Optional[List[str]] | 否 | 要返回的标量字段列表。 <br>  <br> 1. 未设置时返回集合内所有标量字段。 <br> 2. 传入空列表表示不返回任何标量字段。 <br> 3. 字段名必须存在于 collection schema，否则请求报错。 |
| limit | Optional[int] | 否 | 限制返回条数，最大 5000。 |
| offset | Optional[int] | 否 | 分页偏移量，默认 0，过大时会出现深分页性能开销。 |
| partition | Optional[str] | 否 | 仅检索指定分区，默认搜索全部分区。 |
| advance | Optional[SearchAdvance] | 否 | 高级参数集合（post_process_ops、ids_in 等），详见[检索公共参数](/c8p1dfoq/dhd9lm8y) <br> 。 |
# 返回参数
| 名称 | 类型 | 描述 |
| --- | --- | --- |
| request_id | Optional[str] | 请求链路 ID。 |
| code | Optional[str] | 服务返回码，Success 表示成功。 |
| message | Optional[str] | 错误或提示信息。 |
| api | Optional[str] | 具体调用的 API 名称。 |
| result | Optional[SearchResult] | 检索结果主体，结构见下。 |

* SearchResult

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| data | List[SearchItemResult] | 召回到的结果列表，结构见下。 |
| filter_matched_count | Optional[int] | 满足过滤条件的文档总数。 |
| total_return_count | Optional[int] | 本次返回的结果数量。 |
| real_text_query | Optional[str] | 模型可能修正后的真实查询串。 |
| token_usage | Dict[str, Any] | token 计量信息。 |

* SearchItemResult

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| id | Any | 主键值。 |
| fields | Dict[str, Any] | 返回的标量字段内容。 |
| score | Optional[float] | 最终相似度得分。 |
| ann_score | Optional[float] | ANN 粗排得分。 |
# 示例
```python
import os

from vikingdb import IAM
from vikingdb.vector import SearchByScalarRequest, VikingVector

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
request = SearchByScalarRequest(
    field="score",
    order="desc",
    limit=10,
    output_fields=["title", "score"],
)
response = index_client.search_by_scalar(request)
if response.result:
    for item in response.result.data:
        print(item.id, item.fields.get("score"))
```



