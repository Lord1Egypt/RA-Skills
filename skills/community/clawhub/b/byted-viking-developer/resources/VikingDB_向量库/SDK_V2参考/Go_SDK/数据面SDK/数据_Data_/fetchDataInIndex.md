# 概述
fetchData 用于 Index 数据查询。根据主键 id，在指定的 Index 查询单条或多条数据，单次最多可查询100条数据。
Collection 数据写入/删除后，Index 数据更新时间有同步延迟，一般在10s左右，不能立即在 Index 查询到。


# **请求参数**
| 参数名 | 类型 | 必选 | 备注 |
| --- | --- | --- | --- |
| CollectionName | string | 2选1 | Collection 名称，与 resource_id 二选一。 |
| ResourceID | string |  | Collection 资源 ID。 |
| IndexName | string | 是 | 索引名称。 |
| IDs | []interface{} | 是 | 点查的主键列表，最多100条。 |
| Partition | string | 否 | 按分区过滤索引数据。 |
| OutputFields | []string | 否 | 控制返回的标量字段： <br>  <br> 1. 未传时返回全部标量字段。 <br> 2. 传空列表则仅返回向量与 id。 <br> 3. 字段不存在或格式错误会直接报错。 |
# 返回参数
响应体包含公共参数（见下方“响应体公共参数介绍”）。其中 `result` 字段类型为 FetchDataInIndexResult：

* FetchDataInIndexResult

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| Items | []IndexDataItem | 命中的索引数据。 |
| IDsNotExist | []interface{} | 未命中的主键。 |

* IndexDataItem

| 名称 | 类型 | 说明 |
| --- | --- | --- |
| ID | interface{} | 数据主键。 |
| Fields | map[string]interface{} | 标量字段。 |
| DenseVector | []float64 | 落盘的稠密向量。 |
| DenseDim | int | 向量维度。 |
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

    resp, err := client.Index(model.IndexLocator{
       CollectionLocator: model.CollectionLocator{
          CollectionName: "Your Collection Name",
       },
       IndexName: "Your Index Name",
    }).Fetch(ctx, model.FetchDataInIndexRequest{
       IDs: []interface{}{ 1 },
    })
    if err != nil {
       fmt.Println("Fetch failed, err: ", err)
       panic(err)
    }

    fmt.Println(resp.Message)
}
```

