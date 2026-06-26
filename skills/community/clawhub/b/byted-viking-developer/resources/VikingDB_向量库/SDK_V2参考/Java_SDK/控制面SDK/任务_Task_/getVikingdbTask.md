# 概述
查询指定 task 的详情信息和执行进度
# 方法定义
```Java
public GetVikingdbTaskResponse getVikingdbTask(GetVikingdbTaskRequest body) throws ApiException
```

# 请求参数
| 字段名 | 类型 | 必须 | 说明 |
| --- | --- | --- | --- |
| taskId | string | 是 | 任务ID，在创建任务时返回 |
# 返回参数
| **属性** | **类型** | **说明** |
| --- | --- | --- |
| taskId | string | 任务ID |
| taskType | string | 任务类型 |
| taskStatus | string | 任务状态 |
| updatePerson | string | 任务更新人 |
| updateTime | string | 任务信息更新时间 |
| createTime | string | 任务信息创建时间 |
| taskProcessInfo | TaskProcessInfoForGetVikingdbTaskOutput | 任务处理信息，例如进度等 |

* task_type 类型包括

| data_import | 数据导入任务 |
| --- | --- |
| data_export | 数据导出任务 |
| filter_update | 数据过滤更新任务 |
| filter_delete | 数据过滤删除任务 |

* task_status 任务状态包括

| init | queued | confirm | confirmed | running | done | fail |
| --- | --- | --- | --- | --- | --- | --- |
| 初始化中 | 排队中 | 需要人工确认 | 已确认 | 执行中 | 完成 | 失败 |

* TaskProcessInfoForGetVikingdbTaskOutput 

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
## 请求参数
```Java
package org.example.newsubproduct.console.task;

import com.volcengine.ApiClient;
import com.volcengine.ApiException;
import com.volcengine.sign.Credentials;
import com.volcengine.vikingdb.VikingdbApi;
import com.volcengine.vikingdb.model.*;

public class GetVikingdbTask {
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

        GetVikingdbTaskRequest request = new GetVikingdbTaskRequest()
                .taskId("ff39477b-a7f4-5f63-abd5-1592aaf6dc0c");

        try {
            GetVikingdbTaskResponse response = api.getVikingdbTask(request);
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

