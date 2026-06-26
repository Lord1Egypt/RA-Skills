# 概述
searchWithMultiModal 用于多模态数据检索。多模态数据检索是指向量数据库支持直接通过图文等多模态数据类型进行检索，且支持模态的组合，如文搜图，图搜图，图搜文+图等。
* 当前支持文本、图片、视频类型的非结构化数据。
* Collection 数据写入/删除后，Index 数据更新时间预计20s，不能立即在 Index 检索到。

# 前提条件

* 从控制台选择了从向量化开始的数据库类型，并在创建数据集时配置了向量化字段；或通过 create_collection 接口创建数据集时，通过设置 vectorize 参数配置了 Collection 的向量化功能。
* 通过 upsert_data 接口写入数据时，已写入 text或image 类型的字段名称和字段值。
* 通过 create_index 创建索引时，已创建 vector_index 向量索引。

适用于创建向量库时选择"需要向量化" ：当导入的数据是原始数据时，可以通过此接口输入文本、图片等进行检索。

# 方法定义
```Java
    public DataApiResponse<SearchResult> searchByMultiModal(SearchByMultiModalRequest request, RequestAddition addition)
            throws ApiClientException, VectorApiException
```

# **请求参数**
请求参数是 SearchWithMultiModalParam，SearchWithMultiModalParam 实例包含的参数如下表所示。
| **参数** | **类型** | **是否必选** | **说明** |
| --- | --- | --- | --- |
| text | string | 至少选1 | 检索的输入文本。 |
| image | Object |  | 检索的输入图片，当前支持2种方式： <br>  <br> * 图片tos链接。`tos://{bucket}/{object_key}`。 <br> * base64字符串。`base64://{Base64编码}`。 |
| video | Object |  | { <br> "value": tos链接，http/https格式链接 （该字段必填） <br> "fps": 2.0 (0.2-5，该字段选填) <br> } |
| filter | Map<String, Object> | 否 | 过滤条件，详见**标量过滤** <br>  <br> * 默认为空，不做过滤。 <br> * 过滤条件包含 must、must_not、range、range_out四类查询算子，包含 and 和 or 两种对查询算子的组合。 |
| outputFields | List<String> | 否 | 要返回的标量字段列表. <br>  <br> 1. 用户不传 output_fields 时, 返回所有标量字段 <br> 2. 用户传一个空列表不返回标量字段 <br> 3. output_fields格式错误或者过滤字段不是 collection 里的字段时, 接口返回错误 |
| limit | Integer | 否 | 检索结果数量，最大5000个。 |
| offset | Integer | 否 | 偏移量。仅分页场景下使用，不建议设置过大值，否则有深分页影响。默认值为0。设置值至少为0，语义和mysql的offset相同。 |
| advance | SearchAdvance | 否 | 高级参数，详见[检索公共参数](/c8p1dfoq/dhd9lm8y) |
| needInstruction | Boolean | 否 | 由模型默认值决定，豆包系列模型默认为true，其他模型默认为false |
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


public class SearchByMultiModal {

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

        SearchByMultiModalRequest request = SearchByMultiModalRequest.builder()
                .collectionName("your_collection_name") // 替换为您的集合名称
                .indexName("your_index_name") // 替换为您的索引名称
                .text("你好。")
                .limit(5) // 返回最相似的 5 个结果
                .build();

        try {
            DataApiResponse<SearchResult> response = vectorService.searchByMultiModal(request);
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
