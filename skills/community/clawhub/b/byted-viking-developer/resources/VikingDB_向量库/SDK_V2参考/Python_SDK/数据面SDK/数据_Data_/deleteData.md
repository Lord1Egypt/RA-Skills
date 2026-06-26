# 概述
deleteData 用于在指定的 Collection 删除数据，根据主键删除单条或多条数据，单次最多允许删除100条数据。

# **请求参数**
| 参数名 | 类型 | 必选 | 备注 |
| --- | --- | --- | --- |
| collection_name | str | 2选1 | Collection 名称，与 resource_id 二选一。 |
| resource_id | str |  | Collection 对应的资源 ID。 |
| ids | List[Any] | 2选1 | 待删除的主键列表（int 或 str），最多100条，非法请求会整体失败。 |
| delete_all | Optional[bool] |  | 对应 API 字段 `del_all`，为 True 时删除 Collection 内全部数据（索引同步会有短暂延迟）。 |
# 返回参数
本接口仅返回公共参数，`result` 恒为 `null`（详见下方“响应体公共参数介绍”）。
## 响应体公共参数介绍
| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| request_id | string | 请求 ID。 |
| code | string | 操作状态码。成功为`Success`，否则为错误码短语。 |
| message | string | 执行信息。成功则为 `The API call was executed successfully.`。 |
| result | map | 操作结果。若无需返回数据，则 `result = null`。 |
# 示例
## 请求参数
```python
import os

from vikingdb import IAM
from vikingdb.vector import DeleteDataRequest, VikingVector

auth = IAM(
    ak=os.environ["VIKINGDB_AK"],
    sk=os.environ["VIKINGDB_SK"],
)
client = VikingVector(
    host=os.environ["VIKINGDB_HOST"],
    region=os.environ["VIKINGDB_REGION"],
    auth=auth,
    scheme="https",
)

collection_client = client.collection(collection_name=os.environ["VIKINGDB_COLLECTION"])
request = DeleteDataRequest(ids=[2532745373549703702])
response = collection_client.delete(request)
print(f"request_id={response.request_id}")
```



