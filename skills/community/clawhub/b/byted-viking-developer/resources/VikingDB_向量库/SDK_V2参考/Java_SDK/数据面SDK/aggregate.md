# 概述
聚合统计能指定字段进行分组聚合，并可添加过滤操作，最终得到相应的聚合统计结果，辅助了解数据分布等情况。
索引需要包含至少一个枚举类型（string、int64或bool类型）的标量索引字段。


# 方法定义
```Java
    public DataApiResponse<AggregateResult> aggregate(AggregateRequest request)
            throws ApiClientException, VectorApiException
```

# 请求体参数
| 参数名 | 类型 | 必选 | 备注 |
| --- | --- | --- | --- |
| resourceId | String | 2选1 | 资源id |
| collectionName | String |  | collection名称 |
| indexName | String | 是 | 索引名称 |
| filter | Map<String, Object> | 否 | 过滤条件，格式见下文。默认为空，不做过滤 |
| op | string <br>  | 是 | 目前仅支持count。使用count算子时，索引中必须至少存在一个string、int64或bool类型的标量索引字段。 <br>  |
| field | string | 否 | 对指定字段名进行聚合。字段类型支持string，int64，bool且必须为标量索引字段。 |
| cond <br>  | Map<String, Object> <br>  | 否 | 类似SQL里group by的having 子句。仅当field字段存在时，才生效。对于count算子，支持gt，表示仅返回大于阈值的结果项。 |
## 返回参数
Java调用执行上面的任务，返回 List\<Data> 。Data 实例包含的属性如下表所示。
| **属性** |  | **说明** |
| --- | --- | --- |
| agg | Map<String, Object> | 算子类型 |
| op | String |  |
| field | String | String |
# 示例
## 请求参数

```Java
package org.example.newsubproduct.data;

import com.volcengine.vikingdb.runtime.core.ClientConfig;
import com.volcengine.vikingdb.runtime.core.auth.AuthWithAkSk;
import com.volcengine.vikingdb.runtime.enums.Scheme;
import com.volcengine.vikingdb.runtime.exception.VectorApiException;
import com.volcengine.vikingdb.runtime.vector.model.request.*;
import com.volcengine.vikingdb.runtime.vector.model.response.*;
import com.volcengine.vikingdb.runtime.vector.service.VectorService;

public class Aggregate {

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

        AggregateRequest request = AggregateRequest.builder()
                .collectionName("your_collection_name") // 替换为您的集合名称
                .indexName("your_index_name") // 替换为您的索引名称
                .op("count")
                .field("id")
                .build();

        try {
            DataApiResponse<AggregateResult> response = vectorService.aggregate(request);
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
