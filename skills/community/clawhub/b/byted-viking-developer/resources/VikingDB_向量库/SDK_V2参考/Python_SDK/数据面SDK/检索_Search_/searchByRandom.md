# 概述
随机检索是一种在未指定查询内容的情况下，从数据集中随机返回若干条记录的检索方式。随机检索同样支持过滤和对检索结果的后处理，可用于对比召回效果、数据过滤等场景。
`search_by_random` 会在满足过滤条件的数据中随机返回若干条记录。
# **请求参数**
请求参数是 `SearchByRandomRequest`，其字段如下表所示。
| **名称** | **类型** | **必选** | **描述** |
| --- | --- | --- | --- |
| filter | Optional[Dict[str, Any]] | 否 | 标量过滤条件，详见**标量过滤**。 <br>  <br> * 不填表示在集合全量数据中随机返回。 <br> * 支持 must、must_not、range、range_out 等算子，可用 and / or 组合。 |
| output_fields | Optional[List[str]] | 否 | 要返回的标量字段列表。 <br>  <br> 1. 未设置时返回集合内所有标量字段。 <br> 2. 传入空列表表示不返回任何标量字段。 <br> 3. 字段名必须存在于 collection schema，否则请求报错。 |
| limit | Optional[int] | 否 | 限制返回条数，最大 5000。 |
| offset | Optional[int] | 否 | 分页偏移量，默认 0。 |
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
## 请求参数
```python
import os
import json

from vikingdb import IAM
from vikingdb.vector import SearchByRandomRequest, VikingVector

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
request = SearchByRandomRequest(
    limit=3,
    output_fields=["title"],
)
response = index_client.search_by_random(request)
print(f"request_id={response.request_id}")
# 打印完整响应 JSON
print(response.model_dump_json(indent=2, by_alias=True) if hasattr(response, "model_dump_json") else json.dumps(response.model_dump(by_alias=True, mode="json"), ensure_ascii=False, indent=2, sort_keys=True))
```



