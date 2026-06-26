# 概述
searchByVector 用于向量检索。根据查询的向量，搜索与其距离最近的 limit 个向量。
* Collection 数据写入/删除后，Index 数据更新时间预计 20s，不能立即在 Index 检索到。
* 当请求参数 filter 配置时，表示混合检索；当请求参数 filter 没有配置时，表示纯向量检索。

# 前提条件

* 通过 CreateVikingdbCollection 接口创建数据集时，定义字段 fields 已添加 vector 字段。
* 通过 UpsertData 接口写入数据时，已写入 vector 类型的字段名称和字段值。
* 通过 CreateVikingdbIndex 创建索引时，已创建 vector_index 向量索引。

适用于创建向量库时选择"已有向量数据" ：当导入的数据是向量时，可以通过此接口输入向量进行检索。

# **请求参数**
请求参数是 `SearchByVectorRequest`，其字段如下表所示。
| **名称** | **类型** | **必选** | **描述** |
| --- | --- | --- | --- |
| DenseVector | []float64 | 是 | 用于检索的稠密向量，长度需与索引维度一致。 |
| SparseVector | map[string]float64 | 否 | 稀疏向量表示（如 BOW），用于与 dense_vector 混合检索。 |
| Filter | map[string]interface{} | 否 | 标量过滤条件，详见**标量过滤** <br>  <br> * 不填表示纯向量检索。 <br> * 支持 must、must_not、range、range_out 等算子，可用 and / or 组合。 |
| OutputFields | []string | 否 | 要返回的标量字段列表。 <br>  <br> 1. 未设置时返回集合内所有标量字段。 <br> 2. 传入空列表表示不返回任何标量字段。 <br> 3. 字段名必须存在于 collection schema，否则请求报错。 |
| Limit | int | 否 | 限制返回条数，最大 5000。 |
| Offset | int | 否 | 分页偏移量，默认 0，过大时会出现深分页性能开销。 |
| Partition | string | 否 | 仅检索指定分区，默认搜索全部分区数据。 |
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
       limit       = 10
       denseVector = make([]float64, 0, 4096) // 4096 is the dimension of the vector
    )
    for i := 0; i < 4096; i++ {
       denseVector = append(denseVector, 0.5)
    }

    resp, err := client.Index(model.IndexLocator{
       CollectionLocator: model.CollectionLocator{
          CollectionName: "Your Collection Name",
       },
       IndexName: "Your Index Name",
    }).SearchByVector(ctx, model.SearchByVectorRequest{
       SearchBase: model.SearchBase{
          Limit: &limit,
       },
       DenseVector: denseVector,
    })

    if err != nil {
       fmt.Println("SearchByVector failed, err: ", err)
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


