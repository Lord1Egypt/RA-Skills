# 概述
searchById 用于主键 id 检索。根据主键 id，搜索与其距离最近的 limit 个向量。
* 对于使用了 hnsw-hybrid 算法的混合索引，暂时不支持基于 id 进行检索。
* Collection 数据写入/删除后，Index 数据更新时间预计20s，不能立即在 Index 检索到。
* 当请求参数 filter 配置时，表示混合检索；当请求参数 filter 没有配置时，表示纯向量检索。

# 前提条件

* 通过 createCollection 接口创建数据集时，定义字段 fields 已添加 vector 字段。
* 通过 upsertData 接口写入数据时，已写入 vector 类型的字段名称和字段值。
* 通过 createIndex 接口创建索引时，已创建 vectorIndex 向量索引。


# **请求参数**
| **参数** | **类型** | **是否必选** | **参数说明** |
| --- | --- | --- | --- |
| ID | interface{} | 是 | 主键 id。 |
| Filter | map[string]interface{} | 否 | 过滤条件，详见**标量过滤** <br>  <br> * 默认为空，不做过滤。 <br> * 过滤条件包含 must、must_not、range、range_out四类查询算子，包含 and 和 or 两种对查询算子的组合。 |
| OutputFields | []string | 否 | 要返回的标量字段列表. <br>  <br> 1. 用户不传 output_fields 时, 返回所有标量字段 <br> 2. 用户传一个空列表不返回标量字段 <br> 3. output_fields格式错误或者过滤字段不是 collection 里的字段时, 接口返回错误 |
| Limit | int | 否 | 检索结果数量，最大5000个。 |
| Offset | Int | 否 | 偏移量。仅分页场景下使用，不建议设置过大值，否则有深分页影响。默认值为0。设置值至少为0，语义和mysql的offset相同。 |
| Advance | SearchAdvance | 否 | 高级参数，详见[检索公共参数](/c8p1dfoq/dhd9lm8y) |
# 返回参数
| **属性** | 类型 | **说明** |
| --- | --- | --- |
| Data | []SearchItem | 见下 |
| FilterMatchedCount | Int | 筛选匹配数量 |
| TotalReturnCount | Int | 返回数量 |
| RealTextQuery | string |  |
| TokenUsage | interface{} | 使用token |

* List<SearchItem>

| **属性** | 类型 | **说明** |
| --- | --- | --- |
| ID | interface{} | 主键 id。 |
| Fields | map[string]interface{} | 请求返回中的 fields 字段 |
| Score | float64 | 相似度 |
| AnnScore | float64 | ann得分 |

# 示例
## 请求参数

```Java
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

    resp, err := client.Index(model.IndexLocator{
       CollectionLocator: model.CollectionLocator{
          CollectionName: "Your Collection Name",
       },
       IndexName: "Your Index Name",
    }).SearchByID(ctx, model.SearchByIDRequest{
       ID: 1,
    })

    if err != nil {
       fmt.Println("SearchByID failed, err: ", err)
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

## 
