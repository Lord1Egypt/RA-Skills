# 概述
按特定条件批量导出Collection中的数据
使用前请先授权 VikingDB 跨服务访问 TOS [去授权](https://console.volcengine.com/iam/service/attach_role/?ServiceName=ml_platform)

# 方法定义
```Java
public CreateVikingdbTaskResponse createVikingdbTask(CreateVikingdbTaskRequest body) throws ApiException
```

# 请求参数
| 参数 | 子参数 | 类型 | 是否必填 | 描述 |
| --- | --- | --- | --- | --- |
| ProjectName |  | String | 否 | 项目名称 |
| CollectionName |  | String | 2选1 | 数据集名称 |
| ResourceId |  | String |  | 数据集资源ID。请求必须指定ResourceId和CollectionName其中之一。 |
| TaskType |  | String | 是 | data_export |
| TaskConfig |  | TaskConfigForCreateVikingdbTaskInput | 是 | 任务具体配置 |
|  | FileType | String | 是 | 文件类型, json 或者 parquet，必填 |
|  | FilterConds | List<Object> | 否 | 过滤条件。使用参考https://www.volcengine.com/docs/84313/1791133 <br>  <br> * 如果不填入FilterConds，则无关ExportAll，一定导出全部数据。 <br> * 如果填入FilterConds： <br>    * 不写Exportall，或Exportall=false，则默认导出满足条件的数据。 <br>    * 写exportall=true，则强制导出全部数据，此时FilterConds不生效。 |
|  | TosPath | string | 是 | TOS 路径，格式 ：{桶名}/{路径}，注意不是域名。必填 |
|  | ExportAll | Boolean | 否 | 是否导出全部数据，此时filter不生效。默认为false |
## 返回参数
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


public class CreateVikingdbTaskDataExport {
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
                .taskType(CreateVikingdbTaskRequest.TaskTypeEnum.DATA_EXPORT)
                .taskConfig(
                        new TaskConfigForCreateVikingdbTaskInput()
                                .fileType(TaskConfigForCreateVikingdbTaskInput.FileTypeEnum.JSON)
                                .tosPath("test-doc1-tos/output.json")
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


## 后续处理
### 1、从 TOS 下载文件
```Python
import tos
DOMAIN = "api-vikingdb.volces.com"
TOS_ENDPOINT = "tos-cn-beijing.ivolces.com"
REGION = "cn-beijing"
AK = "****"
SK = "****"
COLLECTION_NAME = "example"
BUCKET_NAME = "bucket_name"
TOS_DIR = "tos_dir"

def download(client, bucket_name, object_key, local_path):
    file_path = "{}/{}".format(local_path, object_key)
    try:
        client.get_object_to_file(bucket_name, object_key, file_path)
    except tos.exceptions.TosClientError as e:
        # 操作失败，捕获客户端异常，一般情况为非法请求参数或网络异常
        return 'fail with client error, message:{}, cause: {}'.format(e.message, e.cause)
    except tos.exceptions.TosServerError as e:
        return 'fail with server error : {}'.format(e)
    except Exception as e:
        return 'fail with unknown error: {}'.format(e)
    return ''

client = tos.TosClientV2(AK, SK, TOS_ENDPOINT, REGION)
download(client, BUCKET_NAME, TOS_DIR, "./")
```

### 2、解析 parquet 类型数据
```Python
import pyarrow.parquet as pq
def process_parquet(file_path):
    parquet_file = pq.ParquetFile(file_path)

    file_data_count = sum(parquet_file.metadata.row_group(i).num_rows for i in range(parquet_file.num_row_groups))
    schema = parquet_file.schema.to_arrow_schema()
    row_iterator = parquet_file.iter_batches(batch_size=100)
    # 迭代读取数据
    for batch in row_iterator:
        df = batch.to_pandas()
        for index, row in df.iterrows():
            """
            do what you want
            """
            print(row)
    return ''

process_parquet("1.parquet")
```

