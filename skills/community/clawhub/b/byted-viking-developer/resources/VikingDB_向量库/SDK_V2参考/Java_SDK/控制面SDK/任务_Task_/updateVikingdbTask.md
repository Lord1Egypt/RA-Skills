# 概述
更新指定的任务，当前任务更新只用于**删除**任务的人工确认 环节
# 方法定义
```Java
public UpdateVikingdbTaskResponse updateVikingdbTask(UpdateVikingdbTaskRequest body) throws ApiException 
```

# 请求参数
| 字段名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| taskId | String | 是 | 任务ID，在创建任务时返回 |
| taskStatus <br>  | String <br>  | 只有 confirm 状态可以更新，只能更新为 confirmed，必填 |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |
# 返回参数
| 参数 | 类型 | 示例值 | 描述 |
| --- | --- | --- | --- |
| message | String | success | 操作结果信息 |
# 示例

```Java
package org.example.newsubproduct.console.task;

import com.volcengine.ApiClient;
import com.volcengine.ApiException;
import com.volcengine.sign.Credentials;
import com.volcengine.vikingdb.VikingdbApi;
import com.volcengine.vikingdb.model.*;

public class UpdateVikingdbTask {
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

        UpdateVikingdbTaskRequest request = new UpdateVikingdbTaskRequest()
                .taskId("ff39477b-a7f4-5f63-abd5-1592aaf6dc0c")
                .taskStatus(UpdateVikingdbTaskRequest.TaskStatusEnum.CONFIRMED);

        try {
            UpdateVikingdbTaskResponse response = api.updateVikingdbTask(request);
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
