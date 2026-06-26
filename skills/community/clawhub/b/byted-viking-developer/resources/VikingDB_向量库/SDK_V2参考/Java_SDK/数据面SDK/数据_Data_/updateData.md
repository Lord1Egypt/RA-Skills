# 概述
updateData 用于为已存在数据的部分字段进行更新。支持 text、标量字段、vector 字段的更新。

# 方法定义
```Java
    public DataApiResponse<UpdateDataResult> updateData(UpdateDataRequest request)
            throws ApiClientException, VectorApiException
```


# **请求参数**
| 名称 | 类型 | 描述 | 必选 |
| --- | --- | --- | --- |
| collectionName | String | 数据集的名称。 | 二选一 |
| resourceId | String | 数据集的Id。 |  |
| data | List<Map<String, Object>> | 要更新的数据列表。列表中的每个 Map 代表一条数据，必须包含主键字段。 | 是 |
| ttl | integer | 数据的生存时间（Time-To-Live），单位为秒。超过该时间后数据将被自动删除。 | 否 |

# 返回参数
| 名称 | 类型 | 描述 |
| --- | --- | --- |
| tokenUsage | Object | 本次请求的 token 使用情况。 |
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
import java.util.HashMap;

public class UpdateData {

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

        UpdateDataRequest request = UpdateDataRequest.builder()
                .collectionName("your_collection_name") // 替换为您的集合名称
                .data(Arrays.asList(
                        new HashMap<String, Object>() {{ put("id", 1); put("field1", "new_value1"); }},
                        new HashMap<String, Object>() {{ put("id", 2); put("field1", "new_value2"); }}
                ))
                .build();

        try {
            DataApiResponse<UpdateDataResult> response = vectorService.updateData(request);
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
