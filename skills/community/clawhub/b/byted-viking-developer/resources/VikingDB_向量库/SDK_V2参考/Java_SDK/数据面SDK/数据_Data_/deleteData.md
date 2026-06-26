# 概述
deleteData 用于在指定的 Collection 删除数据，根据主键删除单条或多条数据，单次最多允许删除100条数据。

# 方法定义
```Java
    public DataApiResponse<DeleteDataResult> deleteData(DeleteDataRequest request)
            throws ApiClientException, VectorApiException
```


# **请求参数**
| 参数名 | 类型 | 必选 | 备注 |
| --- | --- | --- | --- |
| resourceId | String | 2选1 | 资源id |
| collectionName | String <br>  |  | collection名称 |
| ids | List<Object> | 2选1 | 删除数据的主键列表（主键为int64或string）。最多100条。 <br> 注意： <br>  <br> * 若为请求参数非法（4xx类型），则会全部失败。 |
|  |  |  |  |
| delAll <br>  | Boolean  |  | 为true时，删除所有数据；默认为false。 <br> 此接口删除所有数据，并不能立刻同步到索引，因此，在一段时间内（5分钟左右），索引内仍可检索到数据 |
# 返回参数
Java 调用执行上面的任务，执行成功无返回信息。

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


public class DeleteData {

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

        DeleteDataRequest request = DeleteDataRequest.builder()
                .collectionName("your_collection_name") // 替换为您的集合名称
                .ids(Arrays.asList(1, 2, 3))
                .build();

        try {
            DataApiResponse<DeleteDataResult> response = vectorService.deleteData(request);
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
