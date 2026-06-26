# 概述
fetchData 用于 Index 数据查询。根据主键 id，在指定的 Index 查询单条或多条数据，单次最多可查询100条数据。
Collection 数据写入/删除后，Index 数据更新时间有同步延迟，一般在10s左右，不能立即在 Index 查询到。


# 方法定义
```Java
    public DataApiResponse<FetchDataInIndexResult> fetchDataInIndex(FetchDataInIndexRequest request)
            throws ApiClientException, VectorApiException
```


# **请求参数**
| 参数名 | 类型 | 必选 | 备注 |
| --- | --- | --- | --- |
| resourceId | String | 2选1 | 资源id |
| collectionName | String <br>  |  | collection名称 |
| indexName | String | 是 | 索引名称 |
| ids | List<Object> | 是 | * 点查数据的主键列表。最多100条 |
|  |  |  |  |
| outputFields <br>  | List<String> | 否 <br>  | 要返回的标量字段列表. <br>  <br> 1. 用户不传 output_fields 时, 返回所有标量字段 <br> 2. 用户传一个空列表不返回标量字段 <br> 3. output_fields格式错误或者过滤字段不是 collection 里的字段时, 接口返回错误 |
# 返回参数
# 返回参数
| 名称 | 类型 | 说明 |
| --- | --- | --- |
| fetch | List<FetchInCollectionItem> | 查询到的数据列表，FetchResult结构见下。 |
| idsNotExist <br>  | List<Object> <br>  | 不存在的主键列表 |

* List<FetchInCollectionItem>

| 参数名 | 类型 | 备注 |
| --- | --- | --- |
| id | Object | 主键值 |
| fields | Map<String, Object> | key为字段名，value为字段值 |
| denseVector | List<Float> | 稠密向量 |
| denseDim | Integer | 稠密向量维度 |
# 示例
## 请求参数

```Java
package org.example.newsubproduct.data.data;

import com.volcengine.vikingdb.runtime.core.ClientConfig;
import com.volcengine.vikingdb.runtime.core.auth.AuthWithAkSk;
import com.volcengine.vikingdb.runtime.enums.Scheme;
import com.volcengine.vikingdb.runtime.exception.VectorApiException;
import com.volcengine.vikingdb.runtime.vector.model.request.*;
import com.volcengine.vikingdb.runtime.vector.model.response.*;
import com.volcengine.vikingdb.runtime.vector.service.VectorService;

import java.util.Arrays;

public class FetchDataInIndex {

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

        FetchDataInIndexRequest request = FetchDataInIndexRequest.builder()
                .collectionName("your_collection_name") // 替换为您的集合名称
                .indexName("your_index_name") // 替换为您的索引名称
                .ids(Arrays.asList(1, 2, 3))
                .build();

        try {
            DataApiResponse<FetchDataInIndexResult> response = vectorService.fetchDataInIndex(request);
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
