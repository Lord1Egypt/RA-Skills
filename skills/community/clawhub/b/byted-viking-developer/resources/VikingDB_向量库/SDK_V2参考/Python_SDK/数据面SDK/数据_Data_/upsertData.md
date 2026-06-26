# 概述
接口用于在指定的数据集 Collection 内写入数据。指定写入的数据是一个map，允许单次插入一条数据或者多条数据，单次最多可插入100条数据。如提供的主键已存在，则更新对应的数据；否则，插入新的数据。
# 请求体参数
| 名称 | 类型 | 描述 | 必选 |
| --- | --- | --- | --- |
| collection_name | str | Collection 的名称，与 resource_id 二选一。 | 二选一 |
| resource_id | str | Collection 的资源 ID。 |  |
| data | List[Dict[str, Any]] | 待写入的数据列表，单次最多100条，每条都需包含主键字段。 | 是 |
| ttl | int | 数据的生存时间，单位为秒，到期后系统自动删除。 | 否 |
| async_write | bool | 对应 API 字段 `async`，开启后以异步方式落库以提升批量吞吐。 | 否 |
# data参数字段值格式
注意：数据插入时主键不能为0

| 字段类型 | 格式 | 说明 |
| --- | --- | --- |
| int64 | 整型数值 | 整数 |
| float32 | 浮点数值 | 浮点数 |
| string | 字符串 | 字符串。内容限制256byte |
| bool | true/false | 布尔类型 |
| list<string> | 字符串数组 | 字符串数组 |
| list<int64> | 整型数组 | 整数数组 |
| vector | * 向量（浮点数数组） <br> * float32/float64压缩为bytes后的base64编码 | 稠密向量 <br>  |
| sparse_vector <br>  | 输入格式的字典列表，来表征稀疏稀疏向量的非零位下标及其对应的值, 其中 token_id 是 string 类型, token_weight 是float 类型 | 稀疏向量 <br>  |
| text | 字符串 | 若为向量化字段，则值不能为空。（若否，可以为空） |
| image | Object | 若为向量化字段，则值不能为空。（若否，可以为空） <br>  <br> * 图片tos链接 `tos://{bucket}/{object}` <br> * http/https格式链接 |
| video | Object | { <br> "value": `tos://{bucket}/{object}`，http/https格式url链接，该字段必填 <br> "fps": 0.2 （取值0.2-5，选填） <br> } |
| date_time | string | 分钟级别： <br> `yyyy-MM-ddTHH:mmZ`或`yyyy-MM-ddTHH:mm±HH:mm` <br> 秒级别： <br> `yyyy-MM-ddTHH:mm:ssZ`或`yyyy-MM-ddTHH:mm:ss±HH:mm` <br> 毫秒级别： <br> `yyyy-MM-ddTHH:mm:ss.SSSZ`或`yyyy-MM-ddTHH:mm:ss.SSS±HH:mm` <br> 例如："2025-08-12T11:33:56+08:00" |
| geoPoint | string | 地理坐标`longitude,latitude`，其中`longitude`取值(-180,180)，`latitude`取值(-90,90) <br> 例如："116.408108,39.915023" |
## 创建时间类型字段(date_time)
只能填写以下格式的其中一种，全部遵循RFC3339标准（https://datatracker.ietf.org/doc/html/rfc3339）
例如："2025-08-12T12:34:56+08:00"
|  | 格式(string) | 示例 | 说明 |
| --- | --- | --- | --- |
| 分钟级别 | `yyyy-MM-ddTHH:mmZ`（utc时间）或 <br> `yyyy-MM-ddTHH:mm±HH:mm`（指定时区） | * `2025-08-12T04:34Z` <br> * `2025-08-12T12:34+08:00` <br>  <br>  | 左侧示例都会解析为北京时间`2025-08-12`的`12:34:00`。 <br>  |
| 秒级别 | `yyyy-MM-ddTHH:mm:ssZ`（utc时间）或 <br> `yyyy-MM-ddTHH:mm:ss±HH:mm`（指定时区） <br>  | * `2025-08-12T04:34:56Z` <br> * `2025-08-12T12:34:56+08:00` <br>  <br>  | 左侧示例都会解析为北京时间`2025-08-12`的`12:34:56`。 <br>  <br>  |
| 毫秒级别 | `yyyy-MM-ddTHH:mm:ss.SSSZ`（utc时间）或 <br> `yyyy-MM-ddTHH:mm:ss.SSS±HH:mm`（带时区） | * `2025-08-12T04:34:56.147Z` <br> * `2025-08-12T12:34:56.147+08:00` <br>  <br>  <br>  | 左侧示例都会解析为北京时间`2025-08-12`的`12:34:56.147`秒。 <br>  |
# 返回参数
响应体包含公共参数（见下方“响应体公共参数介绍”）。其中 `result` 字段类型为 UpsertDataResult：

* UpsertDataResult

| 名称 | 类型 | 描述 |
| --- | --- | --- |
| token_usage | Dict[str, Any] | 本次写入涉及的 token 消耗，字段与计量策略相关。 |
## 响应体公共参数介绍
| 参数名 | 类型 | 说明 |
| --- | --- | --- |
| request_id | string | 请求 ID。 |
| code | string | 操作状态码。成功为`Success`，否则为错误码短语。 |
| message | string | 执行信息。成功则为 `The API call was executed successfully.`，否则为错误信息。 |
| result | map | 操作结果。若无需返回数据，则 `result = null`。 |
# **请求示例代码**
```python
import os
import time

from vikingdb import IAM
from vikingdb.vector import UpsertDataRequest, VikingVector

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

payload = {
    "title": "Python upsert demo",
    "score": 42.5,
    "text": "示例负载，省略其余业务字段",
}
request = UpsertDataRequest(
    data=[payload],
    async_write=False,
)
response = collection_client.upsert(request)
print(f"request_id={response.request_id}")
if response.result:
    print(response.result.token_usage)
```


