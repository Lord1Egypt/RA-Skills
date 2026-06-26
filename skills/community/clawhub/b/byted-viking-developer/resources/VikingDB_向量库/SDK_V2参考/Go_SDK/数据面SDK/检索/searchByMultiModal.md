概述
searchByMultiModal用于多模态数据检索。多模态数据检索是指向量数据库支持直接通过图文等多模态数据类型进行检索，且支持模态的组合，如文搜图，图搜图，图搜文+图等。
* 当前支持文本、图片、视频类型的非结构化数据。
* Collection 数据写入/删除后，Index 数据更新时间预计20s，不能立即在 Index 检索到。

# 前提条件

* 从控制台选择了从向量化开始的数据库类型，并在创建数据集时配置了向量化字段；或通过 create_collection 接口创建数据集时，通过设置 vectorize 参数配置了 Collection 的向量化功能。
* 通过 upsert_data 接口写入数据时，已写入 text或image 类型的字段名称和字段值。
* 通过 create_index 创建索引时，已创建 vector_index 向量索引。

适用于创建向量库时选择"需要向量化" ：当导入的数据是原始数据时，可以通过此接口输入文本、图片等进行检索。

# **请求参数**
请求参数是 `SearchByMultiModalRequest`，其字段如下表所示。
| **名称** | **类型** | **必选** | **描述** |
| --- | --- | --- | --- |
| Text | str | 至少选 1 | 检索的输入文本。 |
| Image | interface{} |  | 检索的输入图片，支持： <br>  <br> * TOS 链接，形如 `tos://{bucket}/{object_key}`。 <br> * Base64 编码，形如 `base64://{Base64编码}`。 |
| Video | interface{} |  | JSON 结构，如： <br> { <br> "value": http/https/TOS 链接（必填） <br> "fps": 2.0 （0.2-5，可选） <br> } |
| Filter | map[string]interface{} | 否 | 标量过滤条件，详见**标量过滤**。 <br>  <br> * 不填表示纯多模态检索。 <br> * 支持 must、must_not、range、range_out 等算子，可用 and / or 组合。 |
| OutputFields | []string | 否 | 要返回的标量字段列表。 <br>  <br> 1. 未设置时返回集合内所有标量字段。 <br> 2. 传入空列表表示不返回任何标量字段。 <br> 3. 字段名必须存在于 collection schema，否则请求报错。 |
| Limit | int | 否 | 限制返回条数，最大 5000。 |
| Offset | int | 否 | 分页偏移量，默认 0，过大时会出现深分页性能开销。 |
| Partition | string | 否 | 指定检索的分区名称。 |
| Advance | SearchAdvance | 否 | 高级参数集合（post_process_ops、ids_in 等），详见[检索公共参数](/c8p1dfoq/dhd9lm8y) <br> 。 |
| NeedInstruction | bool | 否 | 控制是否让模型自动补全 instruction，豆包系列默认 True，其他模型默认 False。 |
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

## 请求参数
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
       text            = "viking"
       needInstruction = true // need instruction improves prompt
       limit           = 10
    )

    resp, err := client.Index(model.IndexLocator{
       CollectionLocator: model.CollectionLocator{
          CollectionName: "Your Collection Name",
       },
       IndexName: "Your Index Name",
    }).SearchByMultiModal(ctx, model.SearchByMultiModalRequest{
       Text:            &text,
       NeedInstruction: &needInstruction,
       SearchBase: model.SearchBase{
          Limit: &limit,
       },
    })

    if err != nil {
       fmt.Println("SearchByMultiModal failed, err: ", err)
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


