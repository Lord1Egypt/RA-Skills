# 接口概述
用于更新已有记忆库的配置信息，包括记忆库的描述、自定义事件类型、自定义画像类型等内容。请注意，该接口采用全量替换策略，请求中提供的字段将覆盖原有配置，而非在原配置基础上增量修改。未包含在请求体中的配置项将被清空或重置。更新仅针对记忆库结构，之前已经添加的数据不受影响，依然可以正常检索。
# **请求接口**
| **URL** | /api/memory/collection/update | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对记忆库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 基于AK/SK生成的签名信息 |
# 请求参数
更新记忆库时，必须带上全部配置，否则会被覆盖。

* CollectionType, CollectionModalType, EventType, ProfileType, EnableAssistantIsolation不可编辑

| **参数名** | **类型** | **是否必须** | **描述** |
| --- | --- | --- | --- |
| CollectionName | String | 否 | 要更新的记忆库的唯一名称。 |
| ProjectName | String | 否 | 项目名称。默认为 default。 |
| ResourceId | String | 否 | 资源 ID。唯一标识符。 |
| Description | String | 否 | 记忆库的描述信息，最多 10000 个字符。 |
| TtlRelative | Integer | 否 | 事件记忆的过期时间，单位为秒。不传则默认永不过期。为保证记忆的完整性，建议不要设置过低的值。范围: (0, 315576000] |
| BuiltinEventTypes | Array of String | 否 | 新的内置事件类型名称列表。提供此字段会覆盖现有的内置事件类型。 |
| BuiltinProfileTypes | Array of String | 否 | 新的内置画像类型名称列表。提供此字段会覆盖现有的内置画像类型。 |
| CustomEventTypeSchemas | Array of EventTypeSchema | 否 | 新的自定义事件类型模式列表。提供此字段会覆盖现有的自定义事件类型。 |
| CustomProfileTypeSchemas | Array of ProfileTypeSchema | 否 | 新的自定义画像类型模式列表。提供此字段会覆盖现有的自定义画像类型。 |
| CpuQuota | Integer | 否 | 创建时默认为1核，可支撑100qps。范围[1, 100]。 |
| Tags | Array of Tag | 否 | 标签，可用于资源管理和分账。 |
| * Key | String | 是 | 标签的键。 |
| * Value | String | 是 | 标签的值。 |
# 响应消息
操作成功时，HTTP状态码为200。
| **字段** | **类型** | **描述** |
| --- | --- | --- |
| ResponseMetadata | Object | 响应元数据信息。 |
| * Region | String | 服务区域，例如"cn-beijing"。 |
| * RequestId | String | 请求唯一标识符。 |
| * Service | String | 服务名称，如"knowledge_base_server"。 |
| * Version | String | API版本号。 |
# 示例代码
## **Python请求**
```Python
import requests
import json
from volcengine.base.Request import Request
from volcengine.Credentials import Credentials
from volcengine.auth.SignerV4 import SignerV4

AK = "your AK" 
SK = "your SK" 
Domain = "api-knowledgebase.mlp.cn-beijing.volces.com"

def prepare_request(method, path, ak, sk, data=None):
  r = Request()
  r.set_shema("http")
  r.set_method(method)
  r.set_host(Domain)
  r.set_path(path)

  if data is not None:
    r.set_body(json.dumps(data))
  credentials = Credentials(ak, sk, 'air', 'cn-north-1')
  SignerV4.sign(r, credentials)
  return r

def internal_request(method, api, payload, params=None):
  req = prepare_request(
                        method = method,
                        path = api,
                        ak = AK,
                        sk = SK,
                        data = payload)


  r = requests.request(method=req.method,
          url="{}://{}{}".format(req.schema, req.host, req.path),
          headers=req.headers,
          data=req.body,
          params=params,
      )
  return r

path = "/api/memory/collection/update"
payload = {
  "CollectionName": "my_first_memory_collection",
  "Description": "用于记录和分析学生英语学习过程的记忆库",
  "CustomEventTypeSchemas": [
    {
      "EventType": "english_study",
      "Description": "记录一次英语学习会话中助教与学生的问答及评分",
      "Properties": [
        {
          "PropertyName": "knowledge_point_name",
          "PropertyValueType": "string",
          "Description": "当前对话涉及的知识点名称",
        },
        {
          "PropertyName": "question",
          "PropertyValueType": "string",
          "Description": "助教提出的问题",
        },
        {
          "PropertyName": "answer",
          "PropertyValueType": "string",
          "Description": "学生的回答",
        },
        {
          "PropertyName": "rating_score",
          "PropertyValueType": "int64",
          "Description": "对学生回答的数值评分",
        },
        {
          "PropertyName": "fluency_score",
          "PropertyValueType": "int64",
          "Description": "口语流利度评分 (1-5)",
        }
      ],
      "Version": "2"
    }
    # 如果还有其他自定义事件类型，且不想改变它们，需要在这里一并列出它们的当前定义
  ]
  # CustomEntityTypeSchemas, BuiltinEventTypes, BuiltinEntityTypes 如果不需要改变，则不传递或传递其当前值
}
rsp = internal_request("POST", path, payload)
print(rsp.json())
```

