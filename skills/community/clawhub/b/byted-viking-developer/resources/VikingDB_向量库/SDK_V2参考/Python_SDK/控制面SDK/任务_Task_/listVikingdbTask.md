# 概述
获取多个task的信息，最多一次性展示20条
# 方法定义
Python SDK 通过 `VIKINGDBApi().list_vikingdb_task(request)` 调用，`request` 类型为 `volcenginesdkvikingdb.ListVikingdbTaskRequest`。
# 请求参数
| **参数** | **类型** | **是否必选** | **描述** |
| --- | --- | --- | --- |
| project_name | str | 否 | 项目名称，对应 API 字段 `ProjectName`。 |
| collection_name | str | 2选1 | Collection 名称，对应 API 字段 `CollectionName`。 |
| resource_id | str |  | Collection 资源 ID，对应 API 字段 `ResourceId`。 |
| task_status | str | 是 | 任务状态，对应 API 字段 `TaskStatus`，取值：`init`/`queued`/`running`/`done`/`fail`/`confirm`/`confirmed`。 |
| task_type | str | 是 | 任务类型，对应 API 字段 `TaskType`，可为 `data_import`、`data_export`、`filter_update`、`filter_delete`。 |
| page_number | int | 否 | 页码，对应 API 字段 `PageNumber`，需 ≥0。 |
| page_size | int | 否 | 分页大小，对应 API 字段 `PageSize`，范围 1~100。 |
# 返回参数
成功返回 `ListVikingdbTaskResponse`，包含分页信息与任务列表：
| **参数** | **类型** | **描述** |
| --- | --- | --- |
| tasks | list[TaskForListVikingdbTaskOutput] | 任务列表，每个元素对应一个任务，字段见下表。 |
| page_number | int | 当前页码，对应 API 字段 `PageNumber`。 |
| page_size | int | 分页大小，对应 API 字段 `PageSize`。 |
| total_count | int | 满足条件的任务总数，对应 API 字段 `TotalCount`。 |
tasks 元素字段：
| **字段** | **类型** | **描述** |
| --- | --- | --- |
| task_id | str | 任务 ID，API 字段 `TaskId`。 |
| task_type | str | 任务类型，API 字段 `TaskType`。 |
| task_status | str | 任务状态，API 字段 `TaskStatus`。 |
| create_time | str | 创建时间，API 字段 `CreateTime`。 |
| update_time | str | 更新时间，API 字段 `UpdateTime`。 |
| update_person | str | 最后更新人，API 字段 `UpdatePerson`。 |
| task_config | TaskConfigForListVikingdbTaskOutput | 任务配置，字段见下表。 |
| task_process_info | TaskProcessInfoForListVikingdbTaskOutput | 任务进度信息，字段见下表。 |
task_config 字段说明：
| **字段** | **类型** | **描述** |
| --- | --- | --- |
| collection_name | str | Collection 名称，API 字段 `CollectionName`。 |
| project_name | str | 项目名称，API 字段 `ProjectName`。 |
| resource_id | str | Collection 资源 ID，API 字段 `ResourceId`。 |
| file_type | str | 导入/导出文件格式，API 字段 `FileType`。 |
| filter_conds | list[object] | 过滤条件数组，API 字段 `FilterConds`。 |
| export_all | bool | 是否导出全部数据，API 字段 `ExportAll`。 |
| ignore_error | bool | 是否忽略单条异常，API 字段 `IgnoreError`。 |
| need_confirm | bool | 是否需要人工确认，API 字段 `NeedConfirm`。 |
| tos_path | str | TOS 路径，API 字段 `TosPath`。 |
| use_public | bool | 是否通过公共域访问 TOS，API 字段 `UsePublic`。 |
| update_fields | object | 字段更新配置，API 字段 `UpdateFields`。 |
task_process_info 字段说明：
| **字段** | **类型** | **描述** |
| --- | --- | --- |
| task_progress | str | 任务进度信息，API 字段 `TaskProgress`。 |
| total_data_count | int | 总数据量，API 字段 `TotalDataCount`。 |
| total_filter_count | int | 满足条件的数据量，API 字段 `TotalFilterCount`。 |
| scan_data_count | int | 已扫描数据条数，API 字段 `ScanDataCount`。 |
| sample_timestamp | str | 抽样时间戳，API 字段 `SampleTimestamp`。 |
| sample_data | list[object] | 抽样结果，API 字段 `SampleData`。 |
| error_message | str | 错误信息，API 字段 `ErrorMessage`。 |
# 示例
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

request = vdb.ListVikingdbTaskRequest(
    collection_name="sdk_demo_collection",
    task_status="running",
    task_type="data_export",
    page_number=0,
    page_size=20,
)
response = client.list_vikingdb_task(request)
print("total:", response.total_count)
for task in response.tasks or []:
    print(task.task_id, task.task_status)
```



