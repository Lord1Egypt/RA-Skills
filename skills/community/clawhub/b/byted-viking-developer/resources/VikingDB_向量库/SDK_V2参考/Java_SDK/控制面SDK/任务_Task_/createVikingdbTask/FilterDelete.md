# 概述
按特定条件批量删除Collection中的数据
# 方法定义
```Java
public CreateVikingdbTaskResponse createVikingdbTask(CreateVikingdbTaskRequest body) throws ApiException
```

# 请求参数
若要将数据备份至TOS，请先授权 VikingDB 跨服务访问 TOS [去授权](https://console.volcengine.com/iam/service/attach_role/?ServiceName=vikingdb)


| 参数 | 子参数 | 类型 | 是否必填 | 描述 |
| --- | --- | --- | --- | --- |
| ProjectName |  | String | 否 | 项目名称 |
| CollectionName |  | String | 2选1 | 数据集名称 |
| ResourceId |  | String |  | 数据集资源ID。请求必须指定ResourceId和CollectionName其中之一。 |
| **TaskType** |  | String | 是 | filter_delete |
| TaskConfig |  | TaskConfigForCreateVikingdbTaskInput | 是 | 任务具体配置 |
|  | FileType | String | 是 | 文件类型, json 或者 parquet，必填 |
|  | NeedConfirm | Boolean | 否 | 是否可跳过人工确认环节，默认为true |
|  | FilterConds | List<Object> | 是 | 过滤条件。使用参考https://www.volcengine.com/docs/84313/1791133 |
|  | TosPath | String | 是 | TOS 路径，格式 ：{桶名}/{路径}，注意不是域名。必填 |
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
import com.volcengine.vikingdb.model.CreateVikingdbTaskRequest;
import com.volcengine.vikingdb.model.CreateVikingdbTaskResponse;
import com.volcengine.vikingdb.model.TaskConfigForCreateVikingdbTaskInput;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;

public class CreateVikingdbTaskFilterDelete {
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

        CreateVikingdbTaskRequest request = new CreateVikingdbTaskRequest()
                .collectionName("test_collection_for_sdk_with_vector")
                .taskType(CreateVikingdbTaskRequest.TaskTypeEnum.FILTER_DELETE)
                .taskConfig(
                        new TaskConfigForCreateVikingdbTaskInput()
                                .filterConds(Collections.singletonList(filter))
                                .needConfirm(true)
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

## 返回参数
| 参数 | 类型 | 示例值 | 描述 |
| --- | --- | --- | --- |
| TaskId | String |  | 任务ID |
| Message | String | success | 操作结果信息 |

## 后续处理
如果需要人工确认，可执行**任务更新**操作
