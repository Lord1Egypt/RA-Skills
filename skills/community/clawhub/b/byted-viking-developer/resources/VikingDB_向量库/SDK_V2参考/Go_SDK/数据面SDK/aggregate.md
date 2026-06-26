# 概述
聚合统计用于对索引中的标量字段做分组统计，可配合过滤条件快速了解数据分布。
索引中至少要有一个 string、int64 或 bool 类型的标量索引字段，可供聚合或筛选。
# 请求体参数
| 参数名 | 类型 | 必选 | 说明 |
| --- | --- | --- | --- |
| ResourceID | string | 二选一 | 资源 ID。与 `collection_name` 二选一，用于定位集合。 |
| CollectionName | string |  | 集合名称。若通过名称访问索引，可配合 `project_name` 使用。 |
| ProjectName | string | 否 | 项目名称。与 `collection_name` 组合使用时可进一步限定作用域。 |
| IndexName | string | 是 | 索引名称。 |
| Filter | map[string]interface{} | 否 | 向量检索通用过滤条件，语法与搜索接口一致，未指定时不过滤。 |
| Partition | string | 否 | 指定要聚合的分区名称。 |
| Op | string | 是 | 聚合算子，当前仅支持 `count`。 |
| Field | string | 否 | 需要分组聚合的标量字段。支持 string、int64 或 bool 类型且需建立索引。 |
| Cond | map[string]interface{} | 否 | 聚合后的二次过滤条件，类似 SQL `HAVING`。目前 count 仅支持 `gt` 比较语法。 |
| Order | string | 否 | 聚合结果排序方向，例如 `desc`。 |
## 返回参数
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| Request_id | string | 请求链路 ID，可用于排查。 |
| Code | string | 错误码，成功时为空。 |
| Message | string | 错误信息。 |
| Api | string | 实际调用的 API 名称。 |
| Result | AggResult | 聚合结果，失败或无结果时可能为 `None`。 |
AggResult 结构
| 字段 | 类型 | 说明 |
| --- | --- | --- |
| Agg | map[string]interface{} | 聚合结果字典。按字段值返回计数，若不指定 `field`，则包含 `_total`。 |
| Op | string | 聚合算子名称。 |
| Field | string | 参与聚合的字段名。 |
# 示例
```go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "github.com/volcengine/vikingdb-go-sdk/vector"
    "github.com/volcengine/vikingdb-go-sdk/vector/model"
    "os"
    "time"
)

func main() {
    var (
       accessKey = os.Getenv("VIKINGDB_AK")
       secretKey = os.Getenv("VIKINGDB_SK")
       endpoint  = "https://api-vikingdb.vikingdb.cn-beijing.volces.com"
       region    = "cn-beijing"
    )

    client, err := vector.New(
       vector.AuthIAM(accessKey, secretKey), // IAM auth
       vector.WithEndpoint(endpoint),
       vector.WithRegion(region),
       vector.WithTimeout(time.Second*30),
       vector.WithMaxRetries(3),
    )
    if err != nil {
       fmt.Println("New client failed, err: ", err)
       panic(err)
    }
    ctx := context.Background()

    var (
       field = "type"
    )

    // SELECT category, COUNT(*) FROM index WHERE score >= 0.3 AND score <= 0.46 GROUP BY category HAVING COUNT(*) > 4
    resp, err := client.Index(model.IndexLocator{
       CollectionLocator: model.CollectionLocator{
          CollectionName: "Your Collection Name",
       },
       IndexName: "Your Index Name",
    }).Aggregate(ctx, model.AggRequest{
       RecallBase: model.RecallBase{
          Filter: map[string]any{
             "op": "range", "field": "score", "gte": 0.3, "lte": 0.46,
          },
       },
       Op:    "count",
       Field: &field,
       Cond:  map[string]any{"gt": 4},
    })

    if err != nil {
       fmt.Println("Aggregate failed, err: ", err)
       panic(err)
    }

    jsonData, err := json.Marshal(resp.Result)
    if err != nil {
       fmt.Println("Marshal result failed, err: ", err)
       panic(err)
    }
    fmt.Println(string(jsonData))
}
```


