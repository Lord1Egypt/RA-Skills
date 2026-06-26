# 概述
接口适用于含有 int64/float32 类型标量索引字段的索引。向量数据库中的标量检索指的是基于标量值的检索方法。在向量数据库中，每个向量都有一个或多个标量值，标量检索可以基于这些标量值进行检索，找到与查询相关的数据。例如文档检索中的作者特征检索。
searchByScalar按标量字段进行排序/分页返回结果。
# 请求参数
请求参数是 `SearchByScalarRequest`，其字段如下表所示。
| **名称** | **类型** | **必选** | **描述** |
| --- | --- | --- | --- |
| Field | string | 是 | 排序使用的标量字段，需为 int64/float32 且已建立标量索引。 |
| Order | string | 否 | 排序方向，取值 `asc`/`desc`，默认 `desc`。 |
| Filter | map[string]interface{} | 否 | 标量过滤条件，详见**标量过滤**。 <br>  <br> * 不填表示对全量索引进行排序。 <br> * 支持 must、must_not、range、range_out 等算子，可用 and / or 组合。 |
| OutputFields | []string | 否 | 要返回的标量字段列表。 <br>  <br> 1. 未设置时返回集合内所有标量字段。 <br> 2. 传入空列表表示不返回任何标量字段。 <br> 3. 字段名必须存在于 collection schema，否则请求报错。 |
| Limit | int | 否 | 限制返回条数，最大 5000。 |
| Offset | int | 否 | 分页偏移量，默认 0，过大时会出现深分页性能开销。 |
| Partition | string | 否 | 仅检索指定分区，默认搜索全部分区。 |
| Advance | SearchAdvance | 否 | 高级参数集合（post_process_ops、ids_in 等），详见[检索公共参数](/c8p1dfoq/dhd9lm8y) <br> 。 |
# 返回参数
| 名称 | 类型 | 描述 |
| --- | --- | --- |
| RequestId | string | 请求链路 ID。 |
| Code | string | 服务返回码，Success 表示成功。 |
| Message | string | 错误或提示信息。 |
| Api | string | 具体调用的 API 名称。 |
| Result | SearchResult | 检索结果主体，结构见下。 |

* SearchResult

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| Data | []SearchItemResult | 召回到的结果列表，结构见下。 |
| FilterMatchedCount | int | 满足过滤条件的文档总数。 |
| TotalReturnCount | int | 本次返回的结果数量。 |
| RealTextQuery | string | 模型可能修正后的真实查询串。 |
| TokenUsage | map[string]interface{} | token 计量信息。 |

* SearchItemResult

| **属性** | 类型 | **说明** |
| --- | --- | --- |
| ID | interface{} | 主键 id。 |
| Fields | map[string]interface{} | 请求返回中的 fields 字段 |
| Score | float64 | 相似度 |
| AnnScore | float64 | ann得分 |
# 示例
```python
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
       // vector.AuthAPIKey(apiKey),            // APIKey auth
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
       limit = 10
       field = "score"
    )

    resp, err := client.Index(model.IndexLocator{
       CollectionLocator: model.CollectionLocator{
          CollectionName: "Your Collection Name",
       },
       IndexName: "Your Index Name",
    }).SearchByScalar(ctx, model.SearchByScalarRequest{
       SearchBase: model.SearchBase{
          Limit: &limit,
       },
       Field: &field,
       Order: model.ScalarOrderAsc,
    })

    if err != nil {
       fmt.Println("SearchByScalar failed, err: ", err)
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


