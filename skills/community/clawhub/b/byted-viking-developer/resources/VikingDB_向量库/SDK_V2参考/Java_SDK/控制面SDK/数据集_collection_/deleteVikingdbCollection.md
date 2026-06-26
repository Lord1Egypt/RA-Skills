# 概述
DeleteCollection 用于删除已创建的数据集 Collection。
* 执行 Collection 删除将会永久删除指定 Collection 下的所有数据，请谨慎操作。
* 在删除 Collection 之前，必须先删除 Collection 关联的所有 Index，才能成功删除 Collection。

# 方法定义
```Java
 public DeleteVikingdbCollectionResponse deleteVikingdbCollection(DeleteVikingdbCollectionRequest body) throws ApiException
```

# **请求参数**
| **参数** | **类型** | **是否必选** | **参数说明** |
| --- | --- | --- | --- |
| projectName | String | 否 | 项目名称 |
| collectionName | string | 2选1 | 指定要删除的 Collection 名称。 <br>  <br> * 只能使用英文字母、数字、下划线_，并以英文字母开头，不能为空。 <br> * 长度要求：[1, 128]。 <br> * Collection 名称不能重复。 |
| resourceId | String |  | 数据集资源ID。请求必须指定ResourceId和CollectionName其中之一。 |
# 返回参数
| 参数 | 类型 | 示例值 | 描述 |
| --- | --- | --- | --- |
| message | String | success | 操作结果信息 |
# 示例
## 请求参数
```Java
package org.example.newsubproduct.console.collection;

import com.volcengine.ApiClient;
import com.volcengine.ApiException;
import com.volcengine.sign.Credentials;
import com.volcengine.vikingdb.VikingdbApi;
import com.volcengine.vikingdb.model.*;

public class DeleteVikingdbCollection {
    public static void main(String[] args) {
        String ak = System.getenv("AK"); // ak
        String sk = System.getenv("SK"); // sk
        String endpoint = "vikingdb.cn-beijing.volcengineapi.com"; // 填写向量库控制面v2的域名  https://www.volcengine.com/docs/84313/1792715
        String region = "cn-beijing"; // 服务区域


        ApiClient apiClient = new ApiClient()
                .setEndpoint(endpoint)
                .setCredentials(Credentials.getCredentials(ak, sk))
                .setRegion(region);


        VikingdbApi api = new VikingdbApi(apiClient);


        DeleteVikingdbCollectionRequest request = new DeleteVikingdbCollectionRequest()
                .collectionName("test_collection_for_sdk_with_vector");

        try {
            DeleteVikingdbCollectionResponse response = api.deleteVikingdbCollection(request);
            System.out.println("response body: " + response);
            System.out.println();
            System.out.println("response meta RequestId: " + response.getResponseMetadata().getRequestId());
            System.out.println("response meta Service: " + response.getResponseMetadata().getService());
            System.out.println("response meta Region: " + response.getResponseMetadata().getRegion());
            System.out.println("response meta Action: " + response.getResponseMetadata().getAction());
            System.out.println("response meta Version: " + response.getResponseMetadata().getVersion());
        } catch (ApiException e) {
            System.out.println("exception http code: " + e.getCode());
            System.out.println("exception response body: " + e.getResponseBody());
            System.out.println();
            System.out.println("exception RequestId: " + e.getResponseMetadata().getRequestId());
            System.out.println("exception Action: " + e.getResponseMetadata().getAction());
            System.out.println("exception Region: " + e.getResponseMetadata().getRegion());
            System.out.println("exception Service: " + e.getResponseMetadata().getService());
            System.out.println("exception Error.Code: " + e.getResponseMetadata().getError().getCode());
            System.out.println("exception Error.Message: " + e.getResponseMetadata().getError().getMessage());
        }
    }
}
```

## 
