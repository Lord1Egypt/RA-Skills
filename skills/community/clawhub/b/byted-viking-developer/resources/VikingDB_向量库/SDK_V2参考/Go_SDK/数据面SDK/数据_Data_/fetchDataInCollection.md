# 概述
根据主键在指定的 Collection 中查询单条或多条数据，单次最多可查询100条数据。
Collection 数据写入/删除后，可以实时查询数据。
# **请求参数**
| 参数名 | 类型 | 必选 | 备注 |
| --- | --- | --- | --- |
| CollectionName | string | 2选1 | Collection 名称，与 resource_id 二选一。 |
| ResourceID | string |  | Collection 资源 ID。 |
| IDs | []interface{} | 是 | * 要查询的主键列表，最多100条。 |
# 返回参数
响应体包含公共参数（见下方“响应体公共参数介绍”）。其中 `result` 字段类型为 FetchDataInCollectionResult：

* FetchDataInCollectionResult

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| Items | []DataItem | 命中的数据列表，结构见下。 |
| NotFoundIDs | []string | 未命中的主键列表。 |

* DataItem

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| ID | interface{} | 数据的主键。 |
| Fields | map[string]interface{} | 全部标量字段，key 为字段名。 |
## 响应体公共参数介绍
| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| RequestID | string | 请求 ID。 |
| Code | string | 操作状态码。成功为`Success`，否则为错误码短语。 |
| Message | string | 执行信息。成功则为 `The API call was executed successfully.`。 |
| Result | map[string]interface{} | 操作结果。若无需返回数据，则 `result = null`。 |
# 示例
## 请求参数
```python
package main

import (
    "context"
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

    resp, err := client.Collection(model.CollectionLocator{
       CollectionName: "Your Collection Name",
    }).Fetch(ctx, model.FetchDataInCollectionRequest{
       IDs: []interface{}{1},
    })
    if err != nil {
       fmt.Println("Fetch failed, err: ", err)
       panic(err)
    }

    fmt.Println(resp.Message)
}
```


