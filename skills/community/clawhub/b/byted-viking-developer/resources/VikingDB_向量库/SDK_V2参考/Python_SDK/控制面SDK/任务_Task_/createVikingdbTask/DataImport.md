# 概述
通过 `CreateVikingdbTask` 接口以 `task_type=data_import` 方式将 TOS 中的数据文件导入到指定 Collection，字段需与 Collection Schema 对齐。
使用前请先授权 VikingDB 跨服务访问 TOS [去授权](https://console.volcengine.com/iam/service/attach_role/?ServiceName=vikingdb)
# 方法定义
Python SDK 通过 `VIKINGDBApi().create_vikingdb_task(request)` 调用，`request` 类型为 `volcenginesdkvikingdb.CreateVikingdbTaskRequest`。
# 请求参数
| **参数** | **子参数** | **类型** | **是否必填** | **描述** |
| --- | --- | --- | --- | --- |
| project_name |  | str | 否 | 任务所属项目，对应 API 字段 `ProjectName`，未填时沿用 SDK 默认项目。 |
| collection_name |  | str | 2选1 | Collection 名称，对应 API 字段 `CollectionName`。 |
| resource_id |  | str |  | Collection 资源 ID，对应 API 字段 `ResourceId`。 |
| task_type |  | str | 是 | 任务类型，对应 API 字段 `TaskType`，导入任务固定为 `data_import`。 |
| task_config |  | TaskConfigForCreateVikingdbTaskInput | 是 | 导入任务配置，对应 API 字段 `TaskConfig`。 |
|  | tos_path | str | 是 | 待导入文件所在的 TOS 路径，对应 API 字段 `TosPath`。格式 ：{桶名}/{路径}，注意不是域名。 |
|  | file_type | str | 是 | TOS 文件格式，对应 API 字段 `FileType`，支持 `parquet`、`json`。 |
|  | ignore_error | bool | 否 | 是否忽略单条导入错误，对应 API 字段 `IgnoreError`。 |
# 返回参数
| **参数** | **类型** | **描述** |
| --- | --- | --- |
| task_id | str | 任务 ID，对应 API 字段 `TaskId` |
| message | str | 任务创建结果描述，对应 API 字段 `Message` |
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
    tos_path="your-bucket/path/to/data.parquet",
    ignore_error=False,
)

request = vdb.CreateVikingdbTaskRequest(
    project_name="default",
    collection_name="sdk_demo_collection",
    task_type="data_import",
    task_config=task_cfg,
)
response = client.create_vikingdb_task(request)
print("task id:", response.task_id)
print("message:", response.message)
```


