# 概述
查询指定 task 的详情信息和执行进度
# 方法定义
Python SDK 通过 `VIKINGDBApi().get_vikingdb_task(request)` 调用，`request` 类型为 `volcenginesdkvikingdb.GetVikingdbTaskRequest`。
# 请求参数
| **参数** | **类型** | **是否必选** | **说明** |
| --- | --- | --- | --- |
| task_id | str | 是 | 任务 ID，对应 API 字段 `TaskId`。 |
# 返回参数
接口返回 `GetVikingdbTaskResponse`，字段如下：
| **参数** | **类型** | **描述** |
| --- | --- | --- |
| task_id | str | 任务 ID，对应 API 字段 `TaskId`。 |
| task_type | str | 任务类型，对应 API 字段 `TaskType`，取值包括 `data_import`、`data_export`、`filter_update`、`filter_delete`。 |
| task_status | str | 任务状态，对应 API 字段 `TaskStatus`，可为 `init`/`queued`/`confirm`/`confirmed`/`running`/`done`/`fail`。 |
| create_time | str | 任务创建时间（RFC3339），对应 API 字段 `CreateTime`。 |
| update_time | str | 最近更新时间，对应 API 字段 `UpdateTime`。 |
| update_person | str | 最后更新人，对应 API 字段 `UpdatePerson`。 |
| task_config | TaskConfigForGetVikingdbTaskOutput | 任务配置详情，对应 API 字段 `TaskConfig`，字段见下表。 |
| task_process_info | TaskProcessInfoForGetVikingdbTaskOutput | 任务进度信息，对应 API 字段 `TaskProcessInfo`，字段见下表。 |
task_config 字段说明：
| **字段** | **类型** | **描述** |
| --- | --- | --- |
| collection_name | str | 任务作用的 Collection，API 字段 `CollectionName`。 |
| project_name | str | 项目名称，API 字段 `ProjectName`。 |
| resource_id | str | Collection 资源 ID，API 字段 `ResourceId`。 |
| file_type | str | 导入/导出文件格式，API 字段 `FileType`。 |
| filter_conds | list[object] | 任务过滤条件数组，API 字段 `FilterConds`。 |
| export_all | bool | 是否导出所有数据，仅 data_export 任务生效，API 字段 `ExportAll`。 |
| ignore_error | bool | 是否忽略单条错误，API 字段 `IgnoreError`。 |
| need_confirm | bool | 是否需要人工确认，API 字段 `NeedConfirm`。 |
| tos_path | str | TOS 路径，API 字段 `TosPath`。 |
| use_public | bool | 是否通过公共域访问 TOS，API 字段 `UsePublic`。 |
| update_fields | object | 字段更新配置，API 字段 `UpdateFields`（filter_update 任务使用）。 |
task_process_info 字段说明：
| **字段** | **类型** | **描述** |
| --- | --- | --- |
| task_progress | str | 任务进度描述，API 字段 `TaskProgress`。 |
| total_data_count | int | 总数据量，API 字段 `TotalDataCount`。 |
| total_filter_count | int | 符合过滤条件的数据量，API 字段 `TotalFilterCount`。 |
| scan_data_count | int | 已扫描数据条数，API 字段 `ScanDataCount`。 |
| sample_timestamp | str | 样本时间戳，API 字段 `SampleTimestamp`。 |
| sample_data | list[object] | 抽样数据，API 字段 `SampleData`。 |
| error_message | str | 错误信息，API 字段 `ErrorMessage`。 |
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

request = vdb.GetVikingdbTaskRequest(task_id="t-20240201xxxx")
response = client.get_vikingdb_task(request)
print("task:", response.task_id, response.task_status)
if response.task_config:
    print("collection:", response.task_config.collection_name)
if response.task_process_info:
    print("progress:", response.task_process_info.task_progress)
```




