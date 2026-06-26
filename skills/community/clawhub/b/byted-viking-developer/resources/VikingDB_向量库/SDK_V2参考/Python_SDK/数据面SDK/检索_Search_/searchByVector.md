# 概述
`search_by_vector` 用于向量检索。根据查询的向量，搜索与其距离最近的 limit 个向量。
* Collection 数据写入/删除后，Index 数据更新时间预计 20s，不能立即在 Index 检索到。
* 当请求参数 filter 配置时，表示混合检索；当请求参数 filter 没有配置时，表示纯向量检索。

# 前提条件

* 通过 create_collection 接口创建数据集时，定义字段 fields 已添加 vector 字段。
* 通过 upsert_data 接口写入数据时，已写入 vector 类型的字段名称和字段值。
* 通过 create_index 创建索引时，已创建 vector_index 向量索引。

适用于创建向量库时选择"已有向量数据" ：当导入的数据是向量时，可以通过此接口输入向量进行检索。

# **请求参数**
请求参数是 `SearchByVectorRequest`，其字段如下表所示。
| **名称** | **类型** | **必选** | **描述** |
| --- | --- | --- | --- |
| dense_vector | List[float] | 是 | 用于检索的稠密向量，长度需与索引维度一致。 |
| sparse_vector | Optional[Dict[str, float]] | 否 | 稀疏向量表示（如 BOW），用于与 dense_vector 混合检索。 |
| filter | Optional[Dict[str, Any]] | 否 | 标量过滤条件，详见**标量过滤** <br>  <br> * 不填表示纯向量检索。 <br> * 支持 must、must_not、range、range_out 等算子，可用 and / or 组合。 |
| output_fields | Optional[List[str]] | 否 | 要返回的标量字段列表。 <br>  <br> 1. 未设置时返回集合内所有标量字段。 <br> 2. 传入空列表表示不返回任何标量字段。 <br> 3. 字段名必须存在于 collection schema，否则请求报错。 |
| limit | Optional[int] | 否 | 限制返回条数，最大 5000。 |
| offset | Optional[int] | 否 | 分页偏移量，默认 0，过大时会出现深分页性能开销。 |
| partition | Optional[str] | 否 | 仅检索指定分区，默认搜索全部分区数据。 |
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

from vikingdb import IAM
from vikingdb.vector import SearchByVectorRequest, VikingVector

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
request = SearchByVectorRequest(
    dense_vector=[0.5] * 1024,  # replace with real same-dim vector
    limit=5,
    output_fields=["title", "score"],
)
response = index_client.search_by_vector(request)
if response.result:
    for item in response.result.data:
        print(item.id, item.score, item.fields.get("title"))
```



