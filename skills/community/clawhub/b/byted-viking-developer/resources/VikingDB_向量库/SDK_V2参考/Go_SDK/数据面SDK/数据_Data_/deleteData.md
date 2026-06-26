# 概述
deleteData 用于在指定的 Collection 删除数据，根据主键删除单条或多条数据，单次最多允许删除100条数据。

# **请求参数**
| 参数名 | 类型 | 必选 | 备注 |
| --- | --- | --- | --- |
| ResourceId | string | 2选1 | 资源id |
| collectionName | String <br>  |  | collection名称 |
| IDs | []interface{} | 2选1 | 删除数据的主键列表（主键为int64或string）。最多100条。 <br> 注意： <br>  <br> * 若为请求参数非法（4xx类型），则会全部失败。 |
|  |  |  |  |
| DelAll <br>  | bool |  | 为true时，删除所有数据；默认为false。 <br> 此接口删除所有数据，并不能立刻同步到索引，因此，在一段时间内（5分钟左右），索引内仍可检索到数据 |
# 返回参数
本接口仅返回公共参数，`result` 恒为 `null`（详见下方“响应体公共参数介绍”）。
## 响应体公共参数介绍
| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| RequestID | string | 请求 ID。 |
| Code | string | 操作状态码。成功为`Success`，否则为错误码短语。 |
| Message | string | 执行信息。成功则为 `The API call was executed successfully.`。 |
| Result | map[string]interface{} | 操作结果。若无需返回数据，则 `result = null`。 |
# 

# 示例
## 请求参数

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
    }).Delete(ctx, model.DeleteDataRequest{
       IDs: []interface{}{1},
    })
    if err != nil {
       fmt.Println("Delete failed, err: ", err)
       panic(err)
    }

    fmt.Println(resp.Message)
}
```


## 
