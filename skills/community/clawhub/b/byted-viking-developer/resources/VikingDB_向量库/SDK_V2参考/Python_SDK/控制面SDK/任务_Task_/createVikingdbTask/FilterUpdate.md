# 概述
通过 `CreateVikingdbTask` 接口并设置 `task_type=filter_update`，可按条件批量更新 Collection 中的标量字段（不支持 vector、sparse_vector、text 类型）。
# 方法定义
Python SDK 通过 `VIKINGDBApi().create_vikingdb_task(request)` 调用，`request` 类型为 `volcenginesdkvikingdb.CreateVikingdbTaskRequest`。
# 请求参数
| **参数** | **子参数** | **类型** | **是否必填** | **描述** |
| --- | --- | --- | --- | --- |
| project_name |  | str | 否 | 任务所属项目，对应 API 字段 `ProjectName`。 |
| collection_name |  | str | 2选1 | Collection 名称，对应 API 字段 `CollectionName`。 |
| resource_id |  | str |  | Collection 资源 ID，对应 API 字段 `ResourceId`。 |
| task_type |  | str | 是 | 任务类型，对应 API 字段 `TaskType`，固定为 `filter_update`。 |
| task_config |  | TaskConfigForCreateVikingdbTaskInput | 是 | 更新任务配置，对应 API 字段 `TaskConfig`。 |
|  | filter_conds | list[object] | 是 | 过滤条件。使用参考 `https://www.volcengine.com/docs/84313/1419289`，对应 API 字段 `FilterConds`。 |
|  | update_fields | object | 是 | 需要更新的字段值，必须是标量字段，不支持 vector、sparse_vector、text 类型字段的更新。对应 API 字段 `UpdateFields`。 |
# 返回参数
| **参数** | **类型** | **描述** |
| --- | --- | --- |
| task_id | str | 任务 ID，对应 API 字段 `TaskId`。 |
| message | str | 任务创建结果描述，对应 API 字段 `Message`。 |
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

update_fields = {
    "status": "archived",
    "score": 0.5,
}

task_cfg = vdb.TaskConfigForCreateVikingdbTaskInput(
    filter_conds=[
        { "op": "must", "field": "type", "conds": ["xxx"] },
        { "op": "range", "field": "score", "gt": 5 }
    ],
    update_fields=update_fields,
)

request = vdb.CreateVikingdbTaskRequest(
    project_name="default",
    task_type="filter_update",
    task_config=task_cfg,
)
response = client.create_vikingdb_task(request)
print("task id:", response.task_id)
print("message:", response.message)
```



