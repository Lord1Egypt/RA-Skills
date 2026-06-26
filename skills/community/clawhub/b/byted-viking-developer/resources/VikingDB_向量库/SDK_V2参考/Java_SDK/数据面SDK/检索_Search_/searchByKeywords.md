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
| keywords | List<String> | 是 | string。关键词列表，列表元素1-10个，元素不允许为空字符串 |
| caseSensitive | Boolean | 否 | 是否大小写严格。默认false。 |
| filter | Map<String, Object> | 否 | 过滤条件，详见**标量过滤** <br>  <br> * 默认为空，不做过滤。 <br> * 过滤条件包含 must、must_not、range、range_out四类查询算子，包含 and 和 or 两种对查询算子的组合。 |
| outputFields | List<String> | 否 | 要返回的标量字段列表. <br>  <br> 1. 用户不传 output_fields 时, 返回所有标量字段 <br> 2. 用户传一个空列表不返回标量字段 <br> 3. output_fields格式错误或者过滤字段不是 collection 里的字段时, 接口返回错误 |
| limit | Integer | 否 | 检索结果数量，最大5000个。 |
| offset | Integer | 否 | 偏移量。仅分页场景下使用，不建议设置过大值，否则有深分页影响。默认值为0。设置值至少为0，语义和mysql的offset相同。 |
| advance | SearchAdvance | 否 | 高级参数，详见[检索公共参数](/c8p1dfoq/dhd9lm8y) |
# 返回参数
| **属性** | 类型 | **说明** |
| --- | --- | --- |
| data | List<SearchItem> | 见下 |
| filterMatchedCount | Integer | 筛选匹配数量 |
| totalReturnCount | Integer | 返回数量 |
| realTextQuery | String |  |
| tokenUsage | Object | 使用token |

* List<SearchItem>

| **属性** | 类型 | **说明** |
| --- | --- | --- |
| id | Object  | 主键 id。 |
| fields | Map<String, Object>  | 请求返回中的 fields 字段 |
| score | Float | 相似度 |
| annScore | Float | ann得分 |

# 示例
## 请求参数

```Java
package org.example.newsubproduct.data.search;


import com.volcengine.vikingdb.runtime.core.ClientConfig;
import com.volcengine.vikingdb.runtime.core.auth.AuthWithAkSk;
import com.volcengine.vikingdb.runtime.enums.Scheme;
import com.volcengine.vikingdb.runtime.exception.VectorApiException;
import com.volcengine.vikingdb.runtime.vector.model.request.*;
import com.volcengine.vikingdb.runtime.vector.model.response.*;
import com.volcengine.vikingdb.runtime.vector.service.VectorService;

import java.util.Arrays;

public class SearchByKeywords {

    public static void main(String[] args) {
        VectorService vectorService = null;
        try {
            vectorService = new VectorService(
                    Scheme.HTTPS,
                    "api-vikingdb.vikingdb.cn-beijing.volces.com", // 填写向量库数据面v2的域名  https://www.volcengine.com/docs/84313/1792715
                    "cn-beijing",
                    new AuthWithAkSk(System.getenv("AK"), System.getenv("SK")),
                    ClientConfig.builder().build()
            );
        } catch (Exception e) {
            System.err.println("Client initialization failed: " + e.getMessage());
            e.printStackTrace();
            return;
        }

        SearchByKeywordsRequest request = SearchByKeywordsRequest.builder()
                .collectionName("your_collection_name") // 替换为您的集合名称
                .indexName("your_index_name") // 替换为您的索引名称
                .keywords(Arrays.asList("keyword1", "keyword2"))
                .limit(10)
                .build();

        try {
            DataApiResponse<SearchResult> response = vectorService.searchByKeywords(request);
            System.out.println("request success:");
            System.out.println(response);
        } catch (VectorApiException vectorApiException) {
            System.err.println("request vectorApiException:");
            System.out.println("apiName: " + vectorApiException.getApiName());
            System.out.println("httpStatusCode: " + vectorApiException.getHttpStatusCode());
            System.out.println("code: " + vectorApiException.getCode());
            System.out.println("message: " + vectorApiException.getMessage());
            System.out.println("requestId: " + vectorApiException.getRequestId());
            System.out.println("responseContext: " + vectorApiException.getResponseContext().getBody());
        } catch (Exception e) {
            System.err.println("request exception, message : " + e.getMessage());
            e.printStackTrace();
        }
    }


}

```

## 
