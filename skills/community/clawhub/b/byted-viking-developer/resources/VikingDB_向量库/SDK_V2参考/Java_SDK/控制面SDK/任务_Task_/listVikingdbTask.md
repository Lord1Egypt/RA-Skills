# 概述
获取多个task的信息，最多一次性展示20条
# 方法定义
```Java
public ListVikingdbTaskResponse listVikingdbTask(ListVikingdbTaskRequest body) throws ApiException
```

# 请求参数
| 参数 | 类型 | 是否必填 | 描述 |
| --- | --- | --- | --- |
| projectName | String | 否 | 项目名称 |
| collectionName | String | 2选1 | 数据集名称 |
| resourceId | String |  | 数据集资源ID。请求必须指定ResourceId和CollectionName其中之一。 |
| taskStatus | String | 是 | 任务状态，见下 |
| taskType | String | 是 | 任务类型，见下 |
| pageNumber | Integer | 否 | 翻页页码。起始为1。 |
| pageSize | Integer | 否 | 翻页每页的大小。 |
# 返回参数
| 字段 | 类型 | 子字段说明 |
| --- | --- | --- |
| tasks <br>  | List<TaskForListVikingdbTaskOutput> | 任务ID |
| pageSize | Integer |  |
| pageNumber | Integer |  |
| totalCount | Integer |  |

* List<TaskForListVikingdbTaskOutput>

| **属性** |  | **类型** | **说明** |
| --- | --- | --- | --- |
| taskId |  | string | 任务ID |
| taskConfig |  | TaskConfigForListVikingdbTaskOutput |  |
|  | collectionName  | String |  |
|  | exportAll  | Boolean |  |
| taskType |  | string | 任务类型 |
| taskStatus |  | string | 任务状态 |
| updatePerson |  | string | 任务更新人 |
| updateTime |  | string | 任务信息更新时间 |
| createTime |  | string | 任务信息创建时间 |
| taskProcessInfo |  | TaskProcessInfoForListVikingdbTaskOutput  | 任务处理信息，见下 |

* taskType 类型包括

| data_import | 数据导入任务 |
| --- | --- |
| data_export | 数据导出任务 |
| filter_update | 数据过滤更新任务 |
| filter_delete | 数据过滤删除任务 |

* taskStatus 任务状态包括

| init | queued | running | done | fail |
| --- | --- | --- | --- | --- |
| 初始化中 | 排队中 | 执行中 | 完成 | 失败 |

* TaskProcessInfoForListVikingdbTaskOutput 包括

| **字段** | **类型** | **说明** |
| --- | --- | --- |
| taskProgress | string | 任务进度 例如50% |
| errorMessage | string | 任务错误信息 |
| sampleData | List<SampleDataForGetVikingdbTaskOutput>  | 采样5条数据用于展示 |
| sampleTimestamp | Integer | 采样的时间戳，后写入的数据不会被处理 |
| scanDataCount | Integer | 当前扫描数据量 |
| totalDataCount | Integer | collection 数据总条数(预估） |
| totalFilterCount | Integer | 已经过滤出的数据 |
# 示例
```Java
package org.example.newsubproduct.console.task;

import com.volcengine.ApiClient;
import com.volcengine.ApiException;
import com.volcengine.sign.Credentials;
import com.volcengine.vikingdb.VikingdbApi;
import com.volcengine.vikingdb.model.*;

public class ListVikingdbTask {
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

        ListVikingdbTaskRequest request = new ListVikingdbTaskRequest()
                .collectionName("test_collection_for_sdk_with_vector")
                .taskStatus(ListVikingdbTaskRequest.TaskStatusEnum.RUNNING)
                .taskType(ListVikingdbTaskRequest.TaskTypeEnum.DATA_IMPORT);

        try {
            ListVikingdbTaskResponse response = api.listVikingdbTask(request);
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
