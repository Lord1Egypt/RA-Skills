# 概述
接口用于在指定的数据集 Collection 内写入数据。指定写入的数据是一个map，允许单次插入一条数据或者多条数据，单次最多可插入100条数据。如提供的主键已存在，则更新对应的数据；否则，插入新的数据。
# 请求体参数
| 名称 | 类型 | 描述 | 必选 |
| --- | --- | --- | --- |
| CollectionName | string | 数据集的名称。 | 二选一 |
| ResourceID | string | 数据集的Id。 |  |
| Data | []map[string]any{} | 要更新的数据列表。列表中的每个 Map 代表一条数据，必须包含主键字段。 | 是 |
| TTL | int32 | 数据的生存时间（Time-To-Live），单位为秒。超过该时间后数据将被自动删除。 | 否 |
| Async | bool | 异步写入开关。默认false。以异步写入的方式可以提高10倍QPS，但增大数据进入索引的延迟，适合大批量离线灌库。 | 否 |
# data参数字段值格式
注意：数据插入时主键不能为0

| 字段类型 | 格式 | 说明 |
| --- | --- | --- |
| int64 | 整型数值 | 整数 |
| float32 | 浮点数值 | 浮点数 |
| string | 字符串 | 字符串。内容限制256byte |
| bool | true/false | 布尔类型 |
| list<string> | 字符串数组 | 字符串数组 |
| list<int64> | 整型数组 | 整数数组 |
| vector | * 向量（浮点数数组） <br> * float32/float64压缩为bytes后的base64编码 | 稠密向量 <br>  |
| sparse_vector <br>  |  输入格式<token_id ,token_weight>的字典列表，来表征稀疏稀疏向量的非零位下标及其对应的值, 其中 token_id 是 string 类型, token_weight 是float 类型 | 稀疏向量 <br>  |
| text | string | 若为向量化字段，则值不能为空。（若否，可以为空） |
| image | interface{} | 若为向量化字段，则值不能为空。（若否，可以为空） <br>  <br> * 图片tos链接 `tos://{bucket}/{object}` <br> * http/https格式链接 |
| video | interface{} | { <br> "value": `tos://{bucket}/{object}`，http/https格式url链接，该字段必填 <br> "fps": 0.2 （取值0.2-5，选填） <br> } |
| dateTime | string | 分钟级别： <br> `yyyy-MM-ddTHH:mmZ`或`yyyy-MM-ddTHH:mm±HH:mm` <br> 秒级别： <br> `yyyy-MM-ddTHH:mm:ssZ`或`yyyy-MM-ddTHH:mm:ss±HH:mm` <br> 毫秒级别： <br> `yyyy-MM-ddTHH:mm:ss.SSSZ`或`yyyy-MM-ddTHH:mm:ss.SSS±HH:mm` <br> 例如："2025-08-12T11:33:56+08:00" |
| geoPoint | string | 地理坐标`longitude,latitude`，其中`longitude`取值(-180,180)，`latitude`取值(-90,90) <br> 例如："116.408108,39.915023" |
## 创建时间类型字段(date_time)
只能填写以下格式的其中一种，全部遵循RFC3339标准（https://datatracker.ietf.org/doc/html/rfc3339）
例如："2025-08-12T12:34:56+08:00"
|  | 格式(string) | 示例 | 说明 |
| --- | --- | --- | --- |
| 分钟级别 | `yyyy-MM-ddTHH:mmZ`（utc时间）或 <br> `yyyy-MM-ddTHH:mm±HH:mm`（指定时区） | * `2025-08-12T04:34Z` <br> * `2025-08-12T12:34+08:00` <br>  <br>  | 左侧示例都会解析为北京时间`2025-08-12`的`12:34:00`。 <br>  |
| 秒级别 | `yyyy-MM-ddTHH:mm:ssZ`（utc时间）或 <br> `yyyy-MM-ddTHH:mm:ss±HH:mm`（指定时区） <br>  | * `2025-08-12T04:34:56Z` <br> * `2025-08-12T12:34:56+08:00` <br>  <br>  | 左侧示例都会解析为北京时间`2025-08-12`的`12:34:56`。 <br>  <br>  |
| 毫秒级别 | `yyyy-MM-ddTHH:mm:ss.SSSZ`（utc时间）或 <br> `yyyy-MM-ddTHH:mm:ss.SSS±HH:mm`（带时区） | * `2025-08-12T04:34:56.147Z` <br> * `2025-08-12T12:34:56.147+08:00` <br>  <br>  <br>  | 左侧示例都会解析为北京时间`2025-08-12`的`12:34:56.147`秒。 <br>  |
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
# **请求示例代码**
```Go
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
    }).Upsert(ctx, model.UpsertDataRequest{
       WriteDataBase: model.WriteDataBase{
          Data: []model.MapStr{
             {
                "id":      1,
                "type":    "type1",
                "name":    "vikingdb data",
                "content": "vikingdb is a vector database",
             },
          },
       },
    })
    if err != nil {
       fmt.Println("Upsert failed, err: ", err)
       panic(err)
    }

    fmt.Println(resp.Message)
}
```


