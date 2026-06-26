# 概述
按特定条件批量更新数据，不支持vector、sparse_vector、text 类型字段的更新
# 方法定义
```Java
public CreateVikingdbTaskResponse createVikingdbTask(CreateVikingdbTaskRequest body) throws ApiException
```

# 请求参数
| 参数 | 子参数 | 类型 | 是否必填 | 描述 |
| --- | --- | --- | --- | --- |
| projectName |  | String | 否 | 项目名称 |
| collectionName |  | String | 2选1 | 数据集名称 |
| resourceId |  | String |  | 数据集资源ID。请求必须指定ResourceId和CollectionName其中之一。 |
| **taskType** |  | String | 是 | filter_update |
| taskConfig |  | TaskConfigForCreateVikingdbTaskInput | 是 | 任务具体配置 |
|  | filterConds | List<Object> | 是 | 过滤条件。使用参考https://www.volcengine.com/docs/84313/1791133 <br>  |
|  | updateFields | Object | 是 | 需要更新的字段值，必须是标量字段，不支持vector、sparse_vector、text 类型字段的更新 |
# 返回参数
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| taskId | String | 任务ID |
| message | String | 操作结果信息 |
# 示例
## 请求参数
```Java
package org.example.newsubproduct.console.task;

import com.volcengine.ApiClient;
import com.volcengine.ApiException;
import com.volcengine.sign.Credentials;
import com.volcengine.vikingdb.VikingdbApi;
import com.volcengine.vikingdb.model.*;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class CreateVikingdbTaskFilterUpdate {
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

        Map<String, Object> filter = new HashMap<>();
        filter.put("op", "must");
        filter.put("field", "city");
        filter.put("conds", Collections.singletonList("beijing"));
        Map<String, Object> updateData = new HashMap<>();
        updateData.put("city", "shanghai");

        CreateVikingdbTaskRequest request = new CreateVikingdbTaskRequest()
                .collectionName("test_collection_for_sdk_with_vector")
                .taskType(CreateVikingdbTaskRequest.TaskTypeEnum.FILTER_UPDATE)
                .taskConfig(
                        new TaskConfigForCreateVikingdbTaskInput()
                                .filterConds(Collections.singletonList(filter))
                                .updateFields(updateData)
                );

        try {
            CreateVikingdbTaskResponse response = api.createVikingdbTask(request);
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
