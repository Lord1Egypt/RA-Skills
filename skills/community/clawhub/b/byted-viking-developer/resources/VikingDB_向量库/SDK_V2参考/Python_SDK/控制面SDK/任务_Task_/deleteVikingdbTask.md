# 概述
删除指定的任务，删除后任务将终止
# 方法定义
Python SDK 通过 `VIKINGDBApi().delete_vikingdb_task(request)` 调用，`request` 类型为 `volcenginesdkvikingdb.DeleteVikingdbTaskRequest`。
# 请求参数
| **参数** | **类型** | **是否必选** | **说明** |
| --- | --- | --- | --- |
| task_id | str | 是 | 任务 ID，对应 API 字段 `TaskId`，可从创建/查询任务接口获取。 |
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

request = vdb.DeleteVikingdbTaskRequest(task_id="t-20240201xxxx")
response = client.delete_vikingdb_task(request)
print(response.message or "delete task finished")
```




