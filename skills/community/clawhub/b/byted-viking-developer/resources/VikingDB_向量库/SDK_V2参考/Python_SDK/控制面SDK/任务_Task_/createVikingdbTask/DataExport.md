# 概述
通过 `CreateVikingdbTask` 接口以 `task_type=data_export` 的方式，将指定 Collection 中的数据批量导出到 TOS。
使用前请先授权 VikingDB 跨服务访问 TOS [去授权](https://console.volcengine.com/iam/service/attach_role/?ServiceName=ml_platform)

# 方法定义
Python SDK 通过 `VIKINGDBApi().create_vikingdb_task(request)` 发起调用，`request` 类型为 `volcenginesdkvikingdb.CreateVikingdbTaskRequest`。
# 请求参数
| **参数** | **子参数** | **类型** | **是否必填** | **描述** |
| --- | --- | --- | --- | --- |
| project_name |  | str | 否 | 任务所属项目，对应 API 字段 `ProjectName`，未填写时默认与 SDK 初始化配置一致（通常为 `default`）。 |
| collection_name |  | str | 2选1 | Collection 名称，对应 API 字段 `CollectionName`，需与任务操作的数据集一致。 |
| resource_id |  | str |  | Collection 资源 ID，对应 API 字段 `ResourceId`。与 `collection_name` 至少提供一个，推荐二者同时传入。 |
| task_type |  | str | 是 | 任务类型，对应 API 字段 `TaskType`。导出任务需设置为 `data_export`，其余可选值还包括 `data_import`、`filter_update`、`filter_delete`。 |
| task_config |  | TaskConfigForCreateVikingdbTaskInput | 是 | 导出任务的详细配置，对应 API 字段 `TaskConfig`。 |
|  | tos_path | str | 是 | TOS 路径，格式 ：{桶名}/{路径}，注意不是域名。对应 API 字段 `TosPath`。 |
|  | file_type | str | 否 | 文件类型，支持 `json` 或 `parquet`。对应 API 字段 `FileType`。默认 `parquet` |
|  | export_all | bool | 否 | 是否导出全部数据，对应 API 字段 `ExportAll`。未填写或为 `False` 时默认导出满足 `filter_conds` 的数据；写 `True` 时强制导出全部数据，此时 `filter_conds` 不生效；若不填入 `filter_conds`，无论 `ExportAll` 是否设置，都会导出全部数据。 |
|  | filter_conds | list[object] | 是 | 过滤条件。使用参考 `https://www.volcengine.com/docs/84313/1419289`，对应 API 字段 `FilterConds`。 |
## 返回参数
| **参数** | **类型** | **描述** |
| --- | --- | --- |
| task_id | str | 任务 ID，对应 API 字段 `TaskId`。 |
| message | str | 接口返回的提示信息，对应 API 字段 `Message`。 |
# 示例
## 请求示例
```python
import os
import volcenginesdkcore
import volcenginesdkvikingdb as vdb
from volcenginesdkvikingdb.api.vikingdb_api import VIKINGDBApi

configuration = volcenginesdkcore.Configuration()
configuration.ak = os.environ["VIKINGDB_AK"]
configuration.sk = os.environ["VIKINGDB_SK"]
configuration.region = os.environ["VIKINGDB_REGION"]
configuration.host = os.environ["VIKINGDB_HOST"]
configuration.scheme = "https"
volcenginesdkcore.Configuration.set_default(configuration)

client = VIKINGDBApi()

task_cfg = vdb.TaskConfigForCreateVikingdbTaskInput(
    file_type="parquet",
    export_all=True,
    tos_path="your-bucket/path/to/export.parquet",
)

request = vdb.CreateVikingdbTaskRequest(
    project_name="default",
    collection_name="sdk_demo_collection",
    task_type="data_export",
    task_config=task_cfg,
)
response = client.create_vikingdb_task(request)
print("task id:", response.task_id)
print("message:", response.message)
```

## 后续处理
### 1、从 TOS 下载文件
```python
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
```

### 2、解析 parquet 类型数据
```python
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


