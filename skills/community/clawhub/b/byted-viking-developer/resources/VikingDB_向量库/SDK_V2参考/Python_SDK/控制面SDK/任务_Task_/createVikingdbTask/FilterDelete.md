# 概述
通过 `CreateVikingdbTask` 接口，并将 `task_type` 设为 `filter_delete`，可按条件批量删除 Collection 中的文档。
# 方法定义
Python SDK 通过 `VIKINGDBApi().create_vikingdb_task(request)` 调用，`request` 类型为 `volcenginesdkvikingdb.CreateVikingdbTaskRequest`。
# 请求参数
若要将数据备份至TOS，请先授权 VikingDB 跨服务访问 TOS [去授权](https://console.volcengine.com/iam/service/attach_role/?ServiceName=vikingdb)

| **参数** | **子参数** | **类型** | **是否必填** | **描述** |
| --- | --- | --- | --- | --- |
| project_name |  | str | 否 | 任务所属项目，对应 API 字段 `ProjectName`，默认继承 SDK 配置。 |
| collection_name |  | str | 2选1 | Collection 名称，对应 API 字段 `CollectionName`。 |
| resource_id |  | str |  | Collection 资源 ID，对应 API 字段 `ResourceId`。 |
| task_type |  | str | 是 | 任务类型，对应 API 字段 `TaskType`，本接口固定为 `filter_delete`。 |
| task_config |  | TaskConfigForCreateVikingdbTaskInput | 是 | 删除任务配置，对应 API 字段 `TaskConfig`。 |
|  | tos_path | str | 否 | TOS 路径，格式 ：{桶名}/{路径}，注意不是域名。必填，对应 API 字段 `TosPath`。 |
|  | file_type | str | 否 | 文件类型, json 或者 parquet，必填，对应 API 字段 `FileType`。 |
|  | filter_conds | Map | 是 | 过滤条件。使用参考 `https://www.volcengine.com/docs/84313/1419289`，对应 API 字段 `FilterConds`。 |
|  | need_confirm | bool | 否 | 是否可跳过人工确认环节，默认为 `true`，对应 API 字段 `NeedConfirm`。 |
# 返回参数
| 参数 | 类型 | 描述 |
| --- | --- | --- |
| task_id | str | 任务ID |
| message | string | 操作结果信息 |
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

filter_conditions = [
    { "op": "must", "field": "type", "conds": ["xxx"] },
    { "op": "range", "field": "score", "gt": 5 }
]

task_cfg = vdb.TaskConfigForCreateVikingdbTaskInput(
    filter_conds=filter_conditions,
    need_confirm=True,
)

request = vdb.CreateVikingdbTaskRequest(
    project_name="default",
    collection_name="sdk_demo_collection",
    task_type="filter_delete",
    task_config=task_cfg,
)
response = client.create_vikingdb_task(request)
print("task id:", response.task_id)
print("message:", response.message)
```

## 后续处理
若 `need_confirm=True`，可在控制台确认或通过 `VIKINGDBApi().update_vikingdb_task()` 调用将任务状态更新为 `confirmed`。

