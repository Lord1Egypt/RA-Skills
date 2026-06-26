# 概述
聚合统计用于对索引中的标量字段做分组统计，可配合过滤条件快速了解数据分布。
索引中至少要有一个 string、int64 或 bool 类型的标量索引字段，可供聚合或筛选。

# 请求体参数
| 参数名 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| resource_id | Optional[str] | 二选一 | 资源 ID。与 `collection_name` 二选一，用于定位集合。 |
| collection_name | Optional[str] |  | 集合名称。若通过名称访问索引，可配合 `project_name` 使用。 |
| project_name | Optional[str] | 否 | 项目名称。与 `collection_name` 组合使用时可进一步限定作用域。 |
| index_name | str | 是 | 索引名称。 |
| filter | Optional[Dict[str, Any]] | 否 | 向量检索通用过滤条件，语法与搜索接口一致，未指定时不过滤。 |
| partition | Optional[str] | 否 | 指定要聚合的分区名称。 |
| op | str | 是 | 聚合算子，当前仅支持 `count`。 |
| field | Optional[str] | 否 | 需要分组聚合的标量字段。支持 string、int64 或 bool 类型且需建立索引。 |
| cond | Optional[Dict[str, Any]] | 否 | 聚合后的二次过滤条件，类似 SQL `HAVING`。目前 count 仅支持 `gt` 比较语法。 |
| order | Optional[str] | 否 | 聚合结果排序方向，例如 `desc`。 |
## 返回参数
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| request_id | Optional[str] | 请求链路 ID，可用于排查。 |
| code | Optional[str] | 错误码，成功时为空。 |
| message | Optional[str] | 错误信息。 |
| api | Optional[str] | 实际调用的 API 名称。 |
| result | Optional[AggResult] | 聚合结果，失败或无结果时可能为 `None`。 |
AggResult 结构：
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| agg | Dict[str, Any] | 聚合结果字典。按字段值返回计数，若不指定 `field`，则包含 `_total`。 |
| op | Optional[str] | 聚合算子名称。 |
| field | Optional[str] | 参与聚合的字段名。 |
# 示例
示例中所需变量（如 `VIKINGDB_AK`、`VIKINGDB_COLLECTION` 等）请在运行前配置到环境变量。

```python
import json
import os

from vikingdb import IAM
from vikingdb.vector import AggRequest, VikingVector

auth = IAM(ak=os.environ["VIKINGDB_AK"], sk=os.environ["VIKINGDB_SK"])
client = VikingVector(
    host=os.environ["VIKINGDB_HOST"],
    region=os.environ["VIKINGDB_REGION"],
    auth=auth,
    scheme="https",
)

index = client.index(
    collection_name=os.environ["VIKINGDB_COLLECTION"],
    project_name=os.getenv("VIKINGDB_PROJECT"),
    index_name=os.environ["VIKINGDB_INDEX"],
)

# SELECT category, COUNT(*) FROM index WHERE score >= 60 AND score <= 100 GROUP BY category HAVING COUNT(*) > 5
request = AggRequest(
    op="count",
    filter={"op": "range", "field": "score", "gte": 60, "lte": 100},
    field="category",
    cond={"gt": 5},
)
response = index.aggregate(request)

agg = response.result.agg if response.result else {}
print(f"aggregate request_id={response.request_id} agg={json.dumps(agg, ensure_ascii=False)}")
```


