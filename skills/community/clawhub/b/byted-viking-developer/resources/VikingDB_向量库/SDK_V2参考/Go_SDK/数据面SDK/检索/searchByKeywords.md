# 概述
SearchByKeywords 用于关键词检索，适用于带有text字段向量化配置（vectorize参数）的索引，支持多个关键词的检索。
# 方法定义
```Java
    public DataApiResponse<SearchResult> searchByKeywords(SearchByKeywordsRequest request)
            throws ApiClientException, VectorApiException
```

# **请求参数**
请求参数是 SearchByIdParam，SearchByIdParam 实例包含的参数如下表所示。
| **参数** | **类型** | **是否必选** | **说明** |
| --- | --- | --- | --- |
| keywords | []string | 是 | string。关键词列表，列表元素1-10个，元素不允许为空字符串 |
| CaseSensitive | bool | 否 | 是否大小写严格。默认false。 |
| Filter | map[string]interface{} | 否 | 过滤条件，详见**标量过滤** <br>  <br> * 默认为空，不做过滤。 <br> * 过滤条件包含 must、must_not、range、range_out四类查询算子，包含 and 和 or 两种对查询算子的组合。 |
| OutputFields | []string | 否 | 要返回的标量字段列表. <br>  <br> 1. 用户不传 output_fields 时, 返回所有标量字段 <br> 2. 用户传一个空列表不返回标量字段 <br> 3. output_fields格式错误或者过滤字段不是 collection 里的字段时, 接口返回错误 |
| Limit | Int | 否 | 检索结果数量，最大5000个。 |
| Offset | Int | 否 | 偏移量。仅分页场景下使用，不建议设置过大值，否则有深分页影响。默认值为0。设置值至少为0，语义和mysql的offset相同。 |
| Advance | SearchAdvance | 否 | 高级参数，详见[检索公共参数](/c8p1dfoq/dhd9lm8y) |
# 返回参数

* SearchResult

| **属性** | 类型 | **说明** |
| --- | --- | --- |
| Data | []SearchItem | 见下 |
| FilterMatchedCount | Int | 筛选匹配数量 |
| TotalReturnCount | Int | 返回数量 |
| RealTextQuery | string |  |
| TokenUsage | interface{} | 使用token |

* SearchItemResult

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

    var (
       limit = 10
    )

    resp, err := client.Index(model.IndexLocator{
       CollectionLocator: model.CollectionLocator{
          CollectionName: "Your Collection Name",
       },
       IndexName: "Your Index Name",
    }).SearchByKeywords(ctx, model.SearchByKeywordsRequest{
       SearchBase: model.SearchBase{
          Limit: &limit,
       },
       Keywords:      []string{"viking"},
       CaseSensitive: false,
    })

    if err != nil {
       fmt.Println("SearchByKeywords failed, err: ", err)
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
