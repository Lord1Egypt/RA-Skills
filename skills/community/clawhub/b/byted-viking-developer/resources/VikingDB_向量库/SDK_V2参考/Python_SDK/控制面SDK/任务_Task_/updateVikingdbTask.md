# 概述
更新指定的任务，当前任务更新只用于**删除**任务的人工确认 环节
# 方法定义
Python SDK 通过 `VIKINGDBApi().update_vikingdb_task(request)` 调用，`request` 类型为 `volcenginesdkvikingdb.UpdateVikingdbTaskRequest`。
# 请求参数
| **参数** | **类型** | **是否必选** | **说明** |
| --- | --- | --- | --- |
| task_id | str | 是 | 任务 ID，对应 API 字段 `TaskId`。 |
| task_status | str | 是 | 新状态，对应 API 字段 `TaskStatus`，目前仅支持设置为 `confirmed` 以确认待删除任务。 |
# 返回参数
| **参数** | **类型** | **描述** |
| --- | --- | --- |
| message | str | 操作结果描述，对应 API 字段 `Message`。 |
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

request = vdb.UpdateVikingdbTaskRequest(
    task_id="t-20240201xxxx",
    task_status="confirmed",
)
response = client.update_vikingdb_task(request)
print(response.message or "task confirmed")
```



