# 接口概述
根据用户账户与指定项目，获取该用户所属的所有记忆库列表。返回每个记忆库的基本信息，包括名称、描述、内置/自定义事件类型与画像类型，以及创建时间和更新时间。
# **请求接口**
| **URL** | /api/memory/collection/list | 统一资源标识符 |
| --- | --- | --- |
| **请求方法** | POST | 客户端对记忆库服务器请求的操作类型 |
| **请求头** | Content-Type: application/json | 请求消息类型 |
|  | Authorization: HMAC-SHA256 *** | 基于AK/SK生成的签名信息 |
# 请求参数
| **参数名** | **类型** | **是否必填** | **描述** |
| --- | --- | --- | --- |
| ProjectName | String | 否 | 项目名称。默认为全部项目。 |
# 响应消息
| **参数名** | **类型** | **参数描述** |
| --- | --- | --- |
| ResponseMetadata | Object | 响应元数据信息。 |
| * Region | String | 服务区域，例如"cn-beijing"。 |
| * RequestId | String | 请求唯一标识符 |
| * Service | String | 服务名称，如"knowledge_base_server"。 |
| * Version | String | API版本号。 |
| Result | Object | 记忆库的详细配置信息。 |
| * CollectionStatus | String | 记忆库状态。 |
| * CollectionType | String | 记忆库类型，标准版/旗舰版。 |
| * CollectionModalType | String | 记忆库的模态类型，纯文本/多模态。 |
| * CreateAt | String | 记忆库创建时间，例如"2025-06-03T06:35:32"。 |
| * CreatedBy | String | 记忆库创建者。 |
| * DescMsg | String | 记忆库描述信息，例如"用于记录和分析学生英语学习过程的记忆库"。 |
| * Name | String | 记忆库名称，例如"english_learning_memory"。 |
| * PipelineConfig | Object | 管道配置信息。 |
| * -TtlRelative | Integer | 记忆库TTL配置 |
| * -CpuQuota | Int | 消耗资源 |
| * -LlmExtractConfig |  |  |
|    * -BuiltinProfileTypes | Array of String | 内置画像类型列表。 |
|    * -BuiltinEventTypes | Array of String | 内置事件类型列表。 |
|    * -CustomProfileTypeSchemas | Array of ProfileTypeSchema | 用户自定义的画像类型模式列表。 |
|    * --AssociatedEventTypes | Array of String | 与此画像类型相关联的事件类型名称列表，例如["english_study"]。 |
|    * --Description | String | 画像类型的详细描述，例如"用于追踪学生在特定英语知识点上的学习进展"。 |
|    * --ProfileType | String | 画像类型的唯一名称，例如"english_knowledge_point"。 |
|    * --EnableAssistantIsolation  <br>  <br>  | Boolean  | 画像是否按照 assistant_id 隔离。默认为 True，即隔离。 |
|    * --Properties | Array of ProfileProperty | 构成此画像类型的属性列表。 |
|    * ---AggregateExpression | Object | 聚合表达式配置，定义此属性如何从关联的事件中聚合计算而来。 |
|    * ---EventPropertyName | String | 参与聚合的事件类型中的属性名称，例如"rating_score"。 |
|    * ----EventType | String | 参与聚合的事件类型名称，例如"english_study"。 |
|    * ----Op | String | 聚合操作符，例如"MAX"、"SUM"、"COUNT"。 |
|    * ---Description | String | 属性的详细描述，例如"知识点的唯一主键ID"。 |
|    * ---IsPrimaryKey | Boolean | 是否为画像的主键，例如true。 |
|    * ---PropertyName | String | 属性名称，例如"id"、"knowledge_point_name"。 |
|    * ---PropertyValueType | String | 属性值的类型，例如"int64"、"string"、"list"。 |
|    * --Role | String | 角色类型，例如"user"。 |
|    * --Version | String | 画像模式版本号，例如"1"。 |
|    * -CustomEventTypeSchemas | Array of EventTypeSchema | 用户自定义的事件类型模式列表。 |
|    * --Description | String | 事件类型的详细描述，例如"记录一次英语学习会话中助教与学生的问答及评分"。 |
|    * --EventType | String | 事件类型的唯一名称，例如"english_study"。 |
|    * --CustomWeightExpression | String | 事件权重表达式。 |
|    * --HasMultiEvent | Boolean | 是否支持多事件，例如true。 |
|    * --OriginalMessagePreserveStrategy | String | 原始消息保存策略，例如"ranges"。 |
|    * --Properties | Array of EventProperty | 构成此事件类型的属性列表。 |
|    * ---Description | String | 属性的详细描述，例如"当前对话涉及的知识点名称"。 |
|    * ---PropertyName | String | 属性名称，例如"knowledge_point_name"、"question"、"answer"。 |
|    * ---PropertyValueType | String | 属性值的类型，例如"string"、"float32"。 |
| * Project | String | 项目名称，例如"default"。 |
| * ResourceId | String | 资源唯一标识符。 |
| * UpdatedAt | String | 最后更新时间，例如"2025-06-03T06:35:32"。 |
| * EventCount | Int | 当前collection事件记忆数量 |
| * ProfileCount | Int | 当前collection画像记忆数量 |
| TotalNum | Int | 项目中记忆库的数量 |
# 示例代码
## Python 代码
```Python
import requests
import json
from volcengine.base.Request import Request
from volcengine.Credentials import Credentials
from volcengine.auth.SignerV4 import SignerV4


AK = "Your AK" 
SK = "Your SK" 
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

path = "/api/memory/collection/list"
payload = {
    "project_name": "default"   
}

rsp = internal_request("POST", path, payload)
print(rsp.json())
```

