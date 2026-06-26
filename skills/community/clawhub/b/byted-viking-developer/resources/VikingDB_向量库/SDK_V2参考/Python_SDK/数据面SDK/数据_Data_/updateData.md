# 概述
updateData 用于为已存在数据的部分字段进行更新。支持 text、标量字段、vector 字段的更新。

# **请求参数**
| 名称 | 类型 | 描述 | 必选 |
| --- | --- | --- | --- |
| collection_name | str | Collection 的名称，与 resource_id 二选一。 | 二选一 |
| resource_id | str | Collection 的资源 ID。 |  |
| data | List[Dict[str, Any]] | 要更新的数据列表，单次最多100条，需包含主键字段及待修改字段。 | 是 |
| ttl | int | 更新后新的生存时间，单位为秒。 | 否 |
| ignore_unknown_fields | bool | 为 True 时忽略未在 schema 中声明的字段，默认校验所有字段。 | 否 |
# 返回参数
响应体包含公共参数（见下方“响应体公共参数介绍”）。其中 `result` 字段类型为 UpdateDataResult：

* UpdateDataResult

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| token_usage | Dict[str, Any] | 本次更新消耗的 token 统计。 |
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
from vikingdb.vector import UpdateDataRequest, VikingVector

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

ID = "2532745373549703702"
request = UpdateDataRequest(
    data=[{"__AUTO_ID__": ID, "score": 47.0, "text": "updated"}], # get ID from console or searchByRandom API
    ignore_unknown_fields=True,
)
response = collection_client.update(request)
print(f"request_id={response.request_id}")
if response.result:
    print(response.result.token_usage)
```



