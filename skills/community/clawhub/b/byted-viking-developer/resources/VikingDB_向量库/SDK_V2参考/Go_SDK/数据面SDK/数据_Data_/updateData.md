# 概述
updateData 用于为已存在数据的部分字段进行更新。支持 text、标量字段、vector 字段的更新。

# **请求参数**
| 名称 | 类型 | 描述 | 必选 |
| --- | --- | --- | --- |
| CollectionName | string | Collection 的名称，与 resource_id 二选一。 | 二选一 |
| ResourceID | string | Collection 的资源 ID。 |  |
| Data | []map[string]any{} | 要更新的数据列表，单次最多100条，需包含主键字段及待修改字段。 | 是 |
| TTL | int | 更新后新的生存时间，单位为秒。 | 否 |
| Async | bool | 异步写入开关。默认false。以异步写入的方式可以提高10倍QPS，但增大数据进入索引的延迟，适合大批量离线灌库。 |  |
# 返回参数
响应体包含公共参数（见下方“响应体公共参数介绍”）。其中 `result` 字段类型为 UpsertDataResult：

* UpsertDataResult

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| TokenUsage | map[string]interface{} | 本次写入涉及的 token 消耗，字段与计量策略相关。 |
## 响应体公共参数介绍
| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| RequestID | string | 请求 ID。 |
| Code | string | 操作状态码。成功为`Success`，否则为错误码短语。 |
| Message | string | 执行信息。成功则为 `The API call was executed successfully.`，否则为错误信息。 |
| Result | map[string]interface{} | 操作结果。若无需返回数据，则 `result = null`。 |
# 
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
    }).Update(ctx, model.UpdateDataRequest{
       WriteDataBase: model.WriteDataBase{
          Data: []model.MapStr{
             {
                "id":      1,
                "type":    "type1",
                "name":    "vikingdb data",
                "content": "vikingdb is a vector database...",
             },
          },
       },
    })
    if err != nil {
       fmt.Println("Update failed, err: ", err)
       panic(err)
    }

    fmt.Println(resp.Message)
}
```

