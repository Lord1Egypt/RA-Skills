# 概述
将 数据导入到 Collection 中，要求文件的列名必须和 Collection fields 重合，否则会解析失败
使用前请先授权 VikingDB 跨服务访问 TOS [去授权](https://console.volcengine.com/iam/service/attach_role/?ServiceName=vikingdb)
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
| **taskType** |  | String | 是 | data_import |
| taskConfig |  | TaskConfigForCreateVikingdbTaskInput | 是 | 任务具体配置 |
|  | FileType | String | 是 | 文件类型, json 或者 parquet，必填 |
|  | TosPath | String | 是 | TOS 路径，格式 ：{桶名}/{路径}，注意不是域名。必填 |
|  | IgnoreError | Boolean | 否 | 设置为 true 时遇到数据会继续解析文件，默认为 false |
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

public class CreateVikingdbTaskDataImport {
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

        CreateVikingdbTaskRequest request = new CreateVikingdbTaskRequest()
                .collectionName("test_collection_for_sdk_with_vector")
                .taskType(CreateVikingdbTaskRequest.TaskTypeEnum.DATA_IMPORT)
                .taskConfig(
                        new TaskConfigForCreateVikingdbTaskInput()
                                .fileType(TaskConfigForCreateVikingdbTaskInput.FileTypeEnum.JSON)
                                .tosPath("test-doc1-tos/pic_search_1000_images.json")
                                .ignoreError(true)
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



